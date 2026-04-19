from __future__ import annotations

from pathlib import Path

DEFAULT_INPUT_GLOB = "data/*.csv"
DEFAULT_OUTPUT_PATH = "data/processed/trending_rows.parquet"
DEFAULT_MANIFEST_PATH = "data/processed/source_manifest.csv"


def discover_country_files(data_glob: str = DEFAULT_INPUT_GLOB):
    raise NotImplementedError


def parse_trending_date(value: str):
    raise NotImplementedError


def normalize_bool(value):
    raise NotImplementedError


def normalize_placeholder_text(value, placeholder: str = "[none]"):
    raise NotImplementedError


def build_trending_rows(
    input_glob: str = DEFAULT_INPUT_GLOB,
    output_path: str = DEFAULT_OUTPUT_PATH,
):
    raise NotImplementedError


def main() -> None:
    build_trending_rows()


if __name__ == "__main__":
    main()
