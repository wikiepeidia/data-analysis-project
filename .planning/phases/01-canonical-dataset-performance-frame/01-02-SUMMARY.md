---
phase: 01-canonical-dataset-performance-frame
plan: 02
subsystem: performance-frame
tags: [python, pandas, pyarrow, pytest, notebook]
requires: [01-01]
provides:
  - Video-country snapshot parquet builder anchored on the first trending observation
  - Notebook contract test for proxy language, limitations, and rerun instructions
  - Phase 1 notebook deliverable documenting the row-level and video-country dataset contract
affects: [phase-02-feature-layer, phase-03-country-category-analysis, phase-04-text-analysis, phase-05-report]
tech-stack:
  added: []
  patterns: [first-trending anchor rows per country-video pair, explicit trending-corpus proxy naming, notebook JSON contract tests]
key-files:
  created: [src/youtube_trends/performance_frame.py, tests/test_performance_frame.py, tests/test_phase1_notebook_contract.py, notebooks/01_canonical_dataset.ipynb]
  modified: [src/youtube_trends/performance_frame.py, tests/test_performance_frame.py]
key-decisions:
  - "Keep the default analysis table at country + video_id grain and anchor it on the first local trending row."
  - "Name trend_days_in_country_proxy explicitly as a trending-corpus proxy and carry the association-only framing into the notebook."
  - "Enforce notebook methodology and limitation language with a JSON-level contract test instead of manual-only review."
patterns-established:
  - "Snapshot contract: compute first and last trend dates plus first-snapshot metrics from the row-level parquet."
  - "Documentation guardrail: assert required headings and methodological caveats directly from the .ipynb JSON."
  - "Phase 1 rerun path: canonical_dataset builds the row-level parquet, then performance_frame derives the snapshot parquet."
requirements-completed: [DATA-03]
duration: 10 min
completed: 2026-04-19
---

# Phase 1 Plan 02: Performance Frame and Notebook Contract Summary

**Video-country snapshot builder, explicit proxy framing, and machine-checkable notebook documentation**

## Performance

- **Duration:** 10 min
- **Started:** 2026-04-19T14:01:32Z
- **Completed:** 2026-04-19T14:11:21Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Built the default video-country snapshot pipeline in `src/youtube_trends/performance_frame.py`, keyed by `country + video_id` and anchored on the first local trending observation.
- Added pytest coverage for the anchor-row rule, per-country trend-day proxy counting, publish-to-first-trend lag, and multi-country separation.
- Added a Phase 1 notebook deliverable plus a notebook JSON contract test that locks the proxy wording, association-only framing, missing-duration limitation, and rerun instructions.
- Verified the real snapshot build end-to-end, producing `data/processed/video_country_snapshot.parquet` with 207,148 rows across 10 countries and 39 columns.

## Task Commits

Each task was committed atomically:

1. **Task 1 scaffold** - `9a9cd1a` (chore)
2. **Task 1 failing contract tests** - `3e220e3` (test)
3. **Task 1 snapshot builder implementation** - `290d10e` (feat)
4. **Task 2 notebook contract and documentation** - `6d3dd42` (feat)

**Plan metadata:** pending

_Note: Task 1 used a RED-to-GREEN TDD cycle before the real parquet verification run._

## Files Created/Modified
- `src/youtube_trends/performance_frame.py` - Builds the video-country snapshot parquet and exposes a module entrypoint for regeneration.
- `tests/test_performance_frame.py` - Regression coverage for anchor selection, proxy counting, lag calculation, and country separation.
- `tests/test_phase1_notebook_contract.py` - Reads the notebook JSON and asserts the required headings, proxy language, limitations, and rerun commands.
- `notebooks/01_canonical_dataset.ipynb` - Documents the row-level table, snapshot table, performance proxy, limitations, and regeneration path.

## Decisions Made
- Preserved country-specific history as the default analysis grain instead of collapsing a video into one global record.
- Framed `trend_days_in_country_proxy` explicitly as a trending-corpus proxy so later phases inherit the no-causality rule from Phase 1.
- Treated the notebook as a contract artifact by testing its headings and caveat language directly, rather than leaving the methodology text to drift.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Relaxed the integer-day assertion to accept pandas integral scalars**
- **Found during:** Task 1 verification
- **Issue:** pandas materialized `publish_to_first_trend_days` as `np.int64`, so a strict `isinstance(value, int)` assertion rejected a correct integer-day result.
- **Fix:** Updated `tests/test_performance_frame.py` to assert `Integral` rather than the Python `int` concrete type.
- **Files modified:** `tests/test_performance_frame.py`
- **Verification:** `python -m pytest tests/test_performance_frame.py -q` passes with 4 tests.
- **Committed in:** `290d10e`

---

**Total deviations:** 1 auto-fixed bug
**Impact on plan:** The fix tightened the verification to match pandas runtime behavior without changing the dataset contract or proxy semantics.

## Issues Encountered
- Notebook creation briefly produced an empty-on-read artifact during the first verification pass, but the on-disk `.ipynb` content was rewritten and the JSON contract test passed on the rerun. No code changes beyond the final notebook file were required.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 1 is complete: the repo now has a canonical row-level parquet, a default video-country snapshot parquet, and a notebook that documents the dataset contract and proxy framing.
- Phase 2 can consume `data/processed/trending_rows.parquet` and `data/processed/video_country_snapshot.parquet` instead of re-reading the raw CSV corpus.
- The notebook and its contract test establish the language baseline future phases should preserve when discussing proxy validity, association limits, and missing video duration.

---
*Phase: 01-canonical-dataset-performance-frame*
*Completed: 2026-04-19*
