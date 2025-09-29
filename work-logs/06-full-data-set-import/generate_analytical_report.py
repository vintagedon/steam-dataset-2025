# =================================================================================================
# File:          generate_analytical_report.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon)  |  GitHub: https://github.com/vintagedon  |  ORCID: 0009-0008-7695-4093
# License:       MIT
# Last Updated:  2025-09-29
#
# Purpose:
#   Execute labeled SQL blocks, render charts, assemble a Markdown analysis report.
#
# Section Map:
#   1) Imports — dependencies and why they're needed
#   2) Configuration & Setup — env, logging, runtime knobs
#   3) Core Components — classes/functions with intent + IO contracts
#   4) Orchestration — how components are wired together
#   5) Entry Point — CLI usage and safe error handling
#
# Provenance / RAG Hints:
#   SOURCE_OF_TRUTH: Steam master JSON & PostgreSQL (see Phase 04 schema)
#   READS / WRITES:  unchanged from original script behavior
#
# Security:
#   - Secrets via .env only (PG_* / STEAM_API_KEY); do not hardcode credentials.
#
# Change Log (docs-only):
#   - 2025-09-29  Added standardized header + dual-audience inline comments; no behavioral changes.
# =================================================================================================

# --- Imports --------------------------------------------------------------------------------------
# Human: Group stdlib vs third-party; fail fast with helpful install hints.
# ML:    DEPENDS_ON — capture runtime libs for reproducibility.
import os
import sys
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from datetime import datetime

# --- Configuration ---
SQL_FILE = 'analysis_queries.sql'
REPORT_FILE = 'steam_full_analysis_report.md'
CHART_DIR = 'charts'
QUERY_SEPARATOR = '-- === END QUERY ==='

# --- Core Component -------------------------------------------------------------------------------
# Human: Prepare output dirs / plotting style.
# ML:    SIDE_EFFECTS: mkdir charts/; style set
def ):
    """Creates the chart directory and sets plot styles."""
    print(f"Ensuring chart directory '{CHART_DIR}' exists...")
    os.makedirs(CHART_DIR, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="viridis")
    plt.style.use('seaborn-v0_8-whitegrid')

# --- Core Component -------------------------------------------------------------------------------
# Human: Convert DataFrame to compact Markdown table.
# ML:    CONTRACT(df->md_table)
def df, max_rows=15):
    """Formats a Pandas DataFrame into a Markdown table."""
    if df.empty:
        return "No results found for this query.\n"
    if len(df) > max_rows:
        display_df = df.head(max_rows)
        truncation_note = f"\n*... (truncated to the top {max_rows} rows)*\n"
    else:
        display_df = df
        truncation_note = "\n"
    return display_df.to_markdown(index=False) + truncation_note

# --- Core Component -------------------------------------------------------------------------------
# Human: Heuristic chart selection + PNG export + section MD.
# ML:    CONTRACT(df->png+md) WRITES chart file
def title, df):
    """Generates a chart based on the query title and returns a Markdown section."""
    # Sanitize title for filename
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
    chart_filename = f"{safe_title.lower().replace(' ', '_')}.png"
    chart_filepath = os.path.join(CHART_DIR, chart_filename)
    report_section = [f"## {title}\n"]

    try:
        plt.figure(figsize=(12, 8))
        
        if "Co-occurrence Heatmap" in title:
            if len(df.columns) < 3: raise ValueError("Heatmap data requires at least 3 columns.")
            heatmap_data = df.pivot(index=df.columns[0], columns=df.columns[1], values=df.columns[2])
            sns.heatmap(heatmap_data, cmap="viridis").set_title(title)
            report_section.append("Shows which genres are most frequently paired on the same game.\n")
        elif "Top 15" in title or "Top 10" in title:
            category_col, value_col = df.columns[0], df.columns[1]
            sns.barplot(x=value_col, y=category_col, data=df, orient='h').set_title(title)
        elif "Score Distribution" in title:
            sns.barplot(x='score_range', y='game_count', data=df).set_title(title)
            plt.xticks(rotation=45)
        elif "Price Distribution by" in title:
            genre_col, price_col = df.columns[0], df.columns[1]
            sns.boxplot(x=price_col, y=genre_col, data=df, orient='h', showfliers=False)
            plt.title(f"{title} (outliers removed)")
            plt.xlabel("Price (USD)")
            summary_stats = df.groupby(genre_col)[price_col].describe()
            report_section.append("Key summary statistics for price by genre:\n")
            report_section.append(format_dataframe_as_markdown(summary_stats.reset_index()))
        elif "Pricing Trends Over Time" in title:
            df_agg = df.groupby('release_year')['initial_price_dollars'].mean().reset_index()
            sns.lineplot(x='release_year', y='initial_price_dollars', data=df_agg).set_title(title)
        elif "Games Released Per Year" in title or "Hardware Trends" in title:
             sns.lineplot(x=df.columns[0], y=df.columns[1], data=df).set_title(title)
        elif "Monthly Game Releases" in title:
             # Ensure correct sorting by month number
             df_sorted = df.sort_values('month_number')
             sns.barplot(x='release_month', y='game_count', data=df_sorted).set_title(title)
             plt.xticks(rotation=45)
        elif "Quality vs. Quantity" in title or "Achievement Count vs. Metacritic" in title:
            # Use column names for robustness
            x_col = df.columns[1]
            y_col = df.columns[2] if "Quality" in title else df.columns[0]
            sns.regplot(x=x_col, y=y_col, data=df, scatter_kws={'alpha':0.2}, line_kws={'color':'red'})
            plt.title(title)
        elif "Platform Support Distribution" in title:
            df_filtered = df[df['game_count'] > df['game_count'].sum() * 0.01]
            plt.pie(df_filtered['game_count'], labels=df_filtered['platform_combination'], autopct='%1.1f%%', startangle=90, wedgeprops={"edgecolor":"k"})
            plt.title(title)
            plt.ylabel('')
        elif "Average Price by Platform Support" in title:
            sns.barplot(x='platform_support', y='average_price_usd', data=df).set_title(title)
        else: # Default for tables like Correlation Matrix
            print(f" -> No specific chart type for '{title}'. Defaulting to table.")
            report_section.append(format_dataframe_as_markdown(df))
            return "\n".join(report_section)

        plt.tight_layout()
        plt.savefig(chart_filepath)
        plt.close()
        report_section.append(f"![{title}]({chart_filepath})\n")
        if "Price Distribution by" not in title:
             report_section.append(format_dataframe_as_markdown(df))
        print(f" -> Successfully generated chart: {chart_filename}")
    except Exception as e:
        print(f" -> ERROR creating chart for '{title}': {e}")
        report_section.append(f"**Could not generate chart due to an error: {e}**\nRaw data:\n")
        report_section.append(format_dataframe_as_markdown(df))
    return "\n".join(report_section)

# --- Orchestration -------------------------------------------------------------------------------
# Human: Wire components; parse args; validate env; run safely.
# ML:    ENTRYPOINT(main) — transactional operations; robust error handling.
def main():
    print("--- Steam Dataset Visual Analysis Report Generator ---")
    setup_environment()
# --- Configuration & Setup ------------------------------------------------------------------------
# Human: Centralize env + logging knobs to keep core logic clean/testable.
# ML:    CONFIG_KEYS — parse constants/env names for orchestration.
    load_dotenv()
    db_name = os.getenv('PG_DB_STEAMFULL', 'steamfull')
    db_config = {
        'host': os.getenv('PG_HOST'), 'port': os.getenv('PG_PORT'),
        'user': os.getenv('PG_APP_USER'), 'password': os.getenv('PG_APP_USER_PASSWORD'),
        'dbname': db_name
    }
    if not all(val for key, val in db_config.items() if key != 'dbname'):
        print("Error: Database credentials missing in .env file.", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Reading queries from {SQL_FILE}...")
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            # Handle both kinds of newlines and filter empty blocks
            queries = [q.strip() for q in f.read().replace('\r\n', '\n').strip().split(QUERY_SEPARATOR) if q.strip()]
        print(f"Found {len(queries)} queries to execute.")
    except FileNotFoundError:
        print(f"Error: SQL file '{SQL_FILE}' not found.", file=sys.stderr)
        sys.exit(1)

    query_results = {}
    conn = None
    try:
        print(f"Connecting to PostgreSQL database '{db_config['dbname']}' at {db_config['host']}...")
        conn = psycopg2.connect(**db_config)
        print("Connection successful.\n")
        for i, query_block in enumerate(queries):
            title = query_block.splitlines()[0].replace('-- ===== CHART TITLE:', '').replace('=====', '').strip()
            print(f"Executing query {i+1}/{len(queries)}: \"{title}\"...")
            try:
                df = pd.read_sql_query(query_block, conn)
                query_results[title] = df
                print(f" -> Success! Fetched {len(df)} rows.")
            except Exception as e:
                print(f" -> ERROR executing query '{title}': {e}", file=sys.stderr)
                if conn and not conn.closed: conn.rollback()
    except psycopg2.OperationalError as e:
        print(f"\nFATAL: Could not connect to the database: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

    report_content = [f"# Steam Dataset Analysis Report ({db_config['dbname']})", f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EDT')}*\n---"]
    print("\n--- Generating Report Sections and Charts ---")
    for title, df in query_results.items():
        # Clean up title for new queries
        clean_title = title.replace("--  NEW QUERY", "").strip()
        report_section = process_and_visualize(clean_title, df)
        report_content.append(report_section)

    try:
        print(f"\nWriting final report to {REPORT_FILE}...")
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(report_content))
        print("--- Report generation complete! ---")
    except IOError as e:
        print(f"Error: Could not write report file: {e}", file=sys.stderr)

# --- Entry Point -----------------------------------------------------------------------------------
# Human: Direct CLI execution path with actionable errors.
# ML:    RUNTIME_START — begin telemetry if needed.
if __name__ == "__main__":
    main()
