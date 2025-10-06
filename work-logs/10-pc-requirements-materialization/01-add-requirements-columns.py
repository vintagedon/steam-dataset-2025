# =====================================================================================================================
# Script Name:    01-add-requirements-columns.py
# Description:    Phase 2.2 Sprint 1: PC Requirements Parsing - Schema Extension
#                 Adds new TEXT columns to the `applications` table to store materialized
#                 PC requirements for minimum and recommended specs (OS, Processor, Memory, Graphics).
#
# Author:         VintageDon (https://github.com/vintagedon)
# Collaborator:   Claude Sonnet 4 (AI Assistant)
#
# Version:        1.0
# Date:           2025-09-29
# License:        MIT License
#
# Usage:          python 01-add-requirements-columns.py
# =====================================================================================================================

import os
import sys
import logging
from pathlib import Path

try:
    import pandas as pd
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install pandas sqlalchemy psycopg2-binary python-dotenv", file=sys.stderr)
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

# --- DDL Command Suite ---
SCHEMA_EXTENSION_COMMANDS = [
    {
        "title": "Add Minimum PC Requirements Columns",
        "query": """
            ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_pc_os_min TEXT;
            ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_pc_processor_min TEXT;
            ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_pc_memory_min TEXT;
            ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_pc_graphics_min TEXT;
        """
    },
    {
        "title": "Add Recommended PC Requirements Columns",
        "query": """
            ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_pc_os_rec TEXT;
            ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_pc_processor_rec TEXT;
            ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_pc_memory_rec TEXT;
            ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_pc_graphics_rec TEXT;
        """
    },
    {
        "title": "Add Comments for Minimum Requirements Columns",
        "query": """
            COMMENT ON COLUMN applications.mat_pc_os_min IS 'Materialized: Parsed OS from pc_requirements->>''minimum''. Source of truth: pc_requirements JSONB.';
            COMMENT ON COLUMN applications.mat_pc_processor_min IS 'Materialized: Parsed Processor from pc_requirements->>''minimum''. Source of truth: pc_requirements JSONB.';
            COMMENT ON COLUMN applications.mat_pc_memory_min IS 'Materialized: Parsed Memory from pc_requirements->>''minimum''. Source of truth: pc_requirements JSONB.';
            COMMENT ON COLUMN applications.mat_pc_graphics_min IS 'Materialized: Parsed Graphics from pc_requirements->>''minimum''. Source of truth: pc_requirements JSONB.';
        """
    },
    {
        "title": "Add Comments for Recommended Requirements Columns",
        "query": """
            COMMENT ON COLUMN applications.mat_pc_os_rec IS 'Materialized: Parsed OS from pc_requirements->>''recommended''. Source of truth: pc_requirements JSONB.';
            COMMENT ON COLUMN applications.mat_pc_processor_rec IS 'Materialized: Parsed Processor from pc_requirements->>''recommended''. Source of truth: pc_requirements JSONB.';
            COMMENT ON COLUMN applications.mat_pc_memory_rec IS 'Materialized: Parsed Memory from pc_requirements->>''recommended''. Source of truth: pc_requirements JSONB.';
            COMMENT ON COLUMN applications.mat_pc_graphics_rec IS 'Materialized: Parsed Graphics from pc_requirements->>''recommended''. Source of truth: pc_requirements JSONB.';
        """
    }
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
          AND column_name LIKE 'mat_pc_%'
        ORDER BY column_name;
    """
}

# --- Orchestration ---
def run_schema_extension():
    """Connects to the database, applies schema changes, and runs verification."""
    logging.info("Starting schema extension for PC requirements columns...")

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
            if len(df) == 8 and df['data_type'].eq('text').all():
                 logging.info("✅ SUCCESS: All 8 materialized PC requirements columns were added correctly as TEXT.")
            else:
                 logging.warning(f"⚠️ VERIFICATION WARNING: Expected 8 TEXT columns, but found {len(df)}. Please review the output.")

    except Exception as e:
        logging.critical(f"An error occurred during schema extension: {e}")
        sys.exit(1)

# --- Entry Point ---
if __name__ == "__main__":
    run_schema_extension()
