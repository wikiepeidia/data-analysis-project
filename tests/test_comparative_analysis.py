from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from youtube_trends.comparative_analysis import (
    CATEGORY_COUNTRY_SUMMARY_FILENAME,
    CATEGORY_CROSS_COUNTRY_SUMMARY_FILENAME,
    COUNTRY_NORMALIZED_FILENAME,
    PATTERN_COUNTRY_SUMMARY_FILENAME,
    PATTERN_CROSS_COUNTRY_SUMMARY_FILENAME,
    build_country_normalized_frame,
    build_category_country_summary,
    build_category_cross_country_summary,
    build_pattern_country_summary,
    build_pattern_cross_country_summary,
    write_comparative_analysis_artifacts,
)


def _build_feature_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "country": "US",
                "video_id": "video-a",
                "category_id": 10,
                "trend_days_in_country_proxy": 3,
                "log1p_first_trending_views": 5.0,
                "engagement_rate_vs_first_trending_views": 0.20,
                "publish_weekday_name_utc": "Monday",
                "publish_hour_utc": 9,
                "description_is_missing": False,
                "tag_count": 8,
                "title_word_count": 6,
            },
            {
                "country": "US",
                "video_id": "video-b",
                "category_id": 20,
                "trend_days_in_country_proxy": 1,
                "log1p_first_trending_views": 3.0,
                "engagement_rate_vs_first_trending_views": 0.05,
                "publish_weekday_name_utc": "Monday",
                "publish_hour_utc": 20,
                "description_is_missing": True,
                "tag_count": 0,
                "title_word_count": 3,
            },
            {
                "country": "JP",
                "video_id": "video-c",
                "category_id": 10,
                "trend_days_in_country_proxy": 2,
                "log1p_first_trending_views": 4.0,
                "engagement_rate_vs_first_trending_views": 0.10,
                "publish_weekday_name_utc": "Friday",
                "publish_hour_utc": 10,
                "description_is_missing": False,
                "tag_count": 12,
                "title_word_count": 10,
            },
            {
                "country": "JP",
                "video_id": "video-d",
                "category_id": 30,
                "trend_days_in_country_proxy": 4,
                "log1p_first_trending_views": 6.0,
                "engagement_rate_vs_first_trending_views": 0.02,
                "publish_weekday_name_utc": "Friday",
                "publish_hour_utc": 1,
                "description_is_missing": True,
                "tag_count": 2,
                "title_word_count": 4,
            },
        ]
    )


def test_build_country_normalized_frame_adds_percentiles_and_buckets() -> None:
    normalized = build_country_normalized_frame(_build_feature_frame())

    us_high = normalized.loc[(normalized["country"] == "US") & (normalized["video_id"] == "video-a")].iloc[0]
    us_low = normalized.loc[(normalized["country"] == "US") & (normalized["video_id"] == "video-b")].iloc[0]

    assert us_high["proxy_percentile_within_country"] == 1.0
    assert us_low["proxy_percentile_within_country"] == 0.5
    assert str(us_high["publish_hour_bucket_utc"]) == "06-11 UTC"
    assert str(us_low["publish_hour_bucket_utc"]) == "18-23 UTC"
    assert str(us_high["tag_count_bucket"]) == "6-10 tags"
    assert str(us_low["description_presence"]) == "description missing"
    assert str(us_high["title_word_count_bucket"]) == "5-8 words"


def test_build_pattern_country_summary_includes_all_phase3_families() -> None:
    normalized = build_country_normalized_frame(_build_feature_frame())
    pattern_country = build_pattern_country_summary(normalized)
    category_country = build_category_country_summary(pattern_country)

    assert {"timing", "metadata", "category"} == set(pattern_country["analysis_family"])

    us_category_ten = category_country.loc[
        (category_country["country"] == "US") & (category_country["category_id"] == "10")
    ].iloc[0]
    assert us_category_ten["video_count"] == 1
    assert us_category_ten["share_within_country"] == 0.5
    assert us_category_ten["median_trend_days_in_country_proxy"] == 3


def test_build_pattern_cross_country_summary_tracks_country_spread() -> None:
    normalized = build_country_normalized_frame(_build_feature_frame())
    pattern_country = build_pattern_country_summary(normalized)
    pattern_cross = build_pattern_cross_country_summary(pattern_country)
    category_cross = build_category_cross_country_summary(pattern_cross)

    category_ten = category_cross.loc[category_cross["category_id"] == "10"].iloc[0]
    assert category_ten["markets_present"] == 2
    assert category_ten["countries_in_top_quartile"] == 1
    assert category_ten["highest_proxy_country"] == "US"
    assert category_ten["lowest_proxy_country"] == "JP"
    assert category_ten["proxy_percentile_spread_across_countries"] == 0.5


def test_write_comparative_analysis_artifacts_persists_expected_outputs(tmp_path: Path) -> None:
    input_path = tmp_path / "video_country_features.parquet"
    output_dir = tmp_path / "phase3_analysis"
    checkpoint_path = tmp_path / "03_cross_country_category_analysis.md"
    _build_feature_frame().to_parquet(input_path, index=False)

    outputs = write_comparative_analysis_artifacts(
        input_path=str(input_path),
        output_dir=str(output_dir),
        checkpoint_path=str(checkpoint_path),
    )

    assert (output_dir / COUNTRY_NORMALIZED_FILENAME).exists()
    assert (output_dir / PATTERN_COUNTRY_SUMMARY_FILENAME).exists()
    assert (output_dir / PATTERN_CROSS_COUNTRY_SUMMARY_FILENAME).exists()
    assert (output_dir / CATEGORY_COUNTRY_SUMMARY_FILENAME).exists()
    assert (output_dir / CATEGORY_CROSS_COUNTRY_SUMMARY_FILENAME).exists()
    assert checkpoint_path.exists()
    assert not outputs["category_cross_country_summary"].empty