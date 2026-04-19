# Phase 1: Canonical Dataset & Performance Frame - Research

**Completed:** 2026-04-19
**Status:** Ready for planning
**Requirements:** DATA-01, DATA-02, DATA-03

## Objective

Research what the executor needs to know to build a trustworthy Phase 1 dataset foundation without introducing false precision or scope creep. This phase must deliver a reproducible canonical dataset contract and a clearly documented trending-corpus performance proxy that later phases can reuse unchanged.

## Locked Decisions from Context

- Keep both a raw row-level history table and a deduplicated default analysis table.
- Make the default analysis table video-level, anchored on the first trending snapshot.
- Use trend-day count as the primary trending-performance proxy.
- Keep views, likes, dislikes, and comment counts as secondary outcomes, not the primary recommendation target.
- Treat `trending_date` as a country-local date only and keep `publish_time` in UTC.
- Preserve raw text and add normalized helper columns; Phase 1 text cleaning stays structural, not NLP-heavy.

## Research Findings

### Canonical Dataset Contract

The canonical foundation should expose two linked datasets, not one:

1. **Row-level history table**
   - One row per raw CSV record.
   - Preserves the full daily trending history for auditability.
   - Must add a `country` field derived from the filename.
   - Must preserve raw text fields and original numeric metrics.

2. **Video-country snapshot table**
   - One row per `country` + `video_id`, not one row per global `video_id`.
   - The anchor row is the earliest `trending_date` observed for that country/video pair.
   - Stores per-country history summaries such as first/last trend date and trend-day count.

This avoids the main dataset trap in this corpus: the same video can appear on many dates and in many countries. A single global deduplicated row would destroy the market-specific timing and persistence that later phases need.

### Parsing and Normalization Rules

- `trending_date` uses the compact `%y.%d.%m` format and should be parsed into a date column such as `trending_date_local`.
- `publish_time` is already an ISO UTC timestamp and should remain UTC in the canonical layer.
- Lag between publish and first trend should be measured in **whole days**, not estimated hours.
- Boolean flags vary by source casing (`False` and `FALSE` were both observed), so normalization must be case-insensitive.
- Placeholder text such as `[none]` and empty descriptions should become consistent missing-value indicators plus helper flags.
- Tags should remain available as the original raw string and as parsed helpers such as `tags_list` and `tag_count`.

### Performance Proxy Recommendation

The cleanest Phase 1 target is:

- `trend_days_in_country_proxy` — count of trending rows for each `country` + `video_id`

Supporting secondary outcomes:

- `first_trending_views`
- `first_trending_likes`
- `first_trending_dislikes`
- `first_trending_comment_count`
- downstream engagement ratios can be added later, but Phase 1 should keep the raw anchor metrics ready

Why this framing fits the assignment:

- It stays honest about the dataset only containing trending videos.
- It favors persistence inside the trending corpus over post-hoc popularity spikes.
- It makes diagnostic comparisons possible when persistence and first-snapshot size disagree.

### Category and Duration Gaps

- No category-label lookup file was found in the repository. Phase 1 should preserve `category_id` and document that human-readable labels are unresolved, not invent them.
- Video duration is not available in the current CSV schema. Phase 1 should explicitly document this as a limitation and should **not** add API enrichment or scraping.

### Recommended Implementation Shape

The smallest reliable repo structure for this phase is:

- `requirements.txt` — explicit Python dependencies for reproducibility
- `src/youtube_trends/canonical_dataset.py` — ingestion, normalization, and row-level output
- `src/youtube_trends/performance_frame.py` — video-country snapshot and proxy computation
- `tests/test_canonical_dataset.py` — schema and normalization tests
- `tests/test_performance_frame.py` — proxy and anchor-row tests
- `tests/test_phase1_notebook_contract.py` — notebook contract checks
- `notebooks/01_canonical_dataset.ipynb` — notebook deliverable for Phase 1 narrative and regeneration path

This keeps checkpoint notebooks available for Phase 1 validation while still moving the brittle parsing logic into importable Python modules that can be tested.

## Risks to Plan Around

1. **Duplicate-row bias** — if later phases consume raw rows directly, the same video may be overweighted.
2. **Temporal overclaiming** — converting `trending_date` into fake timestamps would make lag analysis look more precise than it is.
3. **Outcome leakage** — using views/likes/comments as the main optimization target would confuse creator inputs with post-trending outcomes.
4. **Premature NLP coupling** — aggressive text normalization now would lock later multilingual text work into assumptions that Phase 4 may reject.
5. **Category-label guessing** — hard-coding unverified labels would create silent semantic drift in later plots.

## Validation Architecture

Use lightweight automated verification from the start.

- **Framework:** `pytest`
- **Quick command:** `python -m pytest tests/test_canonical_dataset.py tests/test_performance_frame.py tests/test_phase1_notebook_contract.py -q`
- **Full command:** `python -m pytest -q`
- **Sampling approach:** run the relevant test file after every task commit, then run the phase quick command after each completed plan

Required test coverage for this phase:

- all 10 country files are discovered and tagged with country metadata
- `%y.%d.%m` dates parse correctly
- boolean normalization is case-insensitive
- placeholder text becomes consistent missing-value handling with helper flags
- first trending snapshot is the anchor row for the video-country table
- `trend_days_in_country_proxy` is explicit and counts row history correctly
- the notebook states the proxy, the no-causality constraint, and the missing-duration limitation

## Planning Implications

- **Plan 01 should build the row-level pipeline and validation harness first.**
- **Plan 02 should build the video-country snapshot table and notebook documentation second.**
- The second plan should depend on the first because it consumes the canonical row-level output and shared normalization rules.

## Sources

- `.planning/phases/01-canonical-dataset-performance-frame/01-CONTEXT.md`
- `.planning/research/SUMMARY.md`
- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md`
- `project.md`
- `data/*.csv` schema and sample rows

---
*Research complete: 2026-04-19*
