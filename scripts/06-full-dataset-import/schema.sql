-- =====================================================================================================================
-- Script Name:    schema.sql
-- Description:    The core PostgreSQL schema for the Steam Dataset 2025 project. It defines the tables,
--                 relationships, types, and functions necessary to store and query the collected Steam data.
--                 The design uses a normalized structure for data integrity, with JSONB columns for flexible
--                 storage of complex, nested API data, and includes pgvector support for AI/ML features.
--
-- Author:         vintagedon (https://github.com/vintagedon)
-- Repository:     https://github.com/vintagedon/steam-dataset-2025
--
-- Version:        1.2
-- Date:           2025-09-02
-- License:        MIT License
--
-- =====================================================================================================================
--   MODIFICATION HISTORY
-- =====================================================================================================================
--   Date:           Version:        Modified by:    Description of Changes:
--   --------------- --------------- --------------- -------------------------------------------------------------------
--   2025-09-02      1.2             vintagedon      Corrected all author statistic columns in 'reviews' table from
--                                                   INTEGER to BIGINT to prevent data overflow errors on import.
-- =====================================================================================================================


-- =====================================================================================================================
-- Prerequisites: Extensions and Custom Types
-- =====================================================================================================================

-- Enable pgvector extension. This must be installed on the PostgreSQL server first.
-- It adds the `vector` data type and enables high-performance similarity searches.
CREATE EXTENSION IF NOT EXISTS vector;

-- Using ENUM types is a data integrity best practice. It ensures that the 'type' columns
-- can only contain a pre-defined, valid set of values, preventing typos or invalid data
-- from being inserted at the database level.
CREATE TYPE app_type AS ENUM ('game', 'dlc', 'software', 'video', 'demo', 'music', 'advertising', 'mod', 'episode', 'series');
CREATE TYPE platform_type AS ENUM ('windows', 'mac', 'linux');

-- =====================================================================================================================
-- Core Tables
-- =====================================================================================================================

-- The `applications` table is the central "fact table" of our schema. It contains the primary
-- details for every application (game, DLC, etc.) on Steam.
CREATE TABLE applications (
    -- `appid` is the natural primary key from the Steam API. BIGINT is used to ensure
    -- compatibility with Steam's 64-bit IDs now and in the future.
    appid BIGINT PRIMARY KEY,
    steam_appid BIGINT,
    name_from_applist TEXT NOT NULL,
    name TEXT,
    type app_type,
    is_free BOOLEAN DEFAULT false,
    -- `release_date` is TEXT because the source data contains non-date strings like "To be announced".
    -- Transformation to a valid DATE type is handled in the ETL/application layer.
    release_date TEXT,
    required_age INTEGER DEFAULT 0,
    metacritic_score INTEGER,
    recommendations_total INTEGER,
    
    -- Storing URLs directly as TEXT is efficient.
    header_image TEXT,
    background TEXT,
    
    -- Full description fields, often containing HTML/BBCode.
    detailed_description TEXT,
    short_description TEXT,
    about_the_game TEXT,
    supported_languages TEXT,
    
    -- The `vector` type from pgvector, sized for the all-MiniLM-L6-v2 model (384 dimensions).
    description_embedding vector(384),
    -- A generated column that automatically concatenates key text fields. This is used to create
    -- a dedicated Full-Text Search index for efficient searching without complex application logic.
    combined_text TEXT GENERATED ALWAYS AS ( COALESCE(name, '') || ' ' || COALESCE(short_description, '') || ' ' || COALESCE(about_the_game, '') ) STORED,
    
    -- The JSONB data type is a critical design choice. Instead of creating hundreds of columns
    -- for every possible nested field from the API (many of which are sparse), we store the raw,
    -- complex objects directly. JSONB is a binary, indexed format, making it highly performant
    -- to query into these nested structures. This provides flexibility to handle API changes
    -- without requiring constant schema migrations.
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
    
    -- Foreign key relationship for DLCs, pointing back to their base game's appid.
    base_app_id BIGINT,
    
    -- Metadata about the API call itself.
    success BOOLEAN NOT NULL DEFAULT false,
    fetched_at TIMESTAMPTZ,
    
    -- Standard audit columns. TIMESTAMPTZ (timestamp with time zone) is a best practice
    -- for storing time data to avoid ambiguity.
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- CHECK constraints enforce business rules at the database level, providing a strong
    -- layer of data integrity.
    CONSTRAINT valid_metacritic_score CHECK (metacritic_score IS NULL OR (metacritic_score >= 0 AND metacritic_score <= 100)),
    CONSTRAINT valid_required_age CHECK (required_age >= 0)
);

-- The `reviews` table stores individual user reviews. This is a separate table because of the
-- one-to-many relationship: one application can have many thousands of reviews.
CREATE TABLE reviews (
    -- The `recommendationid` is the natural primary key from the API for a single review.
    recommendationid TEXT PRIMARY KEY,
    -- This is the foreign key linking the review back to the `applications` table.
    -- ON DELETE CASCADE ensures that if an application is deleted, all its associated reviews are also removed.
    appid BIGINT NOT NULL REFERENCES applications(appid) ON DELETE CASCADE,
    
    author_steamid TEXT,
    -- These columns were changed from INTEGER to BIGINT. This was a critical fix discovered during testing,
    -- as some user statistics (like playtime) can exceed the maximum value of a standard 32-bit integer.
    -- Using BIGINT (a 64-bit integer) is a robust solution that prevents data overflow errors.
    author_num_games_owned BIGINT,
    author_num_reviews BIGINT,
    author_playtime_forever BIGINT DEFAULT 0,
    author_playtime_last_two_weeks BIGINT DEFAULT 0,
    author_playtime_at_review BIGINT DEFAULT 0,
    author_last_played BIGINT, -- Stored as a Unix timestamp from the API.
    
    language TEXT DEFAULT 'english',
    review_text TEXT,
    review_embedding vector(384),
    
    -- Timestamps are stored as BIGINTs as they come from the API as Unix timestamps.
    timestamp_created BIGINT,
    timestamp_updated BIGINT,
    
    voted_up BOOLEAN,
    votes_up BIGINT DEFAULT 0,
    votes_funny BIGINT DEFAULT 0,
    weighted_vote_score NUMERIC(10,8), -- NUMERIC is used for precise fixed-point decimal values.
    comment_count BIGINT DEFAULT 0,
    
    steam_purchase BOOLEAN DEFAULT true,
    received_for_free BOOLEAN DEFAULT false,
    written_during_early_access BOOLEAN DEFAULT false,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CHECK (votes_up >= 0),
    CHECK (votes_funny >= 0),
    CHECK (comment_count >= 0)
);

-- =====================================================================================================================
-- Lookup & Junction Tables for Normalization
-- =====================================================================================================================

-- This section implements a normalized schema (specifically, Third Normal Form or 3NF).
-- Instead of storing developer or genre names as repeated text strings in the `applications` table,
-- we store them once in these "lookup" tables. This prevents data redundancy, reduces storage space,
-- and ensures data consistency (e.g., "Valve" and "valve" can't exist as two separate entities).

CREATE TABLE developers ( id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL );
CREATE TABLE publishers ( id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL );
CREATE TABLE genres ( id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL );
CREATE TABLE categories ( id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL );
CREATE TABLE platforms ( id SERIAL PRIMARY KEY, name platform_type UNIQUE NOT NULL );

-- "Junction" tables are used to create many-to-many relationships. For example, a single
-- application can have multiple genres, and a single genre can apply to many applications.
-- This table links the two, with ON DELETE CASCADE maintaining referential integrity.
CREATE TABLE application_developers ( appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE, developer_id INTEGER REFERENCES developers(id) ON DELETE CASCADE, PRIMARY KEY (appid, developer_id) );
CREATE TABLE application_publishers ( appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE, publisher_id INTEGER REFERENCES publishers(id) ON DELETE CASCADE, PRIMARY KEY (appid, publisher_id) );
CREATE TABLE application_genres ( appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE, genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE, PRIMARY KEY (appid, genre_id) );
CREATE TABLE application_categories ( appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE, category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE, PRIMARY KEY (appid, category_id) );
CREATE TABLE application_platforms ( appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE, platform_id INTEGER REFERENCES platforms(id) ON DELETE CASCADE, PRIMARY KEY (appid, platform_id) );

-- =====================================================================================================================
-- Indexes, Functions, and Triggers for Performance and Maintenance
-- =====================================================================================================================

-- B-tree indexes are created on columns that are frequently used in WHERE clauses, JOIN conditions,
-- or ORDER BY clauses to dramatically speed up query performance.
CREATE INDEX IF NOT EXISTS idx_applications_name ON applications(name);
CREATE INDEX IF NOT EXISTS idx_applications_type ON applications(type);
CREATE INDEX IF NOT EXISTS idx_reviews_appid ON reviews(appid);
CREATE INDEX IF NOT EXISTS idx_reviews_voted_up ON reviews(voted_up);

-- This function and the associated triggers are a database automation pattern. They ensure that the
-- `updated_at` column for any record is automatically set to the current time whenever that
-- record is updated, without requiring any logic in the application layer.
CREATE OR REPLACE FUNCTION update_updated_at_column() RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$ language 'plpgsql';
CREATE TRIGGER update_applications_updated_at BEFORE UPDATE ON applications FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_reviews_updated_at BEFORE UPDATE ON reviews FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- This function provides a simple, consolidated way to get high-level statistics about the
-- state of the database with a single, efficient query.
CREATE OR REPLACE FUNCTION get_database_stats()
RETURNS TABLE( total_applications BIGINT, total_games BIGINT, total_dlc BIGINT, total_reviews BIGINT, total_developers BIGINT, total_publishers BIGINT, applications_with_embeddings BIGINT, reviews_with_embeddings BIGINT ) AS $$
BEGIN
    RETURN QUERY SELECT (SELECT COUNT(*) FROM applications), (SELECT COUNT(*) FROM applications WHERE type = 'game'), (SELECT COUNT(*) FROM applications WHERE type = 'dlc'), (SELECT COUNT(*) FROM reviews), (SELECT COUNT(*) FROM developers), (SELECT COUNT(*) FROM publishers), (SELECT COUNT(*) FROM applications WHERE description_embedding IS NOT NULL), (SELECT COUNT(*) FROM reviews WHERE review_embedding IS NOT NULL);
END;
$$ LANGUAGE plpgsql;

-- Pre-populate the `platforms` table with its static, known values.
-- ON CONFLICT DO NOTHING makes this operation idempotent (safe to run multiple times).
INSERT INTO platforms (name) VALUES ('windows'), ('mac'), ('linux') ON CONFLICT (name) DO NOTHING;
