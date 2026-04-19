# Phase 1: Canonical Dataset & Performance Frame - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in `01-CONTEXT.md` — this log preserves the alternatives considered.

**Date:** 2026-04-19
**Phase:** 01-Canonical Dataset & Performance Frame
**Areas discussed:** Analysis grain, Performance proxy, Time semantics, Text normalization

---

## Analysis grain

| Option | Description | Selected |
|--------|-------------|----------|
| Keep both tables | Preserve the raw daily trending rows and also create a deduplicated video-level table for downstream analysis. | ✓ |
| Row-level only | Keep every trending-day row as the only canonical dataset. | |
| Video-level only | Collapse each video to one row and drop daily trending history from the canonical base. | |
| You decide | Let the planner choose the exact structure later. | |

**User's choice:** Keep both tables
**Notes:** Use the video-level table as the default analysis unit.

| Option | Description | Selected |
|--------|-------------|----------|
| Video-level default | Use the deduplicated video table for most comparisons, and keep row-level history for time-based checks. | ✓ |
| Row-level default | Use daily trending observations as the main analysis unit. | |
| Case by case | Choose row-level or video-level later depending on the chart or model. | |
| You decide | Let the planner set the default. | |

**User's choice:** Video-level default
**Notes:** Downstream comparisons should center on the deduplicated video view.

| Option | Description | Selected |
|--------|-------------|----------|
| First trending snapshot | Least contaminated by later post-trending growth and easiest to justify as the first observed success state. | ✓ |
| Latest trending snapshot | Use the most recent row seen for each video. | |
| Peak snapshot | Use the row where views are highest among trending appearances. | |
| Custom | I want a different anchor rule. | |

**User's choice:** First trending snapshot
**Notes:** This avoids using later growth as the canonical anchor.

| Option | Description | Selected |
|--------|-------------|----------|
| Full row history plus summary columns | Keep all raw trending-day rows and add summary fields such as trend-day count and first/last trend date to the video table. | ✓ |
| Trend-day count only | Keep only one aggregated count of appearances after deduplication. | |
| Minimal history | Drop most repeated-trend information once the video table is built. | |
| You decide | Let the planner choose the preservation level. | |

**User's choice:** Full row history plus summary columns
**Notes:** Repeated-trending behavior remains available for validation and later analysis.

---

## Performance proxy

| Option | Description | Selected |
|--------|-------------|----------|
| Trend-day count primary | Use number of trending appearances as the main target, with first-snapshot views/engagement as supporting context. | ✓ |
| First-snapshot views primary | Use the first observed trending row's views as the main target. | |
| Composite score primary | Combine persistence and first-snapshot size into one standardized score. | |
| You decide | Let the planner choose the proxy. | |

**User's choice:** Trend-day count primary
**Notes:** This is the headline measure for stronger trending performance.

| Option | Description | Selected |
|--------|-------------|----------|
| Supporting outcomes only | Keep views, likes, comments, and dislikes as secondary outcome/context metrics, not as the main success target for recommendations. | ✓ |
| Dual role | Allow them to act as both performance outcomes and explanatory features later. | |
| Drop them from framing | Use trend-day count alone for the performance frame. | |
| You decide | Let the planner decide how to position them. | |

**User's choice:** Supporting outcomes only
**Notes:** Recommendation framing should not be driven by post-trending outcomes.

| Option | Description | Selected |
|--------|-------------|----------|
| Primary plus diagnostics | Keep one primary proxy, then explicitly discuss view/engagement mismatches as secondary diagnostics. | ✓ |
| Composite ranking | Force mismatches into one combined ranking score. | |
| Separate leaderboards | Report multiple top lists by metric and avoid a single dominant target. | |
| You decide | Let the planner choose the reporting style. | |

**User's choice:** Primary plus diagnostics
**Notes:** The project should not hide disagreements between persistence and size.

| Option | Description | Selected |
|--------|-------------|----------|
| Very explicit | Label it as a trending-corpus performance proxy and document its limits wherever it appears. | ✓ |
| Methodology only | Explain the caveat once in the methods section, but use a shorter name elsewhere. | |
| Short name only | Use a concise metric name and keep the limitation mostly implicit. | |
| You decide | Let the planner choose the naming convention. | |

**User's choice:** Very explicit
**Notes:** Proxy validity and limits should stay visible throughout the notebook.

---

## Time semantics

| Option | Description | Selected |
|--------|-------------|----------|
| Country-local date only | Treat `trending_date` as a local calendar date without inventing an hour/minute timestamp. | ✓ |
| Midnight timestamp | Convert each date into a synthetic midnight timestamp for every row. | |
| Estimated local time | Try to infer a more precise local time by country. | |
| You decide | Let the planner choose the semantics. | |

**User's choice:** Country-local date only
**Notes:** Avoid fake precision in the canonical dataset.

| Option | Description | Selected |
|--------|-------------|----------|
| Keep UTC plus helpers | Preserve the raw UTC timestamp and add derived date/day helpers later where needed. | ✓ |
| Convert to local time now | Rewrite `publish_time` into country-local time during canonical cleaning. | |
| Date parts only | Drop the raw timestamp after extracting dates and hours. | |
| You decide | Let the planner choose the storage form. | |

**User's choice:** Keep UTC plus helpers
**Notes:** Source timestamps stay intact.

| Option | Description | Selected |
|--------|-------------|----------|
| Whole-day lag | Use day-level lag derived from publish date versus first local trending date, not fake hour precision. | ✓ |
| Estimated hour lag | Derive hour-level lag from synthetic timestamps. | |
| Defer lag metric | Document the semantics now but wait until Phase 2 to define the actual lag feature. | |
| You decide | Let the planner choose the lag rule. | |

**User's choice:** Whole-day lag
**Notes:** Lag is intentionally coarse because the source precision is asymmetric.

| Option | Description | Selected |
|--------|-------------|----------|
| Country-specific history | Keep first/last trend dates and row history per country rather than collapsing to one global trend timeline. | ✓ |
| Global timeline | Collapse all markets into one first/last trend history per video. | |
| Primary market only | Pick one country as canonical for each video's temporal history. | |
| You decide | Let the planner choose the preservation rule. | |

**User's choice:** Country-specific history
**Notes:** Cross-market timing should remain interpretable at the country level.

---

## Text normalization

| Option | Description | Selected |
|--------|-------------|----------|
| Raw plus normalized columns | Keep source text untouched and add cleaned helper columns for later analysis. | ✓ |
| Overwrite with cleaned text | Replace raw text fields with normalized versions. | |
| Mostly raw only | Keep raw text and avoid adding cleaned helper columns until later phases. | |
| You decide | Let the planner choose the storage pattern. | |

**User's choice:** Raw plus normalized columns
**Notes:** Phase 1 should preserve auditability while still making later analysis easier.

| Option | Description | Selected |
|--------|-------------|----------|
| Normalize to missing flags | Convert placeholders into consistent missing-value handling and explicit indicator columns while preserving the raw source in raw fields. | ✓ |
| Keep literal strings | Leave `[none]` and blanks untouched in the canonical text columns. | |
| Replace with tokens | Convert placeholders into synthetic tokens such as `NO_TAGS` or `NO_DESCRIPTION`. | |
| You decide | Let the planner choose the placeholder policy. | |

**User's choice:** Normalize to missing flags
**Notes:** Placeholder handling should be consistent and machine-readable.

| Option | Description | Selected |
|--------|-------------|----------|
| Light structural cleaning | Trim, standardize obvious formatting, parse tags safely, and stop before language-specific NLP transformations. | ✓ |
| Heavy NLP-ready cleaning | Do stronger normalization now, including aggressive token cleanup and language-prep steps. | |
| Minimal cleaning only | Keep almost everything raw and postpone most cleanup. | |
| You decide | Let the planner choose the cleaning depth. | |

**User's choice:** Light structural cleaning
**Notes:** Phase 1 should not pre-commit later NLP choices.

| Option | Description | Selected |
|--------|-------------|----------|
| Raw tag string plus parsed helpers | Keep the original tag string and add parsed tag-list/count helpers without fully flattening tags into a separate table yet. | ✓ |
| Raw tag string only | Keep only the original tags field for now. | |
| Flatten tags now | Explode tags into one-tag-per-row structures during Phase 1. | |
| You decide | Let the planner choose the tag representation. | |

**User's choice:** Raw tag string plus parsed helpers
**Notes:** Helper columns are enough for later analysis without exploding the schema too early.

---

## the agent's Discretion

- Exact column names for canonical and helper fields.
- Whether the canonical build is split between notebook cells and helper scripts.
- Schema validation tooling and QA/assertion implementation details.
- Output file naming for cleaned datasets and helper artifacts.

## Deferred Ideas

None.