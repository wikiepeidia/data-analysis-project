# Phase 1: Canonical Dataset & Performance Frame - Context

**Gathered:** 2026-04-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Build one trustworthy multi-country analysis base and one explicitly documented trending-corpus performance frame that every later phase can reuse. This phase locks the dataset grain, duplicate policy, time semantics, text-normalization boundary, and primary performance proxy; it does not add new analyses, dashboards, API enrichment, or causal claims.

</domain>

<decisions>
## Implementation Decisions

### Analysis Grain
- **D-01:** Keep both the raw daily trending-row dataset and a deduplicated video-level table.
- **D-02:** Use the video-level table as the default unit of analysis for downstream comparisons; keep row-level history for temporal checks and validation.
- **D-03:** Anchor each video-level record on the first trending snapshot rather than the latest or peak row.
- **D-04:** Preserve full repeated-trend history in the row-level dataset and carry summary fields such as per-country trend-day count and first/last trend dates into the video-level table.

### Performance Proxy
- **D-05:** Use trend-day count as the primary headline proxy for stronger trending performance.
- **D-06:** Keep views, likes, dislikes, and comment counts as secondary outcome/context metrics rather than the main success target for recommendations.
- **D-07:** When persistence and size disagree, report the mismatch as a diagnostic instead of forcing a composite ranking.
- **D-08:** Name the primary target explicitly as a proxy within the trending corpus wherever it appears in the dataset and notebook.

### Time Semantics
- **D-09:** Treat `trending_date` as a country-local calendar date only; do not invent hour/minute precision.
- **D-10:** Preserve `publish_time` in raw UTC form and derive helper fields later without overwriting the source timestamp.
- **D-11:** Measure publish-to-trend lag in whole days using publish date versus first local trending date.
- **D-12:** Preserve temporal history per country for multi-country videos rather than collapsing them into one global trend timeline.

### Text Normalization
- **D-13:** Keep raw text fields and add normalized helper columns instead of overwriting source text.
- **D-14:** Convert placeholders such as `[none]` and blank descriptions into consistent missing-value handling plus explicit indicator flags while preserving raw source fields.
- **D-15:** Limit Phase 1 text cleaning to light structural normalization; leave language-specific NLP transformations for later phases.
- **D-16:** Keep the raw tag string and add parsed tag-list/count helper columns, but do not flatten tags into a separate exploded table yet.

### the agent's Discretion
- Exact column names for canonical and helper fields.
- Whether the canonical build is split between notebook cells and helper scripts.
- Schema validation tooling and QA/assertion implementation details.
- Output file naming for cleaned datasets and helper artifacts, as long as raw inputs remain untouched.

</decisions>

<specifics>
## Specific Ideas

No product-style references were requested. The discussion prioritized auditability, explicit caveats, avoiding fake temporal precision, and keeping Phase 1 neutral enough that later NLP work is not pre-committed too early.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Assignment and scope
- `project.md` — Original assignment brief, including the YouTube project requirements and teacher question.
- `.planning/PROJECT.md` — Chosen project scope, all-country coverage, report-first delivery constraint, and core value.
- `.planning/REQUIREMENTS.md` — Phase 1 requirements `DATA-01` to `DATA-03` and global project constraints.

### Phase framing and research guardrails
- `.planning/ROADMAP.md` — Phase 1 goal, success criteria, and sequencing constraints.
- `.planning/research/SUMMARY.md` — Research-backed Phase 1 warnings on duplicate rows, date parsing, proxy validity, and missing duration.
- `.planning/STATE.md` — Current blockers and continuity notes affecting Phase 1 planning.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None yet — there are no existing notebooks, scripts, source modules, or codebase maps to reuse in this repository.

### Established Patterns
- `data/*.csv` contains 10 country files with a consistent 16-column schema across sampled files.
- Raw inputs are already partitioned by country, so source-country metadata must be preserved during ingestion rather than inferred later.
- The repository currently has planning artifacts but no implementation code, so Phase 1 can define the canonical dataset contract without needing to preserve prior code conventions.
- No category-label mapping file was found in `data/`, so Phase 1 should not assume human-readable category labels are already available in-repo.

### Integration Points
- Phase 1 should read from `data/*.csv` and produce the canonical dataset contract that later checkpoint notebooks and final report work will consume.
- Later phases depend on the video-level default unit, trend-day-count proxy, country-aware temporal fields, and raw-plus-normalized text strategy established here.

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 01-canonical-dataset-performance-frame*
*Context gathered: 2026-04-19*