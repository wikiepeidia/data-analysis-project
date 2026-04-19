from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from youtube_trends.performance_frame import build_video_country_snapshot


def _build_rows_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "country": "US",
                "video_id": "video-a",
                "trending_date_local": date(2017, 11, 14),
                "publish_time": pd.Timestamp("2017-11-13T10:00:00Z"),
                "title": "Anchor title",
                "channel_title": "Channel A",
                "category_id": 22,
                "tags": '"alpha"|"beta"',
                "description": "Anchor description",
                "views": 100,
                "likes": 10,
                "dislikes": 1,
                "comment_count": 2,
            },
            {
                "country": "US",
                "video_id": "video-a",
                "trending_date_local": date(2017, 11, 15),
                "publish_time": pd.Timestamp("2017-11-13T10:00:00Z"),
                "title": "Later title",
                "channel_title": "Channel A",
                "category_id": 99,
                "tags": '"gamma"',
                "description": "Later description",
                "views": 150,
                "likes": 12,
                "dislikes": 2,
                "comment_count": 5,
            },
            {
                "country": "CA",
                "video_id": "video-a",
                "trending_date_local": date(2017, 11, 14),
                "publish_time": pd.Timestamp("2017-11-13T10:00:00Z"),
                "title": "Canada anchor",
                "channel_title": "Channel A",
                "category_id": 22,
                "tags": '"north"',
                "description": "Canada description",
                "views": 80,
                "likes": 8,
                "dislikes": 0,
                "comment_count": 1,
            },
            {
                "country": "US",
                "video_id": "video-b",
                "trending_date_local": date(2017, 11, 16),
                "publish_time": pd.Timestamp("2017-11-10T02:00:00Z"),
                "title": "Video B",
                "channel_title": "Channel B",
                "category_id": 24,
                "tags": '"delta"',
                "description": "Video B description",
                "views": 70,
                "likes": 7,
                "dislikes": 0,
                "comment_count": 3,
            },
        ]
    )


def test_first_trending_snapshot_is_anchor() -> None:
    snapshot = build_video_country_snapshot(_build_rows_frame())
    us_video_a = snapshot.loc[(snapshot["country"] == "US") & (snapshot["video_id"] == "video-a")].iloc[0]

    assert us_video_a["title"] == "Anchor title"
    assert us_video_a["category_id"] == 22
    assert us_video_a["first_trending_date_local"] == date(2017, 11, 14)
    assert us_video_a["last_trending_date_local"] == date(2017, 11, 15)
    assert us_video_a["first_trending_views"] == 100


def test_trend_days_proxy_counts_rows_per_country_video() -> None:
    snapshot = build_video_country_snapshot(_build_rows_frame())
    us_video_a = snapshot.loc[(snapshot["country"] == "US") & (snapshot["video_id"] == "video-a")].iloc[0]
    ca_video_a = snapshot.loc[(snapshot["country"] == "CA") & (snapshot["video_id"] == "video-a")].iloc[0]

    assert us_video_a["trend_days_in_country_proxy"] == 2
    assert ca_video_a["trend_days_in_country_proxy"] == 1


def test_publish_to_first_trend_days_is_integer_days() -> None:
    snapshot = build_video_country_snapshot(_build_rows_frame())
    us_video_a = snapshot.loc[(snapshot["country"] == "US") & (snapshot["video_id"] == "video-a")].iloc[0]
    us_video_b = snapshot.loc[(snapshot["country"] == "US") & (snapshot["video_id"] == "video-b")].iloc[0]

    assert us_video_a["publish_to_first_trend_days"] == 1
    assert isinstance(us_video_a["publish_to_first_trend_days"], int)
    assert us_video_b["publish_to_first_trend_days"] == 6


def test_videos_are_not_collapsed_across_countries() -> None:
    snapshot = build_video_country_snapshot(_build_rows_frame())

    assert len(snapshot) == 3
    assert snapshot.loc[snapshot["video_id"] == "video-a", "country"].tolist() == ["CA", "US"]
