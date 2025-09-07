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
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-09-07      1.0             vintagedon      Initial release of the targeted backfill utility.
#
# =====================================================================================================================

import os
import sys
import json
import time
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any

# A try-except block for imports provides a clean, user-friendly exit if dependencies are missing.
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
load_dotenv(dotenv_path=CWD / '.env')

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# This script uses the primary API key, as it's intended for smaller, targeted runs
# where quota is less of a concern than with the full-scale collectors.
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
if not STEAM_API_KEY:
    logging.error("FATAL: STEAM_API_KEY environment variable not set.")
    sys.exit(1)

# --- Constants ---
BASE_DELAY_SECONDS = 1.5 # Using the known-good conservative delay
API_USER_AGENT = 'SteamDataPlatform/2.9-Backfill (https://github.com/vintagedon/steam-dataset-2025)'

class BackfillCollector:
    """
    Handles the targeted re-collection of missing application data.
    This class is a focused utility, contrasting with the more complex, stateful collectors.
    Its job is to perform one specific, stateless task: process a list and generate an output file.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        # Using a requests.Session is a best practice even for smaller scripts. It enables
        # connection pooling, which reuses the underlying TCP connection for multiple requests,
        # improving performance and reducing overhead.
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': API_USER_AGENT})

    def get_app_details(self, appid: int) -> Dict[str, Any]:
        """Fetches detailed information for a single appid, returning the raw API response object."""
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        try:
            response = self.session.get(url, timeout=20)
            # raise_for_status() is a convenient way to handle HTTP errors (4xx or 5xx).
            response.raise_for_status()
            # The API response for a single appid is a dictionary with the appid as the key
            # e.g., {"10": {"success": true, "data": {...}}}
            # We return this entire structure.
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error for appid {appid}: {e}")
        except json.JSONDecodeError:
            logging.error(f"JSON decode error for appid {appid}. The app may be delisted or restricted.")
        
        # This return statement is a critical part of the script's resilience. If any error
        # occurs, we return a standardized failure object instead of crashing. This allows
        # the main loop to continue processing the rest of the appids.
        return {str(appid): {"success": False}}

    def run_collection(self, input_path: Path, output_path: Path):
        """Main orchestration method for the backfill process."""
        logging.info(f"🚀 Starting targeted re-collection from '{input_path.name}'.")
        
        try:
            # Using a list comprehension is a concise, pythonic way to read and parse the input file.
            with input_path.open('r', encoding='utf-8') as f:
                appids_to_fetch = [int(line.strip()) for line in f if line.strip().isdigit()]
        except IOError as e:
            logging.error(f"FATAL: Could not read input file '{input_path.name}'. Error: {e}")
            sys.exit(1)

        if not appids_to_fetch:
            logging.warning("Input file is empty or contains no valid appids. Exiting.")
            return

        logging.info(f"Found {len(appids_to_fetch):,} appids to re-collect.")
        
        all_results = []
        successful_count = 0
        
        # `tqdm` provides a clean, informative progress bar, which is essential for user
        # experience when processing a list of any significant size.
        for appid in tqdm(appids_to_fetch, desc="Re-collecting missing apps"):
            appid_str = str(appid)
            result = self.get_app_details(appid)
            
            # The Steam API nests the actual success flag. We need to check it carefully.
            # This defensive check ensures we correctly identify successful responses.
            if result and appid_str in result and result[appid_str].get('success'):
                # --- CRITICAL TRANSFORMATION ---
                # The raw API response is nested under the appid string (e.g., result['10']).
                # Our master file format, however, expects a flat object like {"success": true, "data": {...}}.
                # This line reformats the raw API response to match our standardized data structure,
                # ensuring that this backfill data can be seamlessly merged later.
                formatted_result = result[appid_str]
                all_results.append(formatted_result)
                successful_count += 1
            else:
                logging.warning(f"Failed to retrieve data for appid {appid}. It may be delisted or restricted.")
                # We still append a failure record to maintain a complete list, though these
                # will likely be filtered out by the master import script.
                all_results.append({"success": False, "data": {"steam_appid": appid}})

            # The delay is crucial to be a good API citizen and avoid rate-limiting.
            time.sleep(BASE_DELAY_SECONDS)

        logging.info(f"Successfully re-collected data for {successful_count}/{len(appids_to_fetch)} applications.")
        
        try:
            # The final output is a JSON array of application detail objects, ready to be
            # appended to or merged with the master dataset.
            with output_path.open('w', encoding='utf-8') as f:
                json.dump(all_results, f, indent=2)
            logging.info(f"✅ Backfill data saved to '{output_path.name}'.")
        except IOError as e:
            logging.error(f"FATAL: Could not write to output file '{output_path.name}'. Error: {e}")
            sys.exit(1)

def main():
    """Parses command-line arguments and initiates the backfill collection."""
    # `argparse` provides a professional, self-documenting command-line interface.
    parser = argparse.ArgumentParser(
        description="Re-collects Steam game data for a specific list of missing appids.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_file", type=Path, help="Path to the text file containing one appid per line (e.g., missing_appids.txt).")
    parser.add_argument("--output", type=Path, default="steam_games_backfill.json", help="Name of the output JSON file for the collected data.")
    args = parser.parse_args()

    collector = BackfillCollector(api_key=STEAM_API_KEY)
    collector.run_collection(input_path=args.input_file, output_path=args.output)

if __name__ == "__main__":
    main()
