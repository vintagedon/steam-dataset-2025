---
title: "Steam Dataset 2025 — Release 1.0.1 PR review corrections"
description: "Per-finding record of the verified corrections applied to PR #6 (DS-2) — the seven November 13 review corrections and the November 22 sample-outcome correction — their public verification, and the open review questions for the maintainer"
author: "VintageDon (https://github.com/vintagedon/)"
date: "2026-11-13"
version: "1.0.1-docs"
status: "active"
tags:
  - type: reference
  - domain: [release, data-engineering]
  - tech: [python, json]
related_documents:
  - "README.md"
  - "collection-outcomes.json"
  - "known-limitations.md"
  - "schema-provenance.json"
---

# PR review corrections — Steam Dataset 2025 (DS-2)

This document maps each verified review finding on
[PR #6](https://github.com/vintagedon/steam-dataset-2025/pull/6) to the change
that repaired it and the verification a reviewer can repeat from the repository
alone. The corrections were applied on top of reviewed head
`49c2a95a4ddb4ded9af75261698cbe314a18a2c7` by gate commits
`3961d686a9f5b6557420c33278abf271048a925f` (A1.1, claim and navigation set)
and the A1.2 walkthrough-proof commit; the PR head carries the final state.

## Findings and repairs

### T25-01 — music/other subtotal arithmetic

**Finding.** The published music/other subtotal (11,084) did not equal the sum
of the measured non-game/DLC/demo types.

**Change.** `docs/analytics/README.md` now publishes **12,084** records
combined, itemized as music 8,684, episode 2,274, video 699, advertising 212,
mod 126, series 82, hardware 7, with a pointer to the measured distribution.

**Verification.** Summing those seven categories in
`raw_corpus.success_record_type_distribution` of
[collection-outcomes.json](collection-outcomes.json) yields 12,084 (not
derived by subtracting game/DLC/demo from a total). Separately summing every
type in that distribution yields 239,341, equal to
`raw_corpus.metrics.success_records.value`.

### T25-02 — nonexistent repository embedding link

**Finding.** The notebook-data navigation linked
`02-semantic-game-discovery/02_embeddings_vectors.npy` as if it were a tracked
repository file; the file is not in the repository (the same page says it is
package-only).

**Change.** `steam-dataset-2025-v1/notebook-data/README.md` now labels the
`.npy` as release-package-only in the structure diagram, navigation guide and
file-specification section, pointing to `docs/data-access.md` and the
[artifact reference](artifact-reference.json) with the explicit prerequisite to
download and extract a release package first. The beginner example in
`steam-dataset-2025-v1/README.md` carries the same label. No `.npy` file was
added or manufactured.

**Verification.** Every relative link in the touched documents resolves on
disk; the `.npy` is referenced only as a package asset, never as a repository
path.

### T25-03 — walkthrough input path contract

**Finding.** The published walkthrough decompressed
`data/01_raw/steam_2025_5k-dataset-reviews_20250901.json.gz` but then opened
`steam_2025_5k-dataset-reviews_20250901.json` at the working directory, so
executing the snippet verbatim from the repository root raised
`FileNotFoundError`.

**Change.** `docs/release-1.0.1/README.md` states the start directory (the
repository root containing `data/`) and the Python step opens
`data/01_raw/steam_2025_5k-dataset-reviews_20250901.json`. See A1.2 proof
below.

### T25-04 — packaging phase navigation

**Finding.** The milestones table labeled Phase 10 "Dataset Packaging" while
linking `work-logs/10-pc-requirements-materialization/` (PC requirements
work); packaging is phase 11.

**Change.** Root `README.md` Phase 10 is relabeled PC Requirements
Materialization; "Dataset Packaging" now identifies Phase 11
(`work-logs/11-packaging-the-release/`) and Phase 12 (notebook generation) is
listed. No historical phase was renumbered.

**Verification.** Each milestone row's label matches the directory it links.

### T25-05 — schema DDL availability

**Finding.** A "Full PostgreSQL DDL" row linked the filename
`steam-dataset-2025-full-schema.sql` at
[schema-provenance.json](schema-provenance.json), which is a deferral record,
not SQL.

**Change.** `steam-dataset-2025-v1/README.md` now describes the link as the
schema-provenance deferral record — verified `schema.sql` extraction is
deferred, no full DDL is published yet — and names the unblock conditions
recorded there.

**Verification.** No link text or prose in the touched documents promises an
extracted schema; deferred dump-dependent fields remain null with reasons in
schema-provenance.json.

### T25-06 — sample row count, grain and filename

**Finding.** `data/01_raw/README.md` described the reviews sample as
"~36,000+" (a loose lower bound) with `.json` link text pointing at `.json.gz`
targets.

**Change.** The rows now publish measured values at stated grain: the reviews
sample holds **37,778 review records across 3,993 of 8,711 sampled
applications** (2025-09-01 merge, review-record grain; 11,202,479 B
compressed, 53,584,150 B decompressed); the games run covers 8,711 sampled
applications with 7,967 successful appdetails records of which 5,000 are type
`game` (2025-08-31 run; 14,089,513 B compressed, 106,144,477 B decompressed).
Link text names the exact `.json.gz` basenames.

**Verification (cross-gate).** The row's 37,778 equals the review-record count
measured independently by the A1.2 walkthrough execution below, and both link
texts equal their targets' basenames exactly.

### T25-07 — unsupported English-only qualification

**Finding.** `collection-outcomes.json` and
`steam-dataset-2025-v1/README.md` described the 1,048,148 packaged reviews as
"English-language". The retained collector requested `language=all`; that
request does not measure the package's language distribution, and the sample's
measured mix (51.6% English) is a sample-grain fact.

**Change.** The JSON now records the collection request (`language=all`) and
states the packaged corpus's language composition is unverified pending
dump/CSV verification; the v1 README statistic row drops the English-only
qualification; `known-limitations.md` carries the `language=all` fact; the
same claim family found by a targeted search of the release-reference, root,
v1 and data-access documents (five occurrences in
`steam-dataset-2025-v1/DATASET_CARD.md`) is qualified the same way. The
independently measured sample-language counts and historical source records
were preserved, not blanket-replaced.

**Verification.** The targeted search over
`docs/release-1.0.1/*`, root `README.md`,
`steam-dataset-2025-v1/{README.md,DATASET_CARD.md,DATA_DICTIONARY.md}` and
`docs/data-access.md` finds no remaining occurrence of the unsupported claim;
the only surviving "English-language" text is the statement that such claims
have been qualified.

## A1.2 walkthrough proof (T25-03)

The walkthrough block was extracted verbatim from the immutable reviewed
commit with
`git show 49c2a95a4ddb4ded9af75261698cbe314a18a2c7:docs/release-1.0.1/README.md`
into a scratch fixture containing a clean repository root with the
hash-verified sample at `data/01_raw/`
(SHA-256 `2be129e154505381c77800ca96ea11f09b8db96ddbd2db935c8421cbb4c35a8c`,
matching the tracked Git LFS pointer and the value pinned in the walkthrough):

- **Historical snippet, clean scratch root:** `gunzip` succeeds, the Python
  step raises
  `FileNotFoundError: 'steam_2025_5k-dataset-reviews_20250901.json'`,
  exit status 1.
- **Amended snippet, same documented layout (fresh root):** exit status 0 with

```text
sampled applications: 8711
applications with >=1 review: 3993
review records: 37778 | non-empty text: 37755
top languages: [('english', 19487), ('schinese', 5209), ('russian', 3756)]
```

Every stated count reconciles: 8,711 sampled applications; 3,993 with reviews;
37,778 review records; 37,755 non-empty; English 19,487; Simplified Chinese
5,209; Russian 3,756. The interpreter was Python 3.14.4. No hand-edited
working-directory workaround was used, and the frozen source and sample bytes
hash-identical before and after the runs (tracked LFS pointers and retained
sample unchanged).

## Sample outcome consistency — F25-01 (2026-11-22, amendment Spec 01b)

**Finding.** The `data/README.md` summary published the sample's collection
outcome at the wrong grain: the sample table described the games file as an
"8,711-record run (5,000 successes)" and the quality table listed
"5,000/8,711" as the record-grain collection outcome. 5,000 is the game-only
subset, not the count of successful fetches, so both cells divided game-only
successes by all sampled applications. The prior repair had fixed
`data/01_raw/README.md` but missed this summary.

**Change.** Both cells in `data/README.md` now publish the measured outcome at
record grain and name the game-only subset as a subset, matching the
`data/01_raw/README.md` phrasing already in place: the sample table reads
"8,711-record run (7,967 successful appdetails records, of which 5,000 are
type `game`)" and the quality table reads "7,967/8,711 (91.4591%) successful
appdetails records in the 5K run; 5,000 of those successes are type `game`".
Gate commit `043f5735eb4f7f01d2b651a45f46e9107ac7ac2b` on the DS-2 branch;
no historical log or original evidence file changed.

**Verification (reproduction from the repository alone).** Download the
tracked games sample, verify it against the pinned digest, and count each
grain separately:

```bash
wget -O steam_2025_5k-dataset-games_20250831.json.gz \
  https://media.githubusercontent.com/media/vintagedon/steam-dataset-2025/main/data/01_raw/steam_2025_5k-dataset-games_20250831.json.gz
sha256sum steam_2025_5k-dataset-games_20250831.json.gz
# 3b46222510ad64b87e8a0c63c92dba8f5788e0b8abdd4a1f3471ca0d7a70f2af
python3 - <<'EOF'
import gzip, json
doc = json.load(gzip.open('steam_2025_5k-dataset-games_20250831.json.gz', 'rt'))
recs = doc['games']
ok = [r for r in recs if r.get('app_details', {}).get('success') is True]
games = [r for r in ok if r['app_details'].get('data', {}).get('type') == 'game']
print(len(recs), len(ok), len(games), f'{len(ok)/len(recs)*100:.4f}%')
EOF
# 8711 7967 5000 91.4591%
```

Any published rate must use the successful-fetch grain (7,967/8,711), never
game-only successes over all applications (5,000/8,711). Checked the other
public sample summaries for the same confusion: the 57.4% in
`docs/analytics/steam-5k-dataset-analysis.md` is the games share of all
8,711 records (5,000 + 1,792 DLC + 1,919 other = 8,711, where "other"
reconciles as 1,175 successful non-game/DLC types plus 744 failed fetches) —
a composition share, not a retrieval rate — and stays; the 5K game-subset
naming elsewhere is legitimate and unchanged. An adversarial validator that
re-derives these counts from the hash-verified sample and checks both cells
fails against reviewed head `ab90945ea2811e85dd727e19f85d23c117e88da4`
(exit 1, citing the old "5,000/8,711" cell) and passes against this repair
(exit 0).

## Deferred lane (unchanged by these corrections)

The dump/schema deferrals recorded by the parent change remain: verified dump
acquisition/decoding was unavailable, so released-population fields in
[collection-outcomes.json](collection-outcomes.json) stay null with reasons,
[schema-provenance.json](schema-provenance.json) records the `schema.sql`
extraction deferral and its unblock conditions, and the 481-row difference
between raw unique successful AppIDs (239,183) and packaged application rows
(239,664) remains unresolved with no asserted cause. Nothing in this repair
reopens Q-03 or claims the difference resolved.

## Review questions

These remain maintainer decisions; neither answer is inferred from the
verifications above.

- **D25-01:** Accept these corrections on PR #6?
- **D25-02:** Accept retaining the existing dump/schema deferrals?
- **D25-03:** Accept the sample-outcome correction (F25-01), aligning
  `data/README.md` with the measured 7,967/8,711 record-grain outcome?
