from __future__ import annotations

from datetime import date, datetime
from glob import glob
from pathlib import Path
import re
from typing import Any

import pandas as pd

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
NUMERIC_COLUMNS = ["category_id", "views", "likes", "dislikes", "comment_count"]
BOOLEAN_COLUMNS = ["comments_disabled", "ratings_disabled", "video_error_or_removed"]
SOURCE_ENCODINGS = ["utf-8", "utf-8-sig", "latin-1"]
_COUNTRY_FILE_PATTERN = re.compile(r"^(?P<country>[A-Za-z]{2})videos\.csv$")


def discover_country_files(data_glob: str = DEFAULT_INPUT_GLOB) -> list[dict[str, str]]:
    discovered: list[dict[str, str]] = []
    for source_name in sorted(glob(data_glob)):
        file_path = Path(source_name)
        match = _COUNTRY_FILE_PATTERN.match(file_path.name)
        if not match:
            continue
        discovered.append(
            {
                "country": match.group("country").upper(),
                "source_file": str(file_path),
            }
        )
    discovered.sort(key=lambda entry: (entry["country"], entry["source_file"]))
    return discovered


def parse_trending_date(value: str) -> date:
    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError("trending_date cannot be blank")
    return datetime.strptime(cleaned, "%y.%d.%m").date()


def normalize_bool(value: Any) -> bool | None:
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
    raise ValueError("Unsupported boolean value: %r" % (value,))


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


def parse_tags(value: Any) -> list[str]:
    helper = normalize_placeholder_text(value)
    if helper["is_missing"]:
        return []

    parsed_tags: list[str] = []
    for raw_tag in str(value).split("|"):
        cleaned_tag = raw_tag.strip().strip('"').strip()
        if cleaned_tag:
            parsed_tags.append(cleaned_tag)
    return parsed_tags


def _validate_source_columns(frame: pd.DataFrame, source_file: str) -> None:
    actual_columns = list(frame.columns)
    if actual_columns != EXPECTED_SOURCE_COLUMNS:
        raise ValueError(
            "%s does not match the expected 16-column schema: %s" % (source_file, actual_columns)
        )


def _resolve_manifest_path(output_path: str | Path) -> Path:
    output = Path(output_path)
    if output == Path(DEFAULT_OUTPUT_PATH):
        return Path(DEFAULT_MANIFEST_PATH)
    return output.with_name("source_manifest.csv")


def _read_source_frame(source_file: str) -> tuple[pd.DataFrame, str]:
    last_error: UnicodeDecodeError | None = None
    for encoding in SOURCE_ENCODINGS:
        try:
            frame = pd.read_csv(
                source_file,
                keep_default_na=False,
                low_memory=False,
                encoding=encoding,
            )
            return frame, encoding
        except UnicodeDecodeError as error:
            last_error = error
    if last_error is not None:
        raise last_error
    raise ValueError("Could not read %s with the supported encodings" % (source_file,))


def _apply_text_helpers(frame: pd.DataFrame) -> pd.DataFrame:
    title_helpers = frame["title"].map(normalize_placeholder_text)
    tags_helpers = frame["tags"].map(normalize_placeholder_text)
    description_helpers = frame["description"].map(normalize_placeholder_text)

    frame["title_normalized"] = title_helpers.map(lambda item: item["normalized"])
    frame["tags_normalized"] = tags_helpers.map(lambda item: item["normalized"])
    frame["description_normalized"] = description_helpers.map(lambda item: item["normalized"])
    frame["tags_is_missing"] = tags_helpers.map(lambda item: item["is_missing"]).astype("boolean")
    frame["description_is_missing"] = description_helpers.map(lambda item: item["is_missing"]).astype("boolean")
    frame["tags_list"] = frame["tags"].map(parse_tags)
    frame["tag_count"] = frame["tags_list"].map(len).astype("int64")
    return frame


def build_trending_rows(
    input_glob: str = DEFAULT_INPUT_GLOB,
    output_path: str = DEFAULT_OUTPUT_PATH,
) -> pd.DataFrame:
    country_files = discover_country_files(input_glob)
    if not country_files:
        raise FileNotFoundError("No source files matched %r" % (input_glob,))

    normalized_frames: list[pd.DataFrame] = []
    manifest_rows: list[dict[str, Any]] = []

    for source in country_files:
        source_file = source["source_file"]
        country = source["country"]
        frame, source_encoding = _read_source_frame(source_file)
        _validate_source_columns(frame, source_file)

        manifest_rows.append(
            {
                "country": country,
                "source_file": source_file,
                "row_count": len(frame),
                "encoding": source_encoding,
            }
        )

        frame["country"] = country
        frame["source_file"] = source_file
        frame["source_encoding"] = source_encoding
        frame["trending_date_local"] = frame["trending_date"].map(parse_trending_date)
        frame["publish_time_raw"] = frame["publish_time"]
        frame["publish_time"] = pd.to_datetime(frame["publish_time"], utc=True, errors="raise")

        for column in NUMERIC_COLUMNS:
            frame[column] = pd.to_numeric(frame[column], errors="raise")

        for column in BOOLEAN_COLUMNS:
            frame[f"{column}_raw"] = frame[column]
            frame[column] = frame[column].map(normalize_bool).astype("boolean")

        frame = _apply_text_helpers(frame)
        normalized_frames.append(frame)

    combined = pd.concat(normalized_frames, ignore_index=True)
    output = Path(output_path)
    manifest_output = _resolve_manifest_path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest_output.parent.mkdir(parents=True, exist_ok=True)

    combined.to_parquet(output, index=False)
    pd.DataFrame(manifest_rows).to_csv(manifest_output, index=False)
    return combined


def main() -> None:
    build_trending_rows()


if __name__ == "__main__":
    main()
