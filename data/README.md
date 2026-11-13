# 📊 Steam Dataset 2025: Data Directory

This directory contains the Steam Dataset 2025 data files and provides comprehensive access information for both sample evaluation and full dataset research applications. The data represents the largest publicly available Steam catalog collection using exclusively official Valve Web APIs.

---

## 📂 Directory Overview

This directory organizes Steam Dataset 2025 data files in a systematic structure supporting both immediate evaluation and comprehensive research applications.

### Data Organization Strategy

- 🎯 Sample Data: Immediate access for evaluation and testing (GitHub compatible)
- 📊 Full Dataset: Complete catalog available through academic archive (Zenodo)
- 🔄 Processing Stages: Clear separation between raw API responses and processed analytical data
- 📚 Complete Documentation: Comprehensive guides for accessing and utilizing all data forms

---

## 🗂️ Directory Contents

This section provides systematic navigation to all data files and subdirectories within the Steam Dataset 2025 data collection.

### Data Subdirectories

| Directory | Content | Size | Access |
|---------------|-------------|----------|------------|
| [01_raw/](01_raw/) | Publicly tracked 5K-run samples (Git LFS) | 14,089,513 + 11,202,479 B | ✅ GitHub Available |
| [02_processed/](02_processed/) | Documentation of the processed/enriched sample stage | README only | 📄 Not tracked in repo |

### Key Data Files

| File | Description | Format | Status |
|----------|-----------------|------------|------------|
| steam_2025_5k-dataset-games_20250831.json.gz | 5,000 game sample with complete metadata | Compressed JSON | ✅ Available |
| steam_2025_5k-dataset-reviews_20250901.json.gz | Player reviews for sample games | Compressed JSON | ✅ Available |
| steam_2025_5k-dataset-enriched_20250901.json | Processed sample with analytics enhancements | JSON | ✅ Available |

---

## 🗂️ Data Structure Overview

Visual representation of the Steam Dataset 2025 data organization across GitHub and the published Zenodo release:

```markdown
data/
├── 📁 01_raw/                    # Publicly tracked API-response samples (Git LFS objects)
│   ├── README.md                 # Raw data documentation
│   ├── steam_2025_5k-dataset-games_20250831.json.gz     # 5K-run games (14,089,513 B)
│   └── steam_2025_5k-dataset-reviews_20250901.json.gz   # 5K-run reviews (11,202,479 B)
├── 📁 02_processed/              # Documentation of processed outputs (not tracked)
│   └── README.md                 # Processed data documentation
└── 📋 README.md                  # This file

PUBLISHED: Zenodo v1.0.0 record (verified 2026-11-13)
├── 📦 steam-dataset-2025-v1.zip                       # 40,212,720 B
├── 📦 steam_dataset_2025_csv_package_v1.zip           # 320,368,878 B
├── 📦 steam_dataset_2025_power_users_dump_v1.zip      # 7,204,002,678 B
└── 📦 steam_dataset_2025_embeddings_package_v1.zip    # 4,870,419,373 B
```

### Navigation Guide

- [📁 Raw Data Directory](01_raw/README.md) - Original Steam API responses and collection metadata
- [📁 Processed Data Directory](02_processed/README.md) - Cleaned, enriched, and analysis-ready formats

---

## 🚀 Quick Access Guide

### For Immediate Evaluation (GitHub)

Sample Dataset - Ready for Download:

- 🎮 Games Sample: [steam_2025_5k-dataset-games_20250831.json.gz](01_raw/steam_2025_5k-dataset-games_20250831.json.gz) (14,089,513 B LFS object; sha256 3b46222510ad64b87e8a0c63c92dba8f5788e0b8abdd4a1f3471ca0d7a70f2af)
- 📝 Reviews Sample: [steam_2025_5k-dataset-reviews_20250901.json.gz](01_raw/steam_2025_5k-dataset-reviews_20250901.json.gz) (11,202,479 B LFS object; sha256 2be129e154505381c77800ca96ea11f09b8db96ddbd2db935c8421cbb4c35a8c)
- 📊 An enriched/processed sample file is documented in 02_processed/README.md but is not tracked in the repository

Quick Start:

```bash
# Download the sample object (LFS content is served by the media endpoint)
wget -O steam_2025_5k-dataset-games_20250831.json.gz \
  https://media.githubusercontent.com/media/vintagedon/steam-dataset-2025/main/data/01_raw/steam_2025_5k-dataset-games_20250831.json.gz

# Verify, then decompress for analysis
sha256sum steam_2025_5k-dataset-games_20250831.json.gz  # 3b46222510ad64b87e8a0c63c92dba8f5788e0b8abdd4a1f3471ca0d7a70f2af
gunzip -k steam_2025_5k-dataset-games_20250831.json.gz

# Ready for analysis!
```

### For Complete Research (Zenodo - Published)

Full Dataset Specifications:

- 📊 Packages: 40,212,720 + 320,368,878 + 7,204,002,678 + 4,870,419,373 bytes (four official ZIPs)
- 🎮 Applications: 239,664 complete catalog entries
- 📝 Reviews: 1,048,148 user reviews  
- 🧠 Embeddings: 1024-dimensional semantic vectors
- 📅 Release: v1.0.0 published 2025-10-05

Access Information:

- 🏛️ Archive: [Zenodo](https://doi.org/10.5281/zenodo.17266923) academic repository
- 🔗 DOI: version [10.5281/zenodo.17266923](https://doi.org/10.5281/zenodo.17266923) · concept [10.5281/zenodo.17266922](https://doi.org/10.5281/zenodo.17266922)
- 📊 Kaggle mirror: [published](https://www.kaggle.com/datasets/crainbramp/steam-dataset-2025-multi-modal-gaming-analytics)

---

## 📊 Dataset Specifications

### Sample Dataset (Currently Available)

| Component | Records | Compressed Size | Uncompressed | Content |
|---------------|-------------|-------------------|------------------|-------------|
| Games Sample | 8,711-record run (5,000 successes) | 14,089,513 B | tracked LFS object | Collection-run artifact with JSONB payloads |
| Reviews Sample | 37,778 review records (5K run) | 11,202,479 B | tracked LFS object | Review sample for the 5K run |
| Enhanced Sample | 5,000 applications | not tracked | N/A | Processed with analytics features (documented in 02_processed/README.md) |

### Full Dataset (Zenodo Release)

| Official package | Bytes | Content |
|------------------|------:|---------|
| steam-dataset-2025-v1.zip | 40,212,720 | Release bundle: docs, notebooks, notebook data |
| steam_dataset_2025_csv_package_v1.zip | 320,368,878 | Accessibility CSV exports |
| steam_dataset_2025_power_users_dump_v1.zip | 7,204,002,678 | Full PostgreSQL dump (239,664 applications; 1,048,148 reviews) |
| steam_dataset_2025_embeddings_package_v1.zip | 4,870,419,373 | 239,664 + 1,048,148 BGE-M3 vectors |

Packaged rows (packaging-time record): 239,664 applications; 1,048,148 reviews; 101,226 developers; 85,699 publishers.

### Data Quality Metrics

| Quality Measure | Sample Dataset | Full Dataset | Notes |
|---------------------|-------------------|------------------|-----------|
| Collection Outcome (record grain) | 5,000/8,711 in the 5K demo run | 239,341/262,791 in the retained raw corpus | Measured from run metadata and raw batches; no HTTP-attempt rate exists in the retained record |
| Metadata Completeness | not measured at sample grain | 59.4874% carry a materialized price currency (USD), dated 2026-08-03 | Missing values stay meaningful NULLs |
| Pricing Information | see packaging records | 59.4874% price-currency coverage | Free games carry no price_overview |
| Review Availability | ~45% of games | ~50% of games | Based on game popularity and user engagement |

---

## 📥 Download Procedures

### Method 1: Direct GitHub Download

For Individual Files:

```bash
# Download specific sample files
curl -L -o games_sample.json.gz "https://github.com/VintageDon/steam-dataset-2025/raw/main/data/01_raw/steam_2025_5k-dataset-games_20250831.json.gz"
curl -L -o reviews_sample.json.gz "https://github.com/VintageDon/steam-dataset-2025/raw/main/data/01_raw/steam_2025_5k-dataset-reviews_20250901.json.gz"

# Decompress
gunzip *.gz
```

For Complete Repository:

```bash
# Clone entire repository
git clone https://github.com/VintageDon/steam-dataset-2025.git
cd steam-dataset-2025/data

# Access all sample data
ls -la 01_raw/ 02_processed/
```

### Method 2: Programmatic Access

Python Example:

```python
import requests
import gzip
import json
from pathlib import Path

def download_sample_data():
    """Download and decompress Steam Dataset 2025 sample data"""
    
    # URLs for sample files
    files = {
        'games': 'https://github.com/VintageDon/steam-dataset-2025/raw/main/data/01_raw/steam_2025_5k-dataset-games_20250831.json.gz',
        'reviews': 'https://github.com/VintageDon/steam-dataset-2025/raw/main/data/01_raw/steam_2025_5k-dataset-reviews_20250901.json.gz'
    }
    
    for name, url in files.items():
        print(f"Downloading {name} sample...")
        response = requests.get(url)
        
        # Save and decompress
        with open(f'{name}_sample.json.gz', 'wb') as f:
            f.write(response.content)
        
        with gzip.open(f'{name}_sample.json.gz', 'rt') as f:
            data = json.load(f)
            
        print(f"✅ {name}: {len(data)} records loaded")
        
        # Save uncompressed for analysis
        with open(f'{name}_sample.json', 'w') as f:
            json.dump(data, f, indent=2)

# Download sample data
download_sample_data()
```

### Method 3: Future Full Dataset Access (Zenodo)

When Available:

- 🏛️ Zenodo Repository: Direct download from academic archive
- 📋 Persistent DOI: Stable citation and access link
- 📦 Complete Package: All components in single archive
- 🔍 Metadata Rich: Complete academic documentation included

---

## 🔍 Data Format Specifications

### JSON Structure Overview

Games Data Structure:

```json
{
  "metadata": {
    "collection_date": "2025-08-31T15:13:05Z",
    "total_records": 5000,
    "successful_games_found": 5000,
    "total_records_processed": 8711,
    "collection_method": "steam_web_api"
  },
  "games": [
    {
      "appid": 123456,
      "name": "Game Title",
      "app_details": {
        "success": true,
        "data": {
          // Complete Steam API response
          "type": "game",
          "name": "Game Title",
          "is_free": false,
          "price_overview": { /* pricing data */ },
          "pc_requirements": { /* system requirements */ },
          "genres": [ /* genre classifications */ ]
        }
      },
      "reviews": {
        // Review data when available
      }
    }
  ]
}
```

### Compression Standards

| Format | Algorithm | Typical Compression | Tools |
|------------|---------------|-------------------------|-----------|
| Raw JSON | None | N/A | Any JSON parser |
| Compressed (.gz) | gzip (level 9) | 70-80% size reduction | gzip, 7-zip, built-in OS tools |

Decompression Examples:

```bash
# Command line
gunzip filename.json.gz
7z x filename.json.gz

# Python
import gzip, json
with gzip.open('filename.json.gz', 'rt') as f:
    data = json.load(f)
```

---

## ⚠️ Important Usage Notes

### Data Currency & Limitations

Temporal Considerations:

- 📅 Collection Period: August-September 2025
- ⏰ Point-in-Time: Data represents snapshot, not real-time values
- 💰 Pricing: Currency rates and promotional pricing reflect collection period
- 📊 Review Counts: User review totals continue growing after collection

Known Constraints:

- 🌍 Geographic Bias: Collection from US-based infrastructure
- 📝 Review Sampling: Limited to 10 recent reviews per application
- 🎮 Content Coverage: 9.4% of Steam catalog missing due to API limitations
- 💡 See [Known Limitations](../docs/limitations.md) for complete analysis

### Appropriate Use Cases

✅ Well-Suited For:

- Historical trend analysis and market research
- Content-based recommendation system development
- Academic research on gaming industry dynamics
- Machine learning model training and evaluation
- Cross-sectional analysis of platform ecosystem

⚠️ Requires Consideration:

- Real-time pricing or availability decisions
- Complete census analysis (account for 9.4% missing data)
- Global market analysis (US collection perspective)
- Longitudinal trend studies (single time point)

---

## 📚 Additional Resources

### Documentation Links

| Resource | Purpose | Relevance |
|--------------|-------------|---------------|
| [Data Access Guide](../docs/data-access.md) | Comprehensive download and usage procedures | Essential for all users |
| [Known Limitations](../docs/limitations.md) | Complete constraint and bias documentation | Critical for research applications |
| [Quick Start Guide](../docs/data-access.md) | 30-minute setup to first analysis | Perfect for new users |
| [Dataset Card](../steam-dataset-2025-v1/DATASET_CARD.md) | Complete academic datasheet | Required for academic applications |

### Technical Resources

| Resource | Content | Audience |
|--------------|-------------|--------------|
| [Multi-Modal Architecture](../docs/methodologies/multi-modal-db-architecture.md) | Database schema and design rationale | Technical implementers |
| [Vector Embeddings](../docs/methodologies/vector-embeddings.md) | Semantic search implementation | ML engineers |
| [ETL Pipeline](../work-logs/README.md) | Complete processing methodology | Data engineers |

---

## 🤝 Support & Contribution

### Getting Help

- 🐛 Data Issues: [GitHub Issues](https://github.com/VintageDon/steam-dataset-2025/issues) with specific file and error information
- 📧 General Questions: Check [Documentation Hub](../docs/README.md) first for existing answers
- 🎓 Academic Inquiries: Reference [Dataset Card](../steam-dataset-2025-v1/DATASET_CARD.md) for comprehensive information

### Data Quality Reports

- 🔍 Error Reporting: Specific data quality issues with file references and expected vs. actual values
- 💡 Enhancement Suggestions: Additional data processing or format suggestions
- 📊 Usage Examples: Share successful analysis approaches and interesting findings

---

Document Information

| Field | Value |
|-----------|-----------|
| Author | VintageDon - [GitHub](https://github.com/VintageDon) |
| Created | 2025-09-07 |
| Last Updated | 2025-09-07 |
| Version | 2.0 |

---
*Tags: data-access, steam-dataset, sample-data, zenodo-release, gaming-analytics*
