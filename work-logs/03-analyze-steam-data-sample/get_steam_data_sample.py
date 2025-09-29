# =====================================================================================================================
# Script Name:    get_steam_data_sample.py
# Description:    A robust data collection tool to fetch a specified number of random game samples from the
#                 Steam API. It gathers application details and review summaries, then saves the aggregated
#                 data to a structured JSON file.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        1.1
# Date:           2025-08-31
# License:        MIT License
#
# Usage:          python get_steam_data_sample.py --count 100 --output "steam_sample_100.json"
#                 Arguments are optional and will use default values if not provided.
#
# Notes:          This script requires the 'requests' and 'python-dotenv' libraries.
#                 Install them using: pip install requests python-dotenv
#                 Create a '.env' file in the same directory with your API key:
#                 STEAM_API_KEY="YOUR_KEY_HERE"
#
# =====================================================================================================================
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-08-31      1.0             vintagedon      Initial release based on test script.
#   2025-08-31      1.1             vintagedon      Refactored for robustness: argparse for CLI, guaranteed collection
#                                                   logic, enhanced error handling, and pythonic best practices.
# =====================================================================================================================

# --- Imports ---
import os
import sys
import json
import time
import random
import logging
import argparse
import requests
from typing import Optional, List, Dict, Any, Set
from datetime import datetime
from json.decoder import JSONDecodeError
from dotenv import load_dotenv

# --- Configuration & Setup ---
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
if not STEAM_API_KEY:
    logging.error("FATAL: STEAM_API_KEY environment variable not set.")
    sys.exit(1)

# --- Constants ---
BASE_DELAY_SECONDS = 1.5
API_USER_AGENT = 'SteamDataPlatform/1.2 (https://github.com/vintagedon/steam-dataset-2025)'
# Heuristic to filter out early Steam tools, dedicated servers, and infrastructure items.
APPID_FILTER_THRESHOLD = 2000


# --- Main Class ---
class SteamDataPuller:
    """
    Manages the process of fetching, processing, and saving a sample of Steam game data.
    """

    def __init__(self, api_key: str):
        """Initializes the puller with an API key and a persistent requests session."""
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': API_USER_AGENT})
        self.collected_data: List[Dict[str, Any]] = []

    def get_app_list(self) -> List[Dict[str, Any]]:
        """
        Retrieves the complete list of applications from the Steam API.
        Returns a list of apps, or an empty list on failure.
        """
        logging.info("Fetching full Steam application list...")
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            # Safely access nested keys to prevent KeyErrors on malformed responses.
            apps = data.get('applist', {}).get('apps', [])
            logging.info(f"Successfully retrieved {len(apps):,} total applications.")
            return apps
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Network error while fetching app list: {e}")
        except JSONDecodeError:
            logging.error("❌ Failed to decode JSON from GetAppList response.")
        return []

    def get_app_details(self, appid: int) -> Dict[str, Any]:
        """
        Fetches detailed information for a single appid.
        Returns a structured dictionary indicating success or failure.
        """
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        base_response = {
            'appid': appid,
            'success': False,
            'fetched_at': datetime.now().isoformat()
        }
        try:
            response = self.session.get(url, timeout=15)
            # Some appids return 401 Unauthorized, we'll treat this as a failure but not a script-ending error.
            if response.status_code == 401:
                logging.warning(f"   - AppID {appid} is restricted (401 Unauthorized).")
                return {**base_response, 'error': '401 Unauthorized'}

            response.raise_for_status()
            data = response.json()
            
            app_data = data.get(str(appid), {})
            if app_data.get('success'):
                return {**base_response, 'success': True, 'data': app_data.get('data', {})}
            else:
                return base_response
                
        except requests.exceptions.RequestException as e:
            logging.error(f"   - Network error fetching details for {appid}: {e}")
            return {**base_response, 'error': str(e)}
        except JSONDecodeError:
            logging.warning(f"   - Failed to decode JSON for {appid}. Response might be empty or malformed.")
            return {**base_response, 'error': 'JSONDecodeError'}

    def save_data(self, output_file: str) -> None:
        """Saves all collected data to a JSON file with metadata."""
        output_data = {
            'metadata': {
                'collected_at': datetime.now().isoformat(),
                'total_records_processed': len(self.collected_data),
                'successful_games_found': len([
                    r for r in self.collected_data if r['app_details']['success'] and r['app_details']['data'].get('type') == 'game'
                ]),
                'api_key_used': self.api_key[:8] + "...",
                'delay_between_requests': BASE_DELAY_SECONDS
            },
            'games': self.collected_data
        }

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
        except IOError as e:
            logging.error(f"❌ Could not write to output file {output_file}: {e}")

    def run_collection(self, target_game_count: int, output_file: str) -> None:
        """Main entry point for the data collection process."""
        logging.info(f"🚀 Starting data collection run. Target: {target_game_count} games. Output: {output_file}")
        
        apps = self.get_app_list()
        if not apps:
            logging.critical("Cannot proceed without an application list. Exiting.")
            return
            
        # Filter the app list to create a pool of candidates to draw from.
        candidate_apps = [app for app in apps if app.get('appid', 0) > APPID_FILTER_THRESHOLD]
        logging.info(f"Filtered to {len(candidate_apps):,} candidate apps (AppID > {APPID_FILTER_THRESHOLD}).")

        # Use a set for processed_appids for O(1) average time complexity lookups, which is highly efficient.
        processed_appids: Set[int] = set()
        games_found = 0
        
        # This while loop is more robust. It continues until the target is met or it runs out of apps to try.
        while games_found < target_game_count and candidate_apps:
            # Pick a random app from our candidate pool.
            app = random.choice(candidate_apps)
            appid = app.get('appid')
            
            # Remove the chosen app to prevent re-picking. This is more efficient than random.sample on a shrinking list.
            candidate_apps.remove(app)
            
            if not appid or appid in processed_appids:
                continue

            processed_appids.add(appid)
            name = app.get('name', 'Unknown')
            logging.info(f"({games_found}/{target_game_count}) Processing AppID {appid}: {name}")
            
            # 1. Get Application Details
            app_details = self.get_app_details(appid)
            
            game_record = {
                'appid': appid,
                'name_from_applist': name,
                'app_details': app_details,
                'reviews': None # Placeholder for potential future addition
            }
            self.collected_data.append(game_record)

            # 2. Check if it's a valid game and increment our counter if so.
            if app_details['success'] and app_details.get('data', {}).get('type') == 'game':
                games_found += 1
                game_data = app_details['data']
                price = game_data.get('price_overview', {}).get('final_formatted', 'Free')
                logging.info(f"   ✅ Found Game: {game_data.get('name', 'Unknown')} | Price: {price}")
            else:
                logging.warning(f"   - Skipped: Not a valid game or details failed.")
            
            # 3. Periodic Saving - crucial for long runs to prevent data loss on crash.
            if len(processed_appids) % 25 == 0:
                logging.info("💾 Performing periodic save...")
                self.save_data(output_file)

            # 4. Rate Limiting Delay
            time.sleep(BASE_DELAY_SECONDS)

        # Final save at the end of the collection run.
        logging.info("💾 Performing final save...")
        self.save_data(output_file)

        logging.info("🎉 Collection complete!")
        logging.info(f"   Target Games: {target_game_count}")
        logging.info(f"   Actual Games Found: {games_found}")
        logging.info(f"   Total Apps Processed: {len(processed_appids)}")
        logging.info(f"   Data saved to {output_file}")


# --- Script Entry Point ---
def main():
    """Parses command-line arguments and initiates the data collection."""
    parser = argparse.ArgumentParser(
        description="Fetch a sample of game data from the Steam API and save it to a JSON file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter # Shows default values in help message.
    )
    parser.add_argument(
        '-c', '--count',
        type=int,
        default=100,
        help="The target number of games to collect."
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default="steam_data_sample.json",
        help="The path to the output JSON file."
    )
    args = parser.parse_args()

    puller = SteamDataPuller(api_key=STEAM_API_KEY)
    puller.run_collection(target_game_count=args.count, output_file=args.output)


if __name__ == "__main__":
    main()
