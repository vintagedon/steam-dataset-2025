# Steam Dataset 2025 - Database Schema Analysis

**Generated:** 2025-09-29 09:03:23 UTC
**Database:** steamfull
**PostgreSQL Version:** PostgreSQL 16.10 (Ubuntu 16.10-1.pgdg24.04+1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0, 64-bit
**pgvector Extension:** v0.8.0
**Total Size:** 21 GB

---

## Table of Contents

1. [Database Overview](#database-overview)
2. [Table Structures](#table-structures)
3. [Relationships](#relationships)
4. [Indexes](#indexes)
5. [JSONB Schema Documentation](#jsonb-schema-documentation)

---

## Database Overview

- **Total Tables:** 13
- **Total Views:** 1
- **Total Indexes:** 30

### Tables by Size

| Table Name | Rows (Actual) | Index/Table Ratio | Total Size | Table Size | Indexes Size | Columns |
|------------|---------------|-------------------|------------|------------|--------------|---------|
| `reviews` | 1,048,148 | 19.58x | 14 GB | 680 MB | 13 GB | 25 |
| `applications` | 239,664 | 2.85x | 6690 MB | 1736 MB | 4954 MB | 58 |
| `application_categories` | 1,077,156 | 0.76x | 79 MB | 45 MB | 34 MB | 2 |
| `application_platforms` | 334,671 | 2.71x | 52 MB | 14 MB | 38 MB | 2 |
| `application_genres` | 587,515 | 0.72x | 43 MB | 25 MB | 18 MB | 2 |
| `application_developers` | 250,817 | 0.69x | 18 MB | 11 MB | 7792 kB | 2 |
| `application_publishers` | 223,048 | 0.72x | 16 MB | 9648 kB | 6944 kB | 2 |
| `developers` | 101,226 | 1.35x | 11 MB | 4976 kB | 6696 kB | 2 |
| `publishers` | 85,699 | 1.40x | 10144 kB | 4232 kB | 5912 kB | 2 |
| `categories` | 462 | 3.50x | 144 kB | 32 kB | 112 kB | 2 |
| `embedding_runs` | 1 | 5.00x | 48 kB | 8192 bytes | 40 kB | 6 |
| `genres` | 154 | 5.00x | 48 kB | 8192 bytes | 40 kB | 2 |
| `platforms` | 3 | 4.00x | 40 kB | 8192 bytes | 32 kB | 2 |

---

## Table Structures

### `application_categories`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `appid` | bigint | ✗ | ✓ | ✓ |  |
| `category_id` | integer | ✗ | ✓ | ✓ |  |

---

### `application_developers`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `appid` | bigint | ✗ | ✓ | ✓ |  |
| `developer_id` | integer | ✗ | ✓ | ✓ |  |

---

### `application_genres`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `appid` | bigint | ✗ | ✓ | ✓ |  |
| `genre_id` | integer | ✗ | ✓ | ✓ |  |

---

### `application_platforms`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `appid` | bigint | ✗ | ✓ | ✓ |  |
| `platform_id` | integer | ✗ | ✓ | ✓ |  |

---

### `application_publishers`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `appid` | bigint | ✗ | ✓ | ✓ |  |
| `publisher_id` | integer | ✗ | ✓ | ✓ |  |

---

### `applications`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `appid` | bigint | ✗ | ✓ |  |  |
| `steam_appid` | bigint | ✓ |  |  |  |
| `name_from_applist` | text | ✗ |  |  |  |
| `name` | text | ✓ |  |  |  |
| `type` | app_type | ✓ |  |  |  |
| `is_free` | boolean | ✓ |  |  |  |
| `release_date` | date | ✓ |  |  |  |
| `required_age` | text | ✓ |  |  |  |
| `metacritic_score` | integer | ✓ |  |  |  |
| `recommendations_total` | integer | ✓ |  |  |  |
| `header_image` | text | ✓ |  |  |  |
| `background` | text | ✓ |  |  |  |
| `detailed_description` | text | ✓ |  |  |  |
| `short_description` | text | ✓ |  |  |  |
| `about_the_game` | text | ✓ |  |  |  |
| `supported_languages` | text | ✓ |  |  |  |
| `combined_text` | text | ✓ |  |  |  |
| `price_overview` | jsonb | ✓ |  |  |  |
| `pc_requirements` | jsonb | ✓ |  |  |  |
| `mac_requirements` | jsonb | ✓ |  |  |  |
| `linux_requirements` | jsonb | ✓ |  |  |  |
| `content_descriptors` | jsonb | ✓ |  |  |  |
| `package_groups` | jsonb | ✓ |  |  |  |
| `achievements` | jsonb | ✓ |  |  |  |
| `screenshots` | jsonb | ✓ |  |  |  |
| `movies` | jsonb | ✓ |  |  |  |
| `ratings` | jsonb | ✓ |  |  |  |
| `base_app_id` | bigint | ✓ |  |  |  |
| `success` | boolean | ✗ |  |  |  |
| `fetched_at` | timestamp with time zone | ✓ |  |  |  |
| `created_at` | timestamp with time zone | ✓ |  |  |  |
| `updated_at` | timestamp with time zone | ✓ |  |  |  |
| `supports_windows` | boolean | ✓ |  |  |  |
| `supports_mac` | boolean | ✓ |  |  |  |
| `supports_linux` | boolean | ✓ |  |  |  |
| `initial_price` | integer | ✓ |  |  |  |
| `final_price` | integer | ✓ |  |  |  |
| `discount_percent` | integer | ✓ |  |  |  |
| `currency` | text | ✓ |  |  |  |
| `achievement_count` | integer | ✓ |  |  |  |
| `embedding_run_id` | bigint | ✓ |  | ✓ |  |
| `description_embedding` | vector(1024) | ✓ |  |  |  |
| `mat_supports_windows` | boolean | ✓ |  |  | Materialized: Derived from pc_requirements JSONB. TRUE if non-null and non-empty object exists. Source of truth: pc_requirements column. Coverage: 99.997% of applications. |
| `mat_supports_mac` | boolean | ✓ |  |  | Materialized: Derived from mac_requirements JSONB. TRUE if non-null and non-empty object exists. Source of truth: mac_requirements column. Coverage: 99.996% of applications. |
| `mat_supports_linux` | boolean | ✓ |  |  | Materialized: Derived from linux_requirements JSONB. TRUE if non-null and non-empty object exists. Source of truth: linux_requirements column. Coverage: 99.875% of applications. |
| `mat_initial_price` | integer | ✓ |  |  | Materialized: Derived from price_overview->>'initial'. Price in cents (INTEGER). Divide by 100.0 for dollar amount. NULL indicates no pricing data or free game. Source of truth: p… |
| `mat_final_price` | integer | ✓ |  |  | Materialized: Derived from price_overview->>'final'. Discounted price in cents (INTEGER). NULL if no price data or game is free. Source of truth: price_overview JSONB column. |
| `mat_discount_percent` | integer | ✓ |  |  | Materialized: Derived from price_overview->>'discount_percent'. Percentage discount (0-100). NULL indicates no pricing data. 0 indicates no active discount. Source of truth: price… |
| `mat_currency` | text | ✓ |  |  | Materialized: Derived from price_overview->>'currency'. ISO 4217 currency code (e.g., USD, EUR, GBP). NULL if no pricing data. Heavy USD bias (59.5%) due to API query origin. Sour… |
| `mat_achievement_count` | integer | ✓ |  |  | Materialized: Derived from achievements->>'total'. Total number of achievements available for this application. NULL if no achievements. Valid range includes edge cases with 5,000… |
| `mat_pc_os_min` | text | ✓ |  |  | Materialized: Parsed OS from pc_requirements->>'minimum'. Source of truth: pc_requirements JSONB. |
| `mat_pc_processor_min` | text | ✓ |  |  | Materialized: Parsed Processor from pc_requirements->>'minimum'. Source of truth: pc_requirements JSONB. |
| `mat_pc_memory_min` | text | ✓ |  |  | Materialized: Parsed Memory from pc_requirements->>'minimum'. Source of truth: pc_requirements JSONB. |
| `mat_pc_graphics_min` | text | ✓ |  |  | Materialized: Parsed Graphics from pc_requirements->>'minimum'. Source of truth: pc_requirements JSONB. |
| `mat_pc_os_rec` | text | ✓ |  |  | Materialized: Parsed OS from pc_requirements->>'recommended'. Source of truth: pc_requirements JSONB. |
| `mat_pc_processor_rec` | text | ✓ |  |  | Materialized: Parsed Processor from pc_requirements->>'recommended'. Source of truth: pc_requirements JSONB. |
| `mat_pc_memory_rec` | text | ✓ |  |  | Materialized: Parsed Memory from pc_requirements->>'recommended'. Source of truth: pc_requirements JSONB. |
| `mat_pc_graphics_rec` | text | ✓ |  |  | Materialized: Parsed Graphics from pc_requirements->>'recommended'. Source of truth: pc_requirements JSONB. |

---

### `categories`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `id` | integer | ✗ | ✓ |  |  |
| `name` | text | ✗ |  |  |  |

---

### `developers`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `id` | integer | ✗ | ✓ |  |  |
| `name` | text | ✗ |  |  |  |

---

### `embedding_runs`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `run_id` | bigint | ✗ | ✓ |  |  |
| `model_name` | text | ✗ |  |  |  |
| `dimension` | integer | ✗ |  |  |  |
| `normalized` | boolean | ✓ |  |  |  |
| `created_at` | timestamp with time zone | ✓ |  |  |  |
| `notes` | text | ✓ |  |  |  |

---

### `genres`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `id` | integer | ✗ | ✓ |  |  |
| `name` | text | ✗ |  |  |  |

---

### `platforms`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `id` | integer | ✗ | ✓ |  |  |
| `name` | platform_type | ✗ |  |  |  |

---

### `publishers`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `id` | integer | ✗ | ✓ |  |  |
| `name` | text | ✗ |  |  |  |

---

### `reviews`

| Column | Type | Nullable | PK | FK | Description |
|--------|------|----------|----|----|-------------|
| `recommendationid` | text | ✗ | ✓ |  |  |
| `appid` | bigint | ✗ |  | ✓ |  |
| `author_steamid` | text | ✓ |  |  |  |
| `author_num_games_owned` | bigint | ✓ |  |  |  |
| `author_num_reviews` | bigint | ✓ |  |  |  |
| `author_playtime_forever` | bigint | ✓ |  |  |  |
| `author_playtime_last_two_weeks` | bigint | ✓ |  |  |  |
| `author_playtime_at_review` | bigint | ✓ |  |  |  |
| `author_last_played` | bigint | ✓ |  |  |  |
| `language` | text | ✓ |  |  |  |
| `review_text` | text | ✓ |  |  |  |
| `timestamp_created` | bigint | ✓ |  |  |  |
| `timestamp_updated` | bigint | ✓ |  |  |  |
| `voted_up` | boolean | ✓ |  |  |  |
| `votes_up` | bigint | ✓ |  |  |  |
| `votes_funny` | bigint | ✓ |  |  |  |
| `weighted_vote_score` | numeric(10,8) | ✓ |  |  |  |
| `comment_count` | bigint | ✓ |  |  |  |
| `steam_purchase` | boolean | ✓ |  |  |  |
| `received_for_free` | boolean | ✓ |  |  |  |
| `written_during_early_access` | boolean | ✓ |  |  |  |
| `created_at` | timestamp with time zone | ✓ |  |  |  |
| `updated_at` | timestamp with time zone | ✓ |  |  |  |
| `embedding_run_id` | bigint | ✓ |  | ✓ |  |
| `review_embedding` | vector(1024) | ✓ |  |  |  |

---

## Relationships

| From Table | From Column | To Table | To Column | Constraint Name |
|------------|-------------|----------|-----------|-----------------|
| `application_categories` | `appid` | `applications` | `appid` | `application_categories_appid_fkey` |
| `application_categories` | `category_id` | `categories` | `id` | `application_categories_category_id_fkey` |
| `application_developers` | `appid` | `applications` | `appid` | `application_developers_appid_fkey` |
| `application_developers` | `developer_id` | `developers` | `id` | `application_developers_developer_id_fkey` |
| `application_genres` | `appid` | `applications` | `appid` | `application_genres_appid_fkey` |
| `application_genres` | `genre_id` | `genres` | `id` | `application_genres_genre_id_fkey` |
| `application_platforms` | `appid` | `applications` | `appid` | `application_platforms_appid_fkey` |
| `application_platforms` | `platform_id` | `platforms` | `id` | `application_platforms_platform_id_fkey` |
| `application_publishers` | `appid` | `applications` | `appid` | `application_publishers_appid_fkey` |
| `application_publishers` | `publisher_id` | `publishers` | `id` | `application_publishers_publisher_id_fkey` |
| `applications` | `embedding_run_id` | `embedding_runs` | `run_id` | `applications_embedding_run_id_fkey` |
| `reviews` | `appid` | `applications` | `appid` | `reviews_appid_fkey` |
| `reviews` | `embedding_run_id` | `embedding_runs` | `run_id` | `reviews_embedding_run_id_fkey` |

---

## Indexes

### Vector Indexes (HNSW)
*HNSW indexes dominate storage due to their comprehensive graph structure for fast similarity search.*

**reviews.idx_reviews_review_embedding_hnsw** (7930 MB) - `CREATE INDEX idx_reviews_review_embedding_hnsw ON public.reviews USING hnsw (review_embedding vector_cosine_ops)`

**applications.idx_applications_description_embedding_hnsw** (1872 MB) - `CREATE INDEX idx_applications_description_embedding_hnsw ON public.applications USING hnsw (description_embedding vector_cosine_ops)`

### Standard Indexes

**`application_categories`**
- `application_categories_pkey` (34 MB)

**`application_developers`**
- `application_developers_pkey` (7760 kB)

**`application_genres`**
- `application_genres_pkey` (18 MB)

**`application_platforms`**
- `application_platforms_pkey` (14 MB)
- `uq_application_platforms_appid_platform_id` (14 MB)
- `idx_application_platforms_platform_id` (10 MB)

**`application_publishers`**
- `application_publishers_pkey` (6912 kB)

**`applications`**
- `idx_applications_name` (21 MB)
- `applications_pkey` (15 MB)
- `idx_applications_final_price` (10 MB)
- `idx_applications_type` (9720 kB)
- `idx_applications_release_date` (7680 kB)

**`categories`**
- `categories_name_key` (48 kB)
- `categories_pkey` (32 kB)

**`developers`**
- `developers_name_key` (4424 kB)
- `developers_pkey` (2232 kB)

**`embedding_runs`**
- `embedding_runs_pkey` (16 kB)
- `uq_embedding_run` (16 kB)

**`game_features_view`**
- `idx_game_features_appid` (104 kB)

**`genres`**
- `genres_name_key` (16 kB)
- `genres_pkey` (16 kB)

**`platforms`**
- `platforms_name_key` (16 kB)
- `platforms_pkey` (16 kB)

**`publishers`**
- `publishers_name_key` (3976 kB)
- `publishers_pkey` (1896 kB)

**`reviews`**
- `reviews_pkey` (51 MB)
- `idx_reviews_appid` (17 MB)
- `idx_reviews_voted_up` (8432 kB)

---

## JSONB Schema Documentation

### `applications.achievements`

| Key Path | Types | Example Value |
|----------|-------|---------------|
| `highlighted` | list | (list) |
| `highlighted[*].name` | str | Beginner |
| `highlighted[*].path` | str | https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1419770/5f8a3184a31a931bfafd80d65f864fcb291a560b.jpg |
| `total` | int | 9 |

### `applications.content_descriptors`

| Key Path | Types | Example Value |
|----------|-------|---------------|
| `ids` | list | (list) |
| `notes` | NoneType, str | The game is in a horror setting. It has cyber zombies and demons in it. In some cases, the depicted figures look like humans, and the degree of clothing Vareys up to nudity in a n… |

### `applications.linux_requirements`

| Key Path | Types | Example Value |
|----------|-------|---------------|
| `minimum` | str | <strong>Minimum:</strong><br><ul class="bb_ul"></ul> |
| `recommended` | str | <strong>Recommended:</strong><br><ul class="bb_ul"></ul> |

### `applications.mac_requirements`

| Key Path | Types | Example Value |
|----------|-------|---------------|
| `minimum` | str | <strong>Minimum:</strong><br><ul class="bb_ul"></ul> |
| `recommended` | str | <strong>Recommended:</strong><br><ul class="bb_ul"></ul> |

### `applications.movies`

| Key Path | Types | Example Value |
|----------|-------|---------------|
| `[*].highlight` | bool | True |
| `[*].id` | int | 256852391 |
| `[*].mp4` | dict | (dict) |
| `[*].mp4.480` | str | http://video.akamai.steamstatic.com/store_trailers/256852391/movie480.mp4?t=1632181750 |
| `[*].mp4.max` | str | http://video.akamai.steamstatic.com/store_trailers/256852391/movie_max.mp4?t=1632181750 |
| `[*].name` | str | Main Trailer |
| `[*].thumbnail` | str | https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/256852391/movie.293x165.jpg?t=1632181750 |
| `[*].webm` | dict | (dict) |
| `[*].webm.480` | str | http://video.akamai.steamstatic.com/store_trailers/256852391/movie480_vp9.webm?t=1632181750 |
| `[*].webm.max` | str | http://video.akamai.steamstatic.com/store_trailers/256852391/movie_max_vp9.webm?t=1632181750 |

### `applications.package_groups`

| Key Path | Types | Example Value |
|----------|-------|---------------|
| `[*].description` | str |  |
| `[*].display_type` | int | 0 |
| `[*].is_recurring_subscription` | str | false |
| `[*].name` | str | default |
| `[*].save_text` | str |  |
| `[*].selection_text` | str | Select a purchase option |
| `[*].subs` | list | (list) |
| `[*].subs[*].can_get_free_license` | str | 0 |
| `[*].subs[*].is_free_license` | bool | False |
| `[*].subs[*].option_description` | str |  |
| `[*].subs[*].option_text` | str | The Legend of Heroes: Kuro no Kiseki Ⅱ -CRIMSON SiN- Advanced Recovery Medicine Set (1) - $1.99 |
| `[*].subs[*].packageid` | int | 807863 |
| `[*].subs[*].percent_savings` | int | 0 |
| `[*].subs[*].percent_savings_text` | str |  |
| `[*].subs[*].price_in_cents_with_discount` | int | 199 |
| `[*].title` | str | Buy The Legend of Heroes: Kuro no Kiseki Ⅱ -CRIMSON SiN- Advanced Recovery Medicine Set (1) |

### `applications.pc_requirements`

| Key Path | Types | Example Value |
|----------|-------|---------------|
| `minimum` | str | <strong>Minimum:</strong><br><ul class="bb_ul"><li>Requires a 64-bit processor and operating system<br></li><li><strong>OS:</strong> Windows 10 64bit<br></li><li><strong>Processor… |
| `recommended` | str | <strong>Recommended:</strong><br><ul class="bb_ul"><li>Requires a 64-bit processor and operating system<br></li><li><strong>OS:</strong> Windows 10 64bit<br></li><li><strong>Proce… |

### `applications.price_overview`

| Key Path | Types | Example Value |
|----------|-------|---------------|
| `currency` | str | USD |
| `discount_percent` | int | 0 |
| `final` | int | 199 |
| `final_formatted` | str | $1.99 |
| `initial` | int | 199 |
| `initial_formatted` | str |  |

### `applications.ratings`

| Key Path | Types | Example Value |
|----------|-------|---------------|
| `agcom` | dict | (dict) |
| `agcom.descriptors` | str | Violenza Linguaggio Scurrile Paura |
| `agcom.rating` | str | 3 |
| `agcom.required_age` | str | 18 |
| `agcom.use_age_gate` | str | true |
| `bbfc` | dict | (dict) |
| `bbfc.rating` | str | U |
| `bbfc.required_age` | str | 16 |
| `bbfc.use_age_gate` | str | true |
| `cero` | dict | (dict) |
| `cero.rating` | str | a |
| `cero.required_age` | str | 16 |
| `cero.use_age_gate` | str | true |
| `crl` | dict | (dict) |
| `crl.rating` | str | 0 |
| `crl.required_age` | str | 16 |
| `crl.use_age_gate` | str | true |
| `csrr` | dict | (dict) |
| `csrr.descriptors` | str | Violence |
| `csrr.rating` | str | G |
| `csrr.required_age` | str | 16 |
| `csrr.use_age_gate` | str | true |
| `dejus` | dict | (dict) |
| `dejus.banned` | str | 0 |
| `dejus.descriptors` | str | Drogas ilícitas Linguagem imprópria Violência |
| `dejus.rating` | str | 16 |
| `dejus.rating_generated` | str | 1 |
| `dejus.required_age` | str | 16 |
| `dejus.use_age_gate` | str | true |
| `esrb` | dict | (dict) |
| `esrb.descriptors` | str | Language Strong Language Mature Humor Cartoon ViolenceAnimated Blood Blood and Gore Violence Use of Drugs |
| `esrb.display_online_music_notice` | str | true |
| `esrb.display_online_notice` | str | true |
| `esrb.interactive_elements` | str | Users Interact In-Game Purchases |
| `esrb.rating` | str | t |
| `esrb.required_age` | str | 17 |
| `esrb.use_age_gate` | str | true |
| `fpb` | dict | (dict) |
| `fpb.rating` | str | A |
| `fpb.required_age` | str | 16 |
| `fpb.use_age_gate` | str | true |
| `kgrb` | dict | (dict) |
| `kgrb.descriptors` | str | Violence |
| `kgrb.rating` | str | all |
| `kgrb.required_age` | str | 16 |
| `kgrb.use_age_gate` | str | true |
| `mda` | dict | (dict) |
| `mda.required_age` | str | 16 |
| `mda.use_age_gate` | str | true |
| `nzoflc` | dict | (dict) |
| `nzoflc.descriptors` | str | Online Interactivity Mild Violence |
| `nzoflc.rating` | str | g |
| `nzoflc.required_age` | str | 16 |
| `nzoflc.use_age_gate` | str | true |
| `oflc` | dict | (dict) |
| `oflc.descriptors` | str | Online Interactivity Mild Violence |
| `oflc.rating` | str | g |
| `oflc.required_age` | str | 16 |
| `oflc.use_age_gate` | str | true |
| `pegi` | dict | (dict) |
| `pegi.descriptors` | str | Violence Fear |
| `pegi.rating` | str | 3 |
| `pegi.required_age` | str | 18 |
| `pegi.use_age_gate` | str | true |
| `steam_germany` | dict | (dict) |
| `steam_germany.banned` | str | 0 |
| `steam_germany.descriptors` | str | Drogen Drastische Gewalt Derbe Sprache |
| `steam_germany.rating` | str | 16 |
| `steam_germany.rating_generated` | str | 1 |
| `steam_germany.required_age` | str | 16 |
| `steam_germany.use_age_gate` | str | 0 |
| `usk` | dict | (dict) |
| `usk.descriptors` | str | Violence |
| `usk.rating` | str | 0 |
| `usk.required_age` | str | 16 |
| `usk.use_age_gate` | str | true |

### `applications.screenshots`

| Key Path | Types | Example Value |
|----------|-------|---------------|
| `[*].id` | int | 0 |
| `[*].path_full` | str | https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1706290/ss_a0ec137f7f9f4b39e8bbf626ba74a3632e9c3985.1920x1080.jpg?t=1628781520 |
| `[*].path_thumbnail` | str | https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1706290/ss_a0ec137f7f9f4b39e8bbf626ba74a3632e9c3985.600x338.jpg?t=1628781520 |
