# Phase 3: Cross-Country Performance & Category Analysis - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the first comparative analysis layer on top of the Phase 2 feature parquet so the project can describe timing, metadata, engagement-context, and category patterns with country-aware interpretation. This phase creates reusable summary artifacts and a Markdown checkpoint/report-draft surface, but it does not start multilingual sentiment modeling, guess category labels, invent duration proxies, or jump straight to final-channel recommendations.

</domain>

<decisions>
## Implementation Decisions

### Analysis Grain and Outcome Framing

- **D-01:** Use `data/processed/video_country_features.parquet` as the default Phase 3 input because it already locks one row per `country + video_id` pair.
- **D-02:** Keep `trend_days_in_country_proxy` as the primary trending-corpus performance outcome for association analysis.
- **D-03:** Keep log views and engagement rate as secondary context signals rather than replacing the primary proxy.
- **D-04:** Write reusable Phase 3 summary artifacts so later checkpoints and the final report can load prepared outputs instead of rebuilding comparisons ad hoc.

### Country-Aware Comparison Rules

- **D-05:** Add within-country normalization before pooled interpretation so large markets do not dominate by raw scale alone.
- **D-06:** Show country-level tables first, then pooled cross-country summaries that explicitly preserve country spread or consistency information.
- **D-07:** Treat high spread across countries as a signal for market-specific behavior, not as noise to hide.
- **D-08:** Keep all language about findings at the level of association inside the trending corpus.

### Timing and Metadata Analysis

- **D-09:** Use grouped descriptive summaries for timing and metadata features rather than black-box modeling in this phase.
- **D-10:** Favor simple, report-friendly buckets such as weekday, UTC hour windows, title-length buckets, tag-count buckets, and description presence.
- **D-11:** Keep timing semantics explicit: UTC for publish-time helpers and country-local date semantics only where already established upstream.
- **D-12:** Do not turn post-trending engagement fields into creator advice; keep them in contextual analysis only.

### Category Analysis

- **D-13:** Compare categories on prevalence, median proxy strength, and engagement context within each country before any pooled category story is stated.
- **D-14:** Keep category identifiers as raw `category_id` values until a verified mapping source exists in-repo.
- **D-15:** Add one cross-country category consistency surface so later reporting can distinguish repeatable patterns from market-specific exceptions.
- **D-16:** Keep missing video duration and unresolved category labels visible in the checkpoint guardrails.

### the agent's Discretion

- Exact bucket edges for hour, tag-count, and title-length groupings.
- Exact artifact filenames under `data/processed/` for the Phase 3 summary outputs.
- Whether Phase 3 presents tables only or tables plus lightweight textual highlight blocks inside the checkpoint.
- The exact split between reusable summary functions and checkpoint-rendering helpers.

</decisions>

<canonical_refs>

## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Assignment and scope

- `project.md` - Original assignment brief and the teacher question about how a new channel can optimize views.
- `.planning/PROJECT.md` - Global report-first scope, Markdown-checkpoint workflow, and final Vietnamese PDF target.
- `.planning/REQUIREMENTS.md` - Phase 3 requirements `FACT-04`, `CAT-01`, and `CAT-02` plus global out-of-scope rules.

### Upstream contracts and guardrails

- `.planning/ROADMAP.md` - Phase 3 goal, success criteria, and dependencies.
- `.planning/STATE.md` - Current phase status and continuity notes.
- `.planning/phases/01-canonical-dataset-performance-frame/01-CONTEXT.md` - Locked time semantics, proxy framing, and causal-language limits.
- `.planning/phases/02-feature-layer-for-timing-metadata-and-engagement/02-CONTEXT.md` - Locked Phase 2 feature semantics and engagement guardrails.
- `.planning/phases/02-feature-layer-for-timing-metadata-and-engagement/02-VERIFICATION.md` - Verified Phase 2 artifact list and rerun command.
- `checkpoints/01_canonical_dataset.md` - Phase 1 dataset contract and limitations.
- `checkpoints/02_feature_layer.md` - Phase 2 feature definitions and interpretation guardrails.

### Research guidance

- `.planning/research/SUMMARY.md` - Standard recommendation for Phase 3: country-normalized comparisons, interpretable visuals/tables, and no causal overclaiming.
- `.planning/research/PITFALLS.md` - High-risk Phase 3 pitfalls around leakage, raw cross-country comparisons, and category-label mistakes.

</canonical_refs>

<code_context>

## Existing Code Insights

### Reusable Assets

- `src/youtube_trends/feature_layer.py` already writes the Phase 2 feature parquet with timing, metadata, proxy, and engagement-context fields.
- `tests/test_feature_layer.py` and `tests/test_phase2_checkpoint_contract.py` show the preferred pattern: small in-memory fixtures plus a checkpoint contract test.
- `checkpoints/02_feature_layer.md` already defines the language Phase 3 must preserve around UTC timing, post-trending context, and missing duration.

### Established Patterns

- Analysis artifacts are persisted as Parquet under `data/processed/`.
- Markdown checkpoints are used as lightweight, machine-checkable methodology and report-draft artifacts.
- The repo prefers importable modules with `python -m` entrypoints instead of notebooks for repeatable work.

### Integration Points

- Phase 3 should read `data/processed/video_country_features.parquet` and write summary artifacts that later phases can load directly.
- Phase 4 should inherit the country-aware comparison framing from Phase 3 before adding multilingual tone analysis.
- Phase 5 will reuse the Phase 3 checkpoint outputs when turning findings into teacher-facing narrative and recommendations.

</code_context>

<specifics>
## Specific Ideas

Keep the output readable for a bachelor-level report: straightforward buckets, obvious metric names, and checkpoint tables that can be lifted into a later Markdown or Quarto report draft without heavy rewriting.

</specifics>

<deferred>
## Deferred Ideas

- Human-readable category labels stay deferred until a verified mapping source is added.
- Multilingual sentiment or metadata-tone analysis remains Phase 4 work.
- Final recommendations for a new channel remain Phase 5 work after the evidence base is complete.

</deferred>

---

*Phase: 03-cross-country-performance-and-category-analysis*
*Context gathered: 2026-04-20*
