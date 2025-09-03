-- =====================================================================================================================
-- Steam Dataset 2025 - Core PostgreSQL Schema with pgvector Support
-- Version: 1.2
-- Change: Corrected all author statistic columns in 'reviews' table from INTEGER to BIGINT to prevent overflow.
-- =====================================================================================================================

-- Enable pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Create enum types for better data consistency
CREATE TYPE app_type AS ENUM ('game', 'dlc', 'software', 'video', 'demo', 'music', 'advertising', 'mod', 'episode', 'series');
CREATE TYPE platform_type AS ENUM ('windows', 'mac', 'linux');

-- =====================================================================================================================
-- Core Tables
-- =====================================================================================================================

CREATE TABLE applications (
    appid BIGINT PRIMARY KEY,
    steam_appid BIGINT,
    name_from_applist TEXT NOT NULL,
    name TEXT,
    type app_type,
    is_free BOOLEAN DEFAULT false,
    release_date TEXT,
    required_age INTEGER DEFAULT 0,
    metacritic_score INTEGER,
    recommendations_total INTEGER,
    header_image TEXT,
    background TEXT,
    detailed_description TEXT,
    short_description TEXT,
    about_the_game TEXT,
    supported_languages TEXT,
    description_embedding vector(384),
    combined_text TEXT GENERATED ALWAYS AS ( COALESCE(name, '') || ' ' || COALESCE(short_description, '') || ' ' || COALESCE(about_the_game, '') ) STORED,
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
    base_app_id BIGINT,
    success BOOLEAN NOT NULL DEFAULT false,
    fetched_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_metacritic_score CHECK (metacritic_score IS NULL OR (metacritic_score >= 0 AND metacritic_score <= 100)),
    CONSTRAINT valid_required_age CHECK (required_age >= 0)
);

-- Individual user reviews table with vector embeddings
CREATE TABLE reviews (
    recommendationid TEXT PRIMARY KEY,
    appid BIGINT NOT NULL REFERENCES applications(appid) ON DELETE CASCADE,
    
    -- --- START OF FIX: Changed INTEGER to BIGINT for all author stats ---
    author_steamid TEXT,
    author_num_games_owned BIGINT,
    author_num_reviews BIGINT,
    author_playtime_forever BIGINT DEFAULT 0,
    author_playtime_last_two_weeks BIGINT DEFAULT 0,
    author_playtime_at_review BIGINT DEFAULT 0,
    author_last_played BIGINT,
    -- --- END OF FIX ---
    
    language TEXT DEFAULT 'english',
    review_text TEXT,
    review_embedding vector(384),
    timestamp_created BIGINT,
    timestamp_updated BIGINT,
    voted_up BOOLEAN,
    votes_up BIGINT DEFAULT 0,
    votes_funny BIGINT DEFAULT 0,
    weighted_vote_score NUMERIC(10,8),
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
-- Lookup & Junction Tables (Unchanged)
-- =====================================================================================================================

CREATE TABLE developers ( id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL );
CREATE TABLE publishers ( id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL );
CREATE TABLE genres ( id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL );
CREATE TABLE categories ( id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL );
CREATE TABLE platforms ( id SERIAL PRIMARY KEY, name platform_type UNIQUE NOT NULL );

CREATE TABLE application_developers ( appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE, developer_id INTEGER REFERENCES developers(id) ON DELETE CASCADE, PRIMARY KEY (appid, developer_id) );
CREATE TABLE application_publishers ( appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE, publisher_id INTEGER REFERENCES publishers(id) ON DELETE CASCADE, PRIMARY KEY (appid, publisher_id) );
CREATE TABLE application_genres ( appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE, genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE, PRIMARY KEY (appid, genre_id) );
CREATE TABLE application_categories ( appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE, category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE, PRIMARY KEY (appid, category_id) );
CREATE TABLE application_platforms ( appid BIGINT REFERENCES applications(appid) ON DELETE CASCADE, platform_id INTEGER REFERENCES platforms(id) ON DELETE CASCADE, PRIMARY KEY (appid, platform_id) );

-- =====================================================================================================================
-- Indexes & Functions (Unchanged)
-- =====================================================================================================================

CREATE INDEX IF NOT EXISTS idx_applications_name ON applications(name);
CREATE INDEX IF NOT EXISTS idx_applications_type ON applications(type);
CREATE INDEX IF NOT EXISTS idx_reviews_appid ON reviews(appid);
CREATE INDEX IF NOT EXISTS idx_reviews_voted_up ON reviews(voted_up);

CREATE OR REPLACE FUNCTION update_updated_at_column() RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$ language 'plpgsql';
CREATE TRIGGER update_applications_updated_at BEFORE UPDATE ON applications FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_reviews_updated_at BEFORE UPDATE ON reviews FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE FUNCTION get_database_stats()
RETURNS TABLE( total_applications BIGINT, total_games BIGINT, total_dlc BIGINT, total_reviews BIGINT, total_developers BIGINT, total_publishers BIGINT, applications_with_embeddings BIGINT, reviews_with_embeddings BIGINT ) AS $$
BEGIN
    RETURN QUERY SELECT (SELECT COUNT(*) FROM applications), (SELECT COUNT(*) FROM applications WHERE type = 'game'), (SELECT COUNT(*) FROM applications WHERE type = 'dlc'), (SELECT COUNT(*) FROM reviews), (SELECT COUNT(*) FROM developers), (SELECT COUNT(*) FROM publishers), (SELECT COUNT(*) FROM applications WHERE description_embedding IS NOT NULL), (SELECT COUNT(*) FROM reviews WHERE review_embedding IS NOT NULL);
END;
$$ LANGUAGE plpgsql;

INSERT INTO platforms (name) VALUES ('windows'), ('mac'), ('linux') ON CONFLICT (name) DO NOTHING;

