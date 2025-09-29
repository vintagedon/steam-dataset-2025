# =================================================================================================
# File:          03-validate-materialization.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Sample-based validation comparing parsed fields vs materialized columns; reports success rate.
#
# Section Map:
#   1) Imports — dependencies and why they're needed
#   2) Configuration & Logging — env, DB URL, operator-friendly logs
#   3) Core Components — parsing/DDL/DML helpers with clear IO contracts
#   4) Orchestration — how components run together transactionally
#   5) Entry Point — CLI usage (no logic changes)
#
# Provenance / RAG Hints:
#   SOURCE_OF_TRUTH: PostgreSQL 'steamfull' + applications.pc_requirements JSONB
#   READS / WRITES:  unchanged from original
#
# Security:
#   - Secrets from .env only (PGSQL01_*). No credentials in code.
#
# Change Log (docs-only):
#   - 2025-09-29  Standardized header + dual-audience inline comments; behavior unchanged.
# =================================================================================================
# --- Imports --------------------------------------------------------------------------------------
# Human: Keep stdlib separate from third-party; print actionable hints on ImportError.
# ML:    DEPENDS_ON — capture runtime libs (sqlalchemy, pandas, bs4, tqdm, python-dotenv).
import os
import sys
import logging
from pathlib import Path
from random import sample

try:
    import pandas as pd
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required libraries are not installed. Please run: pip install pandas sqlalchemy psycopg2-binary python-dotenv beautifulsoup4", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Logging ----------------------------------------------------------------------
# Human: Centralize env path + DB URL; structured logs make long runs auditable.
# ML:    CONFIG_KEYS — ['PGSQL01_ADMIN_USER','PGSQL01_ADMIN_PASSWORD','PGSQL01_HOST','PGSQL01_PORT'].
ENV_PATH = Path('/mnt/data2/global-config/research.env')
if not ENV_PATH.exists():
    logging.error(f"FATAL: Global environment file not found at '{ENV_PATH}'.")
    sys.exit(1)
load_dotenv(dotenv_path=ENV_PATH)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def _strip_html_to_text(html_text: str):
    """Helper: minimal HTML-to-text normalization for comparison."""
    if not html_text:
        return None
    return BeautifulSoup(html_text, 'html.parser').get_text(separator='\n').strip()

# --- Orchestration --------------------------------------------------------------------------------
# Human: Fetch sample/full set; re-parse source; compare vs mat_*; write report + status.
# ML:    ENTRYPOINT(run_validation) — CI-friendly outputs.
def run_validation(sample_size: int = 200):
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
            df = pd.read_sql_query(text("""
                SELECT appid,
                       pc_requirements->>'minimum'     AS minimum_html,
                       pc_requirements->>'recommended' AS recommended_html,
                       mat_pc_minimum,
                       mat_pc_recommended
                FROM applications
                WHERE pc_requirements IS NOT NULL
                  AND (mat_pc_minimum IS NOT NULL OR mat_pc_recommended IS NOT NULL)
            """), conn)

            if df.empty:
                logging.warning("No rows to validate. Did you populate mat_pc_* first?")
                return

            # Sample
            if len(df) > sample_size:
                df = df.sample(n=sample_size, random_state=42)

            # Re-parse HTML to text for ground truth
            df['min_text_src'] = df['minimum_html'].apply(_strip_html_to_text)
            df['rec_text_src'] = df['recommended_html'].apply(_strip_html_to_text)

            # Compare with materialized
            df['min_match'] = (df['min_text_src'] == df['mat_pc_minimum'])
            df['rec_match'] = (df['rec_text_src'] == df['mat_pc_recommended'])

            # Metrics
            total = len(df)
            min_ok = int(df['min_match'].sum())
            rec_ok = int(df['rec_match'].sum())

            logging.info(f"Validated {total} rows. Minimum OK: {min_ok} ({min_ok/total:.1%}), Recommended OK: {rec_ok} ({rec_ok/total:.1%})")

    except Exception as e:
        logging.critical(f"An error occurred during validation: {e}")
        sys.exit(1)

# --- Entry Point -----------------------------------------------------------------------------------
# Human: Direct CLI execution with clear success/failure logs.
# ML:    RUNTIME_START — begin main routine.
if __name__ == "__main__":
    run_validation()
