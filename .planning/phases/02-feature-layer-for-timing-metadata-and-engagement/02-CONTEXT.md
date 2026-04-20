# Phase 2: Feature Layer for Timing, Metadata, and Engagement - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Build one reusable Phase 2 feature table on top of the Phase 1 parquet artifacts so later analysis sections can reuse stable timing, metadata, and engagement fields. This phase engineers creator-input features and clearly labeled outcome-context features, but it does not start cross-country comparisons, category storytelling, sentiment modeling, guessed category labels, or video-duration enrichment.

</domain>

<decisions>
## Implementation Decisions

### Analysis Grain

- **D-01:** Use `data/processed/video_country_snapshot.parquet` as the default Phase 2 feature-engineering base because Phase 1 already locked `country + video_id` as the default analysis grain.
- **D-02:** Preserve Phase 1 proxy and lag fields instead of redefining them in a second way.
- **D-03:** Write a new reusable feature artifact rather than recalculating ad hoc columns inside future checkpoints or report drafts.
- **D-04:** Keep the row-level parquet available for future temporal work, but do not make Phase 2 depend on re-reading raw CSVs.

### Timing Semantics

- **D-05:** Keep publish-time derived features explicitly in UTC because creator-local timezone is unknown.
- **D-06:** Keep publish-to-first-trend lag in whole days using the existing Phase 1 definition.
- **D-07:** Add simple calendar helpers such as hour, weekday, month, quarter, and weekend flags rather than inventing unsupported market-local hour conversions.
- **D-08:** Add observed trend-span helpers from first and last local trending dates for per-country persistence context.

### Metadata Features

- **D-09:** Favor structural, language-light metadata features in Phase 2 so multilingual handling is not faked before Phase 4.
- **D-10:** Use title, description, and tag counts or flags that are inspectable in Markdown checkpoints and easy to explain in a student report.
- **D-11:** Keep missingness explicit for tags and descriptions because placeholder-heavy text is itself informative.
- **D-12:** Do not guess human-readable category labels or invent video-length proxies from text length.

### Engagement Features

- **D-13:** Treat views, likes, dislikes, and comments as first-snapshot outcome context, not pre-publish causal drivers.
- **D-14:** Add comparable ratios with safe zero handling so cross-video comparisons do not rely only on raw counts.
- **D-15:** Add light log-transformed outcome fields for later descriptive modeling support.
- **D-16:** Keep the report language explicit that creator recommendations must emphasize timing and metadata decisions rather than post-trending engagement counts.

### the agent's Discretion

- Exact Phase 2 column names as long as they stay human-readable and stable.
- Whether some structural counts use character length, whitespace-token length, or both.
- The exact split between code module tests and Markdown checkpoint contract tests.
- The file naming of the Phase 2 feature parquet and checkpoint artifact.

</decisions>

<canonical_refs>

## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Assignment and scope

- `project.md` - Original assignment brief, including the YouTube project requirements and teacher question.
- `.planning/PROJECT.md` - Project scope, report-first constraints, and final Vietnamese PDF target.
- `.planning/REQUIREMENTS.md` - Phase 2 requirements `FACT-01` to `FACT-03` and the global out-of-scope rules.

### Upstream data contract

- `.planning/ROADMAP.md` - Phase 2 goal, success criteria, and sequencing constraints.
- `.planning/STATE.md` - Current blockers and the requirement to reuse Phase 1 parquet artifacts.
- `.planning/phases/01-canonical-dataset-performance-frame/01-CONTEXT.md` - Locked Phase 1 semantics for time, proxy naming, text normalization, and grain.
- `.planning/phases/01-canonical-dataset-performance-frame/01-02-SUMMARY.md` - The exact Phase 1 outputs Phase 2 can build on.
- `checkpoints/01_canonical_dataset.md` - Human-readable Phase 1 dataset contract and limitations.

</canonical_refs>

<code_context>

## Existing Code Insights

### Reusable Assets

- `src/youtube_trends/canonical_dataset.py` already provides normalized text helpers, missingness flags, and the row-level parquet writer.
- `src/youtube_trends/performance_frame.py` already provides the video-country snapshot parquet and the explicit proxy fields Phase 2 should preserve.
- `tests/test_canonical_dataset.py` and `tests/test_performance_frame.py` already establish the preferred pattern: small in-memory fixtures plus one write-path test.

### Established Patterns

- Processed analysis tables are written as Parquet under `data/processed/`.
- Markdown checkpoints are used as lightweight, machine-checkable methodology artifacts.
- The codebase favors explicit validation and simple module entrypoints such as `python -m youtube_trends.performance_frame`.

### Integration Points

- Phase 2 should read `data/processed/video_country_snapshot.parquet` and write a reusable feature parquet for later phases.
- Phase 3 will consume Phase 2 timing, metadata, and engagement columns for country-aware comparisons.
- Phase 5 will reuse the Phase 2 checkpoint language when explaining methodology and limitations in the final report.

</code_context>

<specifics>
## Specific Ideas

Keep the feature names straightforward enough that a bachelor-level report can describe them naturally. Favor grounded structural helpers over overengineered text metrics, and keep the final checkpoint readable for low-token review.

</specifics>

<deferred>
## Deferred Ideas

- Human-readable category label mapping belongs in a later, explicitly sourced step.
- Video-duration enrichment remains out of scope unless the user approves a separate enrichment phase.
- Multilingual sentiment or semantic text modeling belongs to Phase 4.

</deferred>

---

*Phase: 02-feature-layer-for-timing-metadata-and-engagement*
*Context gathered: 2026-04-20*
