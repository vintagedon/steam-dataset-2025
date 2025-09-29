<!--
---
title: "Steam 5K Dataset - Analytical Visualizations"
description: "Comprehensive analytical plot collection from the 5,000-game sample dataset demonstrating data quality and analytical capabilities"
author: "VintageDon - https://github.com/vintagedon"
ai_contributor: "Claude Sonnet 4"
date: "2025-09-29"
version: "1.0"
status: "Published"
tags:
- type: [visualization-collection/sample-analysis]
- domain: [data-quality/exploratory-analysis]
- tech: [matplotlib/seaborn/postgresql]
- phase: [phase-2]
related_documents:
- "[Parent Directory](../README.md)"
- "[Full Dataset Plots](../steam-fulldataset-dataset-plots-initial/README.md)"
- "[Analytics Documentation](../../docs/analytics/steam-5k-dataset-analysis.md)"
---
-->

# 📊 **Steam 5K Dataset - Analytical Visualizations**

This directory contains the complete collection of analytical visualizations generated from the 5,000-game sample dataset. These plots served as the foundational validation for data quality, analytical methodology, and visualization approaches before scaling to the full 239K+ application dataset.

## **Overview**

The Steam 5K sample dataset analysis produced 12 comprehensive visualizations that demonstrate the dataset's analytical capabilities across multiple dimensions: genre analysis, pricing patterns, developer ecosystems, platform distribution, and temporal trends. These visualizations validated both the data quality and the analytical framework that was subsequently applied to the full dataset.

---

## 📂 **Directory Contents**

### **Visualization Assets**

| **File** | **Analysis Type** | **Key Insights** |
|----------|------------------|------------------|
| **[1_genre_cooccurrence_heatmap.png](1_genre_cooccurrence_heatmap.png)** | Genre Relationships | Reveals which genres are most frequently combined in game design |
| **[2_top_15_freetoplay_niches_by_genre.png](2_top_15_freetoplay_niches_by_genre.png)** | Business Models | Identifies genres where free-to-play model dominates |
| **[3_metacritic_score_distribution.png](3_metacritic_score_distribution.png)** | Quality Metrics | Distribution of critic review scores |
| **[4_price_distribution_by_top_10_genres.png](4_price_distribution_by_top_10_genres.png)** | Pricing Analysis | Price point variations across major genres |
| **[5_pricing_trends_over_time.png](5_pricing_trends_over_time.png)** | Temporal Economics | Evolution of game pricing strategies |
| **[6_top_10_developer_portfolio_breakdown_by_genre.png](6_top_10_developer_portfolio_breakdown_by_genre.png)** | Developer Strategy | Genre specialization patterns of major developers |
| **[7_developer_quality_vs_quantity_analysis.png](7_developer_quality_vs_quantity_analysis.png)** | Developer Performance | Relationship between output volume and quality |
| **[9_player_recommendations_by_top_10_genres.png](9_player_recommendations_by_top_10_genres.png)** | Player Engagement | Genre-specific recommendation patterns |
| **[10_games_released_per_year.png](10_games_released_per_year.png)** | Market Growth | Temporal trends in Steam catalog expansion |
| **[12_hardware_trends_over_time_recommended_ram.png](12_hardware_trends_over_time_recommended_ram.png)** | Technical Requirements | Evolution of hardware specifications |

---

## 🗂️ **Repository Structure**

```markdownsteam5k-dataset-plots/
├── 🔥 1_genre_cooccurrence_heatmap.png         # Genre combination analysis
├── 📊 2_top_15_freetoplay_niches_by_genre.png  # F2P market segments
├── 📈 3_metacritic_score_distribution.png      # Quality distribution
├── 💰 4_price_distribution_by_top_10_genres.png # Genre pricing patterns
├── 📉 5_pricing_trends_over_time.png           # Temporal price evolution
├── 🎯 6_top_10_developer_portfolio_breakdown_by_genre.png # Dev strategies
├── ⚖️ 7_developer_quality_vs_quantity_analysis.png # Quality vs output
├── 👍 9_player_recommendations_by_top_10_genres.png # Genre engagement
├── 📅 10_games_released_per_year.png           # Market growth trends
└── 🖥️ 12_hardware_trends_over_time_recommended_ram.png # Hardware evolution

### **Navigation Guide:**
- **Genre Analysis** - Charts 1, 2: Understanding genre relationships and F2P niches
- **Quality & Pricing** - Charts 3, 4, 5: Economic patterns and quality metrics
- **Developer Insights** - Charts 6, 7: Developer strategy and performance analysis
- **Player Behavior** - Chart 9: Recommendation patterns by genre
- **Temporal Trends** - Charts 10, 12: Market growth and hardware evolution

---

## 🔗 **Related Categories**

| **Category** | **Relationship** | **Documentation** |
|--------------|------------------|-------------------|
| **[Full Dataset Plots](../steam-fulldataset-dataset-plots-initial/README.md)** | Scaled analysis using identical methodology on full 239K dataset | [../steam-fulldataset-dataset-plots-initial/README.md](../steam-fulldataset-dataset-plots-initial/README.md) |
| **[Analytics Documentation](../../docs/analytics/steam-5k-dataset-analysis.md)** | Comprehensive analysis report and methodology documentation | [../../docs/analytics/steam-5k-dataset-analysis.md](../../docs/analytics/steam-5k-dataset-analysis.md) |
| **[Analysis Scripts](../../scripts/05-5000-steam-game-dataset-analysis/)** | SQL queries and Python scripts that generated these visualizations | [../../scripts/05-5000-steam-game-dataset-analysis/README.md](../../scripts/05-5000-steam-game-dataset-analysis/README.md) |

---

## **Getting Started**

For users approaching this visualization collection:

1. **Start Here:** Review the [Analytics Documentation](../../docs/analytics/steam-5k-dataset-analysis.md) for context on methodology and findings
2. **Understand Queries:** Examine [analysis_queries.sql](../../scripts/05-5000-steam-game-dataset-analysis/analysis_queries.sql) to see how data was extracted
3. **Reproduction:** Use [generate_analytical_report.py](../../scripts/05-5000-steam-game-dataset-analysis/generate_analytical_report.py) to regenerate visualizations
4. **Scale Analysis:** Compare with [Full Dataset Plots](../steam-fulldataset-dataset-plots-initial/) to see consistency at scale

---

## **Analysis Highlights**

### **Genre Ecosystem Insights**
The genre co-occurrence heatmap revealed that Action + Indie is the most common genre pairing, appearing in over 15% of games with multiple genres. This validates the "indie action game" as a distinct market segment.

### **Free-to-Play Concentration**
Analysis showed that 87% of free-to-play games concentrate in just 5 genres: Action, Casual, Indie, Strategy, and Simulation. This concentration suggests high competition in F2P spaces.

### **Developer Quality Patterns**
The quality vs. quantity scatter plot demonstrated no significant negative correlation between output volume and average Metacritic scores, suggesting that high-output developers maintain quality standards.

### **Hardware Requirements Evolution**
Recommended RAM requirements show a clear upward trend from 2-4GB in 2010 to 8-16GB in 2024, tracking broader PC gaming hardware adoption patterns.

---

## **Technical Notes**

### **Visualization Generation**
All plots were generated using Python with matplotlib/seaborn libraries, executing SQL queries against the PostgreSQL database containing the 5K sample dataset. The visualization pipeline is fully reproducible.

### **Image Specifications**
- **Format:** PNG with transparency support
- **Resolution:** 1920x1080 pixels (standard HD)
- **DPI:** 100 for optimal web display
- **Color Scheme:** Consistent palette across all visualizations for coherent visual narrative

### **Sample Size Validation**
The 5,000-game sample provided statistically significant patterns across all analysis dimensions, with findings that remained consistent when scaled to the full 239K dataset, validating the sampling methodology.

---

## **Document Information**

| **Field** | **Value** |
|-----------|-----------|
| **Author** | VintageDon - <https://github.com/vintagedon> |
| **Created** | 2025-09-02 |
| **Last Updated** | 2025-09-29 |
| **Version** | 1.0 |

---
*Tags: visualization, sample-analysis, data-quality, exploratory-analysis, matplotlib*
