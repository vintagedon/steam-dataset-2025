# =====================================================================================================================
# Script Name:    find_missing_appids.py
# Description:    A diagnostic script to identify applications that are present in the reviews dataset but
#                 missing from the applications table in the database. This is used to create a list of
#                 appids for a targeted re-collection run.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        1.0
# Date:           2025-09-07
# License:        MIT License
#
# Usage:          python find_missing_appids.py <database_name> --reviews_file /path/to/reviews.json
#
# =====================================================================================================================
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-09-07      1.0             vintagedon      Initial release of the data reconciliation script.
#
# =====================================================================================================================

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Set

# A try-except block for third-party imports provides a clean, user-friendly exit.
try:
    import psycopg2
    from dotenv import load_dotenv
    from tqdm import tqdm
    import ijson
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install psycopg2-binary python-dotenv tqdm ijson", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
CWD = Path.cwd()
load_dotenv(dotenv_path=CWD / '.env')

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-m-%d %H:%M:%S'
)

def get_existing_appids(db_name: str) -> Set[int]:
    """
    Connects to the PostgreSQL database and fetches the set of all existing appids.
    
    Why a Set? Using a Python `set` is a critical performance optimization. It provides
    O(1) average time complexity for lookups, making the final comparison against
    the millions of review appids extremely fast. A list, by contrast, would have
    O(n) complexity, making the script unfeasibly slow.
    """
    logging.info(f"Connecting to database '{db_name}' to fetch existing application IDs...")
    conn_config = {
        'host': os.getenv('PG_HOST'), 'port': os.getenv('PG_PORT'), 'dbname': db_name,
        'user': os.getenv('PG_APP_USER'), 'password': os.getenv('PG_APP_USER_PASSWORD')
    }
    try:
        with psycopg2.connect(**conn_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT appid FROM applications;")
                # The set comprehension is a concise and efficient way to build the set from the query results.
                existing_appids = {row[0] for row in cursor.fetchall()}
                logging.info(f"Found {len(existing_appids):,} existing applications in the database.")
                return existing_appids
    except psycopg2.Error as e:
        logging.error(f"FATAL: Could not connect to or query the database. Error: {e}")
        sys.exit(1)

def find_missing_ids(reviews_file: Path, existing_appids: Set[int]) -> Set[int]:
    """
    Streams the large reviews JSON file to find all unique appids present within it,
    then calculates the set difference to find which ones are missing from the database.
    """
    logging.info(f"Streaming '{reviews_file.name}' to find appids with reviews...")
    review_appids = set()
    try:
        with reviews_file.open('rb') as f:
            # The key to this function's efficiency is `ijson`. Unlike the standard `json` library
            # which performs a full parse (loading the entire file into RAM), `ijson` is an iterative
            # parser. It reads the file piece by piece, which means its memory footprint is constant
            # and very small, regardless of the file's size. This is the standard professional
            # approach for handling massive JSON datasets.
            # We target 'item' because we assume the root of the JSON is an array of objects.
            for record in tqdm(ijson.items(f, 'item'), desc="Scanning reviews file"):
                appid = record.get('appid')
                if appid:
                    review_appids.add(appid)
    except (ijson.JSONError, IOError) as e:
        logging.error(f"FATAL: Could not read or parse reviews file. Error: {e}")
        sys.exit(1)
    
    logging.info(f"Found {len(review_appids):,} unique appids in the reviews file.")
    
    # This is the core reconciliation logic. The `-` operator on sets performs a highly
    # optimized set difference operation, efficiently finding all items in `review_appids`
    # that are not in `existing_appids`.
    missing_ids = review_appids - existing_appids
    return missing_ids

def main():
    """Main function to orchestrate the diagnostic process."""
    parser = argparse.ArgumentParser(
        description="Find appids present in a reviews JSON file but missing from the database.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("database_name", help="Name of the target database (e.g., 'steamfull').")
    parser.add_argument("--reviews_file", type=Path, required=True, help="Path to the master reviews JSON file.")
    args = parser.parse_args()

    # --- Phase 1: Get the current state from the database ---
    existing_ids = get_existing_appids(args.database_name)
    
    # --- Phase 2: Compare against the source data ---
    missing_ids = find_missing_ids(args.reviews_file, existing_ids)

    # --- Phase 3: Report the findings and generate an actionable artifact ---
    if not missing_ids:
        logging.info("🎉 Success! No applications with reviews are missing from the database.")
        return

    output_file = CWD / "missing_appids.txt"
    logging.warning(f"Found {len(missing_ids)} appids with reviews that are missing from the 'applications' table.")
    
    try:
        # The script's output is not just a report, but a tool. This text file is designed
        # to be used as a direct input for a targeted re-collection script, embodying the
        # UNIX philosophy of small, interoperable tools.
        with output_file.open('w', encoding='utf-8') as f:
            for appid in sorted(list(missing_ids)):
                f.write(f"{appid}\n")
        logging.info(f"List of missing appids has been saved to: {output_file}")
        logging.info("You can now use this file to perform a targeted re-collection of game data.")
    except IOError as e:
        logging.error(f"Failed to write output file. Error: {e}")

if __name__ == "__main__":
    main()
