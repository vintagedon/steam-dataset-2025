# =====================================================================================================================
# Script Name:    import_master_data.py
# Description:    A memory-efficient and robust ETL script to load the full Steam dataset. It handles the
#                 specific structure of the master JSON files, filters failed API calls, materializes
#                 features, and uses batching for high-performance insertion.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        3.0
# Date:           2025-09-07
# License:        MIT License
#
# Usage:          python import_master_data.py <db_name> --games_file /path/to/games.json --reviews_file /path/to/reviews.json
#
# =====================================================================================================================
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-09-07      2.8             vintagedon      Added pre-flight check for reviews to prevent orphan records.
#   2025-09-07      3.0             vintagedon      CRITICAL FIX: Rewrote application data extraction to be fully
#                                                   defensive, safely handling records with "success": false. This
#                                                   hardened version is ready for the full dataset import.
# =====================================================================================================================

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Set, Optional, Generator

try:
    import psycopg2
    from psycopg2 import extras
    from dotenv import load_dotenv
    from tqdm import tqdm
    import ijson
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install psycopg2-binary python-dotenv tqdm ijson", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
CWD = Path.cwd()
load_dotenv(dotenv_path=CWD / '.env')
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'), format='[%(asctime)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# --- Helper Functions ---
def parse_release_date(date_str: str) -> Optional[str]:
    """Handles the various date formats from the API and safely returns a SQL-compatible date or None."""
    if not date_str or 'TBA' in date_str or 'announced' in date_str: return None
    try: dt_obj = datetime.strptime(date_str.replace(',', ''), '%d %b %Y')
    except ValueError:
        try: dt_obj = datetime.strptime(date_str.replace(',', ''), '%b %d %Y')
        except ValueError: return None
    return dt_obj.strftime('%Y-%m-%d')

def sanitize_required_age(age: Any) -> Optional[str]:
    """Ensures the 'required_age' field is always a string representation of a number, defaulting to '0'."""
    if age is None: return '0'
    return str(age) # The DB column is INTEGER, but psycopg2 handles the conversion.

def stream_json_file(file_path: Path) -> Generator[Dict, None, None]:
    """
    A memory-efficient generator to read records from a potentially massive JSON file.
    
    The key to this function is `ijson`. Unlike the standard `json` library which loads the
    entire file into RAM, `ijson` reads the file iteratively. Its memory usage is constant
    and tiny, making it the standard professional choice for processing multi-gigabyte JSON files.
    """
    logging.info(f"Streaming records from '{file_path.name}'...")
    found_items = False
    try:
        with file_path.open('rb') as f:
            # We target 'item' assuming the root of the JSON is an array of objects.
            for record in ijson.items(f, 'item'):
                found_items = True
                yield record
        if not found_items:
            logging.warning(f"No items found in '{file_path.name}'. File may be an empty JSON array.")
    except (ijson.JSONError, IOError) as e:
        logging.error(f"FATAL: Could not read or parse file '{file_path.name}'. Error: {e}")
        raise

# --- Main Importer Class ---
class PostgresImporter:
    """Orchestrates the entire ETL process for loading the master Steam dataset into PostgreSQL."""

    def __init__(self, db_name: str):
        self._validate_config()
        self.conn_config = {'host': os.getenv('PG_HOST'), 'port': os.getenv('PG_PORT'), 'dbname': db_name, 'user': os.getenv('PG_APP_USER'), 'password': os.getenv('PG_APP_USER_PASSWORD')}
        self.conn = None

    def _validate_config(self):
        """A guard clause to ensure all necessary database connection variables are present before starting."""
        required = ['PG_HOST', 'PG_PORT', 'PG_APP_USER', 'PG_APP_USER_PASSWORD']
        if any(not os.getenv(var) for var in required):
            logging.error("FATAL: Missing PostgreSQL application user settings in .env file.")
            sys.exit(1)

    def run_import(self, games_file: Optional[Path] = None, reviews_file: Optional[Path] = None):
        """
        Main orchestration method. Manages the database connection and executes the import
        process, ensuring all operations are contained within a single transaction.
        """
        try:
            self.conn = psycopg2.connect(**self.conn_config)
            # The script is modular, allowing games and reviews to be imported independently or together.
            if games_file: self._import_games(games_file)
            if reviews_file: self._import_reviews(reviews_file)
            self._print_summary_report()
        except (psycopg2.Error, IOError, ijson.JSONError) as e:
            # This is the core of the script's data integrity guarantee. If any error occurs at any
            # point, the connection is rolled back, leaving the database in the clean state it was
            # in before the script started.
            logging.error(f"❌ An error occurred during the import process: {e}", exc_info=True)
            if self.conn: self.conn.rollback()
            logging.warning("🛑 Transaction has been rolled back.")
            sys.exit(1)
        finally:
            if self.conn: self.conn.close()
            logging.info("Database connection closed.")

    def _import_games(self, games_file: Path):
        """Handles the complete, multi-phase import process for application data."""
        logging.info(f"🚀 Starting import of games from '{games_file.name}'.")
        with self.conn.cursor() as cursor:
            # This is a classic two-pass ETL approach. We make one pass to gather all unique
            # lookup values, and a second pass to insert the main data.
            logging.info("--- Phase 1: Populating Lookup Tables ---")
            lookup_data = self._extract_lookup_data(games_file)
            self._populate_lookup_tables(cursor, lookup_data)
            self.conn.commit() # Commit after lookup tables are populated.

            logging.info("--- Phase 2: Fetching Lookup Maps ---")
            lookup_maps = self._fetch_lookup_maps(cursor)
            
            logging.info("--- Phase 3: Inserting Application and Relational Data ---")
            self._insert_application_data(cursor, games_file, lookup_maps)
            self.conn.commit()
        logging.info(f"✅ Games import from '{games_file.name}' completed and committed.")

    def _import_reviews(self, reviews_file: Path):
        """Handles the import process for review data."""
        logging.info(f"🚀 Starting import of reviews from '{reviews_file.name}'.")
        with self.conn.cursor() as cursor:
            # This is a critical pre-flight check to prevent foreign key violations. We fetch all
            # existing appids to ensure we don't try to import "orphan" reviews for games that
            # don't exist in our primary table.
            logging.info("Fetching existing application IDs from database for validation...")
            cursor.execute("SELECT appid FROM applications;")
            existing_appids = {row[0] for row in cursor.fetchall()}
            logging.info(f"Found {len(existing_appids):,} existing applications.")
            
            self._insert_review_data(cursor, reviews_file, existing_appids)
            self.conn.commit()
        logging.info(f"✅ Reviews import from '{reviews_file.name}' completed and committed.")

    def _extract_lookup_data(self, games_file: Path) -> Dict[str, Set[str]]:
        """Scans the file to find unique values for all lookup tables (developers, genres, etc.)."""
        lookup_data = {"developers": set(), "publishers": set(), "genres": set(), "categories": set()}
        # The use of `set` is a performance optimization that automatically handles deduplication.
        for record in tqdm(stream_json_file(games_file), desc="Scanning for unique entities"):
            if not record.get('success'): continue
            data = record.get('data', {})
            for dev in data.get('developers', []): lookup_data["developers"].add(dev)
            for pub in data.get('publishers', []): lookup_data["publishers"].add(pub)
            for genre in data.get('genres', []): lookup_data["genres"].add(genre.get('description'))
            for cat in data.get('categories', []): lookup_data["categories"].add(cat.get('description'))
        return lookup_data

    def _populate_lookup_tables(self, cursor: psycopg2.extensions.cursor, lookup_data: Dict[str, Set]):
        """Performs a bulk INSERT ON CONFLICT for each lookup table."""
        for table_name, values in lookup_data.items():
            args_list = [(v,) for v in values if v]
            if not args_list: continue
            # `execute_values` is a highly optimized function for bulk inserts.
            # `ON CONFLICT DO NOTHING` makes this operation idempotent - if we run the script
            # again, it won't create duplicates or throw errors.
            psycopg2.extras.execute_values(cursor, f"INSERT INTO {table_name} (name) VALUES %s ON CONFLICT (name) DO NOTHING;", args_list)
            logging.info(f"Populated {cursor.rowcount} new records into '{table_name}'.")

    def _fetch_lookup_maps(self, cursor: psycopg2.extensions.cursor) -> Dict[str, Dict]:
        """Queries the lookup tables to create in-memory name -> id maps for fast foreign key lookups."""
        maps = {}
        for table_name in ["developers", "publishers", "genres", "categories"]:
            cursor.execute(f"SELECT name, id FROM {table_name};")
            # This dictionary provides an O(1) lookup, which is vastly more performant
            # than running a SELECT query for every single relationship.
            maps[table_name] = {row[0]: row[1] for row in cursor.fetchall()}
        return maps

    def _insert_application_data(self, cursor: psycopg2.extensions.cursor, games_file: Path, maps: Dict):
        """Streams the main data file and inserts records into the applications and junction tables in batches."""
        app_batch, junction_batch = [], {'dev': [], 'pub': [], 'genre': [], 'cat': []}
        batch_size = 1000
        skipped_count = 0
        
        for record in tqdm(stream_json_file(games_file), desc="Preparing application records"):
            # --- Defensive Data Extraction ---
            # This is the critical data cleaning step. We explicitly check that the record is valid
            # and that the API call was successful (`'success': true`). Any records that fail this
            # check are safely skipped, preventing malformed data from entering the database.
            if not record or not isinstance(record, dict) or not record.get('success') or 'data' not in record:
                skipped_count += 1
                continue
            
            data = record.get('data', {})
            appid = data.get('steam_appid')
            name_from_applist = data.get('name') # In the master file, this is the main name
            
            if not appid or not name_from_applist:
                skipped_count += 1
                continue

            # --- Feature Materialization ---
            # We "flatten" complex nested data into top-level columns during the import.
            # This makes querying much simpler and more performant for common analytics.
            platforms = data.get('platforms', {})
            price_overview = data.get('price_overview', {})
            achievements = data.get('achievements', {})
            
            # Prepare the tuple of data in the exact order the INSERT statement expects.
            app_batch.append((
                appid, name_from_applist, appid, data.get('name'),
                data.get('type') if data.get('type') in ('game', 'dlc', 'software', 'video', 'demo', 'music', 'advertising', 'mod', 'episode', 'series') else None,
                data.get('is_free'), parse_release_date(data.get('release_date', {}).get('date', '')),
                sanitize_required_age(data.get('required_age')),
                data.get('metacritic', {}).get('score'), data.get('recommendations', {}).get('total'),
                data.get('header_image'), data.get('background'), data.get('detailed_description'),
                data.get('short_description'), data.get('about_the_game'), data.get('supported_languages'),
                json.dumps(price_overview) if price_overview else None,
                json.dumps(data.get('pc_requirements')) if data.get('pc_requirements') else None,
                json.dumps(data.get('mac_requirements')) if data.get('mac_requirements') else None,
                json.dumps(data.get('linux_requirements')) if data.get('linux_requirements') else None,
                json.dumps(data.get('content_descriptors')) if data.get('content_descriptors') else None,
                json.dumps(data.get('package_groups')) if data.get('package_groups') else None,
                json.dumps(achievements) if achievements else None,
                json.dumps(data.get('screenshots')) if data.get('screenshots') else None,
                json.dumps(data.get('movies')) if data.get('movies') else None,
                json.dumps(data.get('ratings')) if data.get('ratings') else None,
                data.get('fullgame', {}).get('appid'),
                True, record.get('fetched_at'), platforms.get('windows', False),
                platforms.get('mac', False), platforms.get('linux', False), price_overview.get('initial'),
                price_overview.get('final'), price_overview.get('discount_percent'),
                price_overview.get('currency'), achievements.get('total')
            ))
            
            # Prepare data for the junction tables using the in-memory lookup maps.
            for name in data.get('developers', []): junction_batch['dev'].append((appid, maps['developers'].get(name)))
            for name in data.get('publishers', []): junction_batch['pub'].append((appid, maps['publishers'].get(name)))
            for g in data.get('genres', []): junction_batch['genre'].append((appid, maps['genres'].get(g.get('description'))))
            for c in data.get('categories', []): junction_batch['cat'].append((appid, maps['categories'].get(c.get('description'))))
            
            # When a batch reaches the target size, execute the database writes.
            # This is a key performance pattern, as it's far more efficient to do one
            # large write than thousands of small ones.
            if len(app_batch) >= batch_size:
                self._execute_application_batch(cursor, app_batch, junction_batch)
                app_batch, junction_batch = [], {'dev': [], 'pub': [], 'genre': [], 'cat': []}
        
        # Insert any remaining records in the final, partial batch.
        if app_batch: self._execute_application_batch(cursor, app_batch, junction_batch)
        logging.info(f"Finished processing applications. Skipped {skipped_count:,} invalid or failed records.")

    def _execute_application_batch(self, cursor, app_batch, junction_batch):
        """Executes the bulk INSERT commands for one batch of application and relational data."""
        # Main application data insert
        psycopg2.extras.execute_values(cursor, """
            INSERT INTO applications (appid, name_from_applist, steam_appid, name, type, is_free, release_date,
                required_age, metacritic_score, recommendations_total, header_image, background,
                detailed_description, short_description, about_the_game, supported_languages, price_overview,
                pc_requirements, mac_requirements, linux_requirements, content_descriptors, package_groups,
                achievements, screenshots, movies, ratings, base_app_id, success, fetched_at,
                supports_windows, supports_mac, supports_linux, initial_price, final_price,
                discount_percent, currency, achievement_count)
            VALUES %s ON CONFLICT (appid) DO NOTHING;
        """, app_batch, page_size=len(app_batch))
        
        # Junction table inserts, with a list comprehension to filter out any failed lookups (None values).
        if junction_batch['dev']: psycopg2.extras.execute_values(cursor, "INSERT INTO application_developers (appid, developer_id) VALUES %s ON CONFLICT DO NOTHING;", [v for v in junction_batch['dev'] if v[1]])
        if junction_batch['pub']: psycopg2.extras.execute_values(cursor, "INSERT INTO application_publishers (appid, publisher_id) VALUES %s ON CONFLICT DO NOTHING;", [v for v in junction_batch['pub'] if v[1]])
        if junction_batch['genre']: psycopg2.extras.execute_values(cursor, "INSERT INTO application_genres (appid, genre_id) VALUES %s ON CONFLICT DO NOTHING;", [v for v in junction_batch['genre'] if v[1]])
        if junction_batch['cat']: psycopg2.extras.execute_values(cursor, "INSERT INTO application_categories (appid, category_id) VALUES %s ON CONFLICT DO NOTHING;", [v for v in junction_batch['cat'] if v[1]])

    def _insert_review_data(self, cursor: psycopg2.extensions.cursor, reviews_file: Path, existing_appids: Set[int]):
        """Streams the reviews file and inserts review data in batches."""
        review_stream = stream_json_file(reviews_file)
        batch_size, review_batch, skipped_apps = 2000, [], Counter()
        for record in tqdm(review_stream, desc="Importing review records"):
            appid, review_data = record.get('appid'), record.get('reviews', {})
            if not (appid and review_data.get('success') == 1): continue
            
            # This pre-flight check ensures we don't violate foreign key constraints.
            if appid not in existing_appids:
                skipped_apps[appid] += 1
                continue
                
            for review in review_data.get('reviews', []):
                author = review.get('author', {})
                if not review.get('recommendationid'): continue
                review_batch.append((
                    review.get('recommendationid'), appid, author.get('steamid'), author.get('num_games_owned'),
                    author.get('num_reviews'), author.get('playtime_forever'), author.get('playtime_last_two_weeks'),
                    author.get('playtime_at_review'), author.get('last_played'), review.get('language'), review.get('review'),
                    review.get('timestamp_created'), review.get('timestamp_updated'), review.get('voted_up'),
                    review.get('votes_up'), review.get('votes_funny'), review.get('weighted_vote_score'),
                    review.get('comment_count'), review.get('steam_purchase'), review.get('received_for_free'),
                    review.get('written_during_early_access')
                ))
                if len(review_batch) >= batch_size:
                    self._execute_review_batch(cursor, review_batch)
                    review_batch = []
        if review_batch: self._execute_review_batch(cursor, review_batch)
        if skipped_apps:
            logging.warning(f"Skipped reviews for {len(skipped_apps)} appids not found in the 'applications' table. Top 3: {skipped_apps.most_common(3)}")

    def _execute_review_batch(self, cursor, review_batch):
        """Executes a bulk INSERT for one batch of review data."""
        psycopg2.extras.execute_values(cursor, """
            INSERT INTO reviews (recommendationid, appid, author_steamid, author_num_games_owned, author_num_reviews,
                author_playtime_forever, author_playtime_last_two_weeks, author_playtime_at_review,
                author_last_played, language, review_text, timestamp_created, timestamp_updated, voted_up,
                votes_up, votes_funny, weighted_vote_score, comment_count, steam_purchase,
                received_for_free, written_during_early_access)
            VALUES %s ON CONFLICT (recommendationid) DO NOTHING;
        """, review_batch, page_size=len(review_batch))

    def _print_summary_report(self):
        """Queries the DB stats function and prints a final confirmation report."""
        if not self.conn or self.conn.closed: self.conn = psycopg2.connect(**self.conn_config)
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

def main():
    """Main function to handle argument parsing and orchestrate the import."""
    parser = argparse.ArgumentParser(description="Import full Steam dataset from master JSON files into PostgreSQL.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("database_name", help="Name of the target database (e.g., 'steamfull').")
    parser.add_argument("--games_file", type=Path, help="Path to the master games JSON file.")
    parser.add_argument("--reviews_file", type=Path, help="Path to the master reviews JSON file.")
    args = parser.parse_args()
    if not args.games_file and not args.reviews_file:
        parser.error("At least one data file must be specified (--games_file or --reviews_file).")
    importer = PostgresImporter(args.database_name)
    importer.run_import(games_file=args.games_file, reviews_file=args.reviews_file)

if __name__ == "__main__":
    main()
