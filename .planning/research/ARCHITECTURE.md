# Architecture Patterns

**Domain:** Academic report-first analysis of multi-country YouTube trending data
**Researched:** 2026-04-19
**Project style:** Single-repo, report-first workflow with Markdown checkpoints
**Confidence:** HIGH for workflow structure, MEDIUM for full-corpus multilingual sentiment execution without model validation

## Recommended Architecture

This project should be structured as a report-first analysis workflow centered on one canonical cleaned dataset. The main architectural rule is simple: raw CSV files are read once, standardized once, and every later section works from that canonical table or from clearly derived feature tables. Markdown checkpoints can support exploration notes and QA, but the final teacher submission should come from a cleaner report source. For an academic repo, this gives reproducibility and a defensible audit trail without introducing unnecessary application-style complexity.

The observed repo state makes this separation necessary rather than optional. The `data/` directory contains 10 country CSV files with one shared schema and no category metadata JSON files. The available columns support country comparison, timing analysis, category comparison, engagement analysis, and text analysis through `title`, `tags`, and `description`. They do not include video duration, so any architecture that promises a duration analysis from current repo contents is unsound unless an explicit external enrichment step is added.

The text layer is also genuinely multilingual. Sample rows include English and Korean text, and strict UTF-8 decoding fails on `JPvideos.csv`, `KRvideos.csv`, `MXvideos.csv`, and `RUvideos.csv`. That means raw data intake must include encoding handling and that sentiment analysis cannot assume English-only methods. Because the user wants a stronger NLP component, the architecture should dedicate a separate multilingual NLP branch after cleaning and feature engineering, not treat sentiment as a single late-stage chart.

For a single-repo academic project, keep the physical implementation minimal:

- One primary Markdown or Quarto report source that renders the final Vietnamese PDF.
- One optional helper module only if checkpoint content start repeating loader or cleaning logic.
- Optional cached intermediate outputs only for expensive steps such as NLP inference.

## Recommended Architecture

```text
Raw country CSVs in data/
    -> intake manifest (source_file, country_code, encoding_used, row_count)
    -> raw_union_df
    -> cleaned_df
    -> feature_df
         -> exploratory/category branch
         -> factor-analysis branch
         -> NLP/sentiment branch
    -> integrated findings
    -> final report visuals, recommendations, and Vietnamese PDF narrative
```

### Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|----------------|-------------------|
| Raw Data Intake | Read each country CSV safely, infer country from filename, attach source metadata, log encoding and schema issues | Cleaning & Canonicalization |
| Cleaning & Canonicalization | Parse dates, normalize booleans, standardize missing text, remove impossible rows, deduplicate analysis keys | Feature Engineering, Exploratory Analysis, NLP |
| Feature Engineering | Build timing, engagement, text-length, tag-count, and analysis-ready text fields | Exploratory Analysis, Factor Analysis, NLP |
| Exploratory Analysis | Produce descriptive statistics, category comparisons, country comparisons, and posting-window patterns | Visualization & Storytelling, Recommendations |
| Factor Analysis | Run latent-factor modeling on standardized numeric features and interpret factor loadings | Visualization & Storytelling, Recommendations |
| NLP / Sentiment Pipeline | Build multilingual text representations, sentiment outputs, semantic clusters, and tag/topic signals | Visualization & Storytelling, Recommendations |
| Visualization & Storytelling | Convert branch outputs into a compact set of defensible charts and tables | Recommendations / Output Packaging |
| Recommendations / Output Packaging | Turn evidence into guidance for a new channel and frame limitations clearly | Final report PDF and report source |

## Data Flow

### Stage 1: Raw Data Intake

**What:** Build a row-level union of all country files.

**Inputs:**

- `data/*videos.csv`

**Outputs:**

- `raw_union_df`
- `intake_manifest`

**Required fields added at intake:**

- `country_code` extracted from filename
- `source_file`
- `encoding_used`
- `ingest_status`

**Why first:**
The repo has a shared header layout across files, but not a guaranteed uniform encoding. Intake needs to be the only place where file-level quirks are handled.

### Stage 2: Cleaning & Canonicalization

**What:** Convert the raw union table into one trustworthy analysis table.

**Core cleaning tasks:**

- Parse `publish_time` as UTC datetime.
- Parse `trending_date` from non-standard `yy.dd.mm` format.
- Cast flag columns (`comments_disabled`, `ratings_disabled`, `video_error_or_removed`) to boolean.
- Standardize empty text and placeholder values such as `[none]` in `tags`.
- Normalize line breaks, whitespace, and obvious text noise in `description`.
- Remove or flag rows where key engagement columns are unusable.
- Decide and document the deduplication rule.

**Recommended deduplication key:**

- Keep `video_id + country_code + trending_date` as the row-level observation.

**Outputs:**

- `cleaned_df`

**Why this is central:**
Every later section depends on identical date parsing, identical missing-value rules, and identical text normalization. If those rules drift between checkpoint sections, the whole report becomes hard to defend.

### Stage 3: Feature Engineering

**What:** Build derived variables for the assignment questions.

**Recommended numeric and categorical features:**

- `publish_hour_utc`
- `publish_weekday`
- `publish_month`
- `hours_to_trend` or `days_to_trend`
- `log_views`, `log_likes`, `log_comment_count`
- `like_rate = likes / views`
- `comment_rate = comment_count / views`
- `title_char_len`, `title_word_count`
- `tag_count`
- `description_char_len`, `description_word_count`
- `text_available_flag`
- `engagement_available_flag`

**Recommended text feature objects:**

- `analysis_text = title + cleaned tags + cleaned description`
- `title_tokens`
- `tag_tokens`
- `description_tokens`

**Category handling note:**
The repo currently does not include a category lookup file. For storytelling, add a small explicit category mapping table inside the Markdown checkpoint or in one helper file. Do not rely on implicit category labeling.

**Duration limitation:**
The current schema does not contain video duration. If the assignment asks for length-based findings, the architecture must either:

- mark duration analysis as unsupported by the current dataset, or
- add a separate external enrichment stage using the YouTube API.

For the current single-repo checkpoint-checkpoint scope, the first option is the recommended one.

**Outputs:**

- `feature_df`
- `factor_input_df`
- `nlp_input_df`

### Stage 4: Exploratory Analysis & Category Comparison

**What:** Establish the baseline descriptive story before any latent modeling.

**Questions this stage should answer:**

- Which countries and categories dominate the trending corpus?
- What publish windows appear more often among trending videos?
- Which categories have higher median views, like rates, or comment rates?
- Which title and tag patterns appear frequently in strong-performing categories?

**Outputs:**

- Aggregated tables by country and category
- Time-of-day and day-of-week summaries
- High-level comparative charts

**Why this stage comes before heavy modeling:**
It validates that the cleaned and engineered data behaves sensibly. If the distributions look wrong here, factor analysis and NLP will only amplify the error.

### Stage 5: Factor Analysis Branch

**What:** Use factor analysis to identify latent dimensions behind trending performance.

**Recommended input design:**
Use standardized numeric features, not raw counts alone. A reasonable first pass is:

- `log_views`
- `log_likes`
- `log_comment_count`
- `like_rate`
- `comment_rate`
- `hours_to_trend`
- `title_word_count`
- `tag_count`
- `description_word_count`

**Recommended method:**

- Standardize inputs before fitting.
- Use `FactorAnalysis` from scikit-learn.
- Prefer a small number of interpretable components.
- Use `rotation='varimax'` if interpretability is improved.

**Interpretation goal:**
The point is not dimensionality reduction for its own sake. The point is to label latent dimensions such as:

- engagement intensity
- metadata richness
- fast-trending behavior
- conversational/community response

**Outputs:**

- factor loadings
- factor scores per row or per aggregated unit
- interpretation notes tied back to channel recommendations

### Stage 6: NLP / Sentiment Pipeline

**What:** Build a stronger text-analysis branch that is realistic for a multilingual academic dataset.

**Recommended sub-stages:**

1. **Text normalization**

- Remove URLs where appropriate.
- Normalize tag separators.
- Preserve original script and language; do not force everything into ASCII.
- Build one stable `analysis_text` column.

1. **Language-aware handling**

- Use `country_code` as a weak geographic proxy.
- Optionally add language detection if the implementation remains lightweight.
- Keep a clear flag for rows with too little text to score meaningfully.

1. **Sentiment scoring**

- Preferred: validated multilingual text-classification model.
- Acceptable fallback: sentiment on a clearly scoped subset where language support is known and limitations are stated.
- Not acceptable: running an English-only lexicon model over the full multilingual corpus and presenting it as global sentiment.

1. **Stronger NLP layer**

- Generate multilingual sentence embeddings from `analysis_text`.
- Use embedding space for clustering, semantic similarity, and topic/tag discovery.
- Use this branch to strengthen the report beyond basic sentiment by surfacing cross-country semantic patterns.

**Why this architecture is the right compromise:**
The assignment requires sentiment analysis, but the user also wants stronger NLP. In this dataset, the strongest defensible upgrade is not just “better sentiment.” It is a multilingual text branch that combines sentiment with semantic clustering or topic discovery so the report can say both how content sounds and what content themes dominate trending behavior.

**Recommended outputs:**

- sentiment label and confidence
- sentiment summary by category and country
- semantic cluster/topic label
- top representative tags and title phrases per cluster
- shortlist of tag themes relevant to a new channel

## Suggested Build Order

1. **Build intake manifest and union table.**
Depends on: raw files only.

2. **Build the canonical cleaned table.**
Depends on: intake manifest and raw union table.

3. **Build the feature layer.**
Depends on: cleaned table.

4. **Run baseline EDA and category comparison.**
Depends on: cleaned table and feature layer.

5. **Run factor analysis.**
Depends on: feature layer with numeric variables standardized.

6. **Run the NLP / sentiment branch.**
Depends on: cleaned text fields and feature layer.

7. **Build final visual storytelling.**
Depends on: EDA, factor analysis, and NLP outputs.

8. **Write recommendations and package the final report PDF/source.**
Depends on: all earlier stages.

## Dependency Map

```text
Raw Intake
    -> Cleaning
        -> Feature Engineering
            -> Exploratory / Category Comparison
            -> Factor Analysis
            -> NLP / Sentiment
                -> Visualization / Storytelling
                    -> Recommendations / Final Checkpoint/Report Packaging
```

## Patterns to Follow

### Pattern 1: Canonical Dataset First

**What:** Create one cleaned table and forbid later checkpoint sections from reading raw CSVs again.
**When:** Entire project.
**Example:**

```python
raw_union_df = build_raw_union(data_paths)
cleaned_df = clean_youtube_trending(raw_union_df)
feature_df = build_features(cleaned_df)
```

### Pattern 2: Branch After Feature Engineering

**What:** Let EDA, factor analysis, and NLP operate as separate branches on the same prepared feature layer.
**When:** After cleaning stabilizes.
**Why:** This keeps comparisons aligned and prevents slightly different definitions of the same metric from spreading through the checkpoint/report flow.

### Pattern 3: Cache Only Expensive Work

**What:** Cache NLP outputs or embeddings if reruns become slow, but keep cleaning and feature engineering reproducible and lightweight.
**When:** After the script/checkpoint flow is stable.
**Why:** In a student repo, caching everything adds clutter. Cache the slow branch, not the whole project.

### Pattern 4: Make Limitations Explicit in the Final Narrative

**What:** Surface schema limitations such as missing duration data and incomplete category labels.
**When:** In methods and conclusion sections.
**Why:** Academic analysis is stronger when the limits of inference are clear.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Re-cleaning in Every Section

**What:** Re-reading raw files and applying slightly different cleaning logic in EDA, factor analysis, and NLP cells.
**Why bad:** Results drift and the checkpoint/report flow becomes impossible to audit.
**Instead:** Build one canonical cleaned table first.

### Anti-Pattern 2: English-Only Sentiment on the Whole Corpus

**What:** Running an English lexicon model across Japanese, Korean, Russian, and mixed-language text.
**Why bad:** The scores are not valid for a large part of the corpus.
**Instead:** Use a validated multilingual model or clearly scope sentiment to supported texts.

### Anti-Pattern 3: Factor Analysis on Raw Counts

**What:** Fitting factor analysis directly on views, likes, and comments without scaling or rate features.
**Why bad:** Large count columns dominate the latent factors and reduce interpretability.
**Instead:** Log-transform and standardize, then interpret loadings.

### Anti-Pattern 4: Pretending Category Labels Already Exist

**What:** Building human-readable category charts without an explicit mapping source.
**Why bad:** Quiet label errors undermine the story.
**Instead:** Add a small explicit lookup or keep category IDs with a note.

### Anti-Pattern 5: Claiming Video-Length Insights From This Repo

**What:** Treating duration as an available feature when it is not in the schema.
**Why bad:** The report makes claims the data cannot support.
**Instead:** Mark duration as unavailable or add a separate API enrichment stage.

## Scalability Considerations

| Concern | Current checkpoint scope | If the project grows later |
|---------|------------------------|----------------------------|
| Data volume | About 375,942 rows across 10 CSV files is reasonable for a local script-first workflow | Persist a cleaned Parquet file and load selected columns only |
| Encoding / I/O | Mixed encodings require file-level intake rules | Formalize the intake manifest and fallback logic |
| NLP runtime | Full-corpus transformer inference may be slow on CPU | Deduplicate texts, run inference in one batch job, and cache outputs |
| Reproducibility | The main risk is checkpoint drift between source files | Move loaders and cleaners into pure helper functions |
| Story quality | Too many charts can dilute the report | Keep only visuals that directly support the new-channel recommendation |

## Sources

- Repo observation: `data/` contains 10 country CSV files with one shared header and no category JSON metadata.
- Repo observation: strict UTF-8 decoding fails on `JPvideos.csv`, `KRvideos.csv`, `MXvideos.csv`, and `RUvideos.csv`.
- Repo observation: approximately 375,942 rows across all CSV files, with substantial missing text placeholders (`[none]` tags and blank descriptions).
- Project brief: `.planning/PROJECT.md`
- pandas `read_csv` documentation: <https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html>
- scikit-learn `FactorAnalysis` documentation: <https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.FactorAnalysis.html>
- Sentence Transformers pretrained models documentation: <https://www.sbert.net/docs/sentence_transformer/pretrained_models.html>
- Hugging Face Transformers pipelines documentation: <https://huggingface.co/docs/transformers/en/main_classes/pipelines>
