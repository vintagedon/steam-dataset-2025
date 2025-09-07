# =====================================================================================================================
# Script Name:    setup_database.py
# Description:    A utility to create and configure a PostgreSQL database for the Steam Dataset project.
#                 It reads connection settings from a .env file, applies a schema from an external .sql file,
#                 and grants the necessary privileges to the application user.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        1.4
# Date:           2025-09-07
# License:        MIT License
#
# Usage:          This script operates on one database at a time.
#                 To create a database: python setup_database.py <database_name>
#                 To wipe and recreate: python setup_database.py <database_name> --recreate
#
# =====================================================================================================================
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-09-07      1.4             vintagedon      CRITICAL FIX: Added a final step to grant all necessary
#                                                   privileges to the PG_APP_USER after schema creation to
#                                                   prevent "permission denied" errors during import.
# =====================================================================================================================

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
    print("Please run: pip install psycopg2-binary python-dotenv", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
CWD = Path.cwd()
ENV_FILE = CWD / '.env'
SCHEMA_FILE = CWD / 'schema.sql'
load_dotenv(dotenv_path=ENV_FILE)

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Utility Class for Colorized Output ---
# This simple class improves the user experience by making critical warnings more visible.
class TColors:
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- Main Database Setup Class ---
class PostgresDatabaseSetup:
    """
    Handles the end-to-end process of connecting to PostgreSQL, ensuring the application
    user exists, creating/provisioning a database, and granting correct permissions.
    The design is idempotent, meaning it can be run multiple times safely.
    """
    def __init__(self):
        self.admin_config = {}
        self._load_and_validate_config()

    def _load_and_validate_config(self):
        """
        Loads and validates all required configuration from the environment.
        This is a "guard clause" pattern that fails fast if the environment is not
        correctly configured, preventing cryptic errors later in the script.
        """
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
            'database': 'postgres' # Connect to the default 'postgres' db for admin tasks
        }
        self.app_user = os.getenv('PG_APP_USER')
        self.app_password = os.getenv('PG_APP_USER_PASSWORD')
        logging.info("Configuration loaded and validated successfully.")

    def get_connection(self, config: dict) -> psycopg2.extensions.connection:
        """Establishes and returns a database connection, with robust error handling."""
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
        to the admin user. This is a critical prerequisite for assigning database ownership.
        """
        logging.info(f"Ensuring application user '{self.app_user}' exists...")
        with admin_conn.cursor() as cursor:
            try:
                cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s;", (self.app_user,))
                if cursor.fetchone():
                    logging.info(f"User '{self.app_user}' already exists.")
                else:
                    logging.info(f"User '{self.app_user}' not found. Creating user...")
                    self.execute_admin_command(admin_conn, f"CREATE USER {self.app_user} WITH PASSWORD %s;", (self.app_password,))
                    logging.info(f"✅ User '{self.app_user}' created successfully.")
                
                # This is a key piece of PostgreSQL security logic discovered during debugging.
                # To assign ownership of a database to 'PG_APP_USER', the creating role
                # ('PG_ADMIN_USER') must be a member of that role.
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
        """
        Executes a command that cannot run inside a transaction block (e.g., CREATE/DROP DATABASE).
        It temporarily sets the connection to autocommit mode.
        """
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_DEFAULT)

    def _grant_privileges(self, db_conn: psycopg2.extensions.connection):
        """
        Grants all necessary operational privileges to the application user for the new database.
        This is the final critical step to prevent "permission denied" errors during data import.
        """
        logging.info(f"Granting privileges to '{self.app_user}' on all tables and sequences...")
        with db_conn.cursor() as cursor:
            try:
                # Grant USAGE on the schema itself.
                cursor.execute(f"GRANT USAGE ON SCHEMA public TO {self.app_user};")
                # Grant all standard Data Manipulation Language (DML) privileges on existing tables.
                cursor.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO {self.app_user};")
                # This is a crucial future-proofing step. It ensures that any tables created
                # in the future by the admin user will automatically inherit these privileges.
                cursor.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {self.app_user};")
                # Grant privileges for sequences, which are necessary for the SERIAL primary keys in our lookup tables.
                cursor.execute(f"GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO {self.app_user};")
                cursor.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO {self.app_user};")
                db_conn.commit()
                logging.info("✅ Privileges granted successfully.")
            except psycopg2.Error as e:
                logging.error(f"❌ Failed to grant privileges: {e}")
                db_conn.rollback()
                raise

    def run_setup(self, db_name: str, recreate: bool):
        """Main orchestration method for the entire database setup process."""
        logging.info(f"🚀 Starting setup for database: '{db_name}' on host '{self.admin_config['host']}'")
        
        admin_conn = self.get_connection(self.admin_config)
        
        try:
            # The script follows a strict, logical order of operations:
            # 1. Ensure the user who will own the DB exists.
            self._ensure_app_user_exists(admin_conn)
            
            # 2. Check for the database and handle the --recreate flag.
            with admin_conn.cursor() as cursor:
                db_exists = self.does_db_exist(cursor, db_name)

                if db_exists and recreate:
                    # The interactive confirmation prompt is a critical safety rail to
                    # prevent accidental data loss in a development or production environment.
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

            # 3. Create the database.
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

        # 4. Connect to the new database as admin to apply the schema and grant permissions.
        db_config = self.admin_config.copy()
        db_config['database'] = db_name
        
        db_conn = self.get_connection(db_config)
        try:
            logging.info(f"Applying schema from '{SCHEMA_FILE.name}' to '{db_name}'...")
            with db_conn.cursor() as cursor:
                schema_sql = SCHEMA_FILE.read_text(encoding='utf-8')
                cursor.execute(schema_sql)
                db_conn.commit()
                logging.info(f"✅ Schema applied successfully.")
            
            # 5. Grant final privileges to the application user.
            self._grant_privileges(db_conn)

        except (IOError, psycopg2.Error) as e:
            logging.error(f"❌ Failed during schema application or permission granting: {e}")
            db_conn.rollback()
            sys.exit(1)
        finally:
            db_conn.close()

        logging.info(f"🎉 Setup for database '{db_name}' completed successfully!")

def main():
    """Parses command-line arguments and initiates the database setup utility."""
    parser = argparse.ArgumentParser(
        description="Create and provision a PostgreSQL database for the Steam Dataset project.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("database_name", type=str, help="The name of the database to create (e.g., 'steam5k' or 'steamfull').")
    parser.add_argument("--recreate", action="store_true", help="If specified, the script will drop the database if it already exists.")
    args = parser.parse_args()
    
    try:
        setup = PostgresDatabaseSetup()
        setup.run_setup(db_name=args.database_name, recreate=args.recreate)
    except KeyboardInterrupt:
        logging.info("\n🛑 Setup interrupted by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()

