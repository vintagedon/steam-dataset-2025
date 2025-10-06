#!/usr/bin/env python3
# =================================================================================================
# File:          03-generate-sql-dump.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# AI Collaborators: ChatGPT, Gemini
# License:       MIT
# Last Updated:  2025-10-06
#
# Executive Summary (non-developer audience)
#   Creates the **Power-User SQL Dump Package** for Steam Dataset 2025.
#   - Captures the full database (schema + data) including JSONB and pgvector columns.
#   - Uses PostgreSQL’s directory format for parallelism and reproducibility.
#   - Produces a self-contained artifact suitable for local restoration via `pg_restore`.
#
# Developer Notes (technical audience)
#   • Env: reads Postgres creds from /mnt/data2/global-config/research.env
#   • Format: pg_dump directory mode (-Fd) for parallel jobs, compression Z9
#   • Includes: schema, constraints, JSONB, pgvector data, HNSW indexes
#   • Excludes: ownership/privileges for portability
#   • Manifest: manifest.json embedded alongside dump chunks for metadata
#   • COMMENTING ONLY — no logic changes
# =================================================================================================

import os
import sys
import json
import hashlib
import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# -------------------------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------------------------
ENV_PATH = Path('/mnt/data2/global-config/research.env')
OUTPUT_DIR = Path('./data-packages/power-users-sql-dump')


def load_env():
    """
    Loads environment variables from the standardized env file.

    Non-dev: Provides DB connection credentials required by pg_dump.
    Dev: Ensures all critical variables (PGSQL01_*) exist before proceeding.
    """
    if ENV_PATH.exists() and load_dotenv is not None:
        load_dotenv(ENV_PATH)
        logging.info(f"Loaded environment: {ENV_PATH}")
    elif not ENV_PATH.exists():
        logging.warning(f"Env file not found at {ENV_PATH}; relying on environment")

    for k in ["PGSQL01_DATASET_USER", "PGSQL01_DATASET_PASSWORD", "PGSQL01_HOST", "PGSQL01_PORT"]:
        if not os.getenv(k):
            logging.error(f"Missing required env var: {k}")
            sys.exit(1)


def run_cmd(cmd: list, env=None):
    """
    Executes a shell command (e.g., pg_dump) with subprocess.run and logs output.

    Non-dev: Provides progress and errors in human-readable form.
    Dev: Captures both stdout/stderr; exits non-zero on pg_dump failure.
    """
    logging.info(" ".join(cmd))
    proc = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        logging.error(f"pg_dump failed with exit code {proc.returncode}:")
        logging.error(proc.stderr.strip())
        sys.exit(proc.returncode)
    else:
        if proc.stdout.strip():
            logging.info(proc.stdout.strip())
        if proc.stderr.strip():
            # pg_dump writes progress messages to stderr even on success
            logging.info(proc.stderr.strip())


def main():
    """
    Orchestrates the full SQL dump generation.

    Non-dev:
      - Produces a directory-based pg_dump suitable for re-import via `pg_restore -Fd`.
      - Outputs a manifest.json with metadata and inclusion/exclusion info.

    Dev:
      - Uses parallel jobs (min(8, os.cpu_count())).
      - Z9 compression; directory format for stability and partial restores.
      - Manifest includes pgvector + HNSW index inclusion metadata.
    """
    logging.info("=" * 80)
    logging.info("Steam Dataset 2025 - Power Users SQL Dump")
    logging.info("=" * 80)

    load_env()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    host = os.getenv("PGSQL01_HOST")
    port = os.getenv("PGSQL01_PORT")
    user = os.getenv("PGSQL01_ADMIN_USER")
    password = os.getenv("PGSQL01_ADMIN_PASSWORD")
    dbname = "steamfull"

    # Timestamped artifact naming
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    dump_name = f"steam_dataset_2025_power_users_{ts}"
    dump_path = OUTPUT_DIR / dump_name  # Directory target for pg_dump -Fd

    # Propagate credentials for pg_dump
    env = os.environ.copy()
    env["PGPASSWORD"] = password

    # -------------------------------------------------------------------------------------------------
    # Build pg_dump command
    # -------------------------------------------------------------------------------------------------
    # Non-dev: Generates a compressed, portable directory with all data included.
    # Dev: -Fd = directory format for parallelism; -Z9 = max compression; --jobs set adaptively.
    jobs = str(min(8, os.cpu_count() or 2))

    cmd = [
        "pg_dump",
        "-h", host,
        "-p", str(port),
        "-U", user,
        "-d", dbname,
        "-Fd",              # Directory format
        "-Z", "9",          # Maximum compression
        "--no-owner",       # Portable between hosts
        "--no-privileges",  # Strip grant info
        "--quote-all-identifiers",
        "--jobs", jobs,     # Parallelism
        "-f", str(dump_path)
    ]

    run_cmd(cmd, env=env)

    # -------------------------------------------------------------------------------------------------
    # Write manifest metadata for this dump
    # -------------------------------------------------------------------------------------------------
    # Non-dev: Manifest ensures reproducibility and transparency.
    # Dev: Includes dump metadata, env host/port, format description, and dataset inclusions.
    manifest = {
        "artifact_directory": dump_name,
        "database": dbname,
        "format": "pg_dump directory (-Fd)",
        "compression": "Z9",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "host": host,
        "port": port,
        "include": [
            "full schema",
            "constraints and foreign keys",
            "all data including JSONB columns",
            "pgvector columns (vector[1024])",
            "HNSW indexes for vector similarity search"
        ],
        "exclude": [
            "ownership metadata",
            "privilege grants"
        ]
    }

    manifest_path = dump_path / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    logging.info(f"✓ Dump complete: {dump_path.name}")
    logging.info(f"  Manifest: {manifest_path.name}")
    logging.info(f"  Output dir: {dump_path.resolve()}")


if __name__ == "__main__":
    main()
