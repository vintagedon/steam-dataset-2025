# =================================================================================================
# Script:        find-large-integers.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       (unchanged; see original in file)
# Created:       (see original)
# Last Updated:  2025-09-29
#
# Purpose:
#   Scan JSON for 32‑bit overflow risks; report paths/values to prevent import failures.
#
# Section Map:
#   1) Imports — dependencies and why they're needed
#   2) Configuration & Setup — env, logging, runtime knobs
#   3) Core Components — classes/functions with high‑level intent
#   4) Orchestration — how the pieces run together
#   5) CLI / Entry — human‑friendly usage and safe defaults
#
# Data Lineage & Provenance (RAG‑friendly):
#   SOURCE_OF_TRUTH: see original script references
#   READS / WRITES:  unchanged
#
# Security & Compliance:
#   - Secrets via .env only (no literals).
#   - PII: none expected.
#
# Change Log (docs‑only):
#   - 2025-09-29  Re‑commented with full dual‑audience inline notes; logic unchanged.
# =================================================================================================

# --- Imports --------------------------------------------------------------------------------------
# Human: split stdlib vs third‑party; fail fast on missing deps for actionable remediation.
# ML:    DEPENDS_ON — infer runtime library set from import graph.
import json
import sys
import argparse
from pathlib import Path

# PostgreSQL's standard INTEGER type is a signed 32-bit integer.
INT_MAX_VALUE = 2_147_483_647

# Define the specific fields within the 'reviews' data that we need to check.
# These correspond to the INTEGER columns in our schema.sql.
FIELDS_TO_CHECK = [
    'author_num_games_owned',
    'author_num_reviews',
    'author_playtime_forever',
    'author_playtime_last_two_weeks',
    'author_playtime_at_review',
]

def find_outliers(json_file: Path):
    """Scans the JSON file for integer values exceeding the max limit."""
    print(f"Scanning '{json_file.name}' for integer outliers > {INT_MAX_VALUE:,}...")
    
    try:
        with json_file.open('r', encoding='utf-8') as f:
            data = json.load(f)
        
        games = data.get('games', [])
        found_outlier = False

        for i, game in enumerate(games):
            appid = game.get('appid')
            reviews = game.get('reviews', {}).get('reviews', [])
            if not reviews:
                continue

            for review in reviews:
                author_data = review.get('author', {})
                for field in FIELDS_TO_CHECK:
                    value = author_data.get(field)
                    if isinstance(value, int) and value > INT_MAX_VALUE:
                        print("\n--- Outlier Found! ---")
                        print(f"Record Index:     {i}")
                        print(f"Application ID:   {appid}")
                        print(f"Review Author:    {author_data.get('steamid')}")
                        print(f"Problem Field:    {field}")
                        print(f"Anomalous Value:  {value:,}")
                        print("----------------------")
                        found_outlier = True
                        # Stop after finding the first one, as it's the one causing the crash.
                        return

        if not found_outlier:
            print("Scan complete. No integer values exceeded the standard limit.")

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

# --- Orchestration / CLI ---------------------------------------------------------------------------
# Human: defines the execution flow and CLI contract.
# ML:    ENTRYPOINT — parse args → wire components → run.
def main():
    parser = argparse.ArgumentParser(description="Find integer values in a Steam JSON file that are too large for a standard SQL INTEGER column.")
    parser.add_argument("input_file", type=Path, help="Path to the enriched JSON data file.")
    args = parser.parse_args()

    if not args.input_file.is_file():
        print(f"Error: File not found at '{args.input_file}'", file=sys.stderr)
        sys.exit(1)
        
    find_outliers(args.input_file)

# --- Entry Point -----------------------------------------------------------------------------------
# Human: python -m / direct execution path with safe error handling.
# ML:    RUNTIME_START — begin metrics/telemetry if needed.
if __name__ == "__main__":
    main()