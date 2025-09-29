# =================================================================================================
# File:          03-validate-materialization.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Phase 8 — Validate that materialized columns match their JSONB sources and business rules.
#   Includes discrepancy counts, logic checks, and an overall coverage report.
#
# Section Map:
#   1) Imports                     2) Configuration & Logging
#   3) Validation Query Suite      4) Orchestration (run suite, write report, success flag)
#   5) Entry Point
#
# Provenance / RAG Hints:
#   SOURCE_OF_TRUTH: applications (JSONB) vs materialized applications.mat_* columns
#   WRITES:          ./work-logs/phase-2-validation-results.txt
#
# Security:
#   - Admin creds from env (PGSQL01_*). No secrets in code.
#
# Change Log (docs-only):
#   - 2025-09-29  Standardized header + dual-audience inline notes; logic unchanged.
# =================================================================================================

# --- Imports --------------------------------------------------------------------------------------
import os
import sys
import logging
from pathlib import Path
from datetime import datetime

try:
    import pandas as pd
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install pandas sqlalchemy psycopg2-binary python-dotenv", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ------------------------------------------------------------------------
# Human: read shared env; structured logs; consistent exit behavior.
# ML:    CONFIG_KEYS = ["PGSQL01_ADMIN_USER","PGSQL01_ADMIN_PASSWORD","PGSQL01_HOST","PGSQL01_PORT"]
ENV_PATH = Path('/mnt/data2/global-config/research.env')
if not ENV_PATH.exists():
    logging.error(f"FATAL: Global environment file not found at '{ENV_PATH}'.")
    sys.exit(1)
load_dotenv(dotenv_path=ENV_PATH)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# --- Validation Query Suite -----------------------------------------------------------------------
# Human: each block isolates one family of checks (platforms, pricing, achievements, logic, coverage).
# ML:    BLOCKS = [{"title":str,"query":sql}, ...] — parse to automate CI-like validation.
VALIDATION_QUERIES = [
    {
        "title": "Platform Support Validation",
        "query": """
            WITH validation AS (SELECT appid, mat_supports_windows AS materialized, (pc_requirements IS NOT NULL AND pc_requirements != '{}') AS from_source FROM applications)
            SELECT 'Windows' AS platform, SUM(CASE WHEN materialized != from_source THEN 1 ELSE 0 END) AS discrepancies FROM validation
            UNION ALL
            SELECT 'Mac', SUM(CASE WHEN materialized != from_source THEN 1 ELSE 0 END) FROM (SELECT mat_supports_mac AS materialized, (mac_requirements IS NOT NULL AND mac_requirements != '{}') AS from_source FROM applications) v
            UNION ALL
            SELECT 'Linux', SUM(CASE WHEN materialized != from_source THEN 1 ELSE 0 END) FROM (SELECT mat_supports_linux AS materialized, (linux_requirements IS NOT NULL AND linux_requirements != '{}') AS from_source FROM applications) v;
        """
    },
    {
        "title": "Pricing Data Validation (IS DISTINCT FROM handles NULLs correctly)",
        "query": """
            WITH validation AS (SELECT appid, mat_initial_price AS materialized, (price_overview->>'initial')::INTEGER AS from_source FROM applications WHERE price_overview IS NOT NULL AND price_overview->>'initial' IS NOT NULL AND is_free = FALSE)
            SELECT 'Initial Price' AS metric, SUM(CASE WHEN materialized IS DISTINCT FROM from_source THEN 1 ELSE 0 END) AS discrepancies FROM validation
            UNION ALL
            SELECT 'Final Price', SUM(CASE WHEN materialized IS DISTINCT FROM from_source THEN 1 ELSE 0 END) FROM (SELECT mat_final_price AS materialized, (price_overview->>'final')::INTEGER AS from_source FROM applications WHERE price_overview IS NOT NULL AND price_overview->>'final' IS NOT NULL AND is_free = FALSE) v
            UNION ALL
            SELECT 'Discount %', SUM(CASE WHEN materialized IS DISTINCT FROM from_source THEN 1 ELSE 0 END) FROM (SELECT mat_discount_percent AS materialized, (price_overview->>'discount_percent')::INTEGER AS from_source FROM applications WHERE price_overview IS NOT NULL AND price_overview->>'discount_percent')::INTEGER IS NOT NULL AND is_free = FALSE) v
            UNION ALL
            SELECT 'Currency', SUM(CASE WHEN materialized IS DISTINCT FROM from_source THEN 1 ELSE 0 END) FROM (SELECT mat_currency AS materialized, price_overview->>'currency' AS from_source FROM applications WHERE price_overview IS NOT NULL AND price_overview->>'currency' IS NOT NULL AND is_free = FALSE) v;
        """
    },
    {
        "title": "Achievement Count Validation",
        "query": """
            WITH validation AS (
                SELECT mat_achievement_count AS materialized, (achievements->>'total')::INTEGER AS from_source
                FROM applications WHERE achievements IS NOT NULL AND jsonb_typeof(achievements->'total') = 'number'
            )
            SELECT 'Achievement Count' AS metric, SUM(CASE WHEN materialized IS DISTINCT FROM from_source THEN 1 ELSE 0 END) AS discrepancies FROM validation;
        """
    },
    {
        "title": "Logical Consistency Checks",
        "query": """
            SELECT 'Negative Prices Check' AS check_name, COUNT(*) AS violations FROM applications WHERE mat_initial_price < 0 OR mat_final_price < 0
            UNION ALL
            SELECT 'Discount Logic Check', COUNT(*) FROM applications WHERE mat_discount_percent > 0 AND mat_final_price > mat_initial_price
            UNION ALL
            SELECT 'Free Game Pricing Check', COUNT(*) FROM applications WHERE is_free = TRUE AND mat_initial_price > 0;
        """
    },
    {
        "title": "Final Coverage Quality Report",
        "query": """
            SELECT
                'VALIDATION SUMMARY' AS report_section, COUNT(*) AS total_applications,
                ROUND(100.0 * COUNT(mat_supports_windows) / COUNT(*), 2) AS pct_platform_coverage,
                COUNT(*) FILTER (WHERE mat_supports_windows = TRUE AND mat_supports_mac = TRUE AND mat_supports_linux = TRUE) AS cross_platform_apps,
                ROUND(100.0 * COUNT(mat_initial_price) / COUNT(*), 2) AS pct_pricing_coverage,
                COUNT(*) FILTER (WHERE mat_discount_percent > 0) AS active_discounts,
                ROUND(100.0 * COUNT(mat_achievement_count) / COUNT(*), 2) AS pct_achievement_coverage,
                COUNT(DISTINCT mat_currency) AS unique_currencies
            FROM applications;
        """
    }
]

# --- Orchestration --------------------------------------------------------------------------------
def run_validation():
    """Connects to the database, runs all validation queries, and generates a report."""
    logging.info("Starting validation suite...")

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
    report_path = output_dir / "phase-2-validation-results.txt"
    
    all_passed = True
    report_lines = [f"Materialization Validation Report - Executed: {datetime.now().isoformat()}"]

    try:
        engine = create_engine(db_url, echo=False)
        with engine.connect() as conn:
            for item in VALIDATION_QUERIES:
                title, query = item["title"], item["query"]
                logging.info(f"Executing: {title}...")
                
                df = pd.read_sql_query(text(query), conn)
                
                report_lines.append("\n" + "="*80)
                report_lines.append(f"--- {title.upper()} ---")
                report_lines.append(df.to_markdown(index=False))
                
                # Check for discrepancies or violations
                if 'discrepancies' in df.columns and df['discrepancies'].sum() > 0:
                    all_passed = False
                if 'violations' in df.columns and df['violations'].sum() > 0:
                    all_passed = False

            # Write the final report to a file
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(report_lines))
            
            logging.info(f"Validation report saved to '{report_path}'.")

            # Final console summary
            logging.info("--- VALIDATION SUMMARY ---")
            if all_passed:
                logging.info("✅ SUCCESS: All validation checks passed with 0 discrepancies or violations.")
            else:
                logging.error("✗ FAILURE: One or more validation checks failed. Please review the report for details.")

    except Exception as e:
        logging.critical(f"An error occurred during the validation process: {e}")
        sys.exit(1)

# --- Entry Point ----------------------------------------------------------------------------------
if __name__ == "__main__":
    run_validation()
