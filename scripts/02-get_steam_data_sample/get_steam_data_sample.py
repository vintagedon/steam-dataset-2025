# =====================================================================================================================
# Script Name:    get_steam_data_sample.py
# Description:    A robust data collection tool to fetch a specified number of random game samples from the
#                 Steam API. It gathers application details and saves the aggregated data to a
#                 structured JSON file. It is designed to be resilient, skipping non-game apps
#                 (DLC, soundtracks, etc.) until its target is met.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        1.5
# Date:           2025-08-31
# License:        MIT License
#
# Usage:          This script supports both direct and interactive modes.
#                 Direct:   python get_steam_data_sample.py --count 50
#                 Interactive: python get_steam_data_sample.py
#
# Notes:          This script requires the 'requests' and 'python-dotenv' libraries.
#                 Install them using: pip install requests python-dotenv
#                 A .env file with a valid STEAM_API_KEY is required in the same directory.
#
# =====================================================================================================================
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-08-31      1.0-1.3         vintagedon      Initial development and iterative feature enhancements.
#   2025-08-31      1.4             vintagedon      (Placeholder for previous version)
#   2025-08-31      1.5             vintagedon      Completed a full commenting pass to document the engineering
#                                                   rationale, design patterns, and best practices in the code.
# =====================================================================================================================

# --- Imports ---
import os
import sys
import json
import time
import random
import logging
import argparse
from pathlib import Path
# timezone is imported specifically for creating timezone-aware datetime objects. This is the modern,
# correct way to handle time, avoiding the ambiguity of "naive" datetimes that led to utcnow()'s deprecation.
from datetime import datetime, timezone
from typing import List, Dict, Any, Set, Optional
from json.decoder import JSONDecodeError

# A try-except block for third-party imports provides a clean, user-friendly exit if dependencies are not
# installed, which is crucial for script portability and ease of use.
try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries 'requests' or 'python-dotenv' are not installed.", file=sys.stderr)
    print("Please install them using: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
# Loading environment variables at the module level ensures configuration is available globally
# before any execution logic begins. This is a standard pattern for separating config from code.
load_dotenv()

# Centralized logging is a core principle of robust application design. It provides consistent,
# structured, and timestamped output, which is vastly superior to scattered print() statements
# for debugging, auditing, and monitoring long-running processes.
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# This is a "guard clause" that enforces a critical precondition. The script is non-functional
# without an API key, so it fails fast with an explicit error message rather than allowing
# cryptic errors to surface later in the execution path.
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
if not STEAM_API_KEY:
    logging.error("FATAL: STEAM_API_KEY environment variable not set. Please create a .env file or set it manually.")
    sys.exit(1)

# --- Constants ---
# Defining constants globally makes the code more readable and maintainable. If these
# parameters need to be tuned, they are in one predictable, easily accessible location.
BASE_DELAY_SECONDS = 1.5
API_USER_AGENT = 'SteamDataPlatform/1.5 (https://github.com/vintagedon/steam-dataset-2025)'
APPID_FILTER_THRESHOLD = 2000

# --- Main Class ---
class SteamDataPuller:
    """
    Manages the process of fetching, processing, and saving a sample of Steam game data.
    The object-oriented approach is used here to encapsulate state (like the requests session,
    collected data, and timestamps) and behavior (API calls, saving data) into a single,
    cohesive unit, which improves code organization and reusability.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        # The use of a requests.Session object is a key performance optimization. It enables
        # connection pooling, which reuses the same underlying TCP connection for multiple
        # requests to the same host, avoiding the overhead of establishing a new connection every time.
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': API_USER_AGENT})
        self.collected_data: List[Dict[str, Any]] = []
        # These will store timezone-aware datetimes to accurately calculate the total run duration,
        # which is essential for performance monitoring and data lineage.
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None


    def get_app_list(self) -> List[Dict[str, Any]]:
        """Retrieves the complete list of applications from the Steam API."""
        logging.info("Fetching full Steam application list...")
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        try:
            # Setting an explicit timeout is a critical practice for network robustness.
            # It prevents the script from hanging indefinitely if the remote API is unresponsive.
            response = self.session.get(url, timeout=30)
            # response.raise_for_status() is a convenient and pythonic way to centralize
            # the handling of HTTP errors (status codes 4xx or 5xx).
            response.raise_for_status()
            data = response.json()
            # Safely accessing nested keys with .get() is a defensive programming technique that
            # prevents the script from crashing with a KeyError if the API returns an unexpected structure.
            apps = data.get('applist', {}).get('apps', [])
            logging.info(f"Successfully retrieved {len(apps):,} total applications.")
            return apps
        # Catching specific exception types (RequestException, JSONDecodeError) allows for more
        # granular and informative error logging, which is crucial for diagnosing failures.
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Network error while fetching app list: {e}")
        except JSONDecodeError:
            logging.error("❌ Failed to decode JSON from GetAppList response. The API might be down or returned malformed data.")
        return []

    def get_app_details(self, appid: int) -> Dict[str, Any]:
        """Fetches detailed information for a single appid."""
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        # Defining a base response structure ensures that this function always returns a
        # dictionary with a consistent set of keys, which simplifies the logic in the calling code.
        base_response = {
            'appid': appid,
            'success': False,
            # Using timezone.utc ensures all timestamps are standardized, which is critical for
            # data integrity in any system that might operate across different timezones.
            'fetched_at': datetime.now(timezone.utc).isoformat()
        }
        try:
            response = self.session.get(url, timeout=15)
            # This is an example of handling a "successful failure." A 401 is an expected outcome for
            # restricted content, and the script handles it gracefully instead of treating it as a fatal error.
            if response.status_code == 401:
                logging.warning(f"   - AppID {appid} is restricted (401 Unauthorized).")
                return {**base_response, 'error': '401 Unauthorized'}

            response.raise_for_status()
            data = response.json()
            
            app_data = data.get(str(appid), {})
            # This is a vital check. The Steam API can return a 200 OK status but indicate failure
            # within the JSON body. Trusting only the HTTP status code would lead to corrupt data.
            if app_data.get('success'):
                return {**base_response, 'success': True, 'data': app_data.get('data', {})}
            else:
                return base_response
                
        except requests.exceptions.RequestException as e:
            logging.error(f"   - Network error fetching details for {appid}: {e}")
            return {**base_response, 'error': str(e)}
        except JSONDecodeError:
            logging.warning(f"   - Failed to decode JSON for {appid}. The response might be empty or malformed.")
            return {**base_response, 'error': 'JSONDecodeError'}

    def save_data(self, output_file: Path, target_count: int) -> None:
        """Saves all collected data to a JSON file with a comprehensive metadata block for data lineage."""
        run_duration_seconds = (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else None
        
        # This metadata block is a core tenet of good data engineering. It makes the output file
        # self-describing, providing a complete audit trail of how, when, and with what parameters
        # the data was generated.
        output_data = {
            'metadata': {
                'run_start_timestamp_utc': self.start_time.isoformat() if self.start_time else None,
                'run_end_timestamp_utc': self.end_time.isoformat() if self.end_time else None,
                'run_duration_seconds': run_duration_seconds,
                'target_game_count': target_count,
                'total_records_processed': len(self.collected_data),
                'successful_games_found': len([
                    r for r in self.collected_data if r.get('app_details',{}).get('success') and r.get('app_details',{}).get('data', {}).get('type') == 'game'
                ]),
                # Slicing the API key is a security measure to prevent the full secret from being written to disk.
                'api_key_used': self.api_key[:8] + "...",
                'delay_between_requests': BASE_DELAY_SECONDS
            },
            'games': self.collected_data
        }

        try:
            # Explicitly setting encoding to 'utf-8' is vital for correctly handling international
            # game titles and descriptions, preventing UnicodeEncodeError exceptions.
            with output_file.open('w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
        except IOError as e:
            logging.error(f"❌ Could not write to output file {output_file.name}: {e}")

    def run_collection(self, target_game_count: int, output_file: Path) -> None:
        """Main entry point for the data collection process, orchestrating the entire workflow."""
        self.start_time = datetime.now(timezone.utc)
        logging.info(f"🚀 Starting data collection run. Target: {target_game_count} games. Output: {output_file.name}")
        
        apps = self.get_app_list()
        if not apps:
            logging.critical("Cannot proceed without an application list. Exiting.")
            return
            
        # Pre-filtering the app list is a simple heuristic that significantly improves the "hit rate"
        # of the random sampling, making the script more efficient by not wasting API calls on old tools.
        candidate_apps = [app for app in apps if app.get('appid', 0) > APPID_FILTER_THRESHOLD]
        logging.info(f"Filtered to {len(candidate_apps):,} candidate apps (AppID > {APPID_FILTER_THRESHOLD}).")

        # The choice of a 'set' for tracking processed IDs is a deliberate performance optimization.
        # A set provides O(1) average time complexity for lookups (`in` check), which is far
        # more efficient than a list's O(n) complexity for a long-running process.
        processed_appids: Set[int] = set()
        games_found = 0
        
        # The `while` loop is the core of the script's resilience. Unlike iterating over a fixed-size
        # sample, this structure guarantees that the script will continue working until its primary
        # objective (collecting N games) is met or it exhausts all possibilities.
        while games_found < target_game_count and candidate_apps:
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

            # This is the primary success condition: the API call must succeed AND the item's type must be 'game'.
            if app_details['success'] and app_details.get('data', {}).get('type') == 'game':
                games_found += 1
                game_data = app_details['data']
                price = game_data.get('price_overview', {}).get('final_formatted', 'Free')
                logging.info(f"   ✅ Found Game: {game_data.get('name', 'Unknown')} | Price: {price}")
            else:
                logging.warning(f"   - Skipped: Not a valid game or details failed.")
            
            # Periodic saving is a critical resilience feature. If a long-running script fails or is
            # interrupted, this ensures that not all previously collected data is lost.
            if len(processed_appids) % 25 == 0 and len(processed_appids) > 0:
                logging.info("💾 Performing periodic save...")
                self.end_time = datetime.now(timezone.utc)
                self.save_data(output_file, target_game_count)

            # The delay is not just a suggestion; it's a mandatory practice to be a good API citizen
            # and prevent being rate-limited or IP-banned by the server.
            time.sleep(BASE_DELAY_SECONDS)

        self.end_time = datetime.now(timezone.utc)
        logging.info("💾 Performing final save...")
        self.save_data(output_file, target_game_count)

        logging.info("🎉 Collection complete!")
        logging.info(f"   Target Games: {target_game_count}")
        logging.info(f"   Actual Games Found: {games_found}")
        logging.info(f"   Total Apps Processed: {len(processed_appids)}")
        logging.info(f"   Data saved to {output_file.name}")

# --- Helper Function for Interactive Mode ---
def prompt_for_game_count() -> int:
    """
    Prompts the user to enter the number of games to collect, with validation.
    This function isolates the interactive logic from the main workflow.
    """
    while True:
        choice = input("Enter the target number of games to collect [default: 100]: ")
        # Handle the default case where the user just presses Enter.
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

# --- Script Entry Point ---
def main():
    """
    Parses CLI arguments for direct mode or falls back to interactive mode.
    This hybrid design pattern provides the best of both worlds: scriptability for automation
    and user-friendliness for manual runs.
    """
    parser = argparse.ArgumentParser(
        description="Fetch a sample of game data from the Steam API. Supports both direct and interactive modes.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # The --count flag is optional; `default=None` is the key to detecting whether it was
    # provided by the user, which allows the script to decide whether to enter interactive mode.
    parser.add_argument(
        '-c', '--count',
        type=int,
        default=None,
        help="Optional: The target number of games to collect. If omitted, the script will prompt you."
    )
    args = parser.parse_args()

    # --- Determine target game count (direct vs. interactive) ---
    target_count: int
    if args.count is not None:
        # Direct mode: A value was passed via the --count flag.
        if args.count <= 0:
            logging.error("Error: --count must be a positive number.")
            sys.exit(1)
        target_count = args.count
    else:
        # Interactive mode: No --count flag was used, so we trigger the user prompt.
        target_count = prompt_for_game_count()

    # --- Generate the dynamic, descriptive output filename ---
    # This automated naming convention is crucial for maintaining an organized history of data runs.
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = Path(f"steam_data_{target_count}_games_{timestamp}.json")
    
    # --- Instantiate the class and run the collection ---
    puller = SteamDataPuller(api_key=STEAM_API_KEY)
    puller.run_collection(target_game_count=target_count, output_file=output_file)

# This standard Python construct ensures that the `main()` function is called only when the
# script is executed directly from the command line, not when it's imported as a module
# into another script. This makes the code modular and reusable.
if __name__ == "__main__":
    main()
