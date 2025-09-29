# =================================================================================================
# Script:        test-steam-api.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       1.2.1
# Created:       2025-08-31
# Last Updated:  2025-09-28
#
# Purpose:
#   Establish reliable, sustainable access patterns to Steam's public endpoints:
#   - ISteamApps/GetAppList (catalog size / reachability)
#   - store.steampowered.com/appdetails (per-app data contract)
#   - Empirical, reproducible rate-limit baseline for long-running collectors
#
# Inputs:
#   - ENV: STEAM_API_KEY (required), LOG_LEVEL (optional), API_DELAY_SECONDS (optional), API_USER_AGENT (optional)
# Outputs:
#   - STDOUT logs (timestamped) documenting request outcomes and effective throughput
#
# Operational Profile:
#   - Runtime Context: {os: linux|win|mac, python: 3.9+}
#   - Idempotency: {safe_rerun: true}  # read-only probes; no side effects
#   - Failure Modes: {network_error, json_decode_error, http_4xx_5xx}
#
# Data Lineage & Provenance (RAG-friendly):
#   SOURCE_OF_TRUTH: ["https://api.steampowered.com/ISteamApps/GetAppList/v2/",
#                     "https://store.steampowered.com/api/appdetails?appids=<id>"]
#   READS: ["applist.apps[*]", "appdetails.<appid>"]
#   WRITES: []
#   BUSINESS_RULES: ["Respect delay between calls to avoid throttling"]
#
# Security & Compliance:
#   - No secrets in code or logs. API key read from environment only.
#   - No PII handled; responses are public catalog/metadata.
#
# Usage:
#   python test-steam-api.py full
#   python test-steam-api.py applist
#   python test-steam-api.py details 730
#
# Change Log:
#   - 2025-08-31 v1.0.0 Initial release.
#   - 2025-08-31 v1.2.0 argparse/logging/env externalization; added inline docs.
#   - 2025-09-28 v1.2.1 Dual-audience comments, .env knobs, safer defaults.
# =================================================================================================

import os
import time
import sys
import logging
import argparse
import requests
from typing import Optional, List, Dict, Any
from json.decoder import JSONDecodeError
from dotenv import load_dotenv

# --- Configuration bootstrap ---------------------------------------------------------------------
# Rationale: centralize env loading + log shaping so downstream code stays pure “business logic”.
load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
if not STEAM_API_KEY:
    logging.error("FATAL: STEAM_API_KEY not set. Copy .env.example to .env and configure your key.")
    sys.exit(1)

# Tuning knobs: sourced from .env with safe fallbacks.
BASE_DELAY_SECONDS = float(os.getenv("API_DELAY_SECONDS", "1.5"))
API_USER_AGENT = os.getenv(
    "API_USER_AGENT",
    "SteamDataPlatform/1.1 (https://github.com/vintagedon/steam-dataset-2025)"
)

# --- Core Tester ----------------------------------------------------------------------------------
class SteamAPITester:
    """
    Encapsulated probe suite for Steam endpoints.

    Design notes (ML-friendly):
      - SINGLE_RESPONSIBILITY: each method tests one endpoint/behavior
      - OBSERVABILITY: structured INFO logs; explicit error paths
      - REPRODUCIBILITY: env-driven delay + UA; deterministic appid sample in rate test
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

        # WHY: requests.Session() reuses TCP connections and amortizes TLS setup, which we need for
        # multi-call patterns and for getting “realistic” performance signals before Phase 2–3 scaling.
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': API_USER_AGENT})

    # --- Endpoint: GetAppList ---------------------------------------------------------------------
    def test_app_list(self) -> Optional[List[Dict[str, Any]]]:
        """
        Validates catalog enumeration and basic JSON contract.

        Returns:
          List of {appid, name} dicts or None on failure.
        """
        logging.info("Probing ISteamApps/GetAppList (catalog size/health)...")
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            apps = data.get('applist', {}).get('apps', [])
            logging.info(f"✅ GetAppList OK — {len(apps):,} applications discovered.")
            # Human-friendly peek (bounded) to confirm payload structure without log spam.
            for app in apps[:5]:
                logging.info("   sample: %-8s  %s", app.get('appid'), app.get('name'))
            return apps

        except requests.exceptions.RequestException as e:
            logging.error("❌ GetAppList network/HTTP error: %s", e)
        except JSONDecodeError:
            logging.error("❌ GetAppList invalid JSON (service transient or HTML error page).")
        return None

    # --- Endpoint: appdetails ---------------------------------------------------------------------
    def test_app_details(self, appid: int) -> Optional[Dict[str, Any]]:
        """
        Fetches and validates the appdetails contract for a single app.

        Why:
          appdetails is the backbone for Phase 2+ enrichment and must be consistent at scale.
        """
        logging.info("Probing appdetails for appid=%s ...", appid)
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"

        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            node = data.get(str(appid), {})
            if node.get('success'):
                name = node.get('data', {}).get('name', 'Unknown')
                logging.info("✅ appdetails OK — %s", name)
                return node
            else:
                # Not all appids resolve; result informs downstream collectors to skip/mark.
                logging.warning("⚠️ appdetails success=false (appid=%s). Possibly restricted/unreleased.", appid)
                return None

        except requests.exceptions.RequestException as e:
            logging.error("❌ appdetails network/HTTP error for %s: %s", appid, e)
        except JSONDecodeError:
            logging.error("❌ appdetails JSON decode failed for %s.", appid)
        return None

    # --- Behavior: empirical throttling -----------------------------------------------------------
    def test_rate_limiting(self, test_apps: List[Dict[str, Any]]) -> None:
        """
        Measures a sustainable request cadence by issuing N consecutive appdetails calls.

        Method:
          - Take the last N “newer” appids (IDs trend upward) to mimic realistic patterns.
          - Sleep BASE_DELAY_SECONDS between requests.
          - Report effective requests/minute.

        Output is a durable artifact you can cite in Phase-1 logs and Phase-3 collection tuning.
        """
        N = min(len(test_apps), 10)
        if N == 0:
            logging.warning("No apps available; skipping rate test.")
            return

        logging.info("Running rate-limit probe with %s consecutive appdetails requests...", N)
        start = time.time()
        ok = 0

        for i, app in enumerate(test_apps[-N:]):
            appid = app.get('appid')
            if not appid:
                continue
            logging.info("Request %d/%d  appid=%s", i + 1, N, appid)
            if self.test_app_details(appid):
                ok += 1
            # WHY: honor delay to avoid 429s and emulate production collector behavior.
            if i < N - 1:
                logging.info("Sleeping %.2fs to respect throttle...", BASE_DELAY_SECONDS)
                time.sleep(BASE_DELAY_SECONDS)

        elapsed = max(time.time() - start, 1e-6)
        rpm = ok / elapsed * 60.0
        logging.info("--- Rate Test Summary ------------------------------------------------")
        logging.info(" Successful: %d/%d", ok, N)
        logging.info(" Elapsed:    %.1fs", elapsed)
        logging.info(" Effective:  %.1f requests/min (delay=%.2fs)", rpm, BASE_DELAY_SECONDS)

    # --- Orchestrator -----------------------------------------------------------------------------
    def run_full_test(self) -> None:
        """
        End-to-end Phase-1 verification:
          1) list catalog
          2) fetch a known title
          3) measure a safe cadence
        """
        logging.info("🚀 Starting Steam API Test Suite")
        apps = self.test_app_list()
        if not apps:
            logging.critical("Cannot proceed without applist; aborting.")
            return

        # Known, stable flagship AppID for sanity check.
        csgo_appid = 730
        time.sleep(BASE_DELAY_SECONDS)
        self.test_app_details(csgo_appid)

        time.sleep(BASE_DELAY_SECONDS)
        self.test_rate_limiting(apps)
        logging.info("✅ Steam API Test Suite complete.")

# --- CLI ------------------------------------------------------------------------------------------
def main():
    # WHY argparse: explicit contract, self-documenting CLI, testable entrypoints.
    parser = argparse.ArgumentParser(
        description="Phase-1 Steam API probe suite (catalog, details, cadence).",
        epilog="If no command is specified, the 'full' test runs by default."
    )
    sub = parser.add_subparsers(dest='command', help='Commands')
    sub.add_parser('full', help='Run the full, end-to-end probe suite.')
    sub.add_parser('applist', help='Probe only ISteamApps/GetAppList.')
    p_details = sub.add_parser('details', help='Probe appdetails for a specific AppID.')
    p_details.add_argument('appid', type=int, help='Numeric AppID.')

    args = parser.parse_args()
    tester = SteamAPITester(STEAM_API_KEY)

    # NOTE: default to `full` if no subcommand provided (developer-friendly ergonomics).
    if args.command == "applist":
        tester.test_app_list()
    elif args.command == "details":
        tester.test_app_details(args.appid)
    else:
        tester.run_full_test()

if __name__ == "__main__":
    main()
