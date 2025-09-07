# =====================================================================================================================
# Script Name:    analyze_json_structure.py
# Description:    A memory-efficient script to analyze the structure of large JSON files by streaming.
#                 It reports the total number of records, prints a sample of the first few records, and
#                 provides a statistical summary of key presence to diagnose structural issues without
#                 loading the entire file into memory.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        1.0
# Date:           2025-09-02
# License:        MIT License
#
# Usage:          python analyze_json_structure.py /path/to/your_file.json
#
# =====================================================================================================================
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-09-02      1.0             vintagedon      Initial release. Designed specifically to handle multi-gigabyte
#                                                   JSON files from the full-scale data collection.
# =====================================================================================================================

import sys
import argparse
from pathlib import Path
from collections import Counter

# A try-except block for imports provides a clean, user-friendly exit if dependencies are missing.
try:
    import ijson
    from tqdm import tqdm
except ImportError:
    print("Error: Required libraries 'ijson' or 'tqdm' are not installed.", file=sys.stderr)
    print("Please run: pip install ijson tqdm", file=sys.stderr)
    sys.exit(1)

def analyze_json_stream(file_path: Path):
    """
    Streams a large JSON file to analyze its structure without loading it all into memory.
    
    The key to this function's efficiency is `ijson`. Unlike the standard `json` library
    which performs a full parse (loading the entire file), `ijson` is an iterative parser.
    It reads the file piece by piece and yields items as it finds them, meaning its memory
    footprint is constant and very small, regardless of whether the file is 100MB or 100GB.
    This is the standard, professional approach for handling massive JSON datasets.
    """
    print(f"--- Starting Structural Analysis of '{file_path.name}' ---")
    
    # These keys represent the "ground truth" we expect in every record.
    # We will count their presence to detect any structural degradation in the dataset.
    keys_to_check = ['appid', 'name_from_applist', 'app_details', 'reviews']
    key_counter = Counter()
    total_records = 0
    
    try:
        with file_path.open('rb') as f:
            # We target 'games.item' which tells ijson to yield each object inside the "games" array.
            # This is the entry point for our stream.
            games_stream = ijson.items(f, 'games.item')
            
            print("\n--- Sample Records (First 3) ---")
            for i, record in enumerate(tqdm(games_stream, desc="Streaming records")):
                total_records += 1
                
                # Print the first few records to give a human a "feel" for the data structure.
                if i < 3:
                    print(json.dumps(record, indent=2))
                    if i == 2: print("...")

                # For every record, check for the presence of our core keys.
                for key in keys_to_check:
                    if key in record and record[key] is not None:
                        key_counter[key] += 1
        
        print("\n--- Analysis Complete ---")
        print(f"\nTotal Records Found: {total_records:,}")

        print("\n--- Key Presence Statistics ---")
        print(f"{'Key Name':<25} | {'Presence Count':<20} | {'Presence %':<15}")
        print(f"{'-'*25} | {'-'*20} | {'-'*15}")
        
        for key in keys_to_check:
            count = key_counter.get(key, 0)
            percentage = (count / total_records * 100) if total_records > 0 else 0
            print(f"{key:<25} | {count:<20,} | {percentage:.2f}%")

        # This final check provides a clear go/no-go signal. If core fields are missing
        # from a significant portion of the dataset, it indicates a problem in the
        # collection or merge process that must be investigated.
        if key_counter.get('app_details', 0) / total_records < 0.95:
             print("\nWARNING: A significant number of records may be missing the 'app_details' object.")
        else:
             print("\nSUCCESS: Core data structure appears intact.")

    except ijson.JSONError as e:
        print(f"\nFATAL: A JSON parsing error occurred: {e}", file=sys.stderr)
        print("The file may be corrupted or incomplete.", file=sys.stderr)
    except FileNotFoundError:
        print(f"\nFATAL: File not found at '{file_path}'", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Analyze the structure of a large Steam JSON data file via streaming.")
    parser.add_argument("input_file", type=Path, help="Path to the JSON file to be analyzed.")
    args = parser.parse_args()

    analyze_json_stream(args.input_file)

if __name__ == "__main__":
    main()
