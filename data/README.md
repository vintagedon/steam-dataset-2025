<!--
---
title: "Data"
description: "Raw and processed datasets for Steam Dataset 2025, containing 5,000+ games, 36,265+ user reviews, and enriched analytical datasets supporting multi-modal database implementation and machine learning applications"
author: "VintageDon - https://github.com/vintagedon"
ai_contributor: "Claude Sonnet 4"
date: "2025-09-03"
version: "1.0"
status: "Published"
tags:
- type: [directory-overview/dataset-catalog/data-assets]
- domain: [data-assets/steam-dataset/gaming-data/data-management]
- tech: [json-data/postgresql-import/dataset-management]
- phase: [phase-2/phase-3]
related_documents:
- "[Analytics Documentation](../docs/analytics/README.md)"
- "[Database Schema](../docs/postgresql-database-schema.md)"
- "[Scripts Implementation](../scripts/README.md)"
---
-->

# 📁 Data

This directory contains raw and processed datasets for Steam Dataset 2025, including comprehensive gaming application metadata, user reviews, and enriched analytical datasets. The data assets support multi-modal database implementation, machine learning applications, and advanced gaming market research with systematic quality assurance and validation.

## Overview

The data collection represents the first analytically-native Steam dataset, designed specifically for advanced data science applications rather than simple CSV exports. The datasets capture the complete Steam ecosystem including games, DLC, software, and user engagement data, with systematic API collection methodology ensuring high data quality and comprehensive coverage.

---

## 📁 Directory Contents

This section provides systematic navigation to all data assets and their processing stages.

### Data Processing Stages

| Stage | Purpose | Documentation |
|-----------|-------------|-------------------|
| [01_raw/](01_raw/) | Original Steam API responses and unprocessed data collection | Raw JSON datasets from Steam Web API |
| [02_processed/](02_processed/) | Enriched and validated datasets ready for database import | Quality-assured datasets with enhanced metadata |

### Dataset Catalog

| Dataset | Stage | Content | Records | Link |
|-------------|-----------|-------------|-------------|----------|
| steam_2025_5k-dataset-games_20250831.json | Raw | Complete game metadata from Steam API | 5,000+ games | [01_raw/steam_2025_5k-dataset-games_20250831.json](01_raw/steam_2025_5k-dataset-games_20250831.json) |
| steam_2025_5k-dataset-reviews_20250901.json | Raw | User review data with engagement metrics | 36,265+ reviews | [01_raw/steam_2025_5k-dataset-reviews_20250901.json](01_raw/steam_2025_5k-dataset-reviews_20250901.json) |
| steam_2025_5k-dataset-enchriched_20250901.json | Processed | Validated and enriched combined dataset | Combined | [02_processed/steam_2025_5k-dataset-enchriched_20250901.json.json](02_processed/steam_2025_5k-dataset-enchriched_20250901.json.json) |

---

## 🗂️ Repository Structure

``` markdown
data/
├── 📥 01_raw/                              # Original Steam API responses
│   ├── steam_2025_5k-dataset-games_20250831.json      # Raw game metadata collection
│   └── steam_2025_5k-dataset-reviews_20250901.json    # Raw user review collection
├── ⚙️ 02_processed/                        # Enriched and validated datasets
│   └── steam_2025_5k-dataset-enchriched_20250901.json.json # Quality-assured combined dataset
└── 📖 README.md                           # This file
```

### Navigation Guide

- [📥 Raw Data](01_raw/) - Original Steam API responses and unprocessed collections
- [⚙️ Processed Data](02_processed/) - Enriched datasets with quality assurance and validation

---

## 🔗 Related Categories

This section establishes horizontal relationships within the project knowledge graph, connecting data assets to implementation and analysis.

| Category | Relationship | Documentation |
|--------------|------------------|-------------------|
| [Scripts Implementation](../scripts/README.md) | Scripts generate, validate, and process all dataset assets | [../scripts/README.md](../scripts/README.md) |
| [Analytics Documentation](../docs/analytics/README.md) | Statistical analysis and insights derived from dataset assets | [../docs/analytics/README.md](../docs/analytics/README.md) |
| [Database Schema](../docs/postgresql-database-schema.md) | Database implementation targets and processes dataset assets | [../docs/postgresql-database-schema.md](../docs/postgresql-database-schema.md) |
| [Notebooks](../notebooks/README.md) | Interactive analysis and machine learning applications using datasets | [../notebooks/README.md](../notebooks/README.md) |

---

## Getting Started

For researchers and data scientists accessing Steam Dataset 2025 data assets:

1. Raw Data Exploration: Begin with [raw datasets](01_raw/) to understand original Steam API structures
2. Processed Data Analysis: Use [enriched datasets](02_processed/) for analysis and machine learning applications  
3. Database Implementation: Import datasets using [database scripts](../scripts/04-postgres_schema_design/README.md)
4. Analytical Applications: Apply datasets in [interactive notebooks](../notebooks/README.md) for advanced analysis
5. Quality Assessment: Review [analytics documentation](../docs/analytics/README.md) for data quality metrics and validation

---

## Dataset Characteristics

The Steam Dataset 2025 collection provides comprehensive gaming market representation:

Content Coverage:

- Applications: 8,711 total applications including games, DLC, software, and media
- Primary Games: 5,000 complete game entries with full metadata
- User Reviews: 36,265+ individual user reviews with sentiment and engagement data
- Developer Ecosystem: 6,740 unique developers and 5,605 publishers
- Genre Taxonomy: Comprehensive multi-label genre classification system

Data Quality Metrics:

- API Success Rate: 88.1% successful Steam API responses
- Field Coverage: 260+ unique data fields discovered and mapped
- Temporal Span: Current market snapshot with historical context
- Geographic Scope: Global Steam catalog with regional pricing variations
- Content Diversity: Traditional games plus utility software, creative tools, and media

Technical Specifications:

- Data Format: JSON with nested structures preserving API response fidelity
- Size Metrics: Raw datasets ~240MB, processed datasets ~135MB
- Character Encoding: UTF-8 supporting international content and Unicode
- Validation Status: Systematic integrity checks and quality assurance
- Processing Pipeline: RAVGV methodology ensuring systematic validation

---

## Data Usage Guidelines

Access and Attribution:

- License: MIT License enabling broad research and commercial usage
- Citation: Appropriate attribution required for academic and commercial applications
- Data Privacy: All data sourced from public Steam Web API endpoints
- Ethical Use: Responsible usage supporting gaming research and industry analysis

Technical Considerations:

- File Handling: Large JSON files requiring appropriate memory management
- Database Import: Optimized for PostgreSQL with JSONB and vector support
- Performance: Raw datasets suitable for exploration, processed datasets for production
- Validation: Cross-reference with provided quality metrics and validation reports

Research Applications:

- Gaming Market Analysis: Industry trends, pricing strategies, content evolution
- Machine Learning: Game success prediction, recommendation systems, sentiment analysis
- Academic Research: Digital markets, user behavior, platform economics
- Product Development: Competitive intelligence, market positioning, feature analysis

---

## Document Information

| Field | Value |
|-----------|-----------|
| Author | VintageDon - <https://github.com/vintagedon> |
| Created | 2025-09-03 |
| Last Updated | 2025-09-03 |
| Version | 1.0 |

---
*Tags: data-assets, steam-dataset, gaming-data, json-datasets, research-data*
