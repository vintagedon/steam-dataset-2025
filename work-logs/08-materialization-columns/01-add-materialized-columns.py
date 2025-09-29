# =================================================================================================
# File:          01-add-materialized-columns.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Phase 8 — Schema extension. Add materialized columns (mat_*) to applications for platform support,
#   pricing, and achievements, and document them with descriptive COMMENTs.
#
# Section Map:
#   1) Imports                     2) Configuration & Logging
#   3) DDL Command Suite           4) Orchestration (transactional apply + verification)
#   5) Entry Point
#
# Provenance / RAG Hints:
#   SOURCE_OF_TRUTH: PostgreSQL 'steamfull'
#   WRITES:          applications.mat_* columns + column comments; verification SELECT
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
# Human: use centrally-managed env; structured logs; consistent exit on missing secrets.
# ML:    CONFIG_KEYS = ["PGSQL01_ADMIN_USER","PGSQL01_ADMIN_PASSWORD","PGSQL01_HOST","PGSQL01_PORT"]
ENV_PATH = Path('/mnt/data2/global-config/research.env')
if not ENV_PATH.exists():
    logging.error(f"FATAL: Global environment file not found at '{ENV_PATH}'.")
    sys.exit(1)
load_dotenv(dotenv_path=ENV_PATH)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# --- DDL Command Suite ----------------------------------------------------------------------------
# Human: run DDL + COMMENTs atomically; comments document derivation + caveats.
# ML:    COMMANDS = [{"title":..., "query":...}, ...] — stable sequence for idempotent apply.
SCHEMA_EXTENSION_COMMANDS = [
    {"title": "Add Platform Support Columns", "query": """
        ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_supports_windows BOOLEAN;
        ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_supports_mac BOOLEAN;
        ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_supports_linux BOOLEAN;
    """},
    {"title": "Add Platform Support Comments", "query": """
        COMMENT ON COLUMN applications.mat_supports_windows IS 'Materialized: Derived from pc_requirements JSONB. TRUE if non-null and non-empty object exists. Source of truth: pc_requirements column. Coverage: 99.997% of applications.';
        COMMENT ON COLUMN applications.mat_supports_mac IS 'Materialized: Derived from mac_requirements JSONB. TRUE if non-null and non-empty object exists. Source of truth: mac_requirements column. Coverage: 99.996% of applications.';
        COMMENT ON COLUMN applications.mat_supports_linux IS 'Materialized: Derived from linux_requirements JSONB. TRUE if non-null and non-empty object exists. Source of truth: linux_requirements column. Coverage: 99.875% of applications.';
    """},
    {"title": "Add Pricing Columns", "query": """
        ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_initial_price INTEGER;
        ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_final_price INTEGER;
        ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_discount_percent INTEGER;
        ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_currency TEXT;
    """},
    {"title": "Add Pricing Comments", "query": """
        COMMENT ON COLUMN applications.mat_initial_price IS 'Materialized: Derived from price_overview->>''initial''. Price in cents (INTEGER). Divide by 100.0 for dollar amount. NULL indicates no pricing data or free game. Source of truth: price_overview JSONB column. Currency bias: 59.5% USD due to API query origin.';
        COMMENT ON COLUMN applications.mat_final_price IS 'Materialized: Derived from price_overview->>''final''. Discounted price in cents (INTEGER). NULL if no price data or game is free. Source of truth: price_overview JSONB column.';
        COMMENT ON COLUMN applications.mat_discount_percent IS 'Materialized: Derived from price_overview->>''discount_percent''. Percentage discount (0-100). NULL indicates no pricing data. 0 indicates no active discount. Source of truth: price_overview JSONB column.';
        COMMENT ON COLUMN applications.mat_currency IS 'Materialized: Derived from price_overview->>''currency''. ISO 4217 currency code (e.g., USD, EUR, GBP). NULL if no pricing data. Heavy USD bias (59.5%) due to API query origin. Source of truth: price_overview JSONB column.';
    """},
    {"title": "Add Achievement Column", "query": """
        ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_achievement_count INTEGER;
    """},
    {"title": "Add Achievement Comment", "query": """
        COMMENT ON COLUMN applications.mat_achievement_count IS 'Materialized: Derived from achievements->>''total''. Total number of achievements available for this application. NULL if no achievements. Valid range includes edge cases with 5,000+ achievements. Source of truth: achievements JSONB column.';
    """}
]

VERIFICATION_QUERY = {
    "title": "Verification Query",
    "query": """
        SELECT
            column_name,
            data_type,
            is_nullable,
            col_description('applications'::regclass, ordinal_position) AS column_comment
        FROM information_schema.columns
        WHERE table_name = 'applications'
          AND column_name LIKE 'mat_%'
        ORDER BY column_name;
    """
}

# --- Orchestration --------------------------------------------------------------------------------
def run_schema_extension():
    """Connects to the database, applies schema changes, and runs verification."""
    logging.info("Starting schema extension for materialized columns...")

    db_user = os.getenv('PGSQL01_ADMIN_USER')
    db_pass = os.getenv('PGSQL01_ADMIN_PASSWORD')
    db_host = os.getenv('PGSQL01_HOST')
    db_port = os.getenv('PGSQL01_PORT')
    db_name = 'steamfull'

    if not all([db_user, db_pass, db_host, db_port, db_name]):
        logging.error("Database credentials not found in environment file.")
        sys.exit(1)

    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            # Execute all schema changes within a single transaction for atomicity
            with conn.begin():
                for item in SCHEMA_EXTENSION_COMMANDS:
                    title, query = item["title"], item["query"]
                    logging.info(f"Executing: {title}...")
                    conn.execute(text(query))
            logging.info("✅ Schema changes and comments committed successfully.")

            # Run the final verification query
            logging.info("Running verification query...")
            df = pd.read_sql_query(text(VERIFICATION_QUERY["query"]), conn)

            logging.info("--- SCHEMA VERIFICATION REPORT ---")
            print(df.to_markdown(index=False))
            
            # Final check for success criteria
            if len(df) == 8 and df['is_nullable'].eq('YES').all():
                 logging.info("✅ SUCCESS: All 8 materialized columns were added correctly.")
            else:
                 logging.warning(f"⚠️ VERIFICATION WARNING: Expected 8 columns, but found {len(df)}. Please review the output.")

    except Exception as e:
        logging.critical(f"An error occurred during schema extension: {e}")
        sys.exit(1)

# --- Entry Point ----------------------------------------------------------------------------------
if __name__ == "__main__":
    run_schema_extension()
