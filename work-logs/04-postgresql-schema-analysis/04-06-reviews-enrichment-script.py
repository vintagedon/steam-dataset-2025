# =================================================================================================
# Script:        04-06-reviews-enrichment-script.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       (unchanged; see original in file)
# Created:       (see original)
# Last Updated:  2025-09-29
#
# Purpose:
#   Harvest reviews JSON in batches for offline merge; designed for long runs.
#
# Section Map:
#   1) Imports — dependencies and why they're needed
#   2) Configuration & Setup — env, logging, runtime knobs
#   3) Core Components — classes/functions with high‑level intent
#   4) Orchestration — how the pieces run together
#   5) CLI / Entry — human‑friendly usage and safe defaults
#
# Data Lineage & Provenance (RAG‑friendly):
#   SOURCE_OF_TRUTH: see original script references
#   READS / WRITES:  unchanged
#
# Security & Compliance:
#   - Secrets via .env only (no literals).
#   - PII: none expected.
#
# Change Log (docs‑only):
#   - 2025-09-29  Re‑commented with full dual‑audience inline notes; logic unchanged.
# =================================================================================================

# --- Imports --------------------------------------------------------------------------------------
# Human: split stdlib vs third‑party; fail fast on missing deps for actionable remediation.
# ML:    DEPENDS_ON — infer runtime library set from import graph.
import os
import sys
import json
import time
import random
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Set, Optional

try:
    import requests
    from dotenv import load_dotenv
    from tqdm import tqdm
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install requests python-dotenv tqdm", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Environment Setup ---
CWD = Path.cwd()
(CWD / "state").mkdir(exist_ok=True)
(CWD / "data_reviews").mkdir(exist_ok=True) # Separate output directory for review data
(CWD / "logs").mkdir(exist_ok=True)

log_filename = CWD / f"logs/enrichment_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(log_filename)]
)

# --- Load Primary and Secondary API Keys ---
# --- Configuration & Setup ------------------------------------------------------------------------
# Human: centralize environment + logging so business logic stays testable and clean.
# ML:    CONFIG_KEYS — parse .env to map required/optional runtime knobs.
load_dotenv()
# CRITICAL: This script uses the secondary API key to avoid consuming the primary quota.
STEAM_API_KEY_2 = os.getenv("STEAM_API_KEY_2")
if not STEAM_API_KEY_2:
    logging.error("FATAL: STEAM_API_KEY_2 environment variable not set. This script requires a secondary key.")
    sys.exit(1)

# --- Constants ---
API_DELAY_SECONDS = float(os.getenv('API_DELAY_SECONDS', 1.5)) # Using a conservative delay
API_SAVE_BATCH_SIZE = int(os.getenv('API_SAVE_BATCH_SIZE', 500))
API_MAX_RETRIES = int(os.getenv('API_MAX_RETRIES', 3))
API_USER_AGENT = 'SteamDataPlatform/2.1-Enrichment (https://github.com/vintagedon/steam-dataset-2025)'

# --- State Management ---
class EnrichmentStateManager:
    """Handles loading the source AppID list and managing the state of the enrichment process."""
    def __init__(self, state_dir: Path):
        self.source_ids_file = state_dir / "processed_appids.txt"
        self.processed_reviews_ids_file = state_dir / "processed_reviews_appids.txt"

    def load_source_appids(self) -> List[int]:
        """Loads the master list of appids for which we have appdetails."""
        if not self.source_ids_file.exists():
            logging.error(f"FATAL: Source state file not found: {self.source_ids_file}. Run the main collection script first.")
            sys.exit(1)
        with self.source_ids_file.open('r', encoding='utf-8') as f:
            ids = [int(line.strip()) for line in f if line.strip().isdigit()]
        logging.info(f"Loaded {len(ids):,} source AppIDs to process for reviews.")
        return ids

    def load_processed_review_ids(self) -> Set[int]:
        """Loads the set of AppIDs for which reviews have already been fetched."""
        if not self.processed_reviews_ids_file.exists():
            return set()
        with self.processed_reviews_ids_file.open('r', encoding='utf-8') as f:
            ids = {int(line.strip()) for line in f if line.strip().isdigit()}
        logging.info(f"Loaded {len(ids):,} previously processed review AppIDs.")
        return ids

    def append_processed_id(self, appid: int):
        """Atomically appends a successfully processed AppID to the enrichment state file."""
        with self.processed_reviews_ids_file.open('a', encoding='utf-8') as f:
            f.write(f"{appid}\n")

# --- API Client ---
class ReviewAPIClient:
    """Manages API calls to the 'appreviews' endpoint with session pooling and backoff."""
    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': API_USER_AGENT})
        self.api_key = api_key # This script does not use the key in the URL, but good practice to hold it.

    def get_app_reviews(self, appid: int) -> Optional[Dict[str, Any]]:
        """Fetches review data for an appid with a robust retry mechanism."""
        # The `num_per_page` can be set up to 100. We fetch a large sample.
        url = f"https://store.steampowered.com/appreviews/{appid}?json=1&num_per_page=100&language=all"
        for attempt in range(API_MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=20)
                if response.status_code == 200:
                    data = response.json()
                    # The API returns success=1 on a valid response.
                    return data if data and data.get('success') == 1 else None
                # Handle other statuses similarly to the main collection script
                elif response.status_code in [404, 403]: return None
                elif response.status_code == 429: logging.warning(f"Rate limited (429) on AppID {appid}. Retrying...")
                else: logging.warning(f"Server error (HTTP {response.status_code}) on AppID {appid}. Retrying...")
            
            except requests.exceptions.RequestException as e:
                logging.error(f"Network error for AppID {appid}: {e}. Retrying...")
            
            time.sleep((5 ** attempt) + (random.random() * 0.5))
        
        logging.error(f"PERMANENT FAILURE for review on AppID {appid} after {API_MAX_RETRIES} retries.")
        return None

# --- Main Enrichment Orchestrator ---
class ReviewEnricher:
    """Orchestrates the entire data enrichment pipeline."""
    def __init__(self):
        self.state_manager = EnrichmentStateManager(CWD / "state")
        self.api_client = ReviewAPIClient(api_key=STEAM_API_KEY_2)
        self.output_dir = CWD / "data_reviews"

    def run_enrichment(self):
        """Executes the main enrichment logic."""
        logging.info("🚀 Starting review data enrichment run.")
        
        source_appids = self.state_manager.load_source_appids()
        already_processed = self.state_manager.load_processed_review_ids()
        
        appids_to_fetch = [appid for appid in source_appids if appid not in already_processed]
        if not appids_to_fetch:
            logging.info("🎉 Review data is already up to date with all processed applications.")
            return
            
        logging.info(f"Targeting {len(appids_to_fetch):,} applications for review enrichment.")
        
        batch: List[Dict[str, Any]] = []
        batch_num = (len(list(self.output_dir.glob("*.json")))) + 1
        
        for appid in (pbar := tqdm(appids_to_fetch, desc="Enriching with reviews")):
            pbar.set_postfix_str(f"Current AppID: {appid}")
            
            review_data = self.api_client.get_app_reviews(appid)
            
            # Even if no reviews are found (review_data is None), we mark it as processed
            # to avoid re-checking it in the future.
            if review_data:
                # The output format is critical: we must associate the review data with the appid.
                batch.append({"appid": appid, "review_data": review_data})
            
            self.state_manager.append_processed_id(appid)
            
            if len(batch) >= API_SAVE_BATCH_SIZE:
                self._save_batch(batch, batch_num)
                batch = []
                batch_num += 1

            time.sleep(API_DELAY_SECONDS)

        if batch:
            self._save_batch(batch, batch_num)
            
        logging.info("🎉 Review enrichment complete!")

    def _save_batch(self, batch: List[Dict[str, Any]], batch_num: int):
        """Saves the current in-memory batch to a numbered JSON file."""
        batch_filename = self.output_dir / f"reviews_batch_{batch_num:05d}.json"
        logging.info(f"Saving review batch {batch_num} ({len(batch)} records) to {batch_filename.name}...")
        try:
            with batch_filename.open('w', encoding='utf-8') as f:
                json.dump(batch, f)
        except IOError as e:
            logging.error(f"Could not write batch file {batch_filename.name}: {e}")

# --- Entry Point -----------------------------------------------------------------------------------
# Human: python -m / direct execution path with safe error handling.
# ML:    RUNTIME_START — begin metrics/telemetry if needed.
if __name__ == "__main__":
    try:
        enricher = ReviewEnricher()
        enricher.run_enrichment()
    except KeyboardInterrupt:
        logging.info("\n🛑 User interrupted enrichment. Run the script again to resume.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"An unexpected critical error occurred: {e}", exc_info=True)
        sys.exit(1)