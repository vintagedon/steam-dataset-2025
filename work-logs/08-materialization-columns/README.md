# ⚡ **Enriched Data Directory**

This directory contains processed Steam data enhanced with vector embeddings, derived features, and semantic analysis capabilities. Game descriptions have been transformed into 1024-dimensional embeddings using the BGE-M3 model, enabling semantic search and similarity analysis beyond traditional keyword matching.

## **Overview**

The enriched data tier represents advanced feature engineering applied to validated Steam application data. Text descriptions are converted to dense vector representations that capture semantic meaning, allowing researchers to explore conceptual relationships between games regardless of exact terminology matches. This tier also includes derived analytical features extracted from JSONB structures, providing query-optimized access to frequently analyzed attributes without repeated parsing overhead.

---

## 📁 **Directory Contents**

This section documents enriched data artifacts and their analytical applications.

### **Vector Embedding Files**

| **File Pattern** | **Format** | **Purpose** |
|------------------|------------|-------------|
| **embeddings_YYYYMMDD.npy** | NumPy Binary | Dense 1024-dimensional vectors for all games |
| **embedding_metadata_YYYYMMDD.json** | JSON | app_id mappings and embedding generation metadata |
| **embedding_validation_YYYYMMDD.md** | Markdown | Quality metrics and validation results |

### **Derived Feature Files**

| **File Pattern** | **Format** | **Purpose** |
|------------------|------------|-------------|
| **materialized_features_YYYYMMDD.csv** | CSV | Extracted JSONB fields as flat columns |
| **platform_support_YYYYMMDD.csv** | CSV | Windows/Mac/Linux support indicators |
| **requirements_parsed_YYYYMMDD.csv** | CSV | Hardware requirements as structured data |

---

## 🗂️ **Repository Structure**

Visual representation of enriched data organization:

```markdown
data/03_enriched/
├── 🧠 embeddings_20250901.npy               # BGE-M3 vectors (1024-dim)
├── 📋 embedding_metadata_20250901.json      # Vector generation metadata
├── 📊 materialized_features_20250901.csv    # Derived analytical columns
├── 💻 platform_support_20250901.csv         # OS compatibility matrix
├── 🎮 requirements_parsed_20250901.csv      # Hardware specs structured
├── ✅ embedding_validation_20250901.md      # Quality assurance report
└── 📄 README.md                              # This file
```

### **Navigation Guide:**

- **Embeddings**: Semantic vectors for ~134K successfully retrieved games
- **Metadata**: app_id to vector index mappings and generation parameters
- **Derived Features**: Materialized columns for performance-critical queries
- **Validation**: Embedding quality metrics and coverage statistics

---

## 🔗 **Related Categories**

This section connects enriched data to processing stages and analytical applications.

| **Category** | **Relationship** | **Documentation** |
|--------------|------------------|-------------------|
| **[Processed Data](../02_processed/README.md)** | Source validated data | [02_processed/README.md](../02_processed/README.md) |
| **[Analytics Data](../04_analytics/README.md)** | Final export packages | [04_analytics/README.md](../04_analytics/README.md) |
| **[Vector Scripts](../../scripts/07-vector-embeddings/)** | Embedding generation code | [scripts/07-vector-embeddings/README.md](../../scripts/07-vector-embeddings/README.md) |
| **[Materialization Scripts](../../scripts/08-materialization-columns/)** | Feature extraction code | [scripts/08-materialization-columns/README.md](../../scripts/08-materialization-columns/README.md) |

---

## 🚀 **Getting Started**

This section provides guidance for working with enriched data features.

### **Vector Embedding Usage**

Load and query semantic embeddings:

```python
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

# Load embeddings and metadata
embeddings = np.load('embeddings_20250901.npy')
with open('embedding_metadata_20250901.json', 'r') as f:
    metadata = json.load(f)

# Create app_id to index mapping
app_id_to_idx = {item['app_id']: idx for idx, item in enumerate(metadata['mappings'])}

# Find similar games using cosine similarity
query_app_id = 440  # Team Fortress 2
query_idx = app_id_to_idx[query_app_id]
query_vector = embeddings[query_idx].reshape(1, -1)

# Calculate similarities
similarities = cosine_similarity(query_vector, embeddings)[0]
top_indices = np.argsort(similarities)[-11:-1][::-1]  # Top 10 excluding self

# Get similar app_ids
similar_apps = [metadata['mappings'][idx]['app_id'] for idx in top_indices]
print(f"Games similar to {query_app_id}: {similar_apps}")
```

### **Semantic Search Patterns**

Use embeddings for conceptual game discovery:

```python
# Search by description embedding
search_query = "cooperative multiplayer puzzle game"
query_embedding = embed_text(search_query)  # Using BGE-M3 model

similarities = cosine_similarity([query_embedding], embeddings)[0]
top_matches = np.argsort(similarities)[-20:][::-1]

# Get top matching games
results = [
    {
        'app_id': metadata['mappings'][idx]['app_id'],
        'similarity': similarities[idx]
    }
    for idx in top_matches
]
```

### **Derived Feature Integration**

Access materialized columns for efficient queries:

```python
import pandas as pd

# Load materialized features
features = pd.read_csv('materialized_features_20250901.csv')

# Query without JSONB parsing
windows_games = features[features['supports_windows'] == True]
indie_games = features[features['primary_genre'] == 'Indie']
free_games = features[features['is_free'] == True]

print(f"Windows games: {len(windows_games)}")
print(f"Indie games: {len(indie_games)}")
print(f"Free games: {len(free_games)}")
```

---

## 📚 **Technical Documentation**

This section provides detailed specifications for enriched data formats.

### **Vector Embedding Specifications**

**Model**: BAAI/bge-m3  
**Dimensions**: 1024  
**Normalization**: L2 normalized for cosine similarity  
**Input**: Game detailed_description field (full HTML content)  
**Coverage**: ~134,000 games with successful API retrievals  
**Generation Hardware**: NVIDIA RTX 4090 (24GB VRAM)  
**Processing Time**: ~18 hours for full dataset  

### **Embedding Metadata Structure**

```json
{
  "generation_metadata": {
    "model": "BAAI/bge-m3",
    "dimensions": 1024,
    "timestamp": "2025-09-01T14:23:45Z",
    "total_vectors": 134212,
    "hardware": "NVIDIA RTX 4090"
  },
  "mappings": [
    {
      "index": 0,
      "app_id": 440,
      "name": "Team Fortress 2",
      "description_length": 8432,
      "embedding_norm": 1.0
    }
  ]
}
```

### **Materialized Feature Columns**

Derived columns extracted from JSONB for query performance:

| **Column Name** | **Data Type** | **Source** | **Purpose** |
|-----------------|---------------|------------|-------------|
| **supports_windows** | BOOLEAN | platforms.windows | OS filtering |
| **supports_mac** | BOOLEAN | platforms.mac | OS filtering |
| **supports_linux** | BOOLEAN | platforms.linux | OS filtering |
| **is_free** | BOOLEAN | is_free | Pricing analysis |
| **primary_genre** | VARCHAR(100) | genres[0].description | Genre classification |
| **developer_count** | INTEGER | COUNT(developers) | Portfolio analysis |
| **publisher_count** | INTEGER | COUNT(publishers) | Publisher research |
| **has_achievements** | BOOLEAN | categories contains id=22 | Achievement analysis |
| **multiplayer** | BOOLEAN | categories contains multiplayer | Multiplayer filtering |
| **controller_support** | VARCHAR(50) | controller_support | Input analysis |

### **Hardware Requirements Parsing**

PC requirements extracted into structured format:

```csv
app_id,min_os,min_processor,min_ram_mb,min_storage_gb,rec_os,rec_processor,rec_ram_mb,rec_storage_gb
440,Windows 7,Pentium 4 1.7GHz,512,15,Windows 10,Core 2 Duo 2.4GHz,1024,15
```

**Parsing Logic:**

- Regex extraction from HTML requirements strings
- RAM values converted to MB (1 GB = 1024 MB)
- Storage converted to GB
- NULL for unparseable requirements

---

## 🎯 **Use Cases**

This section identifies analytical applications enabled by enriched data.

### **Semantic Game Discovery**

Find games by conceptual similarity:

- **Similar Games**: "Users who liked X might also enjoy..."
- **Genre Exploration**: Discover games sharing thematic elements
- **Niche Identification**: Find games in underserved categories
- **Content-Based Recommendations**: Match player preferences to descriptions

### **Performance-Optimized Analytics**

Materialized columns eliminate JSONB parsing overhead:

- **Dashboard Queries**: Sub-second response times for common filters
- **Platform Analysis**: Rapid Windows/Mac/Linux support queries
- **Genre Distribution**: Efficient genre-based aggregations
- **Pricing Research**: Fast free-to-play vs paid filtering

### **Hardware Requirement Analysis**

Structured requirements enable quantitative research:

- **System Specs Trends**: RAM/storage growth over time
- **Platform Accessibility**: Games by minimum system requirements
- **Hardware Correlation**: Relationship between specs and pricing/genres
- **Performance Predictions**: Estimate requirements for new releases

### **Multi-Modal Search**

Combine semantic and structured filters:

- **Semantic + Genre**: "Cooperative puzzle games similar to Portal"
- **Semantic + Platform**: "Story-driven indie games for Mac"
- **Semantic + Price**: "Free multiplayer games similar to Team Fortress 2"

---

## 🔍 **Quality Metrics**

This section documents enriched data quality characteristics.

### **Embedding Coverage**

```markdown
Total Games:              239,664
Successful Retrievals:    134,212
Embeddings Generated:     134,189 (99.98% of successful)
Failed Embeddings:        23 (0.02%)

Failure Reasons:
  - Empty descriptions:    18
  - Encoding errors:       5
```

### **Embedding Quality Validation**

```python
# Validation metrics from generation
Average L2 Norm:          1.0000 (normalized)
Vector Dimension Check:   134,189/134,189 (100%)
NaN Detection:            0 vectors
Inf Detection:            0 vectors
Zero Vector Detection:    0 vectors
```

### **Materialized Column Coverage**

For 134,212 successful game retrievals:

| **Feature** | **Coverage** | **Notes** |
|-------------|--------------|-----------|
| **Platform Support** | 100.0% | platforms field always present |
| **Primary Genre** | 98.7% | Most games have genre classifications |
| **Is Free** | 100.0% | Boolean field always defined |
| **Developer Count** | 99.1% | Nearly universal developer attribution |
| **Publisher Count** | 97.8% | High publisher data quality |
| **Has Achievements** | 100.0% | Categories array always present |
| **Multiplayer** | 100.0% | Derived from categories |
| **Controller Support** | 78.3% | Field not present for older games |

### **Requirements Parsing Success**

```markdown
Games with PC Requirements:   87,456 (65.2%)
Successfully Parsed:          73,234 (83.7% of those with requirements)
Partial Parsing:              11,102 (12.7%)
Parse Failures:               3,120 (3.6%)

Parsed Fields Coverage:
  Minimum RAM:                71,445 (81.7%)
  Recommended RAM:            68,923 (78.8%)
  Minimum Storage:            65,234 (74.6%)
  Recommended Storage:        62,109 (71.0%)
  Minimum OS:                 72,890 (83.3%)
  Minimum Processor:          69,112 (79.0%)
```

---

## 🛠️ **Generation Pipeline**

This section describes how enriched features are created from processed data.

### **Vector Embedding Generation**

1. **Data Preparation**: Load validated games with success=true
2. **Description Extraction**: Parse detailed_description from JSONB
3. **Text Preprocessing**: Clean HTML, handle encoding issues
4. **Batch Processing**: Generate embeddings in batches of 32
5. **Normalization**: Apply L2 normalization for cosine similarity
6. **Validation**: Check dimensions, norms, NaN/Inf values
7. **Export**: Save as NumPy binary with JSON metadata

### **Materialization Process**

1. **Schema Analysis**: Identify frequently queried JSONB paths
2. **Column Addition**: Add materialized columns to database schema
3. **Population**: Extract values using JSONB operators
4. **Index Creation**: Build indexes on materialized columns
5. **Validation**: Verify accuracy against JSONB source data
6. **Export**: Generate CSV files for dataset distribution

### **Requirements Parsing**

1. **HTML Extraction**: Parse pc_requirements JSONB field
2. **Regex Matching**: Apply patterns for RAM, storage, OS, processor
3. **Unit Conversion**: Standardize RAM to MB, storage to GB
4. **Validation**: Check for reasonable value ranges
5. **Error Logging**: Track unparseable requirements for manual review
6. **Export**: Generate structured CSV with parsed specifications

---

## 📖 **References**

This section links to related documentation and resources.

### **Internal Documentation**

| **Document** | **Relevance** | **Link** |
|--------------|---------------|----------|
| **Data Dictionary** | Complete schema with materialized columns | [/steam-dataset-2025-v1/DATA_DICTIONARY.md](../../steam-dataset-2025-v1/DATA_DICTIONARY.md) |
| **Vector Embeddings Methodology** | BGE-M3 implementation details | [/docs/methodologies/vector-embeddings.md](../../docs/methodologies/vector-embeddings.md) |
| **Multi-Modal Architecture** | Database design with embeddings | [/docs/methodologies/multi-modal-db-architecture.md](../../docs/methodologies/multi-modal-db-architecture.md) |

### **Generation Scripts**

| **Script Directory** | **Purpose** | **Documentation** |
|---------------------|-------------|-------------------|
| **07-vector-embeddings** | BGE-M3 embedding generation | [README.md](../../scripts/07-vector-embeddings/README.md) |
| **08-materialization-columns** | Feature extraction pipeline | [README.md](../../scripts/08-materialization-columns/README.md) |
| **09-pc-requirements-materialization** | Requirements parsing | [README.md](../../scripts/09-pc-requirements-materialization/README.md) |

### **External Resources**

| **Resource** | **Description** | **Link** |
|--------------|-----------------|----------|
| **BGE-M3 Model** | BAAI's multilingual embedding model | <https://huggingface.co/BAAI/bge-m3> |
| **pgvector Extension** | PostgreSQL vector similarity search | <https://github.com/pgvector/pgvector> |
| **Semantic Search Guide** | Best practices for vector search | <https://www.pinecone.io/learn/vector-embeddings/> |

---

## 📜 **Documentation Metadata**

### **Change Log**

| **Version** | **Date** | **Changes** | **Author** |
|------------|----------|-------------|------------|
| 1.0 | 2025-01-06 | Initial documentation for enriched data tier | VintageDon |

### **Authorship & Collaboration**

**Primary Author:** VintageDon (Donald Fountain)  
**GitHub:** <https://github.com/vintagedon>  
**AI Collaboration:** Claude 3.7 Sonnet (Anthropic) - Documentation structure and technical writing assistance  

**Human Responsibility:** All technical decisions, embedding model selection, and feature engineering strategies are human-defined. AI assistance was used for documentation organization and clarity enhancement.

---

**Document Information**

| **Field** | **Value** |
|-----------|-----------|
| **Author** | VintageDon - <https://github.com/vintagedon> |
| **Created** | 2025-01-06 |
| **Last Updated** | 2025-01-06 |
| **Version** | 1.0 |

---
Tags: vector-embeddings, semantic-search, bge-m3, materialized-columns, feature-engineering, pgvector
