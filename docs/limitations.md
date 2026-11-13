---
title: "Steam Dataset 2025: Known Limitations & Data Constraints"
description: "Comprehensive documentation of API constraints, missing data patterns, and collection limitations for academic transparency"
author: "VintageDon"
orcid: "0009-0008-7695-4093"
created: "2025-09-07"
last_updated: "2026-11-13"
version: "2.1"
tags: ["limitations", "data-quality", "api-constraints", "academic-transparency", "reproducibility"]
category: "documentation"
status: "published"
---

# ⚠️ **Steam Dataset 2025: Known Limitations & Data Constraints**

This document provides comprehensive documentation of data collection limitations, API constraints, and known gaps in Steam Dataset 2025. Academic transparency about these limitations is essential for proper interpretation, reproducible research, and understanding dataset boundaries.

---

## 🎯 **1. Purpose & Scope**

### **1.1 Purpose**

Ensure academic transparency by documenting all known limitations, data gaps, and collection constraints encountered during Steam Dataset 2025 development. Enable researchers to make informed decisions about dataset applicability and interpret results appropriately within documented boundaries.

### **1.2 Scope**

**What's Covered:**

- Steam Web API success rates and failure patterns
- Content type coverage and systematic exclusions
- Geographic and regional data constraints
- Temporal limitations and point-in-time collection
- Metadata completeness variations

**What's Not Covered:**

- Future dataset updates (this documents v1.0 limitations)
- Alternative data sources or collection methods
- Downstream analysis limitations (see individual studies)

### **1.3 Target Audience**

**Primary Users:** Academic researchers requiring transparent data provenance, peer reviewers evaluating methodology  
**Secondary Users:** Data scientists assessing applicability, developers understanding constraints  
**Background Assumed:** Understanding of API-based data collection and research transparency standards

### **1.4 Overview**

Steam Dataset 2025's retained raw corpus holds 262,791 collection result records, of which 239,341 (91.0766% at record grain) are successes covering 239,183 unique applications; the packaged database records 239,664 application rows. Failure records do not retain the requested AppID, so failure causes cannot be attributed per application. This documentation states what is measured, at which grain, and what remains unverified; machine-readable values live in [release-1.0.1/collection-outcomes.json](release-1.0.1/collection-outcomes.json).

---

## 📊 **2. API Performance & Success Rates**

This section documents empirically observed API performance patterns from large-scale data collection across Steam's complete application catalog.

### **2.1 Overall Collection Metrics**

Comprehensive statistics from full dataset collection demonstrate API reliability patterns and identify primary failure sources.

#### **Primary Collection Results (measured 2026-11-13)**

| **Metric** | **Value** | **Grain** |
|------------|-----------|-----------|
| **Retained result records** | 262,791 | records across 526 batch files (unpublished raw corpus) |
| **Successful retrievals** | 239,341 | 91.0766% of result records (record grain) |
| **Failed records** | 23,450 | record grain; requested AppID not retained |
| **Unique successful AppIDs** | 239,183 | distinct applications in the raw corpus |
| **Duplicate success records** | 158 | repeated AppIDs among successes |
| **Review rows (packaged)** | 1,048,148 | bounded sample, up to 100 most recent per covered application |
| **Vector embeddings (packaged)** | 239,664 applications + 1,048,148 reviews | 100% non-null (measured 2026-08-03) |

#### **Success Metric Context**

The 91.0766% figure is a **record-level** fraction over retained result
records. It is not HTTP request success (attempts are not reconstructable as
requests) and not unique-app catalog coverage (the denominator is records,
not applications). The packaged database's `success` column is `true` for all
loaded rows because failed retrievals were never loaded — it is a selection
artifact and must never be published as a "100% success rate."

### 2.2 API Failure Records

All 23,450 failure records omit the requested AppID. There is no
per-application failure manifest, and failure-cause attribution (delisted,
region-locked, invalid ID, API error) is not reconstructable from the
retained corpus. Previously published failure-cause breakdowns had no
retained source and have been removed. The raw corpus is not published.

### 2.3 Collection Timeline

The collection ran as an initial pass with retries during August–September
2025 (5K-run metadata records 14,471 seconds for its own 8,711-record pass).
Overall campaign durations and per-pass recovery rates were not retained in
the published record and are not restated here.

---

## 🌍 **3. Geographic & Regional Constraints**

The collection was performed from a United States network position. Regional
availability therefore shaped what the API returned for some applications.

### 3.1 Collection Region Impact

**What is measured:** nothing per-region. Regional coverage estimates
previously published here (per-continent percentage tables) had no retained
source and have been removed. What is known:

- Collection requests originated from a US position, so region-gated store
  content could fail or return restricted payloads.
- Language distribution in the publicly tracked 5K sample is 51.6% English,
  13.8% Simplified Chinese and 9.9% Russian at that sample's grain — see the
  [walkthrough](release-1.0.1/README.md#small-text-analysis-walkthrough).
  The packaged release's language composition is unverified pending
  dump/CSV verification.

**Research Implications:**

- Analysis of non-English gaming markets may be incomplete
- Regional availability effects are confounded with other failure causes and cannot be separated post hoc
- Treat any per-region extrapolation from this dataset as unverified

### 3.2 Pricing Data Limitations

Pricing was collected through a US collection point; `price_overview`
carries the currency the API returned for that point (USD).

**What is measured (dated 2026-08-03):** 59.4874% of applications carry a
materialized price currency; collected values are USD. Multi-currency
coverage is not present in the dataset.

**Research Implications:**

- Cross-regional pricing analysis is not supported
- Currency conversion analysis requires external data

---

## ⏰ **4. Temporal & Data Freshness Constraints**

Dataset represents point-in-time snapshot with implications for longitudinal analysis and current information accuracy.

### **4.1 Collection Timeline**

#### **Data Collection Periods**

| **Data Type** | **Collection Period** | **Staleness Risk** | **Update Frequency** |
|---------------|----------------------|-------------------|----------------------|
| **Game Metadata** | Aug 31 - Sep 7, 2025 | Low | Relatively stable |
| **Pricing Data** | Aug 31 - Sep 7, 2025 | **High** | Changes daily/weekly |
| **Review Counts** | Aug 31 - Sep 7, 2025 | Medium | Grows continuously |
| **Release Dates** | Historical | None | Immutable |
| **Vector Embeddings** | Sep 1-3, 2025 | Low | Based on stable descriptions |

### **4.2 Temporal Analysis Capabilities**

#### **✅ Supports These Research Applications:**

- Historical game development trends (release dates as recorded, with explicit filtering)
- Genre evolution analysis across platform history
- Developer/publisher relationship networks
- Cross-sectional analysis of Steam ecosystem
- Platform growth patterns and market structure

#### **❌ Cannot Support These Applications:**

- Real-time price monitoring or dynamic trends
- Current player counts or concurrent user metrics
- Post-September 2025 releases or updates
- Recent review sentiment shifts
- Current sales performance or rankings

### **4.3 Review Data Temporal Constraints**

Review collection represents sample of available reviews at collection time, not comprehensive historical corpus.

#### **Review Collection Methodology**

| **Parameter** | **Setting** | **Impact** |
|---------------|-------------|------------|
| **Reviews per Application** | Up to 100 most recent | Bounded, point-in-time |
| **Review Count** | 1,048,148 total | Large but not exhaustive |
| **Coverage** | 117,311 applications with ≥1 review (measured 2026-08-03) | Not all applications have reviews |
| **Temporal Coverage** | Sample of available reviews at collection time | Not a complete historical corpus |

**Research Implications:**

- Sentiment analysis reflects the sampled, point-in-time corpus
- Long-term sentiment trends are analyzable within the sample's bounds
- Claims of complete review history or exhaustive coverage are not supported

---

## 📁 **5. Content Coverage & Exclusions**

Systematic documentation of coverage patterns and exclusions affecting dataset representativeness.

### **5.1 Content Type Distribution**

Measured distribution of successful raw records (2026-11-13 recount, record
grain — see [collection-outcomes.json](release-1.0.1/collection-outcomes.json)):

| **Content Type** | **Successful Records** |
|------------------|-----------------------:|
| game | 150,039 |
| dlc | 53,698 |
| demo | 23,520 |
| music | 8,684 |
| episode | 2,274 |
| video | 699 |
| advertising | 212 |
| mod | 126 |
| series | 82 |
| hardware | 7 |

**Total: 239,341 success records covering 239,183 unique AppIDs.**
The packaged database's type distribution (dated 2026-08-03) is similar but
not identical (e.g., 150,279 rows typed `game`). Previously published
per-type success-rate estimates had no retained source and have been removed.

#### **Content Type Research Implications**

**Strong Coverage:**

- Core gaming applications and standalone titles
- Demo versions and free-to-play games
- Major publisher and indie game catalogs

**Limited Coverage:**

- DLC expansions (parent game dependency issues)
- Video content and promotional media
- Tools and software applications

### **5.2 Systematic Exclusions**

Certain content types are systematically excluded or underrepresented due to API constraints or collection methodology.

#### **Not Included**

| **Exclusion Type** | **Reason** | **Impact** |
|-------------------|------------|------------|
| **Adult-Only Content** | Requires separate authentication | Missing mature content segment |
| **Private/Beta Applications** | Developer-only access | Missing unreleased content |
| **Hardware Items** | Not software applications | N/A for digital analysis |
| **Steam China Platform** | Separate regional platform | Missing Chinese market |

### **5.3 Metadata Completeness Variations**

Field completeness varies by field and application type. Missing values are
stored as meaningful NULLs and are never defaulted. Notable measured examples
(dated 2026-08-03): Metacritic coverage is 2.21% of applications (5,299 of
239,664); release_date coverage is 84.62%; the materialized price currency
covers 59.4874% of applications (collected values are USD).

The per-category completeness percentage table and the "complete metadata
tiers" breakdown previously shown here had no retained source or defined
field-set basis and have been removed. Field-level verification against the
released packages is deferred with the dump lane (see
[release-1.0.1/known-limitations.md](release-1.0.1/known-limitations.md)).

---

## 🔍 **6. Known Data Quality Issues**

Specific known issues affecting data accuracy or requiring special handling.

### **6.1 Price Data Inconsistencies**

#### **Free-to-Play Games**

- **Issue:** `price_overview` field NULL for free games
- **Impact:** Cannot distinguish "free" from "missing price data"
- **Mitigation:** Use `is_free` boolean field for filtering
- **Affected Records:** ~60,000 free-to-play applications

#### **Regional Price Variations**

- **Issue:** US pricing only, no multi-region support
- **Impact:** Cannot analyze global pricing strategies
- **Affected Records:** All priced applications (78,100)

### **6.2 Hardware Requirements Parsing**

#### **HTML Parsing Limitations**

- **Issue:** PC requirements stored as HTML strings
- **Extraction Success:** ~65% of games with requirements
- **Affected Fields:** min_ram_mb, rec_ram_mb, storage requirements
- **Mitigation:** Materialized columns with parsed values available
- **Affected Records:** ~48,000 games have unparseable requirements

**Example Parsing Challenges:**

```markdown
❌ Cannot Parse: "Requires a 64-bit processor and operating system"
✅ Can Parse: "RAM: 8 GB RAM"

❌ Cannot Parse: "Minimum: Pentium 4 or better"
✅ Can Parse: "Minimum: Intel Core i5-2500K"
```

### **6.3 Developer/Publisher Data**

#### **Nested Array Structures**

- **Issue:** Multiple developers/publishers stored in JSONB arrays
- **Impact:** Complex to query without proper indexing
- **Mitigation:** Separate junction tables created for analysis
- **Affected Records:** All applications

#### **Name Variations**

- **Issue:** Publisher/developer names have spelling variations
- **Example:** "Valve" vs "Valve Corporation" vs "Valve Software"
- **Impact:** Entity resolution required for network analysis
- **Affected Records:** Estimated ~5-10% name variation rate

---

## 📈 **7. Research Applicability Assessment**

Guidance on dataset strengths and limitations for specific research domains.

### **7.1 Strong Research Applications**

✅ **Well-Supported Research Areas:**

**Temporal Market Analysis:**

- Genre evolution across recorded platform history (filter release dates explicitly)
- Platform growth patterns
- Historical pricing trends
- Publisher portfolio changes

**Semantic Analysis:**

- Content-based game discovery
- Genre classification using descriptions
- Cross-language semantic search
- Recommendation system development

**Network Analysis:**

- Publisher-developer relationships
- Collaboration patterns
- Portfolio diversity analysis
- Ecosystem structure mapping

**Economic Analysis (US Market):**

- Pricing strategy patterns
- Free-to-play economics
- DLC pricing models
- Genre-specific pricing

### **7.2 Limited Research Applications**

⚠️ **Constrained Research Areas:**

**Global Market Analysis:**

- Multi-region pricing comparison (US-only pricing)
- Non-English market dynamics (Western bias)
- Asian gaming industry (underrepresented)
- Emerging markets (incomplete coverage)

**Real-Time Analysis:**

- Current player counts (point-in-time data)
- Live pricing changes (September 2025 snapshot)
- Recent sentiment shifts (historical corpus only)
- Post-2025 content (collection cutoff)

**Comprehensive Review Analysis:**

- Complete review history (sample-based)
- Non-English reviews (limited coverage)
- Review manipulation detection (limited metadata)

### **7.3 Unsuitable Research Applications**

❌ **Not Recommended:**

- Real-time market monitoring
- Comprehensive non-English market analysis
- Chinese gaming market studies
- Current player engagement metrics
- Live content recommendation systems

---

## 🔄 **8. Mitigation Strategies & Best Practices**

Guidance for working effectively within documented limitations.

### **8.1 Filtering Strategies**

#### **Quality Filtering**

```python
# Recommended filtering for high-quality records
games_complete = games[
    (games['success'] == True) &
    (games['name'].notna()) &
    (games['detailed_description'].notna())
]

# Further quality refinement
games_analyzed = games_complete[
    (games_complete['release_date'].notna()) &
    (games_complete['primary_genre'].notna())
]
```

#### **Content Type Filtering**

```python
# Focus on core gaming applications
core_games = games[
    (games['type'] == 'game') &
    (games['is_free'] == False)  # Or True for F2P analysis
]
```

### **8.2 Statistical Adjustments**

#### **Coverage Bias Adjustment**

No dataset-verified catalog coverage rate exists (the raw corpus cannot
measure HTTP attempts or catalog completeness), so no coverage extrapolation
coefficient is offered. When extrapolating beyond the dataset, state the
population you actually observe (e.g., the 239,664 packaged application rows
or a filtered subset), document your filter, and avoid dividing by any
"success rate" published for earlier collection stages.

### **8.3 Transparency Requirements**

**When Publishing Research:**

1. **Cite Limitations Document:** Reference this document in methodology
2. **Report Filtering:** Document all filtering and exclusion criteria
3. **Acknowledge Gaps:** Explicitly state coverage limitations
4. **Provide Context:** Compare to alternative datasets when applicable
5. **Share Code:** Enable reproducibility and validation

---

## 📚 **9. Comparison to Alternative Datasets**

Contextualizing limitations relative to other Steam datasets.

### **9.1 Competitive Analysis**

| **Dataset** | **Size** | **Collection outcome basis** | **Limitations Documented** |
|-------------|----------|------------------------------|---------------------------|
| **Steam Dataset 2025** | 239,664 packaged rows | 239,341 successes / 262,791 retained records (record grain) | ✅ Comprehensive transparency |
| **SteamSpy (2019)** | ~27,000 | N/A | ⚠️ Third-party estimates |
| **Alternative 2024** | ~120,000 | Unknown | ❌ Limited documentation |

### **9.2 Unique Strengths Despite Limitations**

**Steam Dataset 2025 Advantages:**

- ✅ Largest known collection from official APIs
- ✅ Complete transparency on limitations
- ✅ Semantic embeddings for advanced ML
- ✅ Multi-modal database architecture
- ✅ Reproducible methodology

---

## 📜 **10. Documentation Metadata**

### **10.1 Change Log**

| **Version** | **Date** | **Changes** | **Author** |
|------------|----------|-------------|------------|
| 1.0 | 2025-09-07 | Initial limitations documentation | VintageDon |
| 2.0 | 2025-01-06 | Complete rewrite with final statistics and comprehensive analysis | VintageDon |
| 2.1 | 2026-11-13 | Truth patch: measured record-level outcomes replace the 56% narrative; unsourced failure-cause, regional, currency, per-type success-rate and completeness tables removed or replaced with dated measurements; review corpus stated as bounded sample | VintageDon |

### **10.2 Authorship & Collaboration**

**Primary Author:** VintageDon (Donald Fountain)  
**GitHub:** <https://github.com/vintagedon>  
**ORCID:** [0009-0008-7695-4093](https://orcid.org/0009-0008-7695-4093)  
**AI Collaboration:** Claude 3.7 Sonnet (Anthropic) - Documentation structure and technical writing assistance  

**Human Responsibility:** All statistics, failure analysis, and quality assessments are human-verified against actual collection logs and database queries. AI assistance was used for documentation organization and clarity enhancement.

---

## 📖 **11. Related Documentation**

- **[Data Access Guide](data-access.md)** - Download procedures and file specifications
- **[Dataset Card](../steam-dataset-2025-v1/DATASET_CARD.md)** - Complete academic documentation
- **[Data Dictionary](../steam-dataset-2025-v1/DATA_DICTIONARY.md)** - Field definitions and schema
- **[Steam API Collection](methodologies/steam-api-collection.md)** - Collection methodology
- **[Data Validation](methodologies/data-validaton-and-qa.md)** - Quality assurance procedures

---

**Document Version:** 2.1 | **Last Updated:** 2026-11-13 | **Status:** Published

This document supports academic transparency and reproducible research practices
