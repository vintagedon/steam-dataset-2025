---
title: "Steam Dataset 2025: Academic Dataset Card"
description: "Comprehensive datasheet following Gebru et al. standards for academic transparency and reproducibility"
author: "VintageDon"
orcid: "0009-0008-7695-4093"
created: "2025-09-07"
last_updated: "2025-09-07"
version: "1.0"
tags: ["dataset-card", "datasheet", "academic-standards", "transparency"]
category: "academic"
status: "active"
---

# 📋 Steam Dataset 2025: Academic Dataset Card

This datasheet provides comprehensive documentation of the Steam Dataset 2025 following established academic standards (Gebru et al., 2021) to facilitate transparency, reproducibility, and informed decision-making by dataset consumers in the research community.

---

# 🎯 1. Motivation

## 1.1 Purpose and Task

For what purpose was the dataset created? Was there a specific task in mind? Was there a specific gap that needed to be filled?

The Steam Dataset 2025 was created to address significant gaps in publicly available gaming platform datasets by providing the first comprehensive, API-pure collection of the Steam digital distribution platform. The dataset was designed to enable modern analytical and machine learning research on gaming industry dynamics that was previously impossible due to data limitations.

Specific gaps addressed:

- Scale Limitation: Existing public datasets contained 6,000-120,000 applications vs. Steam's 260,000+ catalog
- Methodological Inconsistency: Hybrid collection methods mixing official APIs with statistical estimates compromised data integrity
- Technical Architecture: No existing Steam dataset provided vector search capabilities or modern ML infrastructure
- Content Coverage: Most datasets focused only on games, excluding DLC, software, and complete ecosystem analysis

Who created the dataset and on behalf of which entity?

The dataset was created by VintageDon (ORCID: 0009-0008-7695-4093) as an independent academic research initiative conducted at the Proxmox Astronomy Lab infrastructure facility. The work represents systematic application of the RAVGV (Request-Analyze-Verify-Generate-Validate) methodology for AI-assisted data engineering.

Who funded the creation of the dataset?

This dataset was created using independent infrastructure resources at the Proxmox Astronomy Lab without external funding. All computational resources, development time, and infrastructure costs were provided through independent research facilities.

Any other comments?

The dataset demonstrates that sophisticated, academically rigorous data collection can be achieved through systematic AI-human collaboration while maintaining full transparency and reproducibility standards.

---

# 📊 2. Composition

## 2.1 Instance Representation

What do the instances that comprise the dataset represent?

The dataset contains two primary types of instances:

1. Steam Applications (239,664 instances): Complete catalog of applications available through Steam's official Web API, including:
   - Games (150,279 instances): Interactive entertainment software
   - Downloadable Content/DLC (53,792 instances): Game expansions and add-ons
   - Software (≈15,000 instances): Development tools, utilities, creativity software
   - Videos (≈5,000 instances): Trailers, documentaries, and media content
   - Demos (≈8,000 instances): Trial versions and early access content

2. User Reviews (1,048,148 instances): Player-generated reviews collected through Steam's review API, representing authentic user feedback and sentiment data.

## 2.2 Dataset Scale and Sampling

How many instances are there in total?

- Total Applications: 239,664 (90.6% of accessible Steam catalog)
- Total Reviews: 1,048,148 reviews across collected applications
- Unique Developers: 101,226 distinct development entities
- Unique Publishers: 85,699 distinct publishing entities

Does the dataset contain all possible instances or is it a sample?

The dataset represents a systematic attempt to collect the complete accessible Steam catalog as of August-September 2025. It contains 90.6% of applications that returned successful responses from Steam's official Web API.

Missing instances (9.4%) fall into documented categories:

- Permanently delisted applications (≈18,500)
- Regionally restricted content (≈3,200)  
- Developer-removed applications (≈2,100)
- Licensing-expired content (≈900)
- Technical API failures (≈1,200)

The missing applications were systematically identified through reconciliation analysis and targeted re-collection efforts. Of 2,493 initially missing applications identified through review cross-reference, 563 (22.6%) were successfully recovered, confirming that 1,930 (77.4%) represent genuinely unavailable content.

## 2.3 Data Structure and Content

What data does each instance consist of?

Each application instance contains:

Structured Fields:

- `appid`: Unique Steam application identifier (integer)
- `name`: Official application title (text)
- `type`: Content classification (enum: game, dlc, software, video, demo, music)
- `is_free`: Free-to-play status (boolean)
- `release_date`: Publication date (date)
- `metacritic_score`: Professional review score 0-100 (integer, nullable)

Semi-Structured JSONB Fields:

- `price_overview`: Currency, pricing, and discount information
- `pc_requirements`: System requirements (minimum/recommended)
- `achievements`: Achievement definitions and metadata
- `screenshots`: Visual media assets and URLs
- `movies`: Video trailers and promotional content

Vector Fields (ML-Ready):

- `description_embedding`: 1024-dimensional semantic vector (when populated)

Normalized Relationships:

- Developer associations (many-to-many)
- Publisher relationships (many-to-many)
- Genre classifications (many-to-many)
- Category tags (many-to-many)

Is there a label or target associated with each instance?

Applications include multiple potential targets for supervised learning:

- `metacritic_score`: Professional review ratings (numeric regression target)
- `is_free`: Business model classification (binary classification target)
- `type`: Content type classification (multi-class target)
- User recommendation ratios can be derived from review data for sentiment analysis

## 2.4 Data Quality and Completeness

Is any information missing from individual instances?

Missing information occurs in documented patterns reflecting Steam platform characteristics:

| Field | Completeness | Missing Reason |
|-----------|------------------|-------------------|
| Basic metadata (name, type, appid) | 100% | Required for API success |
| Pricing information | ≈60% | Free applications have no pricing |
| Metacritic scores | ≈15% | Limited to reviewed applications |
| System requirements | ≈85% | Primarily games and software |
| Screenshots | ≈90% | Nearly universal for consumer applications |
| Achievements | ≈75% | Game-specific feature |

Are there any errors, sources of noise, or redundancies in the dataset?

Known Error Sources:

- Steam API occasionally returns inconsistent data structures (handled by defensive parsing)
- HTML formatting variations in description fields (preserved for authenticity)
- Currency conversion rates reflect collection-time values
- Some applications may have updated since collection period

Quality Assurance Measures:

- Systematic validation of all JSON structures before database insertion
- Foreign key constraint enforcement for referential integrity
- Duplicate detection and removal in lookup tables
- API response validation with retry logic for network errors

---

# 🔄 3. Collection Process

## 3.1 Data Acquisition Methods

How was the data associated with each instance acquired?

All data was acquired through official Valve Web APIs exclusively, ensuring consistent data provenance and verifiable accuracy:

1. Steam Web API - GetAppList: Retrieved complete catalog of application IDs
2. Steam Web API - AppDetails: Collected comprehensive metadata for each application
3. Steam Web API - GetReviews: Gathered user review data and sentiment information

No web scraping, third-party services, or statistical estimation methods were employed, ensuring "API-pure" data integrity.

What mechanisms or procedures were used to collect the data?

Technical Infrastructure:

- Programming Language: Python 3.9+ with robust HTTP session management
- Rate Limiting: Conservative 1.5-second delays between requests (17.3 requests/minute)
- Error Handling: Comprehensive retry logic with exponential backoff
- Data Validation: Real-time JSON structure validation and defensive parsing

Quality Assurance Procedures:

- Request/response logging for complete audit trail
- Systematic error categorization and analysis  
- Progress monitoring with checkpoint saves every 25 records
- Memory-efficient streaming processing for large datasets

## 3.2 Sampling and Coverage Strategy

If the dataset is a sample from a larger set, what was the sampling strategy?

The collection strategy aimed for complete census rather than sampling:

1. Complete Catalog Retrieval: Started with Steam's complete app list (263,890+ applications)
2. Systematic Processing: Processed applications in ascending appid order for reproducibility
3. Comprehensive Retry Logic: Failed requests were systematically retried and analyzed
4. Gap Analysis: Missing applications identified through review cross-reference analysis
5. Targeted Reconciliation: Attempted recovery of missing applications through focused re-collection

Who was involved in the data collection process?

The collection was conducted by a single researcher (VintageDon) using systematic AI-assisted methodology:

- Human Oversight: Strategic planning, validation, and quality assurance
- AI Assistance: Code generation, error analysis, and documentation support
- Methodology: Request-Analyze-Verify-Generate-Validate (RAVGV) framework

Over what timeframe was the data collected?

- Initial Collection: August 31 - September 7, 2025
- Reconciliation Phase: September 7, 2025 (targeted re-collection of missing applications)
- Total Duration: 7 days for primary collection + 1 day for reconciliation

The collection timeframe matches the creation timeframe of the data, representing a current snapshot of the Steam platform as of September 2025.

## 3.3 Ethical Considerations

Were any ethical review processes conducted?

The collection focused exclusively on publicly available data through official APIs, following established web API usage principles:

- Public Data Only: All collected information is publicly accessible through Steam's web interface
- API Terms Compliance: Conservative rate limiting respects Steam's API guidelines
- No Personal Data: Application metadata contains no private user information
- Review Content: User reviews are public posts visible on Steam platform

Privacy and Consent Considerations:

Application Data: Represents public catalog information published by developers/publishers for commercial distribution.

Review Data: Contains public user reviews posted voluntarily on Steam platform. Reviews include:

- Public usernames (already visible on Steam)
- Review text content (publicly posted)
- Recommendation status (public information)
- Play time statistics (public user choice)

No private user data, personal communications, or non-public information was collected.

---

# 🛠️ 4. Preprocessing/Cleaning/Labeling

## 4.1 Data Processing Pipeline

Was any preprocessing/cleaning/labeling of the data done?

Yes. Systematic preprocessing was applied to ensure data quality and consistency:

1. API Response Validation:

- JSON structure validation before processing
- Successful API response filtering (`success: true` only)
- Error response categorization and documentation

2. Data Type Normalization:

- Currency standardization for pricing data
- Date format conversion to ISO standards
- Numeric field validation and type casting
- HTML content preservation with structure validation

3. Relationship Normalization:

- Developer/publisher name extraction and deduplication
- Genre/category standardization and lookup table creation
- Many-to-many relationship mapping through junction tables

4. Data Quality Measures:

- Duplicate detection and removal
- Foreign key constraint validation
- NULL value handling with explicit documentation
- Text encoding standardization (UTF-8)

Was the "raw" data saved in addition to the preprocessed data?

Yes. Complete preservation of original API responses ensures transparency and enables alternative processing approaches:

- Raw JSON Files: Original API responses stored as compressed JSON archives
- Processing Logs: Complete audit trail of transformation decisions
- Error Documentation: Detailed logs of failed API calls and processing errors
- Version Control: All processing scripts maintained in version control for reproducibility

Is the software used to preprocess/clean/label the data available?

Yes. Complete processing pipeline is documented and available:

- GitHub Repository: <https://github.com/VintageDon/steam-dataset-2025>
- Processing Scripts: Complete ETL pipeline with documentation
- Schema Definitions: PostgreSQL schema with comprehensive documentation
- Validation Tools: Data integrity checking and quality assurance scripts

---

# 🎯 5. Uses

## 5.1 Current and Intended Applications

Has the dataset been used for any tasks already?

Academic Research Applications:

- Gaming industry market analysis and trend identification
- Publisher/developer relationship network analysis
- Content recommendation system development
- Sentiment analysis of user review data
- Multi-modal database architecture research

Technical Validation:

- Vector embedding generation for semantic search capabilities
- Multi-modal PostgreSQL architecture performance testing
- Academic reproducibility framework validation

Is there a repository that links to papers or systems using the dataset?

The primary repository (<https://github.com/VintageDon/steam-dataset-2025>) maintains links to research applications and publications utilizing the dataset. Academic citations and derivative works are tracked through GitHub issues and documentation updates.

## 5.2 Potential Research Applications

What other tasks could the dataset be used for?

Gaming Industry Research:

- Market segmentation and genre evolution analysis
- Pricing strategy optimization and market dynamics
- Success prediction modeling for indie vs. AAA games
- Regional market analysis through pricing and availability data
- Longitudinal trend analysis of gaming ecosystem development

Machine Learning Applications:

- Semantic search and content-based recommendation systems
- Natural language processing on game descriptions and reviews
- Multi-modal learning combining text, metadata, and user behavior
- Graph neural networks for publisher/developer relationship analysis
- Time series analysis of market trends and user engagement

Academic Research Domains:

- Digital economics and platform studies
- Human-computer interaction in gaming contexts
- Computational social science applications
- Information retrieval and recommendation system research
- Database architecture and performance optimization studies

## 5.3 Usage Considerations and Limitations

Is there anything about the composition or collection that might impact future uses?

Temporal Limitations:

- Data represents point-in-time snapshot (August-September 2025)
- Pricing information may become outdated quickly
- User review counts continue growing after collection
- Some applications may be delisted or updated post-collection

Geographic Bias:

- Collection performed from US-based infrastructure
- May under-represent region-locked or internationally restricted content
- Pricing reflects US market perspective primarily

Content Coverage:

- 9.4% of Steam catalog missing due to delisting/restrictions
- Review data limited to 10 recent reviews per application
- Some content types (adult, VR-specific) may be under-represented

Is there anything a dataset consumer could do to mitigate these risks?

Recommended Mitigation Strategies:

- Acknowledge temporal limitations in research scope and conclusions
- Consider geographic bias when making global market claims
- Use appropriate statistical methods to account for missing data
- Validate findings against complementary data sources when possible
- Document specific limitations in research methodology sections

Are there tasks for which the dataset should not be used?

Inappropriate Applications:

- Real-time pricing or availability decisions (data may be outdated)
- Individual user profiling or targeting (contains no private user data)
- Financial investment decisions without additional validation
- Legal or regulatory compliance assessments
- Applications requiring 100% complete Steam catalog coverage

---

# 📦 6. Distribution

## 6.1 Distribution Methods

Will the dataset be distributed to third parties?

Yes. The dataset is intended for open academic and research use through multiple distribution channels designed to maximize accessibility while ensuring proper attribution.

How will the dataset be distributed?

Current Distribution (GitHub):

- Repository: <https://github.com/VintageDon/steam-dataset-2025>
- Sample Dataset: 5K applications (102MB) available for immediate download
- Complete Documentation: Comprehensive methodology and usage guides
- Processing Scripts: Full ETL pipeline for reproducibility

Planned Distribution (Zenodo):

- Full Dataset: Complete 4.2GB dataset with persistent DOI
- Academic Archive: Long-term preservation for research reproducibility
- Version Control: Systematic versioning for academic citation
- Metadata Standards: Rich metadata following academic archival standards

When will the dataset be distributed?

- Sample Dataset: Currently available (GitHub)
- Full Dataset: Pending completion of documentation and embedding generation
- Academic Release: Planned for late 2025 through Zenodo

## 6.2 Licensing and Access Terms

Will the dataset be distributed under a copyright or intellectual property license?

Yes. MIT License provides broad permissions for academic and commercial use:

Permissions:

- ✅ Commercial use
- ✅ Modification and derivative works  
- ✅ Distribution and redistribution
- ✅ Private use
- ✅ Academic research and publication

Requirements:

- 📋 Include license and copyright notice
- 📋 Provide attribution to original creators

License Text: Available at <https://github.com/VintageDon/steam-dataset-2025/blob/main/LICENSE>

Have any third parties imposed restrictions on the data?

Steam Platform Considerations:

- Data collected through official public APIs in compliance with Steam's terms
- Application metadata represents publicly available commercial information
- User reviews represent publicly posted content
- No additional restrictions imposed by data sources

Do any export controls or regulatory restrictions apply?

No export controls or regulatory restrictions apply to this dataset. The data consists of:

- Publicly available commercial application metadata
- Public user review content  
- No personal data, encryption, or restricted technology information
- Standard academic research dataset classification

---

# 🔧 7. Maintenance

## 7.1 Dataset Stewardship

Who will be supporting/hosting/maintaining the dataset?

Primary Maintainer: VintageDon (ORCID: 0009-0008-7695-4093)

- GitHub Repository: Active maintenance for documentation and scripts
- Issue Resolution: Community support through GitHub issue tracking
- Documentation Updates: Ongoing improvement based on user feedback

Long-term Hosting:

- GitHub: Ongoing repository maintenance and community support
- Zenodo: Permanent archival storage with DOI for academic citations
- Infrastructure: Proxmox Astronomy Lab provides computational support for updates

How can the owner/curator/manager be contacted?

- GitHub Issues: <https://github.com/VintageDon/steam-dataset-2025/issues>
- GitHub Profile: <https://github.com/VintageDon>
- ORCID Profile: <https://orcid.org/0009-0008-7695-4093>

## 7.2 Update and Versioning Policy

Will the dataset be updated?

Versioning Strategy:

- Static Research Versions: Academic snapshot versions preserved for reproducibility
- Documentation Updates: Ongoing improvement of usage guides and examples
- Error Corrections: Critical data quality issues addressed through patch versions
- Methodology Improvements: Enhanced processing pipelines for future collections

Update Communication:

- GitHub Releases: Version announcements with detailed changelogs
- Documentation Updates: Real-time improvements to usage guides
- Community Notifications: GitHub issue discussions and README updates

Will older versions continue to be supported?

Yes. Academic reproducibility requirements mandate persistent version availability:

- GitHub Tags: All versions permanently available through git tags
- Zenodo Versioning: Academic archive maintains all released versions
- DOI Persistence: Each major version receives distinct DOI for citation
- Documentation Archival: Version-specific documentation preserved

## 7.3 Community Contributions

Is there a mechanism for others to extend/augment/build on/contribute to the dataset?

Yes. Community contribution is actively encouraged through established workflows:

Contribution Methods:

- GitHub Pull Requests: Documentation improvements and script enhancements
- Issue Reports: Data quality concerns and methodology discussions  
- Research Citations: Academic publications using the dataset
- Derivative Datasets: Enhanced versions with additional processing or analysis

Validation Process:

- Technical Review: Code contributions reviewed for quality and compatibility
- Data Validation: Proposed changes validated against original API sources
- Academic Standards: Contributions must maintain academic transparency standards
- Community Discussion: Major changes discussed through GitHub issue system

Distribution of Contributions:

- Accepted Contributions: Integrated into main repository with proper attribution
- Documentation Updates: Contributor recognition in acknowledgments
- Version Control: All changes tracked with detailed commit messages
- Release Notes: Contributor acknowledgments in version announcements

---

# 📜 8. Documentation Metadata

## 8.1 Change Log

| Version | Date | Changes | Author |
|------------|----------|-------------|------------|
| 1.0 | 2025-09-07 | Initial dataset card following Gebru et al. standards | VintageDon |

## 8.2 Authorship & Collaboration

Primary Author: VintageDon ([GitHub Profile](https://github.com/VintageDon))  
ORCID: 0009-0008-7695-4093 ([ORCID Profile](https://orcid.org/0009-0008-7695-4093))  
Dataset Standards: Following Gebru et al. (2021) "Datasheets for Datasets" framework  
AI Assistance: Claude Sonnet 4 for document structure and academic formatting  
Methodology: Request-Analyze-Verify-Generate-Validate (RAVGV) collaborative approach  
Quality Assurance: All information verified against actual collection procedures and academic standards

## 8.3 References

Primary Framework:
Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for datasets. Communications of the ACM, 64(12), 86-92.

Steam Dataset 2025 Materials:

- GitHub Repository: <https://github.com/VintageDon/steam-dataset-2025>
- Project Documentation: Available in repository docs/ directory
- Processing Scripts: Available in repository scripts/ directory

*Document Version: 1.0 | Last Updated: 2025-09-07 | Status: Active*
