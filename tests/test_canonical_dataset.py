from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from youtube_trends.canonical_dataset import (
    EXPECTED_SOURCE_COLUMNS,
    build_trending_rows,
    discover_country_files,
    normalize_bool,
    normalize_placeholder_text,
    parse_trending_date,
)


def _build_source_row(
    *,
    video_id: str,
    trending_date: str,
    title: str,
    channel_title: str,
    category_id: int,
    publish_time: str,
    tags: str,
    views: int,
    likes: int,
    dislikes: int,
    comment_count: int,
    comments_disabled: str,
    ratings_disabled: str,
    video_error_or_removed: str,
    description: str,
) -> dict[str, object]:
    return {
        "video_id": video_id,
        "trending_date": trending_date,
        "title": title,
        "channel_title": channel_title,
        "category_id": category_id,
        "publish_time": publish_time,
        "tags": tags,
        "views": views,
        "likes": likes,
        "dislikes": dislikes,
        "comment_count": comment_count,
        "thumbnail_link": f"https://example.com/{video_id}.jpg",
        "comments_disabled": comments_disabled,
        "ratings_disabled": ratings_disabled,
        "video_error_or_removed": video_error_or_removed,
        "description": description,
    }


def _write_source_csv(path: Path, rows: list[dict[str, object]], encoding: str = "utf-8") -> None:
    frame = pd.DataFrame(rows, columns=EXPECTED_SOURCE_COLUMNS)
    frame.to_csv(path, index=False, encoding=encoding)


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


def test_build_trending_rows_writes_outputs_and_manifest(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_path = tmp_path / "processed" / "trending_rows.parquet"

    _write_source_csv(
        input_dir / "USvideos.csv",
        [
            _build_source_row(
                video_id="us-1",
                trending_date="17.14.11",
                title="  Hello   World  ",
                channel_title="US Channel",
                category_id=22,
                publish_time="2017-11-13T17:13:01.000Z",
                tags='"alpha"|"beta"',
                views=100,
                likes=10,
                dislikes=1,
                comment_count=2,
                comments_disabled="False",
                ratings_disabled="False",
                video_error_or_removed="False",
                description="  sample description  ",
            ),
            _build_source_row(
                video_id="us-2",
                trending_date="17.15.11",
                title="Another title",
                channel_title="US Channel",
                category_id=24,
                publish_time="2017-11-14T01:00:00.000Z",
                tags="[none]",
                views=200,
                likes=20,
                dislikes=2,
                comment_count=4,
                comments_disabled="TRUE",
                ratings_disabled="FALSE",
                video_error_or_removed="FALSE",
                description="",
            ),
        ],
    )
    _write_source_csv(
        input_dir / "JPvideos.csv",
        [
            _build_source_row(
                video_id="jp-1",
                trending_date="18.07.02",
                title="日本語 タイトル",
                channel_title="JP Channel",
                category_id=25,
                publish_time="2018-02-06T03:04:37.000Z",
                tags='事故|"佐賀"',
                views=300,
                likes=30,
                dislikes=3,
                comment_count=6,
                comments_disabled="FALSE",
                ratings_disabled="TRUE",
                video_error_or_removed="FALSE",
                description="  日本語 説明  ",
            )
        ],
    )

    built = build_trending_rows(str(input_dir / "*.csv"), str(output_path))
    manifest_path = output_path.with_name("source_manifest.csv")

    assert output_path.exists()
    assert manifest_path.exists()
    assert set(built["country"].unique().tolist()) == {"JP", "US"}
    assert len(built) == 3

    us_one = built.loc[built["video_id"] == "us-1"].iloc[0]
    us_two = built.loc[built["video_id"] == "us-2"].iloc[0]

    assert us_one["trending_date_local"] == date(2017, 11, 14)
    assert us_one["publish_time"].tzinfo is not None
    assert us_one["publish_time"].utcoffset().total_seconds() == 0
    assert us_one["title_normalized"] == "Hello World"
    assert us_one["tags_list"] == ["alpha", "beta"]
    assert us_one["tag_count"] == 2
    assert bool(us_one["comments_disabled"]) is False

    assert pd.isna(us_two["tags_normalized"])
    assert bool(us_two["tags_is_missing"]) is True
    assert bool(us_two["description_is_missing"]) is True
    assert bool(us_two["comments_disabled"]) is True

    manifest = pd.read_csv(manifest_path)
    assert set(manifest.columns) >= {"country", "source_file", "row_count", "encoding"}
    assert manifest.set_index("country")["row_count"].to_dict() == {"JP": 1, "US": 2}
    assert manifest.set_index("country")["encoding"].to_dict() == {"JP": "utf-8", "US": "utf-8"}

    reloaded = pd.read_parquet(output_path)
    assert {"country", "trending_date_local", "publish_time", "tags_list", "tag_count"}.issubset(reloaded.columns)
    assert len(reloaded) == 3


def test_build_trending_rows_falls_back_to_latin1(tmp_path: Path) -> None:
    input_dir = tmp_path / "latin1"
    input_dir.mkdir()
    output_path = tmp_path / "latin1_processed" / "trending_rows.parquet"

    _write_source_csv(
        input_dir / "MXvideos.csv",
        [
            _build_source_row(
                video_id="mx-1",
                trending_date="18.07.02",
                title="Olé título",
                channel_title="Canal Niño",
                category_id=10,
                publish_time="2018-02-06T03:04:37.000Z",
                tags='"canción"|"niño"',
                views=50,
                likes=5,
                dislikes=0,
                comment_count=1,
                comments_disabled="FALSE",
                ratings_disabled="FALSE",
                video_error_or_removed="FALSE",
                description=" canción útil ",
            )
        ],
        encoding="latin-1",
    )

    built = build_trending_rows(str(input_dir / "*.csv"), str(output_path))
    manifest = pd.read_csv(output_path.with_name("source_manifest.csv"))

    assert built.loc[0, "title_normalized"] == "Olé título"
    assert built.loc[0, "description_normalized"] == "canción útil"
    assert manifest.loc[0, "encoding"] == "latin-1"


def test_build_trending_rows_rejects_schema_drift(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    bad_frame = pd.DataFrame(
        [
            {
                "video_id": "broken-1",
                "trending_date": "17.14.11",
                "title": "Bad row",
            }
        ]
    )
    bad_frame.to_csv(input_dir / "USvideos.csv", index=False)

    with pytest.raises(ValueError, match="expected 16-column schema"):
        build_trending_rows(str(input_dir / "*.csv"), str(tmp_path / "processed" / "trending_rows.parquet"))
