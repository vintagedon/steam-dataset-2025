# =====================================================================================================================
# Script Name:    test_steam_api.py
# Description:    A comprehensive testing suite for the Steam Web API. This script verifies key endpoints
#                 like GetAppList and appdetails, and includes functionality to test API rate
#                 limiting behavior. This version incorporates Python best practices.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        1.2
# Date:           2025-08-31
# License:        MIT License
#
# Usage:          To run the full test suite:
#                 python test_steam_api_commented.py full
#
#                 To run a specific test:
#                 python test_steam_api_commented.py applist
#                 python test_steam_api_commented.py details <appid>
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
#   2025-08-31      1.0             vintagedon      Initial release.
#   2025-08-31      1.1             vintagedon      Refactored for best practices: argparse, logging, type hints,
#                                                   and externalized API key configuration.
#   2025-08-31      1.2             vintagedon      Added detailed line-by-line comments to the refactored script.
# =====================================================================================================================

# --- Imports ---
# os: Used to interact with the operating system, specifically for reading environment variables.
# time: Provides time-related functions, used here for delays (time.sleep) and performance timing.
# sys: Provides access to system-specific parameters and functions, used to exit the script on fatal errors.
# logging: Python's standard library for flexible event logging. More powerful than print().
# argparse: The standard library for parsing command-line arguments, creating professional CLIs.
# requests: A third-party library for making HTTP requests; the de facto standard in Python.
# typing: Provides support for type hints, improving code clarity and allowing for static analysis.
# json.decoder.JSONDecodeError: A specific exception for handling malformed JSON responses.
# dotenv.load_dotenv: A function from the python-dotenv library to load environment variables from a .env file.
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

# This function looks for a file named '.env' in the current directory and loads any
# key-value pairs it contains into the environment variables. This is ideal for local development
# as it keeps secrets out of the code and out of source control (if .env is in .gitignore).
load_dotenv()

# Configure the root logger for the entire application.
# - level=logging.INFO: Sets the minimum level of message to be displayed.
# - format: Defines the structure of the log output, making it consistent and readable.
# - datefmt: Specifies the format for the timestamp in the log messages.
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Securely fetch the API key from the environment variables. os.getenv() returns None if the variable is not found.
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
# This is a critical pre-flight check. If the API key is missing, the script cannot function.
# We log a fatal error and exit with a non-zero status code to indicate failure.
if not STEAM_API_KEY:
    logging.error("FATAL: STEAM_API_KEY environment variable not set. Please create a .env file or set it manually.")
    sys.exit(1)

# Define constants for API interaction. This avoids "magic strings/numbers" in the code, making it easier to read and modify.
BASE_DELAY_SECONDS = 1.5
API_USER_AGENT = 'SteamDataPlatform/1.1 (https://github.com/vintagedon/steam-dataset-2025)'


# --- Main Class ---
class SteamAPITester:
    """
    Encapsulates all functionality for testing the Steam Web API endpoints.
    Using a class allows us to maintain state (like the requests session) cleanly.
    """

    def __init__(self, api_key: str):
        """
        Initializes the tester with an API key and a persistent requests session.
        Type hint 'api_key: str' makes it clear what data type is expected.
        """
        self.api_key = api_key
        # A requests.Session object is used to persist headers and cookies across multiple requests.
        # It also utilizes connection pooling, which can significantly speed up consecutive requests to the same host.
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': API_USER_AGENT})

    def test_app_list(self) -> Optional[List[Dict[str, Any]]]:
        """
        Tests the ISteamApps/GetAppList endpoint.
        The return type hint indicates this function can return a list of dictionaries, or None on failure.
        'List[Dict[str, Any]]' means a list, where each item is a dictionary with string keys and values of any type.
        """
        logging.info("Testing ISteamApps/GetAppList...")
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

        try:
            response = self.session.get(url)
            # This will raise an HTTPError exception if the HTTP status code is 4xx (client error) or 5xx (server error).
            # It's a concise way to handle bad HTTP responses.
            response.raise_for_status()
            data = response.json()
            # Using .get() is a safe way to access dictionary keys. It returns None (or a specified default)
            # if a key is not found, preventing a KeyError exception.
            apps = data.get('applist', {}).get('apps', [])
            
            logging.info(f"✅ GetAppList successful - Found {len(apps):,} applications.")
            
            # Show a sample of the first 5 apps for quick verification.
            for app in apps[:5]:
                logging.info(f"   Sample: {app.get('appid')} - {app.get('name')}")
                
            return apps

        # Catching specific exceptions is better than a generic 'except Exception:'.
        # It makes the error handling more precise and prevents accidentally catching unrelated errors.
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ GetAppList failed due to a network error: {e}")
        except JSONDecodeError:
            logging.error("❌ GetAppList failed: Could not decode JSON response. The API might be down or returned invalid data.")
        
        return None

    def test_app_details(self, appid: int) -> Optional[Dict[str, Any]]:
        """
        Tests the appdetails endpoint for a specific application.
        The 'appid: int' type hint enforces that this function expects an integer.
        """
        logging.info(f"Testing appdetails for appid: {appid}")
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            # The appdetails API nests data under a key matching the appid. We must cast our appid to a string to match.
            app_data = data.get(str(appid), {})
            # The API can return a 200 OK status but indicate failure within the JSON body. This check is crucial.
            if app_data.get('success'):
                game_info = app_data.get('data', {})
                logging.info(f"✅ appdetails successful: {game_info.get('name', 'Unknown')}")
                return app_data
            else:
                logging.warning(f"⚠️ appdetails returned success=false for {appid}. The app may be restricted, unreleased, or invalid.")
                return None

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ appdetails failed for {appid} due to a network error: {e}")
        except JSONDecodeError:
            logging.error(f"❌ appdetails failed for {appid}: Could not decode JSON response.")
        
        return None

    def test_rate_limiting(self, test_apps: List[Dict[str, Any]]) -> None:
        """
        Performs a series of requests to observe and measure API rate behavior.
        The return type hint '-> None' explicitly states that this function does not return a value.
        """
        logging.info("Testing rate limiting with consecutive requests on newer app IDs...")
        start_time = time.time()
        successful_requests = 0
        total_requests = min(len(test_apps), 10)

        if total_requests == 0:
            logging.warning("Skipping rate limiting test: no apps to test with.")
            return

        # Python's list slicing makes it easy to get the last N items from a list.
        # 'test_apps[-total_requests:]' creates a new list containing the last 10 apps.
        for i, app in enumerate(test_apps[-total_requests:]):
            appid = app.get('appid')
            # A safety check in case an app entry is malformed and missing an appid.
            if not appid:
                continue

            logging.info(f"Request {i+1}/{total_requests} - Testing AppID: {appid}")
            if self.test_app_details(appid):
                successful_requests += 1

            # Pause between requests, but not after the very last one.
            if i < total_requests - 1:
                logging.info(f"Waiting {BASE_DELAY_SECONDS}s...")
                time.sleep(BASE_DELAY_SECONDS)

        # Calculate performance metrics.
        elapsed = time.time() - start_time
        rate = (successful_requests / elapsed * 60) if elapsed > 0 else 0

        logging.info("--- Rate Limiting Test Complete ---")
        logging.info(f"   {successful_requests}/{total_requests} successful requests")
        logging.info(f"   {elapsed:.1f}s elapsed")
        logging.info(f"   Effective Rate: {rate:.1f} requests/minute (with {BASE_DELAY_SECONDS}s delay)")

    def run_full_test(self) -> None:
        """Executes the complete test suite in a logical sequence."""
        logging.info("🚀 Starting Steam API Test Suite")
        
        all_apps = self.test_app_list()
        # If the first critical API call fails, we can't proceed with the rest of the tests.
        if not all_apps:
            logging.critical("❌ Cannot continue without the app list. Exiting.")
            return

        # Hardcoding a well-known, public appID (CS2) makes the details test more reliable,
        # ensuring we're not testing a random app that might be restricted or delisted.
        csgo_appid = 730
        
        time.sleep(BASE_DELAY_SECONDS)
        self.test_app_details(csgo_appid)
        
        # A placeholder for the reviews test if it were to be re-implemented.
        # self.test_reviews(csgo_appid) 
        
        time.sleep(BASE_DELAY_SECONDS)
        # The rate limit test uses the full list of apps fetched earlier.
        self.test_rate_limiting(all_apps)

        logging.info("✅ Steam API Test Suite Complete")

# --- Script Entry Point ---
def main():
    """Main function to parse arguments and execute the corresponding tests."""
    
    # argparse provides a professional command-line interface with minimal effort.
    # It handles argument parsing, validation, and automatically generates help messages.
    parser = argparse.ArgumentParser(
        description="A testing suite for the Steam Web API.",
        epilog="If no command is specified, the 'full' test suite will be run by default."
    )
    # Subparsers are used to create distinct commands (like git's 'commit', 'push', etc.).
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Define the 'full' command.
    subparsers.add_parser('full', help='Run the full, end-to-end test suite.')

    # Define the 'applist' command.
    subparsers.add_parser('applist', help='Test the GetAppList endpoint.')

    # Define the 'details' command, which requires an additional argument.
    details_parser = subparsers.add_parser('details', help='Test the appdetails endpoint for a specific AppID.')
    # 'type=int' tells argparse to automatically validate that the input is an integer.
    details_parser.add_argument('appid', type=int, help='The numeric AppID of the application.')

    # This line parses the command-line arguments (like ['details', '730']).
    args = parser.parse_args()

    # Instantiate the main class.
    tester = SteamAPITester(STEAM_API_KEY)

    # Simple logic to route the parsed command to the correct class method.
    if args.command == "applist":
        tester.test_app_list()
    elif args.command == "details":
        tester.test_app_details(args.appid)
    elif args.command == "full":
        tester.run_full_test()
    else:
        # This provides a sensible default action if the user runs the script with no arguments.
        tester.run_full_test()

# The `if __name__ == "__main__":` block is a standard Python convention.
# It ensures that the code inside it only runs when the script is executed directly,
# not when it's imported as a module into another script.
if __name__ == "__main__":
    main()
