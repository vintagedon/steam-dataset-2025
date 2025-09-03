<!--
---
title: "PostgreSQL Database Schema Documentation"
description: "Comprehensive database schema documentation for Steam Dataset 2025, covering table structures, field definitions, relationships, and JSONB optimization strategies for 260+ discovered Steam API fields"
author: "VintageDon - https://github.com/vintagedon"
ai_contributor: "Claude Sonnet 4"
date: "2025-09-02"
version: "1.0" 
status: "Published"
tags:
- type: [kb-article/schema-documentation/database-design]
- domain: [database-design/postgresql/schema-architecture]
- tech: [postgresql-16/jsonb/relational-design/indexing]
- audience: [database-developers/data-engineers/schema-architects]
related_documents:
- "[Steam API Schema Analysis](steam-api-schema-analysis.md)"
- "[PostgreSQL Performance Analysis](database-performance-analysis.md)"
- "[Steam 5K Dataset Analysis](steam-5k-analysis.md)"
---
-->

# 🗄️ PostgreSQL Database Schema Documentation

This document provides comprehensive schema documentation for the Steam Dataset 2025 database implementation, covering normalized table structures, field definitions, relationships, and JSONB optimization strategies. The schema supports 8,711 applications, 36,265 reviews, and complex metadata relationships with pgvector support for semantic search capabilities.

---

# 🎯 1. Introduction

This section establishes the database schema architecture and design principles underlying the Steam Dataset 2025 multi-modal implementation.

## 1.1 Purpose

This schema documentation provides definitive guidance for database developers and data engineers working with the Steam Dataset 2025 implementation. It defines table structures, field relationships, indexing strategies, and JSONB optimization approaches that enable both traditional relational queries and modern vector-based semantic search operations.

## 1.2 Scope

Schema Implementation Coverage:

- Core applications table with 32 fields including JSONB and vector columns
- Reviews table with vector embeddings for 36,265+ user reviews
- Normalized lookup tables for developers, publishers, genres, and categories
- Junction tables supporting many-to-many relationships
- Custom enum types and database functions for enhanced data integrity
- pgvector extension integration for semantic search capabilities

## 1.3 Target Audience

Primary Users: Database developers, data engineers, schema architects working with PostgreSQL  
Secondary Users: Data scientists needing schema understanding, application developers  
Background Assumed: PostgreSQL administration, database design patterns, vector database concepts

## 1.4 Overview

The schema implements a hybrid relational-document architecture, combining normalized relational structures for structured data with JSONB columns for complex Steam API responses. Vector columns enable semantic search across application descriptions and user reviews, while comprehensive indexing strategies ensure query performance across diverse workload patterns.

---

# 🔗 2. Dependencies & Relationships

This section maps the database schema relationships and technical dependencies that enable comprehensive Steam dataset storage and analysis.

## 2.1 Related Components

| Component | Relationship | Integration Points | Documentation |
|---------------|------------------|------------------------|-------------------|
| Steam API Analysis | Field definitions and data type mappings | JSONB structure design, column specifications | [Steam API Schema Analysis](steam-api-schema-analysis.md) |
| Performance Infrastructure | Query optimization and indexing strategies | Index design, vector operations, JSONB queries | [PostgreSQL Performance Analysis](database-performance-analysis.md) |
| Statistical Analysis | Data validation and analytical query patterns | Aggregation queries, genre analysis, quality metrics | [Steam 5K Dataset Analysis](steam-5k-analysis.md) |
| pgvector Extension | Semantic search and similarity operations | Vector embeddings, HNSW indexing, similarity queries | [pgvector Documentation](https://github.com/pgvector/pgvector) |

## 2.2 External Dependencies

- [pgvector Extension](https://github.com/pgvector/pgvector) - Vector similarity search support for semantic operations
- [PostgreSQL 16](https://www.postgresql.org/) - Advanced JSONB support, generated columns, custom types
- [Steam Web API](https://steamcommunity.com/dev) - Official data source defining field structures and relationships

---

# ⚙️ 3. Technical Documentation

This section provides detailed schema definitions, table structures, and relationship mappings derived from the implemented PostgreSQL database.

## 3.1 Schema Architecture Overview

The database implements a hybrid relational-document architecture optimized for both structured queries and flexible JSON data storage.

Core Design Principles:

- Hybrid Architecture: Normalized tables for structured data, JSONB for complex Steam API responses
- Vector Integration: Native pgvector support for semantic search across descriptions and reviews
- Performance Optimization: Strategic indexing for both relational and vector query patterns
- Data Integrity: Custom enum types, constraints, and referential integrity enforcement
- Analytical Support: Generated columns and functions optimized for data science workflows

Schema Version: 1.2 (BIGINT overflow corrections for review author statistics)

## 3.2 Core Table Definitions

### 3.2.1 Applications Table

Primary table storing Steam application metadata with hybrid relational-document structure.

```sql
CREATE TABLE applications (
    -- Primary Identifiers
    appid BIGINT PRIMARY KEY,
    steam_appid BIGINT,
    name_from_applist TEXT NOT NULL,
    name TEXT,
    
    -- Core Metadata
    type app_type,
    is_free BOOLEAN DEFAULT false,
    release_date TEXT,
    required_age INTEGER DEFAULT 0,
    
    -- Quality & Engagement Metrics
    metacritic_score INTEGER,
    recommendations_total INTEGER,
    
    -- Media & Content
    header_image TEXT,
    background TEXT,
    detailed_description TEXT,
    short_description TEXT,
    about_the_game TEXT,
    supported_languages TEXT,
    
    -- Vector Search Support
    description_embedding vector(384),
    combined_text TEXT GENERATED ALWAYS AS (
        COALESCE(name, '') || ' ' || 
        COALESCE(short_description, '') || ' ' || 
        COALESCE(about_the_game, '')
    ) STORED,
    
    -- Complex Data Structures (JSONB)
    price_overview JSONB,
    pc_requirements JSONB,
    mac_requirements JSONB, 
    linux_requirements JSONB,
    content_descriptors JSONB,
    package_groups JSONB,
    achievements JSONB,
    screenshots JSONB,
    movies JSONB,
    ratings JSONB,
    
    -- Relationships & Metadata
    base_app_id BIGINT,
    success BOOLEAN NOT NULL DEFAULT false,
    fetched_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Data Integrity Constraints
    CONSTRAINT valid_metacritic_score CHECK (
        metacritic_score IS NULL OR 
        (metacritic_score >= 0 AND metacritic_score <= 100)
    ),
    CONSTRAINT valid_required_age CHECK (required_age >= 0)
);
```

Key Field Definitions:

| Field | Type | Purpose | Notes |
|-------|------|---------|-------|
| `appid` | BIGINT | Steam application unique identifier | Primary key, references across all tables |
| `type` | app_type | Application category enum | Values: game, dlc, software, video, demo, music, etc. |
| `description_embedding` | vector(384) | Semantic search vector | Generated from combined_text using sentence transformers |
| `combined_text` | TEXT | Generated column for vector input | Concatenates name, short_description, about_the_game |
| `price_overview` | JSONB | Pricing and discount information | Complex Steam pricing structure |
| `*_requirements` | JSONB | Platform system requirements | Parsed HTML requirements by platform |

### 3.2.2 Reviews Table

User review data with vector embeddings for sentiment and semantic analysis.

```sql
CREATE TABLE reviews (
    -- Primary Identification
    recommendationid TEXT PRIMARY KEY,
    appid BIGINT NOT NULL REFERENCES applications(appid) ON DELETE CASCADE,
    
    -- Author Information (BIGINT for overflow prevention)
    author_steamid TEXT,
    author_num_games_owned BIGINT,
    author_num_reviews BIGINT,
    author_playtime_forever BIGINT DEFAULT 0,
    author_playtime_last_two_weeks BIGINT DEFAULT 0,
    author_playtime_at_review BIGINT DEFAULT 0,
    author_last_played BIGINT,
    
    -- Review Content
    language TEXT DEFAULT 'english',
    review_text TEXT,
    review_embedding vector(384),
    
    -- Temporal Data
    timestamp_created BIGINT,
    timestamp_updated BIGINT,
    
    -- Community Engagement
    voted_up BOOLEAN,
    votes_up BIGINT DEFAULT 0,
    votes_funny BIGINT DEFAULT 0,
    weighted_vote_score NUMERIC(10,8),
    comment_count BIGINT DEFAULT 0,
    
    -- Purchase Context
    steam_purchase BOOLEAN DEFAULT true,
    received_for_free BOOLEAN DEFAULT false,
    written_during_early_access BOOLEAN DEFAULT false,
    
    -- Audit Fields
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Data Integrity
    CHECK (votes_up >= 0),
    CHECK (votes_funny >= 0),
    CHECK (comment_count >= 0)
);
```

Schema v1.2 Changes:

All author statistic columns changed from INTEGER to BIGINT to prevent overflow on high-activity accounts:

- `author_num_games_owned`, `author_num_reviews`, `author_playtime_*` fields
- Critical fix for data integrity with power users owning thousands of games

## 3.3 Lookup & Junction Table Architecture

Normalized relationship management using lookup tables and many-to-many junction tables.

### 3.3.1 Lookup Tables

```sql
-- Entity Lookup Tables
CREATE TABLE developers (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE NOT NULL 
);

CREATE TABLE publishers (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE NOT NULL 
);

CREATE TABLE genres (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE NOT NULL 
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE NOT NULL 
);

CREATE TABLE platforms (
    id SERIAL PRIMARY KEY, 
    name platform_type UNIQUE NOT NULL 
);
```

### 3.3.2 Junction Tables (Many-to-Many Relationships)

```sql
-- Application Relationship Tables
CREATE TABLE application_developers (
    appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE,
    developer_id INTEGER REFERENCES developers(id) ON DELETE CASCADE,
    PRIMARY KEY (appid, developer_id)
);

CREATE TABLE application_publishers (
    appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE,
    publisher_id INTEGER REFERENCES publishers(id) ON DELETE CASCADE,
    PRIMARY KEY (appid, publisher_id)
);

CREATE TABLE application_genres (
    appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
    PRIMARY KEY (appid, genre_id)
);

CREATE TABLE application_categories (
    appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (appid, category_id)
);

CREATE TABLE application_platforms (
    appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE,
    platform_id INTEGER REFERENCES platforms(id) ON DELETE CASCADE,
    PRIMARY KEY (appid, platform_id)
);
```

Relationship Design Pattern:

- Cascade Deletion: ON DELETE CASCADE ensures referential integrity
- Composite Primary Keys: Prevent duplicate relationships
- Foreign Key Constraints: Maintain data consistency across tables

## 3.4 Custom Types & Database Functions

Advanced PostgreSQL features enhancing data integrity and analytical capabilities.

### 3.4.1 Enum Type Definitions

```sql
-- Application Type Enumeration
CREATE TYPE app_type AS ENUM (
    'game', 'dlc', 'software', 'video', 'demo', 
    'music', 'advertising', 'mod', 'episode', 'series'
);

-- Platform Type Enumeration  
CREATE TYPE platform_type AS ENUM ('windows', 'mac', 'linux');
```

### 3.4.2 Database Functions

```sql
-- Automatic timestamp update trigger
CREATE OR REPLACE FUNCTION update_updated_at_column() 
RETURNS TRIGGER AS $$
BEGIN 
    NEW.updated_at = NOW(); 
    RETURN NEW; 
END; 
$$ language 'plpgsql';

-- Database statistics function
CREATE OR REPLACE FUNCTION get_database_stats()
RETURNS TABLE(
    total_applications BIGINT,
    total_games BIGINT,
    total_dlc BIGINT,
    total_reviews BIGINT,
    total_developers BIGINT,
    total_publishers BIGINT,
    applications_with_embeddings BIGINT,
    reviews_with_embeddings BIGINT
) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        (SELECT COUNT(*) FROM applications),
        (SELECT COUNT(*) FROM applications WHERE type = 'game'),
        (SELECT COUNT(*) FROM applications WHERE type = 'dlc'),
        (SELECT COUNT(*) FROM reviews),
        (SELECT COUNT(*) FROM developers),
        (SELECT COUNT(*) FROM publishers),
        (SELECT COUNT(*) FROM applications WHERE description_embedding IS NOT NULL),
        (SELECT COUNT(*) FROM reviews WHERE review_embedding IS NOT NULL);
END;
$$ LANGUAGE plpgsql;
```

## 3.5 Indexing Strategy

Performance-optimized indexing supporting diverse query patterns.

### 3.5.1 Standard Indexes

```sql
-- Relational Query Optimization
CREATE INDEX IF NOT EXISTS idx_applications_name ON applications(name);
CREATE INDEX IF NOT EXISTS idx_applications_type ON applications(type);
CREATE INDEX IF NOT EXISTS idx_reviews_appid ON reviews(appid);
CREATE INDEX IF NOT EXISTS idx_reviews_voted_up ON reviews(voted_up);
```

### 3.5.2 Vector Indexes (Post-Import)

```sql
-- HNSW Indexes for Vector Similarity Search
CREATE INDEX ON applications USING hnsw (description_embedding vector_cosine_ops);
CREATE INDEX ON reviews USING hnsw (review_embedding vector_cosine_ops);
```

Vector Index Benefits:

- Logarithmic Search Time: HNSW enables fast approximate nearest neighbor search
- Semantic Query Support: Natural language queries against game descriptions
- Recommendation Engine: Content-based recommendations using vector similarity
- Scalable Performance: Maintains performance with 260,000+ applications

---

# 🛠️ 4. Usage & Maintenance

This section provides practical guidance for database schema utilization, query patterns, and maintenance procedures.

## 4.1 Usage Guidelines

Common Query Patterns:

```sql
-- Find games by genre with pricing information
SELECT a.name, a.type, a.price_overview->'final' as price_cents
FROM applications a
JOIN application_genres ag ON a.appid = ag.appid
JOIN genres g ON ag.genre_id = g.id  
WHERE g.name = 'Action' AND a.is_free = false;

-- Semantic search for similar games
SELECT name, short_description
FROM applications
WHERE description_embedding IS NOT NULL
ORDER BY description_embedding <=> (
    SELECT description_embedding FROM applications WHERE name = 'Cyberpunk 2077'
)
LIMIT 10;

-- Complex JSONB queries for system requirements
SELECT name, pc_requirements->'minimum'
FROM applications
WHERE pc_requirements->'minimum' ? 'Memory'
AND (pc_requirements->'minimum'->>'Memory' ILIKE '%16 GB%');
```

JSONB Query Optimization:

- Use `->` for JSON object access, `->>` for text extraction
- Leverage GIN indexes for containment queries (`@>`, `?`, `?|`)
- Consider materialized columns for frequently accessed JSONB values

## 4.2 Vector Operations

Embedding Generation Workflow:

```python
# Python example for generating embeddings
from sentence_transformers import SentenceTransformer
import psycopg2

model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate application embeddings
conn = psycopg2.connect("host=... dbname=steam5k user=...")
cur = conn.cursor()

cur.execute("SELECT appid, combined_text FROM applications WHERE combined_text IS NOT NULL")
for appid, text in cur.fetchall():
    embedding = model.encode(text)
    cur.execute(
        "UPDATE applications SET description_embedding = %s WHERE appid = %s",
        (embedding.tolist(), appid)
    )
conn.commit()
```

Vector Search Performance:

- Index Creation: Required after embedding population for performance
- Query Optimization: Use `vector_cosine_ops` for cosine similarity
- Batch Processing: Generate embeddings in batches for memory efficiency

## 4.3 Schema Evolution

Adding New Fields:

```sql
-- Safe schema evolution pattern
ALTER TABLE applications ADD COLUMN new_field TEXT;
CREATE INDEX CONCURRENTLY idx_applications_new_field ON applications(new_field);
```

JSONB Field Extensions:

New Steam API fields automatically stored in existing JSONB columns without schema migration, maintaining backward compatibility while supporting future API evolution.

Data Integrity Monitoring:

```sql
-- Validate referential integrity
SELECT COUNT(*) FROM reviews r 
LEFT JOIN applications a ON r.appid = a.appid 
WHERE a.appid IS NULL;

-- Check vector embedding coverage
SELECT 
    COUNT(*) as total_apps,
    COUNT(description_embedding) as with_embeddings,
    ROUND(COUNT(description_embedding) * 100.0 / COUNT(*), 2) as coverage_percent
FROM applications;
```

---

# 📚 5. References & Related Resources

This section provides comprehensive links to schema implementation resources, PostgreSQL documentation, and related technical materials.

## 5.1 Internal References

| Document Type | Title | Relationship | Link |
|-------------------|-----------|------------------|----------|
| API Analysis | Steam API Schema Analysis | Field discovery and type mapping foundation | [steam-api-schema-analysis.md](steam-api-schema-analysis.md) |
| Performance Analysis | PostgreSQL Database Benchmarks | Query performance and indexing validation | [database-performance-analysis.md](database-performance-analysis.md) |
| Statistical Analysis | Steam 5K Dataset Analysis | Data validation and query pattern examples | [steam-5k-analysis.md](steam-5k-analysis.md) |
| Implementation Scripts | PostgreSQL Schema Scripts | Actual schema creation and maintenance scripts | [../scripts/04-postgres_schema_design/README.md](../scripts/04-postgres_schema_design/README.md) |

## 5.2 External Resources

| Resource Type | Title | Description | Link |
|-------------------|-----------|-----------------|----------|
| Extension Documentation | pgvector GitHub Repository | Vector similarity search extension documentation | [pgvector](https://github.com/pgvector/pgvector) |
| Database Reference | PostgreSQL 16 JSONB Documentation | Comprehensive JSONB operations and indexing | [PostgreSQL Docs](https://www.postgresql.org/docs/16/datatype-json.html) |
| Vector Operations | pgvector Usage Guide | Vector indexing and similarity search best practices | [pgvector README](https://github.com/pgvector/pgvector#getting-started) |
| Schema Design | PostgreSQL Best Practices | Advanced PostgreSQL schema design patterns | [PostgreSQL Wiki](https://wiki.postgresql.org/wiki/Don%27t_Do_This) |

---

# 📜 6. Documentation Metadata

This section provides comprehensive information about schema development, implementation validation, and maintenance procedures.

## 6.1 Change Log

| Version | Date | Changes | Author |
|------------|----------|-------------|------------|
| 1.0 | 2025-08-31 | Initial schema implementation with pgvector support | VintageDon |
| 1.1 | 2025-09-01 | Added performance optimization indexes and database functions | VintageDon |
| 1.2 | 2025-09-02 | Fixed INTEGER to BIGINT overflow issues in reviews table | VintageDon |

*Document Version: 1.0 | Last Updated: 2025-09-02 | Status: Published*
