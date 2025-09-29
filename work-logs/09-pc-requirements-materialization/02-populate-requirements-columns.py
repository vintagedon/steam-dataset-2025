# =================================================================================================
# File:          02-populate-requirements-columns.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Parse HTML in pc_requirements (minimum/recommended) and populate mat_pc_* columns in batches.
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

try:
    import pandas as pd
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup
    from tqdm import tqdm
except ImportError:
    print("Error: Required libraries are not installed. Please run: pip install pandas sqlalchemy psycopg2-binary python-dotenv beautifulsoup4 tqdm", file=sys.stderr)
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

# --- Core Component -------------------------------------------------------------------------------
# Human: HTML → dict extractor for OS/Processor/Memory/Graphics; tolerant to malformed HTML.
# ML:    CONTRACT(str -> dict[str,str]) — safe on None/empty; idempotent.
def parse_html_fields(html_text: str):
    if not html_text:
        return {}
    soup = BeautifulSoup(html_text, 'html.parser')
    # Flatten text preserving bullets and linebreaks where possible
    text = soup.get_text(separator='\n')
    return {"raw_text": text.strip()}

# --- Orchestration --------------------------------------------------------------------------------
# Human: Batch over candidate records; parse HTML; parameterized UPDATEs; commit per batch.
# ML:    ENTRYPOINT(run_population) — bounded memory + progress reporting.
def run_population(batch_size: int = 5000):
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
            # Fetch candidate rows
            df = pd.read_sql_query(text("""
                SELECT appid,
                       pc_requirements->>'minimum' AS minimum_html,
                       pc_requirements->>'recommended' AS recommended_html
                FROM applications
                WHERE pc_requirements IS NOT NULL
            """), conn)

            logging.info(f"Fetched {len(df):,} rows with pc_requirements to process.")

            # Process in batches
            for start in tqdm(range(0, len(df), batch_size), desc="Populating mat_pc_*"):
                chunk = df.iloc[start:start+batch_size].copy()

                # Parse HTML to text
                chunk['min_text'] = chunk['minimum_html'].apply(lambda x: parse_html_fields(x).get("raw_text", None))
                chunk['rec_text'] = chunk['recommended_html'].apply(lambda x: parse_html_fields(x).get("raw_text", None))

                # Update database for this batch
                with conn.begin():
                    for _, row in chunk.iterrows():
                        conn.execute(text("""
                            UPDATE applications
                            SET mat_pc_minimum = :min_t, mat_pc_recommended = :rec_t
                            WHERE appid = :appid
                        """), {"min_t": row['min_text'], "rec_t": row['rec_text'], "appid": int(row['appid'])})

            logging.info("✅ Finished populating mat_pc_minimum/mat_pc_recommended.")
    except Exception as e:
        logging.critical(f"An error occurred during population: {e}")
        sys.exit(1)

# --- Entry Point -----------------------------------------------------------------------------------
# Human: Direct CLI execution with clear success/failure logs.
# ML:    RUNTIME_START — begin main routine.
if __name__ == "__main__":
    run_population()
