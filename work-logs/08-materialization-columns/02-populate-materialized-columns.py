# =================================================================================================
# File:          02-populate-materialized-columns.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Phase 8 — Populate materialized columns (mat_*) from their JSONB sources with business rules:
#   - Platform support flags from *_requirements JSONB presence
#   - Pricing from price_overview (excluding is_free=TRUE)
#   - Achievement totals from achievements->>'total'
#
# Section Map:
#   1) Imports                     2) Configuration & Logging
#   3) DML Command Suite           4) Orchestration (transactional execute + progress checks)
#   5) Entry Point
#
# Provenance / RAG Hints:
#   SOURCE_OF_TRUTH: applications JSONB columns
#   WRITES:          applications.mat_* fields
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

try:
    import pandas as pd
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install pandas sqlalchemy psycopg2-binary python-dotenv", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ------------------------------------------------------------------------
# Human: use shared env; explicit logger; fail fast if env missing.
# ML:    CONFIG_KEYS = ["PGSQL01_ADMIN_USER","PGSQL01_ADMIN_PASSWORD","PGSQL01_HOST","PGSQL01_PORT"]
ENV_PATH = Path('/mnt/data2/global-config/research.env')
if not ENV_PATH.exists():
    logging.error(f"FATAL: Global environment file not found at '{ENV_PATH}'.")
    sys.exit(1)
load_dotenv(dotenv_path=ENV_PATH)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# --- DML Command Suite ----------------------------------------------------------------------------
# Human: run DML in a single transaction; interleave DO $$ notices as progress checkpoints.
# ML:    COMMANDS = [{"title":..., "query":...}, ...] — stable sequence for reproducible population.
POPULATION_COMMANDS = [
    {
        "title": "Clear Previously Materialized Data",
        "query": """
            UPDATE applications SET
                mat_supports_windows = NULL,
                mat_supports_mac = NULL,
                mat_supports_linux = NULL,
                mat_initial_price = NULL,
                mat_final_price = NULL,
                mat_discount_percent = NULL,
                mat_currency = NULL,
                mat_achievement_count = NULL;
        """
    },
    {
        "title": "Populate Platform Support Columns",
        "query": """
            UPDATE applications SET
                mat_supports_windows = (pc_requirements IS NOT NULL AND pc_requirements != '{}'),
                mat_supports_mac = (mac_requirements IS NOT NULL AND mac_requirements != '{}'),
                mat_supports_linux = (linux_requirements IS NOT NULL AND linux_requirements != '{}');
        """
    },
    {
        "title": "Platform Support Progress Check",
        "query": """
            DO $$
            DECLARE
                total_rows BIGINT; windows_count BIGINT; mac_count BIGINT; linux_count BIGINT; cross_platform_count BIGINT;
            BEGIN
                SELECT COUNT(*),
                       COUNT(*) FILTER (WHERE mat_supports_windows = TRUE),
                       COUNT(*) FILTER (WHERE mat_supports_mac = TRUE),
                       COUNT(*) FILTER (WHERE mat_supports_linux = TRUE),
                       COUNT(*) FILTER (WHERE mat_supports_windows = TRUE AND mat_supports_mac = TRUE AND mat_supports_linux = TRUE)
                INTO total_rows, windows_count, mac_count, linux_count, cross_platform_count FROM applications;
                RAISE NOTICE '=== Platform Support Populated ===';
                RAISE NOTICE 'Windows Support: % (%.2f%%)', windows_count, (windows_count::NUMERIC / total_rows * 100);
                RAISE NOTICE 'Mac Support: % (%.2f%%)', mac_count, (mac_count::NUMERIC / total_rows * 100);
                RAISE NOTICE 'Linux Support: % (%.2f%%)', linux_count, (linux_count::NUMERIC / total_rows * 100);
                RAISE NOTICE 'Cross-Platform (W+M+L): % (%.2f%%)', cross_platform_count, (cross_platform_count::NUMERIC / total_rows * 100);
            END $$;
        """
    },
    {
        "title": "Populate Pricing Data Columns",
        "query": """
            UPDATE applications SET
                mat_initial_price = (price_overview->>'initial')::INTEGER,
                mat_final_price = (price_overview->>'final')::INTEGER,
                mat_discount_percent = (price_overview->>'discount_percent')::INTEGER,
                mat_currency = price_overview->>'currency'
            WHERE price_overview IS NOT NULL
              AND price_overview->>'initial' IS NOT NULL
              AND is_free = FALSE; -- Business Rule: Do not materialize prices for free games.
        """
    },
    {
        "title": "Pricing Data Progress Check",
        "query": """
            DO $$
            DECLARE
                total_rows BIGINT; priced_count BIGINT; free_count BIGINT; avg_price NUMERIC; discount_active_count BIGINT;
            BEGIN
                SELECT 
                    COUNT(*),
                    COUNT(*) FILTER (WHERE mat_initial_price IS NOT NULL),
                    COUNT(*) FILTER (WHERE is_free = TRUE),
                    ROUND(AVG(mat_initial_price) FILTER (WHERE mat_initial_price > 0) / 100.0, 2),
                    COUNT(*) FILTER (WHERE mat_discount_percent > 0)
                INTO total_rows, priced_count, free_count, avg_price, discount_active_count
                FROM applications;
                RAISE NOTICE '=== Pricing Data Populated ===';
                RAISE NOTICE 'Total Applications: %', total_rows;
                RAISE NOTICE 'Apps with Pricing Data: % (%.2f%%)', priced_count, (priced_count::NUMERIC / total_rows * 100);
                RAISE NOTICE 'Free Games: % (%.2f%%)', free_count, (free_count::NUMERIC / total_rows * 100);
                RAISE NOTICE 'Average Initial Price: $%', avg_price;
                RAISE NOTICE 'Apps with Active Discounts: % (%.2f%%)', discount_active_count, (discount_active_count::NUMERIC / total_rows * 100);
            END $$;
        """
    },
    {
        "title": "Populate Achievement Count Column",
        "query": """
            UPDATE applications SET
                mat_achievement_count = (achievements->>'total')::INTEGER
            WHERE achievements IS NOT NULL
              AND jsonb_typeof(achievements->'total') = 'number';
        """
    },
    {
        "title": "Achievement Count Progress Check",
        "query": """
            DO $$
            DECLARE
                total_rows BIGINT; achievement_count BIGINT; avg_achievements NUMERIC; max_achievements INTEGER; whale_count BIGINT;
            BEGIN
                SELECT 
                    COUNT(*),
                    COUNT(*) FILTER (WHERE mat_achievement_count IS NOT NULL),
                    ROUND(AVG(mat_achievement_count) FILTER (WHERE mat_achievement_count > 0), 1),
                    MAX(mat_achievement_count),
                    COUNT(*) FILTER (WHERE mat_achievement_count >= 5000)
                INTO total_rows, achievement_count, avg_achievements, max_achievements, whale_count
                FROM applications;
                RAISE NOTICE '=== Achievement Count Populated ===';
                RAISE NOTICE 'Total Applications: %', total_rows;
                RAISE NOTICE 'Apps with Achievement Data: % (%.2f%%)', achievement_count, (achievement_count::NUMERIC / total_rows * 100);
                RAISE NOTICE 'Average Achievement Count: %', avg_achievements;
                RAISE NOTICE 'Maximum Achievement Count: %', max_achievements;
                RAISE NOTICE '"Whale Apps" (5000+ achievements): %', whale_count;
            END $$;
        """
    }
]

FINAL_SUMMARY_QUERY = {
    "title": "Final Population Summary",
    "query": """
        SELECT 
            'MATERIALIZATION COMPLETE' AS status,
            COUNT(*) AS total_applications,
            ROUND(100.0 * COUNT(mat_supports_windows) / COUNT(*), 2) AS pct_with_platform,
            ROUND(100.0 * COUNT(mat_initial_price) / COUNT(*), 2) AS pct_with_pricing,
            ROUND(100.0 * COUNT(mat_achievement_count) / COUNT(*), 2) AS pct_with_achievements,
            COUNT(DISTINCT mat_currency) AS unique_currencies
        FROM applications;
    """
}

# --- Orchestration --------------------------------------------------------------------------------
def run_population():
    """Connects to the database and runs all population and progress check queries."""
    logging.info("Starting materialized column population...")

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
        engine = create_engine(db_url, echo=False)
        with engine.connect() as conn:
            with conn.begin(): # Start a transaction
                for item in POPULATION_COMMANDS:
                    title, query = item["title"], item["query"]
                    logging.info(f"Executing: {title}...")
                    conn.execute(text(query))
            
            logging.info("✅ Population scripts committed successfully.")
            
            # Run final summary outside the main transaction
            logging.info(f"Executing: {FINAL_SUMMARY_QUERY['title']}...")
            df = pd.read_sql_query(text(FINAL_SUMMARY_QUERY['query']), conn)
            logging.info("--- FINAL POPULATION SUMMARY ---")
            print(df.to_markdown(index=False))

    except Exception as e:
        logging.critical(f"An error occurred during population: {e}")
        sys.exit(1)

# --- Entry Point ----------------------------------------------------------------------------------
if __name__ == "__main__":
    run_population()
