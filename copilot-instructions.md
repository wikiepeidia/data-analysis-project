<!-- GSD:project-start source:PROJECT.md -->
## Project

**YouTube Trending Content Analysis**

This is a notebook-first data analysis project for an academic assignment built around the Trending YouTube Video Statistics dataset. The project analyzes multi-country trending video data to identify what helps videos trend, compare performance across content categories, and recommend practical actions for a new channel trying to optimize views.

**Core Value:** Produce a defensible, evidence-based analysis that answers the teacher's required questions with clear findings, visuals, and actionable recommendations.

### Constraints

- **Deliverable**: Notebook/report first — the repository should optimize for an academic analysis artifact, not an application.
- **Dataset**: Use all country files in the provided YouTube dataset — cross-market coverage is part of the chosen scope.
- **Assignment**: Must answer the brief's required questions — findings and recommendations are not optional.
- **Method**: Stronger NLP is preferred for sentiment analysis — but it must remain feasible within the dataset's available text and the assignment timeline.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

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
- Add a `country` column from the source filename when loading each CSV.
- Parse `publish_time` explicitly as datetime with timezone awareness.
- Parse `trending_date` explicitly rather than relying on automatic inference; this dataset uses a non-standard compact date style.
- Keep `title`, `tags`, and `description` in string dtype rather than mixed `object` columns.
- Normalize booleans such as `comments_disabled`, `ratings_disabled`, and `video_error_or_removed` immediately.
- Save a unified cleaned table to Parquet before any heavy analysis.
- `pandas`
- `pyarrow`
- `pandera`
### 2. Feature Engineering
- Publish weekday and publish hour
- Time lag from `publish_time` to first trending observation
- Title length and description length
- Tag count and missing-description flag
- Engagement ratios such as likes per view and comments per view
- Number of trending appearances per `video_id`
- Country and category indicators
- `pandas`
- `pyarrow`
- `pandera`
### 3. Analysis and Modeling
- `statsmodels` gives coefficients, confidence intervals, and formula-driven outputs that are easy to explain in a report.
- `scikit-learn` is useful for regularization, preprocessing pipelines, and sanity-check predictive baselines.
- For this assignment, interpretability matters more than squeezing out the last bit of predictive accuracy.
- Descriptive summaries and grouped comparisons first
- Visualization second
- Regression or simple predictive support third
- Recommendations last, tied back to the earlier evidence
- `statsmodels`
- `scikit-learn`
- `seaborn`
- `matplotlib`
### 4. NLP and Sentiment Analysis
- Use `spaCy` for cleaning and normalization.
- Use Hugging Face `transformers` for the actual sentiment or text-classification step if you want the NLP section to be stronger than a classroom baseline.
- Cache NLP outputs by `video_id` to Parquet so repeated trending rows do not trigger repeated inference.
- Run sentiment primarily on `description`, with `title` as a secondary short-text signal.
- Treat `tags` primarily as topic/keyword features, not as the main sentiment source. Tags are often keyword bundles rather than natural sentences.
- Deduplicate by unique video text before transformer inference. The same `title` and `description` can appear across many trending dates.
- If you add semantic grouping, use `sentence-transformers` to cluster recurring content themes or title/description neighborhoods.
- First complete a defensible baseline using `spaCy` plus transformer inference on unique descriptions.
- Only add `sentence-transformers` if the core report is already complete and you want a stronger differentiator.
- `spaCy`
- `transformers`
- `sentence-transformers` as an optional upgrade
## Notebook and Report Tooling
- HTML is easier to iterate on and preserves figures cleanly.
- Quarto can render both HTML and PDF from the same source.
- PDF output is useful for submission, but on Windows it adds TeX tooling overhead that should stay at the very end of the project.
- Use `jupytext` if you want notebooks paired with `.py` or Markdown text for version control.
- Use Quarto report options such as table of contents and numbered sections for an academic structure.
## Visualization Stack
- Category comparison bar charts
- Publish-hour and weekday heatmaps
- Boxplots or violin plots for views and engagement by category/country
- Scatterplots with regression overlays for simple factor relationships
- Small multiples split by country or category
## Data Quality Tooling
- Required columns present in every country file
- Datetime columns successfully parsed
- Boolean flags normalized to expected values
- Numeric metrics non-negative where appropriate
- Text fields present even if empty or missing
- Country identifier added and never null
## Reproducibility Approach
- Use the local Python 3.12 install already preferred by the user.
- Keep a small dependency source file and compile pinned requirements with `pip-tools`.
- Save cleaned and NLP-enriched datasets as Parquet artifacts so later reruns are fast.
- Keep the raw CSVs untouched.
- Render the final report from a single stable source file after the analysis settles.
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
- Analyze timing, title text, tags, description, category, and engagement with the provided data.
- State that video duration is unavailable in the supplied dataset.
- Treat duration as a limitation or future-work note rather than a reason to add a new data-collection pipeline.
## Recommended Package Set
- `pandas`
- `pyarrow`
- `seaborn`
- `matplotlib`
- `statsmodels`
- `scikit-learn`
- `pandera`
- `jupyterlab` or VS Code notebooks
- `quarto` CLI installed separately
- `jupytext` optional
- `spacy`
- `transformers`
- `sentence-transformers` optional
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
- Python 3.12
- `pandas` + `pyarrow` for ingestion, cleaning, and cached Parquet datasets
- VS Code notebooks or JupyterLab for iterative analysis
- `seaborn` + `matplotlib` for the final figures
- `statsmodels` + `scikit-learn` for interpretable factor analysis
- `spaCy` + selective `transformers` inference for the NLP section
- `pandera` for schema validation
- `pip-tools` for pinned dependencies
- `Quarto` for the final report output
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
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.github/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
