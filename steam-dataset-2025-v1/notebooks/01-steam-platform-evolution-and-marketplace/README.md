<!--
---
title: "Notebook 1: Platform Evolution & Market Landscape"
description: "Beginner-friendly analysis of Steam's 28-year evolution, examining temporal growth, genre dynamics, pricing strategies, and platform adoption patterns across 239,664 applications"
author: "VintageDon - https://github.com/vintagedon"
ai_contributor: "Claude 3.5 Sonnet (claude-sonnet-4-20250514)"
date: "2025-10-05"
version: "1.0"
status: "Published"
tags:
- type: [directory-overview/notebook-documentation]
- domain: [data-analysis/temporal-analysis/market-research]
- tech: [jupyter/python/pandas/matplotlib/seaborn]
- phase: [phase-10-publication]
related_documents:
- "[Notebook Development Tracker](../../notebook-development-tracker-updated.md)"
- "[Main Notebooks Directory](../README.md)"
- "[Data Dictionary](../../steam-dataset-2025-v1/DATA_DICTIONARY.md)"
---
-->

# 📊 **Notebook 1: Platform Evolution & Market Landscape**

This directory contains the first of three publication-ready Jupyter notebooks showcasing the Steam Dataset 2025. This beginner-friendly analysis explores Steam's transformation from a game launcher (1997) into the world's largest PC gaming marketplace (2025), examining 239,664 applications across 28 years of platform history.

## **Overview**

**Notebook 1: Platform Evolution & Market Landscape** demonstrates the dataset's temporal depth and materialized analytical columns through accessible exploratory data analysis. It targets data science students, Kaggle beginners, and researchers seeking to understand digital marketplace maturation patterns. The analysis reveals Steam's exponential growth trajectory, genre-based market segmentation, pricing polarization, and the adoption of platform features like achievements.

**Skill Level:** Beginner  
**Estimated Runtime:** 3-5 minutes  
**Primary Focus:** Temporal trends, market dynamics, pricing strategies  
**Dataset Features Showcased:** 28-year historical coverage, materialized columns (`mat_*` prefix), comprehensive metadata

---

## 📁 **Directory Contents**

### **Key Documents**

| **Document** | **Purpose** | **Link** |
|--------------|-------------|----------|
| **notebook-01-steam-platform-evolution-and-market-landscape.ipynb** | Interactive Jupyter notebook with 7 visualizations analyzing platform evolution | [notebook-01-steam-platform-evolution-and-market-landscape.ipynb](notebook-01-steam-platform-evolution-and-market-landscape.ipynb) |
| **notebook-01-steam-platform-evolution-and-market-landscape.pdf** | Static PDF export for quick reference without running code | [notebook-01-steam-platform-evolution-and-market-landscape.pdf](notebook-01-steam-platform-evolution-and-market-landscape.pdf) |
| **README.md** | This file - directory overview and navigation guide | [README.md](README.md) |

### **Data Files (Exported CSVs)**

The notebook requires 6 pre-exported CSV files containing aggregated data from the PostgreSQL database:

| **File** | **Contents** | **Size** | **Query Source** |
|----------|-------------|----------|------------------|
| **01_temporal_growth.csv** | Annual/cumulative release counts (1997-2025) | ~3 KB | Temporal aggregation query |
| **02_genre_evolution.csv** | Genre-year combinations with pricing/counts | ~450 KB | Genre temporal analysis |
| **03_platform_support.csv** | Platform configurations with game counts | ~800 bytes | Platform support matrix |
| **04_pricing_strategy.csv** | Price tier distributions with achievements | ~650 bytes | Pricing tier aggregation |
| **05_publisher_portfolios.csv** | Top 50 publishers with game/DLC breakdown | ~4 KB | Publisher portfolio query |
| **06_achievement_evolution.csv** | Achievement adoption over time | ~2 KB | Achievement temporal query |

**Note:** CSV files are distributed separately via Kaggle dataset: `steam-dataset-2025-notebook-data`

---

## 🗂️ **Repository Structure**

``` markdown
01-steam-platform-evolution-and-marketplace/
├── 📓 notebook-01-steam-platform-evolution-and-market-landscape.ipynb  # Main analysis notebook
├── 📄 notebook-01-steam-platform-evolution-and-market-landscape.pdf    # Static PDF export
├── 📋 README.md                                                        # This file
└── 📊 Data Files (6 CSVs - distributed via Kaggle):
    ├── 01_temporal_growth.csv
    ├── 02_genre_evolution.csv
    ├── 03_platform_support.csv
    ├── 04_pricing_strategy.csv
    ├── 05_publisher_portfolios.csv
    └── 06_achievement_evolution.csv
```

### **Navigation Guide:**

- **📓 [Main Notebook](notebook-01-steam-platform-evolution-and-market-landscape.ipynb)** - Interactive analysis with executable code cells
- **📄 [PDF Export](notebook-01-steam-platform-evolution-and-market-landscape.pdf)** - Quick reference for viewing results without Jupyter
- **📊 Data Files** - Available via Kaggle dataset `steam-dataset-2025-notebook-data/01-platform-evolution/`

---

## 📗 **Analysis Overview**

### **Research Questions Addressed**

1. **Temporal Growth:** How has Steam's content catalog evolved across 28 years? What inflection points mark major platform shifts?
2. **Genre Evolution:** Which genres drive platform growth? How have genre-specific pricing strategies changed over time?
3. **Platform Support:** What patterns emerge in Windows/Mac/Linux support? Does multi-platform correlate with pricing or genre?
4. **Pricing Strategy:** How do developers position products across price tiers? What role does free-to-play occupy?
5. **Publisher Portfolios:** How do top publishers balance portfolio diversification (games vs DLC) and pricing strategies?
6. **Achievement Adoption:** How has Steam's achievement system diffused across the platform?

### **Key Findings**

1. **Exponential Growth:** Steam releases increased 47× from 2010-2025, with 2023 marking peak velocity (14,753 apps)
2. **Genre Dynamics:** Indie and Action genres dominate releases; premium pricing concentrated in RPG/Strategy
3. **Platform Fragmentation:** 72% of games are Windows-exclusive; multi-platform support correlates with higher pricing
4. **Pricing Polarization:** 77.8% of paid games priced under $10, while premium titles ($50+) represent <1%
5. **Achievement Adoption:** Steam Achievements reached 65% adoption by 2025, with mid-tier games showing highest rates

### **Visualizations Included**

| Chart # | Type | Focus |
|---------|------|-------|
| 1 | Dual-axis line/bar | Temporal growth (annual releases + cumulative total) |
| 2 | Stacked area | Content type diversification (games, DLC, other) |
| 3 | Heatmap | Genre popularity evolution (2010-2025, top 10 genres) |
| 4 | Side-by-side bars | Platform support distribution + price correlation |
| 5 | Pie + bar | Pricing tier market share + achievement implementation |
| 6 | Stacked horizontal bars | Publisher portfolio composition (top 15) |
| 7 | Dual-axis line | Achievement system adoption timeline |

---

## 📗 **Related Categories**

| **Category** | **Relationship** | **Documentation** |
|--------------|------------------|-------------------|
| **[Notebooks Directory](../README.md)** | Parent directory containing all 3 publication notebooks | [../README.md](../README.md) |
| **[Notebook 2: Semantic Discovery](../02-semantic-game-discovery/README.md)** | Follows this notebook - intermediate level, showcases vector embeddings | [../02-semantic-game-discovery/README.md](../02-semantic-game-discovery/README.md) |
| **[Notebook 3: Sentiment Prediction](../03-review-sentiment-success-prediction/README.md)** | Advanced analysis building on insights from Notebooks 1 & 2 | [../03-review-sentiment-success-prediction/README.md](../03-review-sentiment-success-prediction/README.md) |
| **[Data Dictionary](../../steam-dataset-2025-v1/DATA_DICTIONARY.md)** | Complete schema reference for understanding data structures | [../../steam-dataset-2025-v1/DATA_DICTIONARY.md](../../steam-dataset-2025-v1/DATA_DICTIONARY.md) |
| **[Work Logs](../../work-logs/README.md)** | Development history showing how this notebook was created | [../../work-logs/README.md](../../work-logs/README.md) |

---

## **Getting Started**

For users new to this notebook:

1. **Start Here:** Open [notebook-01-steam-platform-evolution-and-market-landscape.ipynb](notebook-01-steam-platform-evolution-and-market-landscape.ipynb) in Jupyter or Kaggle
2. **Data Setup:**
   - **Kaggle users:** Add dataset `steam-dataset-2025-notebook-data` to your kernel
   - **Local users:** Download CSVs from Zenodo (<https://doi.org/10.5281/zenodo.17266923>) and extract to `notebook-data/01-platform-evolution/`
3. **Run Notebook:** Execute cells sequentially - environment detection auto-configures data paths
4. **Explore Results:** All visualizations and statistical summaries are included in markdown cells

### **Prerequisites**

- **Python:** 3.9+ recommended
- **Required Packages:** pandas, numpy, matplotlib, seaborn, pathlib
- **Optional:** Jupyter Notebook/Lab (can also run in Kaggle, Google Colab, VS Code)
- **Data Access:** CSV files from Kaggle dataset `steam-dataset-2025-notebook-data`

### **Quick Validation**

After loading data, the notebook includes a validation cell that checks:

- ✅ 29 years of temporal data (1997-2025)
- ✅ 7 pricing tiers (Free + 6 paid ranges)
- ✅ 100K+ applications analyzed
- ✅ Sub-$10 games comprise >70% of paid titles

---

## **Technical Implementation**

### **Data Source**

All CSV files are derived from SQL queries executed against the production PostgreSQL database (`steamfull` on proj-pgsql01). Queries aggregate data using materialized columns for performance:

- **Temporal queries:** Use `release_date` for year extraction
- **Platform queries:** Use `mat_supports_windows/mac/linux` boolean columns
- **Pricing queries:** Use `mat_final_price`, `mat_currency`, `mat_discount_percent`
- **Achievement queries:** Use `mat_achievement_count` extracted from JSONB

### **Query Documentation**

SQL queries used to generate CSVs are documented in:

- Work log: `/work-logs/10-dataset-accessibility-packages/`
- Query files: `01_temporal_growth.sql`, `02_genre_evolution.sql`, etc.

### **Reproducibility**

To regenerate CSVs:

1. Access production database: `psql -h proj-pgsql01 -d steamfull`
2. Execute queries from work-logs directory
3. Export results: `COPY (...) TO '/path/to/csv' CSV HEADER;`
4. Validate row counts match notebook expectations

---

## **Quality Assurance**

### **Validation Process**

This notebook underwent rigorous review:

- ✅ **Data Accuracy:** All statistics cross-validated against source database
- ✅ **Statistical Correctness:** Pricing percentages verified (77.8% sub-$10 paid games)
- ✅ **Visualization Quality:** Charts tested with actual data for clarity and accuracy
- ✅ **External Review:** Gemini Deep Research analysis confirmed publication-readiness
- ✅ **Code Quality:** All cells execute without errors, include proper error handling

### **Known Limitations**

1. **Currency Bias:** Analysis focuses on USD-priced games (59.5% of catalog); international pricing not included
2. **Temporal Aggregation:** Year-level analysis; seasonal patterns within years not explored
3. **Genre Multi-Labeling:** Games assigned to primary genre only for simplicity
4. **Platform Denominator:** Platform support percentages include free-to-play titles
5. **Success Metrics:** Analysis examines presence/pricing but lacks sales/revenue data

---

## **Citation**

When using this notebook in research or publications:

```bibtex
@dataset{fountain2025steam,
  author       = {Fountain, Donald},
  title        = {Steam Dataset 2025: A Large-Scale, Multi-Modal Dataset of the Steam Gaming Platform},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.17266923},
  url          = {https://doi.org/10.5281/zenodo.17266923}
}
```

**Notebook-Specific Citation:**
Fountain, D. (2025). "Platform Evolution & Market Landscape Analysis." In *Steam Dataset 2025* (Notebook 1). Zenodo. <https://doi.org/10.5281/zenodo.17266923>

---

## **Document Information**

| **Field** | **Value** |
|-----------|-----------|
| **Author** | VintageDon - <https://github.com/vintagedon> |
| **Created** | 2025-10-05 |
| **Last Updated** | 2025-10-05 |
| **Version** | 1.0 |
| **Status** | Published |
| **Notebook Runtime** | 3-5 minutes |
| **Skill Level** | Beginner |

---
*Tags: jupyter, notebook, temporal-analysis, pricing-strategy, market-research, steam-platform, data-visualization*

---

## 📋 **Additional Resources**

### **Learning Path**

This notebook is part of a 3-notebook progression:

1. **Notebook 1 (This)** - Platform Evolution → Beginner
2. **[Notebook 2](../02-semantic-game-discovery/README.md)** - Semantic Discovery → Intermediate
3. **[Notebook 3](../03-review-sentiment-success-prediction/README.md)** - Sentiment & Prediction → Advanced

### **External Resources**

- **NBViewer:** [View rendered notebook online](https://nbviewer.org/) (link TBD after publication)
- **Kaggle Kernel:** [Interactive version on Kaggle](https://www.kaggle.com/) (link TBD after publication)
- **GitHub Repository:** <https://github.com/vintagedon/steam-dataset-2025>
- **Dataset DOI:** <https://doi.org/10.5281/zenodo.17266923>

### **Support & Questions**

- **Issues:** Report problems via [GitHub Issues](https://github.com/vintagedon/steam-dataset-2025/issues)
- **Discussions:** Join conversations on [Kaggle Discussions](https://www.kaggle.com/datasets/steam-dataset-2025/discussion)
- **Contact:** <https://github.com/vintagedon>

---

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Copyright:** © 2025 Donald Fountain. All rights reserved under CC BY 4.0.
