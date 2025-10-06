<!--
---
title: "Steam Dataset 2025 - Data Dictionary"
description: "Comprehensive reference documentation for all database tables, columns, data types, and relationships in the Steam Dataset 2025 multi-modal architecture"
author: "VintageDon - https://github.com/vintagedon"
ai_contributor: "Claude 3.5 Sonnet (claude-sonnet-4-20250514)"
date: "2025-10-05"
version: "1.0"
status: "Published"
tags:
- type: [data-dictionary/reference-documentation]
- domain: [data-engineering/database-schema/steam-api]
- tech: [postgresql/pgvector/jsonb/sql]
- audience: [data-scientists/analysts/researchers/developers]
related_documents:
- "[PostgreSQL Database Schema](postgresql-database-schema.md)"
- "[Data Access Guide](data-access.md)"
- "[Infrastructure Overview](infrastructure.md)"
---
-->

# 📚 **Steam Dataset 2025 - Data Dictionary**

This document provides authoritative reference documentation for the complete Steam Dataset 2025 database schema. It defines every table, column, data type, relationship, and nested structure within the multi-modal PostgreSQL architecture, serving as the essential reference for data scientists, analysts, and researchers working with the dataset.

---

# 🎯 **1. Introduction**

This section establishes the foundational context for the data dictionary, defining its purpose, coverage scope, intended users, and relationship to other dataset documentation.

## **1.1 Purpose**

This data dictionary serves as the definitive technical reference for the Steam Dataset 2025 database schema. It provides complete specifications for all 239,664 applications and 1,048,148 user reviews, including normalized relational tables, JSONB nested structures, vector embeddings, and materialized analytical columns. Every data element is documented with its data type, constraints, relationships, and semantic meaning to enable accurate analysis and reproducible research.

## **1.2 Scope**

**What's Covered:**

- Complete PostgreSQL 16.10 schema with all tables, columns, and constraints
- JSONB nested structure specifications with field-level documentation
- Vector embedding columns (1024-dimensional BGE-M3 embeddings)
- Materialized analytical columns for platform support, pricing, and requirements
- All junction tables and many-to-many relationships
- Custom data types (ENUM) and PostgreSQL extensions (pgvector)
- Indexes, views, and materialized views
- Data constraints, validation rules, and referential integrity

## **1.3 Target Audience**

**Primary Users:** Data scientists, ML engineers, analytics professionals working with Steam gaming data  
**Secondary Users:** Academic researchers, students, developers building Steam-related applications  
**Background Assumed:** Basic familiarity with relational databases; PostgreSQL-specific features explained in context

## **1.4 Overview**

The Steam Dataset 2025 employs a hybrid schema architecture combining normalized relational tables for structured metadata with JSONB columns for complex nested data preservation. Vector embeddings enable semantic search capabilities, while materialized columns provide query-optimized access to frequently analyzed attributes. This data dictionary documents the complete schema as implemented in the production PostgreSQL 16.10 database, following the structure defined in `/scripts/04-postgres_schema_design/schema.sql` and extended through materialization phases.

---

# 📗 **2. Dependencies & Relationships**

This section maps the data dictionary's integration with other dataset components and external resources, helping users understand prerequisites and complementary documentation.

## **2.1 Related Components**

| **Component** | **Relationship** | **Integration Points** | **Documentation** |
|---------------|------------------|------------------------|-------------------|
| PostgreSQL Database Schema | Implements the structure documented here | All table definitions, indexes, constraints | [postgresql-database-schema.md](postgresql-database-schema.md) |
| Steam API Collection | Source of all raw data in JSONB columns | `app_details` field structure, API response mapping | [steam-api-collection.md](docs/methodologies/steam-api-collection.md) |
| Vector Embeddings | Provides semantic search capability | `description_embedding` and `review_embedding` columns | [vector-embeddings.md](docs/methodologies/vector-embeddings.md) |
| Data Validation Framework | Ensures data integrity rules documented here | Constraint validation, referential integrity checks | [data-validation-and-qa.md](docs/methodologies/data-validaton-and-qa.md) |

## **2.2 External Dependencies**

- **[PostgreSQL 16.10](https://www.postgresql.org/docs/16/)** - Core database engine with JSONB and array support
- **[pgvector v0.8.0](https://github.com/pgvector/pgvector)** - Extension enabling vector operations and HNSW indexing
- **[Steam Web API](https://steamcommunity.com/dev)** - Official Valve API providing all source data
- **[BGE-M3 Embeddings](https://huggingface.co/BAAI/bge-m3)** - 1024-dimensional multilingual embedding model

---

# ⚙️ **3. Database Schema Documentation**

This section provides comprehensive technical specifications for all database objects, including tables, columns, data types, and structural relationships.

## **3.1 PostgreSQL Extensions & Custom Types**

### Extensions

The database relies on the following PostgreSQL extensions:

| Extension | Version | Purpose |
|-----------|---------|---------|
| `pgvector` | 0.8.0 | Enables vector data type and similarity search operations |

### Custom Data Types (ENUM)

**`app_type`** - Defines Steam application categories

```sql
CREATE TYPE app_type AS ENUM (
    'game', 'dlc', 'software', 'video', 
    'demo', 'music', 'advertising', 'mod', 
    'episode', 'series'
);
```

**Valid Values:** `game`, `dlc`, `software`, `video`, `demo`, `music`, `advertising`, `mod`, `episode`, `series`

**`platform_type`** - Defines supported operating system platforms

```sql
CREATE TYPE platform_type AS ENUM (
    'windows', 'mac', 'linux'
);
```

**Valid Values:** `windows`, `mac`, `linux`

## **3.2 Core Tables**

### **Table: `applications`**

The central table containing comprehensive metadata for all Steam applications.

**Row Count:** 239,664 applications  
**Primary Key:** `appid`  
**Indexes:** Primary key index, HNSW vector index on `description_embedding`, GIN indexes on JSONB columns

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `appid` | `bigint` | PRIMARY KEY, NOT NULL | Unique Steam application identifier |
| `steam_appid` | `bigint` | | Steam store application ID (may differ from appid) |
| `name_from_applist` | `text` | | Application name from Steam master app list |
| `name` | `text` | | Display name from application details API |
| `type` | `app_type` | | Application type (game, dlc, software, etc.) |
| `is_free` | `boolean` | DEFAULT false | Whether application is free-to-play |
| `release_date` | `date` | | Official release date |
| `metacritic_score` | `integer` | CHECK (0-100) | Metacritic review score |
| `detailed_description` | `text` | | Full HTML-formatted description |
| `short_description` | `text` | | Brief plain-text summary |
| `about_the_game` | `text` | | "About" section content |
| `combined_text` | `text` | GENERATED | Concatenation of name + short_description + about_the_game for embeddings |
| `price_overview` | `jsonb` | | Pricing details (see JSONB schema below) |
| `pc_requirements` | `jsonb` | | PC system requirements (see JSONB schema below) |
| `mac_requirements` | `jsonb` | | macOS system requirements |
| `linux_requirements` | `jsonb` | | Linux system requirements |
| `success` | `boolean` | DEFAULT false | API fetch success flag |
| `fetched_at` | `timestamp` | | API fetch timestamp |
| `created_at` | `timestamp` | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| `updated_at` | `timestamp` | DEFAULT CURRENT_TIMESTAMP | Last update timestamp |
| `description_embedding` | `vector(1024)` | | BGE-M3 embedding of combined_text |

**Materialized Columns (Phase 2):**

| Column Name | Data Type | Source | Description |
|-------------|-----------|--------|-------------|
| `mat_supports_windows` | `boolean` | `pc_requirements` | TRUE if PC requirements exist |
| `mat_supports_mac` | `boolean` | `mac_requirements` | TRUE if Mac requirements exist |
| `mat_supports_linux` | `boolean` | `linux_requirements` | TRUE if Linux requirements exist |
| `mat_initial_price` | `integer` | `price_overview->>'initial'` | Initial price in cents |
| `mat_final_price` | `integer` | `price_overview->>'final'` | Final price in cents (after discount) |
| `mat_discount_percent` | `integer` | `price_overview->>'discount_percent'` | Discount percentage (0-100) |
| `mat_currency` | `text` | `price_overview->>'currency'` | ISO 4217 currency code (e.g., USD) |
| `mat_achievement_count` | `integer` | `achievements->>'total'` | Total number of achievements |

**Materialized PC Requirements (Phase 9):**

| Column Name | Data Type | Source | Description |
|-------------|-----------|--------|-------------|
| `mat_pc_os_min` | `text` | `pc_requirements` | Minimum OS requirement |
| `mat_pc_processor_min` | `text` | `pc_requirements` | Minimum processor requirement |
| `mat_pc_memory_min` | `text` | `pc_requirements` | Minimum RAM requirement |
| `mat_pc_graphics_min` | `text` | `pc_requirements` | Minimum graphics card requirement |
| `mat_pc_os_rec` | `text` | `pc_requirements` | Recommended OS requirement |
| `mat_pc_processor_rec` | `text` | `pc_requirements` | Recommended processor requirement |
| `mat_pc_memory_rec` | `text` | `pc_requirements` | Recommended RAM requirement |
| `mat_pc_graphics_rec` | `text` | `pc_requirements` | Recommended graphics card requirement |

#### JSONB Structure: `price_overview`

```json
{
  "currency": "USD",
  "initial": 1999,
  "final": 1499,
  "discount_percent": 25,
  "initial_formatted": "$19.99",
  "final_formatted": "$14.99"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `currency` | string | ISO 4217 currency code |
| `initial` | integer | Original price in cents |
| `final` | integer | Current price in cents (after discount) |
| `discount_percent` | integer | Discount percentage (0-100) |
| `initial_formatted` | string | Human-readable original price |
| `final_formatted` | string | Human-readable current price |

**Note:** 59.5% of applications use USD due to API query origin. Currency reflects the region from which the API was queried.

#### JSONB Structure: `pc_requirements`

```json
{
  "minimum": "<strong>Minimum:</strong><br><ul class=\"bb_ul\"><li><strong>OS:</strong> Windows 10<br></li><li><strong>Processor:</strong> Intel i5<br></li><li><strong>Memory:</strong> 8 GB RAM<br></li><li><strong>Graphics:</strong> GTX 1060</li></ul>",
  "recommended": "<strong>Recommended:</strong><br><ul class=\"bb_ul\"><li><strong>OS:</strong> Windows 11<br></li><li><strong>Processor:</strong> Intel i7<br></li><li><strong>Memory:</strong> 16 GB RAM<br></li><li><strong>Graphics:</strong> RTX 3060</li></ul>"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `minimum` | string | HTML-formatted minimum system requirements |
| `recommended` | string | HTML-formatted recommended system requirements |

**Structure Notes:**

- Content is HTML-formatted with embedded `<strong>`, `<br>`, and `<ul>` tags
- Parsing extracts OS, Processor, Memory, and Graphics specifications
- Phase 9 materialization populates `mat_pc_*_min` and `mat_pc_*_rec` columns
- Not all applications include both minimum and recommended requirements

#### JSONB Structure: `mac_requirements` & `linux_requirements`

Same structure as `pc_requirements` - contains `minimum` and `recommended` HTML-formatted text fields.

**Presence in Dataset:**

- `mac_requirements`: 44.7% of applications
- `linux_requirements`: 37.1% of applications
- Both fields may be empty objects `{}` if platform not supported

#### JSONB Structure: `achievements`

```json
{
  "total": 50,
  "highlighted": [
    {
      "name": "First Victory",
      "path": "https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/570/achievement_icon.jpg"
    },
    {
      "name": "Master Explorer",
      "path": "https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/570/achievement_icon2.jpg"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `total` | integer | Total number of achievements available |
| `highlighted` | array | Array of featured achievements (typically 3-5) |
| `highlighted[].name` | string | Achievement display name |
| `highlighted[].path` | string | CDN URL to achievement icon image |

**Presence:** 21.2% of applications (primarily games)

#### JSONB Structure: `content_descriptors`

```json
{
  "ids": [2, 5],
  "notes": "This Game may contain content not appropriate for all ages, or may not be appropriate for viewing at work: Nudity or Sexual Content, General Mature Content"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `ids` | array | Array of Steam content descriptor IDs |
| `notes` | string | Free-text explanation of mature content warnings |

**Common Content Warnings:**

- Violence, Blood and Gore
- Sexual Content, Nudity
- Strong Language
- Drug/Alcohol Use
- General Mature Content

**Presence:** `ids` array in 21.8% of applications, `notes` in 16.5%

#### JSONB Structure: `movies` (Trailers/Videos)

```json
{
  "movies": [
    {
      "id": 256988261,
      "name": "Launch Trailer",
      "thumbnail": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/256988261/movie.293x165.jpg",
      "webm": {
        "480": "http://video.akamai.steamstatic.com/store_trailers/256988261/movie480_vp9.webm",
        "max": "http://video.akamai.steamstatic.com/store_trailers/256988261/movie_max_vp9.webm"
      },
      "mp4": {
        "480": "http://video.akamai.steamstatic.com/store_trailers/256988261/movie480.mp4",
        "max": "http://video.akamai.steamstatic.com/store_trailers/256988261/movie_max.mp4"
      },
      "highlight": true
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique movie/trailer ID |
| `name` | string | Video title/description |
| `thumbnail` | string | CDN URL to video thumbnail image (293x165) |
| `webm.480` | string | 480p WebM video URL |
| `webm.max` | string | Maximum quality WebM video URL |
| `mp4.480` | string | 480p MP4 video URL |
| `mp4.max` | string | Maximum quality MP4 video URL |
| `highlight` | boolean | Whether this is a featured/main trailer |

**Presence:** 49.2% of applications include video trailers

#### JSONB Structure: `screenshots`

```json
{
  "screenshots": [
    {
      "id": 0,
      "path_thumbnail": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/570/ss_01.600x338.jpg",
      "path_full": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/570/ss_01.1920x1080.jpg"
    },
    {
      "id": 1,
      "path_thumbnail": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/570/ss_02.600x338.jpg",
      "path_full": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/570/ss_02.1920x1080.jpg"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Screenshot sequence number (0-indexed) |
| `path_thumbnail` | string | CDN URL to thumbnail image (600x338) |
| `path_full` | string | CDN URL to full-resolution screenshot (1920x1080) |

**Presence:** 85.0% of applications include screenshots

#### JSONB Structure: `categories`

```json
{
  "categories": [
    {"id": 2, "description": "Single-player"},
    {"id": 1, "description": "Multi-player"},
    {"id": 22, "description": "Steam Achievements"},
    {"id": 28, "description": "Full controller support"}
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Steam category ID |
| `description` | string | Category name/feature description |

**Common Category IDs:**

- 1: Multi-player
- 2: Single-player  
- 9: Co-op
- 22: Steam Achievements
- 23: Steam Cloud
- 28: Full controller support
- 29: Steam Trading Cards

**Presence:** 81.9% of applications
**Note:** These are also normalized into the `application_categories` junction table

#### JSONB Structure: `genres`

```json
{
  "genres": [
    {"id": "1", "description": "Action"},
    {"id": "23", "description": "Indie"},
    {"id": "25", "description": "Adventure"}
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Steam genre ID (stored as string in API) |
| `description` | string | Genre name |

**Presence:** 74.6% of applications
**Note:** These are also normalized into the `application_genres` junction table

#### JSONB Structure: `ratings` (Age Ratings)

The `ratings` JSONB contains nested objects for different regional rating systems. Structure varies by region:

```json
{
  "esrb": {
    "rating": "m",
    "descriptors": "Blood and Gore\nViolence\nStrong Language",
    "interactive_elements": "Users Interact\nIn-Game Purchases",
    "use_age_gate": "true",
    "required_age": "17"
  },
  "pegi": {
    "rating": "18",
    "descriptors": "Violence\nBad Language"
  },
  "dejus": {
    "rating": "16",
    "descriptors": "Violência\nDrogas ilícitas",
    "rating_generated": "1",
    "banned": "0"
  }
}
```

**Common Rating Systems:**

| System | Region | Fields | Description |
|--------|--------|--------|-------------|
| `esrb` | North America | rating, descriptors, required_age | ESRB ratings (e, e10, t, m, ao) |
| `pegi` | Europe | rating, descriptors | PEGI ratings (3, 7, 12, 16, 18) |
| `dejus` | Brazil | rating, descriptors, banned | Brazilian rating system |
| `usk` | Germany | rating, descriptors | USK ratings (0, 6, 12, 16, 18) |
| `steam_germany` | Germany | rating, descriptors | Steam-specific German ratings |
| `cero` | Japan | rating, descriptors | CERO ratings (a, b, c, d, z) |

**Presence:** 77.6% of applications have some ratings data
**Note:** Content is multilingual; descriptors match regional language

#### JSONB Structure: `package_groups` (Purchase Options)

```json
{
  "package_groups": [
    {
      "name": "default",
      "title": "Buy Game Name",
      "description": "",
      "selection_text": "Select a purchase option",
      "save_text": "",
      "display_type": 0,
      "is_recurring_subscription": "false",
      "subs": [
        {
          "packageid": 123456,
          "percent_savings_text": "",
          "percent_savings": 0,
          "option_text": "Game Name - $19.99",
          "option_description": "",
          "can_get_free_license": "0",
          "is_free_license": false,
          "price_in_cents_with_discount": 1999
        }
      ]
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Package group identifier (usually "default") |
| `title` | string | Purchase section title |
| `selection_text` | string | Instruction text for user |
| `display_type` | integer | Display format indicator |
| `subs[]` | array | Array of available purchase packages |
| `subs[].packageid` | integer | Steam package ID |
| `subs[].price_in_cents_with_discount` | integer | Final price in cents |
| `subs[].percent_savings` | integer | Discount percentage |
| `subs[].option_text` | string | Purchase option display text |
| `subs[].is_free_license` | boolean | Whether package is free |

**Presence:** 56.5% of applications (primarily paid games)
**Note:** Free games typically have empty package_groups

---

### **Table: `reviews`**

Stores user-submitted reviews with full text and engagement metrics.

**Row Count:** 1,048,148 reviews  
**Primary Key:** `recommendationid`  
**Foreign Keys:** `appid` → `applications(appid)`  
**Indexes:** Primary key index, foreign key index on `appid`, HNSW vector index on `review_embedding`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `recommendationid` | `text` | PRIMARY KEY, NOT NULL | Unique review identifier |
| `appid` | `bigint` | FOREIGN KEY, NOT NULL | Application being reviewed |
| `author_steamid` | `text` | | Steam ID of review author |
| `author_playtime_forever` | `bigint` | | Author's total playtime (minutes) |
| `review_text` | `text` | | Full review content |
| `timestamp_created` | `bigint` | | Unix timestamp of review creation |
| `timestamp_updated` | `bigint` | | Unix timestamp of last update |
| `voted_up` | `boolean` | | TRUE for positive recommendation |
| `votes_up` | `bigint` | | Number of helpful votes |
| `votes_funny` | `bigint` | | Number of funny votes |
| `weighted_vote_score` | `numeric(10,8)` | | Steam-calculated helpfulness score |
| `review_embedding` | `vector(1024)` | | BGE-M3 embedding of review_text |

**Review Sentiment Analysis:**

- `voted_up = TRUE`: Positive recommendation
- `voted_up = FALSE`: Negative recommendation
- `weighted_vote_score`: Range 0.0-1.0, higher = more helpful

---

### **Table: `developers`**

Lookup table for unique game developers.

**Row Count:** 101,226 unique developers  
**Primary Key:** `developer_id`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `developer_id` | `serial` | PRIMARY KEY | Auto-incrementing developer ID |
| `developer_name` | `text` | UNIQUE, NOT NULL | Developer company/individual name |

---

### **Table: `publishers`**

Lookup table for unique game publishers.

**Row Count:** 85,699 unique publishers  
**Primary Key:** `publisher_id`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `publisher_id` | `serial` | PRIMARY KEY | Auto-incrementing publisher ID |
| `publisher_name` | `text` | UNIQUE, NOT NULL | Publisher company name |

---

### **Table: `genres`**

Lookup table for game genre classifications.

**Row Count:** 154 unique genres  
**Primary Key:** `genre_id`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `genre_id` | `integer` | PRIMARY KEY | Steam genre ID |
| `genre_description` | `text` | UNIQUE, NOT NULL | Genre name (e.g., "Action", "RPG") |

**Common Genres:** Action, Indie, Adventure, Casual, Strategy, RPG, Simulation, Sports, Racing, Early Access

---

### **Table: `categories`**

Lookup table for Steam feature categories.

**Row Count:** 462 unique categories  
**Primary Key:** `category_id`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `category_id` | `integer` | PRIMARY KEY | Steam category ID |
| `category_description` | `text` | UNIQUE, NOT NULL | Category name (e.g., "Single-player") |

**Common Categories:** Single-player, Multi-player, Steam Achievements, Steam Cloud, Controller Support, Steam Trading Cards

---

### **Table: `platforms`**

Lookup table for operating system platforms.

**Row Count:** 3 platforms  
**Primary Key:** `platform_id`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `platform_id` | `serial` | PRIMARY KEY | Auto-incrementing platform ID |
| `platform_name` | `platform_type` | UNIQUE, NOT NULL | Platform name (windows/mac/linux) |

---

### **Table: `embedding_runs`**

Tracks metadata for vector embedding generation batches.

**Primary Key:** `run_id`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `run_id` | `serial` | PRIMARY KEY | Auto-incrementing run ID |
| `model_name` | `text` | NOT NULL | Embedding model identifier |
| `vector_dimension` | `integer` | NOT NULL | Embedding vector size |
| `run_timestamp` | `timestamp` | DEFAULT CURRENT_TIMESTAMP | Embedding generation timestamp |

**Current Configuration:**

- Model: `BAAI/bge-m3`
- Dimension: 1024
- Supports 100+ languages

---

## **3.3 Junction Tables (Many-to-Many Relationships)**

### **Table: `application_developers`**

Links applications to their developers.

**Primary Key:** Composite (`appid`, `developer_id`)  
**Foreign Keys:** `appid` → `applications(appid)`, `developer_id` → `developers(developer_id)`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `appid` | `bigint` | FOREIGN KEY, NOT NULL | Application identifier |
| `developer_id` | `integer` | FOREIGN KEY, NOT NULL | Developer identifier |

---

### **Table: `application_publishers`**

Links applications to their publishers.

**Primary Key:** Composite (`appid`, `publisher_id`)  
**Foreign Keys:** `appid` → `applications(appid)`, `publisher_id` → `publishers(publisher_id)`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `appid` | `bigint` | FOREIGN KEY, NOT NULL | Application identifier |
| `publisher_id` | `integer` | FOREIGN KEY, NOT NULL | Publisher identifier |

---

### **Table: `application_genres`**

Links applications to their genre classifications.

**Primary Key:** Composite (`appid`, `genre_id`)  
**Foreign Keys:** `appid` → `applications(appid)`, `genre_id` → `genres(genre_id)`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `appid` | `bigint` | FOREIGN KEY, NOT NULL | Application identifier |
| `genre_id` | `integer` | FOREIGN KEY, NOT NULL | Genre identifier |

---

### **Table: `application_categories`**

Links applications to their feature categories.

**Primary Key:** Composite (`appid`, `category_id`)  
**Foreign Keys:** `appid` → `applications(appid)`, `category_id` → `categories(category_id)`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `appid` | `bigint` | FOREIGN KEY, NOT NULL | Application identifier |
| `category_id` | `integer` | FOREIGN KEY, NOT NULL | Category identifier |

---

### **Table: `application_platforms`**

Links applications to their supported platforms.

**Primary Key:** Composite (`appid`, `platform_id`)  
**Foreign Keys:** `appid` → `applications(appid)`, `platform_id` → `platforms(platform_id)`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `appid` | `bigint` | FOREIGN KEY, NOT NULL | Application identifier |
| `platform_id` | `integer` | FOREIGN KEY, NOT NULL | Platform identifier |

---

## **3.4 Views & Materialized Views**

### **View: `application_platforms_view`**

**Type:** Standard View  
**Purpose:** Simplified platform support query interface

```sql
CREATE VIEW application_platforms_view AS
SELECT 
    a.appid,
    a.name,
    p.platform_name
FROM applications a
JOIN application_platforms ap ON a.appid = ap.appid
JOIN platforms p ON ap.platform_id = p.platform_id;
```

**Columns:**

- `appid` (bigint) - Application ID
- `name` (text) - Application name
- `platform_name` (platform_type) - Supported platform

---

### **Materialized View: `game_features_view`**

**Type:** Materialized View (pre-computed)  
**Purpose:** Aggregated game metrics for analytical queries  
**Refresh Strategy:** Manual or scheduled refresh required

```sql
CREATE MATERIALIZED VIEW game_features_view AS
SELECT 
    a.appid,
    a.name,
    a.mat_final_price / 100.0 AS price,
    COUNT(DISTINCT r.recommendationid) AS review_count,
    AVG(CASE WHEN r.voted_up THEN 1.0 ELSE 0.0 END) AS review_score,
    COUNT(DISTINCT ad.developer_id) AS developer_count,
    COUNT(DISTINCT dlc.appid) AS dlc_count
FROM applications a
LEFT JOIN reviews r ON a.appid = r.appid
LEFT JOIN application_developers ad ON a.appid = ad.appid
LEFT JOIN applications dlc ON dlc.type = 'dlc' AND a.appid = ANY(dlc.parent_appids)
WHERE a.type = 'game'
GROUP BY a.appid, a.name, a.mat_final_price
HAVING COUNT(DISTINCT r.recommendationid) >= 50;
```

**Columns:**

- `appid` (bigint) - Application ID
- `name` (text) - Game name
- `price` (numeric) - Price in dollars
- `review_count` (bigint) - Total number of reviews
- `review_score` (numeric) - Positive review ratio (0.0-1.0)
- `developer_count` (bigint) - Number of developers
- `dlc_count` (bigint) - Number of DLC packages

**Use Case:** Pre-computed for games with 50+ reviews to accelerate recommendation system queries and success prediction models.

---

# 🛠️ **4. Usage & Query Patterns**

This section provides practical guidance for querying the dataset effectively, including performance optimization and common analytical patterns.

## **4.1 Query Performance Guidelines**

### Best Practices

**Materialized Columns for Common Queries:**

- Use `mat_*` columns for platform, pricing, and achievement queries instead of parsing JSONB
- Example: `WHERE mat_supports_windows = TRUE` instead of `WHERE pc_requirements IS NOT NULL`

**Vector Search Optimization:**

- Always use HNSW indexes for embedding similarity searches
- Limit results with `ORDER BY description_embedding <=> query_vector LIMIT 10`
- Pre-compute query vectors outside of database for repeated searches

**JSONB Query Patterns:**

- Use `->` for JSON object traversal, `->>` for text extraction
- Apply GIN indexes for containment queries: `WHERE price_overview @> '{"currency": "USD"}'`
- Avoid full-text search on JSONB without appropriate indexes

### Common Query Patterns

**Platform-Specific Game Discovery:**

```sql
-- Using materialized columns (fast)
SELECT appid, name, mat_final_price
FROM applications
WHERE mat_supports_linux = TRUE
  AND type = 'game'
  AND mat_final_price < 2000
ORDER BY mat_final_price;
```

**Semantic Game Search:**

```sql
-- Find games similar to a query embedding
SELECT appid, name, short_description,
       description_embedding <=> '[query_vector]' AS similarity
FROM applications
WHERE type = 'game'
ORDER BY description_embedding <=> '[query_vector]'
LIMIT 10;
```

**Review Sentiment Analysis:**

```sql
-- Calculate review metrics by genre
SELECT 
    g.genre_description,
    COUNT(r.recommendationid) AS total_reviews,
    AVG(CASE WHEN r.voted_up THEN 1.0 ELSE 0.0 END) AS positive_ratio
FROM reviews r
JOIN applications a ON r.appid = a.appid
JOIN application_genres ag ON a.appid = ag.appid
JOIN genres g ON ag.genre_id = g.genre_id
WHERE a.type = 'game'
GROUP BY g.genre_description
ORDER BY total_reviews DESC;
```

## **4.2 JSONB Query Examples**

### Accessing Nested JSONB Data

**Extract Price Information:**

```sql
-- Get games with specific currency
SELECT appid, name, 
       price_overview->>'currency' as currency,
       (price_overview->>'final')::int / 100.0 as price_usd
FROM applications
WHERE price_overview->>'currency' = 'USD'
  AND type = 'game';

-- Find discounted games
SELECT appid, name,
       (price_overview->>'initial')::int / 100.0 as original_price,
       (price_overview->>'final')::int / 100.0 as sale_price,
       (price_overview->>'discount_percent')::int as discount
FROM applications
WHERE (price_overview->>'discount_percent')::int > 0
ORDER BY discount DESC;
```

**Query System Requirements:**

```sql
-- Games requiring high-end GPUs (using materialized column)
SELECT appid, name, mat_pc_graphics_rec
FROM applications
WHERE mat_pc_graphics_rec ILIKE '%RTX%'
   OR mat_pc_graphics_rec ILIKE '%3070%'
   OR mat_pc_graphics_rec ILIKE '%3080%';

-- Parse minimum RAM from raw JSONB
SELECT appid, name,
       pc_requirements->>'minimum' as raw_requirements,
       mat_pc_memory_min as parsed_ram
FROM applications
WHERE pc_requirements->>'minimum' IS NOT NULL
LIMIT 10;
```

**Extract Achievement Data:**

```sql
-- Games with high achievement counts
SELECT appid, name,
       (achievements->>'total')::int as achievement_count
FROM applications
WHERE achievements IS NOT NULL
  AND (achievements->>'total')::int > 100
ORDER BY achievement_count DESC;

-- Get highlighted achievements
SELECT appid, name,
       jsonb_array_length(achievements->'highlighted') as featured_count,
       achievements->'highlighted'->0->>'name' as first_achievement
FROM applications
WHERE achievements->'highlighted' IS NOT NULL;
```

**Work with Screenshots and Media:**

```sql
-- Count screenshots per game
SELECT appid, name,
       jsonb_array_length(screenshots) as screenshot_count
FROM applications
WHERE screenshots IS NOT NULL
ORDER BY screenshot_count DESC
LIMIT 20;

-- Extract video trailer URLs
SELECT appid, name,
       movies->0->>'name' as trailer_name,
       movies->0->'mp4'->>'max' as video_url
FROM applications
WHERE movies IS NOT NULL
  AND jsonb_array_length(movies) > 0;
```

**Query Rating Systems:**

```sql
-- Games with mature ESRB ratings
SELECT appid, name,
       ratings->'esrb'->>'rating' as esrb_rating,
       ratings->'esrb'->>'descriptors' as content_warnings
FROM applications
WHERE ratings->'esrb'->>'rating' IN ('m', 'ao');

-- Multi-region rating comparison
SELECT appid, name,
       ratings->'esrb'->>'rating' as esrb,
       ratings->'pegi'->>'rating' as pegi,
       ratings->'usk'->>'rating' as usk
FROM applications
WHERE ratings IS NOT NULL
  AND ratings ? 'esrb'
  AND ratings ? 'pegi';
```

**Advanced JSONB Containment Queries:**

```sql
-- Find games with specific category (using @> containment operator)
SELECT appid, name
FROM applications
WHERE categories @> '[{"id": 22}]'  -- Steam Achievements
LIMIT 100;

-- Games with both single-player and multi-player
SELECT appid, name
FROM applications
WHERE categories @> '[{"id": 2}]'   -- Single-player
  AND categories @> '[{"id": 1}]';  -- Multi-player

-- Search within JSONB text content
SELECT appid, name,
       content_descriptors->>'notes' as warnings
FROM applications
WHERE content_descriptors->>'notes' ILIKE '%violence%';
```

### JSONB Performance Tips

**Use GIN Indexes for Containment:**

```sql
-- Create index for fast containment queries
CREATE INDEX idx_categories_gin ON applications USING GIN (categories);
CREATE INDEX idx_genres_gin ON applications USING GIN (genres);

-- Now this query is fast:
SELECT * FROM applications 
WHERE categories @> '[{"id": 22}]';
```

**Prefer Materialized Columns When Possible:**

```sql
-- SLOW: Parse JSONB on every query
SELECT * FROM applications
WHERE (price_overview->>'final')::int < 1000;

-- FAST: Use pre-materialized column
SELECT * FROM applications
WHERE mat_final_price < 1000;
```

**Extract Arrays Efficiently:**

```sql
-- Extract all screenshot URLs as array
SELECT appid,
       array_agg(screenshot->>'path_full') as screenshot_urls
FROM applications,
     jsonb_array_elements(screenshots) as screenshot
WHERE screenshots IS NOT NULL
GROUP BY appid
LIMIT 10;
```

## **4.3 Data Quality Considerations**

### Known Limitations

**Currency Bias:**

- 59.5% of applications show USD pricing due to API query origin
- Currency reflects the geographic region from which data was collected
- For comparative pricing analysis, filter to single currency or use exchange rates

**PC Requirements Parsing:**

- Phase 9 materialized columns use regex parsing of HTML text
- Parsing accuracy ~85-90% due to inconsistent formatting
- Always validate critical requirements against raw `pc_requirements` JSONB

**Review Coverage:**

- Not all applications have reviews
- Review embeddings prioritized for top 10,000 most-reviewed games
- Filter by `review_count > 0` for review-dependent analyses

**API Success Rate:**

- 56% success rate in data collection (remainder are delisted/regional-locked)
- Check `success = TRUE` to ensure complete application data
- Failed records retain basic app list metadata only

---

# 📚 **5. References & Related Resources**

This section provides comprehensive links to related documentation, external resources, and supporting materials.

## **5.1 Internal References**

| **Document Type** | **Title** | **Relationship** | **Link** |
|-------------------|-----------|------------------|----------|
| Database Schema | PostgreSQL Database Schema | Implementation of this data dictionary | [postgresql-database-schema.md](postgresql-database-schema.md) |
| Methodology | Steam API Collection | Source data structure and collection process | [steam-api-collection.md](docs/methodologies/steam-api-collection.md) |
| Methodology | Vector Embeddings | Embedding generation and semantic search | [vector-embeddings.md](docs/methodologies/vector-embeddings.md) |
| Methodology | Data Validation & QA | Quality assurance procedures | [data-validaton-and-qa.md](docs/methodologies/data-validaton-and-qa.md) |
| Analysis | Steam 5K Dataset Analysis | Initial dataset exploration findings | [steam-5k-dataset-analysis.md](docs/analytics/steam-5k-dataset-analysis.md) |
| Guide | Data Access Guide | Connecting to and querying the database | [data-access.md](data-access.md) |

## **5.2 External Resources**

| **Resource Type** | **Title** | **Description** | **Link** |
|-------------------|-----------|-----------------|----------|
| Official Docs | PostgreSQL 16 Documentation | Core database features and SQL reference | [postgresql.org/docs/16/](https://www.postgresql.org/docs/16/) |
| Official Docs | pgvector Documentation | Vector operations and indexing | [github.com/pgvector/pgvector](https://github.com/pgvector/pgvector) |
| Official Docs | PostgreSQL JSONB Functions | JSONB operators and query methods | [postgresql.org/docs/16/functions-json.html](https://www.postgresql.org/docs/16/functions-json.html) |
| Official API | Steam Web API | Source data API documentation | [steamcommunity.com/dev](https://steamcommunity.com/dev) |
| Model | BGE-M3 Embeddings | Multilingual embedding model | [huggingface.co/BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) |
| Dataset | Original Kaggle Steam Dataset (2019) | Historical reference dataset | [kaggle.com/nikdavis/steam-store-games](https://www.kaggle.com/nikdavis/steam-store-games) |

---

# 📜 **6. Documentation Metadata**

This section provides comprehensive information about document creation, revision history, and authorship.

## **6.1 Change Log**

| **Version** | **Date** | **Changes** | **Author** |
|------------|----------|-------------|------------|
| 1.0 | 2025-10-05 | Initial comprehensive data dictionary creation covering all tables, JSONB structures, and materialized columns | VintageDon |

## **6.2 Authorship & Collaboration**

**Primary Author:** VintageDon ([GitHub Profile](https://github.com/vintagedon))  
**AI Assistance:** Claude 3.5 Sonnet (claude-sonnet-4-20250514)  
**Methodology:** Request-Analyze-Verify-Generate-Validate (RAVGV) collaborative approach  
**Quality Assurance:** All schema definitions validated against production PostgreSQL 16.10 database and cross-referenced with implementation scripts

## **6.3 Technical Notes**

- **Schema Version:** Based on PostgreSQL 16.10 production database
- **Last Schema Update:** Phase 9 - PC Requirements Materialization (September 2025)
- **Validation Sources:**
  - `/scripts/04-postgres_schema_design/schema.sql` - Base schema definition
  - `/work-logs/08-materialization-columns/` - Phase 2 materialization
  - `/work-logs/09-pc-requirements-materialization/` - Phase 9 requirements parsing
  - Production database inspection via `pg_dump` and `\d+` commands

*Document Version: 1.0 | Last Updated: 2025-10-05 | Status: Published*

---

**Repository Navigation:** This data dictionary is part of the [Steam Dataset 2025](../README.md) documentation suite. For schema implementation details, see [PostgreSQL Database Schema](postgresql-database-schema.md). For data access instructions, see [Data Access Guide](data-access.md).
