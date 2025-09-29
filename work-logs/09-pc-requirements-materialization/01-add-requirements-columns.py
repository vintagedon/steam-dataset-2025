# =================================================================================================
# File:          01-add-requirements-columns.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Schema extension: add materialized TEXT columns for minimum/recommended PC requirements + comments.
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
from datetime import datetime

try:
    import pandas as pd
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
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
# Human: DDL + COMMENT statements applied atomically; idempotent via IF NOT EXISTS.
# ML:    COMMAND_LIST(schema_extension) — ordered execution; safe to rerun.
SCHEMA_EXTENSION_COMMANDS = [
    {"title": "Add PC Requirements Columns", "query": """
        ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_pc_minimum TEXT;
        ALTER TABLE applications ADD COLUMN IF NOT EXISTS mat_pc_recommended TEXT;
    """},
    {"title": "Comment Columns", "query": """
        COMMENT ON COLUMN applications.mat_pc_minimum IS 'Materialized: HTML-stripped minimum PC requirements (Windows). Source: pc_requirements JSONB (field: minimum).';
        COMMENT ON COLUMN applications.mat_pc_recommended IS 'Materialized: HTML-stripped recommended PC requirements (Windows). Source: pc_requirements JSONB (field: recommended).';
    """}
]

# --- Orchestration --------------------------------------------------------------------------------
# Human: Connect → BEGIN → apply commands → verify; exits with actionable logs.
# ML:    ENTRYPOINT(run_schema_extension) — transactional DDL apply.
def run_schema_extension():
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
            with conn.begin():
                for item in SCHEMA_EXTENSION_COMMANDS:
                    title, query = item["title"], item["query"]
                    logging.info(f"Executing: {title}...")
                    conn.execute(text(query))
        logging.info("✅ Requirements columns added and commented.")
    except Exception as e:
        logging.critical(f"An error occurred during schema extension: {e}")
        sys.exit(1)

# --- Entry Point -----------------------------------------------------------------------------------
# Human: Direct CLI execution with clear success/failure logs.
# ML:    RUNTIME_START — begin main routine.
if __name__ == "__main__":
    run_schema_extension()
