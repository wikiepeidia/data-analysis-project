from __future__ import annotations

from pathlib import Path

DEFAULT_INPUT_PATH = "data/processed/trending_rows.parquet"
DEFAULT_OUTPUT_PATH = "data/processed/video_country_snapshot.parquet"


def build_video_country_snapshot(rows_df):
    raise NotImplementedError


def write_video_country_snapshot(
    input_path: str = DEFAULT_INPUT_PATH,
    output_path: str = DEFAULT_OUTPUT_PATH,
):
    raise NotImplementedError


def main() -> None:
    write_video_country_snapshot()


if __name__ == "__main__":
    main()
