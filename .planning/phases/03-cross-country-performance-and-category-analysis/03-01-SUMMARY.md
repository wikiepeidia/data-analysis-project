---
phase: 03-cross-country-performance-and-category-analysis
plan: 01
subsystem: comparative-analysis
tags: [python, pandas, pyarrow, pytest, markdown]
requires: [02-02]
provides:
  - Country-normalized Phase 3 row-level frame with reusable percentile and bucket fields
  - Long-form grouped summary artifacts across timing, metadata, and category dimensions
  - One command entrypoint for regenerating Phase 3 outputs from the Phase 2 feature parquet
affects: [03-02, phase-04-multilingual-text-tone-analysis, phase-05-final-report]
tech-stack:
  added: []
  patterns: [within-country percentile normalization, long-form summary tables, checkpoint-friendly module entrypoint]
key-files:
  created: [src/youtube_trends/comparative_analysis.py, tests/test_comparative_analysis.py]
  modified: [src/youtube_trends/__init__.py]
key-decisions:
  - "Normalize performance context within each country before pooled interpretation so large markets do not dominate by raw scale alone."
  - "Keep Phase 3 descriptive and grouped rather than jumping straight to opaque modeling."
  - "Persist reusable Phase 3 summary artifacts so later phases consume stable tables instead of ad hoc notebook logic."
patterns-established:
  - "Country-aware comparison contract: compute proxy, log-view, and engagement-rate percentiles within each country first."
  - "Phase 3 artifact contract: write normalized row-level and grouped long-form summary parquets under data/processed/phase3_analysis/."
  - "Module entrypoint contract: python -m youtube_trends.comparative_analysis regenerates the full comparative analysis surface."
requirements-completed: []
duration: local session
completed: 2026-04-20
---

# Phase 3 Plan 01: Comparative Analysis Scaffold Summary

**Country-normalized analysis frame and reusable grouped summary artifacts**

## Performance

- **Duration:** local session
- **Files modified:** 3

## Accomplishments

- Built `src/youtube_trends/comparative_analysis.py` to normalize performance context within each country and derive report-friendly grouping buckets for timing, metadata, and categories.
- Added reusable long-form country summary and cross-country summary outputs so later checkpoints and report drafting can reuse saved Phase 3 artifacts instead of recalculating comparison logic.
- Added pytest coverage for within-country percentiles, grouped family coverage, cross-country spread tracking, and persisted output files.

## Plan metadata

Plan metadata: pending

## Files Created/Modified

- `src/youtube_trends/comparative_analysis.py` - Builds the normalized Phase 3 frame, grouped summary tables, and persisted analysis outputs.
- `tests/test_comparative_analysis.py` - Regression coverage for normalization, grouped summaries, cross-country spread, and output persistence.
- `src/youtube_trends/__init__.py` - Exposes the new comparative-analysis helpers from the package surface.

## Decisions Made

- Kept `trend_days_in_country_proxy` as the primary comparative outcome while views and engagement stay as secondary context metrics.
- Used simple buckets for publish hour, tag count, title length, and description presence so the outputs stay readable in a bachelor-level report.
- Built summary artifacts in long form so timing, metadata, and category patterns can be compared through one consistent table contract.

## Issues Encountered

None - the comparative-analysis scaffold and persistence path passed on the first focused verification run.

## User Setup Required

None - no external services or new environment setup required.

## Next Phase Readiness

- Plan 02 can now render a Markdown checkpoint with real Phase 3 tables from the saved outputs.
- Phase 4 can later reuse the normalized/country-aware outputs rather than re-implementing Phase 3 comparison logic.

---
_Phase: 03-cross-country-performance-and-category-analysis_
_Completed: 2026-04-20_
