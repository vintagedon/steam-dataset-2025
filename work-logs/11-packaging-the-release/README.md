# 📓 **Notebooks Directory**

This directory contains Jupyter notebooks demonstrating analytical workflows, exploratory data analysis, and research applications using Steam Dataset 2025. Notebooks combine narrative exposition with executable code to showcase dataset capabilities while maintaining reproducibility through pre-exported CSV/Parquet data files.

## **Overview**

The notebooks directory serves as both documentation and executable analysis examples for Steam Dataset 2025. Each notebook addresses specific research questions using different analytical approaches: temporal market analysis, semantic game discovery, and machine learning applications. Notebooks are designed for immediate execution on Kaggle or local environments without database dependencies, using pre-exported data from the analytics tier.

---

## 📁 **Directory Contents**

This section documents available notebooks and their analytical focus.

### **Published Notebooks**

| **Notebook** | **Topic** | **Key Techniques** | **Data Files** |
|--------------|-----------|-------------------|----------------|
| **[01-platform-evolution](01-steam-platform-evolution-and-marketplace/README.md)** | Market trends 1997-2025 | Temporal analysis, genre evolution | 6 CSV files (~3MB) |
| **[02-semantic-discovery](02-semantic-game-discovery/README.md)** | Vector-based game search | Embeddings, cosine similarity | 1 CSV + 1 NPY (~25MB) |
| **[03-semantic-fingerprint](03-the-semantic-fingerprint/README.md)** | Genre classification ML | Random Forest, embeddings | 1 Parquet (~180MB) |

### **Notebook Structure**

Each notebook follows this organizational pattern:

```markdown
notebook-XX-title/
├── 📓 notebook-XX-title.ipynb          # Main Jupyter notebook
├── 📊 data/                             # Pre-exported datasets
│   ├── 01_dataset.csv
│   ├── 02_dataset.csv
│   └── embeddings.npy
├── 📋 notebook-XX-title.pdf            # Static PDF export
└── 📄 README.md                         # Notebook-specific documentation
```

---

## 🗂️ **Repository Structure**

Visual representation of notebooks organization:

```markdown
notebooks/
├── 📈 01-steam-platform-evolution-and-marketplace/
│   ├── notebook-01-steam-platform-evolution.ipynb
│   ├── notebook-01-steam-platform-evolution.pdf
│   ├── data/
│   │   ├── 01_temporal_growth.csv
│   │   ├── 02_genre_evolution.csv
│   │   ├── 03_platform_support.csv
│   │   ├── 04_pricing_strategy.csv
│   │   ├── 05_publisher_portfolios.csv
│   │   └── 06_achievement_evolution.csv
│   └── README.md
├── 🔍 02-semantic-game-discovery/
│   ├── notebook-02-semantic-game-discovery.ipynb
│   ├── notebook-02-semantic-game-discovery.pdf
│   ├── data/
│   │   ├── 01_game_embeddings_sample.csv
│   │   ├── 02_embeddings_appids.csv
│   │   ├── 02_embeddings_vectors.npy
│   │   ├── 02_genre_representatives.csv
│   │   └── 02_semantic_search_examples.json
│   └── README.md
├── 🤖 03-the-semantic-fingerprint/
│   ├── notebook-03-the-semantic-fingerprint.ipynb
│   ├── notebook-03-the-semantic-fingerprint.pdf
│   ├── data/
│   │   ├── 03-the-semantic-fingerprint.parquet
│   │   └── 03-the-semantic-fingerprint-preview.csv
│   └── README.md
└── 📄 README.md                         # This file
```

### **Navigation Guide:**

- **Platform Evolution**: 28-year market analysis with temporal trends
- **Semantic Discovery**: Vector-based game similarity and search
- **Semantic Fingerprint**: Genre classification using ML and embeddings
- **PDF Exports**: Static versions for reading without Jupyter

---

## 🔗 **Related Categories**

This section connects notebooks to data sources and documentation.

| **Category** | **Relationship** | **Documentation** |
|--------------|------------------|-------------------|
| **[Analytics Data](../data/04_analytics/README.md)** | Source datasets for notebooks | [data/04_analytics/README.md](../data/04_analytics/README.md) |
| **[Models](../models/README.md)** | ML models trained in notebooks | [models/README.md](../models/README.md) |
| **[Dataset Documentation](../steam-dataset-2025-v1/)** | Schema and methodology | [steam-dataset-2025-v1/README.md](../steam-dataset-2025-v1/README.md) |
| **[Notebook Generation Scripts](../scripts/12-notebook-generation/)** | Data export scripts | [scripts/12-notebook-generation/README.md](../scripts/12-notebook-generation/README.md) |

---

## 🚀 **Getting Started**

This section provides guidance for using and running notebooks.

### **Running on Kaggle**

Notebooks are optimized for Kaggle execution:

1. **Upload Dataset**: Add `steam-dataset-2025-notebook-data` as input dataset
2. **Open Notebook**: Upload .ipynb file to Kaggle
3. **Configure Paths**: Notebooks auto-detect Kaggle vs local environment
4. **Run All**: Execute cells sequentially or use "Run All"

```python
# Auto-detection pattern used in notebooks
import os

if os.path.exists('/kaggle/input'):
    # Kaggle environment
    DATA_DIR = Path('/kaggle/input/steam-dataset-2025-notebook-data/01-platform-evolution')
    ENV = 'Kaggle'
else:
    # Local environment
    DATA_DIR = Path('../notebook-data/01-platform-evolution')
    ENV = 'Local'

print(f"✅ Environment: {ENV}")
print(f"📁 Data directory: {DATA_DIR}")
```

### **Running Locally**

For local execution without database:

```bash
# Clone repository
git clone https://github.com/vintagedon/steam-dataset-2025.git
cd steam-dataset-2025

# Install dependencies
pip install pandas numpy matplotlib seaborn scikit-learn

# Launch Jupyter
jupyter notebook notebooks/01-steam-platform-evolution-and-marketplace/
```

### **Notebook Citation**

All notebooks include proper dataset attribution:

```python
"""
Dataset: Steam Dataset 2025
Author: Donald Fountain (VintageDon)
Citation: Fountain, D. (2025). Steam Dataset 2025. Zenodo. 
          https://doi.org/10.5281/zenodo.17266923
License: CC BY 4.0
"""
```

---

## 📚 **Notebook Summaries**

This section provides detailed overviews of each notebook's content and findings.

### **Notebook 01: Platform Evolution & Market Landscape**

**Research Questions:**

1. How has Steam's content catalog evolved across 28 years?
2. Which genres drive platform growth and how have pricing strategies changed?
3. What patterns emerge in Windows/Mac/Linux support over time?
4. How do publishers balance portfolio diversification and pricing?
5. How has Steam's achievement system diffused across the platform?

**Key Findings:**

- Exponential growth from 1997-2025 with inflection points marking major platform shifts
- Indie genre explosion post-2010 correlates with Steam Greenlight/Direct programs
- Mac support peaked ~2012, Linux remains niche at 15-20% of releases
- Free-to-play economics transformed monetization strategies post-2015
- Top publishers pursue mixed strategies: some specialize, others diversify

**Methodology:** Temporal aggregation, genre co-occurrence analysis, platform support matrices, pricing tier analysis, publisher portfolio diversity metrics

**Data Files:** 6 CSV files (29-202K rows each, ~3MB total)

---

### **Notebook 02: Semantic Game Discovery**

**Research Questions:**

1. How do vector embeddings capture game concepts beyond keyword matching?
2. Can semantic search discover games with similar gameplay despite different genres?
3. What representative games best exemplify each major genre?
4. How does semantic similarity correlate with genre classifications?

**Key Findings:**

- BGE-M3 embeddings capture gameplay mechanics, narrative themes, and artistic styles
- Semantic search finds conceptual matches across genre boundaries (puzzle-platformers vs pure puzzles)
- Genre representatives identified algorithmically match community consensus choices
- ~73% semantic similarity for same-genre games, ~42% for different genres (clear signal)

**Methodology:** Cosine similarity search, t-SNE visualization, genre centroid analysis, semantic clustering validation

**Data Files:** 1 CSV (1000 game sample), 1 NPY (1024-dim vectors for 134K games, ~520MB), semantic search examples JSON

---

### **Notebook 03: The Semantic Fingerprint**

**Research Questions:**

1. Can game descriptions alone predict genres better than metadata?
2. How does ML performance scale from balanced sampling to class imbalance?
3. What RAM characteristics correlate with genre and description semantics?
4. Which genres are most predictable from text descriptions?

**Key Findings:**

- Embeddings-only model achieves 0.71 F1 (macro) vs 0.58 for metadata-only
- Class imbalance significantly impacts performance (Action 41%, ~1:61 ratio to least common)
- RAM requirements strongly correlate with genre (Indie: 4.2GB avg, Simulation: 8.1GB)
- Strategy and Simulation most predictable (F1 ~0.79), Casual least predictable (F1 ~0.64)

**Methodology:** Random Forest classification with class rebalancing, embedding-based feature engineering, RAM distribution analysis, genre-specific error analysis

**Data Files:** 1 Parquet file (50K games with embeddings and metadata, ~180MB)

---

## 🎯 **Use Cases**

This section identifies applications for notebook examples.

### **Educational Resources**

Notebooks serve as teaching materials:

- **Data Science Curricula**: Real-world dataset with diverse analytical challenges
- **ML Course Examples**: Classification, regression, semantic search demonstrations
- **Visualization Techniques**: Publication-quality plots using matplotlib/seaborn
- **Research Methods**: Reproducible analysis with documented methodology

### **Research Templates**

Notebooks provide starting points for academic research:

- **Reproducible Workflows**: Clear data lineage from source to analysis
- **Methodology Examples**: Temporal analysis, semantic search, ML evaluation patterns
- **Citation Standards**: Proper attribution of dataset and dependencies
- **Extension Points**: Notebooks designed for modification and expansion

### **Dataset Evaluation**

Notebooks demonstrate dataset capabilities:

- **Coverage Assessment**: Show breadth of temporal, genre, platform data
- **Quality Validation**: Demonstrate data completeness and consistency
- **Feature Showcase**: Highlight unique aspects (embeddings, materialized columns)
- **Performance Benchmarks**: Establish baseline model performance

### **Community Engagement**

Notebooks facilitate dataset adoption:

- **Quick Start Examples**: Immediate hands-on experience without setup
- **Competition Seeds**: Kaggle-ready notebooks for ML competitions
- **Discussion Starters**: Analysis findings spark community conversations
- **Contribution Templates**: Patterns for community-contributed notebooks

---

## 🔍 **Technical Specifications**

This section documents notebook development standards.

### **Code Quality Standards**

All notebooks adhere to these principles:

```markdown
✓ Environment Detection:    Auto-detect Kaggle vs local paths
✓ Dependency Management:    Explicit imports with version notes
✓ Reproducibility:          Fixed random seeds (42) for stochastic operations
✓ Error Handling:           Try/except blocks for external dependencies
✓ Documentation:            Markdown cells explain analysis choices
✓ Validation:               Data quality checks before analysis
✓ Visualization:            Consistent color schemes and readable plots
```

### **Data File Optimization**

Notebook data files are optimized for execution:

| **Optimization** | **Implementation** | **Benefit** |
|-----------------|-------------------|-------------|
| **Size Limits** | CSV files <100MB each | Kaggle notebook data size limits |
| **Row Filtering** | `WHERE success = TRUE` | Complete records only |
| **Column Selection** | Only columns used in analysis | Reduced memory footprint |
| **Data Types** | Optimal dtype per column | Faster loading and processing |
| **Compression** | Parquet with Snappy | 2-3x smaller than CSV |

### **Notebook Structure Template**

Standard organization pattern:

```markdown
# [Title]: [Subtitle]
Author: Donald Fountain (VintageDon)
Citation: [Dataset citation]

## Executive Summary
[2-3 sentences: scope, methods, key findings]

## 1. Introduction & Research Questions
[Research questions with numbered list]

## 2. Data Loading & Environment Setup
[Environment detection, library imports, data validation]

## 3. Exploratory Data Analysis
[5+ visualizations with detailed commentary]

## 4. Core Analysis
[Main analytical work addressing research questions]

## 5. Key Findings & Conclusions
[3-5 major findings with implications]

## 6. Limitations & Future Work
[Known limitations and research extensions]

## 7. References
[Dataset citation, documentation links, external resources]
```

---

## 🛠️ **Notebook Development Workflow**

This section describes the notebook creation process.

### **Development Pipeline**

1. **Define Research Questions**: Identify analytical objectives and required data
2. **SQL Query Development**: Write queries to extract necessary data from database
3. **Data Export**: Generate CSV/Parquet files <100MB for notebook usage
4. **Validation**: Verify exported data matches query expectations
5. **Notebook Development**: Build analysis incrementally with validation checks
6. **Review**: Test execution in both local and Kaggle environments
7. **Documentation**: Add markdown cells explaining methodology and findings
8. **PDF Export**: Generate static version for distribution

### **Quality Assurance**

Each notebook undergoes these checks:

```markdown
✓ Execution Test:           Run "Restart & Run All" successfully
✓ Environment Test:         Execute in both local and Kaggle environments
✓ Data Validation:          Verify row counts and column presence
✓ Reproducibility:          Fixed seeds produce identical results
✓ Documentation:            All major sections have explanatory markdown
✓ Citation:                 Dataset attribution present and correct
✓ Visualization:            All plots render correctly and are readable
✓ File Size:                Total notebook data <500MB for Kaggle limits
```

### **Export and Distribution**

1. **Jupyter Export**: Save notebook as .ipynb
2. **PDF Generation**: Export via nbconvert with --to pdf
3. **Data Packaging**: Organize notebook data files in subdirectory
4. **README Creation**: Document notebook purpose and requirements
5. **Repository Integration**: Add to notebooks directory with proper linking
6. **External Distribution**: Upload to Kaggle and link from Zenodo dataset

---

## 📖 **References**

This section links to related documentation and resources.

### **Internal Documentation**

| **Document** | **Relevance** | **Link** |
|--------------|---------------|----------|
| **Data Dictionary** | Schema reference for notebook data | [/steam-dataset-2025-v1/DATA_DICTIONARY.md](../steam-dataset-2025-v1/DATA_DICTIONARY.md) |
| **Dataset Card** | Methodology and collection details | [/steam-dataset-2025-v1/DATASET_CARD.md](../steam-dataset-2025-v1/DATASET_CARD.md) |
| **Analytics Data** | Full analytical datasets | [/data/04_analytics/README.md](../data/04_analytics/README.md) |
| **Notebook Development Guide** | Creation standards | [/docs/notebook-development.md](../docs/notebook-development.md) |

### **Generation Scripts**

| **Script** | **Purpose** | **Documentation** |
|------------|-------------|-------------------|
| **generate-notebook-01.py** | Export temporal analysis data | [scripts/12-notebook-generation/README.md](../scripts/12-notebook-generation/README.md) |
| **generate-notebook-02.py** | Export semantic search data | [scripts/12-notebook-generation/README.md](../scripts/12-notebook-generation/README.md) |
| **export-parquet-notebook-03.py** | Export ML training data | [scripts/12-notebook-generation/README.md](../scripts/12-notebook-generation/README.md) |

### **External Resources**

| **Resource** | **Description** | **Link** |
|--------------|-----------------|----------|
| **Jupyter Documentation** | Notebook format specification | <https://jupyter.org/documentation> |
| **Kaggle Notebooks** | Platform hosting and execution | <https://www.kaggle.com/code> |
| **NBViewer** | Static notebook rendering | <https://nbviewer.org/> |

---

## 📜 **Documentation Metadata**

### **Change Log**

| **Version** | **Date** | **Changes** | **Author** |
|------------|----------|-------------|------------|
| 1.0 | 2025-01-06 | Initial notebooks directory documentation | VintageDon |

### **Authorship & Collaboration**

**Primary Author:** VintageDon (Donald Fountain)  
**GitHub:** <https://github.com/vintagedon>  
**AI Collaboration:** Claude 3.7 Sonnet (Anthropic) - Documentation structure and technical writing assistance  

**Human Responsibility:** All notebook designs, analytical methodologies, and research questions are human-defined. AI assistance was used for documentation organization and clarity enhancement.

---

**Document Information**

| **Field** | **Value** |
|-----------|-----------|
| **Author** | VintageDon - <https://github.com/vintagedon> |
| **Created** | 2025-01-06 |
| **Last Updated** | 2025-01-06 |
| **Version** | 1.0 |

---
Tags: jupyter-notebooks, data-analysis, visualization, machine-learning, reproducible-research, kaggle
