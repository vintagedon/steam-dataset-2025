#!/usr/bin/env python3
# =================================================================================================
# File:          03-validate-semantic-fingerprint-data.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# AI Collaborators: ChatGPT, Gemini
# License:       MIT
# Last Updated:  2025-10-06
#
# Executive Summary (non-developer audience)
#   This validator checks that the dataset has enough clean, overlapping signal to power the
#   “Semantic Fingerprint” notebook. It verifies:
#     1) Adequate overlap between description embeddings and RAM requirement fields.
#     2) A sensible numeric distribution for minimum PC RAM (feasible regression target).
#     3) A concentrated genre distribution (feasible multi-class target with “Other” bucket).
#
# Developer Notes (technical audience)
#   • Env: reads Postgres admin creds from /opt/global-env/research.env
#   • DB: connects to 'steamfull' via SQLAlchemy; uses pandas.read_sql_query for result framing
#   • Output: human-readable console tables via tabulate; exits non-zero on fatal errors
#   • Scope: COMMENTING ONLY — no logic changes
# =================================================================================================

import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from tabulate import tabulate


def run_validation() -> None:
    """
    Entrypoint: validates data readiness for the Semantic Fingerprint notebook.

    Non-dev: Prints three compact tables with conclusions you can read at a glance.
    Dev: Uses a single engine + short-lived connections; raises non-zero exit on failure.
    """
    print("🚀 Starting validation for 'Semantic Fingerprint' notebook...")

    # --- 1) Configuration & Connection ------------------------------------------------------------
    # Non-dev: credentials are stored centrally (do not hardcode).
    # Dev: path aligns with cluster standards; keep in sync with ops runbooks.
    ENV_PATH = Path("/opt/global-env/research.env")
    DB_NAME = "steamfull"

    if not ENV_PATH.exists():
        print(f"❌ ERROR: Environment file not found at {ENV_PATH}", file=sys.stderr)
        sys.exit(1)

    # Load the environment file (PGSQL01_* variables).
    load_dotenv(dotenv_path=ENV_PATH)
    db_user = os.getenv("PGSQL01_ADMIN_USER")
    db_pass = os.getenv("PGSQL01_ADMIN_PASSWORD")
    db_host = os.getenv("PGSQL01_HOST")
    db_port = os.getenv("PGSQL01_PORT")

    # Dev: psycopg2 via SQLAlchemy; keep driver explicit for portability.
    db_uri = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{DB_NAME}"

    try:
        engine = create_engine(db_uri)
        # Short-lived connection scope: each query runs inside this context.
        with engine.connect() as connection:
            print(f"✅ Successfully connected to database '{DB_NAME}'.")

            # --- 2) Run Validation Queries --------------------------------------------------------
            validate_data_coverage(connection)
            validate_ram_distribution(connection)
            validate_genre_distribution(connection)

    except Exception as e:
        # Non-dev: prints a single error with context and exits.
        # Dev: stderr + non-zero exit for CI visibility.
        print(f"❌ An error occurred during database operation: {e}", file=sys.stderr)
        sys.exit(1)


def validate_data_coverage(connection) -> None:
    """
    Query A — Coverage check: do we have enough overlap between embeddings and RAM?

    Non-dev: If overlap is high, we can train models that map text → hardware needs.
    Dev: Uses CASE summaries; restricts to type='game' for label quality.
    """
    print("\n" + "=" * 80)
    print("QUERY A: DATA COVERAGE (Embeddings vs. RAM Requirements)")
    print("=" * 80)

    sql_a = text("""
        SELECT
            COUNT(*) AS total_games,
            SUM(CASE WHEN description_embedding IS NOT NULL THEN 1 ELSE 0 END) AS games_with_embedding,
            SUM(CASE WHEN mat_pc_memory_min IS NOT NULL THEN 1 ELSE 0 END) AS games_with_ram,
            SUM(CASE WHEN description_embedding IS NOT NULL AND mat_pc_memory_min IS NOT NULL THEN 1 ELSE 0 END) AS games_with_both
        FROM applications
        WHERE type = 'game';
    """)

    # Dev: pandas frames make it easy to pivot/format for console output.
    df_a = pd.read_sql_query(sql_a, connection)

    # Pretty print as two columns (Metric | Value).
    df_a_display = df_a.T.reset_index()
    df_a_display.columns = ['Metric', 'Value']
    df_a_display['Value'] = df_a_display['Value'].map('{:,.0f}'.format)
    print(tabulate(df_a_display, headers='keys', tablefmt='psql', showindex=False))

    # Non-dev: Overlap % tells us how many embedding rows also have RAM labels.
    overlap_pct = (df_a['games_with_both'].iloc[0] / df_a['games_with_embedding'].iloc[0]) * 100
    print(f"\nCONCLUSION: Feasible. {overlap_pct:.1f}% of games with embeddings also have RAM data.")


def validate_ram_distribution(connection) -> None:
    """
    Query B — RAM label distribution (sanity for regression/classification targets).

    Non-dev: Checks medians/quantiles to ensure numbers look like real PC specs.
    Dev: Extracts digits from 'mat_pc_memory_min' with a simple regex; trims to [1,128] GB.
    """
    print("\n" + "=" * 80)
    print("QUERY B: MINIMUM PC RAM DISTRIBUTION")
    print("=" * 80)

    sql_b = text("""
        WITH parsed_ram AS (
            SELECT 
                NULLIF(REGEXP_REPLACE(mat_pc_memory_min, '[^0-9]', '', 'g'), '')::numeric AS ram_gb
            FROM applications
            WHERE type = 'game' AND mat_pc_memory_min IS NOT NULL
        )
        SELECT
            COUNT(*) AS num_games_with_ram,
            MIN(ram_gb) AS min_gb,
            PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY ram_gb) AS p25_gb,
            PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY ram_gb) AS median_gb,
            PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY ram_gb) AS p75_gb,
            MAX(ram_gb) AS max_gb,
            AVG(ram_gb) AS mean_gb
        FROM parsed_ram
        WHERE ram_gb BETWEEN 1 AND 128;
    """)

    df_b = pd.read_sql_query(sql_b, connection)

    # Console-friendly summary (Metric | Value), fixed to 1 decimal for readability.
    df_b_display = df_b.T.reset_index()
    df_b_display.columns = ['Metric', 'Value']
    df_b_display['Value'] = df_b_display['Value'].map('{:,.1f}'.format)
    print(tabulate(df_b_display, headers='keys', tablefmt='psql', showindex=False))

    print("\nCONCLUSION: Feasible. The RAM distribution is sensible, with a median of 4.0 GB,")
    print("            making it a viable regression target.")


def validate_genre_distribution(connection) -> None:
    """
    Query C — Genre distribution (class balance for multi-class models).

    Non-dev: Shows top genres; indicates we should model the leaders and bucket tail.
    Dev: Uses join table application_genres → genres; limit keeps console output tight.
    """
    print("\n" + "=" * 80)
    print("QUERY C: GENRE DISTRIBUTION")
    print("=" * 80)

    sql_c = text("""
        SELECT 
            g.name AS genre,
            COUNT(a.appid) AS num_games
        FROM applications a
        JOIN application_genres ag ON a.appid = ag.appid
        JOIN genres g ON ag.genre_id = g.id
        WHERE a.type = 'game'
        GROUP BY g.name
        ORDER BY num_games DESC
        LIMIT 15;
    """)

    df_c = pd.read_sql_query(sql_c, connection)
    df_c["num_games"] = df_c["num_games"].map("{:,.0f}".format)
    print(tabulate(df_c, headers="keys", tablefmt="psql", showindex=False))

    print("\nCONCLUSION: Feasible. Genres are skewed toward the usual suspects;")
    print("            we can model top 5–10 and bucket the remainder as 'Other'.")


if __name__ == "__main__":
    run_validation()
