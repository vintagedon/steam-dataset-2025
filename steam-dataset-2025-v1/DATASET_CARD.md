# Steam Dataset 2025 - Dataset Card

## Dataset Summary

The **Steam Dataset 2025** is a large-scale, multi-modal dataset capturing the complete Steam gaming platform catalog as of August-September 2025. It contains comprehensive metadata for 239,664 applications (games, DLC, software, and media) and 1,048,148 user reviews, with full preservation of nested data structures and pre-computed semantic embeddings for advanced analytics and machine learning research.

**Key Differentiators:**

- **Scale Supremacy**: 239,664 applications across 28 years (1997-2025) vs. competitors' 27K-85K
- **API Purity**: Exclusive use of official Steam Web API with zero third-party dependencies
- **Architectural Innovation**: First Steam dataset with native pgvector integration for semantic search
- **Multi-Modal Design**: PostgreSQL 16.10 + JSONB + 1024-dim BGE-M3 embeddings + HNSW indexing

## Supported Tasks

### Primary Use Cases

- **Recommendation Systems**: Collaborative filtering using 1M+ reviews and semantic embeddings
- **Sentiment Analysis**: Large-scale opinion mining on gaming content
- **Semantic Search**: Vector similarity queries on game descriptions (sub-second performance)
- **Market Analysis**: Pricing strategies across 30+ currencies and 28-year history
- **NLP Research**: Multilingual text analysis (100+ languages supported by BGE-M3)
- **Graph Analysis**: Publisher/developer relationship networks (101K developers, 86K publishers)

### Example Applications

```python
# Semantic game discovery
query_embedding = model.encode("relaxing farming simulation")
results = db.query("""
    SELECT appid, name, short_description
    FROM applications
    WHERE type = 'game'
    ORDER BY description_embedding <=> %s
    LIMIT 10
""", (query_embedding,))

# Review sentiment analysis by genre
sentiment_by_genre = db.query("""
    SELECT g.genre_description,
           AVG(CASE WHEN r.voted_up THEN 1.0 ELSE 0.0 END) as positive_ratio
    FROM reviews r
    JOIN applications a ON r.appid = a.appid
    JOIN application_genres ag ON a.appid = ag.appid
    JOIN genres g ON ag.genre_id = g.genre_id
    GROUP BY g.genre_description
""")
```

## Languages

**Primary Language**: English (majority of content)

**Additional Languages Supported**:

- Chinese (Simplified & Traditional) - significant representation in game titles/descriptions
- Japanese - substantial indie game presence
- European languages (German, French, Spanish, Italian, Portuguese, Russian, Polish, Dutch)
- Asian languages (Korean, Thai, Turkish)
- 100+ languages supported via BGE-M3 multilingual embeddings

**Language Distribution**: Not uniformly distributed; reflects Steam's global marketplace with English dominance and strong Asian game developer presence.

## Dataset Structure

### Data Instances

**Application Record Example**:

```json
{
  "appid": 2267870,
  "name": "Stewart The Fox",
  "type": "game",
  "is_free": false,
  "release_date": "2024-01-05",
  "short_description": "Join Stewart the Fox on an epic adventure...",
  "mat_supports_windows": true,
  "mat_supports_mac": false,
  "mat_supports_linux": false,
  "mat_final_price": 299,
  "mat_currency": "USD",
  "description_embedding": [0.023, -0.451, 0.892, ...],  // 1024 dimensions
  "price_overview": {
    "currency": "USD",
    "initial": 299,
    "final": 299,
    "discount_percent": 0
  }
}
```

**Review Record Example**:

```json
{
  "recommendationid": "123456789",
  "appid": 2267870,
  "author_steamid": "76561198...",
  "author_playtime_forever": 450,
  "review_text": "Great platformer with challenging gameplay...",
  "voted_up": true,
  "votes_up": 15,
  "weighted_vote_score": 0.7234,
  "review_embedding": [0.156, -0.023, 0.678, ...]  // 1024 dimensions
}
```

### Data Fields

#### Core Tables

**`applications` (239,664 rows)**

| Field | Type | Description |
|-------|------|-------------|
| `appid` | bigint | Primary key - Steam application ID |
| `name` | text | Application display name |
| `type` | enum | Application type (game/dlc/software/video/demo/music/etc.) |
| `is_free` | boolean | Free-to-play indicator |
| `release_date` | date | Official release date |
| `metacritic_score` | integer | Metacritic review score (0-100) |
| `detailed_description` | text | Full HTML description |
| `short_description` | text | Brief text summary |
| `price_overview` | jsonb | Pricing data (currency, initial/final price, discount) |
| `pc_requirements` | jsonb | System requirements (minimum/recommended) |
| `description_embedding` | vector(1024) | BGE-M3 semantic embedding |

**Materialized Columns** (Phase 2 & 9 Enrichment):

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `mat_supports_windows` | boolean | pc_requirements | Windows platform support |
| `mat_supports_mac` | boolean | mac_requirements | macOS platform support |
| `mat_supports_linux` | boolean | linux_requirements | Linux platform support |
| `mat_final_price` | integer | price_overview | Price in cents |
| `mat_currency` | text | price_overview | ISO 4217 currency code |
| `mat_achievement_count` | integer | achievements | Total achievements |
| `mat_pc_memory_rec` | text | pc_requirements | Parsed recommended RAM |
| `mat_pc_graphics_rec` | text | pc_requirements | Parsed recommended GPU |

**`reviews` (1,048,148 rows)**

| Field | Type | Description |
|-------|------|-------------|
| `recommendationid` | text | Primary key - Unique review ID |
| `appid` | bigint | Foreign key to applications |
| `author_steamid` | text | Review author Steam ID |
| `author_playtime_forever` | bigint | Total playtime (minutes) |
| `review_text` | text | Full review content |
| `voted_up` | boolean | Positive recommendation indicator |
| `votes_up` | bigint | Helpful vote count |
| `weighted_vote_score` | numeric | Steam helpfulness score (0.0-1.0) |
| `review_embedding` | vector(1024) | BGE-M3 semantic embedding |

#### Junction Tables (Many-to-Many Relationships)

- **`application_developers`**: Links apps to developers (101,226 unique developers)
- **`application_publishers`**: Links apps to publishers (85,699 unique publishers)
- **`application_genres`**: Links apps to genres (154 unique genres)
- **`application_categories`**: Links apps to Steam categories (462 unique categories)
- **`application_platforms`**: Links apps to OS platforms (Windows/Mac/Linux)

### Data Splits

This dataset does not include pre-defined train/validation/test splits. Researchers should create splits appropriate for their specific use case.

**Recommended Splitting Strategies**:

1. **Temporal Split**: Use `release_date` for time-based splits (e.g., train on pre-2023, test on 2024-2025)
2. **Stratified by Genre**: Maintain genre distribution across splits
3. **Popularity-Based**: Separate high-review games (>1000 reviews) for evaluation
4. **Random 80/10/10**: Standard random splits with fixed seed for reproducibility

**Example Code**:

```python
from sklearn.model_selection import train_test_split

# Temporal split
train = df[df['release_date'] < '2023-01-01']
test = df[df['release_date'] >= '2023-01-01']

# Stratified by genre (requires one-hot encoding for multi-label)
from sklearn.model_selection import StratifiedShuffleSplit
```

## Dataset Creation

### Curation Rationale

The Steam Dataset 2025 was created to address critical gaps in existing gaming datasets:

1. **Scale Limitation**: Previous datasets (2019-2024) captured 27K-85K applications, missing the platform's growth to 239K+ apps
2. **Methodological Purity**: Existing datasets rely on third-party APIs (SteamSpy) with accuracy concerns; this dataset uses only official Valve endpoints
3. **Architectural Innovation**: No prior Steam dataset integrates vector embeddings for semantic search natively
4. **Temporal Currency**: Most recent public datasets are 1-2 years old, missing 2024-2025 market evolution

**Target Research Community**:

- Academic researchers studying digital distribution platforms
- Data scientists developing recommendation systems
- NLP researchers requiring large-scale multilingual gaming text
- Market analysts studying pricing strategies and platform economics
- Game developers seeking competitive intelligence

### Source Data

#### Initial Data Collection and Normalization

**Data Source**: Steam Web API (official Valve endpoints)

- **App List API**: `https://api.steampowered.com/ISteamApps/GetAppList/v2/`
- **App Details API**: `https://store.steampowered.com/api/appdetails?appids={appid}`
- **Reviews API**: `https://store.steampowered.com/appreviews/{appid}?json=1`

**Collection Period**: August 31 - September 29, 2025

**Collection Infrastructure**:

- Platform: Proxmox Astronomy Lab enterprise virtualization
- Database: PostgreSQL 16.10 on proj-pgsql01 (Intel i9-13900H, 32GB RAM, Samsung PM983 NVMe)
- GPU: NVIDIA A4000 on proj-gpu01 for embedding generation
- Storage: 21GB total (data + HNSW indexes)

**Collection Methodology**:

1. **Master List Retrieval**: Fetch complete app list (263,890 total Steam IDs)
2. **Rate-Limited Detail Collection**: Conservative 1.5s delays (17.3 requests/minute sustainable)
3. **Success Rate**: 56% successful detail retrieval (remainder delisted/region-locked)
4. **Review Sampling**: 10 reviews per application for initial release
5. **Data Validation**: Multi-phase integrity checks (RAVGV methodology)

**API Response Preservation**:

- Complete JSONB storage of nested API responses
- No data transformation during collection (raw fidelity)
- Materialization performed post-import for query optimization

#### Who are the source language producers?

**Application Metadata**:

- Steam developers/publishers (101,226 developers, 85,699 publishers globally)
- Official game descriptions and marketing content
- Professionally translated store pages for international markets

**User Reviews**:

- Steam community members (global user base)
- Voluntary review submissions with playtime verification
- Mix of casual and professional gaming community members

**Language Demographics**:

- English: Dominant language for descriptions and reviews
- Chinese: Significant presence from Asian game developers
- European languages: Strong representation from EU-based developers
- Demographic details: Not explicitly collected (global Steam users)

### Annotations

#### Annotation process

**This dataset contains NO human annotations.** All data is sourced directly from:

1. **Steam Official APIs**: Application metadata, pricing, requirements
2. **User-Generated Content**: Steam community reviews (voluntary submissions)
3. **Automated Enrichment**: Vector embeddings via BGE-M3 model

**Enrichment Pipeline**:

- **BGE-M3 Embeddings**: Generated via `BAAI/bge-m3` model on NVIDIA A4000
- **Materialized Columns**: Automated extraction from JSONB via regex/SQL functions
- **PC Requirements Parsing**: Rule-based extraction from HTML text (~85-90% accuracy)

No human labeling, classification, or annotation was performed.

#### Who are the annotators?

Not applicable - dataset contains only API-sourced data and user-generated reviews.

### Personal and Sensitive Information

**Personal Information Present**:

- **Steam IDs**: User Steam IDs included in review author fields (e.g., `76561198...`)
- **Playtime Data**: Public playtime statistics for review authors
- **Public Reviews**: User-submitted review text (publicly visible on Steam)

**Privacy Considerations**:

- All data is already publicly accessible via Steam platform
- No private user data (emails, real names, purchase history) included
- Steam IDs are pseudonymous identifiers, not directly identifying
- Users consented to public review visibility when posting

**Recommendation**: Researchers should aggregate review analysis and avoid re-identification attempts. Steam IDs included for research reproducibility only.

## Considerations for Using the Data

### Social Impact of Dataset

**Positive Impacts**:

- **Game Discovery**: Enables better recommendation systems for indie game visibility
- **Academic Research**: Provides large-scale dataset for NLP, recommendation systems, market analysis
- **Market Transparency**: Public pricing/review data promotes informed consumer decisions
- **Developer Insights**: Helps indie developers understand market positioning

**Potential Negative Impacts**:

- **Review Manipulation Detection**: Could enable identification of suspicious review patterns, but also gaming of detection systems
- **Competitive Intelligence**: Enables competitive analysis of pricing/features (both positive and concerning)
- **Bias Amplification**: Review data may reflect platform demographics (primarily Western, male, 18-34)

**Ethical Use Recommendations**:

- Aggregate reviews to protect individual privacy
- Consider demographic bias in recommendation systems
- Use pricing data responsibly (no predatory analysis)
- Respect developer/publisher intellectual property

### Discussion of Biases

**Known Biases in Dataset**:

1. **Geographic Bias**:
   - Currency: 59.5% USD due to API query origin (North America)
   - Language: English-dominant descriptions despite global platform
   - Regional pricing variations not captured uniformly

2. **Demographic Bias (Reviews)**:
   - Steam user base skews male, 18-34, Western countries
   - Review language predominantly English
   - AAA titles over-represented in review volume

3. **Temporal Bias**:
   - Recent games (2020-2025) have more reviews than older titles
   - Early access games may have inflated positive review ratios
   - Delisted games missing (survivorship bias)

4. **Content Type Bias**:
   - Games heavily over-represented vs. software/videos
   - Free-to-play games have different review patterns than paid
   - DLC reviews conflated with base game sentiment

5. **Platform Bias**:
   - Windows-centric (PC requirements most complete)
   - Mac/Linux support under-documented
   - Console ports not distinguished from PC-native

**Mitigation Strategies**:

- Stratify analyses by application type, release year, price tier
- Weight reviews by playtime to reduce review bombing impact
- Cross-reference findings with external market data
- Explicitly report bias limitations in research publications

### Other Known Limitations

**Technical Limitations**:

1. **API Success Rate**: 56% success rate means ~44% of Steam IDs are incomplete (delisted, region-locked, or removed content)
2. **Review Sampling**: Only 10 reviews per app in initial collection (not comprehensive review corpus)
3. **PC Requirements Parsing**: ~85-90% accuracy due to inconsistent HTML formatting
4. **Embedding Coverage**: Review embeddings prioritized for top 10K most-reviewed games
5. **Snapshot Nature**: Data reflects Aug-Sep 2025 state; no historical price/review tracking

**Methodological Limitations**:

1. **No Ground Truth Labels**: No expert-labeled genres, quality scores, or categorizations
2. **Review Authenticity**: Cannot verify review authenticity (potential fake reviews included)
3. **Metadata Gaps**: Not all applications provide complete metadata (e.g., Metacritic scores only 4.1% coverage)
4. **Language Detection**: No explicit language tagging (inferred from content)

**Recommended Validation**:

- Cross-validate findings with SteamDB or SteamSpy where appropriate
- Use `success = TRUE` filter for complete records
- Treat PC requirements materialization as approximations
- Consider external review sources for ground truth validation

## Additional Information

### Dataset Curators

**Primary Curator**: Donald Fountain (VintageDon)

- GitHub: [@vintagedon](https://github.com/vintagedon)
- ORCID: [0009-0008-7695-4093](https://orcid.org/0009-0008-7695-4093)
- Affiliation: Independent Researcher

**Infrastructure**: Proxmox Astronomy Lab enterprise platform
**AI Collaboration**: Claude 3.5 Sonnet (Anthropic) for pipeline development
**Methodology**: RAVGV (Request-Analyze-Verify-Generate-Validate) human-AI collaboration

### Licensing Information

**Dataset License**: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

**You are free to**:

- **Share**: Copy and redistribute the material in any medium or format
- **Adapt**: Remix, transform, and build upon the material for any purpose, even commercially

**Under the following terms**:

- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made

**Code License**: MIT License (for scripts and notebooks in repository)

**Upstream Data**: Steam API data subject to [Steam Web API Terms of Use](https://steamcommunity.com/dev/apiterms)

### Citation Information

```bibtex
@dataset{fountain_2025_steam_dataset,
  author       = {Fountain, Donald},
  title        = {{The Steam Dataset 2025: A Large-Scale, Multi-Modal 
                   Dataset of the Steam Gaming Platform}},
  month        = oct,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.17286923},
  url          = {https://doi.org/10.5281/zenodo.17286923}
}
```

**Recommended Citation Format**:
> Fountain, D. (2025). *The Steam Dataset 2025: A Large-Scale, Multi-Modal Dataset of the Steam Gaming Platform* (Version 1.0.0) [Data set]. Zenodo. <https://doi.org/10.5281/zenodo.17286923>

### Contributions

We welcome contributions from the research community:

**Ways to Contribute**:

- **Bug Reports**: Identify data quality issues or errors
- **Enhancement Requests**: Suggest additional features or analyses
- **Pull Requests**: Improve documentation or add example notebooks
- **Research Applications**: Share your publications using the dataset

**Contribution Guidelines**: See [CONTRIBUTING.md](https://github.com/vintagedon/steam-dataset-2025/blob/main/CONTRIBUTING.md)

**Community**:

- GitHub Issues: [Report bugs or suggest features](https://github.com/vintagedon/steam-dataset-2025/issues)
- Discussions: [Ask questions or share findings](https://github.com/vintagedon/steam-dataset-2025/discussions)

### Acknowledgments

**Technology Stack**:

- PostgreSQL Development Team (PostgreSQL 16.10)
- pgvector Contributors (vector search capability)
- BAAI Research (BGE-M3 embedding model)
- Anthropic (Claude AI collaboration framework)

**Infrastructure**:

- Proxmox VE Team (enterprise virtualization platform)
- Intel & Samsung (hardware enablement)
- NVIDIA (A4000 GPU for embedding generation)

**Community**:

- Kaggle Community (feedback and validation)
- Steam Developer Community (indirect via public API)
- Open Source Data Science Community

**Inspiration**:

- Nik Davis (Original 2019 Kaggle Steam Dataset)
- Academic researchers studying digital distribution platforms
- Open science and reproducible research movements

---

**Dataset Version**: 1.0.0  
**Last Updated**: October 5, 2025  
**Documentation Status**: Published  
**Zenodo DOI**: [10.5281/zenodo.17286923](https://doi.org/10.5281/zenodo.17286923)  
**GitHub Repository**: [vintagedon/steam-dataset-2025](https://github.com/vintagedon/steam-dataset-2025)
