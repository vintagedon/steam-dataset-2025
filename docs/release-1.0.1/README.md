---
title: "Steam Dataset 2025 — Release 1.0.1 documentation"
description: "Corrected, evidence-tracked reference for the published v1.0.0 release: measured collection outcomes, official artifact facts, known limitations, and a small reproducible text-analysis walkthrough"
author: "VintageDon (https://github.com/vintagedon/)"
date: "2026-11-13"
version: "1.0.1-docs"
status: "active"
tags:
  - type: reference
  - domain: [release, data-engineering]
  - tech: [postgresql, jsonb, pgvector]
related_documents:
  - "known-limitations.md"
  - "collection-outcomes.json"
  - "artifact-reference.json"
  - "schema-provenance.json"
---

# Release 1.0.1 documentation — Steam Dataset 2025

This directory is the corrected, evidence-tracked reference layer for the
published **v1.0.0** release. It exists because the original v1.0.0
documentation drifted from the actual release; the repository-wide truth
patch in this change corrects DOI classes, Kaggle availability, package
names and sizes, collection outcome semantics and stale schema claims.
Every number here traces to a recorded source: the official Zenodo record
API, the tracked packaging-time schema analysis, a fresh recount of the
retained raw batches, or the publicly tracked 5K sample.

## Contents

| File | Contents |
|------|----------|
| [collection-outcomes.json](collection-outcomes.json) | Measured raw-corpus outcomes (cohort, grain, numerator, denominator, state, limitation per metric), packaged-population corroboration, deferred released-population fields |
| [artifact-reference.json](artifact-reference.json) | Official v1.0.0 packages (names, bytes, provider checksums), DOI classes, access channels, observation date |
| [known-limitations.md](known-limitations.md) | Prose limitations: sampling bounds, temporal outliers, language caveats, index facts, schema deferral, successor status |
| [schema-provenance.json](schema-provenance.json) | Deferral record for root `schema.sql` extraction (no file fabricated; unblock conditions stated) |

## Headline facts (with sources)

- 239,664 application rows and 1,048,148 review rows in the packaged
  database — packaging-time schema analysis, tracked in-repo.
- Raw collection: 262,791 retained result records; 239,341 successes;
  239,183 unique successful AppIDs (measured 2026-11-13).
- Four official packages totalling the exact byte sizes in
  [artifact-reference.json](artifact-reference.json); the previously
  published 2.8 GB / 85 MB / 520 MB package figures were wrong.
- Kaggle mirror is published at
  `https://www.kaggle.com/datasets/crainbramp/steam-dataset-2025-multi-modal-gaming-analytics`.
- Cite version DOI `10.5281/zenodo.17266923`; use concept DOI
  `10.5281/zenodo.17266922` for version-agnostic links and badges.

## Small text-analysis walkthrough

A five-minute, offline walkthrough that runs entirely from the **publicly
tracked 5K sample** — no database, key, model or package download required.
It demonstrates the review-text grain and its language mix, and reproduces
one stated count.

**Input (pinned bytes).** The sample is tracked in Git via LFS pointers; the
real objects hash to:

| File | Bytes | SHA-256 |
|------|-------|---------|
| `data/01_raw/steam_2025_5k-dataset-reviews_20250901.json.gz` | 11,202,479 | `2be129e154505381c77800ca96ea11f09b8db96ddbd2db935c8421cbb4c35a8c` |
| `data/01_raw/steam_2025_5k-dataset-games_20250831.json.gz` | 14,089,513 | `3b46222510ad64b87e8a0c63c92dba8f5788e0b8abdd4a1f3471ca0d7a70f2af` |

**Sample population.** These are the 5K-era collection artifacts
(2025-08-31 run for games, 2025-09-01 merge for reviews): 8,711 sampled
applications, of which the games run reports 5,000 successful detail
fetches. This is **not** the 239,664-application release population, and
nothing below extrapolates to it.

**Reproduce it** (Python 3.9+, stdlib only). Run both commands from the
**repository root** — the checkout directory that contains `data/`. The
decompression writes into `data/01_raw/`, and the Python step reads the
decompressed file from that same location:

```bash
gunzip -k data/01_raw/steam_2025_5k-dataset-reviews_20250901.json.gz
python3 - <<'EOF'
import json, collections
d = json.load(open('data/01_raw/steam_2025_5k-dataset-reviews_20250901.json'))
apps_with_reviews = texts = nonempty = 0
langs = collections.Counter()
for e in d['reviews']:
    revs = (e.get('review_data') or {}).get('reviews') or []
    if revs: apps_with_reviews += 1
    for r in revs:
        texts += 1
        if (r.get('review') or '').strip(): nonempty += 1
        langs[r.get('language')] += 1
print('sampled applications:', len(d['reviews']))
print('applications with >=1 review:', apps_with_reviews)
print('review records:', texts, '| non-empty text:', nonempty)
print('top languages:', langs.most_common(3))
EOF
```

**Stated count to verify (sample grain):** the reviews sample contains
**37,778 review records** across **3,993 of 8,711** sampled applications;
**37,755 (99.94%)** carry non-empty review text. Top languages by record
count: English 19,487 (51.6%), Simplified Chinese 5,209 (13.8%), Russian
3,756 (9.9%).

**Limitations stated at this grain:** per-application review counts in this
sample are bounded by the collector's pagination, not exhaustive; the
language mix above characterizes this sample only — the packaged release's
language composition is unverified pending dump/CSV verification (see
[known-limitations.md](known-limitations.md)); fields absent from this input
(for example embedding vectors) are not advertised by this walkthrough.

## What this directory is not

- It is not a new release. No Zenodo version, DOI, ZIP or metadata change is
  part of this maintenance unit.
- It does not fabricate a `schema.sql`; the extraction deferral and its
  conditions are recorded in [schema-provenance.json](schema-provenance.json).
- It does not answer the unchanged-package reuse question (Q-03); that is a
  separately scoped decision.
