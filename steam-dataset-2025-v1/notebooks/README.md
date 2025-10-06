<!--
---
title: "Notebooks - Interactive Analysis & Demonstrations"
description: "Navigation hub for Steam Dataset 2025 Jupyter notebooks showcasing platform analytics, semantic search, and machine learning applications"
author: "VintageDon - https://github.com/vintagedon"
ai_contributor: "Claude Sonnet 4"
date: "2025-10-06"
version: "1.0"
status: "Published"
tags:
- type: [directory-overview/notebook-collection]
- domain: [data-science/machine-learning/visualization]
- phase: [phase-3]
related_documents:
- "[Parent Directory](../README.md)"
- "[Notebook Data](../notebook-data/README.md)"
- "[Data Dictionary](../DATA_DICTIONARY.md)"
---
-->

# 📊 **Notebooks - Interactive Analysis & Demonstrations**

Navigation hub for production-ready Jupyter notebooks demonstrating Steam Dataset 2025 capabilities. These notebooks showcase the dataset's unique features through beginner-to-advanced analytical workflows, providing reproducible examples for market analysis, semantic search, and machine learning applications.

---

## **1. Introduction**

### **1.1 Purpose**

This directory contains three publication-ready Jupyter notebooks that demonstrate the Steam Dataset 2025's analytical capabilities and unique features. Each notebook addresses specific research questions using reproducible workflows, comprehensive visualizations, and clear documentation suitable for academic publication, portfolio projects, and educational purposes.

### **1.2 Scope**

**What's Covered:**

- Platform evolution and market dynamics analysis (28-year historical perspective)
- Semantic game discovery using vector embeddings and UMAP visualization
- Machine learning predictions for genre classification and hardware requirements
- Complete data validation and quality assurance procedures
- Production-ready code with comprehensive error handling

### **1.3 Target Audience**

**Primary Users:** Data scientists, ML engineers, and researchers seeking reproducible analytical examples  
**Secondary Users:** Students learning data analysis, portfolio builders, Kaggle competitors  
**Background Assumed:** Python programming, pandas/numpy proficiency, basic machine learning concepts; advanced topics explained with code comments

### **1.4 Overview**

The three notebooks progress from beginner-friendly market analysis through intermediate semantic search to advanced machine learning applications. Each notebook is self-contained with its own data package, includes extensive validation procedures, and provides detailed commentary on methodology and findings. All notebooks are tested for nbviewer and Kaggle compatibility.

---

## **2. Dependencies & Relationships**

### **2.1 Related Components**

| **Component** | **Relationship** | **Integration Points** | **Documentation** |
|---------------|------------------|------------------------|-------------------|
| Notebook Data | Required data files for each notebook | CSV, NPY, JSON, Parquet files pre-processed from database | [../notebook-data/README.md](../notebook-data/README.md) |
| Data Dictionary | Schema reference for understanding data structures | Column definitions, JSONB structures, relationships | [../DATA_DICTIONARY.md](../DATA_DICTIONARY.md) |
| Methodologies | Background on data collection and quality | API collection procedures, validation frameworks | [../../docs/methodologies/README.md](../../docs/methodologies/README.md) |
| Analytics Documentation | Extended analysis beyond notebook scope | Deep-dive analyses, methodology documentation | [../../docs/analytics/README.md](../../docs/analytics/README.md) |

### **2.2 External Dependencies**

**Common Dependencies (All Notebooks):**

- **[Python 3.9+](https://www.python.org/)** - Core programming environment
- **[pandas 2.0+](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[matplotlib 3.7+](https://matplotlib.org/)** - Core visualization library
- **[seaborn 0.12+](https://seaborn.pydata.org/)** - Statistical visualizations

**Advanced Dependencies (Notebooks 2-3):**

- **[numpy 1.24+](https://numpy.org/)** - Numerical computing and vector operations
- **[scikit-learn 1.3+](https://scikit-learn.org/)** - Machine learning algorithms
- **[umap-learn 0.5+](https://umap-learn.readthedocs.io/)** - Dimensionality reduction for visualization

---

## **3. Notebook Collection**

This section provides detailed descriptions of each notebook, helping you identify which notebooks address your analytical or learning objectives.

### **3.1 Notebook 1: Platform Evolution & Market Landscape**

**[01-steam-platform-evolution-and-marketplace](01-steam-platform-evolution-and-marketplace/)**

Comprehensive analysis of Steam's 28-year evolution from 2,400 applications in 1997 to 239,000+ in 2025. Examines market dynamics, pricing strategies, genre trends, publisher portfolios, and platform adoption patterns using materialized analytical columns for efficient querying.

**Difficulty:** Beginner  
**Runtime:** ~5 minutes  
**Data Size:** 6 CSV files, ~15 MB total  
**Notebook File:** [notebook-01-steam-platform-evolution-and-market-landscape.ipynb](01-steam-platform-evolution-and-marketplace/notebook-01-steam-platform-evolution-and-market-landscape.ipynb)  
**PDF Export:** [notebook-01-steam-platform-evolution.pdf](01-steam-platform-evolution-and-marketplace/notebook-01-steam-platform-evolution.pdf)

**Use this notebook when:**

- Learning pandas data analysis and visualization techniques
- Understanding gaming industry market dynamics and trends
- Exploring pricing strategies and content diversification patterns
- Building portfolio projects demonstrating analytical skills
- Teaching data visualization best practices

**Key Visualizations:**

- Dual-axis temporal growth chart (annual releases + cumulative totals)
- Content type diversification over 28 years (stacked area chart)
- Genre popularity heatmap (2010-2025, top 10 genres)
- Platform support distribution with price correlations
- Pricing strategy segmentation (7-tier analysis)
- Publisher portfolio composition (top 20 publishers)
- Achievement system adoption timeline

**Research Questions Answered:**

1. How has Steam's content volume evolved from 1997-2025?
2. What pricing strategies dominate different market segments?
3. Which genres show sustained popularity vs. emerging trends?
4. How do platform support choices correlate with pricing?
5. What differentiates successful publisher portfolio strategies?

**Dataset Features Showcased:**

- ✅ 28-year historical depth (1997-2025)
- ✅ Materialized analytical columns for query performance
- ✅ 239K+ application scale vs. competitors' 27K-85K
- ✅ Complete content type diversity (games, DLC, software, media)

---

### **3.2 Notebook 2: Semantic Game Discovery**

**[02-semantic-game-discovery](02-semantic-game-discovery/)**

Demonstrates semantic search capabilities using 1024-dimensional BGE-M3 vector embeddings. Includes UMAP dimensionality reduction for visualizing game similarity clusters, genre-based representative sampling, and pre-computed semantic search examples across diverse query types.

**Difficulty:** Intermediate-Advanced  
**Runtime:** ~10 minutes (includes UMAP computation)  
**Data Size:** 48 MB (10K games + vectors)  
**Notebook File:** [02-semantic-game-discovery.ipynb](02-semantic-game-discovery/02-semantic-game-discovery.ipynb)  
**PDF Export:** [notebook-02-semantic-game-discovery.pdf](02-semantic-game-discovery/notebook-02-semantic-game-discovery.pdf)

**Use this notebook when:**

- Learning vector embedding applications for text data
- Building semantic search or recommendation systems
- Understanding dimensionality reduction techniques (UMAP)
- Implementing content-based discovery algorithms
- Exploring multilingual NLP capabilities

**Key Visualizations:**

- UMAP 2D projection of 10,000 game embeddings colored by genre
- Genre cluster analysis with centroid calculations
- Inter-genre distance matrix visualization
- Semantic search similarity score distributions
- Sample bias analysis and characteristics

**Research Questions Answered:**

1. Can semantic embeddings cluster games by genre without supervision?
2. What similarity scores indicate "good" semantic matches?
3. How do different query types (mood, mechanics, setting) perform?
4. What biases exist in review-based sampling strategies?
5. Which genres show tight clustering vs. broad semantic diversity?

**Dataset Features Showcased:**

- ✅ 1024-dimensional BGE-M3 embeddings (NO other Steam dataset has this)
- ✅ pgvector integration for fast similarity search
- ✅ Multilingual content preservation (77 genres including non-English)
- ✅ Pre-computed HNSW indexes for production-scale search

**Technical Highlights:**

- Vector quality validation (L2 normalization checks)
- Efficient numpy operations for large-scale embeddings
- UMAP hyperparameter tuning for clear cluster separation
- Semantic search implementation with cosine similarity
- Sample bias quantification and mitigation strategies

---

### **3.3 Notebook 3: The Semantic Fingerprint**

**[03-the-semantic-fingerprint](03-the-semantic-fingerprint/)**

Advanced machine learning analysis predicting game genres and minimum RAM requirements directly from store description embeddings. Demonstrates that semantic "fingerprints" encode both categorical attributes (genre classification: 67% macro-F1) and technical specifications (RAM prediction: ±2.4 GB accuracy) without ever seeing system requirements.

**Difficulty:** Advanced  
**Runtime:** ~15 minutes (includes model training)  
**Data Size:** 112K games, Parquet format  
**Notebook File:** [03-the-semantic-fingerprint.ipynb](03-the-semantic-fingerprint/03-the-semantic-fingerprint.ipynb)  
**PDF Export:** [notebook-03-the-semantic-fingerprint.pdf](03-the-semantic-fingerprint/notebook-03-the-semantic-fingerprint.pdf)

**Use this notebook when:**

- Building ML classification models on text embeddings
- Learning feature engineering from high-dimensional data
- Understanding class imbalance handling techniques (macro-F1)
- Implementing multi-target prediction pipelines
- Evaluating model performance with proper cross-validation

**Key Visualizations:**

- Class imbalance analysis (genre distribution)
- RAM distribution skewness and log transformation
- Genre-RAM correlation heatmap
- Feature importance analysis (if applicable)
- Prediction accuracy by genre and RAM tier

**Research Questions Answered:**

1. Can semantic embeddings predict primary genre better than majority baseline?
2. Do embeddings predict technical requirements (minimum RAM in GB)?
3. How does class imbalance affect genre accuracy and appropriate metrics?
4. What is the relationship between genre and RAM requirements?
5. Which game description patterns correlate with hardware complexity?

**Dataset Features Showcased:**

- ✅ Vector embeddings as ML features (dimension reduction from 1024-dim)
- ✅ JSONB structured data extraction (PC requirements parsing)
- ✅ 111K+ games with complete metadata for training
- ✅ Multi-language content handling

**Technical Highlights:**

- Proper train/test splitting with stratification
- Class imbalance handling with macro-F1 scoring
- Log transformation for skewed continuous targets
- Model interpretability through feature importance
- Production-ready prediction pipeline

**Key Finding:**
Store descriptions act as "semantic fingerprints" encoding measurable technical reality. Games using "Strategy"-like language average 7.2 GB RAM requirements vs. 3.8 GB for "Casual"-style descriptions, proving marketplace language correlates with hardware complexity.

---

## **4. Getting Started**

### **4.1 Usage Pathways**

**For Data Science Learners:**

1. **Start:** [Notebook 1: Platform Evolution](01-steam-platform-evolution-and-marketplace/) - Learn pandas and visualization
2. **Intermediate:** [Notebook 2: Semantic Discovery](02-semantic-game-discovery/) - Explore embeddings and UMAP
3. **Advanced:** [Notebook 3: Semantic Fingerprint](03-the-semantic-fingerprint/) - Build ML models

**For ML Engineers:**

1. **Start:** [Notebook 2: Semantic Discovery](02-semantic-game-discovery/) - Understand embedding space
2. **Build:** [Notebook 3: Semantic Fingerprint](03-the-semantic-fingerprint/) - Implement classification pipeline
3. **Extend:** Customize models for your specific use case

**For Researchers:**

1. **Start:** [Notebook 1: Platform Evolution](01-steam-platform-evolution-and-marketplace/) - Understand dataset scope
2. **Methods:** Review validation procedures and data quality checks in each notebook
3. **Apply:** Adapt methodologies for your research questions

### **4.2 Execution Environments**

**Local Execution:**

```bash
# Install dependencies
pip install pandas matplotlib seaborn numpy scikit-learn umap-learn

# Clone repository
git clone https://github.com/VintageDon/steam-dataset-2025.git
cd steam-dataset-2025/steam-dataset-2025-v1/notebooks

# Launch Jupyter
jupyter notebook
```

**Kaggle Execution:**

1. Upload notebook data package as Kaggle dataset
2. Create new notebook kernel
3. Add notebook data as input dataset
4. Update file paths to `/kaggle/input/`
5. Run all cells

**NBViewer (Read-Only):**
All notebooks tested for nbviewer compatibility. View rendered notebooks without execution:

- Notebook 1: [NBViewer link pending]
- Notebook 2: [NBViewer link pending]
- Notebook 3: [NBViewer link pending]

### **4.3 Common Questions**

**"Which notebook should I start with?"**  
→ [Notebook 1: Platform Evolution](01-steam-platform-evolution-and-marketplace/) for beginners; [Notebook 2: Semantic Discovery](02-semantic-game-discovery/) if comfortable with pandas; [Notebook 3: Semantic Fingerprint](03-the-semantic-fingerprint/) for ML practitioners

**"Do I need the full database?"**  
→ No - Each notebook uses pre-processed CSV/NPY/Parquet files in the [notebook-data](../notebook-data/) directory

**"Can I modify the notebooks?"**  
→ Yes - All notebooks use MIT License; attribution required. Adapt for your projects and research

**"How long do notebooks take to run?"**  
→ Notebook 1: ~5 minutes | Notebook 2: ~10 minutes | Notebook 3: ~15 minutes (on standard laptop)

**"Are these suitable for academic papers?"**  
→ Yes - All notebooks include proper citations, methodology transparency, and reproducible workflows. Use official Zenodo DOI: [10.5281/zenodo.17286923](https://doi.org/10.5281/zenodo.17286923)

---

## **5. References & Related Resources**

### **5.1 Internal References**

| **Document Type** | **Title** | **Relationship** | **Link** |
|-------------------|-----------|------------------|----------|
| Data Package | Notebook Data Directory | Required input files for all notebooks | [../notebook-data/README.md](../notebook-data/README.md) |
| Schema | Data Dictionary | Complete field definitions and structures | [../DATA_DICTIONARY.md](../DATA_DICTIONARY.md) |
| Methodology | Steam API Collection | Data source and quality documentation | [../../docs/methodologies/steam-api-collection.md](../../docs/methodologies/steam-api-collection.md) |
| Methodology | Vector Embeddings | Embedding generation approach | [../../docs/methodologies/vector-embeddings.md](../../docs/methodologies/vector-embeddings.md) |
| Analytics | Steam 5K Analysis | Extended analysis beyond notebooks | [../../docs/analytics/steam-5k-dataset-analysis.md](../../docs/analytics/steam-5k-dataset-analysis.md) |

### **5.2 External Resources**

| **Resource Type** | **Title** | **Description** | **Link** |
|-------------------|-----------|-----------------|----------|
| Dataset Archive | Zenodo Record | Official dataset publication with DOI | [doi.org/10.5281/zenodo.17286923](https://doi.org/10.5281/zenodo.17286923) |
| Repository | GitHub Repository | Complete source code and documentation | [github.com/VintageDon/steam-dataset-2025](https://github.com/VintageDon/steam-dataset-2025) |
| Tutorial | Jupyter Documentation | Notebook execution and customization | [jupyter.org/documentation](https://jupyter.org/documentation) |
| ML Library | scikit-learn User Guide | Machine learning documentation | [scikit-learn.org/stable/user_guide.html](https://scikit-learn.org/stable/user_guide.html) |
| Visualization | UMAP Documentation | Dimensionality reduction technique | [umap-learn.readthedocs.io](https://umap-learn.readthedocs.io/) |

---

## **6. Documentation Metadata**

### **6.1 Change Log**

| **Version** | **Date** | **Changes** | **Author** |
|------------|----------|-------------|------------|
| 1.0 | 2025-10-06 | Initial notebooks directory README with three completed notebooks | VintageDon |

### **6.2 Authorship & Collaboration**

**Primary Author:** VintageDon ([GitHub Profile](https://github.com/VintageDon))  
**AI Assistance:** Claude Sonnet 4 for notebook structure and documentation  
**Methodology:** Request-Analyze-Verify-Generate-Validate-Reflect (RAVGVR)  
**Quality Assurance:** All notebooks tested in fresh Python environments; validation procedures included in each notebook

### **6.3 Notebook Development Status**

**Completed Notebooks:**

- ✅ Notebook 1: Platform Evolution & Market Landscape (Production-ready)
- ✅ Notebook 2: Semantic Game Discovery (Production-ready)
- ✅ Notebook 3: The Semantic Fingerprint (Production-ready)

**Publication Status:**

- ✅ All notebooks tested for nbviewer compatibility
- ✅ PDF exports generated for archival reference
- ⏳ Kaggle publication pending (notebook data package upload in progress)
- ✅ Individual notebook READMEs complete for Notebooks 1 and 3

---

*Document Version: 1.0 | Last Updated: 2025-10-06 | Status: Published*

---

Tags: notebooks, jupyter, data-science, machine-learning, semantic-search, visualization, steam-dataset
