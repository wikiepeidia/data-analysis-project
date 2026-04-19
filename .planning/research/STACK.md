# Technology Stack

**Project:** YouTube Trending Content Analysis
**Researched:** 2026-04-19
**Scope:** All country CSV files in `data/`; deliverable is a notebook/report, not a frontend app
**Overall recommendation:** Use a pandas-first local Python workflow with Jupyter or VS Code notebooks for exploration, Quarto for the final report, PyArrow/Parquet for cleaned intermediates, seaborn/matplotlib for core visuals, statsmodels plus scikit-learn for interpretable analysis, and spaCy plus selective Hugging Face inference for the NLP section.
**Confidence:** HIGH for the core stack, MEDIUM for optional NLP upgrades and optional performance extras

This project does not need a big-data stack. The repository holds about 380k rows across 10 CSV files, which is large enough to benefit from careful typing and Parquet caching, but still small enough for a single-machine notebook workflow. The correct tradeoff is clarity and reproducibility, not infrastructure.

The stack should also reflect the assignment's real constraints. This is an academic notebook/report submission, not an analytics product. That means the most important choices are the ones that make the analysis explainable, fast to rerun, easy to visualize, and easy to defend in writing.

## Recommended Stack

| Layer | Recommendation | Use in This Project | Confidence | Why This Fits |
|------|----------------|---------------------|------------|---------------|
| Python runtime | Python 3.12 | Single local runtime for notebooks, scripts, and report rendering | HIGH | Matches the user's preferred local install and is fully adequate for the recommended libraries. |
| Core dataframe library | `pandas` | Read, clean, join, feature-engineer, aggregate, and export analysis tables | HIGH | This dataset size is well within pandas range, and pandas has the strongest notebook, plotting, and stats interoperability for an academic report. |
| Columnar I/O | `pyarrow` | Fast Parquet export/import for cleaned and feature-engineered data | HIGH | The raw CSVs should be read once, normalized, then cached as Parquet so later notebooks run quickly and consistently. |
| Notebook authoring | VS Code notebooks or `JupyterLab` | Interactive exploration, EDA, feature engineering, and model interpretation | HIGH | This project is notebook-first, so interactive iteration matters more than packaging or deployment. |
| Final report rendering | `Quarto` | Render the final analysis as polished HTML and optionally PDF | HIGH | Quarto is the cleanest way to turn a notebook-style workflow into an academic report without rebuilding the project around slides or dashboards. |
| Static visualization | `seaborn` + `matplotlib` | Publication-style charts for the final notebook/report | HIGH | This assignment needs readable static evidence, not a heavy interactive app. Seaborn gives fast statistical plots and matplotlib gives precise control. |
| Interpretable statistics | `statsmodels` | OLS and formula-based models to explain associations with views, engagement, or repeated trending appearances | HIGH | Statsmodels is better than black-box modeling when the report must explain what is associated with stronger performance. |
| ML utilities | `scikit-learn` | Preprocessing, train/test splits, regularized models, feature importance baselines | HIGH | Useful for practical predictive support, but should remain secondary to interpretable analysis. |
| NLP preprocessing | `spaCy` | Tokenization, normalization, lemmatization, phrase cleaning, and light linguistic preprocessing | HIGH | Stronger and more maintainable than ad hoc regex-only NLP, while still practical in notebooks. |
| Transformer inference | `transformers` | Sentiment or text-classification inference on descriptions and possibly titles | MEDIUM | Stronger than lexicon-only sentiment, but should be applied selectively and cached because multilingual text and repeated rows can make this expensive. |
| Semantic text analysis | `sentence-transformers` | Optional clustering or semantic grouping of titles/descriptions across countries | MEDIUM | Good upgrade if you want a stronger NLP section beyond polarity scores, but not necessary for the first complete submission. |
| Data validation | `pandera` | Schema checks after ingestion and before analysis notebooks consume the cleaned dataset | HIGH | Lightweight, notebook-friendly, and appropriate for catching type drift, missing columns, and invalid booleans without enterprise overhead. |
| Reproducibility | `pip-tools` | Lock dependencies from a small source requirements file | HIGH | Good fit for a coursework repo because it is deterministic without introducing a full environment manager into the workspace. |
| Notebook versioning helper | `jupytext` | Optional pairing of notebooks with text representations for cleaner diffs | MEDIUM | Useful if the project grows to several notebooks, but optional for a single-person academic repo. |
| Optional interactive supplement | `plotly` | Limited interactive exploration during development | MEDIUM | Helpful for a few drill-down views in Jupyter, but should not become the core visualization layer for the submission. |
| Optional faster dataframe engine | `polars` | Only for CSV ingestion or one-off performance bottlenecks | MEDIUM | Fast and modern, but not necessary as the primary dataframe abstraction for this project size and report style. |

## Prescriptive Stack by Workstream

### 1. Data Ingestion and Cleaning

Use `pandas` with explicit parsing rules, then persist the cleaned result to Parquet using `pyarrow`.

Project-specific guidance:
- Add a `country` column from the source filename when loading each CSV.
- Parse `publish_time` explicitly as datetime with timezone awareness.
- Parse `trending_date` explicitly rather than relying on automatic inference; this dataset uses a non-standard compact date style.
- Keep `title`, `tags`, and `description` in string dtype rather than mixed `object` columns.
- Normalize booleans such as `comments_disabled`, `ratings_disabled`, and `video_error_or_removed` immediately.
- Save a unified cleaned table to Parquet before any heavy analysis.

Recommended tools here:
- `pandas`
- `pyarrow`
- `pandera`

### 2. Feature Engineering

Do the main feature work in pandas, not in SQL, not in a separate warehouse, and not in a distributed framework.

Minimum useful engineered features for this dataset:
- Publish weekday and publish hour
- Time lag from `publish_time` to first trending observation
- Title length and description length
- Tag count and missing-description flag
- Engagement ratios such as likes per view and comments per view
- Number of trending appearances per `video_id`
- Country and category indicators

Recommended tools here:
- `pandas`
- `pyarrow`
- `pandera`

### 3. Analysis and Modeling

Use `statsmodels` for the primary explanatory layer and `scikit-learn` only as a secondary support layer.

Why this split matters:
- `statsmodels` gives coefficients, confidence intervals, and formula-driven outputs that are easy to explain in a report.
- `scikit-learn` is useful for regularization, preprocessing pipelines, and sanity-check predictive baselines.
- For this assignment, interpretability matters more than squeezing out the last bit of predictive accuracy.

Recommended analysis pattern:
- Descriptive summaries and grouped comparisons first
- Visualization second
- Regression or simple predictive support third
- Recommendations last, tied back to the earlier evidence

Recommended tools here:
- `statsmodels`
- `scikit-learn`
- `seaborn`
- `matplotlib`

### 4. NLP and Sentiment Analysis

Use a layered NLP stack, not a one-library shortcut.

Primary recommendation:
- Use `spaCy` for cleaning and normalization.
- Use Hugging Face `transformers` for the actual sentiment or text-classification step if you want the NLP section to be stronger than a classroom baseline.
- Cache NLP outputs by `video_id` to Parquet so repeated trending rows do not trigger repeated inference.

Project-specific guidance:
- Run sentiment primarily on `description`, with `title` as a secondary short-text signal.
- Treat `tags` primarily as topic/keyword features, not as the main sentiment source. Tags are often keyword bundles rather than natural sentences.
- Deduplicate by unique video text before transformer inference. The same `title` and `description` can appear across many trending dates.
- If you add semantic grouping, use `sentence-transformers` to cluster recurring content themes or title/description neighborhoods.

Practical recommendation for this assignment:
- First complete a defensible baseline using `spaCy` plus transformer inference on unique descriptions.
- Only add `sentence-transformers` if the core report is already complete and you want a stronger differentiator.

Recommended tools here:
- `spaCy`
- `transformers`
- `sentence-transformers` as an optional upgrade

## Notebook and Report Tooling

Use this workflow:
1. Author exploratory and cleaning work in VS Code notebooks or JupyterLab.
2. Save cleaned and feature-engineered datasets to Parquet.
3. Write the final narrative report in Quarto, either from a `.qmd` file or by rendering a polished notebook.
4. Export HTML first, then PDF only if the course specifically needs PDF.

Why this is the right workflow:
- HTML is easier to iterate on and preserves figures cleanly.
- Quarto can render both HTML and PDF from the same source.
- PDF output is useful for submission, but on Windows it adds TeX tooling overhead that should stay at the very end of the project.

Optional but useful:
- Use `jupytext` if you want notebooks paired with `.py` or Markdown text for version control.
- Use Quarto report options such as table of contents and numbered sections for an academic structure.

## Visualization Stack

**Primary stack:** `seaborn` + `matplotlib`

Use these as the default because the assignment needs static, interpretable figures such as:
- Category comparison bar charts
- Publish-hour and weekday heatmaps
- Boxplots or violin plots for views and engagement by category/country
- Scatterplots with regression overlays for simple factor relationships
- Small multiples split by country or category

**Supplementary stack:** `plotly` only when an interactive notebook view genuinely helps exploration.

Do not build the final submission around interactive-only visuals. The report should still make sense as a static document.

## Data Quality Tooling

Use `pandera` for schema and assumption checks at two points:
1. Immediately after raw CSV ingestion
2. Right before downstream analysis notebooks consume the cleaned dataset

Recommended checks:
- Required columns present in every country file
- Datetime columns successfully parsed
- Boolean flags normalized to expected values
- Numeric metrics non-negative where appropriate
- Text fields present even if empty or missing
- Country identifier added and never null

This is enough discipline for an academic project. You do not need a platform-heavy data observability product.

## Reproducibility Approach

Use a simple reproducible workflow, not environment sprawl.

Recommended approach:
- Use the local Python 3.12 install already preferred by the user.
- Keep a small dependency source file and compile pinned requirements with `pip-tools`.
- Save cleaned and NLP-enriched datasets as Parquet artifacts so later reruns are fast.
- Keep the raw CSVs untouched.
- Render the final report from a single stable source file after the analysis settles.

Recommended repository outputs:
- Raw input: `data/*.csv`
- Cleaned unified dataset: Parquet
- Feature dataset: Parquet
- NLP cache keyed by `video_id`: Parquet
- Final report: Quarto HTML, plus PDF if needed

## Optional Extras Worth Using Only If Needed

| Optional Tool | Use It When | Why It Is Optional |
|---------------|-------------|--------------------|
| `polars` | CSV reading or one transformation becomes noticeably slow | The dataset is not large enough to require a full switch away from pandas. |
| `plotly` | You need one or two interactive drill-down views while exploring | The final report should not depend on interactivity. |
| `sentence-transformers` | You want a stronger text-theme or semantic-clustering section after the required work is finished | Helpful, but not necessary for a strong first submission. |
| `jupytext` | Notebook diffs are becoming noisy or hard to review | Useful process improvement, not a core analysis dependency. |

## What Not to Use for This Assignment

| Do Not Use | Why It Is a Bad Fit Here | Use Instead |
|------------|---------------------------|-------------|
| `Spark`, `Dask`, or a distributed compute stack | Roughly 380k rows does not justify cluster-style tooling, and it would make the project harder to explain and rerun. | `pandas` + `pyarrow` |
| `Dash`, `Streamlit`, or a frontend dashboard stack | The assignment is notebook/report-first, so app work is scope drift. | Jupyter or VS Code notebooks + Quarto |
| `Great Expectations` or other enterprise-grade data-quality platforms | Too much setup overhead for a single academic repo and little benefit over schema checks. | `pandera` |
| `TextBlob` or `NLTK`-only sentiment as the main NLP method | Too weak and too English-centric for a multi-country dataset if you want a stronger NLP section. | `spaCy` plus selective `transformers` inference |
| Training custom deep learning models from scratch | Unnecessary complexity, longer runtime, and weak return for the assignment questions. | Pretrained transformer inference only where needed |
| Orchestration tools like `Airflow`, `Dagster`, or `Prefect` | This project does not need scheduled pipelines or workflow infrastructure. | A small set of notebooks/scripts and Quarto rendering |
| SQL database setup as the center of the workflow | Adds ceremony without solving a real problem for this project size. | Parquet-backed notebook workflow |
| Live YouTube API enrichment for duration or extra metadata | Changes scope, complicates reproducibility, and is not required by the repo brief. | State missing fields such as video length as limitations unless the scope is explicitly expanded |

## Hard Recommendation on Missing Video Length

The assignment brief mentions video length, but the provided dataset schema does not include it. Do not redesign the stack around external scraping or API enrichment unless the project scope is explicitly changed.

For this repo, the correct approach is:
- Analyze timing, title text, tags, description, category, and engagement with the provided data.
- State that video duration is unavailable in the supplied dataset.
- Treat duration as a limitation or future-work note rather than a reason to add a new data-collection pipeline.

## Recommended Package Set

**Core analysis packages**
- `pandas`
- `pyarrow`
- `seaborn`
- `matplotlib`
- `statsmodels`
- `scikit-learn`
- `pandera`

**Notebook/report packages and tools**
- `jupyterlab` or VS Code notebooks
- `quarto` CLI installed separately
- `jupytext` optional

**NLP packages**
- `spacy`
- `transformers`
- `sentence-transformers` optional

**Dependency management**
- `pip-tools`

## Confidence Summary

| Recommendation Area | Level | Notes |
|---------------------|-------|-------|
| Pandas-first local workflow | HIGH | Strongly supported by dataset size, assignment scope, and notebook/report requirements. |
| PyArrow plus Parquet intermediates | HIGH | High payoff for rerun speed and reproducibility with low complexity. |
| Jupyter or VS Code notebooks plus Quarto reporting | HIGH | Best fit for an academic notebook/report deliverable. |
| Seaborn plus matplotlib as the main viz layer | HIGH | Best match for static, defensible charts in a report. |
| Statsmodels plus scikit-learn split | HIGH | Strong interpretability with optional predictive support. |
| SpaCy plus transformers for NLP | MEDIUM | Stronger and more defensible than lexicon-only sentiment, but model/checkpoint choice still needs practical validation on this dataset. |
| Sentence-transformers semantic upgrade | MEDIUM | Valuable if time remains, but not required before the core assignment is complete. |
| Polars as an optional accelerator | MEDIUM | Good library, but not necessary as the primary analysis stack here. |
| Plotly as a limited supplement | MEDIUM | Helpful in exploration, but should not dominate the final submission. |

## Bottom-Line Recommendation

If this project were being started today, I would build it with:
- Python 3.12
- `pandas` + `pyarrow` for ingestion, cleaning, and cached Parquet datasets
- VS Code notebooks or JupyterLab for iterative analysis
- `seaborn` + `matplotlib` for the final figures
- `statsmodels` + `scikit-learn` for interpretable factor analysis
- `spaCy` + selective `transformers` inference for the NLP section
- `pandera` for schema validation
- `pip-tools` for pinned dependencies
- `Quarto` for the final report output

That stack is the best balance of assignment-fit, analytical rigor, reproducibility, and practical execution speed for this specific repository.

## Sources

- Project scope: `.planning/PROJECT.md`
- Existing research style and scope alignment: `.planning/research/FEATURES.md`
- Repository dataset inventory and schema inspection from `data/` country CSV files
- pandas documentation: CSV I/O and text handling (`read_csv`, string dtype, Parquet support)
- JupyterLab documentation
- Quarto documentation: HTML and PDF output formats
- seaborn documentation
- matplotlib documentation
- scikit-learn documentation
- statsmodels documentation
- spaCy documentation
- Hugging Face Transformers documentation: pipelines and text-classification usage
- Sentence Transformers documentation
- Pandera documentation
- pip-tools documentation
- Plotly documentation for Jupyter FigureWidget usage
