# =================================================================================================
# File:          post-import-tasks-steamfull.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Apply post-import SQL tasks (indexes, views) against the steamfull DB from a .sql file.
#
# Section Map:
#   1) Imports — dependencies and why they're needed
#   2) Configuration & Setup — env, logging, runtime knobs
#   3) Core Components — classes/functions with intent + IO contracts
#   4) Orchestration — how components are wired together
#   5) Entry Point — CLI usage and safe error handling
#
# Provenance / RAG Hints:
#   SOURCE_OF_TRUTH: Steam master JSON & PostgreSQL (see Phase 04 schema)
#   READS / WRITES:  unchanged from original script behavior
#
# Security:
#   - Secrets via .env only (PG_* / STEAM_API_KEY); do not hardcode credentials.
#
# Change Log (docs-only):
#   - 2025-09-29  Added standardized header + dual-audience inline comments; no behavioral changes.
# =================================================================================================

# --- Imports --------------------------------------------------------------------------------------
# Human: Group stdlib vs third-party; fail fast with helpful install hints.
# ML:    DEPENDS_ON — capture runtime libs for reproducibility.
import os
import sys
import psycopg2
from dotenv import load_dotenv

# --- Configuration ---
# The SQL script to execute
SQL_FILE = 'post_import_setup_steamfull.sql'

# --- Core Component -------------------------------------------------------------------------------
# Human: Read SQL file and execute against DB.
# ML:    SIDE_EFFECTS: executes multiple statements
def ):
    """
    Connects to the database and executes the contents of the specified SQL file.
    """
    print("--- Post-Import Task Runner ---")
    try:
        # Load database credentials from .env file
        print("Loading database credentials from .env file...")
# --- Configuration & Setup ------------------------------------------------------------------------
# Human: Centralize env + logging knobs to keep core logic clean/testable.
# ML:    CONFIG_KEYS — parse constants/env names for orchestration.
        load_dotenv()
        db_host = os.getenv('PG_HOST')
        db_port = os.getenv('PG_PORT')
        db_user = os.getenv('PG_APP_USER')
        db_password = os.getenv('PG_APP_USER_PASSWORD')
        # Hardcoding the database name as 'steamfull' based on your logs
        db_name = 'steamfull'

        if not all([db_host, db_port, db_user, db_password, db_name]):
            print("Error: Database environment variables are not fully set in .env file.")
            sys.exit(1)

        # Read the entire SQL script
        print(f"Reading SQL commands from {SQL_FILE}...")
        with open(SQL_FILE, 'r') as f:
            sql_script = f.read()

        # Connect to the PostgreSQL database
        print(f"Connecting to PostgreSQL database at {db_host}...")
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        # Autocommit mode to execute each statement individually
        conn.autocommit = True
        cur = conn.cursor()
        print("Connection successful.")

        # Execute the script
        print(f"Executing script: {SQL_FILE}...")
        cur.execute(sql_script)
        print("-> Success! Post-import script executed.")

    except FileNotFoundError:
        print(f"Error: The SQL file '{SQL_FILE}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Database connection closed.")
        print("--- Task execution complete! ---")

# --- Entry Point -----------------------------------------------------------------------------------
# Human: Direct CLI execution path with actionable errors.
# ML:    RUNTIME_START — begin telemetry if needed.
if __name__ == '__main__':
    execute_sql_from_file()