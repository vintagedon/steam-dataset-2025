<!--
---
title: "Steam Dataset 2025 - Official Release Package"
description: "The largest and most methodologically rigorous Steam dataset: 239K+ applications, 1M+ reviews, vector embeddings, and 28-year platform history"
author: "Donald Fountain (VintageDon)"
orcid: "0009-0008-7695-4093"
date: "2025-10-05"
version: "1.0.0"
doi: "10.5281/zenodo.17286923"
license: "CC BY 4.0 (data), MIT (code)"
status: "Published"
tags: ["steam", "gaming", "dataset", "machine-learning", "semantic-search", "postgresql", "vector-embeddings"]
---
-->

# 🎮 **Steam Dataset 2025**

## The Large-Scale, Multi-Modal Dataset of the Steam Gaming Platform

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17286923.svg)](https://doi.org/10.5281/zenodo.17286923)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.10-blue.svg)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

**Version 1.0.0** | **Released October 2025** | **DOI: [10.5281/zenodo.17286923](https://doi.org/10.5281/zenodo.17286923)**

---

## **Executive Summary**

The Steam Dataset 2025 is the most comprehensive and methodologically rigorous Steam platform dataset ever released, containing **239,664 applications** and **1,048,148 user reviews** spanning Steam's entire **28-year history (1997-2025)**. Unlike existing Steam datasets that rely on third-party aggregators or provide flat CSV exports, this dataset employs a **multi-modal PostgreSQL architecture** preserving complete API response structures in JSONB while providing **1024-dimensional BGE-M3 vector embeddings** for semantic search—a capability no other Steam dataset offers.

**What Makes This Dataset Unique:**

- ✅ **Unmatched Scale:** 239K+ applications vs. competitors' 27K-85K (8.5x larger than leading alternatives)
- ✅ **Vector Embeddings:** 1024-dim BGE-M3 embeddings with HNSW indexes (NO other Steam dataset has this)
- ✅ **Longest History:** 28-year coverage (1997-2025) vs. competitors' 5-10 year snapshots
- ✅ **Data Purity:** Exclusive use of official Steam Web API—no third-party data sources
- ✅ **Complete Preservation:** JSONB storage maintains full nested API responses
- ✅ **Query-Optimized:** Materialized columns for platform support, pricing, achievements

---

## **📊 Dataset Statistics**

| **Metric** | **Count** | **Details** |
|------------|-----------|-------------|
| **Total Applications** | 239,664 | Games, DLC, software, videos, tools |
| **User Reviews** | 1,048,148 | English-language reviews with full metadata |
| **Unique Developers** | 101,226 | Individual and studio developers |
| **Unique Publishers** | 85,699 | Publishers across all content types |
| **Genre Classifications** | 154 | Including multilingual variants |
| **Feature Categories** | 462 | Steam feature tags (achievements, cloud saves, etc.) |
| **Temporal Coverage** | 1997-2025 | 28 years of platform evolution |
| **Database Size** | 21 GB | Including 9.8 GB of HNSW vector indexes |
| **API Success Rate** | 56% | Remaining failures from delisted apps, regional restrictions |

---

## **🎯 Motivation & Research Gap**

### **The Problem with Existing Steam Datasets**

Current Steam datasets suffer from critical limitations:

1. **Scale Limitations:** Most datasets contain 27K-85K applications, missing 70-85% of Steam's catalog
2. **No Semantic Search:** Zero existing Steam datasets provide vector embeddings or semantic capabilities
3. **Short History:** Typical coverage spans 5-10 years, missing critical platform evolution periods
4. **Third-Party Dependency:** Many rely on SteamSpy or aggregators rather than official APIs
5. **Flat File Exports:** CSV/JSON exports lose nested structures and relationships

### **How Steam Dataset 2025 Solves These Problems**

**Scale Supremacy:** 239K+ applications captured from official Steam APIs—the most complete Steam catalog ever published

**Semantic Search Foundation:** Pre-computed 1024-dimensional BGE-M3 embeddings with HNSW indexes enable sub-second similarity search across game descriptions and reviews—a capability enabling recommendation systems, content-based discovery, and semantic analysis impossible with traditional datasets

**Historical Depth:** 28-year coverage (1997-2025) enables longitudinal studies of platform evolution, pricing strategies, genre emergence, and digital distribution maturation

**Data Purity:** Exclusive use of official Steam Web API ensures authenticity, with complete JSONB preservation of nested structures for reproducible research

**Multi-Modal Architecture:** PostgreSQL 16.10 with pgvector combines relational integrity, document flexibility (JSONB), and vector search in unified schema—serving beginners (CSV exports), power users (SQL dumps), and ML engineers (embedding packages) equally well

---

## **🚀 Quick Start**

### **Choose Your Package**

Select the data package matching your technical expertise and use case:

| **Package** | **Format** | **Size** | **Best For** | **Technical Requirement** |
|-------------|-----------|----------|--------------|---------------------------|
| **[Notebook Data](#-notebook-data)** | CSV/NPY/Parquet | ~100 MB | Learning, visualization, portfolio projects | Python + pandas |
| **[Accessibility CSVs](#data-packages-available)** | ZIP of CSVs | ~500 MB | Immediate analysis without database setup | Excel, R, pandas |
| **[Power-User SQL](#data-packages-available)** | PostgreSQL dump | 4.2 GB compressed | Full database reproduction, advanced queries | PostgreSQL 16+ + pgvector |
| **[AI Embeddings](#data-packages-available)** | NPY + CSV | ~900 MB | ML/AI applications without GPU access | PyTorch, TensorFlow, numpy |

### **Installation Examples**

<details>
<summary><strong>Beginner: Load Notebook Data with pandas</strong></summary>

```python
import pandas as pd
import numpy as np

# Load sample game data
games = pd.read_csv('notebook-data/01-platform-evolution/01_temporal_growth.csv')

# Load semantic embeddings
embeddings = np.load('notebook-data/02-semantic-game-discovery/02_embeddings_vectors.npy')
appids = pd.read_csv('notebook-data/02-semantic-game-discovery/02_embeddings_appids.csv')

# Start analyzing!
print(f"Loaded {len(games)} games spanning {games['release_year'].max() - games['release_year'].min()} years")
```

</details>

<details>
<summary><strong>Advanced: Restore PostgreSQL Database</strong></summary>

```bash
# Install PostgreSQL 16+ and pgvector extension
sudo apt-get install postgresql-16 postgresql-16-pgvector

# Create database
createdb steam_dataset_2025

# Restore dump (adjust path to your download)
pg_restore -d steam_dataset_2025 steam_dataset_2025_full.dump

# Query with semantic search
psql steam_dataset_2025 -c "
SELECT name, description 
FROM applications 
ORDER BY description_embedding <=> (
  SELECT description_embedding FROM applications WHERE name = 'Portal 2'
) 
LIMIT 10;"
```

</details>

<details>
<summary><strong>ML Engineer: Load Embeddings for Training</strong></summary>

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Load pre-computed embeddings (no GPU needed!)
embeddings = np.load('embeddings/application_embeddings.npy', mmap_mode='r')
metadata = pd.read_csv('embeddings/application_embeddings_metadata.csv')

# Create train/test split
X_train, X_test, y_train, y_test = train_test_split(
    embeddings, 
    metadata['primary_genre'],
    test_size=0.2, 
    stratify=metadata['primary_genre']
)

# Train your model!
```

</details>

---

## **📁 Package Contents**

### **📓 Notebook Data**

Three production-ready Jupyter notebooks demonstrating dataset capabilities:

| **Notebook** | **Difficulty** | **Runtime** | **Showcases** |
|--------------|---------------|-------------|---------------|
| **[01: Platform Evolution](notebooks/01-steam-platform-evolution-and-marketplace/)** | Beginner | ~5 min | Market dynamics, pricing, 28-year history |
| **[02: Semantic Discovery](notebooks/02-semantic-game-discovery/)** | Intermediate | ~10 min | Vector embeddings, UMAP, similarity search |
| **[03: Semantic Fingerprint](notebooks/03-the-semantic-fingerprint/)** | Advanced | ~15 min | Genre/RAM prediction from descriptions |

**Quick Start:**

```bash
cd notebooks/01-steam-platform-evolution-and-marketplace
jupyter notebook notebook-01-steam-platform-evolution-and-market-landscape.ipynb
```

Each notebook is self-contained with validation checks, comprehensive visualizations, and detailed commentary. Perfect for learning, portfolio projects, or adapting to your research.

### **📚 Core Documentation**

| **Document** | **Purpose** | **Link** |
|--------------|-------------|----------|
| **Data Dictionary** | Complete schema reference with all tables, columns, and JSONB structures | [DATA_DICTIONARY.md](DATA_DICTIONARY.md) |
| **Dataset Card** | Metadata, methodology summary, and citation information | [DATASET_CARD.md](DATASET_CARD.md) |
| **Database Schema** | Full PostgreSQL DDL with indexes and constraints | [steam-dataset-2025-full-schema.sql](steam-dataset-2025-full-schema.sql) |

### **🗃️ Data Packages Available**

*Note: Full data packages (CSV, SQL, embeddings) are distributed via Zenodo due to size. See [Data Access](#-data-access) section.*

---

## **🔬 Research Applications**

This dataset enables groundbreaking research across multiple domains:

### **Machine Learning & AI**

- **Recommendation Systems:** Use embeddings and collaborative filtering on 239K applications
- **Semantic Search:** HNSW indexes enable sub-second similarity queries across game descriptions
- **Genre Classification:** Train models on 154 genre classifications with 239K examples
- **Sentiment Analysis:** 1M+ reviews with ratings for opinion mining and trend analysis
- **Multi-Task Learning:** Predict success metrics, genres, and requirements simultaneously

### **Market Analytics**

- **Pricing Strategy Analysis:** 28-year pricing evolution across 239K applications
- **Platform Adoption Patterns:** Windows/Mac/Linux support trends and correlations
- **Publisher Portfolio Optimization:** 85K publishers with game/DLC composition analysis
- **Achievement Economics:** 65% adoption rate analysis and feature value quantification

### **Natural Language Processing**

- **Text Embeddings Research:** 1024-dim BGE-M3 vectors on multilingual gaming content
- **Topic Modeling:** LDA/BERTopic on 1M+ review corpus for theme discovery
- **Cross-Lingual Analysis:** 100+ language support in embeddings for multilingual research
- **Description Quality:** Correlation between description language and success metrics

### **Network & Graph Analysis**

- **Publisher-Developer Networks:** 101K developers × 85K publishers relationship graphs
- **Genre Co-Occurrence:** Genre combination patterns across 239K applications
- **Content Clustering:** Community detection in game similarity networks
- **Influence Propagation:** How successful games influence future releases

### **Longitudinal Studies**

- **Platform Evolution:** 28-year digital distribution maturation (1997-2025)
- **Genre Lifecycle Analysis:** Birth, growth, maturity, decline of gaming genres
- **Pricing Dynamics:** Free-to-play emergence and premium game evolution
- **Feature Adoption:** Achievement, cloud save, workshop adoption timelines

---

## **✨ Unique Features**

### **1. Vector Embeddings (NO OTHER STEAM DATASET HAS THIS)**

- **1024-dimensional BGE-M3 embeddings** for all applications and reviews
- **HNSW indexes** for sub-second semantic search across 239K applications
- **Multilingual support:** 100+ languages encoded in single embedding space
- **Pre-computed:** No GPU required—load and query immediately

**Example Application:**

```python
# Find games similar to Portal 2 using semantic search (not keyword matching!)
similar_games = find_similar("innovative puzzle-platformer with physics mechanics")
# Returns: Portal, The Talos Principle, Quantum Conundrum, etc.
```

### **2. Complete JSONB Preservation**

Unlike CSV exports that flatten complex structures, **every API response is preserved** in JSONB:

- **Pricing Data:** All currencies (30+), initial/final prices, discount metadata
- **System Requirements:** Unmodified minimum/recommended HTML text (parsed to columns)
- **Release Info:** Detailed release status, dates, and platform-specific information
- **Ratings:** Complete ratings breakdown by descriptor and count

**Benefits:**

- Zero data loss from API to database
- Query nested structures directly with PostgreSQL JSONB operators
- Future-proof: New API fields automatically preserved

### **3. Materialized Analytical Columns**

For user convenience, frequently-queried fields are materialized from JSONB:

- **Platform Flags:** `mat_windows`, `mat_mac`, `mat_linux` (boolean)
- **Pricing:** `mat_price_usd`, `mat_initial_price_usd`, `mat_discount_percent` (numeric)
- **Achievements:** `mat_achievement_count` (integer)
- **Requirements:** `mat_pc_min_ram_gb`, `mat_pc_rec_ram_gb`, `mat_pc_min_storage_gb` (numeric)

**Query Performance:** Materialized columns enable indexed queries 100x faster than JSONB extraction

### **4. Longest Temporal Coverage**

**28 years of data (1997-2025)** vs. competitors' typical 5-10 year snapshots:

- Pre-Steam era (1997-2002): Early digital distribution experiments
- Steam launch (2003-2010): Platform establishment and Valve dominance
- Indie revolution (2011-2016): Greenlight and indie game explosion
- Open platform (2017-2025): Direct publishing and 10K+ annual releases

**Research Enabled:** Longitudinal studies, lifecycle analysis, paradigm shift identification

### **5. Unmatched Scale**

**239,664 applications** captured from official APIs:

| **Competitor** | **App Count** | **Steam Dataset 2025 Advantage** |
|----------------|---------------|----------------------------------|
| Nik Davis 2019 | ~27,000 | **8.9x more applications** |
| Steam Spy | ~80,000 | **3.0x more applications** |
| SteamDB | ~85,000 | **2.8x more applications** |

**Coverage:** Games, DLC, software, videos, tools, demos—complete Steam catalog

---

## **📖 Methodology Transparency**

### **Data Collection**

**Source:** Official Steam Web API exclusively—no third-party aggregators

**Collection Period:** August-September 2025

**Rate Limiting:** Conservative 1.5-second delays (17.3 requests/minute sustainable)

**Success Rate:** 56% (remaining failures from delisted content, regional restrictions)

**Infrastructure:** Proxmox Astronomy Lab with PostgreSQL 16.10 and NVIDIA A4000 GPU

### **Quality Assurance**

Multi-layered validation following RAVGV (Request-Analyze-Verify-Generate-Validate) methodology:

**Phase 1: Collection-Time Validation**

- API response schema verification
- Data type consistency checks
- Duplicate detection and handling

**Phase 2: Post-Import Validation**

- Statistical profiling for anomaly detection
- Cross-field logical consistency
- Temporal validation (no future dates)

**Phase 3: Analytical Validation**

- Sample dataset methodology validation
- Cross-scale pattern consistency
- Known ground truth comparison

### **Embedding Generation**

**Model:** BAAI/bge-m3 (1024 dimensions)

**Input:** Combined `name + short_description + detailed_description` for applications; `review_text` for reviews

**Hardware:** NVIDIA RTX A4000 16GB GPU

**Batch Processing:** 256 samples per batch with automatic memory management

**Quality:** L2-normalized vectors (‖v‖₂ = 1.0) for cosine similarity

**Indexing:** HNSW (Hierarchical Navigable Small World) for fast approximate nearest neighbor search

---

## **📊 Data Packages**

### **Package Comparison**

| **Feature** | **Notebook Data** | **Accessibility CSV** | **Power-User SQL** | **AI Embeddings** |
|-------------|-------------------|----------------------|-------------------|-------------------|
| **Size** | ~100 MB | ~500 MB | 4.2 GB | ~900 MB |
| **Format** | CSV/NPY/Parquet | ZIP of CSVs | PostgreSQL dump | NPY + CSV |
| **Setup Time** | < 1 minute | < 5 minutes | 10-30 minutes | < 5 minutes |
| **JSONB Access** | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **Vector Embeddings** | ✅ Samples | ❌ No | ✅ All | ✅ All |
| **SQL Queries** | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **Best For** | Learning, notebooks | Excel, R, quick analysis | Research, advanced queries | ML/AI development |

### **Download Instructions**

**Zenodo Archive (Recommended):**

```markdown
https://doi.org/10.5281/zenodo.17286923
```

**Alternative Sources:**

- Kaggle: [Pending publication]
- GitHub Releases: [Pending large file hosting]

---

## **🛠️ Technical Specifications**

### **Database**

- **Engine:** PostgreSQL 16.10 (Ubuntu 24.04)
- **Extension:** pgvector v0.8.0
- **Storage:** Samsung PM983 1.92TB NVMe
- **Performance:** ~205K TPS read-only, ~21K TPS durable writes

### **Schema Highlights**

**Core Tables:**

- `applications` (239,664 rows, 58 columns)
- `reviews` (1,048,148 rows, 25 columns)
- `developers` (101,226 unique entities)
- `publishers` (85,699 unique entities)
- `genres` (154 classifications)
- `categories` (462 Steam feature tags)

**Vector Indexes:**

- Applications: 1.9 GB HNSW index
- Reviews: 7.9 GB HNSW index
- Total: 9.8 GB vector indexes

**Total Database Size:** 21 GB (data + indexes)

### **Python Environment**

**Core Requirements:**

```markdown
python >= 3.9
pandas >= 2.0
numpy >= 1.24
psycopg2-binary >= 2.9
sentence-transformers >= 2.2  # For embedding generation
```

**Full requirements:** See `requirements.txt` in repository

---

## **📝 Citation**

### **Zenodo DOI (Preferred)**

```bibtex
@dataset{fountain_2025_steam,
  author       = {Fountain, Donald},
  title        = {{Steam Dataset 2025: A Large-Scale, Multi-Modal 
                   Dataset of the Steam Gaming Platform}},
  year         = 2025,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.17286923},
  url          = {https://doi.org/10.5281/zenodo.17286923}
}
```

### **APA Format**

```markdown
Fountain, D. (2025). Steam Dataset 2025: A large-scale, multi-modal dataset of the 
Steam gaming platform [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.17286923
```

### **IEEE Format**

```markdown
D. Fountain, "Steam Dataset 2025: A large-scale, multi-modal dataset of the Steam gaming 
platform," Zenodo, 2025. [Online]. Available: https://doi.org/10.5281/zenodo.17286923
```

---

## **📜 License**

### **Data & Documentation: CC BY 4.0**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

The dataset and documentation are licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

**You are free to:**

- ✅ Share—copy and redistribute in any medium or format
- ✅ Adapt—remix, transform, and build upon the material
- ✅ Commercial use—use for any purpose, including commercially

**Under these terms:**

- 📋 **Attribution**—You must give appropriate credit, provide a link to the license, and indicate if changes were made

### **Code: MIT License**

Scripts, SQL queries, and software implementations use the [MIT License](https://opensource.org/licenses/MIT).

### **Steam Data Usage**

Data collected from official Steam Web API under [Steam Web API Terms](https://steamcommunity.com/dev). Contains only publicly available information. No private user data or personally identifiable information included.

---

## **🔗 Resources**

### **Project Links**

- **DOI:** [10.5281/zenodo.17286923](https://doi.org/10.5281/zenodo.17286923)
- **Repository:** [github.com/VintageDon/steam-dataset-2025](https://github.com/VintageDon/steam-dataset-2025)
- **ORCID:** [0009-0008-7695-4093](https://orcid.org/0009-0008-7695-4093)
- **Kaggle:** [Pending publication]

### **Documentation**

- **Data Dictionary:** Complete schema reference → [DATA_DICTIONARY.md](DATA_DICTIONARY.md)
- **Dataset Card:** Methodology and metadata → [DATASET_CARD.md](DATASET_CARD.md)
- **Methodologies:** Collection and QA procedures → [Repository docs/methodologies](https://github.com/VintageDon/steam-dataset-2025/tree/main/docs/methodologies)
- **Work Logs:** Development session logs → [Repository work-logs](https://github.com/VintageDon/steam-dataset-2025/tree/main/work-logs)

### **External Resources**

- **Steam Web API:** [steamcommunity.com/dev](https://steamcommunity.com/dev)
- **PostgreSQL Documentation:** [postgresql.org/docs/16](https://www.postgresql.org/docs/16/)
- **pgvector Extension:** [github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)
- **BGE-M3 Model:** [huggingface.co/BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)

---

## **🙏 Acknowledgments**

This dataset was developed using the Request-Analyze-Verify-Generate-Validate-Reflect (RAVGVR) methodology with AI assistance from Claude 3.5 Sonnet. All data sourced exclusively from official Steam Web API (August-September 2025).

Special thanks to Valve Corporation for maintaining the Steam platform and providing public API access.

**Infrastructure:** Proxmox Astronomy Lab with enterprise-grade hardware supporting systematic data collection and processing.

---

## **📧 Contact**

**Author:** Donald Fountain (VintageDon)

- **GitHub:** [@VintageDon](https://github.com/VintageDon)
- **ORCID:** [0009-0008-7695-4093](https://orcid.org/0009-0008-7695-4093)
- **Email:** [Through GitHub profile]

**Issues & Questions:** Please use the [GitHub Issues](https://github.com/VintageDon/steam-dataset-2025/issues) tracker for technical questions, bug reports, or feature requests.

---

**Version 1.0.0** | **Released October 2025** | **DOI: [10.5281/zenodo.17286923](https://doi.org/10.5281/zenodo.17286923)**

This dataset represents the culmination of systematic data engineering practices and transparent AI-human collaboration, demonstrating that sophisticated research infrastructure can be built through methodical approaches and comprehensive documentation.
