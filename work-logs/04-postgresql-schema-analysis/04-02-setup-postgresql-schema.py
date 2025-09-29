# =================================================================================================
# Script:        04-02-setup-postgresql-schema.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       (unchanged; see original in file)
# Created:       (see original)
# Last Updated:  2025-09-29
#
# Purpose:
#   Provision PostgreSQL schema and roles for the dataset; idempotent DDL operations.
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
from pathlib import Path

try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries 'psycopg2' or 'python-dotenv' are not installed.", file=sys.stderr)
    print("Please install them using: pip install psycopg2-binary python-dotenv", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
CWD = Path.cwd()
ENV_FILE = CWD / '.env'
SCHEMA_FILE = CWD / 'schema.sql'
# --- Configuration & Setup ------------------------------------------------------------------------
# Human: centralize environment + logging so business logic stays testable and clean.
# ML:    CONFIG_KEYS — parse .env to map required/optional runtime knobs.
load_dotenv(dotenv_path=ENV_FILE)

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Utility Class for Colorized Output ---
class TColors:
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- Main Database Setup Class ---
class PostgresDatabaseSetup:
    """
    Handles the end-to-end process of connecting to PostgreSQL, ensuring the application
    user exists, and then creating/provisioning a database with the project schema.
    """
    def __init__(self):
        self.admin_config = {}
        self._load_and_validate_config()

    def _load_and_validate_config(self):
        """Loads and validates all required configuration from the environment."""
        required_vars = [
            'PG_HOST', 'PG_PORT', 'PG_ADMIN_USER', 'PG_ADMIN_PASSWORD',
            'PG_APP_USER', 'PG_APP_USER_PASSWORD'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            logging.error(f"FATAL: Missing required environment variables in .env file: {', '.join(missing_vars)}")
            sys.exit(1)
            
        if not SCHEMA_FILE.is_file():
            logging.error(f"FATAL: Schema file not found at '{SCHEMA_FILE}'. This script must be run in the same directory.")
            sys.exit(1)

        self.admin_user = os.getenv('PG_ADMIN_USER')
        self.admin_config = {
            'host': os.getenv('PG_HOST'),
            'port': os.getenv('PG_PORT'),
            'user': self.admin_user,
            'password': os.getenv('PG_ADMIN_PASSWORD'),
            'database': 'postgres'
        }
        self.app_user = os.getenv('PG_APP_USER')
        self.app_password = os.getenv('PG_APP_USER_PASSWORD')
        logging.info("Configuration loaded and validated successfully.")

    def get_connection(self, config: dict) -> psycopg2.extensions.connection:
        """Establishes and returns a database connection, handling potential errors."""
        try:
            conn = psycopg2.connect(**config)
            return conn
        except psycopg2.OperationalError as e:
            logging.error(f"❌ Failed to connect to PostgreSQL server at {config['host']}:{config['port']}. Check connection settings and server status.")
            logging.error(f"   Details: {e}")
            sys.exit(1)

    def _ensure_app_user_exists(self, admin_conn: psycopg2.extensions.connection):
        """
        Checks if the application user exists, creates it if not, and grants membership
        to the admin user so it can assign ownership.
        """
        logging.info(f"Ensuring application user '{self.app_user}' exists and is accessible...")
        with admin_conn.cursor() as cursor:
            try:
                cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s;", (self.app_user,))
                if cursor.fetchone():
                    logging.info(f"User '{self.app_user}' already exists.")
                else:
                    logging.info(f"User '{self.app_user}' not found. Creating user...")
                    self.execute_admin_command(admin_conn, f"CREATE USER {self.app_user} WITH PASSWORD %s;", (self.app_password,))
                    logging.info(f"✅ User '{self.app_user}' created successfully.")
                
                # --- THE FIX IS HERE ---
                # After creating the user, the admin must be granted membership in that role
                # to be able to assign ownership of objects (like databases) to it.
                logging.info(f"Granting membership of '{self.app_user}' to '{self.admin_user}'...")
                self.execute_admin_command(admin_conn, f"GRANT {self.app_user} TO {self.admin_user};")
                logging.info(f"✅ Membership granted.")

            except psycopg2.Error as e:
                logging.error(f"❌ Failed to manage application user: {e}")
                raise

    def does_db_exist(self, cursor: psycopg2.extensions.cursor, db_name: str) -> bool:
        """Checks if a database with the given name already exists."""
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
        return cursor.fetchone() is not None

    def execute_admin_command(self, conn: psycopg2.extensions.connection, sql: str, params=None):
        """Executes a command that requires autocommit mode."""
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_DEFAULT)

    def run_setup(self, db_name: str, recreate: bool):
        """Main orchestration method for the entire database setup process."""
        logging.info(f"🚀 Starting setup for database: '{db_name}' on host '{self.admin_config['host']}'")
        
        admin_conn = self.get_connection(self.admin_config)
        
        try:
            self._ensure_app_user_exists(admin_conn)
            
            with admin_conn.cursor() as cursor:
                db_exists = self.does_db_exist(cursor, db_name)

                if db_exists and recreate:
                    print(f"{TColors.BOLD}{TColors.WARNING}WARNING: Database '{db_name}' already exists.{TColors.ENDC}")
                    print(f"{TColors.WARNING}The --recreate flag was used. This will permanently delete the database and all its data.{TColors.ENDC}")
                    
                    confirm = input("Are you absolutely sure you want to continue? Type 'yes' to proceed: ")
                    if confirm.lower() == 'yes':
                        logging.info(f"User confirmed. Dropping database '{db_name}'...")
                        self.execute_admin_command(admin_conn, f"DROP DATABASE {db_name};")
                        logging.info(f"✅ Database '{db_name}' dropped successfully.")
                        db_exists = False
                    else:
                        logging.info("🛑 User aborted recreation. Exiting.")
                        sys.exit(0)
                
                elif db_exists and not recreate:
                    logging.warning(f"Database '{db_name}' already exists. Use the --recreate flag to drop and recreate it. Skipping setup.")
                    sys.exit(0)

            if not db_exists:
                logging.info(f"Creating database '{db_name}' with owner '{self.app_user}'...")
                sql = f"CREATE DATABASE {db_name} WITH OWNER = {self.app_user} ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE = template0;"
                self.execute_admin_command(admin_conn, sql)
                logging.info(f"✅ Database '{db_name}' created successfully.")

        except psycopg2.Error as e:
            logging.error(f"❌ A database error occurred during setup: {e}")
            sys.exit(1)
        finally:
            admin_conn.close()

        db_config = self.admin_config.copy()
        db_config['database'] = db_name
        
        logging.info(f"Applying schema from '{SCHEMA_FILE.name}' to '{db_name}'...")
        with self.get_connection(db_config) as conn:
            with conn.cursor() as cursor:
                try:
                    schema_sql = SCHEMA_FILE.read_text(encoding='utf-8')
                    cursor.execute(schema_sql)
                    conn.commit()
                    logging.info(f"✅ Schema applied successfully.")
                except (IOError, psycopg2.Error) as e:
                    logging.error(f"❌ Failed to apply schema: {e}")
                    conn.rollback()
                    sys.exit(1)

        logging.info(f"🎉 Setup for database '{db_name}' completed successfully!")

# --- Orchestration / CLI ---------------------------------------------------------------------------
# Human: defines the execution flow and CLI contract.
# ML:    ENTRYPOINT — parse args → wire components → run.
def main():
    """Parses command-line arguments and initiates the database setup utility."""
    parser = argparse.ArgumentParser(
        description="Create and provision a PostgreSQL database for the Steam Dataset project.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "database_name",
        type=str,
        help="The name of the database to create (e.g., 'steam_data_5k' or 'steam_data_full')."
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="If specified, the script will drop the database if it already exists and create it from scratch. A confirmation prompt will be shown."
    )
    args = parser.parse_args()
    
    try:
        setup = PostgresDatabaseSetup()
        setup.run_setup(db_name=args.database_name, recreate=args.recreate)
    except KeyboardInterrupt:
        logging.info("\n🛑 Setup interrupted by user.")
        sys.exit(1)

# --- Entry Point -----------------------------------------------------------------------------------
# Human: python -m / direct execution path with safe error handling.
# ML:    RUNTIME_START — begin metrics/telemetry if needed.
if __name__ == "__main__":
    main()
