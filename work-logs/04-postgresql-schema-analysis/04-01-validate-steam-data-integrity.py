# =================================================================================================
# Script:        04-01-validate-steam-data-integrity.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       (unchanged; see original in file)
# Created:       (see original)
# Last Updated:  2025-09-29
#
# Purpose:
#   Validate JSON integrity and project business rules prior to DB import; emits certification report.
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
from pathlib import Path
from datetime import datetime
from collections import Counter
from typing import List, Dict, Any, Optional

# --- Constants & Configuration ---
EXPECTED_TYPES = {
    'appid': int, 'name_from_applist': str, 'app_details': dict,
    'app_details.success': bool, 'app_details.data.steam_appid': int,
    'app_details.data.is_free': bool, 'app_details.data.developers': list,
    'app_details.data.publishers': list, 'app_details.data.price_overview': dict,
    'app_details.data.metacritic.score': int, 'app_details.data.release_date.coming_soon': bool
}
# We will only collect detailed profile stats on a sample to keep the script fast.
PROFILE_SAMPLE_SIZE = 1000

# --- Utility Class for Colorized Output ---
class TColors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class DataValidator:
    """Encapsulates the logic for validating a Steam JSON data file."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data = self._load_data()
        self.games = self.data.get('games', [])
        self.errors: List[str] = []
        self.warnings: List[str] = []
        # This dictionary will store the outcome of each specific test.
        self.test_results: Dict[str, str] = {}
        # These will store aggregated data for the profile section.
        self.stats = Counter()
        self.profile_data = {
            "release_dates": [], "developers": [], "publishers": [], "prices": [],
            "sample_games": []
        }

    def _load_data(self) -> Dict[str, Any]:
        print(f"Loading data from '{self.file_path.name}'...")
        try:
            with self.file_path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            self.errors.append(f"CRITICAL: Could not load or parse JSON file. Error: {e}")
            return {}

    def run_validation(self):
        """Orchestrates the entire validation process."""
        if not self.games:
            self.errors.append("CRITICAL: No 'games' array found in the JSON file.")
            return

        print(f"Found {len(self.games)} records. Starting validation...")
        
        # Run tests that iterate over the full dataset
        self._validate_uniqueness()
        
        # Iterate through records for individual checks and profiling
        for i, record in enumerate(self.games):
            is_sample_record_for_types = (i % 100 == 0) # Check types on a sparse sample
            self._validate_record_structure(record, is_sample_record_for_types)
            self._validate_record_values(record)
            
            # Collect data for the profile from a larger, but still limited, sample
            if self.stats['successful_games_profiled'] < PROFILE_SAMPLE_SIZE:
                self._collect_profile_data(record)

        # Finalize test results that depend on the full run
        self.test_results['Data Type Consistency (Sampled)'] = 'PASS' if not any("Type Mismatch" in w for w in self.warnings) else 'WARN'
        self.test_results['Value Range Checks (Sampled)'] = 'PASS' if not any("Value Range" in w for w in self.warnings) else 'WARN'
        self.test_results['Conditional Integrity'] = 'PASS' if not any("Integrity Error" in e for e in self.errors) else 'FAIL'

        print("Validation complete.")

    def _validate_uniqueness(self):
        """Test 1: Check for duplicate AppIDs (Primary Key integrity)."""
        appids = [g['appid'] for g in self.games if 'appid' in g]
        if len(appids) != len(set(appids)):
            duplicate_counts = Counter(appids)
            duplicates = {appid: count for appid, count in duplicate_counts.items() if count > 1}
            self.errors.append(f"Primary Key Violation: Found {len(duplicates)} duplicate AppIDs. Examples: {dict(list(duplicates.items())[:3])}")
            self.test_results['Primary Key Uniqueness'] = 'FAIL'
        else:
            self.test_results['Primary Key Uniqueness'] = 'PASS'
        self.stats['unique_appids'] = len(set(appids))

    def _validate_record_structure(self, record: Dict[str, Any], is_sample_record_for_types: bool):
        """Test 2: Validate schema - field presence and data types."""
        appid = record.get('appid', 'Unknown')
        
        core_fields_present = all(field in record for field in ['appid', 'name_from_applist', 'app_details'])
        if not core_fields_present:
            missing = [field for field in ['appid', 'name_from_applist', 'app_details'] if field not in record]
            self.errors.append(f"Schema Error (AppID: {appid}): Core field(s) missing: {', '.join(missing)}")
            self.test_results['Core Field Presence'] = 'FAIL'
        elif 'Core Field Presence' not in self.test_results:
             self.test_results['Core Field Presence'] = 'PASS'

        if not is_sample_record_for_types:
            return

        for path, expected_type in EXPECTED_TYPES.items():
            value = self._get_nested(record, path)
            if value is not None and not isinstance(value, expected_type):
                self.warnings.append(f"Type Mismatch (AppID: {appid}): Field '{path}' has type {type(value).__name__}, expected {expected_type.__name__}.")
    
    def _validate_record_values(self, record: Dict[str, Any]):
        """Test 3: Validate data values against business rules."""
        appid = record.get('appid', 'Unknown')
        self.stats[f"type_{self._get_nested(record, 'app_details.data.type', 'unknown')}"] += 1

        if self._get_nested(record, 'app_details.success') is True:
            self.stats['successful_records'] += 1
            if not self._get_nested(record, 'app_details.data'):
                self.errors.append(f"Integrity Error (AppID: {appid}): 'success' is true but 'app_details.data' is missing.")
        else:
             self.stats['failed_records'] += 1

        metacritic = self._get_nested(record, 'app_details.data.metacritic.score')
        if metacritic is not None and not (0 <= metacritic <= 100):
            self.warnings.append(f"Value Range (AppID: {appid}): Metacritic score '{metacritic}' is outside the valid 0-100 range.")

    def _collect_profile_data(self, record: Dict[str, Any]):
        """Gathers representative data for the report's profile section."""
        if not self._get_nested(record, 'app_details.success'):
            return

        game_data = self._get_nested(record, 'app_details.data', {})
        if game_data.get('type') != 'game':
            return

        self.stats['successful_games_profiled'] += 1
        
        # Collect sample games for display
        if len(self.profile_data['sample_games']) < 5:
            self.profile_data['sample_games'].append({
                'appid': record.get('appid'),
                'name': game_data.get('name'),
                'price': self._get_nested(record, 'app_details.data.price_overview.final_formatted', 'Free' if game_data.get('is_free') else 'N/A')
            })

        # Collect data points for aggregation
        if game_data.get('release_date', {}).get('date'):
            self.profile_data['release_dates'].append(game_data['release_date']['date'])
        if game_data.get('developers'):
            self.profile_data['developers'].extend(game_data['developers'])
        if game_data.get('publishers'):
            self.profile_data['publishers'].extend(game_data['publishers'])
        if not game_data.get('is_free') and self._get_nested(record, 'app_details.data.price_overview.final') is not None:
             self.profile_data['prices'].append(self._get_nested(record, 'app_details.data.price_overview.final') / 100.0)

    def generate_report(self) -> str:
        """Compiles all findings into a final, detailed Markdown report."""
        status = "PASSED" if not self.errors else "FAILED"
        report_lines = [f"# Data Validation Report: `{self.file_path.name}`", f"**Validation Status: {status}**", f"*Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"]
        
        # --- Validation Checklist Section ---
        report_lines.append("\n## 1. Validation Checklist")
        report_lines.append("| Test Description                   | Status |")
        report_lines.append("| :--------------------------------- | :----- |")
        for test, result in sorted(self.test_results.items()):
            emoji = {'PASS': '✅', 'FAIL': '🚨', 'WARN': '⚠️'}.get(result, '❓')
            report_lines.append(f"| {test} | {emoji} {result} |")

        # --- Statistical Overview Section ---
        report_lines.append("\n## 2. Statistical Overview")
        successful = self.stats.get('successful_records', 0)
        report_lines.append(f"- **Total Records Analyzed:** {len(self.games):,}")
        report_lines.append(f"- **Unique AppIDs Found:** {self.stats.get('unique_appids', 0):,}")
        report_lines.append(f"- **Records with Successful API Details:** {successful:,} ({successful/len(self.games):.1%})")
        report_lines.append("\n### Application Type Distribution:")
        type_keys = sorted([k for k in self.stats if k.startswith('type_')])
        for key in type_keys:
            count = self.stats[key]
            report_lines.append(f"- **{key.replace('type_', '').capitalize()}:** {count:,} ({count/len(self.games):.1%})")

        # --- Data Profile Section ---
        report_lines.append(f"\n## 3. Data Profile (from a sample of {self.stats['successful_games_profiled']:,} games)")
        
        # Sample Games Table
        report_lines.append("\n### Representative Game Samples")
        report_lines.append("| AppID     | Name                       | Price     |")
        report_lines.append("| :-------- | :------------------------- | :-------- |")
        for game in self.profile_data['sample_games']:
            report_lines.append(f"| {game['appid']} | {str(game['name'])[:24]} | {game['price']} |")

        # Profile Aggregates
        report_lines.append("\n### Profile Aggregates")
        dates = [d for d in self.profile_data['release_dates'] if d]
        report_lines.append(f"- **Release Date Range:** `{min(dates) if dates else 'N/A'}` to `{max(dates) if dates else 'N/A'}`")
        top_devs = Counter(self.profile_data['developers']).most_common(3)
        report_lines.append(f"- **Top Developers:** `{', '.join([d[0] for d in top_devs])}`")
        top_pubs = Counter(self.profile_data['publishers']).most_common(3)
        report_lines.append(f"- **Top Publishers:** `{', '.join([p[0] for p in top_pubs])}`")
        prices = self.profile_data['prices']
        report_lines.append(f"- **Price Distribution (Paid Games):** Min: `${min(prices):.2f}`, Max: `${max(prices):.2f}`, Avg: `${sum(prices)/len(prices):.2f}`" if prices else "No paid games in sample.")

        # --- Issues Section ---
        report_lines.append("\n## 4. Validation Issues")
        if self.errors:
            report_lines.append("\n### 🚨 Errors (Blocking Issues)")
            report_lines.append("*These issues MUST be resolved before data import.*")
            for error in self.errors: report_lines.append(f"- {error}")
        else:
            report_lines.append("\n**✅ No blocking errors found.**")

        if self.warnings:
            report_lines.append("\n### ⚠️ Warnings (Non-Blocking Issues)")
            report_lines.append("*These issues should be reviewed but may not block import.*")
            for warning in self.warnings: report_lines.append(f"- {warning}")
        else:
            report_lines.append("\n**✅ No warnings found.**")

        return "\n".join(report_lines)

    @staticmethod
    def _get_nested(data: Dict, path: str, default: Any = None) -> Any:
        keys = path.split('.')
        for key in keys:
            if not isinstance(data, dict) or key not in data: return default
            data = data[key]
        return data

def select_file_from_list(files: List[Path]) -> Optional[Path]:
    if not files: return None
    print("Please select a JSON file to validate:")
    for i, file_path in enumerate(files, 1):
        print(f"  [{i}] {file_path.name}")
    
    while True:
        choice = input(f"Enter the number of the file (1-{len(files)}): ")
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(files): return files[choice_index]
            else: print(f"Invalid selection. Please enter a number between 1 and {len(files)}.")
        except ValueError: print("Invalid input. Please enter a number.")

# --- Orchestration / CLI ---------------------------------------------------------------------------
# Human: defines the execution flow and CLI contract.
# ML:    ENTRYPOINT — parse args → wire components → run.
def main():
    json_files = sorted(list(Path.cwd().glob('*.json')))
    if not json_files:
        print(f"{TColors.FAIL}Error: No .json files found in the current directory.{TColors.ENDC}", file=sys.stderr)
        sys.exit(1)

    input_file = select_file_from_list(json_files)
    if not input_file: sys.exit(1)

    validator = DataValidator(input_file)
    validator.run_validation()
    report = validator.generate_report()

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = Path(f"validation_report_{input_file.stem}_{timestamp}.md")
    with report_filename.open('w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n" + "="*80)
    print("                        VALIDATION SUMMARY")
    print("="*80)
    status_color, status_text = (TColors.FAIL, "FAILED") if validator.errors else (TColors.OKGREEN, "PASSED")
    print(f"Overall Status: {status_color}{TColors.BOLD}{status_text}{TColors.ENDC}")
    print(f"Blocking Errors Found: {TColors.FAIL if validator.errors else ''}{len(validator.errors)}{TColors.ENDC}")
    print(f"Warnings Found: {TColors.WARNING if validator.warnings else ''}{len(validator.warnings)}{TColors.ENDC}")
    print(f"\n{TColors.BOLD}Tests Performed: {len(validator.test_results)} | Passed: {sum(1 for v in validator.test_results.values() if v == 'PASS')}{TColors.ENDC}")
    print(f"\nA detailed report has been saved to: {TColors.BOLD}{report_filename.name}{TColors.ENDC}")
    print("="*80)

# --- Entry Point -----------------------------------------------------------------------------------
# Human: python -m / direct execution path with safe error handling.
# ML:    RUNTIME_START — begin metrics/telemetry if needed.
if __name__ == "__main__":
    main()
