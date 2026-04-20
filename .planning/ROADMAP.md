# Roadmap: YouTube Trending Content Analysis

## Overview

This roadmap turns the assignment into a reproducible analysis workflow with Markdown checkpoints: first establish a trustworthy multi-country dataset and defensible performance proxy, then engineer reusable features, analyze cross-country and category patterns, layer in multilingual text signals, and finish with an evidence-backed Vietnamese PDF deliverable for the teacher.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Canonical Dataset & Performance Frame** - Build one clean multi-country analysis base and define a defensible trending-performance proxy.
- [x] **Phase 2: Feature Layer for Timing, Metadata, and Engagement** - Engineer the reusable variables needed for creator-input and outcome analysis.
- [x] **Phase 3: Cross-Country Performance & Category Analysis** - Compare timing, metadata, engagement, and categories with country-aware interpretation.
- [x] **Phase 4: Multilingual Text Tone Analysis** - Add sentiment or tone findings with explicit multilingual handling limits.
- [x] **Phase 5: Vietnamese Final Report PDF & Recommendation Playbook** - Deliver the final Vietnamese PDF report, limitations, export workflow, and channel advice.

## Phase Details

### Phase 1: Canonical Dataset & Performance Frame

**Goal**: The project has one trustworthy multi-country dataset and a clearly documented performance target that every later analysis section uses consistently.
**Depends on**: Nothing (first phase)
**Requirements**: DATA-01, DATA-02, DATA-03
**Success Criteria** (what must be TRUE):

  1. The project can load a single harmonized table that covers every country CSV and preserves source-country metadata.
  2. Dates, text fields, booleans, missing values, and repeated trending observations are standardized so later sections reuse the same clean definitions.
  3. The report states a clear trending-performance proxy and explains why it is valid for a trending-only dataset.
  4. The cleaned analysis table can be regenerated end-to-end without manual spreadsheet edits.
**Plans**: 2 plans
Plans:

- [x] 01-01-PLAN.md — Build the row-level canonical dataset pipeline and validation harness.
- [x] 01-02-PLAN.md — Build the video-country snapshot table and Markdown checkpoint performance frame.

### Phase 2: Feature Layer for Timing, Metadata, and Engagement

**Goal**: The analysis workspace exposes stable timing, text-metadata, and engagement features that can support consistent cross-video analysis.
**Depends on**: Phase 1
**Requirements**: FACT-01, FACT-02, FACT-03
**Success Criteria** (what must be TRUE):

  1. Publish-time and trend-lag features are available for every supported analysis row or video unit.
  2. Title, description, and tag-derived metadata fields are engineered with documented definitions that can be inspected in Markdown checkpoints or the report source.
  3. Engagement counts are transformed into comparable metrics or ratios suitable for cross-video comparison.
  4. Downstream analysis sections can reuse one stable feature set instead of recalculating ad hoc columns.
**Plans**: 2 plans
Plans:

- [x] 02-01-PLAN.md — Build the reusable timing and metadata feature table on top of the Phase 1 snapshot parquet.
- [x] 02-02-PLAN.md — Add comparable engagement context metrics and the Markdown checkpoint contract for the feature layer.

### Phase 3: Cross-Country Performance & Category Analysis

**Goal**: The analysis shows which timing, metadata, engagement, and category patterns are associated with stronger trending performance without making invalid pooled comparisons.
**Depends on**: Phase 2
**Requirements**: FACT-04, CAT-01, CAT-02
**Success Criteria** (what must be TRUE):

  1. The analysis checkpoints and report draft present interpretable tables or visuals linking timing, metadata, and engagement structure to the chosen trending-performance proxy.
  2. Content categories are compared on performance, engagement, and prevalence rather than on raw popularity alone.
  3. Country-normalized or country-stratified comparisons are shown before any pooled category conclusion is stated.
  4. A reviewer can see where cross-country patterns are consistent and where market-specific differences remain important.
**Plans**: 2 plans
Plans:

- [x] 03-01-PLAN.md — Build the country-normalized comparative-analysis module and reusable Phase 3 summary artifacts.
- [x] 03-02-PLAN.md — Generate the Phase 3 checkpoint/report-draft tables and lock country-aware category guardrails.

### Phase 4: Multilingual Text Tone Analysis

**Goal**: The project adds text-based sentiment or tone evidence in a way that is credible across multilingual data or explicitly bounded when it is not.
**Depends on**: Phase 2
**Requirements**: NLP-01, NLP-02
**Success Criteria** (what must be TRUE):

  1. Tags and descriptions receive a baseline sentiment or tone analysis that can be inspected alongside other findings.
  2. The Markdown checkpoints and final report explicitly state which languages are supported or how multilingual-aware processing is applied before showing cross-country text conclusions.
  3. Any reported cross-country sentiment findings are limited to supported-language handling rather than implied as universally reliable.
**Plans**: 2 plans
Plans:

- [x] 04-01-PLAN.md — Build the reusable multilingual text-tone frame and summary artifacts on top of the Phase 2 feature parquet.
- [x] 04-02-PLAN.md — Generate the Phase 4 checkpoint and lock multilingual-handling guardrails for cross-country text interpretation.

### Phase 5: Vietnamese Final Report PDF & Recommendation Playbook

**Goal**: The assignment is delivered as a reproducible, teacher-ready Vietnamese PDF with evidence-backed recommendations, explicit limitations, and a clean export workflow.
**Depends on**: Phase 3, Phase 4
**Requirements**: REPT-01, REPT-02, REPT-03, REPT-04
**Success Criteria** (what must be TRUE):

  1. The final Vietnamese PDF answers the teacher's required questions using evidence from the completed analysis phases.
  2. A recommendation playbook translates the findings into specific guidance for a new YouTube channel.
  3. The report includes a limitations section covering trending-only bias, correlation limits, multilingual caveats, and missing duration data.
  4. The analysis can be rerun with stable saved outputs and exported to a teacher-ready Vietnamese PDF without depending on a LaTeX-heavy workflow.
**Plans**: 2 plans
Plans:

- [x] 05-01-PLAN.md — Build the reusable Vietnamese report pipeline, recommendation playbook source, and HTML export surface.
- [x] 05-02-PLAN.md — Generate the real report artifacts, export the final PDF, and close Phase 5 state.

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Canonical Dataset & Performance Frame | 2/2 | Complete | 2026-04-19 |
| 2. Feature Layer for Timing, Metadata, and Engagement | 2/2 | Complete | 2026-04-20 |
| 3. Cross-Country Performance & Category Analysis | 2/2 | Complete | 2026-04-20 |
| 4. Multilingual Text Tone Analysis | 2/2 | Complete | 2026-04-20 |
| 5. Vietnamese Final Report PDF & Recommendation Playbook | 2/2 | Complete | 2026-04-20 |
