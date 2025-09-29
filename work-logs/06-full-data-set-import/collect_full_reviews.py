# =================================================================================================
# Script:        collect_full_reviews.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       1.0
# Created:       2025-09-01
# Last Updated:  2025-09-28
#
# Purpose:
#   Independent, resumable runner to harvest review summaries across the catalog. Designed to run
#   in parallel with appdetails using a separate API key and separate state files.
#
# Inputs:
#   - ENV: STEAM_API_KEY_2 (required), API_DELAY_SECONDS, API_SAVE_BATCH_SIZE, API_MAX_RETRIES (optional)
# Outputs:
#   - data_reviews/reviews_full_batch_*.json + state/* + logs/*
#
# Operational Profile:
#   - Runtime Context: {python: 3.9+}
#   - Idempotency: {safe_rerun: true}
#   - Failure Modes: {rate_limit_429, http_4xx|5xx, network_error, empty_body}
#
# Data Lineage & Provenance:
#   SOURCE_OF_TRUTH: https://store.steampowered.com/appreviews/<appid>?json=1
#   READS: ["applist.apps[*]", "appreviews.<appid>"]
#   WRITES: ["data_reviews/reviews_full_batch_*.json", "state/processed_reviews_full_appids.txt"]
#
# Security & Compliance:
#   - Separate key helps isolate quotas and reduce correlated throttling. No PII expected.
#
# Change Log:
#   - 2025-09-28  Standardized header + dual-audience comments; behavior unchanged.
# =================================================================================================

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

# --- Directory & logging setup --------------------------------------------------------------------
CWD = Path.cwd()
(CWD / "state").mkdir(exist_ok=True)
(CWD / "data_reviews").mkdir(exist_ok=True)
(CWD / "logs").mkdir(exist_ok=True)

log_filename = CWD / f"logs/review_collection_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(log_filename)]
)

# --- Keys & knobs ---------------------------------------------------------------------------------
load_dotenv()
STEAM_API_KEY_2 = os.getenv("STEAM_API_KEY_2")
if not STEAM_API_KEY_2:
    logging.error("FATAL: STEAM_API_KEY_2 environment variable not set. This script requires a secondary key.")
    sys.exit(1)

API_DELAY_SECONDS = float(os.getenv('API_DELAY_SECONDS', 1.5))
API_SAVE_BATCH_SIZE = int(os.getenv('API_SAVE_BATCH_SIZE', 500))
API_MAX_RETRIES = int(os.getenv('API_MAX_RETRIES', 3))
API_USER_AGENT = 'SteamDataPlatform/2.3-ReviewCollector (https://github.com/vintagedon/steam-dataset-2025)'

# --- Review state management ----------------------------------------------------------------------
class ReviewStateManager:
    """Separate state to avoid interference with appdetails collector; enables parallel execution."""
    def __init__(self, state_dir: Path):
        self.app_list_file = state_dir / "app_list_for_reviews.json"
        self.processed_ids_file = state_dir / "processed_reviews_full_appids.txt"

    def load_app_list(self, session: requests.Session) -> List[Dict[str, Any]]:
        """Fetch/cache applist for review scope; keeps runs deterministic."""
        if self.app_list_file.exists():
            logging.info(f"Loading app list from cache: {self.app_list_file.name}")
            with self.app_list_file.open('r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logging.warning("Review app list cache not found. Fetching from Steam API...")
            url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
            try:
                response = session.get(url, timeout=60)
                response.raise_for_status()
                data = response.json()
                apps = data.get('applist', {}).get('apps', [])
                with self.app_list_file.open('w', encoding='utf-8') as f:
                    json.dump(apps, f)
                logging.info(f"Successfully fetched and cached {len(apps):,} applications for review collection.")
                return apps
            except requests.RequestException as e:
                logging.error(f"FATAL: Could not fetch initial app list for reviews: {e}")
                sys.exit(1)

    def load_processed_ids(self) -> Set[int]:
        """Set of already processed ids; ensures forward-only progress across restarts."""
        if not self.processed_ids_file.exists():
            return set()
        with self.processed_ids_file.open('r', encoding='utf-8') as f:
            ids = {int(line.strip()) for line in f if line.strip().isdigit()}
        logging.info(f"Loaded {len(ids):,} previously processed review AppIDs from state file.")
        return ids

    def append_processed_id(self, appid: int):
        """Append as we go (append-only) for crash safety + resumability."""
        with self.processed_ids_file.open('a', encoding='utf-8') as f:
            f.write(f"{appid}\n")

# --- API client (reviews) -------------------------------------------------------------------------
class ReviewAPIClient:
    """Thin wrapper around appreviews endpoint with bounded retries + jitter."""
    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': API_USER_AGENT})

    def get_app_reviews(self, appid: int) -> Optional[Dict[str, Any]]:
        """Fetch reviews JSON; returns None if empty/invalid/not permitted."""
        url = f"https://store.steampowered.com/appreviews/{appid}?json=1&num_per_page=100&language=all"
        for attempt in range(API_MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=20)
                if response.status_code == 200:
                    data = response.json()
                    return data if data and data.get('success') == 1 else None
                elif response.status_code in [404, 403]: return None
                elif response.status_code == 429: logging.warning(f"Rate limited (429) on AppID {appid}. Retrying...")
                else: logging.warning(f"Server error (HTTP {response.status_code}) on AppID {appid}. Retrying...")
            except requests.exceptions.RequestException as e:
                logging.error(f"Network error for AppID {appid}: {e}. Retrying...")
            time.sleep((5 ** attempt) + (random.random() * 0.5))
        logging.error(f"PERMANENT FAILURE for review on AppID {appid} after {API_MAX_RETRIES} retries.")
        return None

# --- Orchestrator ---------------------------------------------------------------------------------
class FullReviewCollector:
    """Sequentially walk applist; save batches of review payloads; update state each id."""
    def __init__(self):
        self.state_manager = ReviewStateManager(CWD / "state")
        self.api_client = ReviewAPIClient(api_key=STEAM_API_KEY_2)
        self.output_dir = CWD / "data_reviews"

    def run_collection(self):
        logging.info("🚀 Starting full-scale review data collection run.")
        
        full_app_list = self.state_manager.load_app_list(self.api_client.session)
        already_processed = self.state_manager.load_processed_ids()
        
        appids_to_fetch = [app['appid'] for app in full_app_list if app['appid'] not in already_processed]
        if not appids_to_fetch:
            logging.info("🎉 Full review collection is already complete.")
            return
            
        logging.info(f"Targeting {len(appids_to_fetch):,} applications for review collection.")
        
        batch: List[Dict[str, Any]] = []
        batch_num = (len(list(self.output_dir.glob("reviews_full_batch_*.json")))) + 1
        
        for appid in (pbar := tqdm(appids_to_fetch, desc="Collecting reviews")):
            pbar.set_postfix_str(f"Current AppID: {appid}")
            
            review_data = self.api_client.get_app_reviews(appid)
            
            if review_data and review_data.get('reviews'):
                batch.append({"appid": appid, "reviews": review_data})
            
            self.state_manager.append_processed_id(appid)
            
            if len(batch) >= API_SAVE_BATCH_SIZE:
                self._save_batch(batch, batch_num)
                batch = []
                batch_num += 1

            time.sleep(API_DELAY_SECONDS)

        if batch:
            self._save_batch(batch, batch_num)
            
        logging.info("🎉 Full review collection complete!")

    def _save_batch(self, batch: List[Dict[str, Any]], batch_num: int):
        """Persist current batch; append-only to simplify recovery and auditing."""
        batch_filename = self.output_dir / f"reviews_full_batch_{batch_num:05d}.json"
        logging.info(f"Saving review batch {batch_num} ({len(batch)} records) to {batch_filename.name}...")
        try:
            with batch_filename.open('w', encoding='utf-8') as f:
                json.dump(batch, f)
        except IOError as e:
            logging.error(f"Could not write batch file {batch_filename.name}: {e}")

if __name__ == "__main__":
    try:
        collector = FullReviewCollector()
        collector.run_collection()
    except KeyboardInterrupt:
        logging.info("\n🛑 User interrupted review collection. Run the script again to resume.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"An unexpected critical error occurred: {e}", exc_info=True)
        sys.exit(1)
