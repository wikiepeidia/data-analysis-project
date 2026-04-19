# Domain Pitfalls

**Domain:** Academic multi-country YouTube trending analysis
**Project:** Trending YouTube Video Statistics report-first workflow with checkpoint notebooks
**Researched:** 2026-04-19
**Overall confidence:** HIGH for dataset-structure pitfalls, MEDIUM for NLP-interpretation pitfalls

## Working Phase Labels For This Project

To make the warnings actionable before a roadmap exists, the pitfalls below refer to these recommended phases:

- **Phase 1 - Research Design and Scope Lock:** define the exact questions the notebook can answer with this dataset.
- **Phase 2 - Cleaning and Standardization:** parse dates, clean text, deduplicate, and create analysis-ready tables.
- **Phase 3 - Comparative Analysis and NLP:** run category, country, timing, and text analyses with clear assumptions.
- **Phase 4 - Recommendations and Final Storytelling:** turn findings into defensible advice for a new channel and package them for the final Vietnamese PDF.

## Critical Pitfalls

### Pitfall 1: Treating every trending row as a different video
**What goes wrong:** The same `video_id` can appear on multiple trending dates, so row counts overstate the number of distinct videos. If every row is treated as an independent sample, hit videos get counted repeatedly and dominate correlations.

**Why it happens:** This dataset tracks trending snapshots, not one clean record per video.

**Consequences:** Statistical summaries become biased, feature importance is inflated, and the notebook may mistake persistence on the trending list for broader popularity.

**Warning signs:**
- The same `video_id` appears many times in one country file.
- Top categories or channels look extreme because one viral video contributed many rows.
- A model or chart becomes much weaker after deduplicating to one row per `video_id` or per `video_id` + country.

**Prevention strategy:**
- Decide the unit of analysis before any major chart: trending observation, unique video, or video-country pair.
- Create at least two tables: a row-level table for trend-duration questions and a deduplicated video-level table for title/tag/category comparisons.
- When measuring factors associated with stronger performance, prefer one representative row per video-country pair or aggregate carefully.

**Phase to address:** Phase 2 - Cleaning and Standardization

### Pitfall 2: Mis-parsing the dotted `trending_date` and mixing it with UTC `publish_time`
**What goes wrong:** `publish_time` is an ISO timestamp, while `trending_date` is a short dotted date such as `18.07.02` that is easy to interpret incorrectly. If the format is parsed incorrectly, or if UTC publish timestamps are mixed with country-market dates without care, any "best posting time" or "time to trend" conclusion becomes unreliable.

**Why it happens:** The two fields use different formats and different levels of precision. The market file also represents where the video trended, not necessarily the creator's local timezone.

**Consequences:** Incorrect weekday/hour bins, impossible negative lag values, misleading golden-hour recommendations, and invalid cross-country timing comparisons.

**Warning signs:**
- Parsed dates produce negative `time_to_trend` values.
- A large share of uploads appear to trend before they were published.
- The notebook switches between UTC hours, local hours, and market-country assumptions without saying so.

**Prevention strategy:**
- Explicitly document how `trending_date` is parsed before using it.
- Keep `publish_time` in UTC as the canonical timestamp, then derive comparison-friendly fields from that choice.
- Use day-level lag when the trending field has no hour component.
- Frame timing insights as market-observed timing patterns, not creator-local posting rules, unless creator geography is known.

**Phase to address:** Phase 2 - Cleaning and Standardization

### Pitfall 3: Claiming to explain "what makes a video trend" with a trending-only dataset
**What goes wrong:** The dataset contains videos that already trended. Without a non-trending comparison group, the notebook cannot estimate the true probability of trending or make strong causal claims about why a video entered the trending list.

**Why it happens:** The assignment wording invites causal language, but the available data is a selected sample of successful cases.

**Consequences:** Overstated conclusions such as "videos with X are more likely to trend" when the data only shows patterns inside the trending set.

**Warning signs:**
- The report uses language like "causes trending" or "predicts trending" without non-trending examples.
- Charts compare only high-view trending videos against lower-view trending videos and present that as a general rule.
- Recommendations are written as if they apply to all YouTube uploads rather than to videos already inside the trending ecosystem.

**Prevention strategy:**
- Reframe the question as "among trending videos, which patterns are associated with stronger performance or longer persistence?"
- Separate descriptive findings from causal claims.
- If no external baseline is added, state clearly that the analysis explains variation within trending videos, not the full path from upload to trending.

**Phase to address:** Phase 1 - Research Design and Scope Lock

### Pitfall 4: Using post-trending outcome variables as if they were pre-trending drivers
**What goes wrong:** `views`, `likes`, `dislikes`, and `comment_count` are observed after a video has already reached the trending dataset snapshot. They are outcomes of exposure, not clean pre-publish inputs. Using them to answer "how can a new channel make videos trend?" creates leakage.

**Why it happens:** Those columns are numeric, easy to model, and often show strong correlations, so they are tempting to treat as explanatory variables.

**Consequences:** Recommendations become circular: "to trend, get more views and likes." That is descriptive, not actionable.

**Warning signs:**
- A feature ranking puts `views` or `likes` at the top of the factors behind trending success.
- The recommendation section tells a new channel to optimize variables it cannot control before publish.
- The notebook does not distinguish pre-publish features from post-exposure outcomes.

**Prevention strategy:**
- Use `views`, `likes`, `dislikes`, and `comment_count` only for outcome analysis, category performance comparisons, or engagement profiling.
- Restrict new-channel recommendations to pre-publish or creator-controlled features: publish timing, title wording, tag structure, description completeness, and category choice.
- Label leakage-prone variables clearly in the methodology section.

**Phase to address:** Phase 3 - Comparative Analysis and NLP

### Pitfall 5: Running one English-only NLP pipeline over all countries
**What goes wrong:** Titles, tags, and descriptions are multilingual across the country CSV files. A single English stopword list, tokenizer, sentiment lexicon, or embedding assumption will underperform badly on Japanese, Korean, Russian, French, German, and mixed-language text.

**Why it happens:** The assignment asks for sentiment analysis, and basic notebook examples usually assume English text.

**Consequences:** False neutral sentiment, broken token frequencies, meaningless keyword clouds, and misleading comparisons where English-speaking markets look more analyzable only because the pipeline fits them better.

**Warning signs:**
- Non-Latin scripts dominate token output as unreadable fragments.
- Sentiment scores cluster near zero for entire countries.
- Important tags disappear because the tokenizer strips punctuation, separators, or non-English characters.

**Prevention strategy:**
- Decide up front whether the NLP analysis will be multilingual or restricted to a justified subset such as English-language markets.
- If the project keeps all countries, treat language as a first-class variable and compare within-language or within-country groups before pooling.
- For a stronger NLP component, prefer multilingual sentence embeddings or multilingual sentiment tools over an English lexicon, and document remaining limitations.
- Keep a simpler fallback: keyword/category/topic patterns if sentiment quality is weak.

**Phase to address:** Phase 3 - Comparative Analysis and NLP

### Pitfall 6: Calling title/tag sentiment "audience sentiment"
**What goes wrong:** The assignment mentions sentiment analysis through tags or descriptions, but those fields reflect creator wording, not how viewers felt. Treating lexical polarity in metadata as audience emotion is conceptually wrong.

**Why it happens:** The dataset does not provide raw viewer comments in a clean, cross-country way, so the available text fields look like the nearest proxy.

**Consequences:** The notebook overclaims psychological insight and may say things like "audiences prefer positive sentiment" when it actually measured title tone or tag wording.

**Warning signs:**
- The report uses phrases like "viewer sentiment" or "public emotion" while analyzing only titles, tags, or descriptions.
- Positive/negative scores are discussed without examples showing that the labels make sense for YouTube metadata.
- Sentiment findings contradict obvious domain context, such as tragedy or news titles receiving strong engagement.

**Prevention strategy:**
- Rename the task precisely: analyze metadata tone, lexical polarity, or semantic framing.
- Validate any sentiment approach with manual samples from at least a few countries before scaling it.
- Pair sentiment-like features with topic/category context so the analysis does not stand alone.
- If validity is weak, replace sentiment with a stronger NLP component such as topic clustering, multilingual keyword extraction, or title-style patterns.

**Phase to address:** Phase 3 - Comparative Analysis and NLP

### Pitfall 7: Comparing raw performance across countries as if the markets were directly equivalent
**What goes wrong:** Raw `views`, `likes`, and `comment_count` are not directly comparable across countries with different population sizes, YouTube adoption, language ecosystems, and channel export patterns.

**Why it happens:** The project scope uses all country CSV files, so pooled plots are easy to produce but easy to misread.

**Consequences:** The notebook may conclude that one market "performs better" when it is mostly measuring market size, channel scale, or platform penetration.

**Warning signs:**
- Country ranking charts rely only on raw totals or means.
- One or two large markets dominate pooled regressions and visual scales.
- Recommendations for a new channel ignore whether the goal is local-market growth or broad international reach.

**Prevention strategy:**
- Normalize within country before pooling: percentiles, ranks, z-scores, log transforms, or country-fixed comparisons.
- Present country-specific findings first, then pooled findings with clear caveats.
- Distinguish between market where a video trended and origin of the channel; they are not the same thing.
- State whether each recommendation is intended for local optimization or cross-market visibility.

**Phase to address:** Phase 3 - Comparative Analysis and NLP

### Pitfall 8: Ignoring missing, synthetic, or low-quality text values
**What goes wrong:** Fields such as `tags` and `description` can be empty, set to `[none]`, or contain boilerplate rather than meaningful content. If these are treated as ordinary text, the NLP output is polluted.

**Why it happens:** Notebook code often jumps straight into tokenization without auditing placeholders and missingness patterns first.

**Consequences:** Top keywords become artifacts, sentiment gets distorted, and missingness itself may hide a real pattern.

**Warning signs:**
- `[none]` appears among the most frequent tokens or tags.
- Empty descriptions are silently converted into empty strings and analyzed as normal observations.
- Boilerplate contact info, links, or copyright notices dominate token output.

**Prevention strategy:**
- Convert placeholders like `[none]` into true missing values before analysis.
- Strip obvious boilerplate such as repeated URLs and promotional footer text where justified.
- Track missingness as its own variable because the presence or absence of tags/descriptions may itself be informative.
- Keep sample outputs to verify that cleaned tokens still look human and topic-relevant.

**Phase to address:** Phase 2 - Cleaning and Standardization

### Pitfall 9: Using category IDs without a verified label mapping
**What goes wrong:** The CSV files contain numeric `category_id` values, but a category label mapping file is not obviously present in the repository snapshot. If labels are guessed from memory or copied from an unrelated source, category comparisons can be mislabeled.

**Why it happens:** The assignment explicitly asks for category comparisons, so there is pressure to attach names quickly.

**Consequences:** Wrong charts, wrong recommendations, and avoidable credibility loss in the report.

**Warning signs:**
- Category labels appear in the notebook without a cited mapping source.
- The same numeric ID is described differently in different notebook sections.
- A category ranking looks implausible because labels are shifted or merged incorrectly.

**Prevention strategy:**
- Verify the category mapping before the first category chart.
- If no trusted mapping file exists in the repo, add one explicit source or keep IDs in intermediate work until the mapping is confirmed.
- Document the mapping source in the notebook appendix or methodology notes.

**Phase to address:** Phase 2 - Cleaning and Standardization

### Pitfall 10: Promising a video-length analysis when the CSV does not contain duration
**What goes wrong:** The assignment brief mentions video length, but the observed CSV header does not include a duration column. If the notebook promises length-based findings without external enrichment, that section will collapse late in the project.

**Why it happens:** The assignment requirement and the dataset schema do not line up perfectly.

**Consequences:** Last-minute scope change, weak proxy variables, or fabricated conclusions.

**Warning signs:**
- The outline includes a full section on video duration before any duration source has been identified.
- Code notebooks start inventing proxies such as title length or description length as if they were video length.
- External API enrichment is mentioned without checking quota, reproducibility, or time cost.

**Prevention strategy:**
- Treat duration as a feasibility checkpoint, not an assumed feature.
- Either secure a reproducible enrichment source early and clearly separate enriched data from the original CSVs, or redefine that assignment bullet as a limitation and focus on publish timing, tags, titles, and categories.
- Do not substitute text-length proxies unless they are explicitly framed as different variables.

**Phase to address:** Phase 1 - Research Design and Scope Lock

### Pitfall 11: Confusing market country with creator country when giving posting recommendations
**What goes wrong:** Each CSV represents the country where the video trended, not necessarily where the channel is based. A "best time to post in Japan" claim may really describe when videos surfaced in the Japanese trending market, not when Japanese creators uploaded them.

**Why it happens:** The dataset is country-organized, which makes it tempting to treat each file as a creator-country dataset.

**Consequences:** Recommendations sound precise but rest on the wrong unit of geography.

**Warning signs:**
- The notebook uses file country as a direct proxy for channel origin.
- Time-window advice is written as creator-local guidance without discussing market-vs-origin ambiguity.
- Cross-country comparisons ignore that the same channel may appear in multiple country files.

**Prevention strategy:**
- Phrase findings as market-facing timing patterns unless creator geography is actually known.
- For recommendations to a new channel, explain whether the target is a specific audience market or a general upload strategy.
- Highlight this limitation explicitly in the timing section.

**Phase to address:** Phase 3 - Comparative Analysis and NLP

## Moderate Pitfalls

### Pitfall 12: Overfitting recommendations to established channels instead of a new channel
**What goes wrong:** Trending datasets overrepresent already large channels, celebrity creators, labels, and institutional media. If their patterns are copied directly, the advice may be unrealistic for a new channel with no existing audience.

**Why it happens:** High-visibility channels dominate the most memorable examples and produce the strongest raw metrics.

**Consequences:** Recommendations become aspirational but unusable, such as relying on celebrity collaborations, breaking-news access, or brand-scale promotion.

**Warning signs:**
- The "best practices" section is built from top channels only.
- Recommended tags are dominated by celebrity names, live-event phrases, or branded franchises.
- The report never discusses which findings remain actionable for a small or unknown channel.

**Prevention strategy:**
- Separate broad patterns from scale-dependent patterns.
- Prefer recommendations based on controllable behaviors: upload consistency, timing windows, metadata clarity, category focus, and title/tag conventions.
- Include at least one section that explicitly filters findings through the lens of a new channel's constraints.

**Phase to address:** Phase 4 - Recommendations and Final Storytelling

### Pitfall 13: Notebook scope creep from trying to do all analyses at full depth
**What goes wrong:** The assignment asks for cleaning, timing analysis, category comparison, sentiment/NLP, and recommendations across all countries. Adding translation, topic modeling, clustering, dashboards, and extra modeling on top of that can produce a messy notebook with shallow conclusions.

**Why it happens:** Academic notebooks often grow section by section without a locked question hierarchy.

**Consequences:** Late delivery, duplicated charts, weak narrative flow, and unfinished validation of the most important claims.

**Warning signs:**
- The notebook outline keeps expanding after the core questions are already covered.
- Large sections are exploratory but do not answer the teacher's required questions.
- The NLP part becomes a side project instead of supporting the final recommendations.

**Prevention strategy:**
- Lock an MVP storyline early: cleaning, timing, metadata/NLP, category comparisons, then recommendations for a new channel.
- Choose one stronger NLP contribution and execute it well rather than stacking many weaker techniques.
- Reserve optional extras for an appendix only after the core notebook is coherent.

**Phase to address:** Phase 1 - Research Design and Scope Lock

### Pitfall 14: Weak storytelling between evidence and recommendations
**What goes wrong:** The notebook may show many charts but fail to answer the business-style question: what should a new channel actually do next?

**Why it happens:** The project becomes chart-driven instead of question-driven.

**Consequences:** The final submission looks busy but not persuasive, and the teacher may see analysis without decision value.

**Warning signs:**
- Sections end with charts but no written takeaway.
- The recommendation section repeats numbers without turning them into actions.
- The notebook does not connect category, timing, and metadata findings into one coherent strategy.

**Prevention strategy:**
- Organize the notebook around the assignment questions, not around libraries or chart types.
- End each major section with a short "so what for a new channel" paragraph.
- Use a final recommendation table with action, evidence, risk, and confidence.

**Phase to address:** Phase 4 - Recommendations and Final Storytelling

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Research design | Claiming to explain overall trending probability from trending-only data | Reframe to variation within trending videos unless an external baseline is added |
| Research design | Planning video-length analysis without duration data | Make duration a go/no-go enrichment decision in the first phase |
| Cleaning | Duplicate videos counted as separate samples | Build row-level and deduplicated tables for different question types |
| Cleaning | Date parsing errors between `trending_date` and `publish_time` | Validate parsing with lag sanity checks before any timing chart |
| Cleaning | `[none]` and empty text polluting NLP | Convert placeholders to missing values and audit text quality samples |
| Cleaning | Category labels guessed from memory | Verify and document the category mapping source before comparison charts |
| NLP | English-only sentiment on multilingual data | Use multilingual methods or explicitly narrow scope |
| NLP | Metadata sentiment misnamed as audience sentiment | Frame results as metadata tone or semantic framing |
| Comparative analysis | Raw country totals treated as directly comparable | Normalize within country and separate local vs pooled findings |
| Comparative analysis | Market country confused with creator country | Phrase timing findings as market-facing unless channel geography is known |
| Recommendations | Leakage from post-trending engagement metrics | Use only creator-controlled features for advice to a new channel |
| Final notebook | Too many analyses, weak story | Keep one main storyline and move extras to an appendix |

## Sources

- `.planning/PROJECT.md` - project scope, deliverable, all-country requirement, stronger NLP preference
- `project.md` - assignment brief and required analyses
- `data/JPvideos.csv` - observed schema showing `trending_date`, `publish_time`, multilingual titles/tags/descriptions, and missing-text patterns such as `[none]`

## Bottom Line

The highest-risk failure modes for this assignment are not visualization issues. They are research-design errors: treating repeated trending rows as independent videos, making causal claims from a trending-only dataset, misreading time fields, and overpromising NLP validity on multilingual metadata. If those four risks are handled early, the final notebook can still be ambitious without becoming fragile.