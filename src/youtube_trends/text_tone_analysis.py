from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any
import unicodedata

import pandas as pd

from youtube_trends.comparative_analysis import build_country_normalized_frame

DEFAULT_INPUT_PATH = "data/processed/video_country_features.parquet"
DEFAULT_OUTPUT_DIR = "data/processed/phase4_analysis"
DEFAULT_CHECKPOINT_PATH = "checkpoints/04_multilingual_text_tone_analysis.md"

TONE_FRAME_FILENAME = "multilingual_text_tone_frame.parquet"
TONE_COUNTRY_SUMMARY_FILENAME = "text_tone_country_summary.parquet"
TONE_CROSS_COUNTRY_SUMMARY_FILENAME = "text_tone_cross_country_summary.parquet"

REQUIRED_TEXT_COLUMNS = {
    "description_normalized",
    "tags_normalized",
    "description_has_links",
    "tags_is_missing",
}
MOJIBAKE_MARKERS = ("Ã", "Ð", "Ñ", "ì", "ã", "â")
EMOJI_RANGES = (
    (0x2600, 0x27BF),
    (0x1F300, 0x1FAFF),
)

TEXT_DIMENSION_SPECS = [
    ("description", "description_tone_bucket"),
    ("description", "description_text_quality"),
    ("description", "description_script_family"),
    ("tags", "tag_tone_bucket"),
    ("tags", "tag_text_quality"),
    ("tags", "tag_script_family"),
]


def _is_missing_scalar(value: Any) -> bool:
    if value is None or value is pd.NA:
        return True
    if isinstance(value, (list, tuple, dict, set)):
        return False
    try:
        return bool(pd.isna(value))
    except TypeError:
        return False


def _clean_text(value: Any) -> str:
    if _is_missing_scalar(value):
        return ""
    return " ".join(str(value).split())


def _count_words(value: Any) -> int:
    text = _clean_text(value)
    if not text:
        return 0
    return len(text.split())


def _count_marks(value: Any, marks: str) -> int:
    text = _clean_text(value)
    return sum(text.count(mark) for mark in marks)


def _has_emoji(value: Any) -> bool:
    text = _clean_text(value)
    for character in text:
        codepoint = ord(character)
        if any(start <= codepoint <= end for start, end in EMOJI_RANGES):
            return True
    return False


def _mojibake_marker_count(value: Any) -> int:
    text = _clean_text(value)
    return sum(text.count(marker) for marker in MOJIBAKE_MARKERS)


def _non_ascii_count(value: Any) -> int:
    text = _clean_text(value)
    return sum(ord(character) > 127 for character in text)


def _classify_text_quality(value: Any) -> str:
    text = _clean_text(value)
    if not text:
        return "missing"

    marker_count = _mojibake_marker_count(text)
    non_ascii_count = _non_ascii_count(text)
    if marker_count >= 2 and non_ascii_count >= marker_count:
        return "likely_mojibake"
    if non_ascii_count == 0:
        return "ascii_or_plain_latin"
    return "readable_multilingual"


def _script_group(character: str) -> str | None:
    if not character.isalpha():
        return None

    unicode_name = unicodedata.name(character, "")
    if "LATIN" in unicode_name:
        return "latin"
    if "CYRILLIC" in unicode_name:
        return "cyrillic"
    if any(token in unicode_name for token in ("CJK", "HIRAGANA", "KATAKANA", "HANGUL")):
        return "east_asian"
    return "other"


def _dominant_script_family(value: Any) -> str:
    text = _clean_text(value)
    if not text:
        return "missing"

    counts = Counter(
        script_group
        for character in text
        if (script_group := _script_group(character)) is not None
    )
    if not counts:
        return "symbolic_or_numeric"

    dominant_label, dominant_count = counts.most_common(1)[0]
    total_letters = sum(counts.values())
    if dominant_label != "other" and dominant_count / total_letters >= 0.6:
        return dominant_label
    return "mixed_or_other"


def _description_tone_bucket(value: Any, is_missing: Any, has_links: Any) -> str:
    if bool(is_missing):
        return "missing"

    quality = _classify_text_quality(value)
    if quality == "likely_mojibake":
        return "corrupted_or_unreadable"

    if bool(has_links) and _count_words(value) >= 6:
        return "link_heavy"
    if _count_marks(value, "!") > 0 or _has_emoji(value):
        return "emphatic"
    if _count_marks(value, "?") > 0:
        return "question_led"
    return "plain_or_informational"


def _tag_tone_bucket(value: Any, is_missing: Any, tag_count: Any) -> str:
    if bool(is_missing):
        return "missing"

    quality = _classify_text_quality(value)
    if quality == "likely_mojibake":
        return "corrupted_or_unreadable"

    text = _clean_text(value)
    if _has_emoji(text) or any(marker in text for marker in "#!?"):
        return "symbolic_or_emphatic"
    if int(tag_count) >= 8:
        return "dense_keywords"
    return "plain_keywords"


def _build_dimension_country_summary(
    tone_df: pd.DataFrame,
    analysis_family: str,
    source_column: str,
) -> pd.DataFrame:
    country_sizes = tone_df.groupby("country").size()
    summary = (
        tone_df.groupby(["country", source_column], observed=True, dropna=False)
        .agg(
            video_count=("video_id", "size"),
            median_trend_days_in_country_proxy=("trend_days_in_country_proxy", "median"),
            median_proxy_percentile_within_country=("proxy_percentile_within_country", "median"),
            median_log_views_percentile_within_country=("log_views_percentile_within_country", "median"),
            median_engagement_percentile_within_country=(
                "engagement_rate_percentile_within_country",
                "median",
            ),
        )
        .reset_index()
        .rename(columns={source_column: "dimension_value"})
    )
    summary["country"] = summary["country"].astype("string")
    summary["dimension_value"] = summary["dimension_value"].astype("string")
    summary["share_within_country"] = summary["video_count"] / summary["country"].map(country_sizes)
    summary["analysis_family"] = analysis_family
    summary["analysis_dimension"] = source_column

    columns = [
        "country",
        "analysis_family",
        "analysis_dimension",
        "dimension_value",
        "video_count",
        "share_within_country",
        "median_trend_days_in_country_proxy",
        "median_proxy_percentile_within_country",
        "median_log_views_percentile_within_country",
        "median_engagement_percentile_within_country",
    ]
    return summary[columns]


def build_multilingual_text_tone_frame(feature_df: pd.DataFrame) -> pd.DataFrame:
    normalized_df = build_country_normalized_frame(feature_df)
    missing_columns = REQUIRED_TEXT_COLUMNS.difference(normalized_df.columns)
    if missing_columns:
        raise ValueError("Missing required columns: %s" % sorted(missing_columns))

    tone_df = normalized_df.copy()
    tone_df["tags_is_missing"] = tone_df["tags_is_missing"].astype("boolean")
    tone_df["description_has_links"] = tone_df["description_has_links"].astype("boolean")

    tone_df["description_text_quality"] = [
        "missing" if bool(is_missing) else _classify_text_quality(text)
        for text, is_missing in zip(
            tone_df["description_normalized"],
            tone_df["description_is_missing"],
            strict=False,
        )
    ]
    tone_df["description_script_family"] = [
        "missing" if bool(is_missing) else _dominant_script_family(text)
        for text, is_missing in zip(
            tone_df["description_normalized"],
            tone_df["description_is_missing"],
            strict=False,
        )
    ]
    tone_df["description_question_count"] = tone_df["description_normalized"].map(
        lambda value: _count_marks(value, "?")
    )
    tone_df["description_exclamation_count"] = tone_df["description_normalized"].map(
        lambda value: _count_marks(value, "!")
    )
    tone_df["description_has_emoji"] = tone_df["description_normalized"].map(_has_emoji).astype("boolean")
    tone_df["description_tone_bucket"] = [
        _description_tone_bucket(text, is_missing, has_links)
        for text, is_missing, has_links in zip(
            tone_df["description_normalized"],
            tone_df["description_is_missing"],
            tone_df["description_has_links"],
            strict=False,
        )
    ]

    tone_df["tag_text_quality"] = [
        "missing" if bool(is_missing) else _classify_text_quality(text)
        for text, is_missing in zip(
            tone_df["tags_normalized"],
            tone_df["tags_is_missing"],
            strict=False,
        )
    ]
    tone_df["tag_script_family"] = [
        "missing" if bool(is_missing) else _dominant_script_family(text)
        for text, is_missing in zip(
            tone_df["tags_normalized"],
            tone_df["tags_is_missing"],
            strict=False,
        )
    ]
    tone_df["tag_has_emoji"] = tone_df["tags_normalized"].map(_has_emoji).astype("boolean")
    tone_df["tag_has_hash_symbol"] = tone_df["tags_normalized"].map(
        lambda value: "#" in _clean_text(value)
    ).astype("boolean")
    tone_df["tag_tone_bucket"] = [
        _tag_tone_bucket(text, is_missing, tag_count)
        for text, is_missing, tag_count in zip(
            tone_df["tags_normalized"],
            tone_df["tags_is_missing"],
            tone_df["tag_count"],
            strict=False,
        )
    ]

    return tone_df.sort_values(["country", "video_id"]).reset_index(drop=True)


def build_tone_country_summary(tone_df: pd.DataFrame) -> pd.DataFrame:
    summaries = [
        _build_dimension_country_summary(tone_df, analysis_family, source_column)
        for analysis_family, source_column in TEXT_DIMENSION_SPECS
    ]
    return pd.concat(summaries, ignore_index=True).sort_values(
        ["country", "analysis_family", "analysis_dimension", "dimension_value"],
        kind="stable",
    ).reset_index(drop=True)


def build_tone_cross_country_summary(country_summary_df: pd.DataFrame) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    grouped = country_summary_df.groupby(
        ["analysis_family", "analysis_dimension", "dimension_value"],
        sort=False,
        dropna=False,
    )

    for (analysis_family, analysis_dimension, dimension_value), group in grouped:
        highest = group.sort_values(
            ["median_proxy_percentile_within_country", "video_count", "country"],
            ascending=[False, False, True],
            kind="stable",
        ).iloc[0]
        lowest = group.sort_values(
            ["median_proxy_percentile_within_country", "video_count", "country"],
            ascending=[True, False, True],
            kind="stable",
        ).iloc[0]
        records.append(
            {
                "analysis_family": analysis_family,
                "analysis_dimension": analysis_dimension,
                "dimension_value": dimension_value,
                "markets_present": int(group["country"].nunique()),
                "total_video_count": int(group["video_count"].sum()),
                "mean_share_within_country": float(group["share_within_country"].mean()),
                "mean_median_proxy_percentile_within_country": float(
                    group["median_proxy_percentile_within_country"].mean()
                ),
                "proxy_percentile_spread_across_countries": float(
                    group["median_proxy_percentile_within_country"].max()
                    - group["median_proxy_percentile_within_country"].min()
                ),
                "highest_proxy_country": str(highest["country"]),
                "lowest_proxy_country": str(lowest["country"]),
            }
        )

    return pd.DataFrame.from_records(records).sort_values(
        ["analysis_family", "analysis_dimension", "dimension_value"],
        kind="stable",
    ).reset_index(drop=True)


def build_text_quality_country_summary(tone_df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        tone_df.groupby("country", sort=True)
        .agg(
            video_count=("video_id", "size"),
            description_missing_share=(
                "description_tone_bucket",
                lambda values: float((values == "missing").mean()),
            ),
            description_likely_mojibake_share=(
                "description_text_quality",
                lambda values: float((values == "likely_mojibake").mean()),
            ),
            tags_missing_share=(
                "tag_tone_bucket",
                lambda values: float((values == "missing").mean()),
            ),
            tags_likely_mojibake_share=(
                "tag_text_quality",
                lambda values: float((values == "likely_mojibake").mean()),
            ),
        )
        .reset_index()
    )
    summary["country"] = summary["country"].astype("string")
    return summary


def _format_markdown_value(value: Any) -> str:
    if pd.isna(value):
        return "n/a"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows available._"

    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(_format_markdown_value(value) for value in row) + " |")
    return "\n".join(lines)


def _checkpoint_preview(frame: pd.DataFrame, columns: list[str], limit: int) -> pd.DataFrame:
    available_columns = [column for column in columns if column in frame.columns]
    return frame.loc[:, available_columns].head(limit)


def build_phase4_checkpoint(
    tone_df: pd.DataFrame,
    cross_country_summary_df: pd.DataFrame,
    output_dir: str,
    input_path: str,
) -> str:
    description_tone = cross_country_summary_df.loc[
        cross_country_summary_df["analysis_dimension"] == "description_tone_bucket"
    ].sort_values(
        ["mean_median_proxy_percentile_within_country", "markets_present", "total_video_count"],
        ascending=[False, False, False],
        kind="stable",
    )
    tag_tone = cross_country_summary_df.loc[
        cross_country_summary_df["analysis_dimension"] == "tag_tone_bucket"
    ].sort_values(
        ["mean_median_proxy_percentile_within_country", "markets_present", "total_video_count"],
        ascending=[False, False, False],
        kind="stable",
    )
    script_quality = cross_country_summary_df.loc[
        cross_country_summary_df["analysis_dimension"].isin(
            [
                "description_text_quality",
                "description_script_family",
                "tag_text_quality",
                "tag_script_family",
            ]
        )
    ].sort_values(
        ["analysis_dimension", "mean_share_within_country", "markets_present"],
        ascending=[True, False, False],
        kind="stable",
    )
    quality_coverage = build_text_quality_country_summary(tone_df).sort_values(
        ["description_likely_mojibake_share", "tags_likely_mojibake_share", "country"],
        ascending=[False, False, True],
        kind="stable",
    )

    description_table = _markdown_table(
        _checkpoint_preview(
            description_tone,
            [
                "dimension_value",
                "markets_present",
                "mean_share_within_country",
                "mean_median_proxy_percentile_within_country",
                "proxy_percentile_spread_across_countries",
            ],
            limit=8,
        )
    )
    tag_table = _markdown_table(
        _checkpoint_preview(
            tag_tone,
            [
                "dimension_value",
                "markets_present",
                "mean_share_within_country",
                "mean_median_proxy_percentile_within_country",
                "proxy_percentile_spread_across_countries",
            ],
            limit=8,
        )
    )
    quality_table = _markdown_table(
        _checkpoint_preview(
            quality_coverage,
            [
                "country",
                "video_count",
                "description_missing_share",
                "description_likely_mojibake_share",
                "tags_missing_share",
                "tags_likely_mojibake_share",
            ],
            limit=10,
        )
    )
    script_table = _markdown_table(
        _checkpoint_preview(
            script_quality,
            [
                "analysis_dimension",
                "dimension_value",
                "markets_present",
                "mean_share_within_country",
            ],
            limit=10,
        )
    )

    lines = [
        "# Phase 4 Multilingual Text Tone Analysis",
        "",
        "This Markdown checkpoint documents the Phase 4 outputs built from "
        f"`{input_path}`. The phase reports metadata tone through Unicode-aware structural features "
        "rather than pretending one semantic sentiment model is reliable across every country file.",
        "",
        "## Analysis artifacts",
        "",
        f"- Input artifact: `{input_path}`",
        f"- Output directory: `{output_dir}`",
        f"- Row-level tone frame: `{output_dir}/{TONE_FRAME_FILENAME}`",
        f"- Tone summary by country: `{output_dir}/{TONE_COUNTRY_SUMMARY_FILENAME}`",
        f"- Cross-country tone summary: `{output_dir}/{TONE_CROSS_COUNTRY_SUMMARY_FILENAME}`",
        "",
        "## Multilingual handling rules",
        "",
        "- `description_tone_bucket` and `tag_tone_bucket` are metadata tone fields. They describe wording structure, not viewer emotion or universal semantic sentiment.",
        "- `description_text_quality` and `tag_text_quality` surface `likely_mojibake` explicitly when corrupted decoding markers make text hard to trust semantically.",
        "- Script family is estimated from Unicode character names so non-Latin text stays visible instead of being forced through English-only token rules.",
        "- Cross-country text conclusions are limited to readable-text coverage and structural metadata tone; this phase does not claim audience sentiment across every language.",
        "",
        "## Description tone tables",
        "",
        "Top description_tone_bucket patterns by mean within-country proxy percentile:",
        "",
        description_table,
        "",
        "## Tag tone tables",
        "",
        "Top tag_tone_bucket patterns by mean within-country proxy percentile:",
        "",
        tag_table,
        "",
        "## Text-quality and coverage notes",
        "",
        "Country-level readable-text coverage preview:",
        "",
        quality_table,
        "",
        "Cross-country script and quality surfaces:",
        "",
        script_table,
        "",
        "High `likely_mojibake` shares mean semantic sentiment would be weak or misleading in those markets. Structural metadata tone remains usable, but it should be read with the coverage table above.",
        "",
        "## Interpretation guardrails",
        "",
        "- The project still reports association inside the trending corpus, not causal effects.",
        "- Phase 4 measures metadata tone, not audience emotion, because the available text comes from titles, tags, and descriptions rather than viewer reactions.",
        "- Corrupted text remains visible through quality buckets instead of being silently pooled into one global sentiment score.",
        "- Phase 3 country-aware comparison rules still apply before any pooled cross-country text statement is made.",
        "- video duration is unavailable in the provided dataset, so this phase does not invent a duration proxy from text fields.",
        "",
        "## Re-run instructions",
        "",
        "Regenerate the Phase 4 text-tone outputs from the repo root with:",
        "",
        "```bash",
        "python -m youtube_trends.text_tone_analysis",
        "```",
        "",
        "This command reads the Phase 2 feature parquet, writes the Phase 4 tone artifacts, and refreshes this checkpoint.",
    ]
    return "\n".join(lines) + "\n"


def write_text_tone_artifacts(
    input_path: str = DEFAULT_INPUT_PATH,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    checkpoint_path: str = DEFAULT_CHECKPOINT_PATH,
) -> dict[str, pd.DataFrame]:
    feature_df = pd.read_parquet(input_path)
    tone_df = build_multilingual_text_tone_frame(feature_df)
    country_summary_df = build_tone_country_summary(tone_df)
    cross_country_summary_df = build_tone_cross_country_summary(country_summary_df)

    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    tone_df.to_parquet(output_root / TONE_FRAME_FILENAME, index=False)
    country_summary_df.to_parquet(output_root / TONE_COUNTRY_SUMMARY_FILENAME, index=False)
    cross_country_summary_df.to_parquet(output_root / TONE_CROSS_COUNTRY_SUMMARY_FILENAME, index=False)

    checkpoint_text = build_phase4_checkpoint(
        tone_df=tone_df,
        cross_country_summary_df=cross_country_summary_df,
        output_dir=output_dir,
        input_path=input_path,
    )
    checkpoint_file = Path(checkpoint_path)
    checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
    checkpoint_file.write_text(checkpoint_text, encoding="utf-8")

    return {
        "tone_frame": tone_df,
        "tone_country_summary": country_summary_df,
        "tone_cross_country_summary": cross_country_summary_df,
    }


def main() -> None:
    write_text_tone_artifacts()


if __name__ == "__main__":
    main()