# =================================================================================================
# Script:        test-steam-api-v2.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       1.1
# Created:       2025-08-31
# Last Updated:  2025-09-28
#
# Purpose:
#   Comprehensive probe of core endpoints (applist, appdetails, rate-limit behavior) with a CLI
#   that can run the full suite or individual checks—useful before scaling collectors.
#
# Inputs:
#   - ENV: STEAM_API_KEY (required)
# Outputs:
#   - Console logs (rate, success ratio; sample app names)
#
# Operational Profile:
#   - Runtime Context: {python: 3.9+}
#   - Idempotency: {safe_rerun: true}
#   - Failure Modes: {network_error, json_decode_error, http_4xx|5xx}
#
# Data Lineage & Provenance:
#   SOURCE_OF_TRUTH:
#     - https://api.steampowered.com/ISteamApps/GetAppList/v2/
#     - https://store.steampowered.com/api/appdetails?appids=<id>
#
# Security & Compliance:
#   - API key via .env only; no PII touching.
#
# Change Log:
#   - 2025-09-28  Standardized header + dual-audience comments; behavior unchanged.
# =================================================================================================

import os
import time
import sys
import logging
import argparse
import requests
from typing import Optional, List, Dict, Any
from json.decoder import JSONDecodeError
from dotenv import load_dotenv

# --- Configuration & Setup ---

# Load environment variables from a .env file for local development.
# This line will not fail if the file doesn't exist.
load_dotenv()

# Configure standardized logging.
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Fetch API key from environment variables. This is more secure than hardcoding.
# The script will exit if the key is not found.
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
if not STEAM_API_KEY:
    logging.error("FATAL: STEAM_API_KEY environment variable not set. Please create a .env file or set it manually.")
    sys.exit(1)

# Constants for API interaction
BASE_DELAY_SECONDS = 1.5
API_USER_AGENT = 'SteamDataPlatform/1.1 (https://github.com/vintagedon/steam-dataset-2025)'


# --- Main Class ---
class SteamAPITester:
    """
    Encapsulates all functionality for testing the Steam Web API endpoints.
    """

    def __init__(self, api_key: str):
        """Initializes the tester with an API key and a persistent requests session."""
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': API_USER_AGENT})

    def test_app_list(self) -> Optional[List[Dict[str, Any]]]:
        """
        Tests the ISteamApps/GetAppList endpoint.

        Returns:
            A list of app dictionaries if successful, otherwise None.
        """
        logging.info("Testing ISteamApps/GetAppList...")
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

        try:
            response = self.session.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            apps = data.get('applist', {}).get('apps', [])
            
            logging.info(f"✅ GetAppList successful - Found {len(apps):,} applications.")
            
            # Show sample apps
            for app in apps[:5]:
                logging.info(f"   Sample: {app.get('appid')} - {app.get('name')}")
                
            return apps

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ GetAppList failed due to a network error: {e}")
        except JSONDecodeError:
            logging.error("❌ GetAppList failed: Could not decode JSON response.")
        
        return None

    def test_app_details(self, appid: int) -> Optional[Dict[str, Any]]:
        """
        Tests the appdetails endpoint for a specific application.

        Returns:
            The application data dictionary if successful, otherwise None.
        """
        logging.info(f"Testing appdetails for appid: {appid}")
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            app_data = data.get(str(appid), {})
            if app_data.get('success'):
                game_info = app_data.get('data', {})
                logging.info(f"✅ appdetails successful: {game_info.get('name', 'Unknown')}")
                return app_data
            else:
                logging.warning(f"⚠️ appdetails returned success=false for {appid}. May be restricted or invalid.")
                return None

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ appdetails failed for {appid} due to a network error: {e}")
        except JSONDecodeError:
            logging.error(f"❌ appdetails failed for {appid}: Could not decode JSON response.")
        
        return None

    def test_rate_limiting(self, test_apps: List[Dict[str, Any]]) -> None:
        """
        Performs a series of requests to observe and measure API rate behavior.
        """
        logging.info("Testing rate limiting with consecutive requests on newer app IDs...")
        start_time = time.time()
        successful_requests = 0
        # MODIFIED: Increased the number of test items to 10 as requested.
        total_requests = min(len(test_apps), 10)

        if total_requests == 0:
            logging.warning("Skipping rate limiting test: no apps to test with.")
            return

        # MODIFIED: Sliced from the end of the list (-total_requests:) to get the latest apps
        # instead of the oldest ones from the beginning.
        for i, app in enumerate(test_apps[-total_requests:]):
            appid = app.get('appid')
            if not appid:
                continue

            logging.info(f"Request {i+1}/{total_requests} - Testing AppID: {appid}")
            if self.test_app_details(appid):
                successful_requests += 1

            if i < total_requests - 1:
                logging.info(f"Waiting {BASE_DELAY_SECONDS}s...")
                time.sleep(BASE_DELAY_SECONDS)

        elapsed = time.time() - start_time
        rate = (successful_requests / elapsed * 60) if elapsed > 0 else 0

        logging.info("--- Rate Limiting Test Complete ---")
        logging.info(f"   {successful_requests}/{total_requests} successful requests")
        logging.info(f"   {elapsed:.1f}s elapsed")
        logging.info(f"   Effective Rate: {rate:.1f} requests/minute (with {BASE_DELAY_SECONDS}s delay)")

    def run_full_test(self) -> None:
        """Executes the complete test suite in sequence."""
        logging.info("🚀 Starting Steam API Test Suite")
        
        all_apps = self.test_app_list()
        if not all_apps:
            logging.critical("❌ Cannot continue without the app list. Exiting.")
            return

        # Use a well-known, simple app for details/reviews test to ensure it exists
        # e.g., Counter-Strike: Global Offensive (appid 730)
        csgo_appid = 730
        
        time.sleep(BASE_DELAY_SECONDS)
        self.test_app_details(csgo_appid)
        
        time.sleep(BASE_DELAY_SECONDS)
        # Add a placeholder for reviews test if re-implemented
        # self.test_reviews(csgo_appid) 
        
        time.sleep(BASE_DELAY_SECONDS)
        self.test_rate_limiting(all_apps)

        logging.info("✅ Steam API Test Suite Complete")

# --- Script Entry Point ---
def main():
    """Main function to parse arguments and execute the corresponding tests."""
    parser = argparse.ArgumentParser(
        description="A testing suite for the Steam Web API.",
        epilog="If no command is specified, the 'full' test suite will be run."
    )
    # Using subparsers is a clean way to handle different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # 'full' command
    subparsers.add_parser('full', help='Run the full, end-to-end test suite.')

    # 'applist' command
    subparsers.add_parser('applist', help='Test the GetAppList endpoint.')

    # 'details' command
    details_parser = subparsers.add_parser('details', help='Test the appdetails endpoint for a specific AppID.')
    details_parser.add_argument('appid', type=int, help='The numeric AppID of the application.')
    
    # 'reviews' command (can be added here if the method is brought back)

    args = parser.parse_args()

    tester = SteamAPITester(STEAM_API_KEY)

    if args.command == "applist":
        tester.test_app_list()
    elif args.command == "details":
        tester.test_app_details(args.appid)
    elif args.command == "full":
        tester.run_full_test()
    else:
        # If no arguments are given, run the full test by default
        tester.run_full_test()

if __name__ == "__main__":
    main()

