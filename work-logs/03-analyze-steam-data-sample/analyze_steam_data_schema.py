# =================================================================================================
# Script:        analyze_steam_data_schema.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       1.0
# Created:       2025-08-31
# Last Updated:  2025-09-28
#
# Purpose:
#   Traverse a Session-02/03 JSON artifact, profile fields (presence, non-null, type),
#   and render a Markdown schema recommendation for PostgreSQL (flat + JSONB guidance).
#
# Inputs:
#   - CLI: input JSON path; -o/--output for report path
# Outputs:
#   - Markdown: schema_report.md (or timestamped name depending on variant)
#
# Operational Profile:
#   - Runtime Context: {python: 3.9+}
#   - Idempotency: {safe_rerun: true}
#   - Failure Modes: {file_not_found, json_decode_error}
#
# Data Lineage & Provenance:
#   SOURCE_OF_TRUTH: "steam_data_*.json" (from Session 02/03 samplers)
#   READS: ["games[*].appid", "games[*].app_details"]
#   WRITES: ["schema_report_*.md"]
#
# Security & Compliance:
#   - No secrets required; file-only analysis.
#
# Change Log:
#   - 2025-09-28  Added standardized header + dual-audience comments (no code changes).
# =================================================================================================

# (existing file content below is unchanged except for comments at the top)
# ---------------------------------------------------------------------------------------------------------------------
# Existing header/comments preserved from submitted script…
# ---------------------------------------------------------------------------------------------------------------------

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
# HUMAN: conservative mapping; nested structs → JSONB for agility, selective GIN indexing downstream.
# ML:    TYPE_MAP = {"str":TEXT,"int":BIGINT,"float":NUMERIC,"bool":BOOLEAN,"dict|list":JSONB,"NoneType":TEXT}
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
    """Load → traverse → aggregate field stats → render Markdown. No side effects on source files."""
    def __init__(self, json_file_path: Path):
        self.file_path = json_file_path
        self.data = self._load_data()
        if not self.data:
            raise ValueError("Failed to load or parse JSON data.")

        self.games = self.data.get('games', [])
        # per-field aggregator (counts, examples)
        self.field_stats = defaultdict(lambda: {
            'types': set(),
            'count': 0,
            'non_null_count': 0,
            'examples': set()
        })

    def _load_data(self) -> Dict[str, Any]:
        """Open + parse with explicit errors for triage; returns {} on failure."""
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
        """Depth-first traversal (dot paths; lists as [*]) to collect coverage + examples."""
        if not self.games:
            print("Warning: No 'games' array found in the JSON file.", file=sys.stderr)
            return

        print(f"Analyzing {len(self.games)} records...")
        for record in self.games:
            self._traverse(record, '')
        print("Analysis complete.")

    def _traverse(self, node: Any, path: str):
        """Recurse on dicts; sample first element for list-of-dicts to learn sub-structure."""
        if not isinstance(node, dict):
            return

        for key, value in node.items():
            current_path = f"{path}.{key}" if path else key
            
            stats = self.field_stats[current_path]
            stats['count'] += 1
            node_type = type(value).__name__
            stats['types'].add(node_type)

            if value is not None and value != '' and value != []:
                stats['non_null_count'] += 1
                if len(stats['examples']) < 3 and node_type in ['str', 'int', 'bool']:
                    stats['examples'].add(str(value))

            if isinstance(value, dict):
                self._traverse(value, current_path)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                self._traverse(value[0], f"{current_path}[*]")

    def calculate_summary_stats(self) -> Dict[str, Any]:
        """Headline metrics reused by console and report; free% is % of games."""
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
        """Markdown report with summary + per-field table + PG recommendations."""
        print("Generating report...")
        report_lines = ["# Steam API Data Schema Analysis Report"]
        
        summary_stats = self.calculate_summary_stats()
        report_lines.append("\n## 1. Dataset Summary")
        report_lines.append("| Metric                             | Value |")
        report_lines.append("| :----------------------------------- | :---- |")
        for key, value in summary_stats.items():
            report_lines.append(f"| {key} | {value} |")

        report_lines.append("\n## 2. Field Analysis & PostgreSQL Schema Recommendation")
        report_lines.append("This table details every field discovered in the dataset.")
        report_lines.append("- **Presence**: How often the field appeared across all analyzed records.")
        report_lines.append("- **Data Types**: The Python data types observed for this field.")
        report_lines.append("- **Recommended PG Type**: JSONB for nested/array structures.")
        report_lines.append("\n| Field Path (Dot Notation) | Presence | Non-Null | Data Types | Recommended PG Type | Notes / Examples |")
        report_lines.append("| :-------------------------- | :------- | :------- | :--------- | :------------------ | :--------------- |")

        total_records = len(self.games)
        for path in sorted(self.field_stats.keys()):
            stats = self.field_stats[path]
            presence = stats['count'] / total_records
            non_null = stats['non_null_count'] / stats['count'] if stats['count'] > 0 else 0
            types_str = ", ".join(sorted(list(stats['types'])))
            
            pg_type = self._infer_postgres_type(stats['types'])
            examples = ", ".join(stats['examples'])

            report_lines.append(
                f"| `{path}` | {presence:.1%} | {non_null:.1%} | {types_str} | **{pg_type}** | {examples} |"
            )
        
        report_lines.append("\n### Notes on PostgreSQL Schema:")
        report_lines.append("- **Primary Key**: `appid` as `PRIMARY KEY`.")
        report_lines.append("- **TEXT vs. VARCHAR**: prefer `TEXT`; length constraints rarely help here.")
        report_lines.append("- **JSONB**: keep nested payloads (e.g., `app_details.data`), index selectively (GIN).")

        return "\n".join(report_lines)

    def _infer_postgres_type(self, types: Set[str]) -> str:
        """Heuristic: prefer JSONB for complex; otherwise numeric/bool/text as seen."""
        if 'dict' in types or 'list' in types:
            return 'JSONB'
        if 'float' in types:
            return 'NUMERIC'
        if 'int' in types:
            return 'BIGINT'
        if 'bool' in types:
            return 'BOOLEAN'
        if 'str' in types:
            return 'TEXT'
        return 'TEXT'

def main():
    """CLI wrapper around analysis/report; defaults retained from original."""
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

        print("\n" + "="*80)
        print("                        SCHEMA ANALYSIS REPORT")
        print("="*80 + "\n")

        summary_stats = analyzer.calculate_summary_stats()
        print("--- DATASET SUMMARY ---")
        for key, value in summary_stats.items():
            print(f"{key+':':<38} {value}")
        print("\n--- TOP-LEVEL FIELDS DISCOVERED ---")
        for path in sorted(analyzer.field_stats.keys()):
             if '.' not in path:
                 print(f"- {path}")
        print(f"\nFull detailed report saved to: {args.output}")

        with args.output.open('w', encoding='utf-8') as f:
            f.write(report)

    except (ValueError, FileNotFoundError) as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
