from __future__ import annotations

from math import isclose, log1p
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from youtube_trends.feature_layer import build_video_country_features, write_video_country_features


def _build_snapshot_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "country": "US",
                "video_id": "video-a",
                "publish_time": pd.Timestamp("2017-11-13T17:13:01Z"),
                "first_trending_date_local": pd.Timestamp("2017-11-14").date(),
                "last_trending_date_local": pd.Timestamp("2017-11-16").date(),
                "publish_to_first_trend_days": 1,
                "trend_days_in_country_proxy": 3,
                "title": "Top 10 Tips?!",
                "title_normalized": "Top 10 Tips?!",
                "tags": '"alpha"|"beta"',
                "tags_normalized": '"alpha"|"beta"',
                "description": "See https://example.com now",
                "description_normalized": "See https://example.com now",
                "tags_is_missing": False,
                "description_is_missing": False,
                "tags_list": ["alpha", "beta"],
                "tag_count": 2,
                "first_trending_views": 100,
                "first_trending_likes": 10,
                "first_trending_dislikes": 2,
                "first_trending_comment_count": 5,
            },
            {
                "country": "JP",
                "video_id": "video-b",
                "publish_time": pd.Timestamp("2017-11-18T03:00:00Z"),
                "first_trending_date_local": pd.Timestamp("2017-11-20").date(),
                "last_trending_date_local": pd.Timestamp("2017-11-20").date(),
                "publish_to_first_trend_days": 2,
                "trend_days_in_country_proxy": 1,
                "title": "News Update",
                "title_normalized": "News Update",
                "tags": "[none]",
                "tags_normalized": None,
                "description": "",
                "description_normalized": None,
                "tags_is_missing": True,
                "description_is_missing": True,
                "tags_list": [],
                "tag_count": 0,
                "first_trending_views": 0,
                "first_trending_likes": 0,
                "first_trending_dislikes": 0,
                "first_trending_comment_count": 0,
            },
        ]
    )


def test_build_video_country_features_adds_timing_columns() -> None:
    features = build_video_country_features(_build_snapshot_frame())
    us_row = features.loc[(features["country"] == "US") & (features["video_id"] == "video-a")].iloc[0]
    jp_row = features.loc[(features["country"] == "JP") & (features["video_id"] == "video-b")].iloc[0]

    assert us_row["publish_hour_utc"] == 17
    assert us_row["publish_weekday_utc"] == 0
    assert us_row["publish_weekday_name_utc"] == "Monday"
    assert bool(us_row["publish_is_weekend_utc"]) is False
    assert us_row["first_trending_weekday_local"] == 1
    assert us_row["trend_span_days_observed"] == 2
    assert bool(jp_row["publish_is_weekend_utc"]) is True


def test_build_video_country_features_adds_metadata_features() -> None:
    features = build_video_country_features(_build_snapshot_frame())
    us_row = features.loc[(features["country"] == "US") & (features["video_id"] == "video-a")].iloc[0]
    jp_row = features.loc[(features["country"] == "JP") & (features["video_id"] == "video-b")].iloc[0]

    assert us_row["title_char_count"] == 13
    assert us_row["title_word_count"] == 3
    assert bool(us_row["title_has_question_mark"]) is True
    assert bool(us_row["title_has_exclamation_mark"]) is True
    assert bool(us_row["title_has_digits"]) is True
    assert bool(us_row["description_has_links"]) is True
    assert isclose(us_row["avg_tag_length_chars"], 4.5)

    assert jp_row["description_char_count"] == 0
    assert jp_row["description_word_count"] == 0
    assert jp_row["tags_char_count"] == 0
    assert isclose(jp_row["avg_tag_length_chars"], 0.0)


def test_build_video_country_features_adds_safe_engagement_features() -> None:
    features = build_video_country_features(_build_snapshot_frame())
    us_row = features.loc[(features["country"] == "US") & (features["video_id"] == "video-a")].iloc[0]
    jp_row = features.loc[(features["country"] == "JP") & (features["video_id"] == "video-b")].iloc[0]

    assert us_row["first_trending_engagement_total"] == 17
    assert isclose(us_row["like_rate_vs_first_trending_views"], 0.10)
    assert isclose(us_row["comment_rate_vs_first_trending_views"], 0.05)
    assert isclose(us_row["engagement_rate_vs_first_trending_views"], 0.17)
    assert isclose(us_row["log1p_first_trending_views"], log1p(100))

    assert pd.isna(jp_row["like_rate_vs_first_trending_views"])
    assert pd.isna(jp_row["engagement_rate_vs_first_trending_views"])


def test_write_video_country_features_persists_output(tmp_path: Path) -> None:
    input_path = tmp_path / "video_country_snapshot.parquet"
    output_path = tmp_path / "video_country_features.parquet"
    _build_snapshot_frame().to_parquet(input_path, index=False)

    written = write_video_country_features(str(input_path), str(output_path))

    assert output_path.exists()
    reloaded = pd.read_parquet(output_path)
    assert len(written) == 2
    assert len(reloaded) == 2
    assert {
        "publish_hour_utc",
        "title_char_count",
        "avg_tag_length_chars",
        "engagement_rate_vs_first_trending_views",
    }.issubset(reloaded.columns)