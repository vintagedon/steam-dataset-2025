# =================================================================================================
# Script:        get_steam_data_sample.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       1.3
# Created:       2025-08-31
# Last Updated:  2025-09-28
#
# Purpose:
#   Fetch a target-sized random sample of Steam "game" apps, validating that the store "appdetails"
#   contract is reachable and stable enough for downstream ETL. Results are written as a structured
#   JSON artifact with run metadata for reproducibility.
#
# Inputs:
#   - ENV: STEAM_API_KEY (required), LOG_LEVEL (optional), API_USER_AGENT (optional)
# Outputs:
#   - File: steam_data_<N>_games_<timestamp>.json (sample + run metadata)
#
# Operational Profile:
#   - Runtime Context: {os: linux|win|mac, python: 3.9+}
#   - Idempotency: {safe_rerun: true}  # read-only to external services; writes a new timestamped file
#   - Failure Modes: {network_error, json_decode_error, http_4xx_5xx, restricted_appids}
#
# Data Lineage & Provenance (RAG-friendly):
#   SOURCE_OF_TRUTH:
#     - https://api.steampowered.com/ISteamApps/GetAppList/v2/
#     - https://store.steampowered.com/api/appdetails?appids=<id>
#   READS: ["applist.apps[*]", "appdetails.<appid>"]
#   WRITES: ["steam_data_<N>_games_<timestamp>.json"]
#   BUSINESS_RULES: ["collect only type=='game'", "throttle requests", "periodic checkpoint every 25 apps"]
#
# Security & Compliance:
#   - No secrets in code or logs; API key is sourced from environment only.
#   - PII: none handled; responses are public catalog/metadata.
#
# Usage:
#   python get_steam_data_sample.py --count 50       # direct mode
#   python get_steam_data_sample.py                  # interactive prompt (defaults to 100)
#
# Change Log:
#   - 2025-08-31 v1.0  Initial release based on test script.
#   - 2025-08-31 v1.1  Refactored for robustness and pythonic best practices.
#   - 2025-08-31 v1.2  Hybrid CLI/interactive mode and timestamped filenames.
#   - 2025-08-31 v1.3  Switched to timezone-aware timestamps for forward compatibility.
#   - 2025-09-28 v1.3  (docs) Standardized header + dual-audience comments; no code changes.
# =================================================================================================

# --- Imports --------------------------------------------------------------------------------------
# Human: split imports clarify stdlib vs deps; early ImportError gives actionable guidance.
# ML:    DEPENDS_ON = ["requests", "python-dotenv"]
import os
import sys
import json
import time
import random
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Set, Optional
from json.decoder import JSONDecodeError

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    # Human: fail fast with remediation hint.
    # ML:    FAILURE_MODE = "missing_dependency"
    print("Error: Required libraries 'requests' or 'python-dotenv' are not installed.", file=sys.stderr)
    print("Please install them using: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ------------------------------------------------------------------------
# Human: centralize env + logging so business logic stays clean/testable.
# ML:    CONFIG = {"env": ["STEAM_API_KEY","LOG_LEVEL?","API_USER_AGENT?"]}
load_dotenv()

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO),
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
if not STEAM_API_KEY:
    # Human: explicit; avoids silent 401 loops.
    # ML:    FAILURE_MODE = "missing_secret"
    logging.error("FATAL: STEAM_API_KEY environment variable not set. Please create a .env file or set it manually.")
    sys.exit(1)

# --- Constants ------------------------------------------------------------------------------------
# Human: operational knobs kept in-code for Session 02 stability; can be env-driven in later phases.
# ML:    THROTTLE_SECONDS = 1.5; CANDIDATE_FILTER = "appid > 2000"
BASE_DELAY_SECONDS = 1.5
API_USER_AGENT = 'SteamDataPlatform/1.3 (https://github.com/vintagedon/steam-dataset-2025)'
APPID_FILTER_THRESHOLD = 2000

# --- Main Class -----------------------------------------------------------------------------------
class SteamDataPuller:
    """
    Encapsulates the sampler pipeline:
      1) GET applist (catalog reachability & size),
      2) filter candidate AppIDs,
      3) loop random candidates → appdetails,
      4) accept only type=='game',
      5) periodically checkpoint to JSON, then final save.

    WHY (design):
      - requests.Session(): connection reuse for realistic performance and fewer TLS setups.
      - explicit logging: reproducible telemetry for later phases to calibrate rate limits.
      - separation of concerns: network fetch, decision logic, persistence are distinct.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': API_USER_AGENT})
        self.collected_data: List[Dict[str, Any]] = []
        # Timestamps to calculate total run duration.
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def get_app_list(self) -> List[Dict[str, Any]]:
        """GET applist → validate JSON contract, return [{appid,name}, ...] or []."""
        logging.info("Fetching full Steam application list...")
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            apps = data.get('applist', {}).get('apps', [])
            logging.info(f"Successfully retrieved {len(apps):,} total applications.")
            return apps
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Network error while fetching app list: {e}")
        except JSONDecodeError:
            logging.error("❌ Failed to decode JSON from GetAppList response. The API might be down or returned malformed data.")
        return []

    def get_app_details(self, appid: int) -> Dict[str, Any]:
        """
        GET appdetails for a single appid and normalize to a stable record:
          {appid, success, fetched_at, data?, error?}
        WHY: downstream ETL wants a predictable envelope even on failures/restrictions.
        """
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        base_response = {
            'appid': appid,
            'success': False,
            'fetched_at': datetime.now(timezone.utc).isoformat()
        }
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code == 401:
                # Human: some AppIDs are geo/age/ownership restricted; skip & record.
                # ML:    SOFT_FAILURE = "restricted_401"
                logging.warning(f"   - AppID {appid} is restricted (401 Unauthorized).")
                return {**base_response, 'error': '401 Unauthorized'}

            response.raise_for_status()
            data = response.json()

            app_data = data.get(str(appid), {})
            if app_data.get('success'):
                return {**base_response, 'success': True, 'data': app_data.get('data', {})}
            else:
                # Human: success==False is normal for some IDs; not an error.
                # ML:    SOFT_FAILURE = "not_found_or_unlisted"
                return base_response

        except requests.exceptions.RequestException as e:
            logging.error(f"   - Network error fetching details for {appid}: {e}")
            return {**base_response, 'error': str(e)}
        except JSONDecodeError:
            logging.warning(f"   - Failed to decode JSON for {appid}. The response might be empty or malformed.")
            return {**base_response, 'error': 'JSONDecodeError'}

    def save_data(self, output_file: Path, target_count: int) -> None:
        """
        Persist full run state:
          - metadata: timing, target, counts, redacted key prefix, delay
          - games:    list of per-app records (as collected)
        WHY: provides a durable audit trail + inputs for later profiling/QA.
        """
        run_duration_seconds = (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else None

        output_data = {
            'metadata': {
                'run_start_timestamp_utc': self.start_time.isoformat() if self.start_time else None,
                'run_end_timestamp_utc': self.end_time.isoformat() if self.end_time else None,
                'run_duration_seconds': run_duration_seconds,
                'target_game_count': target_count,
                'total_records_processed': len(self.collected_data),
                'successful_games_found': len([
                    r for r in self.collected_data
                    if r.get('app_details',{}).get('success')
                    and r.get('app_details',{}).get('data', {}).get('type') == 'game'
                ]),
                'api_key_used': self.api_key[:8] + "...",  # Human: provenance without leaking the secret.
                'delay_between_requests': BASE_DELAY_SECONDS
            },
            'games': self.collected_data
        }

        try:
            with output_file.open('w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
        except IOError as e:
            logging.error(f"❌ Could not write to output file {output_file.name}: {e}")

    def run_collection(self, target_game_count: int, output_file: Path) -> None:
        """
        Orchestrate the sampling loop until target is met or candidates are exhausted.
        Human: random selection + skip non-games; periodic checkpoint every 25 processed.
        ML:    LOOP_INVARIANTS = ["processed_appids unique", "games_found increments on type=='game'"]
        """
        self.start_time = datetime.now(timezone.utc)
        logging.info(f"🚀 Starting data collection run. Target: {target_game_count} games. Output: {output_file.name}")

        apps = self.get_app_list()
        if not apps:
            logging.critical("Cannot proceed without an application list. Exiting.")
            return

        # Filter out tiny legacy/utility IDs for a more game-heavy candidate pool.
        candidate_apps = [app for app in apps if app.get('appid', 0) > APPID_FILTER_THRESHOLD]
        logging.info(f"Filtered to {len(candidate_apps):,} candidate apps (AppID > {APPID_FILTER_THRESHOLD}).")

        processed_appids: Set[int] = set()
        games_found = 0

        while games_found < target_game_count and candidate_apps:
            # Human: choose a random candidate and remove it to avoid reprocessing.
            # ML:    SAMPLING = "random-without-replacement"
            app = random.choice(candidate_apps)
            appid = app.get('appid')
            candidate_apps.pop(candidate_apps.index(app))

            if not appid or appid in processed_appids:
                continue

            processed_appids.add(appid)
            name = app.get('name', 'Unknown')
            logging.info(f"({games_found}/{target_game_count}) Processing AppID {appid}: {name}")

            app_details = self.get_app_details(appid)

            game_record = {
                'appid': appid,
                'name_from_applist': name,
                'app_details': app_details
            }
            self.collected_data.append(game_record)

            if app_details['success'] and app_details.get('data', {}).get('type') == 'game':
                games_found += 1
                game_data = app_details['data']
                price = game_data.get('price_overview', {}).get('final_formatted', 'Free')
                logging.info(f"   ✅ Found Game: {game_data.get('name', 'Unknown')} | Price: {price}")
            else:
                logging.warning(f"   - Skipped: Not a valid game or details failed.")

            # Periodic checkpoint to reduce blast radius on interruption.
            if len(processed_appids) % 25 == 0 and len(processed_appids) > 0:
                logging.info("💾 Performing periodic save...")
                self.end_time = datetime.now(timezone.utc)  # temporary end for interim metrics
                self.save_data(output_file, target_game_count)

            time.sleep(BASE_DELAY_SECONDS)

        self.end_time = datetime.now(timezone.utc)
        logging.info("💾 Performing final save...")
        self.save_data(output_file, target_game_count)

        logging.info("🎉 Collection complete!")
        logging.info(f"   Target Games: {target_game_count}")
        logging.info(f"   Actual Games Found: {games_found}")
        logging.info(f"   Total Apps Processed: {len(processed_appids)}")
        logging.info(f"   Data saved to {output_file.name}")

# --- Interactive helper --------------------------------------------------------------------------
def prompt_for_game_count() -> int:
    """
    Human: simple validated prompt for interactive runs (press Enter for 100).
    ML:    INPUT_VALIDATION = "int>0 or default=100"
    """
    while True:
        choice = input("Enter the target number of games to collect [default: 100]: ")
        if not choice:
            return 100
        try:
            count = int(choice)
            if count > 0:
                return count
            else:
                print("Please enter a positive number.", file=sys.stderr)
        except ValueError:
            print("Invalid input. Please enter a whole number.", file=sys.stderr)

# --- CLI entrypoint -------------------------------------------------------------------------------
def main():
    """
    CLI contract:
      -c/--count <int> : direct mode target; omit to use interactive prompt.
    Default formatter surfaces defaults in -h output (developer ergonomics).
    """
    parser = argparse.ArgumentParser(
        description="Fetch a sample of game data from the Steam API. Supports both direct and interactive modes.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-c', '--count',
        type=int,
        default=None,
        help="Optional: The target number of games to collect. If omitted, the script will prompt you."
    )
    args = parser.parse_args()

    # Determine target game count (direct vs interactive).
    if args.count is not None:
        if args.count <= 0:
            logging.error("Error: --count must be a positive number.")
            sys.exit(1)
        target_count = args.count
    else:
        target_count = prompt_for_game_count()

    # Timestamped output filename for reproducibility.
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = Path(f"steam_data_{target_count}_games_{timestamp}.json")

    # Run the collection.
    puller = SteamDataPuller(api_key=STEAM_API_KEY)
    puller.run_collection(target_game_count=target_count, output_file=output_file)

if __name__ == "__main__":
    main()
