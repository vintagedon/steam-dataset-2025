#!/usr/bin/env python3
# =================================================================================================
# File:          02-generate-csv-package.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# AI Collaborators: ChatGPT, Gemini
# License:       MIT
# Last Updated:  2025-10-06
#
# Executive Summary (non-developer audience)
#   Exports the core Steam Dataset 2025 tables into **clean CSVs** and bundles them into a
#   single ZIP archive for easy download/use (Excel, Pandas, R, Tableau). Includes a
#   README and MANIFEST (with file hashes) so users know exactly what’s inside.
#
# Developer Notes (technical audience)
#   • Env: reads Postgres admin creds from /mnt/data2/global-config/research.env (PGSQL01_*).
#   • Scope-aware export: validates columns against live schema and warns on mismatches.
#   • I/O: chunked exports for large tables; UTF-8 CSVs; ZIP archive with zlib level 9.
#   • Docs: README.md summarizing counts/sizes; MANIFEST.json with SHA256 per file.
#   • Safety: no ORDER BY on large tables; engine.dispose() on exit; non-zero exit on fatal.
#   • COMMENTING ONLY — logic remains unchanged.
# =================================================================================================

"""
Script: generate_csv_package.py
Purpose: Export Steam Dataset 2025 tables to CSV format for accessibility
Author: VintageDon - https://github.com/vintagedon
Date: 2025-09-29
Version: 2.1

Exports all major tables (schema-aware) to CSV, then zips the package.
Changes in v2.1:
- Fixed schema mismatches (e.g., reviews.review_text).
- Removed non-existent application fields.
- Added application_platforms export.
- Schema-aware column selection (skip + warn on missing).
- Faster exports (no ORDER BY 1 on huge tables).
- UTC timestamp in README; engine.dispose(); optional MANIFEST.json with SHA256s.
"""

# --- Standard library imports --------------------------------------------------------------------
import os
import sys
import csv
import json
import hashlib
import logging
import zipfile
from pathlib import Path
from datetime import datetime, timezone

# --- Third-party imports (fail fast with guidance) -----------------------------------------------
try:
    import pandas as pd
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required libraries not installed.", file=sys.stderr)
    print("Run: pip install pandas sqlalchemy psycopg2-binary python-dotenv", file=sys.stderr)
    sys.exit(1)

# -----------------------------------
# Configuration
# -----------------------------------
# Non-dev: Centralized environment file with DB credentials.
# Dev: Keep this aligned with infra standards; do not embed secrets.
ENV_PATH = Path('/mnt/data2/global-config/research.env')

# Non-dev: Where the CSVs, README, and MANIFEST will be written.
# Dev: Stable relative path for CI/release jobs.
OUTPUT_DIR = Path('./data-packages/csv-package')
ZIP_NAME = 'steam_dataset_2025_csv_package.zip'
DB_NAME = 'steamfull'

# Tables to export with configurations
# Non-dev: Human-readable descriptions help users understand each CSV.
# Dev: 'columns' can be 'ALL' or an explicit allowlist. Missing columns are warned & skipped.
EXPORT_CONFIG = {
    'applications': {
        'description': 'Core game/app metadata with materialized features',
        'columns': [
            'appid', 'steam_appid', 'name', 'type', 'is_free',
            'release_date', 'required_age',
            # Descriptions (exclude very large HTML fields)
            'short_description',
            # Supported languages
            'supported_languages',
            # Media
            'header_image', 'background',
            # Ratings / counts
            'metacritic_score', 'recommendations_total',
            # Materialized - Platform Support
            'mat_supports_windows', 'mat_supports_mac', 'mat_supports_linux',
            # Materialized - Pricing
            'mat_initial_price', 'mat_final_price', 'mat_discount_percent', 'mat_currency',
            # Materialized - Achievements
            'mat_achievement_count',
            # Materialized - PC Requirements
            'mat_pc_os_min', 'mat_pc_processor_min', 'mat_pc_memory_min', 'mat_pc_graphics_min',
            'mat_pc_os_rec', 'mat_pc_processor_rec', 'mat_pc_memory_rec', 'mat_pc_graphics_rec',
            # Timestamps
            'created_at', 'updated_at'
        ],
        'chunk_size': 10000,
        'note': 'Excludes large HTML/JSONB fields and vector embeddings'
    },
    'reviews': {
        'description': 'User reviews with author metadata and voting information',
        'columns': [
            'recommendationid', 'appid', 'author_steamid',
            # Author stats
            'author_num_games_owned', 'author_num_reviews',
            'author_playtime_forever', 'author_playtime_last_two_weeks',
            'author_playtime_at_review', 'author_last_played',
            # Review content
            'language', 'review_text',
            # Timestamps
            'timestamp_created', 'timestamp_updated',
            # Voting
            'voted_up', 'votes_up', 'votes_funny', 'weighted_vote_score', 'comment_count',
            # Purchase info
            'steam_purchase', 'received_for_free', 'written_during_early_access',
            # Created/updated timestamps
            'created_at', 'updated_at'
        ],
        'chunk_size': 50000,
        'note': 'Excludes: review_embedding (1024-dim vector - use AI Researcher Package)'
    },
    'genres': {
        'description': 'Genre reference table (Action, RPG, Strategy, etc.)',
        'columns': 'ALL',
        'chunk_size': None
    },
    'categories': {
        'description': 'Category reference table (Single-player, Multi-player, Achievements, etc.)',
        'columns': 'ALL',
        'chunk_size': None
    },
    'developers': {
        'description': 'Developer reference table with unique IDs',
        'columns': 'ALL',
        'chunk_size': None
    },
    'publishers': {
        'description': 'Publisher reference table with unique IDs',
        'columns': 'ALL',
        'chunk_size': None
    },
    'platforms': {
        'description': 'Platform reference table (Windows, Mac, Linux)',
        'columns': 'ALL',
        'chunk_size': None
    },
    'application_genres': {
        'description': 'Many-to-many mapping: applications to genres',
        'columns': 'ALL',
        'chunk_size': 50000
    },
    'application_categories': {
        'description': 'Many-to-many mapping: applications to categories',
        'columns': 'ALL',
        'chunk_size': 50000
    },
    'application_developers': {
        'description': 'Many-to-many mapping: applications to developers',
        'columns': 'ALL',
        'chunk_size': 50000
    },
    'application_publishers': {
        'description': 'Many-to-many mapping: applications to publishers',
        'columns': 'ALL',
        'chunk_size': 50000
    },
    'application_platforms': {
        'description': 'Many-to-many mapping: applications to platforms (windows/mac/linux)',
        'columns': 'ALL',
        'chunk_size': 50000
    }
}

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# -----------------------------------
# Helpers
# -----------------------------------
def setup_environment():
    """Load environment and validate credentials.

    Non-dev: Stops early with a friendly error if the env file/creds are missing.
    Dev: Validates PGSQL01_* variables so we fail fast before connecting.
    """
    if not ENV_PATH.exists():
        logging.error(f"Environment file not found: {ENV_PATH}")
        sys.exit(1)

    load_dotenv(dotenv_path=ENV_PATH)

    required_vars = ['PGSQL01_ADMIN_USER', 'PGSQL01_ADMIN_PASSWORD',
                     'PGSQL01_HOST', 'PGSQL01_PORT']
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        logging.error(f"Missing environment variables: {', '.join(missing)}")
        sys.exit(1)

def create_connection():
    """Create database connection.

    Non-dev: Centralized connection builder.
    Dev: Uses psycopg2 driver via SQLAlchemy; echo disabled for performance.
    """
    db_url = (
        f"postgresql+psycopg2://{os.getenv('PGSQL01_ADMIN_USER')}:"
        f"{os.getenv('PGSQL01_ADMIN_PASSWORD')}@"
        f"{os.getenv('PGSQL01_HOST')}:{os.getenv('PGSQL01_PORT')}/{DB_NAME}"
    )
    engine = create_engine(db_url, echo=False)
    return engine

def get_table_columns(engine, table_name):
    """Get all column names for a table.

    Dev: Relies on information_schema; preserves ordinal position for consistent CSV column order.
    """
    query = text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = :table_name
        ORDER BY ordinal_position
    """)
    with engine.connect() as conn:
        result = pd.read_sql_query(query, conn, params={'table_name': table_name})
    return result['column_name'].tolist()

def _safe_select_columns(engine, table_name, wanted):
    """Intersect desired columns with actual schema; warn on missing.

    Non-dev: Prevents export failures when schema evolves slightly.
    Dev: If 'ALL', returns all columns in stable order; raises if nothing remains.
    """
    if wanted == 'ALL':
        return get_table_columns(engine, table_name), []
    existing = set(get_table_columns(engine, table_name))
    cols = [c for c in wanted if c in existing]
    missing = [c for c in wanted if c not in existing]
    if missing:
        logging.warning(f"{table_name}: skipping missing columns: {', '.join(missing)}")
    if not cols:
        raise RuntimeError(f"{table_name}: no valid columns to export after schema check.")
    return cols, missing

def export_table(engine, table_name, config, output_dir):
    """Export a single table to CSV with chunking for large tables.

    Non-dev: Writes a CSV per table; large tables stream out in chunks.
    Dev: Avoids ORDER BY; uses minimal quoting; logs progress every ~5 chunks.
    """
    logging.info(f"Exporting {table_name}...")
    try:
        # Determine columns to export (schema-aware)
        columns, _missing = _safe_select_columns(engine, table_name, config['columns'])
        columns_str = ', '.join(columns)

        # Build query (no ORDER BY for speed on large tables)
        query = f"SELECT {columns_str} FROM public.{table_name}"

        csv_path = output_dir / f"{table_name}.csv"
        chunk_size = config.get('chunk_size')

        # Export with or without chunking
        if chunk_size:
            logging.info(f"  Using chunked export (chunk_size={chunk_size:,})")
            first_chunk = True
            total_rows = 0
            with engine.connect() as conn:
                for chunk_df in pd.read_sql_query(text(query), conn, chunksize=chunk_size):
                    mode = 'w' if first_chunk else 'a'
                    header = first_chunk
                    # Quote minimally; handle embedded newlines safely
                    chunk_df.to_csv(
                        csv_path, mode=mode, header=header, index=False,
                        encoding='utf-8', quoting=csv.QUOTE_MINIMAL
                    )
                    total_rows += len(chunk_df)
                    first_chunk = False
                    if total_rows and (total_rows % (chunk_size * 5) == 0):
                        logging.info(f"    Progress: {total_rows:,} rows exported...")
            rows = total_rows
        else:
            with engine.connect() as conn:
                df = pd.read_sql_query(text(query), conn)
            df.to_csv(csv_path, index=False, encoding='utf-8', quoting=csv.QUOTE_MINIMAL)
            rows = len(df)

        size_mb = csv_path.stat().st_size / (1024 * 1024)
        cols_count = len(columns)
        logging.info(f"  ✓ {table_name}.csv: {rows:,} rows, {cols_count} columns, {size_mb:.2f} MB")

        return {
            'table': table_name,
            'filename': f"{table_name}.csv",
            'rows': rows,
            'columns': cols_count,
            'size_mb': size_mb,
            'description': config['description']
        }

    except Exception as e:
        logging.error(f"  ✗ Failed to export {table_name}: {e}")
        raise

def get_dataset_statistics(engine):
    """Get comprehensive dataset statistics for README.

    Non-dev: These headline numbers go into README for quick understanding.
    Dev: Single round-trip with scalar subqueries; cheap even on large datasets.
    """
    with engine.connect() as conn:
        stats_query = text("""
            SELECT 
                (SELECT COUNT(*) FROM public.applications) AS total_apps,
                (SELECT COUNT(*) FROM public.applications WHERE type = 'game') AS total_games,
                (SELECT COUNT(*) FROM public.applications WHERE is_free = TRUE) AS free_apps,
                (SELECT COUNT(*) FROM public.reviews) AS total_reviews,
                (SELECT COUNT(DISTINCT appid) FROM public.reviews) AS games_with_reviews,
                (SELECT COUNT(*) FROM public.genres) AS total_genres,
                (SELECT COUNT(*) FROM public.categories) AS total_categories,
                (SELECT COUNT(*) FROM public.developers) AS total_developers,
                (SELECT COUNT(*) FROM public.publishers) AS total_publishers,
                (SELECT MIN(release_date) FROM public.applications WHERE release_date IS NOT NULL) AS earliest_release,
                (SELECT MAX(release_date) FROM public.applications WHERE release_date IS NOT NULL) AS latest_release,
                (SELECT COUNT(*) FROM public.applications WHERE mat_supports_windows = TRUE) AS windows_support,
                (SELECT COUNT(*) FROM public.applications WHERE mat_supports_mac = TRUE) AS mac_support,
                (SELECT COUNT(*) FROM public.applications WHERE mat_supports_linux = TRUE) AS linux_support,
                (SELECT COUNT(DISTINCT mat_currency) FROM public.applications WHERE mat_currency IS NOT NULL) AS currencies
        """)
        result = pd.read_sql_query(stats_query, conn)
    return result.iloc[0].to_dict()

def create_readme(output_dir, export_stats, dataset_stats):
    """Create comprehensive README for CSV package.

    Non-dev: Explains contents, stats, and examples for Python/R.
    Dev: Aggregates table metrics; emits a stable, versionable README.md.
    """
    total_rows = sum(s['rows'] for s in export_stats)
    total_size = sum(s['size_mb'] for s in export_stats)
    generated = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    readme_content = f"""# Steam Dataset 2025 - CSV Package

**Generated:** {generated}  
**Package Type:** Accessibility Package (CSV Format)  
**Target Users:** Students, Data Analysts, Kaggle Beginners  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

## Overview

This package contains the Steam Dataset 2025 in CSV format for easy use with standard data analysis tools like Excel, Pandas, R, and Tableau. **No database setup required.**

### Dataset Statistics

- **Applications:** {dataset_stats['total_apps']:,} total ({dataset_stats['total_games']:,} games, {dataset_stats['free_apps']:,} free)
- **Reviews:** {dataset_stats['total_reviews']:,} reviews covering {dataset_stats['games_with_reviews']:,} games
- **Time Range:** {dataset_stats['earliest_release']} to {dataset_stats['latest_release']}
- **Platform Support:** {dataset_stats['windows_support']:,} Windows, {dataset_stats['mac_support']:,} Mac, {dataset_stats['linux_support']:,} Linux
- **Developers:** {dataset_stats['total_developers']:,} unique developers
- **Publishers:** {dataset_stats['total_publishers']:,} unique publishers
- **Genres:** {dataset_stats['total_genres']} standard genres
- **Categories:** {dataset_stats['total_categories']} Steam categories
- **Currencies:** {dataset_stats['currencies']} different currencies in pricing data

### Package Contents

**Total Size:** {total_size:.1f} MB (CSV aggregate)  
**Total Rows:** {total_rows:,} across all tables  
**Total Files:** {len(export_stats)} CSV files

---

## What's Included

All tables are exported with UTF-8 encoding and include headers.

"""

    # Core tables
    readme_content += "### Core Tables\n\n"
    for stat in export_stats:
        if stat['table'] in ['applications', 'reviews']:
            readme_content += f"**{stat['filename']}**\n"
            readme_content += f"- Description: {stat['description']}\n"
            readme_content += f"- Rows: {stat['rows']:,}\n"
            readme_content += f"- Columns: {stat['columns']}\n"
            readme_content += f"- Size: {stat['size_mb']:.2f} MB\n\n"

    # Reference tables
    readme_content += "### Reference Tables\n\n"
    for stat in export_stats:
        if stat['table'] in ['genres', 'categories', 'developers', 'publishers', 'platforms']:
            readme_content += f"**{stat['filename']}** - {stat['description']} ({stat['rows']:,} rows)\n"

    # Junction tables
    readme_content += "\n### Relationship Tables (Many-to-Many Mappings)\n\n"
    for stat in export_stats:
        if stat['table'].startswith('application_'):
            readme_content += f"**{stat['filename']}** - {stat['description']} ({stat['rows']:,} rows)\n"

    readme_content += """

---

## Quick Start Guide

### Python (Pandas)

python
import pandas as pd

# Load applications data
apps = pd.read_csv('applications.csv')

# Example: Find top-rated free games with Windows support
free_windows = apps[
    (apps['is_free'] == True) & 
    (apps['mat_supports_windows'] == True) &
    (apps['metacritic_score'] >= 80)
].sort_values('metacritic_score', ascending=False)

print(free_windows[['name', 'metacritic_score']].head(10))
`

### R

r
library(tidyverse)

# Load applications
apps <- read_csv('applications.csv')

# Example: Price distribution by genre
genres <- read_csv('genres.csv')
app_genres <- read_csv('application_genres.csv')

# Join and analyze
price_by_genre <- apps %>%
  inner_join(app_genres, by = 'appid') %>%
  inner_join(genres, by = c('genre_id' = 'id')) %>%
  filter(!is_free, mat_initial_price > 0) %>%
  group_by(name.y) %>%
  summarise(avg_price = mean(mat_initial_price / 100, na.rm = TRUE))


### Excel / Google Sheets

1. Import `applications.csv` as a new spreadsheet
2. Use filters and pivot tables for analysis
3. Note: Large files (reviews.csv) may exceed Excel's row limits

---

## Important Notes

### Materialized Columns

Included for easy analysis:

**Platform Support:**

* `mat_supports_windows`, `mat_supports_mac`, `mat_supports_linux` (BOOLEAN)

**Pricing Data:**

* `mat_initial_price`, `mat_final_price` (INTEGER in cents — divide by 100 for dollars)
* `mat_discount_percent` (INTEGER 0–100)
* `mat_currency` (TEXT — ISO 4217 codes like USD, EUR, GBP)

**Achievements:**

* `mat_achievement_count` (INTEGER — total achievements available)

**PC Requirements:**

* `mat_pc_os_min`, `mat_pc_processor_min`, `mat_pc_memory_min`, `mat_pc_graphics_min`
* `mat_pc_os_rec`, `mat_pc_processor_rec`, `mat_pc_memory_rec`, `mat_pc_graphics_rec`

### What's NOT Included

**JSONB Columns:**

* `pc_requirements`, `mac_requirements`, `linux_requirements`
* `price_overview`, `achievements`, `screenshots`, `movies`, `ratings`, `package_groups`, `content_descriptors`

**Vector Embeddings:**

* `description_embedding` (applications)
* `review_embedding` (reviews)

**Large HTML Fields:**

* `detailed_description`, `about_the_game`

For complete data including JSONB and vectors, use the **Power-User SQL Dump Package**.

---

## Known Limitations

1. Requirements parsing originates from text fields and may include noise.
2. Some fields may be NULL where the Steam API returned incomplete data.
3. Pricing currency distribution is skewed toward USD due to API origin.
4. Review languages are mixed; English dominates.

---

## Citation

When using this dataset, please cite:


VintageDon. (2025). The Steam Dataset 2025: A Large-Scale, API-Pure Dataset of the Steam Catalog. Zenodo. https://doi.org/[DOI]


---

## Support

* GitHub Issues: [https://github.com/vintagedon/steam-dataset-2025/issues](https://github.com/vintagedon/steam-dataset-2025/issues)
* Kaggle Discussions: Dataset discussion tab
* Email: [contact information]

---

**Package Version:** 2.1
**Data Collection:** August–September 2025
**Database Version:** PostgreSQL 16.10 with pgvector
**Methodology:** Standard ETL pipeline with validation checks
"""
readme_path = output_dir / 'README.md'
readme_path.write_text(readme_content, encoding='utf-8')
logging.info("  ✓ Created README.md")

def _sha256_file(path: Path) -> str:
"""Compute SHA256 hash for a file (streaming).


Non-dev: Ensures integrity; users can verify downloads.
Dev: Streams in 1MB chunks to keep memory usage bounded.
"""
h = hashlib.sha256()
with path.open('rb') as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b''):
        h.update(chunk)
return h.hexdigest()


def create_manifest(output_dir, export_stats):
"""Create MANIFEST.json with rows, columns, sizes, and SHA256 for each CSV.


Non-dev: Quick inventory for package consumers.
Dev: Rounds size to 2 decimals; includes UTC timestamp.
"""
manifest = {
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "files": []
}
for s in export_stats:
    fp = output_dir / s['filename']
    manifest["files"].append({
        "table": s['table'],
        "filename": s['filename'],
        "rows": s['rows'],
        "columns": s['columns'],
        "size_mb": round(s['size_mb'], 2),
        "sha256": _sha256_file(fp)
    })
path = output_dir / 'MANIFEST.json'
path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
logging.info("  ✓ Created MANIFEST.json")


def create_zip_archive(output_dir, zip_name):
"""Create compressed ZIP archive of all CSV and docs.


Non-dev: Bundles everything into a single download.
Dev: Uses DEFLATED with compresslevel=9; stable subfolder name inside ZIP.
"""
logging.info(f"Creating ZIP archive: {zip_name}")
zip_path = output_dir.parent / zip_name
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
    for file_path in sorted(output_dir.glob('*')):
        if file_path.is_file():
            arcname = f"steam_dataset_2025_csv/{file_path.name}"
            zipf.write(file_path, arcname=arcname)
            logging.info(f"  Added: {file_path.name}")
zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
logging.info(f"  ✓ ZIP created: {zip_size_mb:.2f} MB")
return zip_path


# -----------------------------------

# Main

# -----------------------------------

def main():
"""Orchestrates the CSV package generation.


Steps:
  1) Load env & connect to DB
  2) Gather dataset headline statistics
  3) Export each configured table (chunked where applicable)
  4) Emit README.md and MANIFEST.json
  5) ZIP the package for distribution
"""
logging.info("=" * 80)
logging.info("Steam Dataset 2025 - CSV Package Generator v2.1")
logging.info("=" * 80)

# Setup
setup_environment()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Connect to database
logging.info("Connecting to database...")
engine = create_connection()

try:
    # Get dataset statistics
    logging.info("Gathering dataset statistics...")
    dataset_stats = get_dataset_statistics(engine)

    # Export all tables
    logging.info("\nExporting tables to CSV...")
    export_stats = []
    for table_name, config in EXPORT_CONFIG.items():
        stats = export_table(engine, table_name, config, OUTPUT_DIR)
        export_stats.append(stats)

    # Create README + MANIFEST
    logging.info("\nGenerating package documentation...")
    create_readme(OUTPUT_DIR, export_stats, dataset_stats)
    create_manifest(OUTPUT_DIR, export_stats)

    # Create ZIP archive
    logging.info("\nCreating compressed archive...")
    zip_path = create_zip_archive(OUTPUT_DIR, ZIP_NAME)

    # Summary
    logging.info("\n" + "=" * 80)
    logging.info("CSV PACKAGE GENERATION COMPLETE")
    logging.info("=" * 80)

    total_rows = sum(s['rows'] for s in export_stats)
    total_size_mb = sum(s['size_mb'] for s in export_stats)

    logging.info(f"Tables Exported: {len(export_stats)}")
    logging.info(f"Total Rows: {total_rows:,}")
    logging.info(f"Total CSV Size: {total_size_mb:.2f} MB")
    logging.info(f"ZIP Archive: {zip_path.name} ({zip_path.stat().st_size / (1024*1024):.2f} MB)")
    logging.info(f"Output Location: {zip_path.absolute()}")
    logging.info("\n✓ Ready for Kaggle upload!")
    logging.info("\nDataset Highlights:")
    logging.info(f"  • {dataset_stats['total_apps']:,} applications ({dataset_stats['total_games']:,} games)")
    logging.info(f"  • {dataset_stats['total_reviews']:,} reviews")
    logging.info(f"  • {dataset_stats['total_developers']:,} developers, {dataset_stats['total_publishers']:,} publishers")
    logging.info(f"  • Materialized platform/pricing/requirements columns included")

finally:
    # Ensure connections are closed promptly
    engine.dispose()

if **name** == "**main**":
main()

