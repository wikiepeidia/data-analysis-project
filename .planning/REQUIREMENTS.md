# Requirements: YouTube Trending Content Analysis

**Defined:** 2026-04-19
**Core Value:** Produce a defensible, evidence-based analysis that answers the teacher's required questions with clear findings, visuals, and actionable recommendations.

## v1 Requirements

### Data Foundation

- [x] **DATA-01**: Combine all country CSV files into one harmonized dataset with source-country metadata.
- [x] **DATA-02**: Clean and standardize dates, text fields, booleans, missing values, and duplicate trending rows into an analysis-ready dataset.
- [ ] **DATA-03**: Define and document a valid trending-performance proxy for this trending-only dataset.

### Factor Analysis

- [ ] **FACT-01**: Engineer publish-time and trend-lag features for timing analysis.
- [ ] **FACT-02**: Engineer title, description, and tag-based metadata features for analysis.
- [ ] **FACT-03**: Compute engagement metrics and ratios suitable for cross-video comparison.
- [ ] **FACT-04**: Analyze associations between timing, metadata, engagement structure, and trending performance using interpretable methods and visuals.

### Category Analysis

- [ ] **CAT-01**: Compare content categories on performance, engagement, and prevalence.
- [ ] **CAT-02**: Normalize or stratify category comparisons by country before pooled conclusions are made.

### NLP

- [ ] **NLP-01**: Perform baseline sentiment or tone analysis on tags and descriptions.
- [ ] **NLP-02**: Apply multilingual-aware text handling or explicitly document supported-language limits before reporting cross-country sentiment findings.

### Final Delivery

- [ ] **REPT-01**: Produce a recommendation playbook for a new YouTube channel based on the observed analysis.
- [ ] **REPT-02**: Include a limitations section covering trending-only bias, correlation limits, multilingual caveats, and missing duration data.
- [ ] **REPT-03**: Deliver the analysis in a reproducible notebook/report structure with stable saved outputs.
- [ ] **REPT-04**: Export the final report to a presentation-ready HTML or PDF format.

## v2 Requirements

### Data Foundation

- **DATA-04**: Persist canonical cleaned and feature-engineered tables as reusable Parquet caches.

### Factor Analysis

- **FACT-05**: Add interpretable predictive modeling as supporting analysis for the main findings.

### Category Analysis

- **CAT-03**: Build category archetypes or category-storytelling profiles that summarize strategy differences.

### NLP

- **NLP-03**: Add semantic clustering or deeper topic modeling for text metadata.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Frontend dashboard or web app | The assignment is notebook/report-first, and UI work would dilute analysis quality. |
| Live YouTube API enrichment or scraping | Changes scope, reduces reproducibility, and is not required to answer the assignment questions. |
| Causal claims about what makes videos trend | The dataset is observational and trending-only, so causal conclusions would be invalid. |
| Video-length analysis without a duration enrichment phase | Duration is not present in the current dataset schema, so promising it now would be misleading. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 1 | Complete |
| DATA-02 | Phase 1 | Complete |
| DATA-03 | Phase 1 | Pending |
| FACT-01 | Phase 2 | Pending |
| FACT-02 | Phase 2 | Pending |
| FACT-03 | Phase 2 | Pending |
| FACT-04 | Phase 3 | Pending |
| CAT-01 | Phase 3 | Pending |
| CAT-02 | Phase 3 | Pending |
| NLP-01 | Phase 4 | Pending |
| NLP-02 | Phase 4 | Pending |
| REPT-01 | Phase 5 | Pending |
| REPT-02 | Phase 5 | Pending |
| REPT-03 | Phase 5 | Pending |
| REPT-04 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0

---
*Requirements defined: 2026-04-19*
*Last updated: 2026-04-19 after roadmap creation*
