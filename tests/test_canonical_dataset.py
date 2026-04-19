from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from youtube_trends.canonical_dataset import (
    discover_country_files,
    normalize_bool,
    normalize_placeholder_text,
    parse_trending_date,
)


def test_parse_trending_date_yy_dd_mm() -> None:
    assert parse_trending_date("17.14.11") == date(2017, 11, 14)


def test_normalize_bool_case_insensitive() -> None:
    assert normalize_bool("TRUE") is True
    assert normalize_bool("True") is True
    assert normalize_bool("FALSE") is False
    assert normalize_bool("False") is False


def test_placeholder_text_sets_missing_flags() -> None:
    placeholder = normalize_placeholder_text("[none]")
    blank = normalize_placeholder_text("   ")
    regular = normalize_placeholder_text("  hello\nworld  ")

    assert placeholder["raw"] == "[none]"
    assert placeholder["normalized"] is None
    assert placeholder["is_missing"] is True

    assert blank["raw"] == "   "
    assert blank["normalized"] is None
    assert blank["is_missing"] is True

    assert regular["raw"] == "  hello\nworld  "
    assert regular["normalized"] == "hello world"
    assert regular["is_missing"] is False


def test_all_country_files_are_discovered() -> None:
    discovered = discover_country_files()

    assert [entry["country"] for entry in discovered] == [
        "CA",
        "DE",
        "FR",
        "GB",
        "IN",
        "JP",
        "KR",
        "MX",
        "RU",
        "US",
    ]
    assert len(discovered) == 10
    assert all(Path(entry["source_file"]).name.endswith("videos.csv") for entry in discovered)
