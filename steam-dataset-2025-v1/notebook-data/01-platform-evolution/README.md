<!--
---
title: "Notebook Data Package - Platform Evolution Analysis"
description: "Curated CSV datasets optimized for Notebook 1: Steam Platform Evolution & Market Landscape analysis and visualization workflows"
author: "VintageDon - https://github.com/vintagedon"
ai_contributor: "Claude 3.5 Sonnet (claude-sonnet-4-20250514)"
date: "2025-10-05"
version: "1.0"
status: "Published"
tags:
- type: [data-package/csv-exports/visualization-data]
- domain: [platform-analysis/market-research/temporal-analysis]
- tech: [csv/pandas/data-visualization]
- phase: [phase-10-accessibility-packages]
related_documents:
- "[Notebook 1: Platform Evolution](../../notebooks/01-steam-platform-evolution-and-marketplace/README.md)"
- "[Data Dictionary](../../DATA_DICTIONARY.md)"
- "[Main Dataset README](../../README.md)"
---
-->

# 📊 **Platform Evolution Analysis - CSV Data Package**

This directory contains six curated CSV datasets optimized for the **Steam Platform Evolution & Market Landscape** notebook (Notebook 1). These files provide pre-aggregated, analysis-ready data covering temporal trends, genre evolution, platform support patterns, pricing strategies, publisher portfolios, and achievement adoption from 1997-2025.

## **Overview**

This data package represents the "Accessibility Tier" of the Steam Dataset 2025 publication strategy, providing immediate analytical capability without requiring PostgreSQL setup or complex data processing. Each CSV file corresponds to a specific analytical dimension explored in Notebook 1, enabling reproducible visualization and market analysis workflows.

---

## 📁 **Directory Contents**

### **Key Documents**

| **Document** | **Purpose** | **Link** |
|--------------|-------------|----------|
| **[README.md](README.md)** | This file - directory overview and usage guide | [README.md](README.md) |
| **[README-pending.md](README-pending.md)** | Placeholder for future notebook data packages | [README-pending.md](README-pending.md) |

### **CSV Datasets**

| **File** | **Rows** | **Purpose** | **Key Metrics** |
|----------|----------|-------------|-----------------|
| **[01_temporal_growth.csv](01_temporal_growth.csv)** | 29 | Annual and cumulative application releases | release_year, annual_releases, cumulative_total |
| **[02_genre_evolution.csv](02_genre_evolution.csv)** | 270 | Top 10 genres tracked yearly (2010-2025) | release_year, genre_description, game_count, avg_price |
| **[03_platform_support.csv](03_platform_support.csv)** | 8 | Platform configuration analysis | platform_config, game_count, avg_price, pct_games |
| **[04_pricing_strategy.csv](04_pricing_strategy.csv)** | 7 | Price tier distribution analysis | price_tier, game_count, pct_paid_games, avg_price, price_range |
| **[05_publisher_portfolios.csv](05_publisher_portfolios.csv)** | 30 | Top 30 publishers by game volume | publisher_name, total_items, game_count, dlc_count |
| **[06_achievement_evolution.csv](06_achievement_evolution.csv)** | 20 | Achievement system adoption trends | release_year, games_with_achievements, total_games, adoption_rate, avg_achievement_count |

---

## 🗂️ **Repository Structure**

```markdown
01-platform-evolution/
├── 📊 01_temporal_growth.csv              # 28-year release history (1997-2025)
├── 📊 02_genre_evolution.csv              # Genre trends by year (2010-2025)
├── 📊 03_platform_support.csv             # Platform configuration analysis
├── 📊 04_pricing_strategy.csv             # Price tier distributions
├── 📊 05_publisher_portfolios.csv         # Top publisher composition
├── 📊 06_achievement_evolution.csv        # Achievement adoption timeline
├── 📄 README.md                           # This file
└── 📄 README-pending.md                   # Future package placeholder
```

### **Navigation Guide:**

- **[📊 Temporal Growth](01_temporal_growth.csv)** - Use for annual release trend analysis and platform growth visualization
- **[📊 Genre Evolution](02_genre_evolution.csv)** - Use for genre popularity heatmaps and pricing analysis by genre/year
- **[📊 Platform Support](03_platform_support.csv)** - Use for platform market share and cross-platform pricing studies
- **[📊 Pricing Strategy](04_pricing_strategy.csv)** - Use for price tier distribution and monetization strategy analysis
- **[📊 Publisher Portfolios](05_publisher_portfolios.csv)** - Use for publisher content strategy and game/DLC ratio analysis
- **[📊 Achievement Evolution](06_achievement_evolution.csv)** - Use for feature adoption trends and engagement metric analysis

---

## 🔗 **Related Categories**

| **Category** | **Relationship** | **Documentation** |
|--------------|------------------|-------------------|
| **[Notebook 1: Platform Evolution](../../notebooks/01-steam-platform-evolution-and-marketplace/README.md)** | Primary consumer of these datasets - visualization and analysis notebook | [README.md](../../notebooks/01-steam-platform-evolution-and-marketplace/README.md) |
| **[Data Dictionary](../../DATA_DICTIONARY.md)** | Source schema documentation for these extracted datasets | [DATA_DICTIONARY.md](../../DATA_DICTIONARY.md) |
| **[PostgreSQL Database Schema](../../docs/postgresql-database-schema.md)** | Full relational database these CSVs are derived from | [postgresql-database-schema.md](../../docs/postgresql-database-schema.md) |
| **[Main Dataset](../../README.md)** | Parent dataset overview and complete documentation | [README.md](../../README.md) |

---

## **Getting Started**

For users approaching this data package:

1. **Start Here:** [01_temporal_growth.csv](01_temporal_growth.csv) - Simplest dataset for understanding Steam's growth trajectory
2. **Background Reading:** [Notebook 1: Platform Evolution](../../notebooks/01-steam-platform-evolution-and-marketplace/) - Complete analytical context and visualizations
3. **Implementation:** Load CSVs directly into Pandas, R, or Excel for immediate analysis
4. **Advanced Topics:** [Data Dictionary](../../DATA_DICTIONARY.md) for understanding source schema and materialized columns

---

## **Dataset Specifications**

### **Data Collection Period**

- **Raw Data Collection:** August-September 2025
- **Temporal Coverage:** 1997-2025 (28 years of platform history)
- **Aggregation Date:** September 29, 2025

### **Data Quality Notes**

- All datasets derived from validated PostgreSQL database (56% API success rate)
- Pricing data reflects USD values (59.5% of applications use USD in source data)
- Genre evolution filtered to top 10 genres for visualization clarity
- Publisher portfolios limited to top 30 by game volume to prevent overcrowding
- Achievement data only includes games released 2004+ (feature introduction year)

### **File Format Standards**

- **Encoding:** UTF-8 with BOM for Excel compatibility
- **Delimiter:** Comma (`,`)
- **Null Values:** Empty strings for missing text, blank cells for missing numbers
- **Date Format:** YYYY-MM-DD (ISO 8601) where applicable
- **Numeric Precision:** 2 decimal places for percentages, integers for counts

---

## **Usage Examples**

### **Loading in Python (Pandas)**

```python
import pandas as pd

# Load temporal growth data
temporal = pd.read_csv('01_temporal_growth.csv')
print(temporal.head())

# Quick validation check
print(f"Years covered: {temporal['release_year'].min()} to {temporal['release_year'].max()}")
print(f"Total applications released: {temporal['cumulative_total'].max():,}")
```

### **Loading in R**

```r
# Load platform support data
platform <- read.csv("03_platform_support.csv", stringsAsFactors = FALSE)

# Quick summary statistics
summary(platform$game_count)
sum(platform$game_count)  # Total games across all platform configs
```

### **Opening in Excel**

1. Open Excel
2. File → Open → Select CSV file
3. Use "Text Import Wizard" if needed
4. Ensure UTF-8 encoding for proper character display

---

## **Column Definitions**

### **01_temporal_growth.csv**

| Column | Type | Description |
|--------|------|-------------|
| `release_year` | INTEGER | Year of application release (1997-2025) |
| `annual_releases` | INTEGER | Number of applications released in that year |
| `cumulative_total` | INTEGER | Running total of all applications released through that year |

### **02_genre_evolution.csv**

| Column | Type | Description |
|--------|------|-------------|
| `release_year` | INTEGER | Year of release (2010-2025 for visualization clarity) |
| `genre_description` | TEXT | Genre name from Steam taxonomy (top 10 only) |
| `game_count` | INTEGER | Number of games in this genre/year combination |
| `avg_price` | NUMERIC | Average final price in USD for games in this genre/year |

### **03_platform_support.csv**

| Column | Type | Description |
|--------|------|-------------|
| `platform_config` | TEXT | Platform support configuration (e.g., "Windows only", "Win+Mac") |
| `game_count` | INTEGER | Number of games supporting this platform configuration |
| `avg_price` | NUMERIC | Average final price in USD for games with this configuration |
| `pct_games` | NUMERIC | Percentage of total games with this configuration |

### **04_pricing_strategy.csv**

| Column | Type | Description |
|--------|------|-------------|
| `price_tier` | TEXT | Price category (e.g., "Under $5", "$20-$30") |
| `game_count` | INTEGER | Number of paid games in this price tier |
| `pct_paid_games` | NUMERIC | Percentage of paid games in this tier |
| `avg_price` | NUMERIC | Average price within this tier in USD |
| `price_range` | TEXT | Human-readable price range description |

### **05_publisher_portfolios.csv**

| Column | Type | Description |
|--------|------|-------------|
| `publisher_name` | TEXT | Steam publisher name |
| `total_items` | INTEGER | Total applications published (games + DLC) |
| `game_count` | INTEGER | Number of base games published |
| `dlc_count` | INTEGER | Number of DLC packages published |

### **06_achievement_evolution.csv**

| Column | Type | Description |
|--------|------|-------------|
| `release_year` | INTEGER | Year of game release (2004-2025) |
| `games_with_achievements` | INTEGER | Number of games released with achievement system |
| `total_games` | INTEGER | Total games released in that year |
| `adoption_rate` | NUMERIC | Percentage of games with achievements (0-100) |
| `avg_achievement_count` | NUMERIC | Average number of achievements per game with achievement support |

---

## **Data Validation**

### **Expected Row Counts**

- **01_temporal_growth.csv:** 29 rows (1997-2025)
- **02_genre_evolution.csv:** ~270 rows (16 years × 10 genres, with gaps)
- **03_platform_support.csv:** 8 rows (all platform configurations)
- **04_pricing_strategy.csv:** 7 rows (price tier categories)
- **05_publisher_portfolios.csv:** 30 rows (top 30 publishers)
- **06_achievement_evolution.csv:** 20 rows (2004-2025, feature introduction to present)

### **Validation Queries**

**Temporal Growth Total Applications Check:**

```python
# Should match main dataset application count
assert temporal['cumulative_total'].max() == 239664, "Total applications mismatch"
```

**Genre Evolution Year Range:**

```python
# Should cover 2010-2025 for visualization clarity
assert genre['release_year'].min() == 2010
assert genre['release_year'].max() == 2025
```

**Platform Support Sum:**

```python
# All platform configs should sum to total games
total_games = platform['game_count'].sum()
print(f"Total games across platform configs: {total_games:,}")
```

---

## **Known Limitations**

### **Currency Bias**

- 59.5% of applications show USD pricing due to API query origin from United States
- Currency reflects geographic region of data collection, not game developer location
- For comparative pricing analysis, filter to single currency or apply exchange rate conversions

### **Genre Evolution Scope**

- Filtered to top 10 genres (2010-2025) for visualization readability
- Full genre data available in main PostgreSQL database (154 unique genres)
- Years before 2010 excluded to focus on modern platform period

### **Publisher Portfolio Threshold**

- Limited to top 30 publishers by total application count
- Represents ~45% of total content volume but misses long-tail publishers
- Full publisher relationships available in main database (85,699 unique publishers)

### **Free-to-Play Platform Support**

- Platform support percentages include free-to-play games
- Free games may have different cross-platform support patterns than paid titles
- Consider filtering by `is_free` in main dataset for paid-game-only analysis

---

## **Citation**

If you use these datasets in your research or analysis, please cite the complete Steam Dataset 2025:

**Fountain, D. (2025).** *The Steam Dataset 2025: A Large-Scale, Multi-Modal Dataset of the Steam Gaming Platform.* Zenodo. [https://doi.org/10.5281/zenodo.17266923](https://doi.org/10.5281/zenodo.17266923)

---

## **Document Information**

| **Field** | **Value** |
|-----------|-----------|
| **Author** | VintageDon - <https://github.com/vintagedon> |
| **Created** | 2025-10-05 |
| **Last Updated** | 2025-10-05 |
| **Version** | 1.0 |
| **Data Collection** | August-September 2025 |
| **Aggregation Date** | September 29, 2025 |

---
*Tags: csv-data, platform-evolution, temporal-analysis, market-research, visualization-data, notebook-data-package*

---

## 📋 **Category README Guidelines**

### **Purpose and Function**

This README serves dual purposes:

- **Human Navigation:** Provides clear, scannable directory organization for data analysts
- **Dataset Documentation:** Establishes data provenance, validation rules, and usage patterns

### **Content Principles**

- **Complete Coverage:** Every CSV file documented with purpose, row count, and key metrics
- **Practical Focus:** Usage examples in Python, R, and Excel for accessibility across skill levels
- **Validation Standards:** Clear expected row counts and validation queries for data integrity checks
- **Known Limitations:** Transparent documentation of data scope constraints and filtering decisions

### **Integration with Notebook 1**

This data package is specifically designed for **Notebook 1: Steam Platform Evolution & Market Landscape**:

- All CSV files directly referenced in notebook data loading cells
- Column names match exactly for seamless Pandas/R integration
- Row counts validated in notebook's data validation section
- Visualization choices (genre filtering, publisher limits) documented here for reproducibility
