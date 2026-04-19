# Project Research Summary

**Project:** YouTube Trending Content Analysis
**Domain:** Academic notebook/report-based data analysis
**Researched:** 2026-04-19
**Confidence:** HIGH

## Executive Summary

This project is best treated as an academic notebook/report workflow, not a product app. The strongest approach is a local Python analysis pipeline that reads all country CSVs once, creates one canonical cleaned dataset, branches into category/timing analysis and a separate multilingual NLP layer, then ends with recommendations for a hypothetical new channel. The priority is reproducibility, explainability, and report-ready evidence.

The core analytical framing should be "which patterns are associated with stronger performance inside the trending corpus," not "what causes videos to trend." Recommendations for a new channel should focus on creator-controlled inputs such as posting window, title/tag/description quality, and category focus, while engagement counts stay in the outcome layer. The main risks are duplicate videos being counted as independent samples, bad date parsing, English-only NLP on multilingual text, and promising unsupported duration analysis.

## Key Findings

### Recommended Stack

Use a pandas-first Python 3.12 notebook workflow with Parquet caching and static reporting tools.

**Core technologies:**
- `pandas` + `pyarrow` — unify all country CSVs, normalize types, and cache cleaned/feature tables to Parquet
- VS Code notebooks or Jupyter — interactive exploration and the main analysis workflow
- `seaborn` + `matplotlib` — static, report-ready figures for category, timing, and comparison charts
- `statsmodels` + `scikit-learn` — interpretable regression/factor support rather than black-box modeling
- `spaCy` + multilingual `transformers` — metadata tone/sentiment and stronger text analysis across countries
- Quarto — final HTML/PDF report rendering from the notebook workflow

### Expected Features

**Must have (table stakes):**
- Multi-country ingestion with country/source metadata for every CSV
- Canonical cleaning for encodings, `trending_date`, `publish_time`, booleans, missing text, and duplicate handling
- Feature engineering for timing, text length, tag count, engagement ratios, and category/country fields
- Category comparison and timing analysis with interpretable visuals
- Sentiment or metadata-tone analysis on tags/descriptions with explicit multilingual caveats
- Final recommendations for a new channel plus a limitations section

**Should have (differentiators):**
- Unique-video versus row-level robustness checks
- Country-normalized comparisons before pooled conclusions
- Semantic clustering or stronger multilingual NLP if baseline sentiment is weak

**Defer (v2+ / out of scope):**
- Frontend dashboard or web app
- YouTube API enrichment unless duration becomes mandatory and feasible
- Heavy deep-learning/custom models or generic EDA not tied to assignment questions

### Architecture Approach

Build one canonical cleaned table and make every later notebook section consume it instead of re-reading raw CSVs. After feature engineering, branch into aligned analysis tracks so category comparisons, timing patterns, and NLP all use the same definitions.

**Major components:**
1. Intake and manifest — read all files safely, add country/source/encoding metadata
2. Canonical cleaning and features — parse dates, normalize text/flags, handle duplicates, build derived variables
3. Analysis branches — category/timing comparisons, interpretable factor support, multilingual text analysis
4. Storytelling and output — integrate findings into recommendations, limitations, and the final notebook/report

### Critical Pitfalls

1. **Repeated trending rows treated as different videos** — keep both row-level and deduplicated video-level views
2. **Misparsed `trending_date` or naive mixing with UTC `publish_time`** — validate lag fields before any timing conclusions
3. **Causal claims from a trending-only dataset** — frame findings as associations within trending videos
4. **Using views/likes/comments as actionable inputs for a new channel** — keep them as outcomes, not recommendation drivers
5. **English-only sentiment over the whole corpus** — use multilingual tooling or explicitly narrow scope
6. **Promising video-length analysis without duration data** — treat duration as a limitation unless an enrichment phase is approved

## Implications for Roadmap

### Phase 1: Scope Lock and Feasibility
**Rationale:** Avoid invalid claims before implementation starts.
**Delivers:** Final question framing, unit of analysis, category-label plan, duration decision, NLP scope.
**Addresses:** Assignment-fit analysis, limitations, recommendation guardrails.
**Avoids:** Causal overclaiming and missing-duration scope failure.

### Phase 2: Canonical Data Foundation
**Rationale:** Every later section depends on identical parsing and cleaning.
**Delivers:** Intake manifest, unified cleaned dataset, deduplicated analysis table, feature table, Parquet caches.
**Uses:** `pandas`, `pyarrow`, `pandera`.
**Avoids:** Duplicate bias, date bugs, placeholder-text pollution, guessed category labels.

### Phase 3: Core Comparative Analysis
**Rationale:** Answer the required assignment questions before optional upgrades.
**Delivers:** Timing analysis, category comparisons, country-normalized summaries, interpretable visuals, preliminary recommendation signals.
**Uses:** `seaborn`, `matplotlib`, `statsmodels`.
**Implements:** Descriptive and factor-analysis branches.
**Avoids:** Leakage from post-trending metrics and raw cross-country comparisons.

### Phase 4: NLP, Recommendations, and Final Report
**Rationale:** Sentiment must support the final channel advice, not sit as a disconnected appendix.
**Delivers:** Metadata-tone or multilingual sentiment results, optional semantic grouping, recommendation table for a new channel, final notebook/report narrative.
**Uses:** `spaCy`, multilingual `transformers`, Quarto.
**Avoids:** English-only NLP, weak storytelling, and advice overfit to big-channel behavior.

### Phase Ordering Rationale

- Cleaning and unit-of-analysis decisions are prerequisites for every credible chart and model.
- Category and timing analysis should precede advanced NLP because they directly answer the assignment and validate the dataset.
- NLP belongs after stable text cleaning but before final recommendations so it can influence the advice section.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 1:** Confirm category label source and whether duration remains a documented limitation
- **Phase 4:** Choose and validate a multilingual sentiment model or fallback metadata-tone method

Phases with standard patterns (skip research-phase):
- **Phase 2:** Standard pandas/Parquet notebook workflow
- **Phase 3:** Standard grouped analysis and interpretable modeling patterns

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Strong fit for dataset size, academic workflow, and deliverable |
| Features | HIGH | Closely aligned with assignment requirements and repo scope |
| Architecture | HIGH | Canonical-dataset-first workflow is appropriate for notebook analysis |
| Pitfalls | HIGH | Driven by observed dataset structure and assignment mismatch risks |

**Overall confidence:** HIGH

### Gaps to Address

- Video duration is not present in the current CSV schema; treat it as a limitation or add a deliberate enrichment phase
- Category labels need a verified mapping source before human-readable category charts
- Multilingual sentiment quality should be validated on a small manual sample before full-corpus claims

## Sources

### Primary
- `.planning/research/STACK.md`
- `.planning/research/FEATURES.md`
- `.planning/research/ARCHITECTURE.md`
- `.planning/research/PITFALLS.md`

---
*Research completed: 2026-04-19*
*Ready for roadmap: yes*
