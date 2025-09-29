# =================================================================================================
# Script:        collect_full_dataset.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       1.0
# Created:       2025-08-31
# Last Updated:  2025-09-28
#
# Purpose:
#   Resumable, long-running collector for full Steam appdetails coverage with stateful progress,
#   batched JSON output, and conservative throttling/backoff suitable for unattended runs.
#
# Inputs:
#   - ENV: STEAM_API_KEY (required), API_DELAY_SECONDS, API_SAVE_BATCH_SIZE, API_MAX_RETRIES (optional)
# Outputs:
#   - data/steam_data_batch_*.json + state/* + logs/*
#
# Operational Profile:
#   - Runtime Context: {python: 3.9+}
#   - Idempotency: {safe_rerun: true}  # state files ensure forward progress
#   - Failure Modes: {rate_limit_429, http_4xx|5xx, network_error, empty_body}
#
# Data Lineage & Provenance:
#   SOURCE_OF_TRUTH: https://store.steampowered.com/api/appdetails?appids=<id>
#   READS: ["applist.apps[*]", "appdetails.<appid>"]
#   WRITES: ["data/steam_data_batch_*.json", "state/*.txt|json", "logs/*.log"]
#
# Security & Compliance:
#   - Secrets via .env only. No PII expected.
#
# Change Log:
#   - 2025-09-28  Standardized header + dual-audience comments; behavior unchanged.
# =================================================================================================

import os
import sys
import json
import time
import logging
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Set, Optional

try:
    import requests
    from dotenv import load_dotenv
    from tqdm import tqdm
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

# --- Working directories (resumable contract) -----------------------------------------------------
CWD = Path.cwd()
(CWD / "state").mkdir(exist_ok=True)
(CWD / "data").mkdir(exist_ok=True)
(CWD / "logs").mkdir(exist_ok=True)

# --- Logging to console + rotating file -----------------------------------------------------------
log_filename = CWD / f"logs/collection_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_filename)
    ]
)

# --- Config from environment ----------------------------------------------------------------------
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
if not STEAM_API_KEY:
    logging.error("FATAL: STEAM_API_KEY environment variable not set. Please create a .env file.")
    sys.exit(1)

API_DELAY_SECONDS = float(os.getenv('API_DELAY_SECONDS', 1.5))
API_SAVE_BATCH_SIZE = int(os.getenv('API_SAVE_BATCH_SIZE', 500))
API_MAX_RETRIES = int(os.getenv('API_MAX_RETRIES', 3))
API_USER_AGENT = 'SteamDataPlatform/2.0 (https://github.com/vintagedon/steam-dataset-2025)'

# --- State manager (append-only durability) -------------------------------------------------------
class StateManager:
    """Cache applist; track processed/failed ids to guarantee forward progress across restarts."""
    def __init__(self, state_dir: Path):
        self.app_list_file = state_dir / "app_list.json"
        self.processed_ids_file = state_dir / "processed_appids.txt"
        self.failed_ids_file = state_dir / "failed_appids.txt"

    def load_app_list(self, session: requests.Session) -> List[Dict[str, Any]]:
        """Load cached applist or fetch once; provides deterministic work queue."""
        if self.app_list_file.exists():
            logging.info(f"Loading app list from cache: {self.app_list_file}")
            with self.app_list_file.open('r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logging.warning("App list cache not found. Fetching from Steam API (this happens only once)...")
            url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
            try:
                response = session.get(url, timeout=60)
                response.raise_for_status()
                data = response.json()
                apps = data.get('applist', {}).get('apps', [])
                with self.app_list_file.open('w', encoding='utf-8') as f:
                    json.dump(apps, f)
                logging.info(f"Successfully fetched and cached {len(apps):,} applications.")
                return apps
            except requests.RequestException as e:
                logging.error(f"FATAL: Could not fetch initial app list: {e}")
                sys.exit(1)

    def load_processed_ids(self) -> Set[int]:
        """Union of processed + failed to skip permanently; fast O(1) membership during main loop."""
        processed_ids = set()
        for state_file in [self.processed_ids_file, self.failed_ids_file]:
            if state_file.exists():
                with state_file.open('r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            processed_ids.add(int(line.strip()))
                        except ValueError:
                            continue
        logging.info(f"Loaded {len(processed_ids):,} previously processed AppIDs from state files.")
        return processed_ids

    def append_processed(self, appid: int):
        """Durable write-through on success to minimize rework after crashes."""
        with self.processed_ids_file.open('a', encoding='utf-8') as f:
            f.write(f"{appid}\n")

    def append_failed(self, appid: int):
        """Record permanent failure for transparency + skip logic."""
        with self.failed_ids_file.open('a', encoding='utf-8') as f:
            f.write(f"{appid}\n")

# --- Steam API client (retry + backoff) -----------------------------------------------------------
class SteamAPIClient:
    """Session-scoped client with exponential backoff to be a good API citizen."""
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': API_USER_AGENT})

    def get_app_details(self, appid: int) -> Optional[Dict[str, Any]]:
        """Call appdetails with bounded retries; return parsed node or None on permanent failure."""
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        for attempt in range(API_MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=20)
                if response.status_code == 200:
                    data = response.json()
                    return data.get(str(appid)) if data and str(appid) in data else None
                elif response.status_code in [404, 401, 403]:
                    logging.warning(f"Hard failure for AppID {appid} (HTTP {response.status_code}). Not retrying.")
                    return None
                elif response.status_code == 429:
                    logging.warning(f"Rate limited (HTTP 429). Waiting longer before retry {attempt + 1}/{API_MAX_RETRIES}...")
                else:
                    logging.warning(f"Server error (HTTP {response.status_code}). Retrying ({attempt + 1}/{API_MAX_RETRIES})...")
            except requests.exceptions.RequestException as e:
                logging.error(f"Network error for AppID {appid}: {e}. Retrying ({attempt + 1}/{API_MAX_RETRIES})...")
            # HUMAN: geometric growth with jitter to reduce collision under load.
            time.sleep((5 ** attempt) + (random.random() * 0.5))
        logging.error(f"PERMANENT FAILURE for AppID {appid} after {API_MAX_RETRIES} retries.")
        return None

# --- Orchestrator --------------------------------------------------------------------------------
class DataCollector:
    """Main loop: resolve worklist → fetch → batch to disk → update state; repeat until complete."""
    def __init__(self):
        self.state_manager = StateManager(CWD / "state")
        self.api_client = SteamAPIClient()
        self.data_dir = CWD / "data"

    def run_collection(self):
        logging.info("🚀 Starting full-scale data collection run.")
        
        full_app_list = self.state_manager.load_app_list(self.api_client.session)
        already_processed = self.state_manager.load_processed_ids()
        
        appids_to_fetch = [app['appid'] for app in full_app_list if app['appid'] not in already_processed]
        if not appids_to_fetch:
            logging.info("🎉 No new applications to process. Collection is up to date.")
            return
            
        logging.info(f"Targeting {len(appids_to_fetch):,} new applications for collection.")
        
        batch: List[Dict[str, Any]] = []
        batch_num = (len(list(self.data_dir.glob("*.json")))) + 1
        
        for appid in (pbar := tqdm(appids_to_fetch, desc="Collecting app details")):
            pbar.set_postfix_str(f"Current AppID: {appid}")
            
            details = self.api_client.get_app_details(appid)
            
            if details:
                batch.append(details)
                self.state_manager.append_processed(appid)
            else:
                self.state_manager.append_failed(appid)
            
            if len(batch) >= API_SAVE_BATCH_SIZE:
                self._save_batch(batch, batch_num)
                batch = []
                batch_num += 1

            time.sleep(API_DELAY_SECONDS)

        if batch:
            self._save_batch(batch, batch_num)
            
        logging.info("🎉 Collection complete!")

    def _save_batch(self, batch: List[Dict[str, Any]], batch_num: int):
        """Write batch to JSON; each batch is an append-only artifact for durability."""
        batch_filename = self.data_dir / f"steam_data_batch_{batch_num:05d}.json"
        logging.info(f"Saving batch {batch_num} ({len(batch)} records) to {batch_filename.name}...")
        try:
            with batch_filename.open('w', encoding='utf-8') as f:
                json.dump(batch, f)
        except IOError as e:
            logging.error(f"Could not write batch file {batch_filename.name}: {e}")

if __name__ == "__main__":
    try:
        collector = DataCollector()
        collector.run_collection()
    except KeyboardInterrupt:
        logging.info("\n🛑 User interrupted the process. Run the script again to resume.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"An unexpected critical error occurred: {e}", exc_info=True)
        sys.exit(1)
