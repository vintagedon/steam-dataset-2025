# =================================================================================================
# File:          5k_report_generator.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Execute labeled SQL blocks, capture tabular results, and compile a Markdown report.
#
# Provenance / RAG Hints:
#   SOURCE_OF_TRUTH: PostgreSQL 'steam5k' database (see schema in Phase 04)
#   READS:          Labeled SQL blocks in 'analysis_queries.sql' (for .py), steam5k DB tables/views
#   WRITES:         Markdown report(s); chart images (visual variant)
#
# Operational Profile:
#   - Runtime: Python 3.9+
#   - Idempotency: Re-running regenerates report artifacts deterministically (DB state-dependent).
#   - Failure Modes: DB connectivity, missing env vars, malformed SQL blocks.
#
# Security:
#   - Secrets come from .env (PG_*). Avoid hardcoding credentials.
#
# Usage (unchanged logic):
#   $ python 5k_report_generator.py
#   Ensure '.env' has PG_HOST, PG_PORT, PG_APP_USER, PG_APP_USER_PASSWORD (and DB is reachable).
#
# Change Log (docs-only):
#   - 2025-09-29  Added standardized header and dual-audience comments; no behavioral changes.
# =================================================================================================

# --- Imports --------------------------------------------------------------------------------------
# Human: Group stdlib, third‑party, and project imports; fail fast on missing optional deps.
# ML:    DEPENDS_ON — derive runtime libraries and versions from import graph.
import os
import sys
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# --- Configuration & Runtime Knobs ---------------------------------------------------------------
# Human: Centralize filenames, separators, output paths; keep behavior switchable via env where sane.
# ML:    CONFIG_KEYS — extract constant names for downstream orchestration.
# --- Configuration ---
SQL_FILE = 'analysis_queries.sql'
REPORT_FILE = 'steam_analysis_report.md'
QUERY_SEPARATOR = '-- === END QUERY ==='

# --- Core Component -------------------------------------------------------------------------------
# Human: Convert DB rows to Markdown table with headers and alignment.
# ML:    CONTRACT(format->md_table): headers:list, rows:list -> str
def format_results_as_markdown(headers, data):
    """Formats query results into a Markdown table."""
    if not data:
        return "No results found for this query.\n"

    # Create header
    header_line = "| " + " | ".join(map(str, headers)) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"

    # Create data rows
    data_lines = []
    for row in data:
        data_lines.append("| " + " | ".join(map(str, row)) + " |")

    return "\n".join([header_line, separator_line] + data_lines) + "\n"

# --- Orchestration -------------------------------------------------------------------------------
# Human: Load env; parse SQL blocks; connect; execute; aggregate results; write report.
# ML:    ENTRYPOINT(main): uses CONFIG_KEYS + DB creds; transactional per‑query execution.
def main():
    """Main function to generate the report."""
    print("--- Steam 5k Analysis Report Generator ---")

    # --- Load Environment Variables ---
    print("Loading database credentials from .env file...")
    load_dotenv()
    db_config = {
        'host': os.getenv('PG_HOST'),
        'port': os.getenv('PG_PORT'),
        'user': os.getenv('PG_APP_USER'),
        'password': os.getenv('PG_APP_USER_PASSWORD'),
        'dbname': 'steam5k' # Assuming the database name is static
    }

    if not all(db_config.values()):
        print("Error: One or more required environment variables are missing.")
        print("Please ensure PG_HOST, PG_PORT, PG_APP_USER, and PG_APP_USER_PASSWORD are in your .env file.")
        sys.exit(1)

    # --- Read SQL Queries ---
    try:
        print(f"Reading queries from {SQL_FILE}...")
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        queries = sql_content.strip().split(QUERY_SEPARATOR)
        queries = [q.strip() for q in queries if q.strip()]
        print(f"Found {len(queries)} queries to execute.")

    except FileNotFoundError:
        print(f"Error: The SQL file '{SQL_FILE}' was not found.")
        sys.exit(1)

    # --- Database Connection and Execution ---
    conn = None
    report_content = []
    
    # Add report header
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S EDT')
    report_content.append(f"# Steam 5k Dataset Analysis Report")
    report_content.append(f"*Generated on: {timestamp}*\n")
    report_content.append("---\n")

    try:
        print(f"Connecting to PostgreSQL database at {db_config['host']}...")
        conn = psycopg2.connect(**db_config)
        print("Connection successful.\n")

        for i, query_block in enumerate(queries):
            # Each query will be in its own transaction context.
            try:
                with conn.cursor() as cur:
                    # Extract title from the first line of the block
                    first_line = query_block.splitlines()[0]
                    title = first_line.replace('-- ===== CHART TITLE:', '').replace('=====', '').strip()

                    print(f"Executing query {i+1}/{len(queries)}: \"{title}\"...")

                    cur.execute(query_block)
                    
                    # Fetch headers and data if the query returns results
                    if cur.description:
                        headers = [desc[0] for desc in cur.description]
                        data = cur.fetchall()
                        # Append formatted results to the report
                        report_content.append(f"## {title}\n")
                        report_content.append(format_results_as_markdown(headers, data))
                        print(f" -> Success! Fetched {len(data)} rows.")
                    else:
                        report_content.append(f"## {title}\n")
                        report_content.append("Query executed successfully, but returned no data.\n")
                        print(f" -> Success! Query returned no data.")
            
            except psycopg2.Error as e:
                # If a query fails, roll back the transaction and log the error
                conn.rollback() 
                error_message = f"Error executing query \"{title}\": {e}"
                print(f" -> {error_message}")
                report_content.append(f"## {title}\n")
                report_content.append(f"**Error executing this query.**\n```sql\n{e}\n```\n")

    except psycopg2.OperationalError as e:
        print(f"\nFATAL: Could not connect to the database: {e}")
        print("Please check your .env credentials and ensure the database is running and accessible.")
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

    # --- Write Report to File ---
    try:
        print(f"Writing comprehensive report to {REPORT_FILE}...")
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_content))
        print("--- Report generation complete! ---")
    except IOError as e:
        print(f"Error: Could not write report file: {e}")
        sys.exit(1)


# --- Entry Point -----------------------------------------------------------------------------------
# Human: Allows direct CLI execution. Keep exception messages actionable for operators.
# ML:    RUNTIME_START — start timers/telemetry if desired.
if __name__ == "__main__":
    main()
