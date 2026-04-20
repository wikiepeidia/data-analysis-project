# Phase 1 Canonical Dataset and Performance Frame

This Markdown checkpoint documents the canonical dataset contract for later phases in a text format that is cheaper to diff, summarize, and reuse.

## Raw data inventory

- Source corpus: `data/*videos.csv`
- Country coverage: 10 country files
- Country metadata is derived from each filename prefix and preserved in downstream artifacts.

## Canonical row-level table

- Output artifact: `data/processed/trending_rows.parquet`
- Grain: one row per raw trending observation
- Phase 1 preserves raw text while adding helper columns for parsed dates, normalized booleans, tag parsing, and missing-value flags.

## Video-country snapshot table

- Output artifact: `data/processed/video_country_snapshot.parquet`
- Default analysis grain: one row per `country + video_id`
- Anchor rule: use the first local trending observation for that country-video pair
- Multi-country videos remain separate rows instead of being collapsed into one global timeline.

## Trending-corpus performance proxy

The primary Phase 1 target is `trend_days_in_country_proxy`, defined as the number of row-level trending observations for a given `country + video_id` pair. This is a trending-corpus proxy, not a causal score. The project reports association inside the trending corpus rather than causes of entering the trending list. Views, likes, dislikes, and comments remain secondary context metrics captured from the first trending snapshot.

## Limitations

This dataset only contains videos that were already trending, so the analysis can describe association inside the trending corpus but not causal effects. Human-readable category labels are unresolved in the current repository, and video duration is unavailable in the provided dataset. Those limits must stay visible in later reporting.

## Re-run instructions

Regenerate the cached Phase 1 artifacts from the repo root with:

```bash
python -m youtube_trends.canonical_dataset
python -m youtube_trends.performance_frame
```

The first command rebuilds the row-level canonical parquet and source manifest. The second command rebuilds the video-country snapshot parquet from the canonical row-level table.
