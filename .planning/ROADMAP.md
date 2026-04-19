# Roadmap: YouTube Trending Content Analysis

## Overview

This roadmap turns the assignment into a reproducible notebook-first analysis workflow: first establish a trustworthy multi-country dataset and defensible performance proxy, then engineer reusable features, analyze cross-country and category patterns, layer in multilingual text signals, and finish with an evidence-backed report and exportable final deliverable.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Canonical Dataset & Performance Frame** - Build one clean multi-country analysis base and define a defensible trending-performance proxy.
- [ ] **Phase 2: Feature Layer for Timing, Metadata, and Engagement** - Engineer the reusable variables needed for creator-input and outcome analysis.
- [ ] **Phase 3: Cross-Country Performance & Category Analysis** - Compare timing, metadata, engagement, and categories with country-aware interpretation.
- [ ] **Phase 4: Multilingual Text Tone Analysis** - Add sentiment or tone findings with explicit multilingual handling limits.
- [ ] **Phase 5: Reproducible Report & Recommendation Playbook** - Deliver the final notebook/report, limitations, export, and channel advice.

## Phase Details

### Phase 1: Canonical Dataset & Performance Frame
**Goal**: The project has one trustworthy multi-country dataset and a clearly documented performance target that every later analysis section uses consistently.
**Depends on**: Nothing (first phase)
**Requirements**: DATA-01, DATA-02, DATA-03
**Success Criteria** (what must be TRUE):
  1. The notebook can load a single harmonized table that covers every country CSV and preserves source-country metadata.
  2. Dates, text fields, booleans, missing values, and repeated trending observations are standardized so later sections reuse the same clean definitions.
  3. The report states a clear trending-performance proxy and explains why it is valid for a trending-only dataset.
  4. The cleaned analysis table can be regenerated end-to-end without manual spreadsheet edits.
**Plans**: 2 plans
Plans:
- [ ] 01-01-PLAN.md — Build the row-level canonical dataset pipeline and validation harness.
- [ ] 01-02-PLAN.md — Build the video-country snapshot table and notebook performance frame.

### Phase 2: Feature Layer for Timing, Metadata, and Engagement
**Goal**: The notebook exposes stable timing, text-metadata, and engagement features that can support consistent cross-video analysis.
**Depends on**: Phase 1
**Requirements**: FACT-01, FACT-02, FACT-03
**Success Criteria** (what must be TRUE):
  1. Publish-time and trend-lag features are available for every supported analysis row or video unit.
  2. Title, description, and tag-derived metadata fields are engineered with documented definitions that can be inspected in the notebook.
  3. Engagement counts are transformed into comparable metrics or ratios suitable for cross-video comparison.
  4. Downstream analysis sections can reuse one stable feature set instead of recalculating ad hoc columns.
**Plans**: TBD

### Phase 3: Cross-Country Performance & Category Analysis
**Goal**: The analysis shows which timing, metadata, engagement, and category patterns are associated with stronger trending performance without making invalid pooled comparisons.
**Depends on**: Phase 2
**Requirements**: FACT-04, CAT-01, CAT-02
**Success Criteria** (what must be TRUE):
  1. The notebook presents interpretable tables or visuals linking timing, metadata, and engagement structure to the chosen trending-performance proxy.
  2. Content categories are compared on performance, engagement, and prevalence rather than on raw popularity alone.
  3. Country-normalized or country-stratified comparisons are shown before any pooled category conclusion is stated.
  4. A reviewer can see where cross-country patterns are consistent and where market-specific differences remain important.
**Plans**: TBD

### Phase 4: Multilingual Text Tone Analysis
**Goal**: The project adds text-based sentiment or tone evidence in a way that is credible across multilingual data or explicitly bounded when it is not.
**Depends on**: Phase 2
**Requirements**: NLP-01, NLP-02
**Success Criteria** (what must be TRUE):
  1. Tags and descriptions receive a baseline sentiment or tone analysis that can be inspected alongside other findings.
  2. The notebook explicitly states which languages are supported or how multilingual-aware processing is applied before showing cross-country text conclusions.
  3. Any reported cross-country sentiment findings are limited to supported-language handling rather than implied as universally reliable.
**Plans**: TBD

### Phase 5: Reproducible Report & Recommendation Playbook
**Goal**: The assignment is delivered as a reproducible notebook/report with evidence-backed recommendations, explicit limitations, and a presentation-ready export.
**Depends on**: Phase 3, Phase 4
**Requirements**: REPT-01, REPT-02, REPT-03, REPT-04
**Success Criteria** (what must be TRUE):
  1. The final notebook/report answers the teacher's required questions using evidence from the completed analysis phases.
  2. A recommendation playbook translates the findings into specific guidance for a new YouTube channel.
  3. The report includes a limitations section covering trending-only bias, correlation limits, multilingual caveats, and missing duration data.
  4. The analysis can be rerun with stable saved outputs and exported to presentation-ready HTML or PDF.
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Canonical Dataset & Performance Frame | 0/2 | Planned | - |
| 2. Feature Layer for Timing, Metadata, and Engagement | 0/TBD | Not started | - |
| 3. Cross-Country Performance & Category Analysis | 0/TBD | Not started | - |
| 4. Multilingual Text Tone Analysis | 0/TBD | Not started | - |
| 5. Reproducible Report & Recommendation Playbook | 0/TBD | Not started | - |
