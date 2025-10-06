# =================================================================================================
# File:          export_notebook_2_data.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# AI Collaborator: Claude.ai, Gemini
# License:       MIT
# Last Updated:  2025-10-05
#
# Purpose (Executive Summary – non-developer audience):
#   Generates the **static data artifacts** for Notebook 2: “Semantic Game Discovery”.
#   It exports:
#     • Clean CSVs for canonical analytical slices (e.g., top-reviewed games by genre)
#     • Numpy .npy files containing dense vector embeddings for games and reviews
#     • A small set of pre-computed semantic search examples for demo UX
#
#   These exports let notebook readers jump straight to analysis/visualization without
#   running heavy queries or GPU embedding steps live inside the notebook.
#
# Developer Notes (technical audience):
#   • Reads DB creds from /opt/global-env/research.env (PGSQL01_* variables)
#   • Uses SQLAlchemy for querying; Pandas/Numpy for serialization
#   • Keeps all queries centralized in ANALYTICAL_QUERIES
#   • Saves outputs into a timestamped directory: ./notebook_2_data_exports_YYYYmmdd_hhMMss
#
# Usage:
#   python export_notebook_2_data.py
#
# Operational Guidance:
#   • Ensure the target DB (default: steamfull) is reachable and embeddings exist where required
#   • Run on a host with sufficient RAM/IO for CSV and .npy serialization
#   • Outputs are designed to be versionable artifacts checked into the repo/notebook-data
# =================================================================================================

# --- 1. Imports & Configuration ------------------------------------------------------------------
# Dual-audience guidance:
#  - Non-dev: These imports bring in database, dataframes, and vector utilities.
#  - Dev: Keep import order stable to make linter output predictable during CI.

import os
import sys
import logging
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Fail fast with helpful messages if essential libraries are missing.
try:
    import pandas as pd
    import numpy as np
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
    from sentence_transformers import SentenceTransformer
except ImportError:
    # Non-dev: If you see this, your Python environment is missing required libraries.
    # Dev: Keep the message explicit for ops runbooks.
    print("Error: Required libraries are not installed.", file=sys.stderr)
    print("Please run: pip install pandas sqlalchemy psycopg2-binary python-dotenv sentence-transformers numpy", file=sys.stderr)
    sys.exit(1)

# --- Configuration & Logging Setup ---------------------------------------------------------------
# Non-dev: We load credentials from a central, secure env file.
# Dev: Keep this path aligned with your infra standards (Ansible roles / .env policy).
ENV_PATH = Path('/opt/global-env/research.env')
if not ENV_PATH.exists():
    logging.error(f"FATAL: Global environment file not found at '{ENV_PATH}'.")
    sys.exit(1)
load_dotenv(dotenv_path=ENV_PATH)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- 2. SQL Query Library & ML Setup -------------------------------------------------------------
# Non-dev: We write outputs into a new, time-stamped folder each run.
# Dev: This avoids accidental overwrites and makes runs auditable.
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_DIR = Path(f"./notebook_2_data_exports_{TIMESTAMP}")
OUTPUT_DIR.mkdir(exist_ok=True)

# Dual-audience:
#  - These canonical queries generate the lightweight CSVs the notebook consumes.
#  - Keep them deterministic, small(ish), and fast to execute so exports remain stable.

ANALYTICAL_QUERIES: Dict[str, Dict[str, Any]] = {
    # CSV: Top 1000 most-reviewed games overall (for quick demos & charts)
    "01_top1000_most_reviewed_games": {
        "description": "Top 1000 most reviewed games (appid, name, review_count).",
        "query": """
            SELECT
                a.appid,
                COALESCE(a.name, a.name_from_applist) AS name,
                COUNT(r.recommendationid) AS review_count
            FROM applications a
            LEFT JOIN reviews r ON a.appid = r.appid
            WHERE a.type = 'game' AND a.success = TRUE
            GROUP BY a.appid, COALESCE(a.name, a.name_from_applist)
            ORDER BY review_count DESC
            LIMIT 1000;
        """
    },

    # CSV: Balanced sample – top 100 by genre (useful for stratified demos)
    "02_top100_by_genre_balanced": {
        "description": "A balanced sample of the top 100 games for each genre.",
        "query": """
            WITH ranked_games AS (
                SELECT
                    a.appid, a.name, g.name as genre,
                    COUNT(r.recommendationid) as review_count,
                    ROW_NUMBER() OVER (PARTITION BY g.name ORDER BY COUNT(r.recommendationid) DESC) as genre_rank
                FROM applications a
                JOIN application_genres ag ON a.appid = ag.appid
                JOIN genres g ON ag.genre_id = g.id
                LEFT JOIN reviews r ON a.appid = r.appid
                WHERE a.type = 'game' AND a.success = TRUE AND a.description_embedding IS NOT NULL
                GROUP BY a.appid, a.name, g.name
            )
            SELECT appid, name, genre, review_count
            FROM ranked_games
            WHERE genre_rank <= 100
            ORDER BY genre, genre_rank;
        """
    }
}

# --- 3. Orchestration -----------------------------------------------------------------------------
def export_csv_data(engine):
    """
    For analysts (non-dev): Executes each ANALYTICAL_QUERIES entry and writes a clean CSV
    that the notebook can read directly.

    For developers:
    - Uses SQLAlchemy connections with Pandas read_sql for portability.
    - Each output is named <key>.csv under OUTPUT_DIR to keep references stable.
    """
    with engine.connect() as conn:
        for filename_base, query_info in ANALYTICAL_QUERIES.items():
            description = query_info["description"]
            query = query_info["query"]
            output_path = OUTPUT_DIR / f"{filename_base}.csv"
            logging.info(f"Executing query for: {description} -> '{output_path.name}'...")
            # Dev: Keep dtype inference default; these are demo-scale extracts.
            df = pd.read_sql(text(query), conn)
            df.to_csv(output_path, index=False, encoding="utf-8")
            logging.info(f"Wrote {len(df):,} rows -> {output_path}")

def export_embeddings_numpy(engine):
    """
    Non-dev: Exports dense embeddings from the database to .npy files so the notebook
    can load them instantly (no GPU or DB calls needed).

    Dev:
    - Assumes embeddings already populated in applications.description_embedding and
      reviews.review_embedding (vector extension).
    - Emits two artifacts:
        * app_embeddings.npy with mapping file app_embeddings_index.csv (appid order)
        * review_embeddings.npy with mapping file review_embeddings_index.csv (recommendationid order)
    - Keeps rows in DB natural ORDER BY appid/recommendationid for deterministic mapping.
    """
    apps_out_path = OUTPUT_DIR / "app_embeddings.npy"
    apps_index_csv = OUTPUT_DIR / "app_embeddings_index.csv"
    reviews_out_path = OUTPUT_DIR / "review_embeddings.npy"
    reviews_index_csv = OUTPUT_DIR / "review_embeddings_index.csv"

    with engine.connect() as conn:
        # --- Applications (game description embeddings) -------------------------------------------
        logging.info("Exporting application description embeddings to .npy ...")
        # Dev: SELECT order matters – do not alter without also changing index export.
        app_rows = conn.execute(text("""
            SELECT appid, description_embedding
            FROM applications
            WHERE type = 'game' AND success = TRUE AND description_embedding IS NOT NULL
            ORDER BY appid;
        """)).fetchall()

        if app_rows:
            app_ids = [row[0] for row in app_rows]
            # Non-dev: The DB stores vectors; here we convert them to a 2D numpy array.
            app_vecs = np.vstack([np.array(row[1]) for row in app_rows])
            np.save(apps_out_path, app_vecs)
            pd.DataFrame({"appid": app_ids}).to_csv(apps_index_csv, index=False)
            logging.info(f"Saved app embeddings: {app_vecs.shape} -> {apps_out_path.name}, index -> {apps_index_csv.name}")
        else:
            logging.info("No application embeddings found to export.")

        # --- Reviews (review text embeddings) ------------------------------------------------------
        logging.info("Exporting review embeddings to .npy ...")
        # Dev: Filter to English for size/signal; adapt as needed for multilingual notebooks.
        review_rows = conn.execute(text("""
            SELECT recommendationid, review_embedding
            FROM reviews
            WHERE review_embedding IS NOT NULL AND language = 'english'
            ORDER BY recommendationid;
        """)).fetchall()

        if review_rows:
            rec_ids = [row[0] for row in review_rows]
            review_vecs = np.vstack([np.array(row[1]) for row in review_rows])
            np.save(reviews_out_path, review_vecs)
            pd.DataFrame({"recommendationid": rec_ids}).to_csv(reviews_index_csv, index=False)
            logging.info(f"Saved review embeddings: {review_vecs.shape} -> {reviews_out_path.name}, index -> {reviews_index_csv.name}")
        else:
            logging.info("No review embeddings found to export.")

def generate_semantic_search_examples(engine):
    """
    Non-dev: Creates a tiny “starter pack” of semantic searches so the notebook can
    demonstrate results instantly.

    Dev:
    - Encodes a small list of queries with a sentence-transformer (CPU works; GPU faster).
    - Saves query vectors + labels as JSON for easy notebook consumption.
    - The notebook then uses pgvector (or in-memory cosine) to show nearest neighbors.
    """
    # Keep the model small for portability; notebook can swap to heavier models if needed.
    model_name = os.getenv("NOTEBOOK2_ENCODER_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    logging.info(f"Encoding starter semantic queries with model: {model_name}")
    model = SentenceTransformer(model_name)

    demo_queries = [
        "cozy farming game with community and pixel art",
        "futuristic first-person shooter with competitive multiplayer",
        "grand strategy about managing an empire and diplomacy",
        "open-world survival crafting on a hostile planet",
        "turn-based JRPG with party building and rich story"
    ]

    # Encode to unit-normalized vectors (default behavior for this model)
    q_vecs = model.encode(demo_queries, normalize_embeddings=True, convert_to_numpy=True)

    # Persist as a small JSON artifact the notebook can parse directly.
    # (JSON keeps this human-readable; size is trivial.)
    examples_path = OUTPUT_DIR / "semantic_query_examples.json"
    payload = {
        "model": model_name,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "queries": [
            {"text": q, "vector": vec.tolist()} for q, vec in zip(demo_queries, q_vecs)
        ]
    }
    examples_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    logging.info(f"Wrote starter semantic queries -> {examples_path.name}")

# --- 4. Main Entry Point -------------------------------------------------------------------------
def main():
    """
    Non-dev: Bootstraps DB connection and runs all export steps in order.
    Dev: Uses PGSQL01_* admin creds and the fixed DB name 'steamfull'.
    """
    # Centralized, explicit env var names for operational clarity.
    db_user = os.getenv('PGSQL01_ADMIN_USER')
    db_pass = os.getenv('PGSQL01_ADMIN_PASSWORD')
    db_host = os.getenv('PGSQL01_HOST')
    db_port = os.getenv('PGSQL01_PORT')
    db_name = 'steamfull'

    if not all([db_user, db_pass, db_host, db_port]):
        logging.error("Database credentials not found in environment file. Halting.")
        sys.exit(1)

    # Dev: psycopg2 driver via SQLAlchemy; keep protocol explicit for portability.
    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    try:
        engine = create_engine(db_url)
        
        # --- Run all export functions ---
        # Non-dev: Each step writes files into the timestamped folder created above.
        export_csv_data(engine)
        export_embeddings_numpy(engine)
        generate_semantic_search_examples(engine)

    except Exception as e:
        # Dev/Ops: Let systemd/tmux/log shipping capture structured CRITICAL lines.
        logging.critical(f"A critical error occurred: {e}")
        sys.exit(1)

    logging.info(f"🎉 All data exports for Notebook 2 are complete. Files are in '{OUTPUT_DIR.resolve()}'.")

if __name__ == "__main__":
    main()
