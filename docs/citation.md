<!--
---
title: "Steam Dataset 2025: Citation & Licensing Guide"
description: "Academic citation formats, DOI information, version tracking, and licensing terms for the Steam Dataset 2025 project"
author: "VintageDon"
orcid: "0009-0008-7695-4093"
created: "2025-09-07"
last_updated: "2025-10-06"
version: "2.0"
tags: ["citation", "licensing", "academic", "dataset", "steam", "zenodo", "doi"]
category: "documentation"
status: "active"
---
-->

# 📚 **Steam Dataset 2025: Citation & Licensing Guide**

This document provides official citation formats, DOI information, version tracking, and licensing terms for the Steam Dataset 2025. It ensures proper attribution and clarifies usage rights for researchers, data scientists, and academic institutions working with this dataset.

---

## **1. Introduction**

### **1.1 Purpose**

This guide establishes standardized citation formats for academic and professional use of the Steam Dataset 2025, provides official DOI information for permanent reference, clarifies licensing terms for dataset and code, and tracks version information to ensure reproducible research practices and proper attribution.

### **1.2 Scope**

**What's Covered:**

- Official Zenodo DOI and citation formats
- Academic citation formats (APA, IEEE, Chicago) for papers and publications
- Software repository citation guidelines
- Licensing terms: CC BY 4.0 for dataset, MIT for code
- Version tracking and release information
- Attribution requirements for derivative works

### **1.3 Target Audience**

**Primary Users:** Academic researchers, data scientists publishing papers, students conducting research  
**Secondary Users:** Industry practitioners, Kaggle competitors, open source contributors  
**Background Assumed:** Basic familiarity with academic citation practices, DOI systems, and open source licensing

### **1.4 Overview**

The Steam Dataset 2025 is officially published on Zenodo: version 1.0.0 carries DOI 10.5281/zenodo.17266923 (concept DOI 10.5281/zenodo.17266922 for version-agnostic references) and is also mirrored on Kaggle. This document provides the citation formats needed for academic papers, clarifies the dual licensing structure (CC BY 4.0 for data, MIT for code), and tracks version information for reproducibility.

---

## **2. Official Dataset Citation**

This section provides the primary citation formats using the official Zenodo DOI. These formats should be used for all academic publications, research papers, and professional references to the dataset.

### **2.1 Zenodo Citation (Primary)**

The official Zenodo citation with DOI is the preferred format for academic publications and ensures permanent accessibility through archival preservation.

**APA Format (7th Edition):**

```markdown
Fountain, D. (2025). Steam Dataset 2025: A large-scale, multi-modal dataset of the Steam 
gaming platform [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.17266922
```

**IEEE Format:**

```markdown
D. Fountain, "Steam Dataset 2025: A large-scale, multi-modal dataset of the Steam gaming 
platform," Zenodo, 2025. [Online]. Available: https://doi.org/10.5281/zenodo.17266922
```

**Chicago Format (17th Edition):**

```markdown
Fountain, Donald. "Steam Dataset 2025: A Large-Scale, Multi-Modal Dataset of the Steam 
Gaming Platform." Zenodo, 2025. https://doi.org/10.5281/zenodo.17266922.
```

**BibTeX Entry:**

```bibtex
@dataset{fountain_2025_steam,
  author       = {Fountain, Donald},
  title        = {{The Steam Dataset 2025: A Large-Scale, Multi-Modal 
                    Dataset of the Steam Gaming Platform}},
  year         = 2025,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.17266923},
  url          = {https://doi.org/10.5281/zenodo.17266923}
}
```

### **2.2 ORCID Integration**

For academic submissions requiring ORCID identification:

**Author ORCID:** `0009-0008-7695-4093`  
**ORCID Profile:** <https://orcid.org/0009-0008-7695-4093>

**Enhanced Citation with ORCID (APA):**

```markdown
Fountain, D. (ORCID: 0009-0008-7695-4093). (2025). Steam Dataset 2025: A large-scale, 
multi-modal dataset of the Steam gaming platform [Dataset]. Zenodo. 
https://doi.org/10.5281/zenodo.17266922
```

### **2.3 DOI Badge**

For inclusion in presentations, papers, or websites:

**Markdown Badge:**

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17266922.svg)](https://doi.org/10.5281/zenodo.17266922)
```

**HTML Badge:**

```html
<a href="https://doi.org/10.5281/zenodo.17266922">
  <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.17266922.svg" alt="DOI">
</a>
```

---

## **3. Repository & Code Citation**

This section provides citation formats for referencing the GitHub repository, data collection scripts, analytics framework, or technical methodology implementations.

### **3.1 GitHub Repository Citation**

Use this format when citing the repository itself, implementation code, or methodology documentation rather than the dataset.

**APA Format:**

```markdown
Fountain, D. (2025). Steam Dataset 2025: Data collection and analytics framework 
(Version 1.0.0) [Computer software]. GitHub. 
https://github.com/VintageDon/steam-dataset-2025
```

**IEEE Format:**

```markdown
D. Fountain, "Steam Dataset 2025: Data collection and analytics framework," 
Version 1.0.0, GitHub, 2025. [Online]. Available: 
https://github.com/VintageDon/steam-dataset-2025
```

### **3.2 Data Package Citations**

Different citation formats for specific data package types when users work with particular dataset variants.

**CSV Package Citation:**

```markdown
Fountain, D. (2025). Steam Dataset 2025: Accessibility CSV package [Data files]. 
Zenodo. https://doi.org/10.5281/zenodo.17266922
```

**SQL Database Dump Citation:**

```markdown
Fountain, D. (2025). Steam Dataset 2025: PostgreSQL database dump [Database]. 
Zenodo. https://doi.org/10.5281/zenodo.17266922
```

**Vector Embeddings Package Citation:**

```markdown
Fountain, D. (2025). Steam Dataset 2025: Pre-computed vector embeddings (BGE-M3) 
[Data files]. Zenodo. https://doi.org/10.5281/zenodo.17266922
```

### **3.3 Kaggle Dataset Citation**

Citation format for the Kaggle-published version of the dataset.

**Status:** Published
**Kaggle URL:** https://www.kaggle.com/datasets/crainbramp/steam-dataset-2025-multi-modal-gaming-analytics

**Kaggle Citation:**

```markdown
Fountain, D. (2025). Steam Dataset 2025 [Dataset]. Kaggle. 
https://www.kaggle.com/datasets/crainbramp/steam-dataset-2025-multi-modal-gaming-analytics
```

---

## **4. Licensing & Usage Rights**

This section outlines the dual licensing structure: Creative Commons Attribution 4.0 International (CC BY 4.0) for the dataset and documentation, and MIT License for code and scripts.

### **4.1 Dataset License: CC BY 4.0**

The Steam Dataset 2025 data files and documentation are released under Creative Commons Attribution 4.0 International License.

**License:** CC BY 4.0  
**License URL:** <https://creativecommons.org/licenses/by/4.0/>

**What's Covered:**

- All data files (CSV, SQL dumps, NPY embeddings)
- Documentation (README files, methodology docs, data dictionary)
- Jupyter notebooks and analytical reports

**Permissions:**

- ✅ Share: Copy and redistribute in any medium or format
- ✅ Adapt: Remix, transform, and build upon the material
- ✅ Commercial use: Use for commercial purposes
- ✅ No additional restrictions: Cannot apply legal or technological measures that restrict others

**Requirements:**

- 📋 **Attribution:** Must give appropriate credit, provide link to license, and indicate if changes were made
- 📋 **No additional restrictions:** Cannot apply terms that legally restrict others from doing anything the license permits

**Limitations:**

- ❌ No warranties: Dataset provided "as-is" without warranties of any kind
- ❌ Liability: Author not liable for any claims arising from use

### **4.2 Code License: MIT**

The code, scripts, and software implementations are released under the MIT License.

**License:** MIT License  
**License URL:** <https://opensource.org/licenses/MIT>

**What's Covered:**

- Python data collection scripts
- SQL schema creation scripts
- Database processing utilities
- Analysis and visualization code

**Permissions:**

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

**Requirements:**

- 📋 Include license and copyright notice
- 📋 Provide attribution to original authors

**Limitations:**

- ❌ No warranty or liability coverage
- ❌ No trademark rights granted

### **4.3 Attribution Requirements**

Minimum attribution required for all uses of the Steam Dataset 2025:

**Short Form (for space-constrained contexts):**

```markdown
Steam Dataset 2025 by Donald Fountain (https://doi.org/10.5281/zenodo.17266922)
Licensed under CC BY 4.0
```

**Full Form (for papers and documentation):**

```markdown
Steam Dataset 2025: A Large-Scale, Multi-Modal Dataset of the Steam Gaming Platform
Author: Donald Fountain (ORCID: 0009-0008-7695-4093)
DOI: 10.5281/zenodo.17266923 (version) / 10.5281/zenodo.17266922 (concept)
License: CC BY 4.0 (dataset), MIT (code)
Repository: https://github.com/VintageDon/steam-dataset-2025
```

### **4.4 Steam Data Usage Considerations**

The dataset contains data collected from Steam's public APIs under their terms of service. Users should be aware of additional considerations when using Steam-sourced data.

**Steam Terms Compliance:**

- Data collected using official Steam Web API
- Respects Steam's rate limiting and usage guidelines  
- Collected from Steam's public APIs; review records include author account identifiers, and the redistribution scope of Steam-origin content is under review
- No private user data beyond what Steam's public APIs expose
- No redistribution of Steam's proprietary assets or copyrighted content

**Recommended Practice:** Users conducting research or building applications on this dataset should familiarize themselves with Steam's current API Terms of Use at <https://steamcommunity.com/dev>.

---

## **5. Version Information & Release Status**

This section tracks dataset versions, release dates, and package availability to support reproducible research and proper version citation.

### **5.1 Current Release Information**

**Dataset Version:** 1.0.0  
**Release Date:** October 5, 2025  
**Collection Period:** August - September 2025  
**Database Snapshot Date:** September 29, 2025

**Zenodo Record:**

- **Version DOI:** 10.5281/zenodo.17266923 (cite this for v1.0.0)
- **Concept DOI:** 10.5281/zenodo.17266922 (version-agnostic references)
- **Status:** ✅ Published and archived
- **Preservation:** Permanent archival storage

**GitHub Repository:**

- **Repository:** <https://github.com/VintageDon/steam-dataset-2025>
- **Status:** ✅ Active development and maintenance
- **Latest Release:** v1.0.0

**Kaggle Dataset:**

- **Status:** ✅ Published
- **URL:** https://www.kaggle.com/datasets/crainbramp/steam-dataset-2025-multi-modal-gaming-analytics

### **5.2 Data Packages Available**

Current release includes four official packages (sizes verified against the Zenodo record, 2026-11-13):

| **Package** | **Size (bytes)** | **Format** | **Use Case** | **Status** |
|-------------|------------------|------------|--------------|------------|
| `steam-dataset-2025-v1.zip` | 40,212,720 | ZIP bundle | Documentation, notebooks, notebook data | ✅ Available |
| `steam_dataset_2025_csv_package_v1.zip` | 320,368,878 | ZIP of CSVs | No database setup required | ✅ Available |
| `steam_dataset_2025_power_users_dump_v1.zip` | 7,204,002,678 | PostgreSQL dump | Complete database restoration | ✅ Available |
| `steam_dataset_2025_embeddings_package_v1.zip` | 4,870,419,373 | Embeddings package | ML/AI applications | ✅ Available |

### **5.3 Dataset Specifications**

**Coverage Statistics:**

- **Total Applications:** 239,664 (packaging-time record)
- **Games:** ~150,300 games with type=game (measured 2026-08-03)
- **Reviews:** 1,048,148 reviews in a bounded per-application sample
- **Temporal Coverage:** release dates as recorded by Steam (1969–9998 incl. sentinel values; filter explicitly)
- **Vector Embeddings:** 1024-dimensional BGE-M3 embeddings
- **Database Technology:** PostgreSQL 16.14 with pgvector 0.8.0 (collection database, measured 2026-08-03)

**Quality Metrics:**

- **Raw collection outcome:** 239,341 successful retrievals across 262,791 retained result records (record-level; see [collection-outcomes.json](release-1.0.1/collection-outcomes.json))
- **Data Completeness:** metadata fields carry meaningful NULLs (missing values are never defaulted); see the known-limitations reference
- **Review Coverage:** bounded sample of up to 100 most recent reviews per covered application

### **5.4 Version Citation Guidelines**

For reproducibility, always cite the specific version used in your research:

**APA Format with Version:**

```markdown
Fountain, D. (2025). Steam Dataset 2025: A large-scale, multi-modal dataset of the 
Steam gaming platform (Version 1.0.0) [Dataset]. Zenodo. 
https://doi.org/10.5281/zenodo.17266922
```

**In-Text Version Reference:**

```markdown
Analysis performed using Steam Dataset 2025 v1.0.0 (database snapshot: 2025-09-29) 
[Citation].
```

---

## **6. References & Related Resources**

### **6.1 Internal References**

| **Document Type** | **Title** | **Relationship** | **Link** |
|-------------------|-----------|------------------|----------|
| Repository README | Main Documentation | Complete dataset overview and features | [README.md](https://github.com/VintageDon/steam-dataset-2025/blob/main/README.md) |
| Data Dictionary | Complete Schema Documentation | Full database schema and field definitions | [DATA_DICTIONARY.md](https://github.com/VintageDon/steam-dataset-2025/blob/main/steam-dataset-2025-v1/DATA_DICTIONARY.md) |
| Methodology | Steam API Collection | Data collection procedures and quality | [steam-api-collection.md](https://github.com/VintageDon/steam-dataset-2025/blob/main/docs/methodologies/steam-api-collection.md) |
| Methodology | Data Validation & QA | Quality assurance procedures | [data-validaton-and-qa.md](https://github.com/VintageDon/steam-dataset-2025/blob/main/docs/methodologies/data-validaton-and-qa.md) |
| Analytics | Platform Evolution Analysis | Comprehensive dataset analysis | [steam-5k-dataset-analysis.md](https://github.com/VintageDon/steam-dataset-2025/blob/main/docs/analytics/steam-5k-dataset-analysis.md) |

### **6.2 External Resources**

| **Resource Type** | **Title** | **Description** | **Link** |
|-------------------|-----------|-----------------|----------|
| Archive | Zenodo Dataset Record | Permanent archival version with DOI | [doi.org/10.5281/zenodo.17266922](https://doi.org/10.5281/zenodo.17266922) |
| Official API | Steam Web API Documentation | Source data API reference | [steamcommunity.com/dev](https://steamcommunity.com/dev) |
| Database | PostgreSQL 16 Documentation | Database engine documentation | [postgresql.org/docs/16/](https://www.postgresql.org/docs/16/) |
| Extension | pgvector Documentation | Vector operations and similarity search | [github.com/pgvector/pgvector](https://github.com/pgvector/pgvector) |
| ML Model | BGE-M3 Embeddings | Multilingual embedding model used | [huggingface.co/BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) |
| Historical Reference | Kaggle Steam Dataset (2019) | Original Nik Davis dataset | [kaggle.com/datasets/nikdavis/steam-store-games](https://www.kaggle.com/datasets/nikdavis/steam-store-games) |

---

## **7. Documentation Metadata**

### **7.1 Change Log**

| **Version** | **Date** | **Changes** | **Author** |
|------------|----------|-------------|------------|
| 1.0 | 2025-09-07 | Initial citation guide creation with ORCID and Zenodo integration | VintageDon |
| 2.0 | 2025-10-06 | Updated with official Zenodo DOI, dual licensing clarification, version 1.0.0 release info | VintageDon |
| 2.1 | 2026-11-13 | Truth patch: DOI typo corrected (version/concept classes distinguished), Kaggle citation filled in, official package table with verified bytes, population figures corrected to packaging-time records | VintageDon |

### **7.2 Authorship & Collaboration**

**Primary Author:** VintageDon ([GitHub Profile](https://github.com/VintageDon))  
**ORCID:** 0009-0008-7695-4093 ([ORCID Profile](https://orcid.org/0009-0008-7695-4093))  
**AI Assistance:** Claude Sonnet 4 for document structure and citation format validation  
**Methodology:** Request-Analyze-Verify-Generate-Validate-Reflect (RAVGVR) collaborative approach  
**Quality Assurance:** All citation formats validated against APA 7th, IEEE, and Chicago 17th edition standards

---

*Document Version: 2.1 | Last Updated: 2026-11-13 | Status: Active*

---

Tags: citation, licensing, academic, dataset, steam, zenodo, doi, cc-by-4.0, mit-license, reproducibility
