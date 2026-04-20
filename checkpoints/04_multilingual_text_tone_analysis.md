# Phase 4 Multilingual Text Tone Analysis

This Markdown checkpoint documents the Phase 4 outputs built from `data/processed/video_country_features.parquet`. The phase reports metadata tone through Unicode-aware structural features rather than pretending one semantic sentiment model is reliable across every country file.

## Analysis artifacts

- Input artifact: `data/processed/video_country_features.parquet`
- Output directory: `data/processed/phase4_analysis`
- Row-level tone frame: `data/processed/phase4_analysis/multilingual_text_tone_frame.parquet`
- Tone summary by country: `data/processed/phase4_analysis/text_tone_country_summary.parquet`
- Cross-country tone summary: `data/processed/phase4_analysis/text_tone_cross_country_summary.parquet`

## Multilingual handling rules

- `description_tone_bucket` and `tag_tone_bucket` are metadata tone fields. They describe wording structure, not viewer emotion or universal semantic sentiment.
- `description_text_quality` and `tag_text_quality` surface `likely_mojibake` explicitly when corrupted decoding markers make text hard to trust semantically.
- Script family is estimated from Unicode character names so non-Latin text stays visible instead of being forced through English-only token rules.
- Cross-country text conclusions are limited to readable-text coverage and structural metadata tone; this phase does not claim audience sentiment across every language.

## Description tone tables

Top description_tone_bucket patterns by mean within-country proxy percentile:

| dimension_value | markets_present | mean_share_within_country | mean_median_proxy_percentile_within_country | proxy_percentile_spread_across_countries |
| --- | --- | --- | --- | --- |
| corrupted_or_unreadable | 9 | 0.350 | 0.426 | 0.657 |
| missing | 10 | 0.059 | 0.418 | 0.280 |
| emphatic | 10 | 0.024 | 0.407 | 0.280 |
| question_led | 10 | 0.007 | 0.407 | 0.424 |
| plain_or_informational | 10 | 0.098 | 0.403 | 0.280 |
| link_heavy | 10 | 0.497 | 0.395 | 0.388 |

## Tag tone tables

Top tag_tone_bucket patterns by mean within-country proxy percentile:

| dimension_value | markets_present | mean_share_within_country | mean_median_proxy_percentile_within_country | proxy_percentile_spread_across_countries |
| --- | --- | --- | --- | --- |
| plain_keywords | 10 | 0.110 | 0.436 | 0.280 |
| symbolic_or_emphatic | 10 | 0.031 | 0.430 | 0.280 |
| corrupted_or_unreadable | 9 | 0.283 | 0.426 | 0.616 |
| dense_keywords | 10 | 0.494 | 0.395 | 0.388 |
| missing | 10 | 0.111 | 0.383 | 0.314 |

## Text-quality and coverage notes

Country-level readable-text coverage preview:

| country | video_count | description_missing_share | description_likely_mojibake_share | tags_missing_share | tags_likely_mojibake_share |
| --- | --- | --- | --- | --- | --- |
| RU | 34282 | 0.063 | 0.891 | 0.101 | 0.842 |
| JP | 12912 | 0.104 | 0.820 | 0.156 | 0.734 |
| KR | 15876 | 0.101 | 0.816 | 0.221 | 0.702 |
| MX | 33513 | 0.108 | 0.590 | 0.200 | 0.259 |
| FR | 30581 | 0.081 | 0.020 | 0.143 | 0.003 |
| CA | 24427 | 0.040 | 0.007 | 0.067 | 0.003 |
| DE | 29627 | 0.044 | 0.004 | 0.081 | 0.002 |
| GB | 3272 | 0.018 | 0.001 | 0.054 | 0.001 |
| US | 6351 | 0.017 | 0.001 | 0.042 | 0.000 |
| IN | 16307 | 0.018 | 0.000 | 0.043 | 0.000 |

Cross-country script and quality surfaces:

| analysis_dimension | dimension_value | markets_present | mean_share_within_country |
| --- | --- | --- | --- |
| description_script_family | latin | 10 | 0.912 |
| description_script_family | missing | 10 | 0.059 |
| description_script_family | mixed_or_other | 7 | 0.033 |
| description_script_family | cyrillic | 4 | 0.005 |
| description_script_family | east_asian | 5 | 0.005 |
| description_script_family | symbolic_or_numeric | 8 | 0.001 |
| description_text_quality | readable_multilingual | 10 | 0.389 |
| description_text_quality | likely_mojibake | 9 | 0.350 |
| description_text_quality | ascii_or_plain_latin | 10 | 0.237 |
| description_text_quality | missing | 10 | 0.059 |

High `likely_mojibake` shares mean semantic sentiment would be weak or misleading in those markets. Structural metadata tone remains usable, but it should be read with the coverage table above.

## Interpretation guardrails

- The project still reports association inside the trending corpus, not causal effects.
- Phase 4 measures metadata tone, not audience emotion, because the available text comes from titles, tags, and descriptions rather than viewer reactions.
- Corrupted text remains visible through quality buckets instead of being silently pooled into one global sentiment score.
- Phase 3 country-aware comparison rules still apply before any pooled cross-country text statement is made.
- video duration is unavailable in the provided dataset, so this phase does not invent a duration proxy from text fields.

## Re-run instructions

Regenerate the Phase 4 text-tone outputs from the repo root with:

```bash
python -m youtube_trends.text_tone_analysis
```

This command reads the Phase 2 feature parquet, writes the Phase 4 tone artifacts, and refreshes this checkpoint.
