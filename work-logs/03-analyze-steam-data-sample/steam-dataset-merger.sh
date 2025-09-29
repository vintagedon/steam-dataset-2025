#!/bin/bash
# =================================================================================================
# Script:        steam-dataset-merger.sh
# Project:       Steam Dataset 2025
# Repository:    https://github.com/vintagedon/steam-dataset-2025
# Author:        Don (vintagedon) | ORCID: 0009-0008-7695-4093
# License:       MIT
# Version:       1.0.0
# Created:       2025-09-01
# Last Updated:  2025-09-28
#
# Purpose:
#   Memory-efficient merger for per-batch JSON artifacts (games and reviews) into two master arrays
#   using jq. Designed for very large datasets with minimal RAM pressure.
#
# Inputs:
#   - GAME_DATA_DIR: dir with steam_data_batch_*.json
#   - REVIEWS_DIR:   dir with reviews_full_batch_*.json
# Outputs:
#   - OUTPUT_DIR/steam_games_master.json
#   - OUTPUT_DIR/steam_reviews_master.json
#
# Operational Profile:
#   - Runtime Context: bash + jq
#   - Idempotency: safe (re-runs overwrite master outputs)
#   - Failure Modes: missing jq, invalid JSON, no matching input files
#
# Security & Compliance:
#   - No secrets. Validates JSON prior to merge.
#
# Change Log:
#   - 2025-09-28  Standardized header + inline comments (no logic changes).
# =================================================================================================

# Steam Dataset 2025 - Master File Merger (Bash)
# Memory-efficient JSON merging using jq

set -e  # Exit on any error

# Configuration (HUMAN: adjust paths for your environment; use fast local storage for TEMP_DIR)
GAME_DATA_DIR="/mnt/data/steam-dataset-refresh/data_gamedata"
REVIEWS_DIR="/mnt/data/steam-dataset-refresh/data_reviews"
OUTPUT_DIR="/mnt/data2/steam-dataset-refresh"
TEMP_DIR="/mnt/data2/steam_merge_temp"

# Colors for output (cosmetic)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Steam Dataset 2025 - Master File Merger${NC}"
echo -e "${CYAN}=======================================${NC}"

# Dependency check (jq is required for streaming-safe merges)
command -v jq >/dev/null 2>&1 || { echo -e "${RED}Error: jq is required but not installed.${NC}" >&2; exit 1; }

# Workspace (idempotent)
mkdir -p "$OUTPUT_DIR"
mkdir -p "$TEMP_DIR"

# Cleanup handler to avoid leftover temp files
cleanup() {
    echo -e "\n${YELLOW}Cleaning up temporary files...${NC}"
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# merge_json_files: concatenates arrays in input batches without loading everything in memory
merge_json_files() {
    local input_dir="$1"
    local file_pattern="$2"
    local output_file="$3"
    local data_type="$4"
    
    echo -e "\n${GREEN}🔄 MERGING $data_type FILES${NC}"
    echo "=================================================="
    
    # Enumerate + sort for deterministic order
    local files=($(find "$input_dir" -name "$file_pattern" -type f | sort))
    local total_files=${#files[@]}
    
    if [ $total_files -eq 0 ]; then
        echo -e "${RED}Error: No files found matching pattern '$file_pattern' in '$input_dir'${NC}"
        return 1
    fi
    
    echo "Found $total_files files to merge"
    
    # Initialize output to empty JSON array
    echo "[]" > "$output_file"
    
    local processed=0
    local total_records=0
    
    for file in "${files[@]}"; do
        ((processed++))
        # Progress indicator on a cadence
        if [ $((processed % 25)) -eq 0 ] || [ $processed -eq $total_files ]; then
            local percent=$((processed * 100 / total_files))
            echo "  Processing file $processed/$total_files (${percent}%): $(basename "$file")"
        fi
        
        # Validate before merging to avoid corrupt output
        if ! jq empty "$file" 2>/dev/null; then
            echo -e "  ${YELLOW}Warning: Skipping invalid JSON file: $(basename "$file")${NC}"
            continue
        fi
        
        # Count records for telemetry (jq 'length' works for top-level arrays)
        local file_records=$(jq 'length' "$file" 2>/dev/null || echo "0")
        total_records=$((total_records + file_records))
        
        # Merge arrays in a temp file to reduce risk under I/O contention
        local temp_merge="$TEMP_DIR/temp_merge_$$.json"
        jq -s '.[0] + .[1]' "$output_file" "$file" > "$temp_merge"
        mv "$temp_merge" "$output_file"
        
        # Periodic sync checkpoint
        if [ $((processed % 50)) -eq 0 ]; then
            sync
            echo "    Memory checkpoint: $total_records records processed"
        fi
    done
    
    # Final stats (size + record count)
    local final_count=$(jq 'length' "$output_file" 2>/dev/null || echo "0")
    local file_size_mb=$(du -m "$output_file" | cut -f1)
    
    echo -e "\n${GREEN}✅ $data_type merge complete:${NC}"
    echo "  Files processed: $processed"
    echo "  Records merged: $final_count"
    echo "  Output size: ${file_size_mb}MB"
    
    return 0
}

# Validate master outputs to catch late-stage corruption
validate_output() {
    local file="$1"
    local data_type="$2"
    
    echo -n "  Validating $data_type master file... "
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ File not found${NC}"
        return 1
    fi
    
    if jq empty "$file" 2>/dev/null; then
        local count=$(jq 'length' "$file")
        echo -e "${GREEN}✅ Valid ($count records)${NC}"
        return 0
    else
        echo -e "${RED}❌ Invalid JSON${NC}"
        return 1
    fi
}

# Timing (telemetry for long merges)
start_time=$(date +%s)

# ======================
# MERGE GAME DATA FILES
# ======================
game_output="$OUTPUT_DIR/steam_games_master.json"
echo -e "\n${CYAN}Target output: $game_output${NC}"
if merge_json_files "$GAME_DATA_DIR" "steam_data_batch_*.json" "$game_output" "GAME DATA"; then
    echo -e "${GREEN}Game data merge successful${NC}"
else
    echo -e "${RED}Game data merge failed${NC}"
    exit 1
fi

# ======================
# MERGE REVIEW FILES
# ======================
reviews_output="$OUTPUT_DIR/steam_reviews_master.json"
echo -e "\n${CYAN}Target output: $reviews_output${NC}"
if merge_json_files "$REVIEWS_DIR" "reviews_full_batch_*.json" "$reviews_output" "REVIEWS"; then
    echo -e "${GREEN}Reviews merge successful${NC}"
else
    echo -e "${RED}Reviews merge failed${NC}"
    exit 1
fi

# ======================
# VALIDATION & SUMMARY
# ======================
echo -e "\n${GREEN}🔍 VALIDATING OUTPUT FILES${NC}"
echo "=================================================="
game_valid=false
reviews_valid=false
if validate_output "$game_output" "game data"; then game_valid=true; fi
if validate_output "$reviews_output" "reviews"; then reviews_valid=true; fi

end_time=$(date +%s)
duration=$((end_time - start_time))
minutes=$((duration / 60))
seconds=$((duration % 60))

game_records=$(jq 'length' "$game_output" 2>/dev/null || echo "0")
review_records=$(jq 'length' "$reviews_output" 2>/dev/null || echo "0")
total_records=$((game_records + review_records))

game_size_mb=$(du -m "$game_output" 2>/dev/null | cut -f1)
reviews_size_mb=$(du -m "$reviews_output" 2>/dev/null | cut -f1)

echo -e "\n${CYAN}============================================================${NC}"
echo -e "${CYAN}                    MERGE OPERATION COMPLETE${NC}"
echo -e "${CYAN}============================================================${NC}"
echo -e "\n${GREEN}📈 FINAL STATISTICS:${NC}"
echo "  Game data records: $(printf "%'d" $game_records)"
echo "  Review records: $(printf "%'d" $review_records)"
echo "  Total records merged: $(printf "%'d" $total_records)"
echo "  Processing time: ${minutes}m ${seconds}s"
echo -e "\n${GREEN}📁 OUTPUT FILES:${NC}"
if [ "$game_valid" = true ]; then
    echo -e "  ✅ $game_output (${game_size_mb}MB)"
else
    echo -e "  ❌ $game_output (validation failed)"
fi

if [ "$reviews_valid" = true ]; then
    echo -e "  ✅ $reviews_output (${reviews_size_mb}MB)"
else
    echo -e "  ❌ $reviews_output (validation failed)"
fi

if [ "$game_valid" = true ] && [ "$reviews_valid" = true ]; then
    echo -e "\n${GREEN}🎉 Master files created successfully!${NC}"
    echo -e "${GREEN}Ready for database import or further processing.${NC}"
    exit 0
else
    echo -e "\n${YELLOW}⚠️ Some operations failed. Check the output above for details.${NC}"
    exit 1
fi
