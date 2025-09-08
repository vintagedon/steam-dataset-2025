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
| [01_raw/](01_raw/) | Original Steam API responses (sample) | 102MB | ✅ GitHub Available |
| [02_processed/](02_processed/) | Cleaned and enriched sample data | 85MB | ✅ GitHub Available |

### Key Data Files

| File | Description | Format | Status |
|----------|-----------------|------------|------------|
| steam_2025_5k-dataset-games_20250831.json.gz | 5,000 game sample with complete metadata | Compressed JSON | ✅ Available |
| steam_2025_5k-dataset-reviews_20250901.json.gz | Player reviews for sample games | Compressed JSON | ✅ Available |
| steam_2025_5k-dataset-enriched_20250901.json | Processed sample with analytics enhancements | JSON | ✅ Available |

---

## 🗂️ Data Structure Overview

Visual representation of the complete Steam Dataset 2025 data organization across both GitHub and planned Zenodo releases:

```markdown
data/
├── 📁 01_raw/                    # Original API responses
│   ├── README.md                 # Raw data documentation
│   ├── steam_2025_5k-dataset-games_20250831.json.gz     # 5K sample (102MB)
│   └── steam_2025_5k-dataset-reviews_20250901.json.gz   # Sample reviews (45MB)
├── 📁 02_processed/              # Cleaned and enriched data
│   ├── README.md                 # Processed data documentation
│   └── steam_2025_5k-dataset-enriched_20250901.json     # Enhanced sample (85MB)
└── 📋 README.md                  # This file

FUTURE: Zenodo Full Dataset (4.2GB total)
├── 🎮 steam_games_master.json           # Complete games catalog (2.8GB)
├── 📝 steam_reviews_master.json         # Complete review collection (1.4GB)
├── 🧠 steam_embeddings_master.json      # Vector embeddings (600MB)
└── 📊 steam_sample_5k.json              # Sample subset for reference
```

### Navigation Guide

- [📁 Raw Data Directory](01_raw/README.md) - Original Steam API responses and collection metadata
- [📁 Processed Data Directory](02_processed/README.md) - Cleaned, enriched, and analysis-ready formats

---

## 🚀 Quick Access Guide

### For Immediate Evaluation (GitHub)

Sample Dataset - Ready for Download:

- 🎮 Games Sample: [steam_2025_5k-dataset-games_20250831.json.gz](01_raw/steam_2025_5k-dataset-games_20250831.json.gz) (102MB)
- 📝 Reviews Sample: [steam_2025_5k-dataset-reviews_20250901.json.gz](01_raw/steam_2025_5k-dataset-reviews_20250901.json.gz) (45MB)
- 📊 Enhanced Sample: [steam_2025_5k-dataset-enriched_20250901.json](02_processed/steam_2025_5k-dataset-enriched_20250901.json) (85MB)

Quick Start:

```bash
# Download sample dataset
wget https://github.com/VintageDon/steam-dataset-2025/raw/main/data/01_raw/steam_2025_5k-dataset-games_20250831.json.gz

# Decompress for analysis
gunzip steam_2025_5k-dataset-games_20250831.json.gz

# Ready for analysis!
```

### For Complete Research (Zenodo - Planned)

Full Dataset Specifications:

- 📊 Total Size: 4.2GB (complete Steam ecosystem)
- 🎮 Applications: 239,664 complete catalog entries
- 📝 Reviews: 1,048,148 user reviews  
- 🧠 Embeddings: 1024-dimensional semantic vectors
- 📅 Release: Pending completion of documentation and embedding generation

Access Information:

- 🏛️ Archive: Zenodo academic repository (planned)
- 🔗 DOI: Persistent identifier for academic citation (pending)
- 📋 Notification: GitHub repository updates when available

---

## 📊 Dataset Specifications

### Sample Dataset (Currently Available)

| Component | Records | Compressed Size | Uncompressed | Content |
|---------------|-------------|-------------------|------------------|-------------|
| Games Sample | 5,000 applications | 102MB | ~250MB | Complete metadata, JSONB fields |
| Reviews Sample | ~50,000 reviews | 45MB | ~120MB | User reviews for sample games |
| Enhanced Sample | 5,000 applications | N/A | 85MB | Processed with analytics features |

### Full Dataset (Zenodo Release)

| Component | Records | Estimated Size | Content |
|---------------|-------------|-------------------|-------------|
| Complete Games | 239,664 applications | 2.8GB | Full Steam catalog metadata |
| Complete Reviews | 1,048,148 reviews | 1.4GB | User reviews across all collected games |
| Vector Embeddings | 239,664 vectors | 600MB | 1024-dimensional semantic embeddings |
| Total Dataset | Complete ecosystem | 4.2GB | Comprehensive Steam analytics platform |

### Data Quality Metrics

| Quality Measure | Sample Dataset | Full Dataset | Notes |
|---------------------|-------------------|------------------|-----------|
| API Success Rate | 56% (demonstration) | 90.6% (systematic) | Sample designed for variety, full optimized for coverage |
| Metadata Completeness | 100% basic fields | 100% basic fields | All records include core identification |
| Pricing Information | ~60% coverage | ~60% coverage | Free games have no pricing data |
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
    "api_success_rate": "56%",
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
| [Quick Start Guide](../docs/quick-start.md) | 30-minute setup to first analysis | Perfect for new users |
| [Dataset Card](../paper/dataset-card.md) | Complete academic datasheet | Required for academic applications |

### Technical Resources

| Resource | Content | Audience |
|--------------|-------------|--------------|
| [Multi-Modal Architecture](../docs/methodologies/multi-modal-architecture.md) | Database schema and design rationale | Technical implementers |
| [Vector Embeddings](../docs/methodologies/vector-embeddings.md) | Semantic search implementation | ML engineers |
| [ETL Pipeline](../docs/methodologies/etl-pipeline.md) | Complete processing methodology | Data engineers |

---

## 🤝 Support & Contribution

### Getting Help

- 🐛 Data Issues: [GitHub Issues](https://github.com/VintageDon/steam-dataset-2025/issues) with specific file and error information
- 📧 General Questions: Check [Documentation Hub](../docs/README.md) first for existing answers
- 🎓 Academic Inquiries: Reference [Dataset Card](../paper/dataset-card.md) for comprehensive information

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
