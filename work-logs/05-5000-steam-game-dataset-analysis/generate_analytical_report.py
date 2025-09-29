# =================================================================================================
# File:          generate_analytical_report.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Run labeled SQL blocks, build DataFrames, render charts, and assemble a visual report.
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
#   $ python generate_analytical_report.py
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
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from datetime import datetime

# --- Configuration & Runtime Knobs ---------------------------------------------------------------
# Human: Centralize filenames, separators, output paths; keep behavior switchable via env where sane.
# ML:    CONFIG_KEYS — extract constant names for downstream orchestration.
# --- Configuration ---
SQL_FILE = 'analysis_queries.sql'
REPORT_FILE = 'steam_analysis_report_visual.md'
CHART_DIR = 'charts' # Directory to save generated charts
QUERY_SEPARATOR = '-- === END QUERY ==='

# --- New Function: Ensure chart directory exists ---
# --- Core Component -------------------------------------------------------------------------------
# Human: Create output directories and set plotting style for consistent visuals.
# ML:    SIDE_EFFECTS: mkdir charts/; global style for matplotlib/seaborn
def setup_environment():
    """Creates the chart directory if it doesn't exist."""
    print(f"Ensuring chart directory '{CHART_DIR}' exists...")
    os.makedirs(CHART_DIR, exist_ok=True)
    
    # Set a professional style for all plots
    sns.set_theme(style="whitegrid")
    plt.style.use('seaborn-v0_8-whitegrid')


# --- Modified Function: Now accepts a Pandas DataFrame ---
# --- Core Component -------------------------------------------------------------------------------
# Human: Compact view of DataFrame; truncation keeps reports readable.
# ML:    CONTRACT(df->md_table): DataFrame -> str (<=max_rows)
def format_dataframe_as_markdown(df, max_rows=15):
    """Formats a Pandas DataFrame into a Markdown table, truncating if too long."""
    if df.empty:
        return "No results found for this query.\n"
    
    # Truncate the DataFrame if it's too large to display
    if len(df) > max_rows:
        display_df = df.head(max_rows)
        truncation_note = f"\n*... (truncated to the top {max_rows} rows)*\n"
    else:
        display_df = df
        truncation_note = "\n"

    return display_df.to_markdown(index=False) + truncation_note

# --- New Function: Core logic for processing and visualization ---
# --- Core Component -------------------------------------------------------------------------------
# Human: Heuristically select chart type based on block title; save PNG + embed table snippet.
# ML:    CONTRACT(df->png+md): title:str, df:DataFrame -> markdown_section:str; WRITES chart file
def process_and_visualize(title, df):
    """
    Analyzes a DataFrame based on its title, generates a chart, 
    and returns a formatted Markdown section for the report.
    """
    chart_filename = f"{title.lower().replace(' ', '_').replace('(', '').replace(')', '')}.png"
    chart_filepath = os.path.join(CHART_DIR, chart_filename)
    report_section = [f"## {title}\n"]

    try:
        # Set a figure size for better readability
        plt.figure(figsize=(12, 8))

        # --- Logic to select the right chart and summary based on title ---
        if "Co-occurrence Heatmap" in title:
            # Pivot the data to create a matrix for the heatmap
            heatmap_data = df.pivot(index='genre_a', columns='genre_b', values='co_occurrence_count')
            sns.heatmap(heatmap_data, cmap="viridis").set_title(title)
            report_section.append("Shows which genres are most frequently paired on the same game.\n")

        elif "Top 15" in title or "Top 10" in title:
            # Assumes the first column is the category and the second is the value
            category_col, value_col = df.columns[0], df.columns[1]
            sns.barplot(x=value_col, y=category_col, data=df, orient='h').set_title(title)
            plt.tight_layout() # Adjust layout to prevent labels from being cut off

        elif "Score Distribution" in title:
            score_col = df.columns[1]
            sns.barplot(x='score_range', y=score_col, data=df).set_title(title)
            plt.xticks(rotation=45)
            plt.tight_layout()

        elif "Price Distribution by" in title:
            genre_col, price_col = df.columns[0], df.columns[1]
            sns.boxplot(x=price_col, y=genre_col, data=df, orient='h', showfliers=False) # Outliers hidden for clarity
            plt.title(f"{title} (outliers removed for clarity)")
            plt.xlabel("Price (USD)")
            plt.tight_layout()
            # Add summary statistics as the text part of the report
            summary_stats = df.groupby(genre_col)[price_col].describe()
            report_section.append("Key summary statistics for price by genre:\n")
            report_section.append(format_dataframe_as_markdown(summary_stats.reset_index()))

        elif "Pricing Trends Over Time" in title:
            # Aggregate data for a cleaner plot
            df_agg = df.groupby('release_year')['initial_price_dollars'].mean().reset_index()
            sns.lineplot(x='release_year', y='initial_price_dollars', data=df_agg).set_title(title)
            report_section.append("Shows the average initial price of games released each year.\n")
            report_section.append(format_dataframe_as_markdown(df_agg))
        
        elif "Games Released Per Year" in title:
            sns.lineplot(x='release_year', y='game_count', data=df).set_title(title)
            report_section.append("Shows the volume of game releases on Steam over time.\n")

        elif "Quality vs. Quantity" in title:
            sns.scatterplot(x='quantity_games_released', y='avg_metacritic_score', data=df).set_title(title)
            report_section.append("Plots developers by the number of games released vs. their average critic score.\n")

        else:
             # Default for unrecognized chart types: just show the table
            print(f" -> No specific chart type for '{title}'. Defaulting to table.")
            report_section.append(format_dataframe_as_markdown(df))
            return "\n".join(report_section)


        # Save the plot
        plt.savefig(chart_filepath)
        plt.close() # Close the figure to free up memory

        # Add image link and a sample of the data to the report
        report_section.append(f"![{title}]({chart_filepath})\n")
        if "Price Distribution by" not in title: # Avoid duplicating data
             report_section.append(format_dataframe_as_markdown(df))
        
        print(f" -> Successfully generated chart: {chart_filename}")

    except Exception as e:
        print(f" -> ERROR creating chart for '{title}': {e}")
        report_section.append(f"**Could not generate chart due to an error: {e}**\n")
        report_section.append("Raw data:\n")
        report_section.append(format_dataframe_as_markdown(df))

    return "\n".join(report_section)


# --- Orchestration -------------------------------------------------------------------------------
# Human: Load env; parse SQL blocks; connect; execute; aggregate results; write report.
# ML:    ENTRYPOINT(main): uses CONFIG_KEYS + DB creds; transactional per‑query execution.
def main():
    """Main function to generate the report."""
    print("--- Steam Dataset Visual Analysis Report Generator ---")
    setup_environment()

    # --- Load Environment Variables ---
    print("Loading database credentials...")
    load_dotenv()
    db_config = {
        'host': os.getenv('PG_HOST'), 'port': os.getenv('PG_PORT'),
        'user': os.getenv('PG_APP_USER'), 'password': os.getenv('PG_APP_USER_PASSWORD'),
        'dbname': 'steam5k'
    }
    if not all(db_config.values()):
        print("Error: Database credentials missing in .env file.", file=sys.stderr)
        sys.exit(1)

    # --- Read SQL Queries ---
    try:
        print(f"Reading queries from {SQL_FILE}...")
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            queries = [q.strip() for q in f.read().strip().split(QUERY_SEPARATOR) if q.strip()]
        print(f"Found {len(queries)} queries to execute.")
    except FileNotFoundError:
        print(f"Error: SQL file '{SQL_FILE}' not found.", file=sys.stderr)
        sys.exit(1)

    # --- Phase 1: Data Retrieval ---
    query_results = {}
    conn = None
    try:
        print(f"Connecting to PostgreSQL database at {db_config['host']}...")
        conn = psycopg2.connect(**db_config)
        print("Connection successful.\n")

        for i, query_block in enumerate(queries):
            first_line = query_block.splitlines()[0]
            title = first_line.replace('-- ===== CHART TITLE:', '').replace('=====', '').strip()
            print(f"Executing query {i+1}/{len(queries)}: \"{title}\"...")

            try:
                # Use pandas to execute the query directly into a DataFrame
                df = pd.read_sql_query(query_block, conn)
                if not df.empty:
                    query_results[title] = df
                    print(f" -> Success! Fetched {len(df)} rows.")
                else:
                    print(f" -> Success! Query returned no data.")
            except Exception as e:
                print(f" -> ERROR executing query '{title}': {e}", file=sys.stderr)
                conn.rollback() # Rollback the transaction on error

    except psycopg2.OperationalError as e:
        print(f"\nFATAL: Could not connect to the database: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

    # --- Phase 2 & 3: Process, Visualize, and Write Report ---
    report_content = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S EDT')
    report_content.append(f"# Steam Dataset Analysis Report")
    report_content.append(f"*Generated on: {timestamp}*\n---\n")

    print("\n--- Generating Report Sections and Charts ---")
    for title, df in query_results.items():
        report_section = process_and_visualize(title, df)
        report_content.append(report_section)

    try:
        print(f"\nWriting final report to {REPORT_FILE}...")
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_content))
        print("--- Report generation complete! ---")
    except IOError as e:
        print(f"Error: Could not write report file: {e}", file=sys.stderr)
        sys.exit(1)

# --- Entry Point -----------------------------------------------------------------------------------
# Human: Allows direct CLI execution. Keep exception messages actionable for operators.
# ML:    RUNTIME_START — start timers/telemetry if desired.
if __name__ == "__main__":
    main()