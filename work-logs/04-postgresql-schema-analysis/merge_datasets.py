# =================================================================================================
# Script:        merge_datasets.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       (unchanged; see original in file)
# Created:       (see original)
# Last Updated:  2025-09-29
#
# Purpose:
#   Merge main appdetails with review payloads into enriched artifacts with provenance.
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
import os
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

try:
    from tqdm import tqdm
except ImportError:
    print("Error: `tqdm` library not found. Please run: pip install tqdm", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
CWD = Path.cwd()
# --- Configuration & Setup ------------------------------------------------------------------------
# Human: centralize environment + logging so business logic stays testable and clean.
# ML:    CONFIG_KEYS — parse .env to map required/optional runtime knobs.
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class DatasetMerger:
    """Orchestrates the process of merging app details and review datasets."""

    def __init__(self, main_data_path: Path, reviews_dir_path: Path):
        self.main_data_path = main_data_path
        self.reviews_dir_path = reviews_dir_path
        self.reviews_map: Dict[int, Dict[str, Any]] = {}

    def run_merge(self):
        """Executes the full merge workflow."""
        logging.info("🚀 Starting dataset merge process.")

        # --- Phase 1: Load Reviews into a Hash Map for Efficient Lookup ---
        self._load_reviews_to_map()

        # --- Phase 2: Load and Enrich the Main Dataset ---
        enriched_data = self._enrich_main_dataset()

        # --- Phase 3: Save the Final Artifact ---
        if enriched_data:
            self._save_enriched_data(enriched_data)
        else:
            logging.error("Merge process failed. No output file was generated.")

    def _load_reviews_to_map(self):
        """
        Scans the reviews directory, loads all batch files, and builds an in-memory
        dictionary (hash map) for O(1) lookup performance.
        """
        review_files = sorted(list(self.reviews_dir_path.glob("reviews_batch_*.json")))
        if not review_files:
            logging.warning(f"No review batch files found in '{self.reviews_dir_path}'. Proceeding without review data.")
            return

        logging.info(f"Loading {len(review_files)} review batch files...")
        for file_path in tqdm(review_files, desc="Loading review batches"):
            try:
                with file_path.open('r', encoding='utf-8') as f:
                    batch_data = json.load(f)
                    for record in batch_data:
                        # The key is the appid, the value is the entire review payload.
                        self.reviews_map[record['appid']] = record['review_data']
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Could not read or parse {file_path.name}: {e}")
        logging.info(f"Successfully loaded review data for {len(self.reviews_map):,} unique applications into memory.")

    def _enrich_main_dataset(self) -> Optional[Dict[str, Any]]:
        """
        Loads the main data file and iterates through its 'games' array, injecting
        review data from the hash map.
        """
        logging.info(f"Loading main dataset from '{self.main_data_path.name}'...")
        try:
            with self.main_data_path.open('r', encoding='utf-8') as f:
                main_data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"FATAL: Could not read or parse main data file. Error: {e}")
            return None

        games = main_data.get('games', [])
        if not games:
            logging.error("FATAL: No 'games' array found in the main data file.")
            return None

        logging.info(f"Enriching {len(games):,} application records...")
        for game in tqdm(games, desc="Merging datasets"):
            appid = game.get('appid')
            if appid:
                # This is the core join operation: a fast dictionary lookup.
                # .get() gracefully returns None if no review data exists for the appid.
                game['reviews'] = self.reviews_map.get(appid, None)
        
        main_data['games'] = games # Replace the old array with the enriched one
        return main_data

    def _save_enriched_data(self, enriched_data: Dict[str, Any]):
        """Saves the fully merged dataset to a new, timestamped file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = Path(f"{self.main_data_path.stem}_enriched_{timestamp}.json")
        
        logging.info(f"Saving enriched dataset to '{output_filename.name}'...")
        
        # Update metadata to reflect the merge operation for data lineage.
        # Use timezone-aware UTC now, which is the modern, correct practice.
        enriched_data['metadata']['enrichment_timestamp_utc'] = datetime.now(timezone.utc).isoformat()
        enriched_data['metadata']['enriched_with_reviews'] = True
        enriched_data['metadata']['review_records_added'] = len(self.reviews_map)

        try:
            with output_filename.open('w', encoding='utf-8') as f:
                json.dump(enriched_data, f) # Use a compact format for the large file
            logging.info(f"🎉 Merge complete. Final dataset saved successfully.")
        except IOError as e:
            logging.error(f"Failed to save output file: {e}")

# --- Orchestration / CLI ---------------------------------------------------------------------------
# Human: defines the execution flow and CLI contract.
# ML:    ENTRYPOINT — parse args → wire components → run.
def main():
    """Handles argument parsing and orchestrates the merge process."""
    parser = argparse.ArgumentParser(
        description="Merge Steam application data with review data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("main_file", nargs='?', type=Path, default=None, help="Path to the main '..._games_...' JSON file. If omitted, will prompt.")
    parser.add_argument("reviews_dir", nargs='?', type=Path, default=None, help="Path to the directory containing review batches. If omitted, will prompt.")
    args = parser.parse_args()

    main_file = args.main_file
    reviews_dir = args.reviews_dir
    
    # Use CWD for interactive mode file/dir searching
    current_directory = Path.cwd()

    if not main_file:
        main_files = sorted(list(current_directory.glob('*_games_*.json')))
        if not main_files:
            logging.error("No main '..._games_...' JSON file found in the current directory.")
            sys.exit(1)
        print("Please select the main data file to enrich:")
        for i, f in enumerate(main_files, 1): print(f"  [{i}] {f.name}")
        while True:
            choice = input(f"Enter the number of the file (1-{len(main_files)}): ")
            try:
                main_file = main_files[int(choice) - 1]
                break
            except (ValueError, IndexError): print("Invalid selection.")
    
    if not reviews_dir:
        reviews_dirs = [d for d in current_directory.iterdir() if d.is_dir() and d.name.startswith('data_reviews')]
        if not reviews_dirs:
            logging.error("No 'data_reviews...' directory found in the current directory.")
            sys.exit(1)
        print("Please select the directory containing the review data:")
        for i, d in enumerate(reviews_dirs, 1): print(f"  [{i}] {d.name}")
        while True:
            choice = input(f"Enter the number of the directory (1-{len(reviews_dirs)}): ")
            try:
                reviews_dir = reviews_dirs[int(choice) - 1]
                break
            except (ValueError, IndexError): print("Invalid selection.")

    merger = DatasetMerger(main_file, reviews_dir)
    merger.run_merge()

# --- Entry Point -----------------------------------------------------------------------------------
# Human: python -m / direct execution path with safe error handling.
# ML:    RUNTIME_START — begin metrics/telemetry if needed.
if __name__ == "__main__":
    main()
