# Feature Landscape

**Domain:** Academic report-first analysis of Trending YouTube Video Statistics with checkpoint notebooks
**Researched:** 2026-04-19
**Scope:** All country CSV files in `data/`; final deliverable is a teacher-ready Vietnamese PDF, not a frontend app, with notebooks kept as checkpoints
**Confidence:** HIGH for assignment-fit recommendations, MEDIUM for optional differentiators

A strong project in this domain should optimize for defensible analysis, not breadth for its own sake. The best final report is the one that answers the required questions clearly, uses the dataset honestly, and converts findings into practical recommendations for a new YouTube channel, while checkpoint notebooks stay supporting artifacts.

The key constraint is that this dataset contains videos that already trended. That means the project cannot directly answer "what makes any uploaded video trend" in a causal sense. Instead, it should analyze what characteristics are associated with stronger performance within the trending set and state that limitation explicitly.

## Table Stakes for This Assignment

Features users expect. Missing = the project will feel incomplete or academically weak.

| Capability | Why Expected | Complexity | Major Dependencies | Notes |
|---------|--------------|------------|--------------------|-------|
| Multi-country data ingestion and harmonization | The assignment scope is all country files, so the notebook must combine them into one analysis-ready dataset with a country identifier. | Medium | Iterating through all CSVs, schema consistency checks, type coercion, missing-value handling | Parse `trending_date` and `publish_time`, standardize booleans, and preserve country as a first-class feature. |
| Unit-of-analysis and success-proxy definition | The raw data is at the daily trending-row level, not the upload level. A strong project must define what "performance" means before analysis. | Medium | Cleaned combined dataset, duplicate handling across dates, metric design | Recommended proxies: views, engagement ratios, and number of trending appearances per video. State clearly that no non-trending control group exists. |
| Core feature engineering for trending factors | The required question is what factors help videos trend, so the notebook needs engineered variables that represent timing, metadata, and engagement structure. | Medium | Harmonized data, parsed datetimes, proxy definition | Minimum useful features: publish weekday/hour, lag from publish to trend, title length, description length, tag count, missing-description flag, engagement ratios, and category/country indicators. |
| Required factor analysis with interpretable visuals | The project must show evidence for which factors are associated with stronger trending performance. | Medium | Feature engineering, success proxy, visualization setup | Favor grouped summaries, correlation analysis, regression-style interpretation, and clear charts over black-box modeling. |
| Category comparison across markets | The assignment explicitly requires comparison across content categories. | Medium | Harmonized data, category identifiers, aggregation logic | Compare category-level views, engagement, publish timing, and sentiment patterns. If category labels are unavailable in-repo, use `category_id` consistently or add a small lookup table. |
| Sentiment analysis on tags and descriptions | The assignment explicitly requires sentiment analysis, so some text-analysis capability is mandatory. | Medium | Text cleaning, tokenization policy, language-handling policy, missing-text handling | Baseline is enough if it is honest: sentiment on descriptions plus tag-text cues, with limitations for multilingual and keyword-style tags. |
| Synthesis into recommendations for a new channel | The final deliverable must convert descriptive findings into practical guidance. | Low | Completed factor, sentiment, and category analyses | Recommendations should cover posting windows, category focus, metadata hygiene, and what not to over-interpret. |
| Clear academic report structure with checkpoint notebooks | Even good analysis can score poorly if the narrative is weak. | Low | All prior analyses, plotting outputs, written interpretation | Minimum structure: question, data, preprocessing, method, findings, recommendations, limitations, conclusion. |
| Limitations and validity discussion | This dataset has selection bias, repeated rows per video, and cross-country language issues. Ignoring those would weaken the submission. | Low | Understanding of dataset structure and methods used | Must explicitly discuss correlation vs causation, trending-only sample bias, and multilingual text limitations. |

## Differentiators

Features that materially improve the project if time allows. These strengthen the report, but they are not necessary before the table-stakes work is complete.

| Capability | Value Proposition | Complexity | Major Dependencies | Notes |
|---------|-------------------|------------|--------------------|-------|
| Cross-country transferability analysis | Distinguishes globally consistent patterns from country-specific ones, which makes recommendations more nuanced and defensible. | High | Harmonized data, factor analysis, category comparison | Useful outputs: country clusters, market-specific posting windows, and categories that travel well across markets. |
| Multilingual-aware sentiment strategy | Improves the weakest part of the assignment by treating non-English descriptions and tags more carefully. | High | Language detection, translation or multilingual sentiment tooling, cleaned text | Stronger than applying one English lexicon to every market. If done, include a sensitivity comparison versus the baseline method. |
| Interpretable predictive modeling | Adds rigor by testing how well engineered features explain variation in views or repeat trending appearances. | Medium-High | Feature matrix, train/test split, outlier treatment, evaluation metrics | Keep it interpretable: linear models, regularized regression, or tree-based feature importance. Use prediction only to support interpretation, not as the main deliverable. |
| Robustness and sensitivity checks | Shows academic maturity by testing whether conclusions survive different assumptions. | Medium | Base analyses complete, alternative aggregations, transform choices | Recommended checks: unique-video vs daily-row aggregation, log-transformed views, outlier trimming, per-country re-runs. |
| Category-storytelling layer | Makes the report more compelling by moving from raw category comparisons to category archetypes and strategy implications. | Medium | Category comparison, recommendations synthesis | Example: compare music, entertainment, and news not just on views but on timing, text tone, and engagement structure. |
| Reproducible output packaging | Makes the submission cleaner and easier to defend if asked to rerun or explain steps. | Low-Medium | Stable notebook flow, cleaned-data export, figure generation | Examples: a saved cleaned dataset, a configuration cell, and figures with consistent titles/captions. |

## Anti-Features

Features to explicitly avoid because they add work without improving the assignment outcome.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Frontend dashboard or web app | The brief is report-first, and UI work will consume time that should go into analysis quality. | Build clear checkpoint notebooks and publication-quality figures for the final report. |
| Causal claims about the YouTube algorithm | The dataset is observational and includes only trending videos, so causal language would overstate the evidence. | Use associative language such as "is associated with" or "appears correlated with." |
| Heavy deep-learning or LLM sentiment pipeline | The dataset text is noisy, multilingual, and often short; a complex model adds risk without guaranteed value. | Use a transparent baseline first, then add multilingual-aware sentiment only if time remains. |
| Live scraping or YouTube API enrichment | This changes project scope, introduces reproducibility issues, and is unnecessary for the assignment questions. | Stay within the repository dataset and document its limitations honestly. |
| Thumbnail, frame, or video-content computer vision analysis | Interesting, but far outside the core assignment and not supported by the current dataset. | Focus on metadata, timing, text, engagement, and category signals. |
| Recommendation engine or channel-growth simulator | This turns an analysis project into a product-design project and will likely stay half-finished. | End with a concise recommendation playbook grounded in the observed analyses. |
| Excessive generic EDA | Many plots with no clear link to the research questions make the report look busy rather than rigorous. | Keep each chart tied to one assignment question or recommendation. |
| Comment-level NLP | The dataset only has comment counts, not comment text, so this would require new data collection. | Analyze `comment_count` as engagement, not comment sentiment. |

## Feature Dependencies

```text
Multi-country ingestion and harmonization
  -> Unit-of-analysis and success-proxy definition
  -> Core feature engineering

Core feature engineering
  -> Factor analysis
  -> Category comparison
  -> Recommendation synthesis

Text cleaning and language-handling policy
  -> Sentiment analysis
  -> Recommendation synthesis on titles/tags/descriptions

Factor analysis + Category comparison + Sentiment analysis
  -> Recommendations for a new channel

All analyses
  -> Limitations discussion
  -> Final report narrative and PDF packaging
```

## MVP Recommendation

Prioritize:
1. Multi-country ingestion and harmonization
2. Unit-of-analysis plus success-proxy definition
3. Core feature engineering for timing, text, category, and engagement
4. Factor analysis and category comparison with clear visuals
5. Baseline sentiment analysis with explicit multilingual limitations
6. Final recommendations for a new channel plus a limitations section

Defer:
- Cross-country transferability analysis: valuable, but not before the assignment-required questions are answered cleanly.
- Interpretable predictive modeling: useful only after the descriptive analysis is already strong.
- Multilingual-aware sentiment upgrades: worth doing if the baseline sentiment results look too weak or too English-biased.

## Recommended Capability Set for This Project

If time is limited, the strongest version of this project is:
1. A clean combined dataset across all countries
2. A defensible definition of trending performance within the available data
3. Interpretable analysis of timing, metadata, engagement, and categories
4. A baseline sentiment section over tags/descriptions with honest caveats
5. Practical recommendations for a hypothetical new channel
6. A concise methodology and limitations discussion that protects the analysis from overclaiming

That combination is strong enough for an academic submission because it is aligned with the assignment, feasible within a checkpoint-notebook workflow, and rigorous about what the dataset can and cannot support.

## Sources

- Project brief: `.planning/PROJECT.md`
- Repository dataset inventory: `data/` country CSV files
- Representative schema check: `data/USvideos.csv` header (`video_id`, `trending_date`, `title`, `channel_title`, `category_id`, `publish_time`, `tags`, `views`, `likes`, `dislikes`, `comment_count`, flags, `description`)
