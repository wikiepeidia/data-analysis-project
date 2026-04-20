from __future__ import annotations

from math import log1p
from pathlib import Path
from typing import Any

import pandas as pd

DEFAULT_INPUT_PATH = "data/processed/video_country_snapshot.parquet"
DEFAULT_OUTPUT_PATH = "data/processed/video_country_features.parquet"
REQUIRED_COLUMNS = {
    "country",
    "video_id",
    "publish_time",
    "first_trending_date_local",
    "last_trending_date_local",
    "publish_to_first_trend_days",
    "trend_days_in_country_proxy",
    "title",
    "title_normalized",
    "tags",
    "tags_normalized",
    "description",
    "description_normalized",
    "tags_is_missing",
    "description_is_missing",
    "tags_list",
    "tag_count",
    "first_trending_views",
    "first_trending_likes",
    "first_trending_dislikes",
    "first_trending_comment_count",
}
QUESTION_MARKS = {"?"}
EXCLAMATION_MARKS = {"!"}


def _normalize_feature_inputs(snapshot_df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = REQUIRED_COLUMNS.difference(snapshot_df.columns)
    if missing_columns:
        raise ValueError("Missing required columns: %s" % sorted(missing_columns))

    normalized = snapshot_df.copy()
    normalized["publish_time"] = pd.to_datetime(normalized["publish_time"], utc=True, errors="raise")
    normalized["first_trending_date_local"] = pd.to_datetime(
        normalized["first_trending_date_local"],
        errors="raise",
    ).dt.date
    normalized["last_trending_date_local"] = pd.to_datetime(
        normalized["last_trending_date_local"],
        errors="raise",
    ).dt.date
    normalized["publish_to_first_trend_days"] = pd.to_numeric(
        normalized["publish_to_first_trend_days"],
        errors="raise",
    ).astype("int64")
    normalized["trend_days_in_country_proxy"] = pd.to_numeric(
        normalized["trend_days_in_country_proxy"],
        errors="raise",
    ).astype("int64")

    for column in [
        "tag_count",
        "first_trending_views",
        "first_trending_likes",
        "first_trending_dislikes",
        "first_trending_comment_count",
    ]:
        normalized[column] = pd.to_numeric(normalized[column], errors="raise").astype("int64")

    return normalized


def _is_missing_scalar(value: Any) -> bool:
    return value is None or value is pd.NA or (isinstance(value, float) and pd.isna(value))


def _clean_text(value: Any) -> str:
    if _is_missing_scalar(value):
        return ""
    return " ".join(str(value).split())


def _count_words(value: Any) -> int:
    text = _clean_text(value)
    if not text:
        return 0
    return len(text.split())


def _contains_any(value: Any, chars: set[str]) -> bool:
    text = _clean_text(value)
    return any(character in text for character in chars)


def _has_digits(value: Any) -> bool:
    text = _clean_text(value)
    return any(character.isdigit() for character in text)


def _contains_url(value: Any) -> bool:
    text = _clean_text(value).lower()
    return any(token in text for token in ("http://", "https://", "www."))


def _average_tag_length(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, list):
        tags = value
    else:
        tags = list(value)

    cleaned = [str(tag).strip() for tag in tags if str(tag).strip()]
    if not cleaned:
        return 0.0
    return sum(len(tag) for tag in cleaned) / len(cleaned)


def _safe_ratio(numerator: Any, denominator: Any) -> float:
    if _is_missing_scalar(numerator) or _is_missing_scalar(denominator):
        return float("nan")

    denominator_value = float(denominator)
    if denominator_value == 0.0:
        return float("nan")
    return float(numerator) / denominator_value


def _safe_log1p(value: Any) -> float:
    if _is_missing_scalar(value):
        return float("nan")
    return log1p(float(value))


def build_video_country_features(snapshot_df: pd.DataFrame) -> pd.DataFrame:
    features = _normalize_feature_inputs(snapshot_df)

    publish_time = features["publish_time"]
    first_trending = pd.to_datetime(features["first_trending_date_local"], errors="raise")
    last_trending = pd.to_datetime(features["last_trending_date_local"], errors="raise")

    features["publish_date_utc"] = publish_time.dt.date
    features["publish_hour_utc"] = publish_time.dt.hour.astype("int64")
    features["publish_weekday_utc"] = publish_time.dt.weekday.astype("int64")
    features["publish_weekday_name_utc"] = publish_time.dt.day_name()
    features["publish_month_utc"] = publish_time.dt.month.astype("int64")
    features["publish_quarter_utc"] = publish_time.dt.quarter.astype("int64")
    features["publish_is_weekend_utc"] = publish_time.dt.weekday.isin([5, 6]).astype("boolean")
    features["first_trending_weekday_local"] = first_trending.dt.weekday.astype("int64")
    features["first_trending_weekday_name_local"] = first_trending.dt.day_name()
    features["trend_span_days_observed"] = (last_trending - first_trending).dt.days.astype("int64")

    features["title_char_count"] = features["title_normalized"].map(lambda value: len(_clean_text(value))).astype("int64")
    features["title_word_count"] = features["title_normalized"].map(_count_words).astype("int64")
    features["title_has_question_mark"] = features["title"].map(lambda value: _contains_any(value, QUESTION_MARKS)).astype("boolean")
    features["title_has_exclamation_mark"] = features["title"].map(lambda value: _contains_any(value, EXCLAMATION_MARKS)).astype("boolean")
    features["title_has_digits"] = features["title"].map(_has_digits).astype("boolean")
    features["description_char_count"] = features["description_normalized"].map(lambda value: len(_clean_text(value))).astype("int64")
    features["description_word_count"] = features["description_normalized"].map(_count_words).astype("int64")
    features["description_has_links"] = features["description_normalized"].map(_contains_url).astype("boolean")
    features["tags_char_count"] = features["tags_normalized"].map(lambda value: len(_clean_text(value))).astype("int64")
    features["avg_tag_length_chars"] = features["tags_list"].map(_average_tag_length).astype("float64")

    features["first_trending_engagement_total"] = (
        features["first_trending_likes"]
        + features["first_trending_dislikes"]
        + features["first_trending_comment_count"]
    ).astype("int64")
    features["like_rate_vs_first_trending_views"] = [
        _safe_ratio(likes, views)
        for likes, views in zip(features["first_trending_likes"], features["first_trending_views"], strict=False)
    ]
    features["dislike_rate_vs_first_trending_views"] = [
        _safe_ratio(dislikes, views)
        for dislikes, views in zip(features["first_trending_dislikes"], features["first_trending_views"], strict=False)
    ]
    features["comment_rate_vs_first_trending_views"] = [
        _safe_ratio(comment_count, views)
        for comment_count, views in zip(
            features["first_trending_comment_count"],
            features["first_trending_views"],
            strict=False,
        )
    ]
    features["engagement_rate_vs_first_trending_views"] = [
        _safe_ratio(total, views)
        for total, views in zip(
            features["first_trending_engagement_total"],
            features["first_trending_views"],
            strict=False,
        )
    ]
    features["log1p_first_trending_views"] = features["first_trending_views"].map(_safe_log1p)
    features["log1p_first_trending_likes"] = features["first_trending_likes"].map(_safe_log1p)
    features["log1p_first_trending_comment_count"] = features["first_trending_comment_count"].map(_safe_log1p)

    return features.sort_values(["country", "video_id"]).reset_index(drop=True)


def write_video_country_features(
    input_path: str = DEFAULT_INPUT_PATH,
    output_path: str = DEFAULT_OUTPUT_PATH,
) -> pd.DataFrame:
    snapshot_df = pd.read_parquet(input_path)
    features = build_video_country_features(snapshot_df)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    features.to_parquet(output, index=False)
    return features


def main() -> None:
    write_video_country_features()


if __name__ == "__main__":
    main()