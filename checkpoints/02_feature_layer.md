# Phase 2 Feature Layer

This Markdown checkpoint documents the reusable Phase 2 feature table built on top of the Phase 1 video-country snapshot parquet.

## Feature table artifact

- Input artifact: `data/processed/video_country_snapshot.parquet`
- Output artifact: `data/processed/video_country_features.parquet`
- Default grain: one row per `country + video_id`
- Phase 2 adds reusable feature columns without redefining the Phase 1 proxy columns or raw text fields.

## Timing features

- `publish_hour_utc`, `publish_weekday_utc`, `publish_weekday_name_utc`, `publish_month_utc`, and `publish_quarter_utc` are derived from `publish_time` and stay explicitly in UTC.
- `publish_is_weekend_utc` marks Saturday and Sunday in UTC time.
- `publish_to_first_trend_days` remains the whole-day lag between the UTC publish date and the first local trending date.
- `first_trending_weekday_local`, `first_trending_weekday_name_local`, and `trend_span_days_observed` summarize when a video first appeared and how long the observed trending span lasted inside one country.

## Metadata features

- Title helpers: `title_char_count`, `title_word_count`, `title_has_question_mark`, `title_has_exclamation_mark`, and `title_has_digits`.
- Description helpers: `description_char_count`, `description_word_count`, and `description_has_links`.
- Tag helpers: `tag_count`, `tags_is_missing`, `tags_char_count`, and `avg_tag_length_chars`.
- These features stay structural and language-light so Phase 2 does not pretend to solve multilingual NLP before Phase 4.

## Engagement context features

- `first_trending_engagement_total` combines first-snapshot likes, dislikes, and comment counts.
- `like_rate_vs_first_trending_views`, `dislike_rate_vs_first_trending_views`, `comment_rate_vs_first_trending_views`, and `engagement_rate_vs_first_trending_views` turn first-snapshot counts into comparable rates with safe zero handling.
- `log1p_first_trending_views`, `log1p_first_trending_likes`, and `log1p_first_trending_comment_count` provide stable transformed outcome fields for downstream descriptive analysis.
- These engagement features are post-trending context, not pre-publish drivers. Recommendations for a new channel still need to focus on creator-controlled inputs.

## Interpretation guardrails

- Timing fields must stay labeled as UTC or local-date semantics exactly as documented above; do not turn them into creator-local claims unless creator geography is known.
- Category labels remain unresolved in-repo and should not be guessed from memory in downstream checkpoints or reports.
- The project still reports association inside the trending corpus, not causal effects.
- video duration is unavailable in the provided dataset, so Phase 2 does not invent a duration proxy from title or description length.

## Re-run instructions

Regenerate the Phase 2 feature table from the repo root with:

```bash
python -m youtube_trends.feature_layer
```

This command reads `data/processed/video_country_snapshot.parquet` and writes `data/processed/video_country_features.parquet`.
