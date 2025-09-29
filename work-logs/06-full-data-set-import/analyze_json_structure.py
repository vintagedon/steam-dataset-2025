# =================================================================================================
# File:          analyze_json_structure.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Stream large JSON arrays to profile structure, sample records, and key presence stats.
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
# Script Name:    analyze_json_structure.py
# Description:    A memory-efficient script to analyze the structure of large JSON files by streaming.
#                 It reports the total number of records, prints a sample of the first few records, and
#                 provides a statistical summary of key presence to diagnose structural issues.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.comcom/vintagedon/steam-dataset-2025
#
# Version:        1.1
# Date:           2025-09-07
# License:        MIT License
#
# Usage:          python analyze_json_structure.py /path/to/your_file.json
#
# =====================================================================================================================
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-09-07      1.0             vintagedon      Initial release.
#   2025-09-07      1.1             vintagedon      BUGFIX: Added a custom JSON encoder to handle the 'Decimal'
#                                                   type found in review data, preventing serialization errors.
# =====================================================================================================================
# --- Imports --------------------------------------------------------------------------------------
# Human: Group stdlib vs third-party; fail fast with helpful install hints.
# ML:    DEPENDS_ON — capture runtime libs for reproducibility.
import sys
import json
import argparse
from pathlib import Path
from collections import Counter
from decimal import Decimal

try:
    import ijson
    from tqdm import tqdm
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install tqdm ijson", file=sys.stderr)
    sys.exit(1)

# --- Core Component -------------------------------------------------------------------------------
# Human: Single responsibility; easier to test and reason about.
# ML:    CONTRACT — stable method IO for downstream automation.
class CustomJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle data types that the default encoder doesn't, like Decimal.
    """
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Convert Decimal to a float for JSON serialization.
            # This is acceptable for display/analysis purposes.
            return float(obj)
        return super().default(obj)

def analyze_file(file_path: Path):
    """Analyzes a given JSON file and prints a report."""
    if not file_path.is_file():
        print(f"Error: File not found at '{file_path}'")
        return

    print("=" * 80)
    print(f"ANALYSIS REPORT FOR: {file_path.name}")
    print("=" * 80)

    try:
        # --- Count total records first ---
        print("\n[Phase 1/3] Counting total records...")
        with file_path.open('rb') as f:
            record_count = sum(1 for _ in tqdm(ijson.items(f, 'item'), desc="Counting records"))
        print(f"Total records found: {record_count:,}")

        if record_count == 0:
            print("File contains no records to analyze.")
            return

        # --- Print sample records ---
        print("\n[Phase 2/3] Displaying first 3 records...")
        with file_path.open('rb') as f:
            parser = ijson.items(f, 'item')
            for i, record in enumerate(parser):
                if i < 3:
                    print(f"\n--- Record {i+1} ---")
                    # Use the custom encoder to prevent crashes on Decimal types
                    print(json.dumps(record, indent=2, cls=CustomJSONEncoder))
                else:
                    break
        
        # --- Analyze Key Presence ---
        print("\n[Phase 3/3] Analyzing key presence statistics...")
        with file_path.open('rb') as f:
            key_counter = Counter()
            parser = ijson.items(f, 'item')
            for record in tqdm(parser, total=record_count, desc="Analyzing keys"):
                if isinstance(record, dict):
                    keys = list(record.keys())
                    key_counter.update(keys)

            print("\n--- Top-Level Key Presence ---")
            print(f"{'Key Name':<35} {'Occurrences':<20} {'Percentage':<10}")
            print(f"{'-'*35:<35} {'-'*20:<20} {'-'*10:<10}")
            for key, count in key_counter.most_common():
                percentage = (count / record_count) * 100
                print(f"{key:<35} {count:<20,} {percentage:>9.2f}%")

    except Exception as e:
        print(f"\nAn error occurred during analysis: {e}")

    print("\n" + "=" * 80)
    print("Analysis complete.")


# --- Orchestration -------------------------------------------------------------------------------
# Human: Wire components; parse args; validate env; run safely.
# ML:    ENTRYPOINT(main) — transactional operations; robust error handling.
def main():
    parser = argparse.ArgumentParser(
        description="Analyze the structure of a large JSON file containing an array of objects.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("file_path", type=Path, help="Path to the JSON file to analyze.")
    args = parser.parse_args()
    analyze_file(args.file_path)

# --- Entry Point -----------------------------------------------------------------------------------
# Human: Direct CLI execution path with actionable errors.
# ML:    RUNTIME_START — begin telemetry if needed.
if __name__ == "__main__":
    main()
