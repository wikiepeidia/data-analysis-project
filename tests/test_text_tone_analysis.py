from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from youtube_trends.text_tone_analysis import (
    TONE_COUNTRY_SUMMARY_FILENAME,
    TONE_CROSS_COUNTRY_SUMMARY_FILENAME,
    TONE_FRAME_FILENAME,
    build_multilingual_text_tone_frame,
    build_tone_country_summary,
    write_text_tone_artifacts,
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
                "tag_count": 3,
                "title_word_count": 6,
                "description_normalized": "How did this happen? Watch now",
                "tags_normalized": "music|live|show",
                "description_has_links": False,
                "tags_is_missing": False,
            },
            {
                "country": "US",
                "video_id": "video-b",
                "category_id": 20,
                "trend_days_in_country_proxy": 1,
                "log1p_first_trending_views": 3.0,
                "engagement_rate_vs_first_trending_views": 0.05,
                "publish_weekday_name_utc": "Tuesday",
                "publish_hour_utc": 20,
                "description_is_missing": True,
                "tag_count": 0,
                "title_word_count": 3,
                "description_normalized": None,
                "tags_normalized": None,
                "description_has_links": False,
                "tags_is_missing": True,
            },
            {
                "country": "JP",
                "video_id": "video-c",
                "category_id": 15,
                "trend_days_in_country_proxy": 4,
                "log1p_first_trending_views": 6.0,
                "engagement_rate_vs_first_trending_views": 0.12,
                "publish_weekday_name_utc": "Friday",
                "publish_hour_utc": 11,
                "description_is_missing": False,
                "tag_count": 9,
                "title_word_count": 8,
                "description_normalized": "Ã¥Ð½Ã© ìë",
                "tags_normalized": "Ã©|Ðº|ìì",
                "description_has_links": False,
                "tags_is_missing": False,
            },
            {
                "country": "MX",
                "video_id": "video-d",
                "category_id": 10,
                "trend_days_in_country_proxy": 2,
                "log1p_first_trending_views": 4.0,
                "engagement_rate_vs_first_trending_views": 0.08,
                "publish_weekday_name_utc": "Saturday",
                "publish_hour_utc": 14,
                "description_is_missing": False,
                "tag_count": 4,
                "title_word_count": 7,
                "description_normalized": "Nuevo video oficial estreno visita https://canal.example comparte y comenta ya",
                "tags_normalized": "musica|estreno|🔥|viral",
                "description_has_links": True,
                "tags_is_missing": False,
            },
        ]
    )


def test_build_multilingual_text_tone_frame_adds_quality_and_script_features() -> None:
    tone_df = build_multilingual_text_tone_frame(_build_feature_frame())

    us_row = tone_df.loc[(tone_df["country"] == "US") & (tone_df["video_id"] == "video-a")].iloc[0]
    jp_row = tone_df.loc[(tone_df["country"] == "JP") & (tone_df["video_id"] == "video-c")].iloc[0]
    mx_row = tone_df.loc[(tone_df["country"] == "MX") & (tone_df["video_id"] == "video-d")].iloc[0]

    assert us_row["description_text_quality"] == "ascii_or_plain_latin"
    assert us_row["description_script_family"] == "latin"
    assert us_row["description_tone_bucket"] == "question_led"
    assert us_row["tag_tone_bucket"] == "plain_keywords"

    assert jp_row["description_text_quality"] == "likely_mojibake"
    assert jp_row["description_tone_bucket"] == "corrupted_or_unreadable"
    assert jp_row["tag_text_quality"] == "likely_mojibake"
    assert jp_row["tag_tone_bucket"] == "corrupted_or_unreadable"

    assert mx_row["description_tone_bucket"] == "link_heavy"
    assert bool(mx_row["tag_has_emoji"]) is True
    assert mx_row["tag_tone_bucket"] == "symbolic_or_emphatic"


def test_build_tone_country_summary_separates_description_and_tag_dimensions() -> None:
    tone_df = build_multilingual_text_tone_frame(_build_feature_frame())
    country_summary = build_tone_country_summary(tone_df)

    assert {"description", "tags"} == set(country_summary["analysis_family"])

    us_description = country_summary.loc[
        (country_summary["country"] == "US")
        & (country_summary["analysis_dimension"] == "description_tone_bucket")
        & (country_summary["dimension_value"] == "question_led")
    ].iloc[0]
    mx_tags = country_summary.loc[
        (country_summary["country"] == "MX")
        & (country_summary["analysis_dimension"] == "tag_tone_bucket")
        & (country_summary["dimension_value"] == "symbolic_or_emphatic")
    ].iloc[0]

    assert us_description["video_count"] == 1
    assert us_description["share_within_country"] == 0.5
    assert mx_tags["video_count"] == 1
    assert mx_tags["share_within_country"] == 1.0


def test_write_text_tone_artifacts_persists_expected_outputs(tmp_path: Path) -> None:
    input_path = tmp_path / "video_country_features.parquet"
    output_dir = tmp_path / "phase4_analysis"
    checkpoint_path = tmp_path / "04_multilingual_text_tone_analysis.md"
    _build_feature_frame().to_parquet(input_path, index=False)

    outputs = write_text_tone_artifacts(
        input_path=str(input_path),
        output_dir=str(output_dir),
        checkpoint_path=str(checkpoint_path),
    )

    assert (output_dir / TONE_FRAME_FILENAME).exists()
    assert (output_dir / TONE_COUNTRY_SUMMARY_FILENAME).exists()
    assert (output_dir / TONE_CROSS_COUNTRY_SUMMARY_FILENAME).exists()
    assert checkpoint_path.exists()
    assert not outputs["tone_cross_country_summary"].empty