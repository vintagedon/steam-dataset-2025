#!/usr/bin/env python3
# =================================================================================================
# Script:        100-game-steam-api-test.py
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | GitHub: https://github.com/vintagedon | ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       1.0.0
# Created:       2025-08-31
# Last Updated:  2025-09-28
#
# Purpose:
#   Proof-of-concept sampler that pulls a small set of Steam apps, validates appdetails,
#   and (when a valid game) fetches a small batch of reviews. Useful for Phase-2/3 validation.
#
# Inputs:
#   - Hardcoded API key (NOTE: move to .env for production; see Security notes below)
# Outputs:
#   - JSON file: steam_data_sample.json (sample + basic metadata)
#
# Operational Profile:
#   - Runtime Context: {os: linux|win|mac, python: 3.9+}
#   - Idempotency: {safe_rerun: true}  # read-only against upstream; overwrites same output file
#   - Failure Modes: {network_error, json_decode_error, http_4xx_5xx, restricted_appids}
#
# Data Lineage & Provenance:
#   SOURCE_OF_TRUTH:
#     - https://api.steampowered.com/ISteamApps/GetAppList/v2/
#     - https://store.steampowered.com/api/appdetails?appids=<id>
#     - https://store.steampowered.com/appreviews/<id>?json=1
#   READS: ["applist.apps[*]", "appdetails.<appid>", "appreviews.<appid>"]
#   WRITES: ["steam_data_sample.json"]
#
# Security & Compliance:
#   - WARNING: API key is hardcoded for quick tests. Rotate and migrate to .env immediately.
#   - No PII processed; all content is public catalog/metadata/reviews.
#
# Usage:
#   python 100-game-steam-api-test.py
#
# Change Log:
#   - 2025-09-28 v1.0.0  Standardized header + dual-audience comments added (no code changes).
# =================================================================================================

"""
Simple Steam data pull - 100 games
Build off the proven test script, store to JSON file
"""

import requests
import json
import time
from datetime import datetime
import random

# Configuration
# HUMAN: For quick experiments. For long runs, externalize to .env and use requests.Session with backoff.
# ML:    CONFIG = {"BASE_DELAY": 1.5, "OUTPUT_FILE": "steam_data_sample.json", "TARGET_GAMES": 100}
STEAM_API_KEY = "--REPLACE_ME---"  # NOTE: move to .env; rotate this key.
BASE_DELAY = 1.5  # seconds between requests
OUTPUT_FILE = "steam_data_sample.json"
TARGET_GAMES = 100

class SteamDataPuller:
    # WHY: encapsulate networking + business logic for reuse and observability.
    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SteamDataPlatform/1.0 (craincraft.com)'
        })
        self.collected_data = []
        
    def log(self, message):
        # HUMAN: simple timestamped print for quick visibility in ad-hoc runs.
        # ML:    LOG_FORMAT = "[YYYY-MM-DD HH:MM:SS] message"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def get_app_list(self):
        """Get full app list from Steam (catalog reachability + size sanity)."""
        self.log("Fetching Steam app list...")
        
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            apps = data['applist']['apps']
            
            self.log(f"Retrieved {len(apps):,} applications")
            return apps
            
        except Exception as e:
            self.log(f"❌ Failed to get app list: {e}")
            return []
    
    def get_app_details(self, appid):
        """Get detailed info for a single app (primary contract for downstream ETL)."""
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            app_data = data.get(str(appid), {})
            if app_data.get('success'):
                return {
                    'appid': appid,
                    'success': True,
                    'data': app_data['data'],
                    'fetched_at': datetime.now().isoformat()
                }
            else:
                # HUMAN: not all appids resolve; record as unsuccessful but keep moving.
                return {
                    'appid': appid,
                    'success': False,
                    'data': None,
                    'fetched_at': datetime.now().isoformat()
                }
                
        except Exception as e:
            # HUMAN: network/transient errors recorded in-line with appid to support triage.
            return {
                'appid': appid,
                'success': False,
                'error': str(e),
                'fetched_at': datetime.now().isoformat()
            }
    
    def get_sample_reviews(self, appid, max_reviews=10):
        """Get sample reviews for an app (sanity-check the reviews endpoint/contract)."""
        url = f"https://store.steampowered.com/appreviews/{appid}?json=1&num_per_page={max_reviews}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get('success') == 1:
                return {
                    'success': True,
                    'query_summary': data['query_summary'],
                    'reviews': data.get('reviews', [])
                }
            else:
                return {'success': False}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def collect_game_data(self, appid, name):
        """Collects per-app bundle: appdetails (+reviews if it's a game)."""
        self.log(f"Processing {appid}: {name}")
        
        app_details = self.get_app_details(appid)
        
        game_record = {
            'appid': appid,
            'name': name,
            'app_details': app_details
        }
        
        # HUMAN: reviews fetched only for valid 'game' type; avoids wasted calls.
        if app_details['success'] and app_details['data'].get('type') == 'game':
            time.sleep(0.5)  # Small delay between API calls
            reviews = self.get_sample_reviews(appid)
            game_record['reviews'] = reviews
            
            # Useful telemetry for quick inspections
            game_data = app_details['data']
            price = game_data.get('price_overview', {}).get('final_formatted', 'Free')
            developers = ', '.join(game_data.get('developers', ['Unknown']))
            
            self.log(f"   ✅ Game: {game_data.get('name', 'Unknown')} | {price} | {developers}")
            
            if reviews['success']:
                review_count = reviews['query_summary']['total_reviews']
                self.log(f"   📝 Reviews: {review_count:,} total")
        else:
            self.log(f"   ⚠️  Not a game or failed: {app_details.get('success', False)}")
        
        return game_record
    
    def save_data(self):
        """Persist run to JSON (minimal lineage for reproducibility)."""
        output_data = {
            'metadata': {
                'collected_at': datetime.now().isoformat(),
                'total_records': len(self.collected_data),
                'successful_games': len([r for r in self.collected_data if r['app_details']['success']]),
                'api_key_used': self.api_key[:8] + "...",
                'delay_used': BASE_DELAY
            },
            'games': self.collected_data
        }
        
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        self.log(f"💾 Data saved to {OUTPUT_FILE}")
    
    def run_collection(self):
        """Main loop: sample candidates → collect appdetails (+reviews for games) → periodic save."""
        self.log(f"🚀 Starting data collection for {TARGET_GAMES} games")
        
        apps = self.get_app_list()
        if not apps:
            self.log("❌ Cannot proceed without app list")
            return
        
        # HUMAN: heuristics to bias toward actual games (skip early infra/tooling appids).
        candidate_apps = [app for app in apps if app['appid'] > 1000]
        
        self.log(f"Found {len(candidate_apps):,} candidate apps (appid > 1000)")
        
        # Random fan-out; we expect to discard non-games along the way.
        sample_apps = random.sample(candidate_apps, min(TARGET_GAMES * 3, len(candidate_apps)))
        
        self.log(f"Randomly sampling {len(sample_apps)} apps to find {TARGET_GAMES} games")
        
        collected_games = 0
        total_processed = 0
        
        for app in sample_apps:
            if collected_games >= TARGET_GAMES:
                break
                
            total_processed += 1
            
            game_record = self.collect_game_data(app['appid'], app['name'])
            self.collected_data.append(game_record)
            
            if (game_record['app_details']['success'] and 
                game_record['app_details']['data'].get('type') == 'game'):
                collected_games += 1
            
            if total_processed % 10 == 0:
                self.log(f"Progress: {collected_games}/{TARGET_GAMES} games collected, {total_processed} total processed")
            
            if total_processed % 25 == 0:
                self.save_data()
                self.log("💾 Periodic save completed")
            
            time.sleep(BASE_DELAY)
        
        self.save_data()
        
        self.log(f"🎉 Collection complete!")
        self.log(f"   Games collected: {collected_games}")
        self.log(f"   Total records: {len(self.collected_data)}")
        self.log(f"   Output file: {OUTPUT_FILE}")

if __name__ == "__main__":
    puller = SteamDataPuller(STEAM_API_KEY)
    puller.run_collection()
