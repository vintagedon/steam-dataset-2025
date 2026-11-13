---
title: "Steam Dataset 2025 v1.0.0 — Known Limitations"
description: "Measured collection outcomes, sampling boundaries, temporal and language limitations, and deferred schema verification for the published v1.0.0 release"
author: "VintageDon (https://github.com/vintagedon/)"
date: "2026-11-13"
version: "1.0.1-docs"
status: "active"
tags:
  - type: reference
  - domain: [data-quality, release]
  - tech: [postgresql, jsonb, pgvector]
---

# Known Limitations — Steam Dataset 2025 v1.0.0

This page states, at the grain each number was measured, what the published
v1.0.0 release does and does not support. Machine-readable values live in
[collection-outcomes.json](collection-outcomes.json); package facts live in
[artifact-reference.json](artifact-reference.json). Database-grain figures are
dated measurements from a read-only session on 2026-08-03 unless marked
otherwise; re-verification against the released dump is deferred (see
[schema-provenance.json](schema-provenance.json)).

## Collection outcomes (measured 2026-11-13, raw corpus)

The retained raw application corpus is 526 batch files holding 262,791 result
records. Of those, 239,341 records are successes (91.0766% at record grain)
and 23,450 are failures. 239,183 unique AppIDs were successfully collected;
158 success records repeat an already-collected AppID.

These are **record-level** facts:

- The 91.0766% fraction is neither HTTP request success nor unique-app
  catalog coverage. Its denominator is retained result records, not attempts
  reconstructable as HTTP requests.
- All 23,450 failure records omit the requested AppID. No per-application
  failure manifest exists, and HTTP-attempt completeness cannot be measured
  from the retained corpus. Failure-cause breakdowns (delisted, region-locked,
  invalid ID, API error) previously published in repository documentation had
  no retained source and have been removed.
- The earlier published "56% success rate / 134,212 successful retrievals /
  105,452 failures" family described an intermediate collection stage, not
  the retained corpus, and has been removed in favor of the measured values
  above.
- The raw corpus itself is not published.

## Population of the packaged database

The packaging-time schema analysis (tracked at
`work-logs/11-packaging-the-release/schema_analysis_report.md`) records
239,664 application rows, 1,048,148 review rows, 101,226 developers and
85,699 publishers. Raw unique successful AppIDs (239,183) and packaged
application rows (239,664) differ by exactly 481; because verified-dump
decoding was deferred, this difference is **unresolved**. No join between the
raw corpus and the released artifact has been established, and no cause is
asserted for the 481-row difference.

## Review corpus is a bounded sample, not a complete history

Reviews were collected as a bounded per-application sample: up to the 100
most recent reviews per covered application, covering 117,311 applications
(dated 2026-08-03 measurement). The retained collector requested
`language=all`; that request does not measure the packaged corpus's language
composition, which remains unverified pending dump/CSV verification. The
corpus is not a complete historical review archive, and "complete historical
coverage" claims have been removed.
Review records include author account identifiers (`author_steamid`); the
reuse decision for unchanged packages is tracked separately and is not
settled here.

## Temporal range

Release dates are stored as recorded by Steam. Unfiltered values span
1969-12-31 through 9998-12-31, including sentinel and outlier values (204
rows dated after 2025 per the dated measurement). Unqualified "1997-2025"
range claims have been qualified: longitudinal work requires an explicit
date filter and should state it.

## Language and text limitations

- For the packaged release, language composition of the review corpus is
  **unverified** pending dump/CSV verification; "English-language reviews"
  claims have been qualified accordingly.
- The publicly tracked 5K-era sample
  (`data/01_raw/steam_2025_5k-dataset-reviews_20250901.json.gz`) measured
  51.6% English, 13.8% Simplified Chinese and 9.9% Russian review text at its
  grain — see the [walkthrough](README.md#small-text-analysis-walkthrough).
  Sample composition must not be extrapolated to the release.

## Schema documentation and `schema.sql`

No verified `schema.sql` extraction exists at the repository root. The two
historical schema documents (`docs/postgresql-database-schema.md` and
`steam-dataset-2025-v1/DATA_DICTIONARY.md`) describe a database that does not
match the packaged release (they predate it) and are marked superseded in
place. Verified schema extraction is deferred; see
[schema-provenance.json](schema-provenance.json) for the deferral record and
unblock conditions. No restore or bootstrap guarantee is advertised.

## Architecture and index facts

The packaged database's index inventory (packaging-time record) is B-tree
plus two HNSW vector indexes (applications 1,872 MB, reviews 7,930 MB).
There is no RUM and no GIN index on any public table. Lexical or hybrid
search is **not implemented** in v1.0.0; any GIN/RUM DDL seen in older
methodology documents is an illustrative proposal, not the shipped database.

## Versions

The collection database was PostgreSQL 16.14 with pgvector 0.8.0 (measured
2026-08-03). Older documents stating 16.10 or pgvector 0.5.0 are corrected
or superseded. Restoring the power-user dump requires a PostgreSQL 16+
environment with pgvector; the dump's own source versions were not re-read in
this unit.

## Citation classes

Version DOI `10.5281/zenodo.17266923` for version-specific citations;
concept DOI `10.5281/zenodo.17266922` for version-agnostic references and
badges. `10.5281/zenodo.17286923` is an invalid typo that appeared in 22
places and has been corrected. See
[artifact-reference.json](artifact-reference.json).

## Successor dataset

A 2026 successor collection is in progress and not yet published. No public
link is provided until it is accepted and publicly reachable; this
maintenance work does not depend on it.
