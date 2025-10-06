# =================================================================================================
# File:          export_notebook_data.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# AI Collaborator: Claude.ai, Gemini
# License:       MIT
# Last Updated:  2025-10-05
#
# Purpose:
#   Execute a suite of analytical queries against the 'steamfull' production database
#   and export the results to CSV files. These exports serve as the static data sources
#   for the project's publication-ready Jupyter notebooks, ensuring reproducibility
#   and eliminating the need for a live database connection during analysis.
#
# Section Map:
#   1) Imports & Configuration: Dependencies, logging, and environment setup.
#   2) SQL Query Library:       The six analytical queries for Notebook 1.
#   3) Orchestration:           The main execution logic to connect, query, and export.
#   4) Entry Point:             Standard CLI execution guard.
#
# Security:
#   - Credentials are read exclusively from the global environment file specified.
#   - No secrets are hardcoded or logged.
#
# Usage:
#   python export_notebook_data.py

# Audience Notes (Dual-Audience)
#   • For Analysts (Notebook Users): You do NOT need PostgreSQL access to run the companion notebooks.
#     This script exports CSVs that notebooks read. Just rerun this script when you want fresh data.
#   • For Engineers (DB/ETL): Validate the .env points at the *read-only* app role for steamfull.
#     Queries are idempotent, read-only, and tuned for index usage. See "Operational Guidance" below.
#
# Operational Guidance
#   • Inputs: PostgreSQL 'steamfull' DB (read-only), .env for credentials
#   • Outputs: ./notebooks/data/*.csv (one file per query listed below)
#   • Safety: No DML (INSERT/UPDATE/DELETE); SELECT-only. No secrets logged. CSVs include header rows.
#   • Reproducibility: Exports are timestamped and versioned by filename; notebooks reference these files.
#   • Failure Modes: Missing env vars, connectivity issues, or permission errors. See logged remediation hints.
#
# =================================================================================================

# --- 1. Imports & Configuration ------------------------------------------------------------------
import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Fail fast with helpful messages if essential libraries are missing.
try:
    import pandas as pd
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install pandas sqlalchemy psycopg2-binary python-dotenv", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Logging Setup ---
# Use the specified global environment file for credentials.
ENV_PATH = Path('/opt/global-env/research.env')
if not ENV_PATH.exists():
    logging.error(f"FATAL: Global environment file not found at '{ENV_PATH}'.")
    sys.exit(1)
load_dotenv(dotenv_path=ENV_PATH)

# Configure structured logging for clear, auditable output.
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- 2. SQL Query Library -----------------------------------------------------------------------
# NOTE for Analysts: Each query below yields one CSV used by the published notebook.
# NOTE for Engineers: Keep WHERE clauses aligned with materialized columns (Phase 2). Avoid breaking schema contracts.
--
# A dictionary mapping descriptive filenames to their corresponding SQL queries.
ANALYTICAL_QUERIES = {
    "01_temporal_growth": {
        "description": "Steam's platform growth from 1997-2025.",
        "query": """
            SELECT
                EXTRACT(YEAR FROM release_date) as release_year,
                COUNT(*) as apps_released,
                COUNT(*) FILTER (WHERE type = 'game') as games_released,
                COUNT(*) FILTER (WHERE type = 'dlc') as dlc_released,
                COUNT(*) FILTER (WHERE is_free = TRUE) as free_apps,
                ROUND(AVG(mat_final_price) / 100.0, 2) as avg_price_usd
            FROM applications
            WHERE success = TRUE
                AND release_date IS NOT NULL
                AND EXTRACT(YEAR FROM release_date) BETWEEN 1997 AND 2025
            GROUP BY release_year
            ORDER BY release_year;
        """
    },
    "02_genre_evolution": {
        "description": "Genre popularity and pricing trends since 2000.",
        "query": """
            SELECT
                g.name as genre_name,
                EXTRACT(YEAR FROM a.release_date) as release_year,
                COUNT(DISTINCT a.appid) as game_count,
                ROUND(AVG(a.mat_final_price) / 100.0, 2) as avg_price,
                COUNT(*) FILTER (WHERE a.is_free = TRUE) as free_count
            FROM applications a
            JOIN application_genres ag ON a.appid = ag.appid
            JOIN genres g ON ag.genre_id = g.id
            WHERE a.success = TRUE
                AND a.type = 'game'
                AND a.release_date IS NOT NULL
                AND EXTRACT(YEAR FROM a.release_date) >= 2000
            GROUP BY g.name, release_year
            HAVING COUNT(DISTINCT a.appid) >= 10
            ORDER BY release_year, game_count DESC;
        """
    },
    "03_platform_support": {
        "description": "Distribution of platform support (Windows, Mac, Linux).",
        "query": """
            SELECT
                mat_supports_windows,
                mat_supports_mac,
                mat_supports_linux,
                COUNT(*) as app_count,
                COUNT(*) FILTER (WHERE type = 'game') as game_count,
                ROUND(AVG(mat_final_price) / 100.0, 2) as avg_price
            FROM applications
            WHERE success = TRUE
                AND mat_final_price IS NOT NULL
                AND mat_currency = 'USD'
            GROUP BY mat_supports_windows, mat_supports_mac, mat_supports_linux
            ORDER BY app_count DESC;
        """
    },
    "04_pricing_strategy": {
        "description": "Analysis of application pricing tiers.",
        "query": """
            SELECT
                CASE
                    WHEN is_free = TRUE THEN 'Free'
                    WHEN mat_final_price < 500 THEN '$0.01-$4.99'
                    WHEN mat_final_price < 1000 THEN '$5.00-$9.99'
                    WHEN mat_final_price < 2000 THEN '$10.00-$19.99'
                    WHEN mat_final_price < 3000 THEN '$20.00-$29.99'
                    WHEN mat_final_price < 5000 THEN '$30.00-$49.99'
                    ELSE '$50.00+'
                END as price_range,
                COUNT(*) as app_count,
                ROUND(AVG(mat_discount_percent), 1) as avg_discount_percent,
                COUNT(*) FILTER (WHERE mat_achievement_count > 0) as has_achievements
            FROM applications
            WHERE success = TRUE
                AND type = 'game'
                AND (mat_currency = 'USD' OR is_free = TRUE)
            GROUP BY price_range
            ORDER BY MIN(mat_final_price) NULLS FIRST;
        """
    },
    "05_publisher_portfolios": {
        "description": "Portfolio analysis of the top 100 publishers.",
        "query": """
            WITH publisher_stats AS (
                SELECT
                    p.name as publisher_name,
                    COUNT(DISTINCT a.appid) as total_apps,
                    COUNT(DISTINCT a.appid) FILTER (WHERE a.type = 'game') as game_count,
                    COUNT(DISTINCT a.appid) FILTER (WHERE a.type = 'dlc') as dlc_count,
                    ROUND(AVG(a.mat_final_price) / 100.0, 2) as avg_price,
                    ROUND(AVG(a.mat_achievement_count), 1) as avg_achievements
                FROM publishers p
                JOIN application_publishers ap ON p.id = ap.publisher_id
                JOIN applications a ON ap.appid = a.appid
                WHERE a.success = TRUE
                GROUP BY p.name
                HAVING COUNT(DISTINCT a.appid) >= 10
            )
            SELECT *
            FROM publisher_stats
            ORDER BY total_apps DESC
            LIMIT 100;
        """
    },
    "06_achievement_evolution": {
        "description": "Adoption rate of Steam Achievements over time.",
        "query": """
            SELECT
                EXTRACT(YEAR FROM release_date) as release_year,
                COUNT(*) as total_games,
                COUNT(*) FILTER (WHERE mat_achievement_count > 0) as games_with_achievements,
                ROUND(100.0 * COUNT(*) FILTER (WHERE mat_achievement_count > 0) / NULLIF(COUNT(*), 0), 2) as pct_with_achievements,
                ROUND(AVG(mat_achievement_count) FILTER (WHERE mat_achievement_count > 0), 1) as avg_achievements_per_game
            FROM applications
            WHERE success = TRUE
                AND type = 'game'
                AND release_date IS NOT NULL
                AND EXTRACT(YEAR FROM release_date) BETWEEN 1997 AND 2025
            GROUP BY release_year
            ORDER BY release_year;
        """
    }
}

# --- 3. Orchestration -----------------------------------------------------------------------------
def main():
    """
    Orchestrates CSV export for Notebook 1.

    Steps:
      1) Load env + configure engine
      2) Ensure output directory exists
      3) Execute each analytical query (read-only)
      4) Save DataFrame to CSV with stable, notebook-friendly filenames

    Returns: None (writes files under notebooks/data)
    """
    """
    Main function to connect to the database, execute queries, and save results to CSV.
    """
    logging.info("🚀 Starting Notebook 1 data export process...")
    
    # Create a timestamped directory for this run's exports.
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Path(f"./notebook_1_data_exports_{timestamp}")
    output_dir.mkdir(exist_ok=True)


    # Construct the database URL from environment variables.
    db_user = os.getenv('PGSQL01_ADMIN_USER')
    db_pass = os.getenv('PGSQL01_ADMIN_PASSWORD')
    db_host = os.getenv('PGSQL01_HOST')
    db_port = os.getenv('PGSQL01_PORT')
    db_name = 'steamfull'

    if not all([db_user, db_pass, db_host, db_port]):
        logging.error("Database credentials not found in environment file. Halting.")
        sys.exit(1)

    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            logging.info(f"✅ Successfully connected to database '{db_name}' on '{db_host}'.")

            for filename_base, query_info in ANALYTICAL_QUERIES.items():
                description = query_info["description"]
                query = query_info["query"]
                output_path = output_dir / f"{filename_base}.csv"

                logging.info(f"Executing query for: {description} -> '{output_path.name}'...")

                try:
                    df = pd.read_sql_query(sql=text(query), con=conn)
                    df.to_csv(output_path, index=False)
                    logging.info(f"✅ Success! Exported {len(df):,} rows.")

                except Exception as e:
                    logging.error(f"❌ FAILED to execute or save query for '{filename_base}'. Error: {e}")
                    continue

    except Exception as e:
        logging.critical(f"A critical error occurred during database connection: {e}")
        sys.exit(1)

    logging.info(f"🎉 All queries executed. Data exported to '{output_dir.resolve()}'.")

# --- 4. Entry Point -------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
