# Phase 4: Multilingual Text Tone Analysis - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Build a credible Phase 4 text-analysis layer on top of the saved feature parquet so the project can describe description and tag tone across countries without pretending the multilingual corpus is uniformly readable. This phase adds reusable text-tone artifacts and a Markdown checkpoint surface, but it does not attempt full semantic topic modeling, machine translation, human-readable category remapping, or the final teacher-facing recommendation playbook.

</domain>

<decisions>
## Implementation Decisions

### Analysis Grain and Inputs

- **D-01:** Use `data/processed/video_country_features.parquet` as the Phase 4 source because it already locks one row per `country + video_id` pair and preserves the normalized text fields.
- **D-02:** Reuse the country-normalized comparison contract from Phase 3 so text-tone findings are not pooled across markets on raw scale alone.
- **D-03:** Analyze `description_normalized` and `tags_normalized` separately because descriptions behave like noisy prose while tags behave like short keyword bundles.
- **D-04:** Keep `trend_days_in_country_proxy` as the primary comparative outcome and treat any text signal as association inside the trending corpus.

### Multilingual Handling Strategy

- **D-05:** Do not default to full semantic multilingual sentiment scoring, because the saved corpus contains heavy mojibake in several countries and would make pooled polarity claims look stronger than the text quality supports.
- **D-06:** Use Unicode-aware structural tone features that stay credible across scripts: punctuation, emoji/symbol presence, link-heavy writing, keyword density, script family, and text-quality buckets.
- **D-07:** Add explicit `likely_mojibake` or equivalent text-quality buckets so corrupted text is surfaced as a first-class limitation instead of silently mixed with readable rows.
- **D-08:** Keep supported-language limits explicit in the checkpoint: structural tone is cross-country, but semantic sentiment remains bounded by text quality and is not treated as universal audience emotion.

### Reporting and Interpretation

- **D-09:** Report tone as metadata wording or structural framing, not as viewer sentiment.
- **D-10:** Keep grouped summaries and checkpoint tables readable for a grounded bachelor-level report rather than building a black-box classifier.
- **D-11:** Treat missing descriptions, missing tags, and corrupted text as findings worth reporting, because they affect how much confidence later text conclusions deserve.
- **D-12:** Preserve the existing limitations: no causal claims, no guessed category labels, and no invented video-duration proxy.

### the agent's Discretion

- Exact threshold rules for tone buckets, script-family buckets, and mojibake heuristics.
- Exact artifact names under `data/processed/phase4_analysis/` as long as they stay stable and readable.
- Whether the Phase 4 checkpoint shows separate description/tag tables only or also adds compact coverage notes.
- Whether Phase 4 imports the Phase 3 normalization helper directly or mirrors the same percentile logic locally.

</decisions>

<canonical_refs>

## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Assignment and scope

- `project.md` - Original assignment brief, including the requirement for baseline sentiment analysis through tags or descriptions.
- `.planning/PROJECT.md` - Global report-first scope, Markdown checkpoint workflow, and final Vietnamese PDF target.
- `.planning/REQUIREMENTS.md` - Phase 4 requirements `NLP-01` and `NLP-02` plus global out-of-scope rules.

### Upstream contracts and guardrails

- `.planning/ROADMAP.md` - Phase 4 goal, success criteria, and dependencies.
- `.planning/STATE.md` - Current continuity note that multilingual handling must be decided before tone claims are made.
- `.planning/phases/02-feature-layer-for-timing-metadata-and-engagement/02-CONTEXT.md` - Locked text-field structure, missingness rules, and Phase 2 feature semantics.
- `.planning/phases/03-cross-country-performance-and-category-analysis/03-CONTEXT.md` - Locked Phase 3 country-normalized comparison rules and association-only framing.
- `.planning/phases/03-cross-country-performance-and-category-analysis/03-VERIFICATION.md` - Verified Phase 3 artifact list and rerun command.
- `checkpoints/02_feature_layer.md` - Phase 2 text-feature definitions and missing-duration guardrails.
- `checkpoints/03_cross_country_category_analysis.md` - Phase 3 country-aware interpretation rules that Phase 4 must inherit.

### Research and corpus-quality guidance

- `.planning/research/SUMMARY.md` - Recommends choosing between a multilingual model and a bounded metadata-tone fallback.
- `.planning/research/PITFALLS.md` - High-risk warnings about English-only sentiment, corrupted text, and confusing metadata tone with audience emotion.
- `data/processed/source_manifest.csv` - Shows that `JP`, `KR`, `MX`, and `RU` were decoded through `latin-1`, which matters for text-quality interpretation.

</canonical_refs>

<code_context>

## Existing Code Insights

### Reusable Assets

- `src/youtube_trends/feature_layer.py` already exposes the normalized text fields, missingness flags, tag counts, and description link flag needed for structural tone analysis.
- `src/youtube_trends/comparative_analysis.py` already provides a reusable country-normalized frame builder and long-form summary pattern.
- `tests/test_feature_layer.py`, `tests/test_comparative_analysis.py`, and the Phase 2/3 checkpoint contract tests establish the preferred pattern: small in-memory fixtures plus one checkpoint text contract.

### Established Patterns

- Reusable analysis outputs are persisted as Parquet under `data/processed/`.
- Markdown checkpoints are the methodology artifact and are guarded by direct text-level pytest checks.
- The repo favors importable modules with `python -m` entrypoints instead of notebook-only logic.

### Integration Points

- Phase 4 should read `data/processed/video_country_features.parquet` and write reusable Phase 4 artifacts under a dedicated processed subdirectory.
- Phase 5 will need the Phase 4 checkpoint wording when explaining multilingual limits and text-based findings in the final Vietnamese report.
- Phase 4 should stay compatible with the Phase 3 country-aware framing so text findings can be compared beside the earlier timing/category outputs.

</code_context>

<specifics>
## Specific Ideas

- Real corpus profiling showed very high non-ASCII rates across many markets and very high mojibake-marker rates for `JP`, `KR`, and `RU`, with substantial risk in `MX` as well.
- `transformers`, `torch`, and `sentence_transformers` are installed, but full-corpus semantic sentiment still looks like the wrong default because text corruption is the main credibility bottleneck, not missing libraries.
- Keep the Phase 4 report tone grounded: say structural tone or metadata framing, not grand claims about emotional polarity or audience psychology.

</specifics>

<deferred>
## Deferred Ideas

- Full multilingual transformer sentiment scoring can be revisited only if a later phase explicitly repairs or re-ingests the corrupted text markets.
- Semantic clustering or topic modeling remains optional future work rather than the default Phase 4 baseline.
- Translation-based normalization is deferred because it would add scope, runtime, and new failure modes late in the project.

</deferred>

---

*Phase: 04-multilingual-text-tone-analysis*
*Context gathered: 2026-04-20*
