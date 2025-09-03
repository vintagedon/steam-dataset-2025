<!--
---
title: "Raw Data Collection"
description: "Original Steam API data collection results containing unprocessed games and reviews data from official Steam Web APIs"
author: "VintageDon - https://github.com/vintagedon"
date: "2025-09-03"
version: "1.0"
status: "Published"
tags:
- type: [directory-overview/raw-data/api-collection]
- domain: [data-collection/steam-api/json-data]
- tech: [steam-web-api/json/data-ingestion]
- phase: [phase-2]
related_documents:
- "[Data Overview](../README.md)"
- "[02_processed](../02_processed/README.md)"
- "[Collection Scripts](../../scripts/02-get_steam_data_sample/README.md)"
---
-->

# 📊 Raw Data Collection

Original Steam API data collection results containing unprocessed games and reviews data from official Steam Web APIs. This directory stores the direct output from Steam API collection scripts, preserving the original JSON structure and response format for validation, analysis, and processing pipeline development.

## Overview

The raw data directory contains the foundational datasets collected directly from Steam's official Web APIs without any transformation or enrichment. These files represent the authentic API responses and serve as the authoritative source for all downstream processing. The data maintains the original JSON structure, including all metadata, timestamps, and API response formatting, ensuring complete traceability from source to final analytical products.

This raw format enables validation of processing pipelines, supports multiple analysis approaches, and preserves the complete information context for advanced analytical applications that may require access to original API structures.

---

## 📁 Directory Contents

This section provides systematic access to all raw data files with detailed metadata and collection information.

### Raw Data Files

| File | Content Type | Collection Date | Records | Size |
|----------|------------------|-------------------|-------------|----------|
| [steam_2025_5k-dataset-games_20250831.json](steam_2025_5k-dataset-games_20250831.json) | Steam applications (games, DLC, software) | 2025-08-31 | ~5,000 | ~106 MB |
| [steam_2025_5k-dataset-reviews_20250901.json](steam_2025_5k-dataset-reviews_20250901.json) | User reviews and ratings | 2025-09-01 | ~36,000+ | Variable |

### Collection Methodology

The raw data collection follows systematic protocols established during Phase 2 development:

API Sources: All data collected exclusively from official Steam Web APIs

- `appdetails` API for application metadata
- `reviews` API for user review content
- `applist` API for application discovery

Rate Limiting: Conservative approach maintaining API compliance

- 1.5 second delays between requests
- ~17.3 requests per minute sustainable rate
- Exponential backoff for error handling

Data Integrity: Complete response preservation

- Full JSON responses stored without modification
- API timestamps and metadata preserved
- Success/failure status tracking maintained

---

## 🗂️ Repository Structure

Visual representation of the raw data directory organization:

```markdown
01_raw/
├── 🎮 steam_2025_5k-dataset-games_20250831.json      # Applications collection
├── 📝 steam_2025_5k-dataset-reviews_20250901.json    # Reviews collection  
├── 📋 README.md                                       # This file
└── 📄 [collection-metadata...]                       # Collection logs and metadata
```

### File Naming Convention

Raw data files follow a systematic naming pattern for clear identification:

- `steam_YYYY_[size]-dataset-[type]_YYYYMMDD.json`
- Size indicator (5k, 10k, full) for dataset scope identification
- Collection date for temporal tracking and version control
- Type specification (games, reviews, metadata) for content clarity

---

## 🔗 Related Categories

This section establishes data flow relationships within the project pipeline architecture.

| Category | Relationship | Documentation |
|--------------|------------------|-------------------|
| [Processed Data](../02_processed/README.md) | Downstream enrichment and transformation target | [../02_processed/README.md](../02_processed/README.md) |
| [Collection Scripts](../../scripts/02-get_steam_data_sample/README.md) | Source automation and collection methodology | [../../scripts/02-get_steam_data_sample/README.md](../../scripts/02-get_steam_data_sample/README.md) |
| [Data Overview](../README.md) | Parent data architecture and pipeline context | [../README.md](../README.md) |
| [Database Schema](../../scripts/04-postgres_schema_design/README.md) | Relational transformation and storage target | [../../scripts/04-postgres_schema_design/README.md](../../scripts/04-postgres_schema_design/README.md) |

---

## Data Structure Overview

### Applications Data Structure

The games dataset contains comprehensive application metadata with the following key components:

Core Metadata: Application ID, name, type classification, release information
Rich Content: HTML-formatted descriptions, developer/publisher information, pricing data
Media Assets: Screenshot URLs, trailer links, header images
Technical Specs: System requirements, platform support, controller compatibility
Business Data: Pricing history, package information, regional availability

### Reviews Data Structure

The reviews dataset provides detailed user feedback with comprehensive context:

Review Content: Full review text, recommendation status, helpfulness votes
Author Context: User playtime, games owned, review history
Temporal Data: Review timestamps, last update information, purchase context
Community Metrics: Helpfulness votes, comment counts, visibility status

### API Response Preservation

Raw data files maintain complete API response structure including:

- Success Indicators: API call success/failure status
- Response Metadata: Timestamps, API version information
- Error Context: Failure reasons and diagnostic information
- Rate Limiting: Request timing and throttling data

---

## Usage Guidelines

### Data Access Patterns

Validation and Quality Assurance: Use raw data for validating processing pipelines and ensuring transformation accuracy against original source data.

Schema Development: Reference original JSON structure when designing database schemas and transformation logic.

Research Applications: Access complete API context for academic research requiring full data provenance and original response formatting.

Backup and Recovery: Maintain raw data as authoritative backup for regenerating processed datasets with updated methodologies.

### Technical Considerations

File Size Management: Large JSON files require appropriate tooling for efficient processing. Consider streaming JSON parsers for memory-efficient access.

Encoding Standards: All files use UTF-8 encoding to support international content and special characters in game descriptions and reviews.

Parsing Requirements: JSON structure includes nested objects and arrays requiring recursive parsing for complete data extraction.

Version Control: Raw data files are immutable once collected. New collections create new files with updated timestamps rather than modifying existing data.

---

## Document Information

| Field | Value |
|-----------|-----------|
| Author | VintageDon - <https://github.com/vintagedon> |
| Created | 2025-09-03 |
| Last Updated | 2025-09-03 |
| Version | 1.0 |

---
*Tags: raw-data, steam-api, json-collection, data-ingestion, api-responses*
