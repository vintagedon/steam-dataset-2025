# 🧹 **Processed Data Directory**

This directory contains cleaned, validated, and quality-checked Steam application data ready for enrichment and analysis. Raw JSON data from the Steam API has been normalized, validated against schema requirements, and organized into structured formats that support both relational database operations and analytical workflows.

## **Overview**

The processed data tier represents the first transformation stage in the Steam Dataset 2025 pipeline. Data here has undergone validation, deduplication, and quality checks to ensure consistency and reliability. Failed API requests have been filtered out, JSONB structures have been validated, and records are enriched with success indicators that enable analysts to distinguish between complete and partial data. This tier serves as the foundation for vector embedding generation, materialized column creation, and final analytical dataset preparation.

---

## 📁 **Directory Contents**

This section documents the structure and purpose of processed data artifacts within the collection pipeline.

### **Expected Data Files**

| **File Pattern** | **Format** | **Purpose** |
|------------------|------------|-------------|
| **steam_processed_games_YYYYMMDD.json** | JSON | Validated game metadata with success flags |
| **steam_processed_reviews_YYYYMMDD.json** | JSON | Cleaned user review data with validation markers |
| **validation_report_YYYYMMDD.md** | Markdown | Data quality metrics and validation results |
| **processing_log_YYYYMMDD.txt** | Plain Text | Detailed processing logs with error tracking |

### **Data Validation Standards**

| **Check Type** | **Validation Rule** | **Action on Failure** |
|----------------|--------------------|-----------------------|
| **Schema Compliance** | All required fields present | Flag record with success=false |
| **Data Type Validation** | Numeric fields contain valid integers | Convert or flag as invalid |
| **JSONB Structure** | Nested objects parse correctly | Preserve raw data, mark for review |
| **Duplicate Detection** | Unique app_id per record | Keep most recent, log duplicates |
| **Content Completeness** | Critical fields not null/empty | Flag incomplete records |

---

## 🗂️ **Repository Structure**

Visual representation of the processed data organization:

```markdown
data/02_processed/
├── 📊 steam_processed_games_YYYYMMDD.json    # Validated game records
├── 💬 steam_processed_reviews_YYYYMMDD.json  # Cleaned review data
├── 📋 validation_report_YYYYMMDD.md          # Quality metrics
├── 📝 processing_log_YYYYMMDD.txt            # Detailed processing logs
└── 📄 README.md                               # This file
```

### **Navigation Guide:**

- **Game Data**: Processed records with ~56% success rate (valid API responses)
- **Review Data**: User reviews linked to valid app_ids only
- **Validation Reports**: Statistical summaries of data quality checks
- **Processing Logs**: Detailed error tracking and processing metrics

---

## 🔗 **Related Categories**

This section connects processed data to upstream sources and downstream applications.

| **Category** | **Relationship** | **Documentation** |
|--------------|------------------|-------------------|
| **[Raw Data](../01_raw/README.md)** | Source data from Steam API | [01_raw/README.md](../01_raw/README.md) |
| **[Enriched Data](../03_enriched/README.md)** | Vector embeddings and derived features | [03_enriched/README.md](../03_enriched/README.md) |
| **[Analytics Data](../04_analytics/README.md)** | Final analytical datasets | [04_analytics/README.md](../04_analytics/README.md) |
| **[Processing Scripts](../../scripts/04-postgresql-schema-analysis/)** | Validation and transformation code | [scripts/04-postgresql-schema-analysis/README.md](../../scripts/04-postgresql-schema-analysis/README.md) |

---

## 🚀 **Getting Started**

This section provides guidance for working with processed Steam data.

### **Data Quality Understanding**

The processed dataset maintains transparency about API collection challenges:

- **Success Rate**: ~56% of API requests return complete data
- **Failure Patterns**: Delisted games, regional restrictions, content type variations
- **Quality Indicators**: Every record includes `success` boolean flag
- **Filtering Strategy**: Most analyses filter to `success = TRUE` for complete records

### **Common Analysis Patterns**

```python
import json
import pandas as pd

# Load processed data
with open('steam_processed_games_20250831.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame with success filter
df = pd.DataFrame(data)
complete_games = df[df['success'] == True]

print(f"Total records: {len(df)}")
print(f"Complete records: {len(complete_games)} ({len(complete_games)/len(df)*100:.1f}%)")
```

### **Processing Pipeline Integration**

**Upstream Dependencies:**

- Raw JSON files from `/data/01_raw/`
- Validation schemas from `/scripts/04-postgresql-schema-analysis/`

**Downstream Applications:**

- PostgreSQL database import scripts
- Vector embedding generation
- Materialized column population
- CSV export generation

### **Quality Assurance**

Validation reports include:

- Total records processed
- Success/failure breakdown by reason
- Schema compliance statistics
- Data type validation results
- Duplicate detection summary
- Field completeness metrics

---

## 📚 **Technical Documentation**

This section provides detailed technical specifications for processed data structures.

### **Record Structure**

Processed records maintain the Steam API response structure with added metadata:

```json
{
  "steam_appid": 440,
  "success": true,
  "data": {
    "type": "game",
    "name": "Team Fortress 2",
    "detailed_description": "...",
    "about_the_game": "...",
    "short_description": "...",
    "header_image": "...",
    "website": "...",
    "pc_requirements": {...},
    "mac_requirements": {...},
    "linux_requirements": {...},
    "developers": ["Valve"],
    "publishers": ["Valve"],
    "price_overview": {...},
    "platforms": {...},
    "categories": [...],
    "genres": [...],
    "release_date": {...}
  },
  "_processing_metadata": {
    "validation_timestamp": "2025-08-31T12:00:00Z",
    "validation_passed": true,
    "warnings": []
  }
}
```

### **Validation Logic**

Processing scripts apply these validation rules:

1. **Required Fields Check**: `steam_appid`, `success`, `data` must be present
2. **Type Validation**: Numeric fields validated as integers, booleans as true/false
3. **JSONB Parsing**: Nested structures validated for parseable JSON
4. **Referential Integrity**: Review app_ids must exist in games dataset
5. **Temporal Validation**: Release dates within reasonable range (1990-2025)

### **Performance Characteristics**

| **Metric** | **Value** |
|------------|-----------|
| **Total Applications** | 239,664 |
| **Successful Retrievals** | ~134,000 (56%) |
| **Failed Retrievals** | ~105,000 (44%) |
| **Processing Time** | ~110 hours (full dataset) |
| **Average Record Size** | ~15KB (successful), ~500B (failed) |
| **Validation Time** | ~2 hours (full dataset) |

---

## 🎯 **Use Cases**

This section identifies common scenarios for working with processed data.

### **Database Import Preparation**

Processed data is optimized for PostgreSQL import:

- Schema-validated JSONB structures
- Success flags enable filtered imports
- Consistent field types across records
- Validation metadata for quality tracking

### **Exploratory Data Analysis**

Quality metrics inform analysis strategies:

- Filter to successful records for complete data
- Analyze failure patterns to understand coverage gaps
- Use validation reports to assess field completeness
- Identify data quality issues before modeling

### **Research Applications**

Processed data supports reproducible research:

- Transparent documentation of data quality
- Validation logs enable quality assessment
- Processing metadata tracks transformations
- Success indicators support sensitivity analysis

---

## 🔍 **Quality Metrics**

This section documents typical data quality characteristics for the processed tier.

### **Success Rate Analysis**

```markdown
Total API Requests:     239,664
Successful Responses:   134,212 (56.0%)
Failed Responses:       105,452 (44.0%)

Failure Breakdown:
  - Delisted/Removed:    45,231 (19.0%)
  - Regional Restricted: 28,134 (11.7%)
  - Invalid App IDs:     18,903 (7.9%)
  - API Errors:          13,184 (5.5%)
```

### **Field Completeness**

For successful records (success=true):

| **Field Category** | **Completeness** | **Notes** |
|-------------------|------------------|-----------|
| **Basic Metadata** | 99.8% | name, type, app_id nearly always present |
| **Descriptions** | 94.2% | detailed_description most complete |
| **Media Assets** | 87.5% | header_image highly available |
| **Pricing** | 78.1% | Free games lack price_overview |
| **Requirements** | 65.3% | PC requirements most common |
| **Release Date** | 98.6% | Highly reliable field |

### **Data Type Validation**

```markdown
Schema Validation Results:
✓ Type consistency:     99.9% (134,078/134,212)
✓ JSONB parsing:        99.7% (133,809/134,212)
✓ Numeric fields:       99.8% (133,944/134,212)
✓ Boolean fields:       100.0% (134,212/134,212)
⚠ Temporal fields:      98.6% (132,325/134,212)
```

---

## 🛠️ **Processing Pipeline**

This section describes how raw data transforms into the processed tier.

### **Transformation Steps**

1. **Load Raw Data**: Read gzipped JSON from `/data/01_raw/`
2. **Parse Records**: Extract individual application records
3. **Validate Schema**: Check required fields and data types
4. **Clean Data**: Handle nulls, convert types, normalize strings
5. **Add Metadata**: Append processing timestamps and validation flags
6. **Quality Check**: Generate validation reports and statistics
7. **Write Output**: Save processed JSON with compression

### **Error Handling**

Processing scripts implement robust error handling:

```python
# Example processing pattern
for app_id, raw_record in raw_data.items():
    try:
        # Validate and transform
        processed = validate_and_clean(raw_record)
        processed['_processing_metadata'] = {
            'validation_timestamp': datetime.utcnow().isoformat(),
            'validation_passed': True,
            'warnings': []
        }
        output_data.append(processed)
    except ValidationError as e:
        # Log failure but continue processing
        logger.warning(f"Validation failed for {app_id}: {e}")
        failed_records.append({
            'app_id': app_id,
            'error': str(e),
            'raw_data': raw_record
        })
```

### **Validation Scripts**

Processing occurs through these scripts:

| **Script** | **Purpose** | **Location** |
|------------|-------------|--------------|
| **validate_steam_data_integrity.py** | Schema validation and quality checks | `/scripts/04-postgresql-schema-analysis/` |
| **setup_postgresql_schema.py** | Database preparation and import | `/scripts/04-postgresql-schema-analysis/` |
| **import_json_to_pgsql.py** | Bulk data import to PostgreSQL | `/scripts/04-postgresql-schema-analysis/` |

---

## 📖 **References**

This section links to related documentation and resources that provide context for processed data usage.

### **Internal Documentation**

| **Document** | **Relevance** | **Link** |
|--------------|---------------|----------|
| **Data Dictionary** | Complete schema reference | [/steam-dataset-2025-v1/DATA_DICTIONARY.md](../../steam-dataset-2025-v1/DATA_DICTIONARY.md) |
| **PostgreSQL Schema** | Database implementation details | [/docs/postgresql-database-schema.md](../../docs/postgresql-database-schema.md) |
| **Collection Methodology** | Steam API data acquisition | [/docs/methodologies/steam-api-collection.md](../../docs/methodologies/steam-api-collection.md) |
| **Data Validation** | Quality assurance processes | [/docs/methodologies/data-validation-and-qa.md](../../docs/methodologies/data-validation-and-qa.md) |

### **Related Scripts**

| **Script Directory** | **Purpose** | **Documentation** |
|---------------------|-------------|-------------------|
| **04-postgresql-schema-analysis** | Validation and import | [README.md](../../scripts/04-postgresql-schema-analysis/README.md) |
| **06-full-dataset-import** | Production dataset processing | [README.md](../../scripts/06-full-dataset-import/README.md) |

### **External Resources**

| **Resource** | **Description** | **Link** |
|--------------|-----------------|----------|
| **Steam Web API** | Official API documentation | <https://steamcommunity.com/dev> |
| **PostgreSQL JSONB** | JSONB data type reference | <https://www.postgresql.org/docs/current/datatype-json.html> |
| **Data Quality Patterns** | Best practices for data validation | <https://www.oreilly.com/library/view/bad-data-handbook/9781449324957/> |

---

## 📜 **Documentation Metadata**

### **Change Log**

| **Version** | **Date** | **Changes** | **Author** |
|------------|----------|-------------|------------|
| 1.0 | 2025-01-06 | Initial documentation for processed data tier | VintageDon |

### **Authorship & Collaboration**

**Primary Author:** VintageDon (Donald Fountain)  
**GitHub:** <https://github.com/vintagedon>  
**AI Collaboration:** Claude 3.7 Sonnet (Anthropic) - Documentation structure and technical writing assistance  

**Human Responsibility:** All technical decisions, data validation strategies, and quality standards are human-defined. AI assistance was used for documentation organization and clarity enhancement.

---

**Document Information**

| **Field** | **Value** |
|-----------|-----------|
| **Author** | VintageDon - <https://github.com/vintagedon> |
| **Created** | 2025-01-06 |
| **Last Updated** | 2025-01-06 |
| **Version** | 1.0 |

---
Tags: processed-data, data-validation, data-quality, steam-api, data-pipeline, jsonb, postgresql
