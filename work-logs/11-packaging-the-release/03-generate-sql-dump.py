#!/usr/bin/env python3
# Script: 03-generate-sql-dump.py
# Purpose: Create a Power Users SQL dump (pg_dump directory format) of the `steamfull` DB,
#          preserving full schema, data (JSONB), vector embeddings, and HNSW indexes.
# Author: VintageDon - https://github.com/vintagedon
# Date: 2025-09-29
# Version: 1.2

import os
import sys
import json
import hashlib
import logging
import subprocess
from datetime import datetime, timezone # Correctly import timezone
from pathlib import Path
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-m-%d %H:%M:%S'
)

ENV_PATH = Path('/mnt/data2/global-config/research.env')
OUTPUT_DIR = Path('./data-packages/power-users-sql-dump')

def load_env():
    if ENV_PATH.exists() and load_dotenv is not None:
        load_dotenv(ENV_PATH)
        logging.info(f"Loaded environment: {ENV_PATH}")
    elif not ENV_PATH.exists():
        logging.warning(f"Env file not found at {ENV_PATH}; relying on environment")
    for k in ["PGSQL01_DATASET_USER","PGSQL01_DATASET_PASSWORD","PGSQL01_HOST","PGSQL01_PORT"]:
        if not os.getenv(k):
            logging.error(f"Missing required env var: {k}")
            sys.exit(1)

def run_cmd(cmd: list, env=None):
    logging.info(" ".join(cmd))
    proc = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        logging.error(f"pg_dump failed with exit code {proc.returncode}:")
        logging.error(proc.stderr.strip())
        sys.exit(proc.returncode)
    else:
        if proc.stdout.strip():
            logging.info(proc.stdout.strip())
        # pg_dump often prints progress to stderr, so we log it on success too
        if proc.stderr.strip():
            logging.info(proc.stderr.strip())

def main():
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

    # FIX: Use timezone-aware datetime to resolve DeprecationWarning
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    dump_name = f"steam_dataset_2025_power_users_{ts}"
    dump_path = OUTPUT_DIR / dump_name # This will now be a directory

    env = os.environ.copy()
    env["PGPASSWORD"] = password

    # pg_dump flags:
    # -Fd: directory format (REQUIRED for parallel jobs)
    # -Z9: max compression for files within the directory
    # --no-owner/--no-privileges: portable
    # --quote-all-identifiers: stable diffs/reproducible DDL
    jobs = str(min(8, os.cpu_count() or 2))
    
    # --- CRITICAL FIX: Changed -Fc to -Fd ---
    cmd = [
        "pg_dump",
        "-h", host,
        "-p", str(port),
        "-U", user,
        "-d", dbname,
        "-Fd", # Use Directory format
        "-Z", "9",
        "--no-owner",
        "--no-privileges",
        "--quote-all-identifiers",
        "--jobs", jobs,
        "-f", str(dump_path) # This is now a directory path
    ]
    run_cmd(cmd, env=env)

    # Note: Checksum is removed as it's not straightforward for a directory
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
            "constraints, FKs",
            "all data (including JSONB)",
            "pgvector columns (vector(1024))",
            "HNSW indexes"
        ],
        "exclude": [
            "owners/privileges"
        ]
    }
    manifest_path = dump_path / "manifest.json" # Place manifest inside the dump directory
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    logging.info(f"✓ Dump complete: {dump_path.name}")
    logging.info(f"  Manifest: {manifest_path.name}")
    logging.info(f"  Output dir: {dump_path.resolve()}")

if __name__ == "__main__":
    main()
