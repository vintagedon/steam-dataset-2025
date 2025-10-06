# =====================================================================================================================
# Script Name:    02-populate-requirements-columns.py
# Description:    Phase 2.2 Sprint 1: PC Requirements Parsing - Data Population
#                 Connects to the database, fetches records with pc_requirements data,
#                 parses the HTML using BeautifulSoup, and populates the materialized
#                 mat_pc_* columns using safe, parameterized queries.
#
# Author:         VintageDon (https://github.com/vintagedon)
# Collaborator:   Claude Sonnet 4 (AI Assistant)
#
# Version:        1.2 (Handles non-dict data types for pc_requirements)
# Date:           2025-09-29
# License:        MIT License
#
# Usage:          python 02-populate-requirements-columns.py
# =====================================================================================================================

import os
import sys
import logging
from pathlib import Path
import json

try:
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup
    from tqdm import tqdm
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install pandas sqlalchemy psycopg2-binary python-dotenv beautifulsoup4 tqdm", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
ENV_PATH = Path('/mnt/data2/global-config/research.env')
if not ENV_PATH.exists():
    logging.error(f"FATAL: Global environment file not found at '{ENV_PATH}'.")
    sys.exit(1)
load_dotenv(dotenv_path=ENV_PATH)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Constants ---
TARGET_FIELDS = ['OS', 'Processor', 'Memory', 'Graphics']
BATCH_SIZE = 2000

# --- Core Parsing Logic ---
def parse_html_fields(html_text: str) -> dict:
    if not html_text or not isinstance(html_text, str) or html_text.strip() == '':
        return {}
    
    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        fields = {}
        for li in soup.find_all('li'):
            strong = li.find('strong')
            if strong:
                label = strong.get_text(strip=True).rstrip(':*').strip()
                if label in TARGET_FIELDS:
                    value = li.get_text(strip=True).replace(strong.get_text(strip=True), '', 1).strip()
                    fields[label] = value
        return fields
    except Exception:
        return {}

# --- Orchestration ---
def run_population():
    logging.info("Starting population of materialized PC requirements columns...")

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
            logging.info("Fetching appids with PC requirements data...")
            
            fetch_query = text("""
                SELECT appid, pc_requirements 
                FROM applications 
                WHERE pc_requirements IS NOT NULL AND pc_requirements != '{}'::jsonb;
            """)
            result = conn.execute(fetch_query)
            records_to_process = result.fetchall()
            
            if not records_to_process:
                logging.warning("No records with PC requirements found to process.")
                return

            logging.info(f"Found {len(records_to_process):,} records to process. Starting population in batches of {BATCH_SIZE}.")

            for i in tqdm(range(0, len(records_to_process), BATCH_SIZE), desc="Populating Columns"):
                batch = records_to_process[i:i + BATCH_SIZE]
                
                with conn.begin(): # Start a transaction for the batch
                    for row in batch:
                        appid, pc_req_json = row
                        
                        try:
                            pc_req = json.loads(pc_req_json) if isinstance(pc_req_json, str) else pc_req_json
                        except (json.JSONDecodeError, TypeError):
                            continue
                        
                        # --- CRITICAL FIX ---
                        # Verify that pc_req is a dictionary before trying to call .get() on it.
                        if not isinstance(pc_req, dict):
                            logging.debug(f"Skipping appid {appid} because pc_requirements is not a dictionary (type: {type(pc_req)}).")
                            continue

                        min_fields = parse_html_fields(pc_req.get('minimum'))
                        rec_fields = parse_html_fields(pc_req.get('recommended'))

                        # Only proceed if we actually parsed something
                        if not min_fields and not rec_fields:
                            continue

                        params = {
                            "appid": appid,
                            "os_min": min_fields.get('OS'),
                            "proc_min": min_fields.get('Processor'),
                            "mem_min": min_fields.get('Memory'),
                            "gfx_min": min_fields.get('Graphics'),
                            "os_rec": rec_fields.get('OS'),
                            "proc_rec": rec_fields.get('Processor'),
                            "mem_rec": rec_fields.get('Memory'),
                            "gfx_rec": rec_fields.get('Graphics')
                        }

                        update_query = text("""
                            UPDATE applications SET
                                mat_pc_os_min = :os_min,
                                mat_pc_processor_min = :proc_min,
                                mat_pc_memory_min = :mem_min,
                                mat_pc_graphics_min = :gfx_min,
                                mat_pc_os_rec = :os_rec,
                                mat_pc_processor_rec = :proc_rec,
                                mat_pc_memory_rec = :mem_rec,
                                mat_pc_graphics_rec = :gfx_rec
                            WHERE appid = :appid;
                        """)
                        conn.execute(update_query, params)
            
            logging.info("✅ Population of PC requirements columns complete.")

    except Exception as e:
        logging.critical(f"An unexpected error occurred during population: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# --- Entry Point ---
if __name__ == "__main__":
    run_population()
