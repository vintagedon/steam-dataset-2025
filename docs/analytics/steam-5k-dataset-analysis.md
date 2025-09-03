<!--
---
title: "Steam 5K Dataset Statistical Analysis"
description: "Comprehensive statistical analysis of the Steam Dataset 2025 prototype implementation, providing baseline metrics and insights from 5,000 games, 8,711 applications, and 36,265 user reviews"
author: "VintageDon - https://github.com/vintagedon"
ai_contributor: "Claude Sonnet 4"
date: "2025-09-02"
version: "1.0"
status: "Published"
tags:
- type: [kb-article/statistical-analysis/baseline-metrics]
- domain: [data-analysis/gaming-analytics/dataset-validation]
- tech: [postgresql/pgvector/data-science/statistical-analysis]
- audience: [data-scientists/analysts/researchers]
related_documents:
- "[Steam API Data Schema Analysis](steam-api-schema-analysis.md)"
- "[PostgreSQL Schema Design](../scripts/04-postgres_schema_design/README.md)"
- "[Database Performance Benchmarks](database-performance-analysis.md)"
---
-->

# 📊 Steam 5K Dataset Statistical Analysis

This document provides comprehensive statistical analysis of the Steam Dataset 2025 prototype implementation, examining 5,000 games within a corpus of 8,711 total applications. The analysis establishes baseline metrics for content taxonomy, commercial patterns, and quality distributions that validate the dataset's analytical potential and inform scaling strategies for the complete 260,000+ application collection.

---

# 🎯 1. Introduction

This section establishes the analytical foundation for understanding the Steam Dataset 2025 prototype implementation and its statistical characteristics across multiple dimensions of gaming market analysis.

## 1.1 Purpose

This statistical analysis quantifies the fundamental characteristics of the Steam gaming ecosystem as captured in our 5,000-game prototype dataset. It provides empirical validation of data collection methodologies, establishes baseline metrics for comparative analysis, and demonstrates the analytical depth possible with the multi-modal database architecture.

## 1.2 Scope

Dataset Composition Analyzed:

- 8,711 total applications (games, DLC, software, media)
- 5,000 primary games with complete metadata
- 1,792 downloadable content packages
- 36,265 user reviews with sentiment and engagement data
- 6,740 unique developers and 5,605 publishers

## 1.3 Target Audience

Primary Users: Data scientists, gaming industry analysts, academic researchers studying digital markets  
Secondary Users: Game developers, publishers, platform strategists interested in market intelligence  
Background Assumed: Understanding of statistical concepts, familiarity with gaming industry terminology

## 1.4 Overview

This analysis demonstrates the Steam Dataset 2025's capability to support sophisticated market research through systematic examination of content taxonomy, pricing strategies, quality metrics, and developer ecosystems. The findings establish quantitative baselines that will inform full-scale implementation and provide comparative benchmarks for longitudinal analysis.

---

# 🔗 2. Dependencies & Relationships

This section maps the analytical relationships and technical dependencies that enable comprehensive statistical analysis of the Steam gaming dataset.

## 2.1 Related Components

| Component | Relationship | Integration Points | Documentation |
|---------------|------------------|------------------------|-------------------|
| PostgreSQL Schema | Data foundation providing normalized structure | Applications, reviews, developers, genres tables | [schema.sql](../scripts/04-postgres_schema_design/schema.sql) |
| Collection Pipeline | Source data validation and quality assurance | Success rates, content type distribution | [Steam API Analysis](steam-api-schema-analysis.md) |
| Performance Infrastructure | Database optimization supporting analytical queries | Query performance, indexing strategies | [PostgreSQL Benchmarks](database-performance-analysis.md) |
| JSONB Analytics | Complex data structure analysis capabilities | Content descriptors, system requirements parsing | [Advanced JSONB Queries](../scripts/04-postgres_schema_design/README.md) |

## 2.2 External Dependencies

- [PostgreSQL 16](https://www.postgresql.org/) - Relational database with JSONB support and analytical functions
- [Steam Web API](https://steamcommunity.com/dev) - Official data source providing application metadata and user reviews
- Statistical Analysis Tools - Python/pandas for data validation and additional statistical calculations

---

# ⚙️ 3. Technical Documentation

This section provides detailed statistical findings and analytical insights derived from the Steam Dataset 2025 prototype implementation, organized by analytical domain.

## 3.1 Dataset Composition & Scale

The prototype implementation demonstrates significant scale and diversity across multiple content categories.

High-Level Metrics:

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Applications | 8,711 | 100% |
| Primary Games | 5,000 | 57.4% |
| Downloadable Content | 1,792 | 20.6% |
| Other Content Types | 1,919 | 22.0% |
| Total User Reviews | 36,265 | - |
| Unique Developers | 6,740 | - |
| Unique Publishers | 5,605 | - |

Content Distribution Analysis:

The dataset captures substantial diversity in application types, with games comprising the majority but significant representation of downloadable content and specialized software applications. The 7.2:1 ratio of reviews to games (36,265:5,000) indicates robust user engagement data availability.

## 3.2 Content Taxonomy & Genre Distribution

Genre analysis reveals the structural characteristics of the modern Steam catalog and identifies dominant content categories.

Top 15 Genre Distribution:

| Genre | Game Count | Market Share |
|-------|------------|-------------|
| Indie | 4,400 | 88.0% |
| Action | 2,794 | 55.9% |
| Casual | 2,621 | 52.4% |
| Adventure | 2,517 | 50.3% |
| Simulation | 1,570 | 31.4% |
| Strategy | 1,539 | 30.8% |
| RPG | 1,510 | 30.2% |
| Free To Play | 710 | 14.2% |
| Early Access | 473 | 9.5% |
| Sports | 254 | 5.1% |
| Racing | 245 | 4.9% |
| Massively Multiplayer | 206 | 4.1% |
| Design & Illustration | 149 | 3.0% |
| Web Publishing | 114 | 2.3% |
| Utilities | 74 | 1.5% |

Key Taxonomic Insights:

- Indie Dominance: 88% of games carry the "Indie" tag, reflecting Steam's role as a platform for independent developers
- Multi-Genre Prevalence: High percentages indicate extensive genre overlap, with games typically carrying 3-4 genre tags
- Content Diversity: Representation across traditional gaming genres plus utility and creative software categories

## 3.3 Commercial Analysis & Pricing Patterns

Economic analysis reveals pricing strategies and business model distribution across the Steam platform.

Business Model Distribution:

- Free-to-Play Games: 653 (13.1%)
- Paid Games: 4,347 (86.9%)

Price Distribution for Paid Games:

| Price Range | Game Count | Cumulative % |
|-------------|------------|--------------|
| $0.01 - $20.00 | 4,523 | 92.3% |
| $20.01 - $40.00 | 225 | 96.9% |
| $40.01 - $60.00 | 34 | 97.6% |
| $60.01 - $80.00 | 9 | 97.8% |
| $80.01 - $100.00 | 7 | 97.9% |
| >$100.00 | 20 | 100.0% |

Pricing Strategy Analysis:

The distribution demonstrates a heavily skewed market toward lower price points, with 92.3% of paid games priced under $20. This reflects the indie-dominated nature of the platform and competitive pricing strategies for digital distribution.

## 3.4 Quality Metrics & Reception Analysis

Critical reception analysis examines the relationship between professional reviews and market positioning.

Metacritic Score Distribution:

| Score Bracket | Count | Quality Tier |
|---------------|-------|-------------|
| 90-100 (Universal Acclaim) | 4 | Elite |
| 75-89 (Generally Favorable) | 98 | High Quality |
| 50-74 (Mixed/Average) | 67 | Standard |
| 0-49 (Generally Unfavorable) | 3 | Poor |

Developer Performance Analysis:

Top developers by average Metacritic score (minimum 2 rated products):

| Developer | Rated Products | Average Score |
|-----------|----------------|---------------|
| IO Interactive A/S | 2 | 87.00 |
| CAPCOM Co., Ltd. | 2 | 85.00 |
| Kluge Interactive | 2 | 83.00 |
| Robot Entertainment | 2 | 83.00 |
| Chucklefish | 2 | 82.00 |

Publisher Performance Analysis:

| Publisher | Rated Products | Average Score |
|-----------|----------------|---------------|
| WB Games | 2 | 88.50 |
| IO Interactive A/S | 2 | 87.00 |
| CAPCOM Co., Ltd. | 2 | 85.00 |
| Electronic Arts | 3 | 82.66 |

Quality Correlation Analysis:

- Price vs. Metacritic Score: Pearson's correlation coefficient of 0.1202 indicates minimal linear relationship between price and critical reception
- Market Implication: Quality and pricing operate through complex, non-linear relationships in the digital gaming market

---

# 🛠️ 4. Usage & Maintenance

This section provides practical guidance for leveraging statistical analysis findings and maintaining analytical currency as the dataset scales.

## 4.1 Usage Guidelines

Analytical Applications:

- Market Research: Use genre distribution and pricing analysis for competitive intelligence
- Investment Analysis: Developer and publisher performance metrics inform portfolio decisions
- Platform Strategy: Content taxonomy guides curation and recommendation algorithms
- Academic Research: Statistical baselines enable longitudinal studies of digital market evolution

Statistical Interpretation:

- Sample Representativeness: 5K dataset provides statistically significant representation of Steam's indie-heavy catalog
- Scaling Considerations: Genre percentages and pricing distributions expected to remain stable at full 260K scale
- Correlation Limitations: Low price-quality correlation suggests market complexity requiring multivariate analysis

## 4.2 Analytical Extensions

Advanced Statistical Methods:

- Cluster Analysis: Genre co-occurrence patterns reveal market niches and hybrid categories
- Regression Modeling: Multi-factor analysis of success predictors beyond simple price-quality correlations
- Time Series Analysis: Release date patterns and temporal market evolution (requires full dataset)
- Network Analysis: Developer-publisher relationship mapping and ecosystem analysis

## 4.3 Data Quality Considerations

Statistical Validity:

- Coverage Bias: Steam API success rate (~56%) may introduce selection bias toward more successful titles
- Temporal Representation: Dataset captures current market state; historical analysis requires longitudinal collection
- Regional Limitations: Analysis reflects global Steam catalog; regional pricing variations require additional analysis

---

# 📚 5. References & Related Resources

This section provides comprehensive links to supporting documentation, analytical tools, and research materials that extend the statistical analysis capabilities.

## 5.1 Internal References

| Document Type | Title | Relationship | Link |
|-------------------|-----------|------------------|----------|
| Schema Analysis | Steam API Data Schema Analysis | Complementary technical analysis of data structure | [steam-api-schema-analysis.md](steam-api-schema-analysis.md) |
| Performance Analysis | PostgreSQL Database Benchmarks | Infrastructure supporting analytical queries | [database-performance-analysis.md](database-performance-analysis.md) |
| Implementation Guide | PostgreSQL Schema Design | Technical implementation of analyzed data structures | [../scripts/04-postgres_schema_design/README.md](../scripts/04-postgres_schema_design/README.md) |
| Collection Pipeline | Steam API Testing Results | Data collection methodology validation | [../scripts/01-test-steam-api/README.md](../scripts/01-test-steam-api/README.md) |

## 5.2 External Resources

| Resource Type | Title | Description | Link |
|-------------------|-----------|-----------------|----------|
| Industry Analysis | Steam Platform Statistics | Valve's official platform metrics for comparative analysis | [Steam Database](https://steamdb.info/) |
| Academic Research | Digital Game Market Analysis | Peer-reviewed research on digital gaming economics | [Game Studies Journal](http://gamestudies.org/) |
| Statistical Methods | Gaming Analytics Methodology | Best practices for statistical analysis of gaming data | [IEEE Computer Society](https://www.computer.org/) |
| Market Intelligence | Gaming Industry Reports | Professional market analysis for context and validation | [Newzoo Games Market Reports](https://newzoo.com/) |

---

# 📜 6. Documentation Metadata

This section provides comprehensive information about document creation, analytical methodology, and quality assurance procedures.

## 6.1 Change Log

| Version | Date | Changes | Author |
|------------|----------|-------------|------------|
| 1.0 | 2025-09-02 | Initial statistical analysis documentation from 5K prototype dataset | VintageDon |

*Document Version: 1.0 | Last Updated: 2025-09-02 | Status: Published*
