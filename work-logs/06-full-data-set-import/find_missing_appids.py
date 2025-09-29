# =================================================================================================
# File:          find_missing_appids.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Compare master reviews JSON vs DB applications to produce a backfill appid list.
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

# --- Imports --------------------------------------------------------------------------------------
# Human: Group stdlib vs third-party; fail fast with helpful install hints.
# ML:    DEPENDS_ON — capture runtime libs for reproducibility.
import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Set

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
# --- Configuration & Setup ------------------------------------------------------------------------
# Human: Centralize env + logging knobs to keep core logic clean/testable.
# ML:    CONFIG_KEYS — parse constants/env names for orchestration.
load_dotenv(dotenv_path=CWD / '.env')

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Core Component -------------------------------------------------------------------------------
# Human: Fetch appids from DB for set membership checks.
# ML:    CONTRACT(db->set[int])
def db_name: str) -> Set[int]:
    """Connects to the database and fetches the set of all existing appids."""
    logging.info(f"Connecting to database '{db_name}' to fetch existing application IDs...")
    conn_config = {
        'host': os.getenv('PG_HOST'), 'port': os.getenv('PG_PORT'), 'dbname': db_name,
        'user': os.getenv('PG_APP_USER'), 'password': os.getenv('PG_APP_USER_PASSWORD')
    }
    try:
        with psycopg2.connect(**conn_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT appid FROM applications;")
                existing_appids = {row[0] for row in cursor.fetchall()}
                logging.info(f"Found {len(existing_appids):,} existing applications in the database.")
                return existing_appids
    except psycopg2.Error as e:
        logging.error(f"FATAL: Could not connect to or query the database. Error: {e}")
        sys.exit(1)

# --- Core Component -------------------------------------------------------------------------------
# Human: Compute set difference between sources.
# ML:    CONTRACT(reviews:set - existing:set)
def reviews_file: Path, existing_appids: Set[int]) -> Set[int]:
    """Streams the reviews file and finds appids that are not in the existing set."""
    logging.info(f"Streaming '{reviews_file.name}' to find appids with reviews...")
    review_appids = set()
    try:
        with reviews_file.open('rb') as f:
            for record in tqdm(ijson.items(f, 'item'), desc="Scanning reviews file"):
                appid = record.get('appid')
                if appid:
                    review_appids.add(appid)
    except (ijson.JSONError, IOError) as e:
        logging.error(f"FATAL: Could not read or parse reviews file. Error: {e}")
        sys.exit(1)
    
    logging.info(f"Found {len(review_appids):,} unique appids in the reviews file.")
    
    missing_ids = review_appids - existing_appids
    return missing_ids

# --- Orchestration -------------------------------------------------------------------------------
# Human: Wire components; parse args; validate env; run safely.
# ML:    ENTRYPOINT(main) — transactional operations; robust error handling.
def main():
    parser = argparse.ArgumentParser(
        description="Find appids present in the reviews file but missing from the database.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("database_name", help="Name of the target database (e.g., 'steamfull').")
    parser.add_argument("--reviews_file", type=Path, required=True, help="Path to the master reviews JSON file.")
    args = parser.parse_args()

    existing_ids = get_existing_appids(args.database_name)
    missing_ids = find_missing_ids(args.reviews_file, existing_ids)

    if not missing_ids:
        logging.info("🎉 Success! No applications with reviews are missing from the database.")
        return

    output_file = CWD / "missing_appids.txt"
    logging.warning(f"Found {len(missing_ids)} appids with reviews that are missing from the 'applications' table.")
    
    try:
        with output_file.open('w', encoding='utf-8') as f:
            for appid in sorted(list(missing_ids)):
                f.write(f"{appid}\n")
        logging.info(f"List of missing appids has been saved to: {output_file}")
        logging.info("You can now use this file to perform a targeted re-collection of game data.")
    except IOError as e:
        logging.error(f"Failed to write output file. Error: {e}")

# --- Entry Point -----------------------------------------------------------------------------------
# Human: Direct CLI execution path with actionable errors.
# ML:    RUNTIME_START — begin telemetry if needed.
if __name__ == "__main__":
    main()
