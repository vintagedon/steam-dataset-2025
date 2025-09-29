# =================================================================================================
# Script:        04-03-import-json-to-pgsql.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       (unchanged; see original in file)
# Created:       (see original)
# Last Updated:  2025-09-29
#
# Purpose:
#   ETL loader from JSON artifacts into normalized Postgres tables with transaction safety.
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
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Set, Optional

try:
    import psycopg2
    from psycopg2 import extras
    from dotenv import load_dotenv
    from tqdm import tqdm
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install psycopg2-binary python-dotenv tqdm", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
CWD = Path.cwd()
ENV_FILE = CWD / '.env'
# --- Configuration & Setup ------------------------------------------------------------------------
# Human: centralize environment + logging so business logic stays testable and clean.
# ML:    CONFIG_KEYS — parse .env to map required/optional runtime knobs.
load_dotenv(dotenv_path=ENV_FILE)

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Helper Functions ---
def parse_release_date(date_str: str) -> Optional[str]:
    """
    Transforms a Steam release date string into a SQL-compatible 'YYYY-MM-DD' format.
    Handles various formats and returns None for non-parseable strings like "To be announced".
    """
    if not date_str or 'TBA' in date_str or 'announced' in date_str:
        return None
    try:
        # Steam uses formats like "1 Nov, 2022" or "Nov 1, 2022"
        dt_obj = datetime.strptime(date_str.replace(',', ''), '%d %b %Y')
    except ValueError:
        try:
            dt_obj = datetime.strptime(date_str.replace(',', ''), '%b %d %Y')
        except ValueError:
            return None
    return dt_obj.strftime('%Y-%m-%d')

# --- Main Importer Class ---
class PostgresImporter:
    """Orchestrates the ETL process of loading Steam data into PostgreSQL."""

    def __init__(self, db_name: str):
        self._validate_config()
        self.conn_config = {
            'host': os.getenv('PG_HOST'), 'port': os.getenv('PG_PORT'), 'dbname': db_name,
            'user': os.getenv('PG_APP_USER'), 'password': os.getenv('PG_APP_USER_PASSWORD')
        }
        self.conn = None

    def _validate_config(self):
        """Ensures all necessary database connection variables are set."""
        required_vars = ['PG_HOST', 'PG_PORT', 'PG_APP_USER', 'PG_APP_USER_PASSWORD']
        if any(not os.getenv(var) for var in required_vars):
            logging.error(f"FATAL: Missing PostgreSQL application user connection settings in .env file.")
            sys.exit(1)

    def run_import(self, json_file: Path):
        """Main orchestration method for the entire import process."""
        logging.info(f"🚀 Starting import of '{json_file.name}' into database '{self.conn_config['dbname']}'.")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            games = data.get('games', [])
            if not games:
                logging.warning("No 'games' array found in the JSON file. Nothing to import.")
                return
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"FATAL: Could not read or parse input file. Error: {e}")
            sys.exit(1)

        try:
            self.conn = psycopg2.connect(**self.conn_config)
            with self.conn.cursor() as cursor:
                logging.info("--- Phase 1: Populating Lookup Tables ---")
                lookup_data = self._extract_lookup_data(games)
                self._populate_lookup_tables(cursor, lookup_data)

                logging.info("--- Phase 2: Fetching Lookup Maps ---")
                lookup_maps = self._fetch_lookup_maps(cursor)

                logging.info("--- Phase 3: Inserting Application, Review, and Relational Data ---")
                self._insert_main_data(cursor, games, lookup_maps)

            self.conn.commit()
            logging.info("✅ Transaction committed successfully.")
            self._print_summary_report()

        except psycopg2.Error as e:
            logging.error(f"❌ A database error occurred during the import: {e}")
            if self.conn: self.conn.rollback()
            logging.warning("🛑 Transaction has been rolled back.")
            sys.exit(1)
        finally:
            if self.conn: self.conn.close()
            logging.info("Database connection closed.")

    def _extract_lookup_data(self, games: List[Dict]) -> Dict[str, Set[str]]:
        """Scans all records to find unique values for lookup tables."""
        lookup_data = { "developers": set(), "publishers": set(), "genres": set(), "categories": set() }
        for game in tqdm(games, desc="Scanning for unique entities"):
            details = game.get('app_details', {}).get('data', {})
            if not details: continue
            
            for dev in details.get('developers', []): lookup_data["developers"].add(dev)
            for pub in details.get('publishers', []): lookup_data["publishers"].add(pub)
            for genre in details.get('genres', []): lookup_data["genres"].add(genre['description'])
            for cat in details.get('categories', []): lookup_data["categories"].add(cat['description'])
        return lookup_data

    def _populate_lookup_tables(self, cursor: psycopg2.extensions.cursor, lookup_data: Dict[str, Set]):
        """Performs a bulk INSERT ON CONFLICT for each lookup table."""
        for table_name, values in lookup_data.items():
            if not values: continue
            args_list = [(v,) for v in values]
            psycopg2.extras.execute_values(cursor, f"INSERT INTO {table_name} (name) VALUES %s ON CONFLICT (name) DO NOTHING;", args_list)
            logging.info(f"Populated {cursor.rowcount} new records into '{table_name}'.")

    def _fetch_lookup_maps(self, cursor: psycopg2.extensions.cursor) -> Dict[str, Dict]:
        """Queries the lookup tables to create in-memory name -> id maps."""
        maps = {}
        for table_name in ["developers", "publishers", "genres", "categories"]:
            cursor.execute(f"SELECT name, id FROM {table_name};")
            maps[table_name] = {row[0]: row[1] for row in cursor.fetchall()}
        return maps

    def _insert_main_data(self, cursor: psycopg2.extensions.cursor, games: List[Dict], maps: Dict):
        """Iterates through games and inserts data into all remaining tables."""
        for game in tqdm(games, desc="Importing main records"):
            details = game.get('app_details', {})
            data = details.get('data', {})
            appid = game.get('appid')
            if not appid: continue
            
            release_date = parse_release_date(data.get('release_date', {}).get('date', ''))
            app_type = data.get('type') if data.get('type') in ('game', 'dlc', 'software', 'video', 'demo', 'music') else None

            # --- Insert into `applications` table ---
            cursor.execute("""
                INSERT INTO applications (
                    appid, name_from_applist, success, fetched_at, steam_appid, name, type, is_free, 
                    release_date, required_age, metacritic_score, recommendations_total, header_image, 
                    background, detailed_description, short_description, about_the_game, supported_languages, 
                    price_overview, pc_requirements, mac_requirements, linux_requirements, content_descriptors, 
                    package_groups, achievements, screenshots, movies, base_app_id
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (appid) DO UPDATE SET
                    name_from_applist = EXCLUDED.name_from_applist, success = EXCLUDED.success, 
                    fetched_at = EXCLUDED.fetched_at, name = EXCLUDED.name, 
                    -- Add more fields to update on conflict as needed
                    updated_at = NOW();
            """, (
                appid, game.get('name_from_applist'), details.get('success'), details.get('fetched_at'),
                data.get('steam_appid'), data.get('name'), app_type, data.get('is_free'), release_date,
                data.get('required_age', 0), data.get('metacritic', {}).get('score'),
                data.get('recommendations', {}).get('total'), data.get('header_image'), data.get('background'),
                data.get('detailed_description'), data.get('short_description'), data.get('about_the_game'),
                data.get('supported_languages'), json.dumps(data.get('price_overview')), json.dumps(data.get('pc_requirements')),
                json.dumps(data.get('mac_requirements')), json.dumps(data.get('linux_requirements')),
                json.dumps(data.get('content_descriptors')), json.dumps(data.get('package_groups')),
                json.dumps(data.get('achievements')), json.dumps(data.get('screenshots')),
                json.dumps(data.get('movies')), data.get('fullgame', {}).get('appid')
            ))

            if not data: continue
            
            # --- Populate Junction Tables ---
            dev_ids = [maps['developers'].get(name) for name in data.get('developers', []) if maps['developers'].get(name)]
            if dev_ids: psycopg2.extras.execute_values(cursor, "INSERT INTO application_developers (appid, developer_id) VALUES %s ON CONFLICT DO NOTHING;", [(appid, dev_id) for dev_id in dev_ids])
            
            pub_ids = [maps['publishers'].get(name) for name in data.get('publishers', []) if maps['publishers'].get(name)]
            if pub_ids: psycopg2.extras.execute_values(cursor, "INSERT INTO application_publishers (appid, publisher_id) VALUES %s ON CONFLICT DO NOTHING;", [(appid, pub_id) for pub_id in pub_ids])
            
            genre_ids = [maps['genres'].get(g['description']) for g in data.get('genres', []) if maps['genres'].get(g['description'])]
            if genre_ids: psycopg2.extras.execute_values(cursor, "INSERT INTO application_genres (appid, genre_id) VALUES %s ON CONFLICT DO NOTHING;", [(appid, genre_id) for genre_id in genre_ids])
            
            category_ids = [maps['categories'].get(c['description']) for c in data.get('categories', []) if maps['categories'].get(c['description'])]
            if category_ids: psycopg2.extras.execute_values(cursor, "INSERT INTO application_categories (appid, category_id) VALUES %s ON CONFLICT DO NOTHING;", [(appid, cat_id) for cat_id in category_ids])

            # --- Populate Reviews Table ---
            reviews = game.get('reviews', {}).get('reviews', [])
            if reviews:
                review_data_to_insert = []
                for review in reviews:
                    author = review.get('author', {})
                    review_data_to_insert.append((
                        review.get('recommendationid'), appid, author.get('steamid'),
                        author.get('num_games_owned'), author.get('num_reviews'), author.get('playtime_forever'),
                        author.get('playtime_last_two_weeks'), author.get('playtime_at_review'), author.get('last_played'),
                        review.get('language'), review.get('review'), review.get('timestamp_created'),
                        review.get('timestamp_updated'), review.get('voted_up'), review.get('votes_up'),
                        review.get('votes_funny'), review.get('weighted_vote_score'), review.get('comment_count'),
                        review.get('steam_purchase'), review.get('received_for_free'), review.get('written_during_early_access')
                    ))
                
                if review_data_to_insert:
                    psycopg2.extras.execute_values(cursor, """
                        INSERT INTO reviews (
                            recommendationid, appid, author_steamid, author_num_games_owned, author_num_reviews,
                            author_playtime_forever, author_playtime_last_two_weeks, author_playtime_at_review,
                            author_last_played, language, review_text, timestamp_created, timestamp_updated,
                            voted_up, votes_up, votes_funny, weighted_vote_score, comment_count,
                            steam_purchase, received_for_free, written_during_early_access
                        ) VALUES %s ON CONFLICT (recommendationid) DO NOTHING;
                    """, review_data_to_insert)

    def _print_summary_report(self):
        """Queries the DB stats function and prints a final confirmation report."""
        if not self.conn: return
        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM get_database_stats();")
                stats = cursor.fetchone()
                if stats:
                    print("\n" + "="*80)
                    print("                        IMPORT SUMMARY REPORT")
                    print("="*80)
                    print(f"{'Total Applications:':<30} {stats['total_applications']:,}")
                    print(f"{'  - Games:':<30} {stats['total_games']:,}")
                    print(f"{'  - DLC:':<30} {stats['total_dlc']:,}")
                    print(f"{'Total Reviews:':<30} {stats['total_reviews']:,}")
                    print(f"{'Unique Developers Imported:':<30} {stats['total_developers']:,}")
                    print(f"{'Unique Publishers Imported:':<30} {stats['total_publishers']:,}")
                    print("="*80)
        except psycopg2.Error as e:
            logging.warning(f"Could not generate summary report. Error: {e}")

# --- Orchestration / CLI ---------------------------------------------------------------------------
# Human: defines the execution flow and CLI contract.
# ML:    ENTRYPOINT — parse args → wire components → run.
def main():
    """Main function to handle argument parsing and orchestrate the import."""
    parser = argparse.ArgumentParser(description="Import a Steam JSON data file into the PostgreSQL database.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("database_name", nargs='?', default=None, help="Name of the target database. If omitted, will prompt.")
    parser.add_argument("input_file", nargs='?', type=Path, default=None, help="Path to the input JSON file. If omitted, will prompt.")
    args = parser.parse_args()

    db_name = args.database_name
    input_file = args.input_file

    if not db_name:
        db_name = input("Enter the target database name (e.g., steam5k): ")
    if not input_file:
        json_files = sorted(list(CWD.glob('*_enriched_*.json')))
        if not json_files:
            logging.error("No '*_enriched_*.json' files found in the current directory.")
            sys.exit(1)
        print("Please select an enriched JSON file to import:")
        for i, f in enumerate(json_files, 1): print(f"  [{i}] {f.name}")
        while True:
            choice = input(f"Enter the number of the file (1-{len(json_files)}): ")
            try:
                input_file = json_files[int(choice) - 1]
                break
            except (ValueError, IndexError):
                print("Invalid selection.")

    importer = PostgresImporter(db_name)
    importer.run_import(input_file)

# --- Entry Point -----------------------------------------------------------------------------------
# Human: python -m / direct execution path with safe error handling.
# ML:    RUNTIME_START — begin metrics/telemetry if needed.
if __name__ == "__main__":
    main()

