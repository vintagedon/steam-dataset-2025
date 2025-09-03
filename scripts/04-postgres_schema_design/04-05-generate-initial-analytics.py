# =====================================================================================================================
# Script Name:    generate_initial_report.py
# Description:    Connects to the finalized Steam dataset database to perform an initial suite of
#                 analytical queries. It generates a comprehensive Markdown report detailing dataset
#                 statistics, content trends, commercial insights, and quality metrics to inform a
#                 full-scale data analysis plan.
#
# Author:         vintagedon (https://github.com/vintagedon)
# Repository:     https://github.com/vintagedon/steam-dataset-2025
#
# Version:        1.3
# Date:           2025-09-01
# License:        MIT License
#
# Usage:          Run with the target database name as an argument.
#                 Example: python generate_initial_report.py steam_data_5k
#
# =====================================================================================================================
#   MODIFICATION HISTORY
# =====================================================================================================================
#   Date:           Version:        Modified by:    Description of Changes:
#   --------------- --------------- --------------- -------------------------------------------------------------------
#   2025-08-31      1.2             vintagedon      Corrected developer quality query.
#   2025-09-01      1.3             vintagedon      Implemented the full, verified suite of analytical queries
#                                                   to produce a complete report.
# =====================================================================================================================

import os
import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime

try:
    import psycopg2
    from psycopg2.extras import DictCursor
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install psycopg2-binary python-dotenv", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Setup ---
load_dotenv()
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'), format='[%(asctime)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class InitialReporter:
    """Generates an initial analysis report from the Steam database."""

    def __init__(self, db_name: str):
        self._validate_config()
        self.conn_config = {
            'host': os.getenv('PG_HOST'), 'port': os.getenv('PG_PORT'), 'dbname': db_name,
            'user': os.getenv('PG_APP_USER'), 'password': os.getenv('PG_APP_USER_PASSWORD')
        }
        self.report_lines = [f"# Initial Analysis Report: Steam Dataset ('{db_name}')"]
        self.report_lines.append(f"*Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    def _validate_config(self):
        """Ensures application user connection settings are present."""
        required = ['PG_HOST', 'PG_PORT', 'PG_APP_USER', 'PG_APP_USER_PASSWORD']
        if any(not os.getenv(var) for var in required):
            logging.error("FATAL: Missing PostgreSQL application connection settings in .env file.")
            sys.exit(1)

    def run_report_generation(self):
        """Orchestrates the entire report generation process."""
        logging.info(f"🚀 Generating initial analysis report for database '{self.conn_config['dbname']}'.")
        
        try:
            with psycopg2.connect(**self.conn_config, cursor_factory=DictCursor) as conn:
                with conn.cursor() as cursor:
                    self._run_overview_queries(cursor)
                    self._run_taxonomy_queries(cursor)
                    self._run_commercial_queries(cursor)
                    self._run_quality_queries(cursor)

            report_content = "\n\n".join(self.report_lines)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = Path(f"initial_analysis_report_{self.conn_config['dbname']}_{timestamp}.md")
            
            with report_filename.open('w', encoding='utf-8') as f:
                f.write(report_content)
            logging.info(f"🎉 Report generation complete. Output saved to: {report_filename.name}")

        except psycopg2.Error as e:
            logging.error(f"❌ A database error occurred: {e}")
            sys.exit(1)

    # --- Query Execution Methods ---

    def _run_overview_queries(self, cursor):
        self.report_lines.append("## 1. High-Level Dataset Overview")
        cursor.execute("SELECT * FROM get_database_stats();")
        stats = cursor.fetchone()
        if not stats: return
        
        table = "| Metric | Count |\n| :--- | :--- |\n"
        table += f"| Total Applications | {stats['total_applications']:,} |\n"
        table += f"| Total Games | {stats['total_games']:,} |\n"
        table += f"| Total DLCs | {stats['total_dlc']:,} |\n"
        table += f"| Total Reviews | {stats['total_reviews']:,} |\n"
        table += f"| Unique Developers | {stats['total_developers']:,} |\n"
        table += f"| Unique Publishers | {stats['total_publishers']:,} |\n"
        self.report_lines.append(table)

    def _run_taxonomy_queries(self, cursor):
        self.report_lines.append("## 2. Content & Taxonomy Analysis")
        cursor.execute("""
            SELECT g.name, COUNT(ag.appid) as game_count
            FROM genres g JOIN application_genres ag ON g.id = ag.genre_id
            GROUP BY g.name ORDER BY game_count DESC LIMIT 15;
        """)
        self.report_lines.append("### Top 15 Most Common Genres")
        self._add_table_from_cursor(cursor)

    def _run_commercial_queries(self, cursor):
        self.report_lines.append("## 3. Commercial Analysis")
        cursor.execute("""
            SELECT 
                COUNT(*) FILTER (WHERE is_free = true) AS free_games,
                COUNT(*) FILTER (WHERE is_free = false) AS paid_games
            FROM applications WHERE type = 'game';
        """)
        stats = cursor.fetchone()
        if not stats or (stats['free_games'] + stats['paid_games'] == 0): return
        total = stats['free_games'] + stats['paid_games']
        self.report_lines.append(f"### Free vs. Paid Games\n- **Free-to-Play:** {stats['free_games']:,} ({stats['free_games']/total:.1%})\n- **Paid:** {stats['paid_games']:,} ({stats['paid_games']/total:.1%})")

        cursor.execute("""
            SELECT
                WIDTH_BUCKET(CAST(price_overview->>'final' AS NUMERIC) / 100.0, 0, 101, 5) AS bucket,
                COUNT(*) AS num_games
            FROM applications
            WHERE is_free = false AND price_overview->>'final' IS NOT NULL AND CAST(price_overview->>'final' AS NUMERIC) > 0
            GROUP BY bucket ORDER BY bucket;
        """)
        self.report_lines.append("### Price Distribution (for Paid Games)")
        price_table = "| Price Range | Game Count |\n| :--- | :--- |\n"
        ranges = ["$0.01 - $20", "$20.01 - $40", "$40.01 - $60", "$60.01 - $80", "$80.01 - $100", ">$100"]
        data = {row['bucket']: row['num_games'] for row in cursor.fetchall()}
        for i, r in enumerate(ranges, 1):
            price_table += f"| {r} | {data.get(i, 0):,} |\n"
        self.report_lines.append(price_table)

    def _run_quality_queries(self, cursor):
        self.report_lines.append("## 4. Quality & Reception Analysis")

        # Metacritic Score Distribution
        cursor.execute("""
            SELECT
                CASE
                    WHEN metacritic_score >= 90 THEN '90-100 (Universal Acclaim)'
                    WHEN metacritic_score >= 75 THEN '75-89 (Generally Favorable)'
                    WHEN metacritic_score >= 50 THEN '50-74 (Mixed/Average)'
                    ELSE '0-49 (Generally Unfavorable)'
                END AS score_bracket,
                COUNT(*) AS count
            FROM applications
            WHERE metacritic_score IS NOT NULL AND metacritic_score > 0
            GROUP BY score_bracket ORDER BY count DESC;
        """)
        self.report_lines.append("### Metacritic Score Distribution")
        self._add_table_from_cursor(cursor)

        # Top Developers by Avg. Metacritic Score
        cursor.execute("""
            SELECT 
                d.name as developer_name, 
                COUNT(a.appid) AS num_rated_products, 
                TRUNC(AVG(a.metacritic_score), 2) as avg_score
            FROM developers d
            JOIN application_developers ad ON d.id = ad.developer_id
            JOIN applications a ON ad.appid = a.appid
            WHERE a.metacritic_score IS NOT NULL AND a.metacritic_score > 0
            GROUP BY d.name
            HAVING COUNT(a.appid) >= 2
            ORDER BY avg_score DESC, num_rated_products DESC
            LIMIT 10;
        """)
        self.report_lines.append("### Top 10 Developers by Avg. Metacritic Score (min. 2 rated products)")
        self._add_table_from_cursor(cursor)

        # Top Publishers by Avg. Metacritic Score
        cursor.execute("""
            SELECT
                p.name AS publisher_name,
                COUNT(a.appid) AS num_rated_products,
                TRUNC(AVG(a.metacritic_score), 2) AS avg_score
            FROM publishers p
            JOIN application_publishers ap ON p.id = ap.publisher_id
            JOIN applications a ON ap.appid = a.appid
            WHERE a.metacritic_score IS NOT NULL AND a.metacritic_score > 0
            GROUP BY p.name
            HAVING COUNT(a.appid) >= 2
            ORDER BY avg_score DESC, num_rated_products DESC
            LIMIT 10;
        """)
        self.report_lines.append("### Top 10 Publishers by Avg. Metacritic Score (min. 2 rated products)")
        self.report_lines.append("*Note: The minimum number of rated products is set low for this sample dataset. A higher threshold should be used for the full dataset to ensure statistical significance.*")
        self._add_table_from_cursor(cursor)

        # Price vs. Quality Correlation
        cursor.execute("""
            SELECT
                TRUNC(CAST(CORR(metacritic_score, CAST(price_overview->>'final' AS NUMERIC) / 100.0) AS NUMERIC), 4) AS correlation
            FROM applications
            WHERE metacritic_score IS NOT NULL AND metacritic_score > 0
                AND is_free = false AND price_overview->>'final' IS NOT NULL;
        """)
        correlation = cursor.fetchone()['correlation']
        self.report_lines.append(f"### Price vs. Metacritic Score Correlation\n- **Pearson's Correlation Coefficient:** `{correlation}`\n- *Interpretation: A value close to 1 suggests a strong positive correlation, close to -1 suggests a strong negative correlation, and close to 0 suggests little to no correlation.*")

    def _add_table_from_cursor(self, cursor):
        """Helper to format cursor results into a Markdown table."""
        if cursor.rowcount == 0:
            self.report_lines.append("No data found for this query.")
            return
        
        headers = [desc[0] for desc in cursor.description]
        table = f"| {' | '.join(headers)} |\n| {' :--- |' * len(headers)}\n"
        for row in cursor.fetchall():
            table += f"| {' | '.join(str(v) for v in row)} |\n"
        self.report_lines.append(table)

def main():
    parser = argparse.ArgumentParser(description="Generate an initial analysis report from the Steam DB.")
    parser.add_argument("database_name", help="The name of the target database.")
    args = parser.parse_args()

    reporter = InitialReporter(args.database_name)
    reporter.run_report_generation()

if __name__ == "__main__":
    main()

