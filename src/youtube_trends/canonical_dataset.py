from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
from typing import Any

DEFAULT_INPUT_GLOB = "data/*.csv"
DEFAULT_OUTPUT_PATH = "data/processed/trending_rows.parquet"
DEFAULT_MANIFEST_PATH = "data/processed/source_manifest.csv"
EXPECTED_SOURCE_COLUMNS = [
    "video_id",
    "trending_date",
    "title",
    "channel_title",
    "category_id",
    "publish_time",
    "tags",
    "views",
    "likes",
    "dislikes",
    "comment_count",
    "thumbnail_link",
    "comments_disabled",
    "ratings_disabled",
    "video_error_or_removed",
    "description",
]
_COUNTRY_FILE_PATTERN = re.compile(r"^(?P<country>[A-Za-z]{2})videos\.csv$")


def discover_country_files(data_glob: str = DEFAULT_INPUT_GLOB) -> list[dict[str, str]]:
    discovered: list[dict[str, str]] = []
    for file_path in sorted(Path().glob(data_glob)):
        match = _COUNTRY_FILE_PATTERN.match(file_path.name)
        if not match:
            continue
        discovered.append(
            {
                "country": match.group("country").upper(),
                "source_file": str(file_path),
            }
        )
    discovered.sort(key=lambda entry: entry["country"])
    return discovered


def parse_trending_date(value: str):
    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError("trending_date cannot be blank")
    return datetime.strptime(cleaned, "%y.%d.%m").date()


def normalize_bool(value: Any):
    if value is None:
        return None
    if isinstance(value, bool):
        return value

    cleaned = str(value).strip().lower()
    if cleaned in {"", "nan", "none", "null"}:
        return None
    if cleaned == "true":
        return True
    if cleaned == "false":
        return False
    raise ValueError(f"Unsupported boolean value: {value!r}")


def normalize_placeholder_text(value: Any, placeholder: str = "[none]") -> dict[str, Any]:
    raw = value
    if value is None:
        return {"raw": raw, "normalized": None, "is_missing": True}

    text = str(value)
    collapsed = " ".join(text.split())
    lowered = collapsed.casefold()
    if lowered in {"", placeholder.casefold(), "nan", "none", "null"}:
        return {"raw": raw, "normalized": None, "is_missing": True}
    return {"raw": raw, "normalized": collapsed, "is_missing": False}


def build_trending_rows(
    input_glob: str = DEFAULT_INPUT_GLOB,
    output_path: str = DEFAULT_OUTPUT_PATH,
):
    raise NotImplementedError("Task 2 implements the canonical row-level dataset builder")


def main() -> None:
    build_trending_rows()


if __name__ == "__main__":
    main()
