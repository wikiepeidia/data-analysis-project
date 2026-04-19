# Requirements: YouTube Trending Content Analysis

**Defined:** 2026-04-19
**Core Value:** Produce a defensible, evidence-based analysis that answers the teacher's required questions with clear findings, visuals, and actionable recommendations.

## v1 Requirements

### Data Foundation

- [ ] **DATA-01**: Combine all country CSV files into one harmonized dataset with source-country metadata.
- [ ] **DATA-02**: Clean and standardize dates, text fields, booleans, missing values, and duplicate trending rows into an analysis-ready dataset.
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
| DATA-01 | TBD | Pending |
| DATA-02 | TBD | Pending |
| DATA-03 | TBD | Pending |
| FACT-01 | TBD | Pending |
| FACT-02 | TBD | Pending |
| FACT-03 | TBD | Pending |
| FACT-04 | TBD | Pending |
| CAT-01 | TBD | Pending |
| CAT-02 | TBD | Pending |
| NLP-01 | TBD | Pending |
| NLP-02 | TBD | Pending |
| REPT-01 | TBD | Pending |
| REPT-02 | TBD | Pending |
| REPT-03 | TBD | Pending |
| REPT-04 | TBD | Pending |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 0
- Unmapped: 15 ⚠

---
*Requirements defined: 2026-04-19*
*Last updated: 2026-04-19 after initial definition*