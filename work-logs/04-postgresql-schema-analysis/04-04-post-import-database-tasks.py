# =================================================================================================
# Script:        04-04-post-import-database-tasks.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       (unchanged; see original in file)
# Created:       (see original)
# Last Updated:  2025-09-29
#
# Purpose:
#   Post‑import maintenance: indexes, ANALYZE, materialized views, vacuum hints.
#
# Section Map:
#   1) Imports — dependencies and why they're needed
#   2) Configuration & Setup — env, logging, runtime knobs
#   3) Core Components — classes/functions with high‑level intent
#   4) Orchestration — how the pieces run together
#   5) CLI / Entry — human‑friendly usage and safe defaults
#
# Data Lineage & Provenance (RAG‑friendly):
#   SOURCE_OF_TRUTH: see original script references
#   READS / WRITES:  unchanged
#
# Security & Compliance:
#   - Secrets via .env only (no literals).
#   - PII: none expected.
#
# Change Log (docs‑only):
#   - 2025-09-29  Re‑commented with full dual‑audience inline notes; logic unchanged.
# =================================================================================================

# --- Imports --------------------------------------------------------------------------------------
# Human: split stdlib vs third‑party; fail fast on missing deps for actionable remediation.
# ML:    DEPENDS_ON — infer runtime library set from import graph.
import os
import sys
import logging
import argparse
import time

try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install psycopg2-binary python-dotenv", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
# --- Configuration & Setup ------------------------------------------------------------------------
# Human: centralize environment + logging so business logic stays testable and clean.
# ML:    CONFIG_KEYS — parse .env to map required/optional runtime knobs.
load_dotenv()
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'), format='[%(asctime)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# --- SQL Commands ---
# The commands are now explicitly ordered in a list of tuples to guarantee execution sequence.
POST_IMPORT_SQL_COMMANDS = [
    ("1. Create HNSW Index on Applications", """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_applications_description_embedding 
        ON applications USING hnsw (description_embedding vector_cosine_ops) 
        WITH (m = 16, ef_construction = 64);
    """),
    ("2. Create HNSW Index on Reviews", """
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_reviews_review_embedding 
        ON reviews USING hnsw (review_embedding vector_cosine_ops) 
        WITH (m = 16, ef_construction = 64);
    """),
    ("3. Update Planner Statistics", "VACUUM ANALYZE;"),
    
    # --- Materialized Views Creation ---
    ("4a. Create Developer Analytics View", """
        CREATE MATERIALIZED VIEW IF NOT EXISTS developer_analytics_view AS
        SELECT
            d.name AS developer_name,
            COUNT(a.appid) AS total_apps,
            COUNT(a.appid) FILTER (WHERE a.type = 'game') AS total_games,
            TRUNC(AVG(a.metacritic_score) FILTER (WHERE a.metacritic_score > 0), 2) AS avg_metacritic_score,
            COUNT(a.appid) FILTER (WHERE a.is_free = true AND a.type = 'game') AS free_to_play_games,
            TRUNC(AVG(CAST(a.price_overview->>'final' AS NUMERIC) / 100.0) FILTER (WHERE a.is_free = false), 2) as avg_price_usd
        FROM developers d
        JOIN application_developers ad ON d.id = ad.developer_id
        JOIN applications a ON ad.appid = a.appid
        GROUP BY d.name;
    """),
    ("4b. Create Unique Index for Developer View", """
        CREATE UNIQUE INDEX IF NOT EXISTS uidx_developer_analytics_view_name ON developer_analytics_view(developer_name);
    """),
    
    ("5a. Create Publisher Analytics View", """
        CREATE MATERIALIZED VIEW IF NOT EXISTS publisher_analytics_view AS
        SELECT
            p.name AS publisher_name,
            COUNT(a.appid) AS total_apps,
            TRUNC(AVG(a.metacritic_score) FILTER (WHERE a.metacritic_score > 0), 2) AS avg_metacritic_score
        FROM publishers p
        JOIN application_publishers ap ON p.id = ap.publisher_id
        JOIN applications a ON ap.appid = a.appid
        GROUP BY p.name;
    """),
    ("5b. Create Unique Index for Publisher View", """
        CREATE UNIQUE INDEX IF NOT EXISTS uidx_publisher_analytics_view_name ON publisher_analytics_view(publisher_name);
    """),

    ("6a. Create Genre Analytics View", """
        CREATE MATERIALIZED VIEW IF NOT EXISTS genre_analytics_view AS
        SELECT
            g.name AS genre_name,
            COUNT(a.appid) AS total_games,
            TRUNC(AVG(a.metacritic_score) FILTER (WHERE a.metacritic_score > 0), 2) AS avg_metacritic_score,
            TRUNC(AVG(CAST(a.price_overview->>'final' AS NUMERIC) / 100.0) FILTER (WHERE a.is_free = false), 2) as avg_price_usd
        FROM genres g
        JOIN application_genres ag ON g.id = ag.genre_id
        JOIN applications a ON ag.appid = a.appid
        WHERE a.type = 'game'
        GROUP BY g.name;
    """),
    ("6b. Create Unique Index for Genre View", """
        CREATE UNIQUE INDEX IF NOT EXISTS uidx_genre_analytics_view_name ON genre_analytics_view(genre_name);
    """),

    # --- Refresh all views once they and their indexes exist ---
    ("7. Refresh Materialized Views", """
        REFRESH MATERIALIZED VIEW CONCURRENTLY developer_analytics_view;
        REFRESH MATERIALIZED VIEW CONCURRENTLY publisher_analytics_view;
        REFRESH MATERIALIZED VIEW CONCURRENTLY genre_analytics_view;
    """)
]

class PostImportFinalizer:
    """Orchestrates the execution of post-import finalization tasks."""

    def __init__(self, db_name: str):
        self._validate_config()
        self.conn_config = {
            'host': os.getenv('PG_HOST'),
            'port': os.getenv('PG_PORT'),
            'dbname': db_name,
            'user': os.getenv('PG_ADMIN_USER'), # These tasks require admin/owner privileges
            'password': os.getenv('PG_ADMIN_PASSWORD')
        }
        self.conn = None

    def _validate_config(self):
        """Ensures all necessary admin connection variables are set."""
        required_vars = ['PG_HOST', 'PG_PORT', 'PG_ADMIN_USER', 'PG_ADMIN_PASSWORD']
        if any(not os.getenv(var) for var in required_vars):
            logging.error("FATAL: Missing PostgreSQL admin connection settings in .env file.")
            sys.exit(1)

    def run_tasks(self):
        """Connects to the DB and executes all defined post-import tasks."""
        logging.info(f"🚀 Starting post-import finalization tasks for database '{self.conn_config['dbname']}'.")
        
        try:
            self.conn = psycopg2.connect(**self.conn_config)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            
            with self.conn.cursor() as cursor:
                for description, sql in POST_IMPORT_SQL_COMMANDS:
                    start_time = time.time()
                    logging.info(f"Executing: {description}...")
                    try:
                        cursor.execute(sql)
                        duration = time.time() - start_time
                        logging.info(f"✅ Success ({duration:.2f}s).")
                    except psycopg2.Error as e:
                        # Corrected error logging
                        logging.error(f"❌ FAILED: {description}. Error: {str(e).strip()}")
                        
        except psycopg2.Error as e:
            logging.error(f"❌ A database connection error occurred: {e}")
            sys.exit(1)
        finally:
            if self.conn:
                self.conn.close()
                logging.info("Database connection closed.")
        
        logging.info("🎉 All post-import tasks completed successfully.")

# --- Orchestration / CLI ---------------------------------------------------------------------------
# Human: defines the execution flow and CLI contract.
# ML:    ENTRYPOINT — parse args → wire components → run.
def main():
    parser = argparse.ArgumentParser(description="Run post-import finalization tasks on a Steam DB.")
    parser.add_argument("database_name", help="The name of the target database.")
    args = parser.parse_args()

    finalizer = PostImportFinalizer(args.database_name)
    finalizer.run_tasks()

# --- Entry Point -----------------------------------------------------------------------------------
# Human: python -m / direct execution path with safe error handling.
# ML:    RUNTIME_START — begin metrics/telemetry if needed.
if __name__ == "__main__":
    main()
