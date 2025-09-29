# Phase 5: Analytics Framework and Visualization

> **Session Date:** 2025-09-03  
> **Status:** Complete  
> **Scripts Produced:** 2 production scripts | 1 SQL query library | 14 visualizations  
> **Key Innovation:** Metadata-driven visualization engine with decoupled SQL analytics

---

## Problem Statement

The steam5k database was populated and optimized, but its analytical value remained unproven. The project needed a scalable, automated framework to execute complex queries and generate shareable reports with professional visualizations - validating both the database design and the dataset's research potential.

---

## Solution Overview

Built a two-component analytics framework: a SQL query library containing 16+ sophisticated analyses, and a Python orchestration engine that executes queries, generates appropriate visualizations, and compiles publication-quality Markdown reports. The metadata-driven approach allows analysts to add new queries without modifying code.

---

## What Was Built

### Quick Reference

| Artifact | Purpose | Key Feature |
|----------|---------|-------------|
| `generate_analytical_report.py` | Visual report generator | Metadata-driven chart routing |
| `5k_report_generator.py` | Text-only report variant | Lightweight table-focused output |
| `analysis_queries.sql` | Query library | 16 labeled analytical queries |

---

### Script 1: `generate_analytical_report.py`

**Purpose:** Core orchestration engine that executes SQL queries and generates visual analytics reports

**Key Capabilities:**

- Parses SQL file for labeled query blocks with metadata
- Routes to appropriate chart type based on title keywords
- Uses Pandas/Seaborn/Matplotlib for publication-quality visuals
- Compiles Markdown report with embedded charts and data tables

**Usage:**

```bash
python3 generate_analytical_report.py steam5k
# Generates report + charts/ directory with 14 PNGs
```

**Performance Notes:** Complete suite of 16 complex queries + 14 chart generations executes in <30 seconds, validating Phase 4 optimization strategy.

<details>
<summary>Execution Output</summary>

```bash
--- Steam Dataset Visual Analysis Report Generator ---
Ensuring chart directory 'charts' exists...
Loading database credentials...
Reading queries from analysis_queries.sql...
Found 16 queries to execute.
Connecting to PostgreSQL database at 10.25.20.8...
Connection successful.

Executing query 1/16: "1. Genre Co-occurrence Heatmap"...
 -> Success! Fetched 380 rows.
Successfully generated chart: 1_genre_cooccurrence_heatmap.png

Executing query 2/16: "2. Top 15 Free-to-Play Niches (by Genre)"...
 -> Success! Fetched 15 rows.
Successfully generated chart: 2_top_15_freetoplay_niches_by_genre.png

[... 14 more queries ...]

Executing query 16/16: "12. Hardware Trends Over Time (Recommended RAM)"...
 -> Success! Fetched 12 rows.
Successfully generated chart: 12_hardware_trends_over_time_recommended_ram.png

Writing final report to analytical_report_steam5k_20250903_162847.md...
--- Report generation complete! ---
```

</details>

---

### Script 2: `5k_report_generator.py`

**Purpose:** Lightweight text-only report generator for quick data review

**Key Capabilities:**

- Executes same query library without visualization overhead
- Outputs clean Markdown tables for rapid inspection
- Lower dependency footprint (no matplotlib/seaborn)
- Useful for CI/CD validation or text-only environments

**Usage:**

```bash
python3 5k_report_generator.py
# Generates steam_analysis_report.md
```

---

### SQL Library: `analysis_queries.sql`

**Purpose:** Standalone query library demonstrating database analytical capabilities

**Query Categories:**

- Genre analysis (co-occurrence patterns, F2P niches)
- Quality metrics (Metacritic distributions, developer reputation)
- Commercial intelligence (pricing trends, market segmentation)
- Temporal analysis (release patterns, hardware evolution)
- Correlation studies (price/quality relationships)

**Key Features:**

- Metadata comments for automation (`-- ===== CHART TITLE: ... =====`)
- Complex SQL patterns (CTEs, window functions, regex parsing)
- Optimized for indexed tables and materialized views

<details>
<summary>Sample Query: Genre Co-occurrence Heatmap</summary>

```sql
-- ===== CHART TITLE: 1. Genre Co-occurrence Heatmap =====
-- Purpose: To find which genres are most frequently paired together on the same game.
-- Chart Type: Heatmap
WITH GameGenres AS (
    SELECT a.appid, g.name as genre_name
    FROM applications a
    JOIN application_genres ag ON a.appid = ag.appid
    JOIN genres g ON ag.genre_id = g.id
    WHERE a.type = 'game'
)
SELECT
    gg1.genre_name AS genre_a,
    gg2.genre_name AS genre_b,
    COUNT(*) AS co_occurrence_count
FROM
    GameGenres gg1
JOIN
    GameGenres gg2 ON gg1.appid = gg2.appid AND gg1.genre_name < gg2.genre_name
GROUP BY gg1.genre_name, gg2.genre_name
ORDER BY co_occurrence_count DESC
LIMIT 50;
-- === END QUERY ===
```

</details>

---

## Technical Approach

### Architecture Decisions

**Decoupled SQL and Python:** The critical architectural decision was separating analytical logic (SQL) from orchestration logic (Python). Data analysts can write/test queries without touching code, while the Python script serves as a generic, reusable reporting engine. This modularity is essential for research datasets where analytical questions evolve.

**Metadata-Driven Visualization:** Rather than hardcoding chart selection (`if query_title == "Genre Heatmap":`), the system parses keywords from SQL comments. This makes the framework extensible - new analyses require only SQL changes, not code modifications.

**Pandas as Bridge Layer:** All results load into Pandas DataFrames, providing a powerful intermediate representation. This pattern enables seamless integration with Python's data science ecosystem (NumPy, SciPy, scikit-learn) while maintaining clean separation from the database.

### Key Implementation Patterns

1. **Visualization Router Pattern:** The `process_and_visualize()` function inspects DataFrame metadata and routes to appropriate Seaborn functions based on title keywords. Scalable approach handling multiple chart types without conditional bloat.

2. **Automated Asset Management:** Script creates output directories, generates standardized filenames, saves charts, and embeds relative paths in Markdown - ensuring portable, self-contained reports.

3. **Query Block Parser:** Custom delimiter system (`-- === END QUERY ===`) enables clean separation of multi-statement queries while preserving SQL file readability for direct psql execution.

### Technical Innovations

**Keyword-Based Chart Selection:** Novel approach using SQL comment metadata to drive Python visualization logic. Eliminates tight coupling while maintaining human readability of query library.

---

## Validation & Results

### Success Metrics

- ✅ **Query Execution:** All 16 complex queries executed successfully without errors
- ✅ **Performance:** Complete analytics pipeline (query + visualization) completed in <30 seconds
- ✅ **Output Quality:** 14 publication-ready charts + comprehensive Markdown report generated
- ✅ **Database Validation:** Confirmed Phase 4 schema design supports complex analytical workloads

### Key Analytical Findings

| Discovery | Insight | Business Implication |
|-----------|---------|---------------------|
| Genre dominance | "Indie" + "Action" most common pairing | Market saturation in indie action space |
| F2P market maturity | "Free to Play" is distinct genre with 800+ games | Established business model with dedicated audience |
| Quality clustering | 70-80 Metacritic range most populated | Bulk of commercially viable games score "good" not "great" |
| Price correlation | Weak correlation (0.12) between price and Metacritic | Quality doesn't command premium pricing |

---

## Integration Points

**Database:** Queries steam5k PostgreSQL database via application user credentials

**File System:**

- Reads: `analysis_queries.sql` for query definitions
- Writes: `analytical_report_*.md` (Markdown report), `charts/*.png` (visualizations)

**External Dependencies:** Pandas (DataFrame operations), Matplotlib/Seaborn (visualization), psycopg2 (PostgreSQL driver)

---

## Usage Guide

### Prerequisites

```bash
# Core dependencies
pip install pandas matplotlib seaborn psycopg2-binary python-dotenv

# Environment variables in .env
PG_HOST=10.25.20.8
PG_PORT=5432
PG_APP_USER=steam_app
PG_APP_USER_PASSWORD=<password>
```

### Running the Analytics Pipeline

**Step 1: Generate Visual Report (Recommended)**

```bash
python3 generate_analytical_report.py steam5k
# Output: analytical_report_steam5k_YYYYMMDD_HHMMSS.md + charts/ directory
```

**Step 2: Alternative Text-Only Report**

```bash
python3 5k_report_generator.py
# Output: steam_analysis_report.md (no charts, faster execution)
```

### Verification

```bash
# Verify report generated
ls -lh analytical_report_steam5k_*.md

# Verify all charts created
ls -lh charts/*.png | wc -l  # Should output: 14

# Quick quality check on first chart
file charts/1_genre_cooccurrence_heatmap.png  # Confirm PNG format
```

### Adding New Analyses

```sql
-- In analysis_queries.sql, add:

-- ===== CHART TITLE: Your Analysis Title =====
-- Purpose: Description of what this query reveals
-- Chart Type: [Bar/Line/Scatter/Heatmap]
SELECT ...
-- === END QUERY ===
```

No Python code changes required - script auto-detects and visualizes new queries.

---

## Lessons Learned

### Challenges Overcome

| Challenge | Root Cause | Solution | Technical Approach |
|-----------|-----------|----------|-------------------|
| Hardcoded visualization logic | Initial design tied chart type to query position | Keyword-based routing system | Parse SQL comments for chart type hints |
| Query maintenance burden | SQL scattered across Python strings | External SQL file with delimiter | Split on `-- === END QUERY ===` separator |
| Chart filename conflicts | Multiple queries generating same filename | Standardized naming convention | Slugify title + preserve execution order |
| Report portability issues | Absolute paths broke when moving reports | Relative path generation | Use `Path.relative_to()` for Markdown embeds |

### Technical Insights

**PostgreSQL Query Performance Excellent:** Complex queries with multiple joins, CTEs, and aggregations consistently sub-second on 8.7k row dataset. Validates Phase 4 indexing and materialized view strategy.

**Pandas as Universal Data Layer:** Using DataFrames as intermediate representation between SQL and visualization proved extremely flexible. Same data structure works for tables, charts, statistical analysis, or ML feature engineering.

**Seaborn High-Level API Power:** Single-line chart generation (`sns.barplot(...)`) produces publication-quality output. Dramatically reduces code complexity compared to raw Matplotlib.

### Process Insights

**Metadata-Driven Systems Scale:** The keyword-parsing approach eliminates code churn when adding analyses. New queries require only SQL knowledge, democratizing analytics contributions.

**Decoupling Enables Parallel Development:** Data analysts can develop/test queries in psql while Python engineers improve the reporting engine. True separation of concerns.

---

## Next Steps

### Immediate Actions

1. Apply framework to full 239k application dataset (steam_full database)
2. Expand query library with ML-focused analyses (embeddings, clustering)
3. Add automated report scheduling for dataset monitoring

### Enhancement Opportunities

**Short-term:** Add interactive visualizations using Plotly, implement query result caching for iterative report generation

**Medium-term:** Develop parameterized query templates, add statistical significance testing for correlations, implement A/B comparison reports

**Long-term:** Build web dashboard using Streamlit/Dash for live exploration, integrate with Jupyter for notebook-based analysis, add anomaly detection for data quality monitoring

---

## Session Metadata

**Development Environment:** Python 3.12, PostgreSQL 16, Pandas 2.x, Matplotlib 3.x, Seaborn 0.13  
**Total Development Time:** ~6 hours  
**Session Type:** Production development + analytical validation  
**Code Version:** All scripts v1.0 - production ready

---

**Related Worklogs:**

- Phase 4: Database Pipeline Implementation (steam5k creation)
- Phase 6: Full Dataset Scaling (apply framework to 239k apps)
- Publication Roadmap: Packaging for Kaggle/Zenodo release
-
