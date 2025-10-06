# 📊 **Analytics Data Directory**

This directory contains final analytical datasets ready for distribution and research applications. Data from all processing stages has been consolidated into optimized formats including CSV exports, Parquet files for big data workflows, and SQL dumps for database restoration. These production-ready datasets power the Steam Dataset 2025 release on Kaggle and Zenodo.

## **Overview**

The analytics data tier represents the final stage of the Steam Dataset 2025 pipeline. All validation, enrichment, and materialization work converges here into curated datasets that balance completeness with usability. Export packages are optimized for different use cases: CSV files for pandas/R workflows, Parquet for Apache Spark and big data systems, and SQL dumps for researchers who need the full relational schema with vector embeddings intact.

---

## 📁 **Directory Contents**

This section documents production dataset exports and their intended applications.

### **CSV Export Packages**

| **File** | **Records** | **Size** | **Purpose** |
|----------|------------|----------|-------------|
| **steam_games.csv** | 134,212 | ~85MB | Core game metadata with materialized columns |
| **steam_reviews.csv** | 1,048,148 | ~320MB | User review data with recommendations |
| **steam_genres.csv** | 15,342 | ~450KB | Genre classifications and mappings |
| **steam_categories.csv** | 12,889 | ~380KB | Category assignments and definitions |
| **steam_developers.csv** | 38,721 | ~1.2MB | Developer portfolio data |
| **steam_publishers.csv** | 29,456 | ~950KB | Publisher portfolio data |

### **Parquet Files**

| **File** | **Records** | **Size** | **Purpose** |
|----------|------------|----------|-------------|
| **steam_games.parquet** | 134,212 | ~45MB | Columnar format for big data workflows |
| **steam_reviews.parquet** | 1,048,148 | ~180MB | Review data optimized for Spark/Dask |
| **steam_embeddings.parquet** | 134,189 | ~520MB | Vector embeddings with metadata |

### **SQL Dumps**

| **File** | **Size** | **Purpose** |
|----------|----------|-------------|
| **steam_dataset_2025_schema.sql** | ~125KB | DDL for database recreation |
| **steam_dataset_2025_data.sql.gz** | ~2.8GB | Complete data dump with embeddings |
| **steam_dataset_2025_indexes.sql** | ~18KB | Index definitions for performance |

---

## 🗂️ **Repository Structure**

Visual representation of analytics data organization:

```markdown
data/04_analytics/
├── 📦 csv-exports/
│   ├── steam_games.csv
│   ├── steam_reviews.csv
│   ├── steam_genres.csv
│   ├── steam_categories.csv
│   ├── steam_developers.csv
│   └── steam_publishers.csv
├── 🏛️ parquet-exports/
│   ├── steam_games.parquet
│   ├── steam_reviews.parquet
│   └── steam_embeddings.parquet
├── 💾 sql-dumps/
│   ├── steam_dataset_2025_schema.sql
│   ├── steam_dataset_2025_data.sql.gz
│   └── steam_dataset_2025_indexes.sql
├── 📊 notebook-data/
│   ├── 01-platform-evolution/
│   ├── 02-semantic-discovery/
│   └── 03-semantic-fingerprint/
└── 📄 README.md                              # This file
```

### **Navigation Guide:**

- **CSV Exports**: Standard format for immediate pandas/R/Excel usage
- **Parquet Files**: Optimized for distributed computing frameworks
- **SQL Dumps**: Complete database restoration with vector support
- **Notebook Data**: Pre-exported datasets for Jupyter notebook examples

---

## 🔗 **Related Categories**

This section connects analytics exports to source data and documentation.

| **Category** | **Relationship** | **Documentation** |
|--------------|------------------|-------------------|
| **[Enriched Data](../03_enriched/README.md)** | Source for final exports | [03_enriched/README.md](../03_enriched/README.md) |
| **[Notebooks](../../notebooks/README.md)** | Analysis examples using these exports | [notebooks/README.md](../../notebooks/README.md) |
| **[Dataset Documentation](../../steam-dataset-2025-v1/)** | Data dictionary and dataset card | [steam-dataset-2025-v1/README.md](../../steam-dataset-2025-v1/README.md) |
| **[Export Scripts](../../scripts/11-packaging-the-release/)** | Generation scripts for exports | [scripts/11-packaging-the-release/README.md](../../scripts/11-packaging-the-release/README.md) |

---

## 🚀 **Getting Started**

This section provides guidance for working with analytical datasets.

### **CSV Usage Patterns**

Load and analyze core game data:

```python
import pandas as pd

# Load primary datasets
games = pd.read_csv('steam_games.csv')
reviews = pd.read_csv('steam_reviews.csv')
genres = pd.read_csv('steam_genres.csv')

# Basic analysis
print(f"Total games: {len(games)}")
print(f"Total reviews: {len(reviews)}")
print(f"Unique genres: {len(genres['genre'].unique())}")

# Filter for Windows games
windows_games = games[games['supports_windows'] == True]
print(f"Windows games: {len(windows_games)} ({len(windows_games)/len(games)*100:.1f}%)")

# Join operations
games_with_genres = games.merge(genres, left_on='app_id', right_on='app_id')
```

### **Parquet for Big Data**

Use columnar format for efficient large-scale analysis:

```python
import pyarrow.parquet as pq
import pandas as pd

# Read Parquet with column selection
columns = ['app_id', 'name', 'release_year', 'primary_genre', 'price_usd']
games = pd.read_parquet('steam_games.parquet', columns=columns)

# Efficient filtering with predicate pushdown
indie_games = pd.read_parquet(
    'steam_games.parquet',
    filters=[('primary_genre', '=', 'Indie')]
)

# Load embeddings for semantic analysis
embeddings_table = pq.read_table('steam_embeddings.parquet')
embeddings_df = embeddings_table.to_pandas()
```

### **SQL Database Restoration**

Restore complete PostgreSQL database:

```bash
# Create database
createdb steam_dataset_2025

# Restore schema
psql steam_dataset_2025 < steam_dataset_2025_schema.sql

# Load data
gunzip -c steam_dataset_2025_data.sql.gz | psql steam_dataset_2025

# Create indexes
psql steam_dataset_2025 < steam_dataset_2025_indexes.sql

# Verify installation
psql steam_dataset_2025 -c "SELECT COUNT(*) FROM games;"
```

---

## 📚 **Technical Documentation**

This section provides detailed specifications for analytical export formats.

### **CSV Export Specifications**

**Encoding**: UTF-8  
**Delimiter**: Comma (,)  
**Quote Character**: Double quote (")  
**Line Terminator**: LF (\\n)  
**Header Row**: Yes (column names)  
**NULL Representation**: Empty string or explicit "NULL"  
**Date Format**: ISO 8601 (YYYY-MM-DD)  
**Boolean Format**: TRUE/FALSE strings  

### **Column Definitions - steam_games.csv**

Key columns in the primary export file:

| **Column** | **Type** | **Description** |
|------------|----------|-----------------|
| **app_id** | INTEGER | Unique Steam application identifier |
| **name** | TEXT | Game title |
| **release_date** | DATE | Initial release date |
| **release_year** | INTEGER | Extracted year for temporal analysis |
| **type** | TEXT | Application type (game, dlc, software) |
| **is_free** | BOOLEAN | Free-to-play indicator |
| **price_usd** | DECIMAL | USD price (NULL for free games) |
| **supports_windows** | BOOLEAN | Windows platform support |
| **supports_mac** | BOOLEAN | macOS platform support |
| **supports_linux** | BOOLEAN | Linux platform support |
| **primary_genre** | TEXT | Primary genre classification |
| **developer_count** | INTEGER | Number of developers |
| **publisher_count** | INTEGER | Number of publishers |
| **has_achievements** | BOOLEAN | Steam achievements support |
| **multiplayer** | BOOLEAN | Multiplayer capability |
| **metacritic_score** | INTEGER | Metacritic rating (NULL if not rated) |
| **positive_reviews** | INTEGER | Count of positive user reviews |
| **negative_reviews** | INTEGER | Count of negative user reviews |
| **min_ram_mb** | INTEGER | Minimum RAM requirement (MB) |
| **rec_ram_mb** | INTEGER | Recommended RAM requirement (MB) |

### **Parquet Schema**

Parquet files use Apache Arrow schema definitions:

```markdown
steam_games.parquet:
  app_id: int32
  name: string
  release_date: date32
  release_year: int16
  type: string (dictionary encoded)
  is_free: bool
  price_usd: decimal(10,2)
  supports_windows: bool
  supports_mac: bool
  supports_linux: bool
  primary_genre: string (dictionary encoded)
  ...

steam_embeddings.parquet:
  app_id: int32
  embedding: fixed_size_list<float>[1024]
  embedding_norm: float
  description_length: int32
```

### **SQL Dump Structure**

Database dump includes:

1. **Schema DDL**: Table definitions, custom types, extensions
2. **Data**: COPY statements for bulk loading
3. **Constraints**: Primary keys, foreign keys, check constraints
4. **Indexes**: B-tree, GiST (for vectors), GIN (for JSONB)
5. **Views**: Analytical views and materialized views
6. **Functions**: Stored procedures for common operations

---

## 🎯 **Use Cases**

This section identifies analytical applications for export packages.

### **Kaggle Competition Setup**

CSV exports enable immediate Kaggle notebook usage:

- **No Database Required**: Direct pandas loading
- **Version Control**: Track dataset versions across competitions
- **Collaboration**: Easy sharing and forking
- **Accessibility**: Works in all Kaggle environments

### **Apache Spark Workflows**

Parquet files optimize distributed computing:

- **Column Pruning**: Read only needed columns
- **Predicate Pushdown**: Filter at file level
- **Compression**: Efficient storage and network transfer
- **Schema Evolution**: Handle schema changes gracefully

### **Research Reproducibility**

SQL dumps ensure exact database recreation:

- **Complete Schema**: Includes extensions, indexes, views
- **Vector Embeddings**: pgvector data preserved
- **JSONB Structures**: Original nested data intact
- **Referential Integrity**: All foreign keys maintained

### **Custom Data Pipelines**

Mix formats for optimal workflows:

- **Exploration**: Start with CSV for quick pandas analysis
- **Production**: Move to Parquet for performance
- **Advanced Features**: Restore SQL for vector search and graph queries

---

## 🔍 **Quality Assurance**

This section documents export validation and quality checks.

### **Export Validation**

All exports undergo these quality checks:

```markdown
✓ Row Count Match:        Database vs Export record counts identical
✓ Schema Validation:      Column types match source definitions
✓ NULL Handling:          Proper NULL representation in CSV
✓ Data Integrity:         Foreign key relationships preserved
✓ Encoding:               UTF-8 encoding verified
✓ Completeness:           No truncated records
✓ File Integrity:         Hash checksums generated
```

### **CSV Validation Report**

```markdown
steam_games.csv:
  Records Exported:       134,212
  Database Records:       134,212
  Match:                  ✓ 100%
  
  Columns Exported:       45
  Schema Columns:         45
  Match:                  ✓ 100%
  
  NULL Values:            12,834 (various optional fields)
  Invalid Values:         0
  Encoding Issues:        0
```

### **Parquet Validation**

```markdown
steam_games.parquet:
  Records:                134,212
  Compressed Size:        45.2 MB
  Uncompressed:           127.8 MB
  Compression Ratio:      2.83:1
  
  Schema Valid:           ✓
  No Null Violations:     ✓
  Dictionary Encoding:    ✓ (type, primary_genre)
  Statistics Present:     ✓ (all columns)
```

### **SQL Dump Validation**

```markdown
Restoration Test:
  Create Database:        ✓
  Schema Load:            ✓ (125 KB)
  Data Load:              ✓ (2.8 GB compressed)
  Index Creation:         ✓ (18 KB)
  Foreign Keys:           ✓ (all validated)
  Vector Extension:       ✓ (pgvector loaded)
  
  Record Counts:
    games:                134,212 ✓
    reviews:              1,048,148 ✓
    genres:               15,342 ✓
    categories:           12,889 ✓
    developers:           38,721 ✓
    publishers:           29,456 ✓
```

---

## 🛠️ **Export Generation**

This section describes how analytical datasets are created.

### **CSV Export Pipeline**

1. **Query Execution**: Extract data with materialized columns
2. **Type Conversion**: Convert PostgreSQL types to CSV-compatible formats
3. **NULL Handling**: Map NULL to empty string or explicit "NULL"
4. **Encoding**: Ensure UTF-8 encoding for international content
5. **Compression**: Optional gzip compression for large files
6. **Validation**: Compare row counts and sample validation
7. **Checksums**: Generate SHA-256 hashes for integrity verification

### **Parquet Export Process**

1. **Schema Definition**: Map PostgreSQL to Arrow types
2. **Batch Reading**: Process data in memory-efficient batches
3. **Dictionary Encoding**: Apply to categorical columns
4. **Compression**: Use Snappy compression algorithm
5. **Statistics**: Generate column statistics for query optimization
6. **Validation**: Verify schema and record counts

### **SQL Dump Creation**

1. **Schema Export**: pg_dump with schema-only flag
2. **Data Export**: pg_dump with data-only flag in COPY format
3. **Index Export**: Separate index definitions for rebuild
4. **Compression**: Gzip compression for data section
5. **Validation**: Restore to test database and verify

---

## 📖 **References**

This section links to related documentation and resources.

### **Internal Documentation**

| **Document** | **Relevance** | **Link** |
|--------------|---------------|----------|
| **Data Dictionary** | Complete field definitions | [/steam-dataset-2025-v1/DATA_DICTIONARY.md](../../steam-dataset-2025-v1/DATA_DICTIONARY.md) |
| **Dataset Card** | Methodology and citation | [/steam-dataset-2025-v1/DATASET_CARD.md](../../steam-dataset-2025-v1/DATASET_CARD.md) |
| **Notebook Examples** | Analysis workflows using exports | [/notebooks/README.md](../../notebooks/README.md) |

### **Export Scripts**

| **Script** | **Purpose** | **Documentation** |
|------------|-------------|-------------------|
| **generate-csv-package.py** | CSV export generation | [scripts/11-packaging-the-release/README.md](../../scripts/11-packaging-the-release/README.md) |
| **generate-sql-dump.py** | Database dump creation | [scripts/11-packaging-the-release/README.md](../../scripts/11-packaging-the-release/README.md) |
| **export-parquet-notebook-03.py** | Parquet file generation | [scripts/12-notebook-generation/README.md](../../scripts/12-notebook-generation/README.md) |

### **External Resources**

| **Resource** | **Description** | **Link** |
|--------------|-----------------|----------|
| **Apache Parquet** | Columnar storage format | <https://parquet.apache.org/> |
| **PostgreSQL pg_dump** | Backup and export utility | <https://www.postgresql.org/docs/current/app-pgdump.html> |
| **pandas DataFrame** | CSV loading and analysis | <https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html> |

---

## 📜 **Documentation Metadata**

### **Change Log**

| **Version** | **Date** | **Changes** | **Author** |
|------------|----------|-------------|------------|
| 1.0 | 2025-01-06 | Initial documentation for analytics data tier | VintageDon |

### **Authorship & Collaboration**

**Primary Author:** VintageDon (Donald Fountain)  
**GitHub:** <https://github.com/vintagedon>  
**AI Collaboration:** Claude 3.7 Sonnet (Anthropic) - Documentation structure and technical writing assistance  

**Human Responsibility:** All export specifications, validation criteria, and quality standards are human-defined. AI assistance was used for documentation organization and clarity enhancement.

---

**Document Information**

| **Field** | **Value** |
|-----------|-----------|
| **Author** | VintageDon - <https://github.com/vintagedon> |
| **Created** | 2025-01-06 |
| **Last Updated** | 2025-01-06 |
| **Version** | 1.0 |

---
Tags: analytics-data, csv-exports, parquet, sql-dumps, dataset-distribution, kaggle, zenodo
