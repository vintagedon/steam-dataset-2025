# =====================================================================================================================
# Script Name:    generate_analytical_report.py
# Description:    An analytics script that connects to the Steam dataset database, executes a suite of
#                 pre-defined SQL queries, and generates a rich Markdown report with data tables and
#                 visualizations (charts, heatmaps) to provide initial insights into the dataset.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        1.0
# Date:           2025-09-02
# License:        MIT License
#
# Usage:          Run with the target database name as an argument.
#                 Example: python generate_analytical_report.py steam_data_5k
#
# Prerequisites:  - A populated PostgreSQL database.
#                 - An 'analysis_queries.sql' file in the same directory.
#                 - Required libraries: psycopg2, pandas, matplotlib, seaborn, python-dotenv
#
# =====================================================================================================================
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-09-02      1.0             vintagedon      Initial release of the visual reporting script.
#
# =====================================================================================================================

import os
import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime

# A try-except block for imports provides a clean, user-friendly exit if dependencies are missing.
# This is a best practice for creating distributable command-line tools.
try:
    import psycopg2
    from psycopg2.extras import DictCursor
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required data analysis libraries are not installed.", file=sys.stderr)
    print("Please run: pip install pandas matplotlib seaborn psycopg2-binary python-dotenv", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Constants ---
# By decoupling the SQL from the Python code, we adhere to the separation of concerns principle.
# This allows the SQL (the "what") to be developed, tested, and maintained independently of the Python
# orchestration logic (the "how"). This is a hallmark of a robust data pipeline.
SQL_FILE = Path('analysis_queries.sql')
CHART_DIR = Path('charts') # Directory to save generated charts
QUERY_SEPARATOR = '-- === END QUERY ==='

def setup_environment():
    """
    Prepares the execution environment by creating the chart directory and setting
    a professional, consistent style for all generated visualizations.
    """
    logging.info(f"Ensuring chart directory '{CHART_DIR}' exists...")
    CHART_DIR.mkdir(exist_ok=True)
    
    # Set a professional theme for all plots for consistency and visual appeal.
    sns.set_theme(style="whitegrid", palette="viridis")
    plt.style.use('seaborn-v0_8-whitegrid')

def format_dataframe_as_markdown(df: pd.DataFrame, max_rows=15) -> str:
    """
    Formats a Pandas DataFrame into a Markdown table. To keep the report concise,
    it truncates the table if it exceeds a maximum number of rows.
    """
    if df.empty:
        return "No data found for this query.\n"
    # Truncate for display if necessary
    truncation_note = ""
    if len(df) > max_rows:
        df = df.head(max_rows)
        truncation_note = f"\n*... (truncated to the top {max_rows} rows)*\n"
    return df.to_markdown(index=False) + truncation_note

def process_and_visualize(title: str, df: pd.DataFrame) -> str:
    """
    The core visualization engine. This function acts as a "router", inspecting the
    title of the query to determine the most appropriate chart type. It generates,
    saves, and formats the output for the Markdown report.
    """
    chart_filename = f"{title.lower().replace(' ', '_').replace('&', 'and')}.png"
    chart_filepath = CHART_DIR / chart_filename
    report_section = [f"### {title}\n"]

    try:
        # Set a standard figure size for consistent chart dimensions.
        plt.figure(figsize=(12, 8))
        
        # --- Visualization Logic Router ---
        # This pattern uses keywords in the query title to select the correct plot type. It's a simple
        # yet effective way to map data to visualizations without complex code.
        if "Top 15" in title or "Top 10" in title:
            category_col, value_col = df.columns[0], df.columns[1]
            sns.barplot(x=value_col, y=category_col, data=df, orient='h').set_title(title)
            # tight_layout() is important for preventing chart labels from being cut off in the final image.
            plt.tight_layout()
        elif "Distribution" in title:
            # Assumes the first column is the category/bucket and the second is the count.
            category_col, value_col = df.columns[0], df.columns[1]
            sns.barplot(x=category_col, y=value_col, data=df).set_title(title)
            plt.xticks(rotation=45, ha='right') # Improve label readability for vertical charts.
            plt.tight_layout()
        else:
            # If no specific chart type is matched, we default to showing only the data table.
            # This makes the script resilient to new queries being added without visualization logic.
            logging.warning(f"No specific chart type for '{title}'. Defaulting to table-only output.")
            report_section.append(format_dataframe_as_markdown(df))
            return "\n".join(report_section)

        # Save the plot to a file and, critically, close the figure to free up memory.
        # Forgetting plt.close() in a loop can lead to memory leaks in scripts generating many charts.
        plt.savefig(chart_filepath)
        plt.close()
        logging.info(f"Successfully generated chart: {chart_filepath.name}")
        
        # --- Assemble the Markdown section for the report ---
        report_section.append(f"![{title}]({chart_filepath.relative_to(CWD)})\n")
        report_section.append(format_dataframe_as_markdown(df))

    except Exception as e:
        # Gracefully handle any errors during plotting, ensuring the report still generates.
        # This prevents a single faulty query/chart from halting the entire process.
        logging.error(f"Could not generate chart for '{title}': {e}")
        report_section.append(f"**Could not generate chart due to an error: {e}**\n")
        report_section.append("Raw data:\n")
        report_section.append(format_dataframe_as_markdown(df))

    return "\n".join(report_section)

def main():
    """Main function to orchestrate the entire report generation process."""
    parser = argparse.ArgumentParser(description="Generate a visual analysis report from the Steam DB.")
    parser.add_argument("database_name", help="The name of the target database (e.g., 'steam5k').")
    args = parser.parse_args()
    
    setup_environment()

    # --- Load Database Credentials ---
    logging.info("Loading database credentials from .env file...")
    load_dotenv()
    db_config = {
        'host': os.getenv('PG_HOST'), 'port': os.getenv('PG_PORT'),
        'user': os.getenv('PG_APP_USER'), 'password': os.getenv('PG_APP_USER_PASSWORD'),
        'dbname': args.database_name
    }
    if not all(v for k, v in db_config.items() if k != 'password'): # Password can be empty
        logging.error("Database connection credentials missing in .env file.")
        sys.exit(1)

    # --- Read SQL Queries from External File ---
    try:
        logging.info(f"Reading queries from {SQL_FILE.name}...")
        with SQL_FILE.open('r', encoding='utf-8') as f:
            # Split the file content into individual query blocks using our custom separator.
            queries = [q.strip() for q in f.read().strip().split(QUERY_SEPARATOR) if q.strip()]
        logging.info(f"Found {len(queries)} queries to execute.")
    except FileNotFoundError:
        logging.error(f"FATAL: SQL file '{SQL_FILE.name}' not found. It must be in the same directory.")
        sys.exit(1)

    # --- Phase 1: Data Retrieval from PostgreSQL ---
    query_results: Dict[str, pd.DataFrame] = {}
    conn = None
    try:
        logging.info(f"Connecting to PostgreSQL database '{args.database_name}' at {db_config['host']}...")
        conn = psycopg2.connect(**db_config)
        logging.info("Connection successful.\n")

        for query_block in queries:
            # The title is embedded in the SQL file itself, a simple but effective metadata pattern.
            title = query_block.splitlines()[0].replace('-- ===== CHART TITLE:', '').replace('=====', '').strip()
            logging.info(f"Executing query: \"{title}\"...")

            try:
                # pandas.read_sql_query is a highly efficient way to execute a query and
                # load the results directly into a structured DataFrame, automatically handling data types.
                df = pd.read_sql_query(query_block, conn)
                query_results[title] = df
                logging.info(f" -> Success! Fetched {len(df)} rows.")
            except Exception as e:
                logging.error(f" -> ERROR executing query '{title}': {e}", exc_info=True)
                # It is good practice to rollback a transaction on any error, even for SELECTs,
                # to ensure a clean connection state for the next query.
                if conn: conn.rollback()
    
    except psycopg2.OperationalError as e:
        logging.critical(f"FATAL: Could not connect to the database: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            logging.info("\nDatabase connection closed.")

    # --- Phase 2: Generate Report Content (Visualize & Format) ---
    report_content = [f"# Steam Dataset Analysis Report: `{args.database_name}`"]
    report_content.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n---")

    logging.info("\n--- Generating Report Sections and Charts ---")
    for title, df in query_results.items():
        report_section = process_and_visualize(title, df)
        report_content.append(report_section)

    # --- Phase 3: Write Final Report to Disk ---
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = Path(f"analytical_report_{args.database_name}_{timestamp}.md")
    try:
        logging.info(f"\nWriting final report to {report_filename.name}...")
        with report_filename.open('w', encoding='utf-8') as f:
            f.write("\n\n".join(report_content))
        logging.info("--- Report generation complete! ---")
    except IOError as e:
        logging.error(f"Could not write report file: {e}")

if __name__ == "__main__":
    main()

