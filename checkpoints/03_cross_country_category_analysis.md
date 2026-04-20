# Phase 3 Cross-Country Performance and Category Analysis

This Markdown checkpoint documents the country-aware comparative outputs built from `data/processed/video_country_features.parquet`. The phase keeps `trend_days_in_country_proxy` as the primary trending-corpus outcome and uses country-normalized summaries before pooled interpretation.

## Analysis artifacts

- Input artifact: `data/processed/video_country_features.parquet`
- Output directory: `data/processed/phase3_analysis`
- Country-normalized video table: `data/processed/phase3_analysis/country_normalized_video_country_features.parquet`
- Pattern summary by country: `data/processed/phase3_analysis/pattern_country_summary.parquet`
- Cross-country pattern summary: `data/processed/phase3_analysis/pattern_cross_country_summary.parquet`
- Category summary by country: `data/processed/phase3_analysis/category_country_summary.parquet`
- Cross-country category summary: `data/processed/phase3_analysis/category_cross_country_summary.parquet`

## Country-normalized comparison rules

- `trend_days_in_country_proxy` remains the primary association target, with log views and engagement rate kept as secondary context.
- Country-normalized percentile ranks are computed inside each market before pooled interpretation so large markets do not dominate the story by raw scale alone.
- Timing and metadata tables are reported as grouped association summaries, not causal claims about what makes any upload trend.
- Category comparisons use raw `category_id` values until a verified label source is added to the repo.

## Timing and metadata association tables

Top recurring timing patterns by mean within-country proxy percentile:

| analysis_dimension | dimension_value | markets_present | mean_median_proxy_percentile_within_country | proxy_percentile_spread_across_countries |
| --- | --- | --- | --- | --- |
| publish_hour_bucket_utc | 12-17 UTC | 10 | 0.436 | 0.280 |
| publish_weekday_name_utc | Friday | 10 | 0.436 | 0.280 |
| publish_weekday_name_utc | Thursday | 10 | 0.436 | 0.280 |
| publish_weekday_name_utc | Wednesday | 10 | 0.436 | 0.280 |
| publish_weekday_name_utc | Monday | 10 | 0.430 | 0.280 |
| publish_weekday_name_utc | Tuesday | 10 | 0.430 | 0.280 |
| publish_weekday_name_utc | Saturday | 10 | 0.430 | 0.280 |
| publish_hour_bucket_utc | 06-11 UTC | 10 | 0.412 | 0.280 |

Top recurring metadata patterns by mean within-country proxy percentile:

| analysis_dimension | dimension_value | markets_present | mean_median_proxy_percentile_within_country | proxy_percentile_spread_across_countries |
| --- | --- | --- | --- | --- |
| title_word_count_bucket | 0-4 words | 10 | 0.436 | 0.280 |
| description_presence | description present | 10 | 0.430 | 0.280 |
| tag_count_bucket | 11+ tags | 10 | 0.430 | 0.280 |
| title_word_count_bucket | 5-8 words | 10 | 0.430 | 0.280 |
| tag_count_bucket | 1-5 tags | 10 | 0.424 | 0.280 |
| title_word_count_bucket | 9-12 words | 10 | 0.418 | 0.280 |
| title_word_count_bucket | 13+ words | 10 | 0.418 | 0.280 |
| description_presence | description missing | 10 | 0.418 | 0.280 |

## Category comparison tables

Country-level category preview:

| country | category_id | video_count | share_within_country | median_proxy_percentile_within_country |
| --- | --- | --- | --- | --- |
| CA | 30 | 1 | 0.000 | 0.996 |
| CA | 23 | 1946 | 0.080 | 0.714 |
| CA | 10 | 1564 | 0.064 | 0.714 |
| CA | 28 | 636 | 0.026 | 0.714 |
| CA | 15 | 211 | 0.009 | 0.714 |
| CA | 19 | 202 | 0.008 | 0.714 |
| CA | 24 | 8248 | 0.338 | 0.297 |
| CA | 25 | 2941 | 0.120 | 0.297 |
| CA | 22 | 2559 | 0.105 | 0.297 |
| CA | 17 | 1932 | 0.079 | 0.297 |
| CA | 26 | 1272 | 0.052 | 0.297 |
| CA | 1 | 1151 | 0.047 | 0.297 |

Cross-country category summary:

| category_id | markets_present | mean_share_within_country | mean_median_proxy_percentile_within_country | highest_proxy_country | lowest_proxy_country |
| --- | --- | --- | --- | --- | --- |
| 30 | 5 | 0.000 | 0.681 | CA | FR |
| 44 | 3 | 0.000 | 0.579 | FR | DE |
| 19 | 10 | 0.005 | 0.511 | JP | DE |
| 10 | 10 | 0.089 | 0.501 | CA | JP |
| 23 | 10 | 0.063 | 0.500 | JP | GB |
| 28 | 10 | 0.021 | 0.482 | JP | IN |
| 15 | 10 | 0.015 | 0.478 | CA | JP |
| 1 | 10 | 0.052 | 0.467 | IN | JP |
| 20 | 10 | 0.031 | 0.449 | IN | JP |
| 43 | 8 | 0.003 | 0.442 | US | IN |

## Cross-country consistency notes

Largest category spreads across countries show where the same `category_id` behaves differently by market:

| category_id | markets_present | proxy_percentile_spread_across_countries | highest_proxy_country | lowest_proxy_country |
| --- | --- | --- | --- | --- |
| 43 | 8 | 0.683 | US | IN |
| 30 | 5 | 0.620 | CA | FR |
| 28 | 10 | 0.520 | JP | IN |
| 44 | 3 | 0.481 | FR | DE |
| 1 | 10 | 0.471 | IN | JP |
| 20 | 10 | 0.471 | IN | JP |
| 10 | 10 | 0.423 | CA | JP |
| 15 | 10 | 0.423 | CA | JP |
| 23 | 10 | 0.422 | JP | GB |
| 27 | 10 | 0.386 | GB | IN |

Cross-country consistency should be read together with the country tables above. High mean percentile with low spread suggests a more repeatable pattern, while high spread marks market-specific behavior that should stay local in the report narrative.

## Interpretation guardrails

- The project still reports association inside the trending corpus, not causal effects.
- `views`, `likes`, `dislikes`, and `comment_count` remain post-trending context rather than creator-controlled pre-publish drivers.
- Category labels stay as raw `category_id` values until a verified mapping source is added.
- Country-normalized pooling is required before any pooled category conclusion is stated in the report draft.
- video duration is unavailable in the provided dataset, so this phase does not invent a duration proxy from metadata counts.

## Re-run instructions

Regenerate the Phase 3 comparative outputs from the repo root with:

```bash
python -m youtube_trends.comparative_analysis
```

This command reads the Phase 2 feature parquet, writes the country-normalized and summary parquets, and refreshes this checkpoint.
