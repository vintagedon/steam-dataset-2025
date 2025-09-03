<!--
---
title: "Data Dictionary and Schema Documentation"
description: "Comprehensive documentation of the Steam Dataset 2025 database schema, including table structures, JSONB field definitions, relationships, and analytical views for multi-modal gaming analytics"
author: "VintageDon - https://github.com/vintagedon"
ai_contributor: "Claude Sonnet 4"
date: "2025-09-02"
version: "1.0"
status: "Published"
tags:
- type: [data-dictionary/schema-documentation/database-design]
- domain: [database-schema/postgresql/steam-api/gaming-analytics]
- tech: [postgresql-16/jsonb/pgvector/steam-web-api]
- audience: [data-scientists/analysts/developers/researchers]
related_documents:
- "[Infrastructure Documentation](infrastructure-pending.md)"
- "[Project Repository Overview](../README.md)"
- "[Database Schema SQL](../database/schema.sql)"
---
-->

# 📊 Data Dictionary and Schema Documentation

This document provides comprehensive documentation of the Steam Dataset 2025 database schema, covering table structures, JSONB field definitions, relationship mappings, and analytical views. The schema supports multi-modal analytics combining relational data processing, document analysis, and vector similarity search across 260,000+ Steam applications and millions of user reviews.

---

# 🎯 1. Introduction

This section establishes the context and structure for the Steam Dataset 2025 database schema, documenting the design decisions and architectural patterns that enable sophisticated gaming analytics applications.

## 1.1 Purpose

This data dictionary serves as the definitive reference for understanding and working with the Steam Dataset 2025 database schema. It provides complete field definitions, relationship documentation, and usage guidance for researchers, analysts, and developers working with Steam gaming data at scale.

## 1.2 Scope

What's Covered:

- Complete table schema definitions with field-level documentation
- JSONB structure analysis and common access patterns
- Relationship mappings and foreign key constraints
- Materialized views for analytical performance
- Vector embedding schema for semantic search applications

## 1.3 Target Audience

Primary Users: Data scientists, analysts, database developers working with Steam gaming data  
Secondary Users: Academic researchers, ML engineers, business intelligence developers  
Background Assumed: Basic SQL knowledge, familiarity with JSON data structures, understanding of relational database concepts

## 1.4 Overview

The schema employs a hybrid approach combining normalized relational tables for structured data with JSONB columns for semi-structured Steam API responses. Vector columns support semantic similarity search using pgvector, enabling advanced analytics impossible with traditional flat-file approaches.

---

# 📋 2. Core Database Tables

This section documents the primary tables containing Steam application and user review data, providing the foundation for all analytical operations.

## 2.1 Applications Table

The applications table contains comprehensive metadata for all Steam applications including games, DLC, software, and media content.

| Column | Type | Description | Source | Example |
|--------|------|-------------|---------|---------|
| appid | BIGINT PRIMARY KEY | Steam Application ID | Steam App List API | 730, 1245620, 271590 |
| name | TEXT NOT NULL | Application name | Steam App List API | "Counter-Strike 2", "Elden Ring" |
| type | TEXT | Content type classification | Steam AppDetails API | "game", "dlc", "music" |
| is_free | BOOLEAN | Free-to-play status | Steam AppDetails API | true, false |
| steam_appid | BIGINT | Duplicate AppID from details | Steam AppDetails API | Matches appid |
| short_description | TEXT | Brief application summary | Steam AppDetails API | Marketing tagline |
| about_the_game | TEXT | Detailed description (HTML) | Steam AppDetails API | Full game description |
| detailed_description | TEXT | Extended description (HTML) | Steam AppDetails API | Comprehensive details |
| website | TEXT | Official website URL | Steam AppDetails API | Developer website |
| legal_notice | TEXT | Copyright and legal information | Steam AppDetails API | Licensing details |
| header_image | TEXT | Main promotional image URL | Steam AppDetails API | Store header graphic |
| background | TEXT | Store background image URL | Steam AppDetails API | Full background image |
| background_raw | TEXT | Raw background image URL | Steam AppDetails API | Unprocessed background |
| capsule_image | TEXT | Small capsule image URL | Steam AppDetails API | List view thumbnail |
| capsule_imagev5 | TEXT | Version 5 capsule image | Steam AppDetails API | Updated thumbnail |
| release_date | DATE | Application release date | Steam AppDetails API | Extracted from JSON |
| coming_soon | BOOLEAN | Pre-release status | Steam AppDetails API | Release planning |
| required_age | INTEGER | Age rating requirement | Steam AppDetails API | Content rating |
| metacritic_score | INTEGER | Professional critic score | Steam AppDetails API | 0-100 rating |
| metacritic_url | TEXT | Metacritic review URL | Steam AppDetails API | External review link |
| support_email | TEXT | Developer support contact | Steam AppDetails API | Technical support |
| support_url | TEXT | Support website URL | Steam AppDetails API | Help documentation |
| windows_support | BOOLEAN | Windows platform support | Derived from JSONB | Platform compatibility |
| mac_support | BOOLEAN | Mac platform support | Derived from JSONB | Platform compatibility |
| linux_support | BOOLEAN | Linux platform support | Derived from JSONB | Platform compatibility |
| controller_support | TEXT | Controller support level | Steam AppDetails API | "full", "partial" |
| achievement_count | INTEGER | Total achievements available | Derived from JSONB | Game completion metrics |
| initial_price | INTEGER | Original price in cents | Derived from JSONB | Economic analysis |
| final_price | INTEGER | Current price in cents | Derived from JSONB | Pricing trends |
| discount_percent | INTEGER | Current discount percentage | Derived from JSONB | Sale analysis |
| currency | TEXT | Price currency code | Derived from JSONB | Regional pricing |
| app_details | JSONB | Complete API response | Steam AppDetails API | Full structured data |
| created_at | TIMESTAMP | Record creation time | System generated | Data pipeline tracking |
| updated_at | TIMESTAMP | Last modification time | System generated | Change tracking |
| description_embedding | vector(384) | Semantic text embedding | Generated via ML | Similarity search |

### Key Relationships

- One-to-many with `reviews` table via `appid`
- Many-to-many with `developers` via `application_developers` junction
- Many-to-many with `publishers` via `application_publishers` junction  
- Many-to-many with `genres` via `application_genres` junction
- Many-to-many with `categories` via `application_categories` junction

## 2.2 Reviews Table

The reviews table contains user-generated reviews with metadata for sentiment analysis and recommendation modeling.

| Column | Type | Description | Source | Example |
|--------|------|-------------|---------|---------|
| recommendationid | BIGINT PRIMARY KEY | Unique review identifier | Steam Reviews API | System generated ID |
| appid | BIGINT NOT NULL | Referenced application | Steam Reviews API | Foreign key to applications |
| steamid | TEXT | Reviewer Steam ID (anonymized) | Steam Reviews API | User identifier |
| voted_up | BOOLEAN | Recommendation status | Steam Reviews API | true (positive), false (negative) |
| votes_up | INTEGER | Helpful votes received | Steam Reviews API | Community feedback |
| votes_funny | INTEGER | Funny votes received | Steam Reviews API | Community engagement |
| weighted_vote_score | DECIMAL | Weighted helpfulness score | Steam Reviews API | Algorithm-derived rating |
| comment_count | INTEGER | Comments on review | Steam Reviews API | Discussion engagement |
| steam_purchase | BOOLEAN | Purchased through Steam | Steam Reviews API | Purchase verification |
| received_for_free | BOOLEAN | Received as gift/promotion | Steam Reviews API | Acquisition method |
| written_during_early_access | BOOLEAN | Written during early access | Steam Reviews API | Development phase |
| review_text | TEXT | Full review content | Steam Reviews API | User opinion text |
| timestamp_created | TIMESTAMP | Review creation time | Steam Reviews API | Publication date |
| timestamp_updated | TIMESTAMP | Last review update | Steam Reviews API | Edit tracking |
| author_steamid | TEXT | Author Steam ID | Steam Reviews API | Reviewer identification |
| author_num_games_owned | INTEGER | Reviewer's game library size | Steam Reviews API | User engagement level |
| author_num_reviews | INTEGER | Reviews written by author | Steam Reviews API | Reviewer activity |
| author_playtime_forever | INTEGER | Total playtime (minutes) | Steam Reviews API | Game engagement |
| author_playtime_last_two_weeks | INTEGER | Recent playtime (minutes) | Steam Reviews API | Current activity |
| author_playtime_at_review | INTEGER | Playtime when reviewed (minutes) | Steam Reviews API | Experience context |
| author_last_played | TIMESTAMP | Last play session | Steam Reviews API | Recency indicator |
| language | TEXT | Review language code | Steam Reviews API | Internationalization |
| created_at | TIMESTAMP | Record creation time | System generated | Data pipeline tracking |
| updated_at | TIMESTAMP | Last modification time | System generated | Change tracking |
| review_embedding | vector(384) | Semantic text embedding | Generated via ML | Similarity search |

---

# 🏗️ 3. Lookup and Relationship Tables

This section documents the normalized lookup tables that establish relationships between applications and their associated metadata, enabling efficient querying and analysis.

## 3.1 Developers Table

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| id | SERIAL PRIMARY KEY | Unique developer identifier | Auto-generated |
| name | TEXT NOT NULL UNIQUE | Developer/studio name | "Valve Corporation", "FromSoftware" |
| created_at | TIMESTAMP | Record creation time | System generated |

## 3.2 Publishers Table

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| id | SERIAL PRIMARY KEY | Unique publisher identifier | Auto-generated |
| name | TEXT NOT NULL UNIQUE | Publisher company name | "Steam", "Bandai Namco" |
| created_at | TIMESTAMP | Record creation time | System generated |

## 3.3 Genres Table

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| id | SERIAL PRIMARY KEY | Unique genre identifier | Auto-generated |
| name | TEXT NOT NULL UNIQUE | Genre classification | "Action", "RPG", "Strategy" |
| description | TEXT | Detailed genre description | Extended definition |
| created_at | TIMESTAMP | Record creation time | System generated |

## 3.4 Categories Table

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| id | SERIAL PRIMARY KEY | Unique category identifier | Auto-generated |
| steam_category_id | INTEGER | Steam's internal category ID | Official Steam identifier |
| name | TEXT NOT NULL | Category name | "Single-player", "Multi-player" |
| description | TEXT | Category description | Feature explanation |
| created_at | TIMESTAMP | Record creation time | System generated |

## 3.5 Junction Tables

Junction tables establish many-to-many relationships between applications and their associated metadata:

- application_developers: Links applications to developer studios
- application_publishers: Links applications to publishing companies  
- application_genres: Links applications to genre classifications
- application_categories: Links applications to feature categories

Each junction table contains:

- `appid` (BIGINT, references applications.appid)
- `{entity}_id` (INTEGER, references respective lookup table)
- `created_at` (TIMESTAMP, system generated)

---

# 📚 4. JSONB Structure Documentation

This section provides detailed documentation of the complex JSONB fields that store rich, semi-structured data from the Steam API, enabling advanced analytics impossible with flat relational structures.

## 4.1 Applications.app_details JSONB Structure

The `app_details` JSONB column contains the complete Steam AppDetails API response with nested objects and arrays supporting sophisticated queries.

### Core Application Metadata

```json
{
  "steam_appid": 730,
  "name": "Counter-Strike 2",
  "type": "game",
  "is_free": true,
  "detailed_description": "<p>Rich HTML content...</p>",
  "about_the_game": "<p>Game overview...</p>",
  "short_description": "Brief marketing text",
  "supported_languages": "English<strong>*</strong><br><strong>*</strong>languages with full audio support",
  "header_image": "https://shared.akamai.steamstatic.com/...",
  "website": "https://www.counter-strike.net/"
}
```

### Pricing Information

```json
{
  "price_overview": {
    "currency": "USD",
    "initial": 1999,
    "final": 1499,
    "discount_percent": 25,
    "initial_formatted": "$19.99",
    "final_formatted": "$14.99"
  },
  "package_groups": [
    {
      "name": "default",
      "title": "Buy Counter-Strike 2",
      "description": "",
      "selection_text": "Select a purchase option",
      "subs": [
        {
          "packageid": 29,
          "option_text": "Counter-Strike 2 - $14.99",
          "price_in_cents_with_discount": 1499
        }
      ]
    }
  ]
}
```

### Platform Support and Requirements

```json
{
  "platforms": {
    "windows": true,
    "mac": false,
    "linux": true
  },
  "pc_requirements": {
    "minimum": "<strong>Minimum:</strong><br><ul class=\"bb_ul\"><li><strong>OS:</strong> Windows 10<br></li><li><strong>Processor:</strong> Intel Core i5-2300 or AMD FX-4350<br></li><li><strong>Memory:</strong> 8 GB RAM<br></li></ul>",
    "recommended": "<strong>Recommended:</strong><br><ul class=\"bb_ul\"><li><strong>OS:</strong> Windows 10<br></li><li><strong>Processor:</strong> Intel Core i5-8400 or AMD Ryzen 5 2600<br></li><li><strong>Memory:</strong> 16 GB RAM<br></li></ul>"
  },
  "linux_requirements": {
    "minimum": "System Supporting Source Engine",
    "recommended": "Ubuntu 18.04 or later"
  }
}
```

### Content Classification

```json
{
  "genres": [
    {"id": "1", "description": "Action"},
    {"id": "37", "description": "Free To Play"}
  ],
  "categories": [
    {"id": 1, "description": "Multi-player"},
    {"id": 49, "description": "PvP"},
    {"id": 8, "description": "Valve Anti-Cheat enabled"}
  ],
  "content_descriptors": {
    "ids": [2, 5],
    "notes": "Includes online features that may expose players to unrated user-generated content"
  }
}
```

### Media Assets

```json
{
  "screenshots": [
    {
      "id": 0,
      "path_thumbnail": "https://shared.akamai.steamstatic.com/...600x338.jpg",
      "path_full": "https://shared.akamai.steamstatic.com/...1920x1080.jpg"
    }
  ],
  "movies": [
    {
      "id": 256658589,
      "name": "Counter-Strike 2 - Announcement Trailer",
      "thumbnail": "https://shared.akamai.steamstatic.com/...",
      "webm": {"480": "...", "max": "..."},
      "mp4": {"480": "...", "max": "..."},
      "highlight": true
    }
  ]
}
```

### Achievement System

```json
{
  "achievements": {
    "total": 167,
    "highlighted": [
      {
        "name": "World Traveler",
        "path": "https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/730/..."
      }
    ]
  }
}
```

### Release and Business Information

```json
{
  "release_date": {
    "coming_soon": false,
    "date": "Sep 27, 2023"
  },
  "developers": ["Valve"],
  "publishers": ["Valve"],
  "dlc": [730, 731, 732],
  "metacritic": {
    "score": 85,
    "url": "https://www.metacritic.com/game/pc/counter-strike-2"
  }
}
```

## 4.2 Common JSONB Query Patterns

### Platform Detection

```sql
-- Find games supporting specific platforms
SELECT appid, name 
FROM applications 
WHERE app_details -> 'platforms' ->> 'windows' = 'true'
  AND app_details -> 'platforms' ->> 'linux' = 'true';
```

### Price Range Filtering

```sql
-- Find games in specific price range
SELECT appid, name, 
       (app_details -> 'price_overview' ->> 'final')::integer / 100.0 AS price_usd
FROM applications 
WHERE app_details -> 'price_overview' IS NOT NULL
  AND (app_details -> 'price_overview' ->> 'final')::integer BETWEEN 1000 AND 3000;
```

### Genre Analysis

```sql
-- Extract and count genres
SELECT genre_data ->> 'description' AS genre, COUNT(*) AS game_count
FROM applications,
     jsonb_array_elements(app_details -> 'genres') AS genre_data
WHERE app_details -> 'genres' IS NOT NULL
GROUP BY genre_data ->> 'description'
ORDER BY game_count DESC;
```

### System Requirements Parsing

```sql
-- Extract RAM requirements from system specs
SELECT appid, name,
       CASE 
         WHEN app_details -> 'pc_requirements' ->> 'minimum' ~ '\d+ GB RAM'
         THEN regexp_replace(app_details -> 'pc_requirements' ->> 'minimum', 
                            '.*?(\d+) GB RAM.*', '\1')::integer
         ELSE NULL
       END AS min_ram_gb
FROM applications
WHERE app_details -> 'pc_requirements' ->> 'minimum' IS NOT NULL;
```

---

# 📈 5. Analytical Views and Indexes

This section documents the materialized views and specialized indexes that provide optimized access patterns for common analytical queries and machine learning applications.

## 5.1 Materialized Views

### Developer Analytics View

```sql
CREATE MATERIALIZED VIEW developer_analytics AS
SELECT 
    d.id,
    d.name,
    COUNT(ad.appid) AS total_applications,
    COUNT(CASE WHEN a.type = 'game' THEN 1 END) AS total_games,
    AVG(a.metacritic_score) FILTER (WHERE a.metacritic_score IS NOT NULL) AS avg_metacritic_score,
    COUNT(a.metacritic_score) AS metacritic_review_count,
    AVG(a.final_price::float / 100) FILTER (WHERE a.final_price > 0) AS avg_price_usd,
    MIN(a.release_date) AS first_release_date,
    MAX(a.release_date) AS latest_release_date
FROM developers d
LEFT JOIN application_developers ad ON d.id = ad.developer_id
LEFT JOIN applications a ON ad.appid = a.appid
GROUP BY d.id, d.name;

CREATE UNIQUE INDEX ON developer_analytics (id);
```

### Publisher Analytics View

```sql
CREATE MATERIALIZED VIEW publisher_analytics AS
SELECT 
    p.id,
    p.name,
    COUNT(ap.appid) AS total_applications,
    COUNT(CASE WHEN a.type = 'game' THEN 1 END) AS total_games,
    AVG(a.metacritic_score) FILTER (WHERE a.metacritic_score IS NOT NULL) AS avg_metacritic_score,
    COUNT(a.metacritic_score) AS metacritic_review_count,
    AVG(a.final_price::float / 100) FILTER (WHERE a.final_price > 0) AS avg_price_usd
FROM publishers p
LEFT JOIN application_publishers ap ON p.id = ap.publisher_id
LEFT JOIN applications a ON ap.appid = a.appid
GROUP BY p.id, p.name;

CREATE UNIQUE INDEX ON publisher_analytics (id);
```

### Genre Analytics View

```sql
CREATE MATERIALIZED VIEW genre_analytics AS
SELECT 
    g.id,
    g.name,
    COUNT(ag.appid) AS total_applications,
    COUNT(CASE WHEN a.type = 'game' THEN 1 END) AS total_games,
    AVG(a.metacritic_score) FILTER (WHERE a.metacritic_score IS NOT NULL) AS avg_metacritic_score,
    AVG(a.final_price::float / 100) FILTER (WHERE a.final_price > 0) AS avg_price_usd,
    COUNT(CASE WHEN a.is_free = true THEN 1 END) AS free_games_count
FROM genres g
LEFT JOIN application_genres ag ON g.id = ag.genre_id
LEFT JOIN applications a ON ag.appid = a.appid
GROUP BY g.id, g.name;

CREATE UNIQUE INDEX ON genre_analytics (id);
```

## 5.2 Specialized Indexes

### Performance Indexes

```sql
-- Core application lookups
CREATE INDEX idx_applications_type ON applications (type);
CREATE INDEX idx_applications_release_date ON applications (release_date);
CREATE INDEX idx_applications_metacritic ON applications (metacritic_score) WHERE metacritic_score IS NOT NULL;
CREATE INDEX idx_applications_price ON applications (final_price) WHERE final_price IS NOT NULL;

-- Review analysis indexes
CREATE INDEX idx_reviews_appid_voted_up ON reviews (appid, voted_up);
CREATE INDEX idx_reviews_timestamp ON reviews (timestamp_created);
CREATE INDEX idx_reviews_language ON reviews (language);
CREATE INDEX idx_reviews_steam_purchase ON reviews (steam_purchase);

-- JSONB performance indexes
CREATE INDEX idx_applications_jsonb_platforms ON applications USING gin ((app_details -> 'platforms'));
CREATE INDEX idx_applications_jsonb_genres ON applications USING gin ((app_details -> 'genres'));
CREATE INDEX idx_applications_jsonb_categories ON applications USING gin ((app_details -> 'categories'));
```

### Vector Search Indexes

```sql
-- HNSW indexes for semantic similarity search
CREATE INDEX idx_applications_description_embedding 
ON applications USING hnsw (description_embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX idx_reviews_embedding 
ON reviews USING hnsw (review_embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

### Full-Text Search Indexes

```sql
-- Text search capabilities
CREATE INDEX idx_applications_fts 
ON applications USING gin (to_tsvector('english', name || ' ' || COALESCE(short_description, '')));

CREATE INDEX idx_reviews_fts 
ON reviews USING gin (to_tsvector('english', review_text));
```

---

# 🔧 6. Usage Examples and Common Patterns

This section provides practical examples demonstrating effective use of the schema for common analytical tasks and advanced queries.

## 6.1 Basic Analytics Queries

### Top Games by Genre

```sql
WITH genre_games AS (
    SELECT 
        a.appid,
        a.name,
        a.metacritic_score,
        g.name AS genre_name
    FROM applications a
    JOIN application_genres ag ON a.appid = ag.appid
    JOIN genres g ON ag.genre_id = g.id
    WHERE a.type = 'game' 
      AND a.metacritic_score IS NOT NULL
),
ranked_games AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY genre_name ORDER BY metacritic_score DESC) as rank
    FROM genre_games
)
SELECT genre_name, name, metacritic_score
FROM ranked_games 
WHERE rank <= 5
ORDER BY genre_name, metacritic_score DESC;
```

### Price Analysis by Platform Support

```sql
SELECT 
    CASE 
        WHEN windows_support AND mac_support AND linux_support THEN 'Cross-Platform'
        WHEN windows_support AND (mac_support OR linux_support) THEN 'Windows + Other'
        WHEN windows_support THEN 'Windows Only'
        ELSE 'Other Platform'
    END AS platform_category,
    COUNT(*) AS game_count,
    AVG(final_price::float / 100) AS avg_price_usd,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY final_price::float / 100) AS median_price_usd
FROM applications 
WHERE type = 'game' 
  AND final_price IS NOT NULL 
  AND final_price > 0
GROUP BY platform_category
ORDER BY avg_price_usd DESC;
```

## 6.2 Advanced JSONB Analysis

### System Requirements Trend Analysis

```sql
SELECT 
    EXTRACT(YEAR FROM release_date) AS release_year,
    COUNT(*) AS games_released,
    COUNT(CASE WHEN app_details -> 'pc_requirements' ->> 'minimum' ~ '\d+ GB RAM' 
               THEN 1 END) AS games_with_ram_spec,
    AVG(CASE 
        WHEN app_details -> 'pc_requirements' ->> 'minimum' ~ '(\d+) GB RAM'
        THEN regexp_replace(app_details -> 'pc_requirements' ->> 'minimum', 
                           '.*?(\d+) GB RAM.*', '\1')::integer
        ELSE NULL
    END) AS avg_min_ram_gb
FROM applications
WHERE type = 'game' 
  AND release_date >= '2015-01-01'
  AND app_details -> 'pc_requirements' IS NOT NULL
GROUP BY EXTRACT(YEAR FROM release_date)
ORDER BY release_year;
```

## 6.3 Vector Similarity Search

### Semantic Game Discovery

```sql
-- Find games similar to a specific title using vector embeddings
WITH target_game AS (
    SELECT description_embedding 
    FROM applications 
    WHERE appid = 730  -- Counter-Strike 2
),
similar_games AS (
    SELECT 
        a.appid,
        a.name,
        a.short_description,
        a.description_embedding <=> tg.description_embedding AS similarity_distance
    FROM applications a, target_game tg
    WHERE a.appid != 730
      AND a.description_embedding IS NOT NULL
    ORDER BY similarity_distance
    LIMIT 10
)
SELECT appid, name, short_description, similarity_distance
FROM similar_games;
```

---

# 📚 7. References & Related Resources

This section provides comprehensive references to related documentation and external resources supporting schema understanding and usage.

## 7.1 Internal References

| Document Type | Title | Relationship | Link |
|-------------------|-----------|------------------|----------|
| [Infrastructure Documentation] | System Performance and Configuration | Hardware supporting this schema | [infrastructure-pending.md] |
| [Schema Definition] | Complete SQL Schema | Full schema creation scripts | [../database/schema.sql] |
| [API Documentation] | Steam API Integration | Source data specifications | [../src/data/steam_api_documentation.md] |

---

# 📜 8. Documentation Metadata

## 8.1 Change Log

| Version | Date | Changes | Author |
|------------|----------|-------------|------------|
| 1.0 | 2025-09-02 | Initial data dictionary with complete schema documentation | VintageDon |

*Document Version: 1.0 | Last Updated: 2025-09-02 | Status: Published*
