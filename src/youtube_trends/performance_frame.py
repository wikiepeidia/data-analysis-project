from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

DEFAULT_INPUT_PATH = "data/processed/trending_rows.parquet"
DEFAULT_OUTPUT_PATH = "data/processed/video_country_snapshot.parquet"
GROUP_KEY = ["country", "video_id"]
REQUIRED_COLUMNS = {
    "country",
    "video_id",
    "trending_date_local",
    "publish_time",
    "title",
    "channel_title",
    "category_id",
    "tags",
    "description",
    "views",
    "likes",
    "dislikes",
    "comment_count",
}


def _normalize_snapshot_inputs(rows_df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = REQUIRED_COLUMNS.difference(rows_df.columns)
    if missing_columns:
        raise ValueError("Missing required columns: %s" % sorted(missing_columns))

    normalized = rows_df.copy()
    normalized["trending_date_local"] = pd.to_datetime(normalized["trending_date_local"], errors="raise").dt.date
    normalized["publish_time"] = pd.to_datetime(normalized["publish_time"], utc=True, errors="raise")
    return normalized


def _build_anchor_rows(normalized_rows: pd.DataFrame) -> pd.DataFrame:
    sorted_rows = normalized_rows.sort_values(GROUP_KEY + ["trending_date_local", "publish_time"]).reset_index(drop=True)
    grouped = sorted_rows.groupby(GROUP_KEY, sort=True, dropna=False)

    anchor_rows = grouped.head(1).copy()
    anchor_rows["first_trending_date_local"] = anchor_rows["trending_date_local"]
    anchor_rows["first_trending_views"] = anchor_rows["views"].astype("int64")
    anchor_rows["first_trending_likes"] = anchor_rows["likes"].astype("int64")
    anchor_rows["first_trending_dislikes"] = anchor_rows["dislikes"].astype("int64")
    anchor_rows["first_trending_comment_count"] = anchor_rows["comment_count"].astype("int64")
    anchor_rows["publish_to_first_trend_days"] = [
        int((first_date - publish_time.date()).days)
        for first_date, publish_time in zip(
            anchor_rows["first_trending_date_local"],
            anchor_rows["publish_time"],
            strict=False,
        )
    ]

    summary = grouped.agg(
        last_trending_date_local=("trending_date_local", "max"),
        trend_days_in_country_proxy=("trending_date_local", "size"),
    ).reset_index()

    snapshot = anchor_rows.merge(summary, on=GROUP_KEY, how="left", validate="one_to_one")
    snapshot["trend_days_in_country_proxy"] = snapshot["trend_days_in_country_proxy"].astype("int64")
    snapshot = snapshot.sort_values(GROUP_KEY).reset_index(drop=True)
    return snapshot


def build_video_country_snapshot(rows_df: pd.DataFrame) -> pd.DataFrame:
    normalized_rows = _normalize_snapshot_inputs(rows_df)
    return _build_anchor_rows(normalized_rows)


def write_video_country_snapshot(
    input_path: str = DEFAULT_INPUT_PATH,
    output_path: str = DEFAULT_OUTPUT_PATH,
) -> pd.DataFrame:
    rows_df = pd.read_parquet(input_path)
    snapshot = build_video_country_snapshot(rows_df)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    snapshot.to_parquet(output, index=False)
    return snapshot


def main() -> None:
    write_video_country_snapshot()


if __name__ == "__main__":
    main()
