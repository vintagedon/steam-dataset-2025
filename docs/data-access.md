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

This guide provides comprehensive information for accessing Steam Dataset 2025 across multiple platforms. The complete dataset (239,664 applications, 1M+ reviews) is now available through Zenodo (with persistent DOI), Kaggle (with interactive notebooks), and GitHub (with sample data for testing).

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

Steam Dataset 2025 is available through three complementary channels: **Zenodo** for permanent academic hosting with DOI citation (recommended for research), **Kaggle** for interactive notebooks and community engagement (coming soon), and **GitHub** for 5K sample data and code repository access (perfect for testing).

---

## 📦 **2. Dataset Access Options**

This section outlines all available access methods, helping you choose the right platform for your needs.

### **2.1 Zenodo: Official Academic Release (Recommended for Research)**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17286923.svg)](https://doi.org/10.5281/zenodo.17286923)

**Best For:** Academic research, publications, permanent archival access  
**Status:** ✅ Published and Available

#### **Dataset Package Contents**

| **File** | **Format** | **Size** | **Description** |
|----------|------------|----------|-----------------|
| **steam_games.csv** | CSV | ~85MB | Core game metadata with materialized columns |
| **steam_reviews.csv** | CSV | ~320MB | 1,048,148 user reviews with metadata |
| **steam_genres.csv** | CSV | ~450KB | Genre classifications and mappings |
| **steam_categories.csv** | CSV | ~380KB | Category assignments |
| **steam_developers.csv** | CSV | ~1.2MB | Developer portfolio data |
| **steam_publishers.csv** | CSV | ~950KB | Publisher portfolio data |
| **steam_games.parquet** | Parquet | ~45MB | Columnar format for big data workflows |
| **steam_embeddings.npy** | NumPy | ~520MB | BGE-M3 vector embeddings (1024-dim) |
| **steam_dataset_2025.sql.gz** | SQL | ~2.8GB | Complete PostgreSQL database dump |
| **documentation/** | Various | ~15MB | Data dictionary, dataset card, notebooks |

#### **Download Procedure**

```bash
# Option 1: Direct browser download
# Visit: https://doi.org/10.5281/zenodo.17286923
# Click "Download" on the files you need

# Option 2: Command line download (requires zenodo_get)
pip install zenodo-get
zenodo_get 10.5281/zenodo.17286923

# Option 3: wget download (replace with actual file URLs from Zenodo)
wget https://zenodo.org/record/17286923/files/steam_games.csv
wget https://zenodo.org/record/17286923/files/steam_reviews.csv
```

#### **Advantages**

- ✅ **Permanent DOI** for academic citation
- ✅ **Version Controlled** releases with change tracking
- ✅ **Academic Standard** hosting for research credibility
- ✅ **Long-Term Preservation** guaranteed by Zenodo/CERN
- ✅ **Complete Package** including documentation and notebooks

**[📥 Access on Zenodo](https://doi.org/10.5281/zenodo.17286923)**

---

### **2.2 Kaggle: Interactive Analysis Platform (Coming Soon)**

**Best For:** Interactive exploration, community discussions, GPU-accelerated notebooks  
**Status:** 🔄 Publication Pending

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

#### **Access Procedure (When Available)**

1. Visit Kaggle dataset page: `https://kaggle.com/datasets/vintagedon/steam-dataset-2025`
2. Click "New Notebook" for instant Jupyter environment
3. Or download CSV files directly from dataset page
4. Join discussions and competitions

**Advantages:**

- ✅ **No Download Required** - Work directly in browser
- ✅ **Instant Environment** - Pre-configured with all libraries
- ✅ **Community Features** - Discussions, competitions, forking
- ✅ **Free Resources** - GPU access and storage included

**[📊 Explore on Kaggle](#)** *(Link available upon publication)*

---

### **2.3 GitHub: Sample Dataset & Code Repository**

**Best For:** Testing workflows, exploring methodology, accessing ETL code  
**Status:** ✅ Available Now

#### **GitHub Contents**

| **Component** | **Location** | **Size** | **Description** |
|---------------|--------------|----------|-----------------|
| **5K Sample Games** | `data/01_raw/` | ~102MB | Representative sample across genres/eras |
| **5K Sample Reviews** | `data/01_raw/` | ~45MB | User reviews for sample games |
| **ETL Scripts** | `scripts/` | N/A | Complete pipeline code (12 phases) |
| **Documentation** | `docs/` | N/A | Technical specifications and guides |
| **Notebooks** | `steam-dataset-2025-v1/notebooks/` | N/A | 3 analysis examples with PDFs |
| **Work Logs** | `work-logs/` | N/A | Development history (10 phases) |

#### **Access Procedure**

```bash
# Option 1: Clone complete repository
git clone https://github.com/vintagedon/steam-dataset-2025.git
cd steam-dataset-2025

# Option 2: Download specific sample files
wget https://github.com/vintagedon/steam-dataset-2025/raw/main/data/01_raw/steam_2025_5k-dataset-games_20250831.json.gz
wget https://github.com/vintagedon/steam-dataset-2025/raw/main/data/01_raw/steam_2025_5k-dataset-reviews_20250901.json.gz

# Decompress sample data
gunzip data/01_raw/*.gz

# Or use GitHub's "Download ZIP" for easy access
```

#### **Advantages**

- ✅ **Immediate Access** - No registration required
- ✅ **Code Repository** - All ETL and processing scripts
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

**steam_games.csv** (134,212 games, ~85MB)

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

**steam_reviews.csv** (1,048,148 reviews, ~320MB)

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
- **Coverage:** 134,189 games with embeddings

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
- ✅ **Indexes** - Optimized B-tree, GiST, and GIN indexes
- ✅ **Views** - Analytical views and materialized views

#### **Restoration Procedure**

```bash
# Prerequisites: PostgreSQL 16+ with pgvector extension

# Create database
createdb steam_dataset_2025

# Restore from compressed dump
gunzip -c steam_dataset_2025.sql.gz | psql steam_dataset_2025

# Verify restoration
psql steam_dataset_2025 -c "SELECT COUNT(*) FROM games;"
# Should return: 239664

# Test vector search capability
psql steam_dataset_2025 -c "SELECT COUNT(*) FROM games WHERE description_embedding IS NOT NULL;"
# Should return: 134189
```

---

## 📊 **4. Data Quality & Coverage**

Understanding data completeness and quality characteristics for proper analysis planning.

### **4.1 Collection Statistics**

| **Metric** | **Value** | **Percentage** |
|------------|-----------|----------------|
| **Total Applications Processed** | 239,664 | 100% |
| **Successful Metadata Retrieval** | 134,212 | 56.0% |
| **Failed Retrievals** | 105,452 | 44.0% |
| **Vector Embeddings Generated** | 134,189 | 99.98% of successful |
| **User Reviews Collected** | 1,048,148 | N/A |

### **4.2 Success Rate Context**

**Why 56% Success Rate?**

The 44% "failure" rate represents expected patterns, not data quality issues:

- **Delisted Games** (19.0%) - Games removed from Steam store
- **Regional Restrictions** (11.7%) - Content not available in collection region
- **Invalid App IDs** (7.9%) - Deprecated or placeholder IDs
- **API Errors** (5.5%) - Temporary Steam API issues

**Filtering Guidance:**

```python
# Most analyses should filter to successful records
games_complete = games[games['success'] == True]

# Or equivalently, filter out NULL critical fields
games_complete = games[games['name'].notna()]
```

### **4.3 Field Completeness**

For successfully retrieved games (134,212 records):

| **Field Category** | **Completeness** | **Notes** |
|-------------------|------------------|-----------|
| **Basic Metadata** | 99.8% | name, type, app_id nearly universal |
| **Descriptions** | 94.2% | detailed_description most complete |
| **Media Assets** | 87.5% | header_image highly available |
| **Pricing** | 78.1% | Free games lack price_overview |
| **PC Requirements** | 65.3% | Parsed from HTML when available |
| **Release Date** | 98.6% | Highly reliable field |
| **Vector Embeddings** | 99.98% | Generated from descriptions |

---

## 🎓 **5. Citation & Academic Use**

Proper attribution for academic publications and research applications.

### **5.1 Required Citation**

**BibTeX Format:**

```bibtex
@dataset{fountain_2025_steam,
  author       = {Fountain, Donald},
  title        = {{Steam Dataset 2025: Multi-Modal Gaming 
                   Analytics Platform}},
  month        = jan,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.17286923},
  url          = {https://doi.org/10.5281/zenodo.17286923}
}
```

**APA Format:**

```markdown
Fountain, D. (2025). Steam Dataset 2025: Multi-Modal Gaming Analytics 
Platform (Version 1.0.0) [Data set]. Zenodo. 
https://doi.org/10.5281/zenodo.17286923
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

### **8.2 Authorship & Collaboration**

**Primary Author:** VintageDon (Donald Fountain)  
**GitHub:** <https://github.com/vintagedon>  
**ORCID:** [0009-0008-7695-4093](https://orcid.org/0009-0008-7695-4093)  
**AI Collaboration:** Claude 3.7 Sonnet (Anthropic) - Documentation structure and technical writing assistance  

**Human Responsibility:** All dataset specifications, access procedures, and technical details are human-verified. AI assistance was used for documentation organization and clarity enhancement.

---

**Document Version:** 2.0 | **Last Updated:** January 6, 2025 | **Status:** Published

*Access the complete dataset at: [https://doi.org/10.5281/zenodo.17286923](https://doi.org/10.5281/zenodo.17286923)*
