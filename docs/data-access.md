<!--
---
title: "Steam Dataset 2025: Data Access Guide"
description: "Complete guide to accessing 239,664 Steam applications via Zenodo, Kaggle, and GitHub with download procedures and file specifications"
author: "VintageDon"
orcid: "0009-0008-7695-4093"
created: "2025-09-07"
last_updated: "2025-01-06"
version: "2.0"
tags: ["data-access", "download", "zenodo", "kaggle", "dataset"]
category: "documentation"
status: "published"
---
-->

# 📥 Steam Dataset 2025: Data Access Guide

This guide provides comprehensive information for accessing Steam Dataset 2025 across multiple platforms. The complete dataset (239,664 applications, 1,048,148 reviews in a bounded per-application sample) is available through Zenodo (with persistent DOI) and Kaggle (published mirror with interactive notebooks). GitHub hosts documentation, the publicly tracked 5K samples and the development history — not the release packages.

---

## 🎯 **1. Purpose & Scope**

### **1.1 Purpose**

Enable researchers, data scientists, and developers to access Steam Dataset 2025 through the most appropriate channel for their use case, whether that's permanent academic hosting (Zenodo), collaborative analysis (Kaggle), or quick sampling (GitHub).

### **1.2 Scope**

**What's Covered:**

- ✅ Complete dataset access via Zenodo (239,664 applications)
- ✅ Interactive analysis via Kaggle notebooks
- ✅ Sample dataset for immediate testing (5K games via GitHub)
- ✅ File formats, sizes, and download procedures
- ✅ Citation requirements and academic use guidance

### **1.3 Target Audience**

**Primary Users:** Academic researchers requiring DOI citation, data scientists performing large-scale analysis  
**Secondary Users:** Students learning with sample data, developers building Steam-related applications  
**Background Assumed:** Basic familiarity with CSV/Parquet files, Jupyter notebooks, or academic datasets

### **1.4 Overview**

Steam Dataset 2025 is available through three complementary channels: **Zenodo** for permanent academic hosting with DOI citation (recommended for research), **Kaggle** for interactive notebooks and community engagement (published), and **GitHub** for 5K sample data and the development history (perfect for testing).

---

## 📦 **2. Dataset Access Options**

This section outlines all available access methods, helping you choose the right platform for your needs.

### **2.1 Zenodo: Official Academic Release (Recommended for Research)**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17266922.svg)](https://doi.org/10.5281/zenodo.17266922)

**Best For:** Academic research, publications, permanent archival access  
**Status:** ✅ Published and Available

#### **Official v1.0.0 Record Packages**

The Zenodo record exposes four ZIP packages (names, bytes and provider checksums verified 2026-11-13; see [artifact reference](release-1.0.1/artifact-reference.json)):

| **Package** | **Format** | **Bytes** | **Description** |
|-------------|------------|----------:|-----------------|
| **steam-dataset-2025-v1.zip** | ZIP | 40,212,720 | Release bundle: documentation, dataset card, notebooks, notebook data |
| **steam_dataset_2025_csv_package_v1.zip** | ZIP of CSVs | 320,368,878 | Accessibility CSV exports (core tables, no database required) |
| **steam_dataset_2025_power_users_dump_v1.zip** | PostgreSQL dump | 7,204,002,678 | Complete database dump for full restoration |
| **steam_dataset_2025_embeddings_package_v1.zip** | Embeddings package | 4,870,419,373 | Pre-computed BGE-M3 1024-dim vectors |

The individual CSV, Parquet and NPY files previously listed here are members inside these packages, not separately downloadable record files; their exact member list is available after downloading the package.

#### **Download Procedure**

```bash
# Option 1: Direct browser download
# Visit: https://doi.org/10.5281/zenodo.17266922
# Click "Download" on the files you need

# Option 2: Command line download (requires zenodo_get)
pip install zenodo-get
zenodo_get 10.5281/zenodo.17266923

# Option 3: wget download (replace with actual file URLs from Zenodo)
wget https://zenodo.org/record/17266923/files/steam_dataset_2025_csv_package_v1.zip
wget https://zenodo.org/record/17266923/files/steam_dataset_2025_power_users_dump_v1.zip
```

#### **Advantages**

- ✅ **Permanent DOI** for academic citation
- ✅ **Version Controlled** releases with change tracking
- ✅ **Academic Standard** hosting for research credibility
- ✅ **Long-Term Preservation** guaranteed by Zenodo/CERN
- ✅ **Complete Package** including documentation and notebooks

**[📥 Access on Zenodo](https://doi.org/10.5281/zenodo.17266922)**

---

### **2.2 Kaggle: Interactive Analysis Platform (Published)**

**Best For:** Interactive exploration, community discussions, GPU-accelerated notebooks  
**Status:** ✅ Published

#### **Kaggle Features**

- 📓 **Pre-Loaded Notebooks** - 3 production-ready analysis examples
- 💬 **Community Discussion** - Forums for questions and collaboration
- 🚀 **Zero Setup** - Instant Jupyter environment
- 🎮 **GPU Access** - Free GPU acceleration for ML workflows
- 📊 **Version Tracking** - Fork and modify for your analysis

#### **Expected Contents**

| **Component** | **Description** |
|---------------|-----------------|
| **Main Dataset** | Core CSV files optimized for pandas/notebook use |
| **Notebook Data** | Pre-exported subsets for notebook examples |
| **Sample Notebooks** | Platform evolution, semantic search, ML prediction |
| **Discussion Forum** | Community Q&A and collaboration space |

#### **Access Procedure**

1. Visit the Kaggle dataset page: `https://www.kaggle.com/datasets/crainbramp/steam-dataset-2025-multi-modal-gaming-analytics`
2. Click "New Notebook" for instant Jupyter environment
3. Or download CSV files directly from dataset page
4. Join discussions and competitions

**Advantages:**

- ✅ **No Download Required** - Work directly in browser
- ✅ **Instant Environment** - Pre-configured with all libraries
- ✅ **Community Features** - Discussions, competitions, forking
- ✅ **Free Resources** - GPU access and storage included

**[📊 Explore on Kaggle](https://www.kaggle.com/datasets/crainbramp/steam-dataset-2025-multi-modal-gaming-analytics)**

---

### **2.3 GitHub: Sample Dataset & Code Repository**

**Best For:** Testing workflows, exploring methodology, accessing ETL code  
**Status:** ✅ Available Now

#### **GitHub Contents**

| **Component** | **Location** | **Size** | **Description** |
|---------------|--------------|----------|-----------------|
| **5K Sample Games** | `data/01_raw/` | 14,089,513 B | 5K-run collection artifact (Git LFS object) |
| **5K Sample Reviews** | `data/01_raw/` | 11,202,479 B | Review sample from the 5K run (Git LFS object) |
| **Pipeline History** | `work-logs/` | N/A | Collection/processing code and records (12 phase directories; relocation to `scripts/` is planned maintenance) |
| **Documentation** | `docs/` | N/A | Technical specifications and guides |
| **Notebooks** | `steam-dataset-2025-v1/notebooks/` | N/A | 3 analysis examples with PDFs |
| **Work Logs** | `work-logs/` | N/A | Development history (12 phases) |

#### **Access Procedure**

```bash
# Option 1: Clone complete repository (sample files are Git LFS objects)
git clone https://github.com/vintagedon/steam-dataset-2025.git
cd steam-dataset-2025
git lfs pull --include "data/01_raw/*.json.gz"

# Option 2: Download the two tracked sample objects directly
wget -O steam_2025_5k-dataset-games_20250831.json.gz \
  https://media.githubusercontent.com/media/vintagedon/steam-dataset-2025/main/data/01_raw/steam_2025_5k-dataset-games_20250831.json.gz
wget -O steam_2025_5k-dataset-reviews_20250901.json.gz \
  https://media.githubusercontent.com/media/vintagedon/steam-dataset-2025/main/data/01_raw/steam_2025_5k-dataset-reviews_20250901.json.gz

# Verify against the pinned SHA-256, then decompress
sha256sum steam_2025_5k-dataset-games_20250831.json.gz   # 3b46222510ad64b87e8a0c63c92dba8f5788e0b8abdd4a1f3471ca0d7a70f2af
sha256sum steam_2025_5k-dataset-reviews_20250901.json.gz # 2be129e154505381c77800ca96ea11f09b8db96ddbd2db935c8421cbb4c35a8c
gunzip -k steam_2025_5k-dataset-*.json.gz
```

#### **Advantages**

- ✅ **Immediate Access** - No registration required
- ✅ **Pipeline History** - Collection and processing code retained in `work-logs/`
- ✅ **Quick Testing** - 5K sample perfect for workflow validation
- ✅ **Development History** - Complete work logs and methodology
- ✅ **Version Control** - Full git history and branching

**[💻 Access on GitHub](https://github.com/vintagedon/steam-dataset-2025)**

---

## 🗂️ **3. File Formats & Specifications**

This section provides technical details about file formats, structures, and handling procedures.

### **3.1 CSV Files**

**Standard Format for Immediate pandas/R Usage**

#### **Format Specifications**

- **Encoding:** UTF-8 (supports international game titles)
- **Delimiter:** Comma (`,`)
- **Quote Character:** Double quote (`"`)
- **Line Terminator:** LF (`\n`)
- **Header Row:** Yes (column names included)
- **NULL Representation:** Empty string or explicit "NULL"

#### **Primary CSV Files**

**steam_games.csv** (member of `steam_dataset_2025_csv_package_v1.zip`; the whole ZIP is 320,368,878 bytes; member row counts are stated after package download, not invented here)

```python
import pandas as pd

# Load core dataset
games = pd.read_csv('steam_games.csv')

# Key columns available
print(games.columns)
# ['app_id', 'name', 'release_date', 'release_year', 'type', 
#  'is_free', 'price_usd', 'supports_windows', 'supports_mac',
#  'supports_linux', 'primary_genre', 'developer_count', 
#  'publisher_count', 'has_achievements', 'multiplayer',
#  'metacritic_score', 'positive_reviews', 'negative_reviews',
#  'min_ram_mb', 'rec_ram_mb', ...]
```

**steam_reviews.csv** (member of the CSV package; the packaged database holds 1,048,148 review rows; the 320,368,878-byte figure is the whole ZIP, not this member file)

```python
# Load review data
reviews = pd.read_csv('steam_reviews.csv')

# Review structure
print(reviews.columns)
# ['app_id', 'recommendationid', 'author_steamid', 'timestamp',
#  'voted_up', 'votes_up', 'votes_funny', 'weighted_vote_score',
#  'comment_count', 'steam_purchase', 'received_for_free',
#  'written_during_early_access', 'playtime_at_review', ...]
```

---

### **3.2 Parquet Files**

**Optimized Columnar Format for Big Data Workflows**

#### **Format Advantages**

- ⚡ **Fast Queries** - Columnar storage enables column pruning
- 📦 **Compression** - 2-3x smaller than equivalent CSV
- 🎯 **Schema Preserved** - Data types stored in file
- 🔍 **Predicate Pushdown** - Filter at file level for speed

#### **Usage Example**

```python
import pandas as pd
import pyarrow.parquet as pq

# Read Parquet with column selection
columns = ['app_id', 'name', 'release_year', 'primary_genre', 'price_usd']
games = pd.read_parquet('steam_games.parquet', columns=columns)

# Or filter during read (predicate pushdown)
indie_games = pd.read_parquet(
    'steam_games.parquet',
    filters=[('primary_genre', '=', 'Indie')]
)

# For Apache Spark
df = spark.read.parquet('steam_games.parquet')
df.filter(df.release_year > 2020).groupBy('primary_genre').count().show()
```

---

### **3.3 Vector Embeddings**

**BGE-M3 Semantic Vectors for Content-Based Analysis**

#### **Format Specifications**

- **File Format:** NumPy binary (`.npy`)
- **Dimensions:** 1024 per game
- **Model:** BAAI/bge-m3 (multilingual)
- **Normalization:** L2 normalized for cosine similarity
- **Coverage:** 239,664 applications with embeddings in the packaged database (100% non-null, measured 2026-08-03)

#### **Usage Example**

```python
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load embeddings and metadata
embeddings = np.load('steam_embeddings.npy')
games = pd.read_csv('steam_games.csv')

# Find similar games
query_app_id = 440  # Team Fortress 2
query_idx = games[games['app_id'] == query_app_id].index[0]
query_vector = embeddings[query_idx].reshape(1, -1)

# Calculate similarities
similarities = cosine_similarity(query_vector, embeddings)[0]

# Get top 10 similar games
top_indices = np.argsort(similarities)[-11:-1][::-1]
recommendations = games.iloc[top_indices][['app_id', 'name', 'primary_genre']]
recommendations['similarity'] = similarities[top_indices]

print(recommendations)
```

---

### **3.4 SQL Database Dump**

**Complete PostgreSQL Restoration for Advanced Users**

#### **Contents**

- ✅ **Schema DDL** - All table definitions with constraints
- ✅ **Complete Data** - All 239,664 applications and 1M+ reviews
- ✅ **Vector Extension** - pgvector setup for semantic search
- ✅ **Indexes** - B-tree indexes plus two HNSW vector indexes (no GIN/GiST in the packaged database)
- ✅ **Views** - Analytical views and materialized views

#### **Restoration Procedure**

A verified schema reference for the packaged dump is deferred (see
[schema-provenance.json](release-1.0.1/schema-provenance.json)); the command
shape below is indicative and no restore guarantee is advertised. The dump
itself is `steam_dataset_2025_power_users_dump_v1.zip` (7,204,002,678 bytes).

```bash
# Prerequisites: PostgreSQL 16+ with pgvector extension

# Restore the power-user dump package contents per the package's own README

# Verify against the packaging-time record:
# applications: 239,664 rows (58 columns)
# reviews:      1,048,148 rows (25 columns)
# description_embedding / review_embedding: vector(1024), 100% non-null (2026-08-03 measurement)
```

---

## 📊 **4. Data Quality & Coverage**

Understanding data completeness and quality characteristics for proper analysis planning.

### **4.1 Collection Outcomes (measured)**

Measured 2026-11-13 from the retained raw batches; machine-readable values with
grain and denominators live in [collection-outcomes.json](release-1.0.1/collection-outcomes.json).

| **Metric** | **Value** | **Grain** |
|------------|-----------|-----------|
| **Retained result records** | 262,791 | records across 526 batch files |
| **Successful retrievals** | 239,341 | record-level (91.0766% of result records) |
| **Failed records** | 23,450 | record-level; requested AppID not retained in failure records |
| **Unique successful AppIDs** | 239,183 | distinct applications in the raw corpus |
| **User Reviews (packaged)** | 1,048,148 | bounded sample, up to 100 most recent per covered application |

The record-level fraction is not HTTP request success and not catalog coverage.

### **4.2 Failure Records Context**

The 23,450 failure records do not retain the requested AppID, so failure
causes cannot be attributed per application and HTTP-attempt completeness is
not measurable from the retained corpus. Earlier published failure-cause
breakdowns (delisted/regional/invalid/API-error percentages) had no retained
source and have been removed.

**Filtering Guidance:**

```python
# Filter out NULL critical fields for clean analyses
games_complete = games[games['name'].notna()]

# Note: the packaged database's success flag is true for all loaded rows
# (failed retrievals were never loaded); it cannot select "complete" records.
```

### **4.3 Field Completeness**

Field-level completeness varies by application type and field; missing values
are stored as meaningful NULLs and are never defaulted. A dated field-coverage
measurement (2026-08-03) is summarized in the
[known limitations](limitations.md) and [release 1.0.1 reference](release-1.0.1/known-limitations.md);
the per-category percentage table previously shown here had no retained
source and has been removed.

---

## 🎓 **5. Citation & Academic Use**

Proper attribution for academic publications and research applications.

### **5.1 Required Citation**

**BibTeX Format:**

```bibtex
@dataset{fountain_2025_steam,
  author       = {Fountain, Donald},
  title        = {{The Steam Dataset 2025: A Large-Scale, Multi-Modal 
                   Dataset of the Steam Gaming Platform}},
  month        = oct,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.17266923},
  url          = {https://doi.org/10.5281/zenodo.17266923}
}
```

**APA Format:**

```markdown
Fountain, D. (2025). Steam Dataset 2025: Multi-Modal Gaming Analytics 
Platform (Version 1.0.0) [Data set]. Zenodo. 
https://doi.org/10.5281/zenodo.17266922
```

### **5.2 License Terms**

**Dataset License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

**You Are Free To:**

- ✅ Share - Copy and redistribute in any medium or format
- ✅ Adapt - Remix, transform, and build upon the material
- ✅ Commercial Use - Use for any purpose, including commercial

**Under These Terms:**

- 📝 **Attribution** - Give appropriate credit and link to license
- 🔓 **No Additional Restrictions** - No legal/technical measures limiting permitted uses

---

## 🚀 **6. Quick Start Examples**

Common workflows for getting started with the dataset.

### **6.1 Basic Exploratory Analysis**

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load core dataset
games = pd.read_csv('steam_games.csv')

# Filter to complete records
games = games[games['name'].notna()]

# Basic statistics
print(f"Total games: {len(games)}")
print(f"Free games: {games['is_free'].sum()} ({games['is_free'].sum()/len(games)*100:.1f}%)")
print(f"Windows games: {games['supports_windows'].sum()}")

# Genre distribution
top_genres = games['primary_genre'].value_counts().head(10)
print("\nTop 10 Genres:")
print(top_genres)

# Temporal analysis
games['release_year'] = pd.to_datetime(games['release_date']).dt.year
yearly_releases = games.groupby('release_year').size()

plt.figure(figsize=(12, 6))
yearly_releases.plot(kind='bar')
plt.title('Steam Games Released Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Games')
plt.tight_layout()
plt.show()
```

### **6.2 Semantic Search Application**

```python
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load data
games = pd.read_csv('steam_games.csv')
embeddings = np.load('steam_embeddings.npy')

def find_similar_games(query_app_id, top_n=10):
    """Find games similar to query using semantic embeddings"""
    
    # Get query embedding
    query_idx = games[games['app_id'] == query_app_id].index[0]
    query_vector = embeddings[query_idx].reshape(1, -1)
    
    # Calculate similarities
    similarities = cosine_similarity(query_vector, embeddings)[0]
    
    # Get top N (excluding query itself)
    top_indices = np.argsort(similarities)[-top_n-1:-1][::-1]
    
    # Build results
    results = games.iloc[top_indices][['app_id', 'name', 'primary_genre', 'release_year']]
    results['similarity'] = similarities[top_indices]
    
    return results

# Example: Find games similar to Portal 2
similar = find_similar_games(620)  # Portal 2 app_id
print(similar)
```

### **6.3 Database Queries (PostgreSQL)**

Illustrative queries against a simplified `games`-shaped view of the data;
the packaged schema's verified reference is deferred (see
[schema-provenance.json](release-1.0.1/schema-provenance.json)).

```sql
-- Top publishers by game count
SELECT 
    p.name AS publisher,
    COUNT(DISTINCT gp.game_id) AS game_count,
    AVG(g.price_usd) AS avg_price
FROM publishers p
JOIN game_publishers gp ON p.id = gp.publisher_id
JOIN games g ON gp.game_id = g.id
WHERE g.success = TRUE
GROUP BY p.id, p.name
ORDER BY game_count DESC
LIMIT 10;

-- Genre evolution over time
SELECT 
    EXTRACT(YEAR FROM release_date) AS year,
    primary_genre,
    COUNT(*) AS game_count
FROM games
WHERE success = TRUE 
    AND release_date IS NOT NULL
GROUP BY year, primary_genre
ORDER BY year DESC, game_count DESC;

-- Semantic search using pgvector
SELECT 
    g.app_id,
    g.name,
    g.primary_genre,
    1 - (g.description_embedding <=> query_embedding) AS similarity
FROM games g,
    (SELECT description_embedding AS query_embedding 
     FROM games 
     WHERE app_id = 440) q  -- Team Fortress 2
WHERE g.description_embedding IS NOT NULL
ORDER BY g.description_embedding <=> q.query_embedding
LIMIT 10;
```

---

## 📞 **7. Support & Additional Resources**

### **7.1 Getting Help**

- **🐛 Technical Issues:** [GitHub Issues](https://github.com/vintagedon/steam-dataset-2025/issues)
- **💬 Questions:** [GitHub Discussions](https://github.com/vintagedon/steam-dataset-2025/discussions)
- **📖 Documentation:** [Full Documentation Hub](https://github.com/vintagedon/steam-dataset-2025/tree/main/docs)
- **📓 Notebook Examples:** [Interactive Notebooks](https://github.com/vintagedon/steam-dataset-2025/tree/main/steam-dataset-2025-v1/notebooks)

### **7.2 Related Documentation**

| **Document** | **Purpose** | **Link** |
|--------------|-------------|----------|
| **Dataset Card** | Complete academic documentation | [DATASET_CARD.md](../steam-dataset-2025-v1/DATASET_CARD.md) |
| **Data Dictionary** | Field definitions and schema | [DATA_DICTIONARY.md](../steam-dataset-2025-v1/DATA_DICTIONARY.md) |
| **PostgreSQL Schema** | Database implementation | [postgresql-database-schema.md](postgresql-database-schema.md) |
| **Vector Embeddings** | BGE-M3 methodology | [methodologies/vector-embeddings.md](methodologies/vector-embeddings.md) |
| **Limitations** | Known constraints | [limitations.md](limitations.md) |

---

## 📜 **8. Documentation Metadata**

### **8.1 Change Log**

| **Version** | **Date** | **Changes** | **Author** |
|------------|----------|-------------|------------|
| 1.0 | 2025-09-07 | Initial data access guide | VintageDon |
| 2.0 | 2025-01-06 | Complete rewrite for published dataset with Zenodo DOI | VintageDon |
| 2.1 | 2026-11-13 | Truth patch: official package table with verified bytes, Kaggle published, LFS-correct sample access, measured collection outcomes, removed unsourced failure breakdowns | VintageDon |

### **8.2 Authorship & Collaboration**

**Primary Author:** VintageDon (Donald Fountain)  
**GitHub:** <https://github.com/vintagedon>  
**ORCID:** [0009-0008-7695-4093](https://orcid.org/0009-0008-7695-4093)  
**AI Collaboration:** Claude 3.7 Sonnet (Anthropic) - Documentation structure and technical writing assistance  

**Human Responsibility:** All dataset specifications, access procedures, and technical details are human-verified. AI assistance was used for documentation organization and clarity enhancement.

---

**Document Version:** 2.1 | **Last Updated:** 2026-11-13 | **Status:** Published

*Access the complete dataset at: [https://doi.org/10.5281/zenodo.17266922](https://doi.org/10.5281/zenodo.17266922)*
