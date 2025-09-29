# =================================================================================================
# File:          00-data-analysis.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Phase 8 — Reconnaissance prior to materialization. Execute exploratory SQL against 'steamfull'
#   to understand JSONB patterns (requirements, price_overview, achievements) before creating
#   materialized columns and population logic.
#
# Section Map:
#   1) Imports                     — deps and why they matter
#   2) Configuration & Logging     — env load, connection URL, operator-friendly logs
#   3) Analysis Query Suite        — labeled SQL blocks for repeatable EDA
#   4) Orchestration               — connect → run queries → write report
#   5) Entry Point                 — CLI execution
#
# Provenance / RAG Hints:
#   SOURCE_OF_TRUTH: PostgreSQL database 'steamfull'
#   READS:           applications (JSONB columns: *_requirements, price_overview, achievements)
#   WRITES:          ./work-logs/phase-2-analysis-output.txt
#
# Security:
#   - Secrets from env file only (PGSQL01_*). No credentials in code.
#
# Change Log (docs-only):
#   - 2025-09-29  Standardized header + dual-audience inline notes; logic unchanged.
# =================================================================================================

# --- Imports --------------------------------------------------------------------------------------
# Human: pandas for tabular output; SQLAlchemy for safe SQL execution; dotenv for env-managed creds.
# ML:    DEPENDS_ON = ["pandas", "sqlalchemy", "psycopg2-binary", "python-dotenv"]
import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# A try-except block for imports provides a clean, user-friendly exit if dependencies are missing.
try:
    import pandas as pd
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries are not installed. Please run: pip install pandas sqlalchemy psycopg2-binary python-dotenv", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ------------------------------------------------------------------------
# Human: use a centrally-managed env file; fail fast if missing; structured logging for ops.
# ML:    CONFIG_KEYS = ["PGSQL01_ADMIN_USER","PGSQL01_ADMIN_PASSWORD","PGSQL01_HOST","PGSQL01_PORT"]
ENV_PATH = Path('/mnt/data2/global-config/research.env')
if not ENV_PATH.exists():
    logging.error(f"FATAL: Global environment file not found at '{ENV_PATH}'.")
    sys.exit(1)
load_dotenv(dotenv_path=ENV_PATH)

# Setup professional logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# --- Analysis Query Suite -------------------------------------------------------------------------
# Human: concise, labeled blocks make the report deterministic and reviewable.
# ML:    BLOCKS = [{"title":str,"query":sql}, ...] — stable identifiers for downstream automation.
ANALYSIS_QUERIES = [
    {
        "title": "Summary Statistics",
        "query": """
            SELECT 'Total Applications' AS metric, COUNT(*) AS value FROM applications UNION ALL
            SELECT 'Apps with pc_requirements', COUNT(*) FROM applications WHERE pc_requirements IS NOT NULL AND pc_requirements != '{}' UNION ALL
            SELECT 'Apps with mac_requirements', COUNT(*) FROM applications WHERE mac_requirements IS NOT NULL AND mac_requirements != '{}' UNION ALL
            SELECT 'Apps with linux_requirements', COUNT(*) FROM applications WHERE linux_requirements IS NOT NULL AND linux_requirements != '{}' UNION ALL
            SELECT 'Apps with price_overview', COUNT(*) FROM applications WHERE price_overview IS NOT NULL UNION ALL
            SELECT 'Apps with achievements', COUNT(*) FROM applications WHERE achievements IS NOT NULL;
        """
    },
    {
        "title": "Platform Support Combinations",
        "query": """
            SELECT
                CASE WHEN pc_requirements IS NOT NULL AND pc_requirements != '{}' THEN 'W' ELSE '-' END ||
                CASE WHEN mac_requirements IS NOT NULL AND mac_requirements != '{}' THEN 'M' ELSE '-' END ||
                CASE WHEN linux_requirements IS NOT NULL AND linux_requirements != '{}' THEN 'L' ELSE '-' END AS platform_combo,
                COUNT(*) AS app_count,
                ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percent
            FROM applications GROUP BY platform_combo ORDER BY app_count DESC LIMIT 20;
        """
    },
    {
        "title": "Pricing Patterns by Currency",
        "query": """
            SELECT
                price_overview->>'currency' AS currency,
                COUNT(*) AS app_count,
                ROUND(AVG((price_overview->>'initial')::INTEGER) / 100.0, 2) AS avg_initial_price,
                ROUND(AVG((price_overview->>'final')::INTEGER) / 100.0, 2) AS avg_final_price
            FROM applications WHERE price_overview IS NOT NULL
            GROUP BY price_overview->>'currency'
            ORDER BY app_count DESC;
        """
    },
    {
        "title": "Free vs. Priced Applications",
        "query": """
            SELECT is_free, price_overview IS NOT NULL AS has_price_data, COUNT(*) AS app_count
            FROM applications GROUP BY is_free, has_price_data ORDER BY app_count DESC;
        """
    },
    {
        "title": "Pricing Anomalies (e.g., Negative Prices)",
        "query": """
            SELECT appid, name, (price_overview->>'initial')::INTEGER AS initial_cents, (price_overview->>'final')::INTEGER AS final_cents, (price_overview->>'discount_percent')::INTEGER AS discount_pct
            FROM applications WHERE price_overview IS NOT NULL AND (
                (price_overview->>'initial')::INTEGER < 0 OR (price_overview->>'final')::INTEGER < 0 OR
                (price_overview->>'discount_percent')::INTEGER > 100 OR (price_overview->>'discount_percent')::INTEGER < 0 OR
                ((price_overview->>'final')::INTEGER > (price_overview->>'initial')::INTEGER AND (price_overview->>'discount_percent')::INTEGER > 0)
            ) LIMIT 50;
        """
    },
    {
        "title": "Achievement Count Distribution",
        "query": """
            SELECT (achievements->>'total')::INTEGER AS achievement_count, COUNT(*) AS app_count
            FROM applications WHERE achievements IS NOT NULL AND jsonb_typeof(achievements->'total') = 'number'
            GROUP BY (achievements->>'total')::INTEGER
            ORDER BY achievement_count DESC LIMIT 20;
        """
    },
    {
        "title": "Achievement Data Anomalies",
        "query": """
            SELECT appid, name, (achievements->>'total')::INTEGER AS total_achievements, jsonb_array_length(achievements->'highlighted') AS highlighted_count
            FROM applications WHERE achievements IS NOT NULL AND jsonb_typeof(achievements->'total') = 'number' AND (
                (achievements->>'total')::INTEGER < 0 OR (achievements->>'total')::INTEGER > 10000
            ) LIMIT 20;
        """
    }
]

# --- Orchestration --------------------------------------------------------------------------------
# Human: connect with SQLAlchemy; run each query; persist a text report for auditability.
# ML:    ENTRYPOINT(run_analysis): uses CONFIG_KEYS; deterministic given DB state.
def run_analysis():
    """Connects to the database, runs the queries, and writes the output to a log file."""
    output_dir = Path("./work-logs")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "phase-2-analysis-output.txt"

    logging.info("Starting reconnaissance analysis...")

    # Construct the database URL for SQLAlchemy from environment variables
    db_user = os.getenv('PGSQL01_ADMIN_USER')
    db_pass = os.getenv('PGSQL01_ADMIN_PASSWORD')
    db_host = os.getenv('PGSQL01_HOST')
    db_port = os.getenv('PGSQL01_PORT')
    db_name = 'steamfull'

    if not all([db_user, db_pass, db_host, db_port, db_name]):
        logging.error("Database credentials not found in environment file. Please check the path and contents.")
        sys.exit(1)

    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    try:
        engine = create_engine(db_url)
        with engine.connect() as conn, open(output_file, 'w', encoding='utf-8') as f:
            logging.info(f"Successfully connected to the database. Output will be saved to '{output_file}'.")
            f.write(f"Reconnaissance Analysis Report - Executed: {datetime.now().isoformat()}\n")
            f.write("="*80 + "\n\n")

            for item in ANALYSIS_QUERIES:
                title, query = item["title"], item["query"]
                f.write(f"--- {title.upper()} ---\n\n")
                logging.info(f"Executing query: {title}...")

                try:
                    # Use sqlalchemy.text() to execute the query safely
                    df = pd.read_sql_query(text(query), conn)
                    f.write(df.to_markdown(index=False))
                    f.write("\n\n" + "="*80 + "\n\n")

                except Exception as e:
                    logging.error(f"Failed to execute query '{title}': {e}")
                    f.write(f"ERROR: Could not execute query.\nDetails: {e}\n\n" + "="*80 + "\n\n")

        logging.info("Analysis complete. Report generated successfully.")

    except Exception as e:
        logging.critical(f"An error occurred: {e}")
        sys.exit(1)

# --- Entry Point ----------------------------------------------------------------------------------
if __name__ == "__main__":
    run_analysis()
