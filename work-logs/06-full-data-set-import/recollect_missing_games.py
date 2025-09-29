# =================================================================================================
# File:          recollect_missing_games.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Targeted re-collection of missing appdetails by appid list; saves backfill JSON.
#
# Section Map:
#   1) Imports — dependencies and why they're needed
#   2) Configuration & Setup — env, logging, runtime knobs
#   3) Core Components — classes/functions with intent + IO contracts
#   4) Orchestration — how components are wired together
#   5) Entry Point — CLI usage and safe error handling
#
# Provenance / RAG Hints:
#   SOURCE_OF_TRUTH: Steam master JSON & PostgreSQL (see Phase 04 schema)
#   READS / WRITES:  unchanged from original script behavior
#
# Security:
#   - Secrets via .env only (PG_* / STEAM_API_KEY); do not hardcode credentials.
#
# Change Log (docs-only):
#   - 2025-09-29  Added standardized header + dual-audience inline comments; no behavioral changes.
# =================================================================================================

# =====================================================================================================================
# Script Name:    recollect_missing_games.py
# Description:    A targeted data collection script that reads a list of appids from a text file
#                 (e.g., missing_appids.txt) and re-fetches their appdetails from the Steam API.
#                 This is used to backfill data for API calls that failed during the main collection.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        1.0
# Date:           2025-09-07
# License:        MIT License
#
# Usage:          python recollect_missing_games.py <input_file.txt> --output <output_file.json>
# Example:        python recollect_missing_games.py missing_appids.txt --output steam_games_backfill.json
#
# =====================================================================================================================

# --- Imports --------------------------------------------------------------------------------------
# Human: Group stdlib vs third-party; fail fast with helpful install hints.
# ML:    DEPENDS_ON — capture runtime libs for reproducibility.
import os
import sys
import json
import time
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any

try:
    import requests
    from dotenv import load_dotenv
    from tqdm import tqdm
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install requests python-dotenv tqdm", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
CWD = Path.cwd()
# --- Configuration & Setup ------------------------------------------------------------------------
# Human: Centralize env + logging knobs to keep core logic clean/testable.
# ML:    CONFIG_KEYS — parse constants/env names for orchestration.
load_dotenv(dotenv_path=CWD / '.env')

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
if not STEAM_API_KEY:
    logging.error("FATAL: STEAM_API_KEY environment variable not set.")
    sys.exit(1)

# --- Constants ---
BASE_DELAY_SECONDS = 1.5
API_USER_AGENT = 'SteamDataPlatform/2.9-Backfill (https://github.com/vintagedon/steam-dataset-2025)'

class BackfillCollector:
    """Handles the targeted re-collection of missing application data."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': API_USER_AGENT})

    def get_app_details(self, appid: int) -> Dict[str, Any]:
        """Fetches detailed information for a single appid, returning the raw API response object."""
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            # The API response for a single appid is a dictionary with the appid as the key
            # e.g., {"10": {"success": true, "data": {...}}}
            # We return this entire structure to match the master file format.
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error for appid {appid}: {e}")
        except json.JSONDecodeError:
            logging.error(f"JSON decode error for appid {appid}.")
        # Return a standard failure object if anything goes wrong
        return {str(appid): {"success": False}}

    def run_collection(self, input_path: Path, output_path: Path):
        """Main orchestration method for the backfill process."""
        logging.info(f"🚀 Starting targeted re-collection from '{input_path.name}'.")
        
        try:
            with input_path.open('r', encoding='utf-8') as f:
                appids_to_fetch = [int(line.strip()) for line in f if line.strip().isdigit()]
        except IOError as e:
            logging.error(f"FATAL: Could not read input file '{input_path.name}'. Error: {e}")
            sys.exit(1)

        logging.info(f"Found {len(appids_to_fetch):,} appids to re-collect.")
        
        all_results = []
        successful_count = 0
        
        for appid in tqdm(appids_to_fetch, desc="Re-collecting missing apps"):
            # The API uses the appid as the key in its response, so we convert it to a string.
            appid_str = str(appid)
            result = self.get_app_details(appid)
            
            # The Steam API nests the actual success flag. We need to check it.
            if result and appid_str in result and result[appid_str].get('success'):
                # We need to reshape the data to match the master file structure
                # The master file has {"success": true, "data": {...}}
                # The API gives {"appid": {"success": true, "data": {...}}}
                # Let's reformat to be safe.
                formatted_result = result[appid_str]
                all_results.append(formatted_result)
                successful_count += 1
            else:
                logging.warning(f"Failed to retrieve data for appid {appid}. It may be delisted or restricted.")
                all_results.append({"success": False}) # Add a failure record to match master file

            time.sleep(BASE_DELAY_SECONDS)

        logging.info(f"Successfully re-collected data for {successful_count}/{len(appids_to_fetch)} applications.")
        
        try:
            with output_path.open('w', encoding='utf-8') as f:
                json.dump(all_results, f)
            logging.info(f"✅ Backfill data saved to '{output_path.name}'.")
        except IOError as e:
            logging.error(f"FATAL: Could not write to output file '{output_path.name}'. Error: {e}")
            sys.exit(1)

# --- Orchestration -------------------------------------------------------------------------------
# Human: Wire components; parse args; validate env; run safely.
# ML:    ENTRYPOINT(main) — transactional operations; robust error handling.
def main():
    parser = argparse.ArgumentParser(
        description="Re-collects Steam game data for a specific list of missing appids.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_file", type=Path, help="Path to the text file containing one appid per line (e.g., missing_appids.txt).")
    parser.add_argument("--output", type=Path, default="steam_games_backfill.json", help="Name of the output JSON file for the collected data.")
    args = parser.parse_args()

    collector = BackfillCollector(api_key=STEAM_API_KEY)
    collector.run_collection(input_path=args.input_file, output_path=args.output)

# --- Entry Point -----------------------------------------------------------------------------------
# Human: Direct CLI execution path with actionable errors.
# ML:    RUNTIME_START — begin telemetry if needed.
if __name__ == "__main__":
    main()
