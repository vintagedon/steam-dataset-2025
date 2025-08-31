# =====================================================================================================================
# Script Name:    analyze_steam_data_schema.py
# Description:    Analyzes a JSON file from the Steam API to produce a detailed schema report. This script
#                 traverses the data structure, identifies all unique fields, infers their data types and
#                 presence, calculates summary statistics, and generates a recommended PostgreSQL schema.
#                 The output is designed to inform database design and data science exploration.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        1.0
# Date:           2025-08-31
# License:        MIT License
#
# Usage:          python analyze_steam_data_schema.py <input_json_file> --output <report_markdown_file>
#                 Example: python analyze_steam_data_schema.py steam_data_sample.json --output schema_report.md
#
# =====================================================================================================================
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-08-31      1.0             vintagedon      Initial release.
#
# =====================================================================================================================

import json
import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple

# --- Type Mapping for PostgreSQL ---
# This dictionary provides a clean mapping from Python types to appropriate PostgreSQL types.
# Using BIGINT for integers is a safe default for IDs.
# TEXT is highly flexible for string data of unknown length.
# JSONB is the critical choice for nested objects/arrays, as it's indexed and highly performant.
TYPE_TO_POSTGRES = {
    'str': 'TEXT',
    'int': 'BIGINT',
    'float': 'NUMERIC',
    'bool': 'BOOLEAN',
    'dict': 'JSONB',
    'list': 'JSONB',
    'NoneType': 'TEXT' # Could be any type, TEXT is a safe bet
}

class SchemaAnalyzer:
    """
    Encapsulates the logic for loading, analyzing, and reporting on the Steam data schema.
    """
    def __init__(self, json_file_path: Path):
        """Initializes the analyzer and loads the source data."""
        self.file_path = json_file_path
        self.data = self._load_data()
        if not self.data:
            raise ValueError("Failed to load or parse JSON data.")

        self.games = self.data.get('games', [])
        # A defaultdict simplifies the process of aggregating field statistics.
        # It automatically creates an entry for a new field, avoiding KeyError checks.
        self.field_stats = defaultdict(lambda: {
            'types': set(),
            'count': 0,
            'non_null_count': 0,
            'examples': set()
        })

    def _load_data(self) -> Dict[str, Any]:
        """Loads and parses the JSON file, with robust error handling."""
        print(f"Attempting to load data from: {self.file_path}")
        if not self.file_path.is_file():
            print(f"Error: File not found at '{self.file_path}'", file=sys.stderr)
            return {}
        try:
            with self.file_path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{self.file_path}'. {e}", file=sys.stderr)
        except IOError as e:
            print(f"Error: Could not read file '{self.file_path}'. {e}", file=sys.stderr)
        return {}

    def analyze(self):
        """Main method to run the full analysis process."""
        if not self.games:
            print("Warning: No 'games' array found in the JSON file.", file=sys.stderr)
            return

        print(f"Analyzing {len(self.games)} records...")
        for record in self.games:
            # The heart of the analysis is this recursive traversal.
            self._traverse(record, '')
        print("Analysis complete.")

    def _traverse(self, node: Any, path: str):
        """
        Recursively traverses the JSON structure to identify and profile each field.
        - node: The current dictionary or list being inspected.
        - path: The dot-notation path to the current node (e.g., 'app_details.data').
        """
        # Base case: If the node is not a dictionary, we can't traverse further down this path.
        if not isinstance(node, dict):
            return

        for key, value in node.items():
            current_path = f"{path}.{key}" if path else key
            
            # Record statistics for the current field.
            stats = self.field_stats[current_path]
            stats['count'] += 1
            node_type = type(value).__name__
            stats['types'].add(node_type)

            if value is not None and value != '' and value != []:
                stats['non_null_count'] += 1
                # Collect a few non-sensitive examples for context in the report.
                if len(stats['examples']) < 3 and node_type in ['str', 'int', 'bool']:
                    stats['examples'].add(str(value))

            # Recursive step: If the value is a dictionary, traverse into it.
            if isinstance(value, dict):
                self._traverse(value, current_path)
            # If the value is a list containing dictionaries, traverse into the first one
            # to analyze the sub-structure. This assumes list items have a consistent schema.
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # We add a '[*]' to the path to signify an array of objects.
                self._traverse(value[0], f"{current_path}[*]")

    def calculate_summary_stats(self) -> Dict[str, Any]:
        """Calculates high-level statistics about the dataset."""
        total_records = len(self.games)
        successful_details = sum(1 for g in self.games if g.get('app_details', {}).get('success'))
        games_identified = sum(1 for g in self.games if g.get('app_details', {}).get('data', {}).get('type') == 'game')
        free_games = sum(1 for g in self.games if g.get('app_details', {}).get('data', {}).get('is_free'))

        return {
            "Total Records Analyzed": total_records,
            "Records with Successful API Details": f"{successful_details} ({successful_details/total_records:.1%})",
            "Records Identified as 'Game'": f"{games_identified} ({games_identified/total_records:.1%})",
            "Free Games": f"{free_games} ({free_games/games_identified:.1%})" if games_identified > 0 else "0 (0.0%)",
        }

    def generate_report(self) -> str:
        """Generates a comprehensive Markdown report from the analysis."""
        print("Generating report...")
        report_lines = ["# Steam API Data Schema Analysis Report"]
        
        # --- Summary Section ---
        summary_stats = self.calculate_summary_stats()
        report_lines.append("\n## 1. Dataset Summary")
        report_lines.append("| Metric                             | Value |")
        report_lines.append("| :----------------------------------- | :---- |")
        for key, value in summary_stats.items():
            report_lines.append(f"| {key} | {value} |")

        # --- Field Analysis and Schema Section ---
        report_lines.append("\n## 2. Field Analysis & PostgreSQL Schema Recommendation")
        report_lines.append("This table details every field discovered in the dataset.")
        report_lines.append("- **Presence**: How often the field appeared across all analyzed records.")
        report_lines.append("- **Data Types**: The Python data types observed for this field.")
        report_lines.append("- **Recommended PG Type**: A suggested PostgreSQL column type. `JSONB` is recommended for any nested or array structures.")
        report_lines.append("\n| Field Path (Dot Notation) | Presence | Non-Null | Data Types | Recommended PG Type | Notes / Examples |")
        report_lines.append("| :-------------------------- | :------- | :------- | :--------- | :------------------ | :--------------- |")

        total_records = len(self.games)
        for path in sorted(self.field_stats.keys()):
            stats = self.field_stats[path]
            presence = stats['count'] / total_records
            non_null = stats['non_null_count'] / stats['count'] if stats['count'] > 0 else 0
            types_str = ", ".join(sorted(list(stats['types'])))
            
            # --- PostgreSQL Type Inference Logic ---
            pg_type = self._infer_postgres_type(stats['types'])
            examples = ", ".join(stats['examples'])

            report_lines.append(
                f"| `{path}` | {presence:.1%} | {non_null:.1%} | {types_str} | **{pg_type}** | {examples} |"
            )
        
        report_lines.append("\n### Notes on PostgreSQL Schema:")
        report_lines.append("- **Primary Key**: `appid` is the clear candidate for a `PRIMARY KEY`.")
        report_lines.append("- **TEXT vs. VARCHAR**: `TEXT` is used as a safe default for strings of unknown length. It has no performance penalty compared to `VARCHAR` in modern PostgreSQL.")
        report_lines.append("- **JSONB**: This type is crucial. It stores JSON in a decomposed binary format, which allows it to be queried and indexed efficiently. Fields like `app_details.data` or `reviews` should be stored in a single `JSONB` column rather than flattening them into dozens of SQL columns.")

        return "\n".join(report_lines)

    def _infer_postgres_type(self, types: Set[str]) -> str:
        """Infers the best PostgreSQL type from a set of observed Python types."""
        if 'dict' in types or 'list' in types:
            return 'JSONB'
        if 'float' in types: # If any float is seen, promote to numeric
            return 'NUMERIC'
        if 'int' in types:
            return 'BIGINT'
        if 'bool' in types:
            return 'BOOLEAN'
        if 'str' in types:
            return 'TEXT'
        return 'TEXT' # Default fallback

def main():
    """Main function to parse arguments and run the analyzer."""
    parser = argparse.ArgumentParser(
        description="Analyze a Steam API JSON data file and generate a schema report.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_file", type=Path, help="Path to the input JSON file (e.g., steam_data_sample.json)")
    parser.add_argument("-o", "--output", type=Path, default="schema_report.md", help="Path to the output Markdown report file.")
    args = parser.parse_args()

    try:
        analyzer = SchemaAnalyzer(args.input_file)
        analyzer.analyze()
        report = analyzer.generate_report()

        # Output to terminal
        print("\n" + "="*80)
        print("                        SCHEMA ANALYSIS REPORT")
        print("="*80 + "\n")
        # For terminal, we'll print a simplified version
        summary_stats = analyzer.calculate_summary_stats()
        print("--- DATASET SUMMARY ---")
        for key, value in summary_stats.items():
            print(f"{key+':':<38} {value}")
        print("\n--- TOP-LEVEL FIELDS DISCOVERED ---")
        for path in sorted(analyzer.field_stats.keys()):
             if '.' not in path: # Just show top-level fields for brevity
                 print(f"- {path}")
        print(f"\nFull detailed report saved to: {args.output}")

        # Save full report to markdown file
        with args.output.open('w', encoding='utf-8') as f:
            f.write(report)

    except (ValueError, FileNotFoundError) as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
