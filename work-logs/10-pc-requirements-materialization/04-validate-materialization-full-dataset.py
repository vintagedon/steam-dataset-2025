# =====================================================================================================================
# Script Name:    03-validate-materialization-full-dataset.py
# Description:    Phase 2.2 Sprint 1: PC Requirements Parsing - FULL VALIDATION SUITE
#                 Compares ALL materialized mat_pc_* columns against their original
#                 pc_requirements JSONB source to certify the accuracy of the ETL process.
#
# Author:         VintageDon (https://github.com/vintagedon)
# Collaborator:   Claude Sonnet 4 (AI Assistant)
#
# Version:        1.1 (Modified for full dataset validation)
# Date:           2025-09-29
# License:        MIT License
#
# Usage:          python 03-validate-materialization-full-dataset.py
# =====================================================================================================================

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
import json

try:
    import pandas as pd
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup
    from tqdm import tqdm
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install pandas sqlalchemy psycopg2-binary python-dotenv beautifulsoup4 tqdm", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
ENV_PATH = Path('/mnt/data2/global-config/research.env')
if not ENV_PATH.exists():
    logging.error(f"FATAL: Global environment file not found at '{ENV_PATH}'.")
    sys.exit(1)
load_dotenv(dotenv_path=ENV_PATH)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Constants ---
TARGET_FIELDS = ['OS', 'Processor', 'Memory', 'Graphics']

# --- Core Parsing Logic ---
def parse_html_fields(html_text: str) -> dict:
    if not html_text or not isinstance(html_text, str) or html_text.strip() == '':
        return {}
    
    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        fields = {}
        for li in soup.find_all('li'):
            strong = li.find('strong')
            if strong:
                label = strong.get_text(strip=True).rstrip(':*').strip()
                if label in TARGET_FIELDS:
                    value = li.get_text(strip=True).replace(strong.get_text(strip=True), '', 1).strip()
                    fields[label] = value
        return fields
    except Exception:
        return {}

# --- Orchestration ---
def run_validation():
    logging.info("Starting FULL DATASET validation of materialized PC requirements...")

    db_user = os.getenv('PGSQL01_ADMIN_USER')
    db_pass = os.getenv('PGSQL01_ADMIN_PASSWORD')
    db_host = os.getenv('PGSQL01_HOST')
    db_port = os.getenv('PGSQL01_PORT')
    db_name = 'steamfull'

    if not all([db_user, db_pass, db_host, db_port, db_name]):
        logging.error("Database credentials not found in environment file.")
        sys.exit(1)

    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    
    output_dir = Path("./work-logs")
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / "phase-2-pc-requirements-validation-report-FULL.txt"
    
    report_lines = [
        "=" * 100,
        "PC Requirements Materialization - FULL DATASET - Validation Report",
        f"Executed: {datetime.now().isoformat()}",
        "=" * 100,
        ""
    ]

    try:
        engine = create_engine(db_url, echo=False)
        with engine.connect() as conn:
            logging.info(f"Fetching ALL records with PC requirements for validation...")
            
            # --- MODIFICATION: Query now fetches the entire dataset, not a sample ---
            full_dataset_query = text("""
                SELECT 
                    appid,
                    pc_requirements,
                    mat_pc_os_min, mat_pc_processor_min, mat_pc_memory_min, mat_pc_graphics_min,
                    mat_pc_os_rec, mat_pc_processor_rec, mat_pc_memory_rec, mat_pc_graphics_rec
                FROM applications 
                WHERE pc_requirements IS NOT NULL AND pc_requirements != '{}'::jsonb;
            """)
            df_records = pd.read_sql_query(full_dataset_query, conn)

            if df_records.empty:
                logging.warning("No records found to validate.")
                return

            logging.info(f"Found {len(df_records):,} records. Comparing source JSONB to materialized columns...")

            discrepancies = []
            total_comparisons = 0
            mismatch_count = 0

            for _, row in tqdm(df_records.iterrows(), total=len(df_records), desc="Validating Full Dataset"):
                pc_req = json.loads(row['pc_requirements']) if isinstance(row['pc_requirements'], str) else row['pc_requirements']
                if not isinstance(pc_req, dict):
                    continue

                min_fields = parse_html_fields(pc_req.get('minimum'))
                rec_fields = parse_html_fields(pc_req.get('recommended'))

                field_map = {
                    'mat_pc_os_min': min_fields.get('OS'), 'mat_pc_os_rec': rec_fields.get('OS'),
                    'mat_pc_processor_min': min_fields.get('Processor'), 'mat_pc_processor_rec': rec_fields.get('Processor'),
                    'mat_pc_memory_min': min_fields.get('Memory'), 'mat_pc_memory_rec': rec_fields.get('Memory'),
                    'mat_pc_graphics_min': min_fields.get('Graphics'), 'mat_pc_graphics_rec': rec_fields.get('Graphics')
                }

                for col_name, parsed_value in field_map.items():
                    db_value = row[col_name]
                    parsed_value_norm = parsed_value if parsed_value else ''
                    db_value_norm = db_value if db_value else ''
                    
                    total_comparisons += 1
                    if parsed_value_norm != db_value_norm:
                        mismatch_count += 1
                        if len(discrepancies) < 20:
                            discrepancies.append({
                                "appid": row['appid'],
                                "field": col_name,
                                "expected": parsed_value_norm,
                                "actual": db_value_norm
                            })

            # --- Generate Report ---
            success_rate = 100 * (1 - (mismatch_count / total_comparisons)) if total_comparisons > 0 else 100
            
            report_lines.append("### FULL DATASET VALIDATION SUMMARY ###")
            report_lines.append(f"  - Total Records Validated: {len(df_records):,}")
            report_lines.append(f"  - Total Field Comparisons: {total_comparisons:,}")
            report_lines.append(f"  - Mismatched Fields: {mismatch_count:,}")
            report_lines.append(f"  - Success Rate: {success_rate:.4f}%")
            report_lines.append("")

            if success_rate >= 99.0:
                report_lines.append("✅ STATUS: SUCCESS - Discrepancy rate is below the 1% threshold.")
                logging.info(f"✅ SUCCESS: Full dataset validation passed with a {success_rate:.4f}% match rate.")
            else:
                report_lines.append("🚨 STATUS: FAILURE - Discrepancy rate is above the 1% threshold.")
                logging.error(f"🚨 FAILURE: Full dataset validation failed with a {success_rate:.4f}% match rate.")

            if discrepancies:
                report_lines.append("\n### SAMPLE DISCREPANCIES (up to 20) ###")
                for d in discrepancies:
                    report_lines.append(f"- AppID {d['appid']} | Field: {d['field']}")
                    report_lines.append(f"  - Expected: '{d['expected']}'")
                    report_lines.append(f"  - Actual:   '{d['actual']}'")

            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(report_lines))
            
            logging.info(f"Full validation report saved to: {report_path}")

    except Exception as e:
        logging.critical(f"An error occurred during validation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# --- Entry Point ---
if __name__ == "__main__":
    run_validation()
