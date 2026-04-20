from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

DEFAULT_INPUT_PATH = "data/processed/video_country_features.parquet"
DEFAULT_OUTPUT_DIR = "data/processed/phase3_analysis"
DEFAULT_CHECKPOINT_PATH = "checkpoints/03_cross_country_category_analysis.md"

COUNTRY_NORMALIZED_FILENAME = "country_normalized_video_country_features.parquet"
PATTERN_COUNTRY_SUMMARY_FILENAME = "pattern_country_summary.parquet"
PATTERN_CROSS_COUNTRY_SUMMARY_FILENAME = "pattern_cross_country_summary.parquet"
CATEGORY_COUNTRY_SUMMARY_FILENAME = "category_country_summary.parquet"
CATEGORY_CROSS_COUNTRY_SUMMARY_FILENAME = "category_cross_country_summary.parquet"

REQUIRED_COLUMNS = {
    "country",
    "video_id",
    "category_id",
    "trend_days_in_country_proxy",
    "log1p_first_trending_views",
    "engagement_rate_vs_first_trending_views",
    "publish_weekday_name_utc",
    "publish_hour_utc",
    "description_is_missing",
    "tag_count",
    "title_word_count",
}

WEEKDAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
HOUR_BUCKET_ORDER = ["00-05 UTC", "06-11 UTC", "12-17 UTC", "18-23 UTC"]
TAG_BUCKET_ORDER = ["0 tags", "1-5 tags", "6-10 tags", "11+ tags"]
TITLE_BUCKET_ORDER = ["0-4 words", "5-8 words", "9-12 words", "13+ words"]
DESCRIPTION_PRESENCE_ORDER = ["description present", "description missing"]

DIMENSION_SPECS = [
    ("timing", "publish_weekday_name_utc", "publish_weekday_name_utc"),
    ("timing", "publish_hour_bucket_utc", "publish_hour_bucket_utc"),
    ("metadata", "description_presence", "description_presence"),
    ("metadata", "tag_count_bucket", "tag_count_bucket"),
    ("metadata", "title_word_count_bucket", "title_word_count_bucket"),
    ("category", "category_id", "category_id"),
]


def _bucket_publish_hour(value: Any) -> str:
    hour = int(value)
    if hour < 6:
        return "00-05 UTC"
    if hour < 12:
        return "06-11 UTC"
    if hour < 18:
        return "12-17 UTC"
    return "18-23 UTC"


def _bucket_tag_count(value: Any) -> str:
    tag_count = int(value)
    if tag_count <= 0:
        return "0 tags"
    if tag_count <= 5:
        return "1-5 tags"
    if tag_count <= 10:
        return "6-10 tags"
    return "11+ tags"


def _bucket_title_word_count(value: Any) -> str:
    word_count = int(value)
    if word_count <= 4:
        return "0-4 words"
    if word_count <= 8:
        return "5-8 words"
    if word_count <= 12:
        return "9-12 words"
    return "13+ words"


def _rank_within_country(values: pd.Series) -> pd.Series:
    return values.rank(pct=True, method="average")


def _normalize_analysis_inputs(feature_df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = REQUIRED_COLUMNS.difference(feature_df.columns)
    if missing_columns:
        raise ValueError("Missing required columns: %s" % sorted(missing_columns))

    normalized = feature_df.copy()
    normalized["country"] = normalized["country"].astype("string")
    normalized["video_id"] = normalized["video_id"].astype("string")
    normalized["category_id"] = pd.to_numeric(normalized["category_id"], errors="raise").astype("Int64")
    normalized["trend_days_in_country_proxy"] = pd.to_numeric(
        normalized["trend_days_in_country_proxy"],
        errors="raise",
    ).astype("int64")
    normalized["log1p_first_trending_views"] = pd.to_numeric(
        normalized["log1p_first_trending_views"],
        errors="raise",
    ).astype("float64")
    normalized["engagement_rate_vs_first_trending_views"] = pd.to_numeric(
        normalized["engagement_rate_vs_first_trending_views"],
        errors="coerce",
    ).astype("float64")
    normalized["publish_hour_utc"] = pd.to_numeric(normalized["publish_hour_utc"], errors="raise").astype("int64")
    normalized["tag_count"] = pd.to_numeric(normalized["tag_count"], errors="raise").astype("int64")
    normalized["title_word_count"] = pd.to_numeric(normalized["title_word_count"], errors="raise").astype("int64")
    normalized["description_is_missing"] = normalized["description_is_missing"].astype("boolean")

    normalized["publish_weekday_name_utc"] = pd.Categorical(
        normalized["publish_weekday_name_utc"],
        categories=WEEKDAY_ORDER,
        ordered=True,
    )
    normalized["publish_hour_bucket_utc"] = pd.Categorical(
        normalized["publish_hour_utc"].map(_bucket_publish_hour),
        categories=HOUR_BUCKET_ORDER,
        ordered=True,
    )
    normalized["tag_count_bucket"] = pd.Categorical(
        normalized["tag_count"].map(_bucket_tag_count),
        categories=TAG_BUCKET_ORDER,
        ordered=True,
    )
    normalized["title_word_count_bucket"] = pd.Categorical(
        normalized["title_word_count"].map(_bucket_title_word_count),
        categories=TITLE_BUCKET_ORDER,
        ordered=True,
    )
    normalized["description_presence"] = pd.Categorical(
        normalized["description_is_missing"].map(
            lambda value: "description missing" if bool(value) else "description present"
        ),
        categories=DESCRIPTION_PRESENCE_ORDER,
        ordered=True,
    )

    normalized["proxy_percentile_within_country"] = normalized.groupby("country")[
        "trend_days_in_country_proxy"
    ].transform(_rank_within_country)
    normalized["log_views_percentile_within_country"] = normalized.groupby("country")[
        "log1p_first_trending_views"
    ].transform(_rank_within_country)
    normalized["engagement_rate_percentile_within_country"] = normalized.groupby("country")[
        "engagement_rate_vs_first_trending_views"
    ].transform(_rank_within_country)

    return normalized.sort_values(["country", "video_id"]).reset_index(drop=True)


def build_country_normalized_frame(feature_df: pd.DataFrame) -> pd.DataFrame:
    return _normalize_analysis_inputs(feature_df)


def _build_dimension_country_summary(
    normalized_df: pd.DataFrame,
    analysis_family: str,
    analysis_dimension: str,
    source_column: str,
) -> pd.DataFrame:
    country_sizes = normalized_df.groupby("country").size()
    summary = (
        normalized_df.groupby(["country", source_column], observed=True, dropna=False)
        .agg(
            video_count=("video_id", "size"),
            median_trend_days_in_country_proxy=("trend_days_in_country_proxy", "median"),
            median_proxy_percentile_within_country=("proxy_percentile_within_country", "median"),
            median_log1p_first_trending_views=("log1p_first_trending_views", "median"),
            median_log_views_percentile_within_country=("log_views_percentile_within_country", "median"),
            median_engagement_rate_vs_first_trending_views=(
                "engagement_rate_vs_first_trending_views",
                "median",
            ),
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
    summary["analysis_dimension"] = analysis_dimension

    columns = [
        "country",
        "analysis_family",
        "analysis_dimension",
        "dimension_value",
        "video_count",
        "share_within_country",
        "median_trend_days_in_country_proxy",
        "median_proxy_percentile_within_country",
        "median_log1p_first_trending_views",
        "median_log_views_percentile_within_country",
        "median_engagement_rate_vs_first_trending_views",
        "median_engagement_percentile_within_country",
    ]
    return summary[columns]


def build_pattern_country_summary(normalized_df: pd.DataFrame) -> pd.DataFrame:
    summaries = [
        _build_dimension_country_summary(normalized_df, family, dimension, source_column)
        for family, dimension, source_column in DIMENSION_SPECS
    ]
    return pd.concat(summaries, ignore_index=True).sort_values(
        ["country", "analysis_family", "analysis_dimension", "dimension_value"],
        kind="stable",
    ).reset_index(drop=True)


def build_pattern_cross_country_summary(pattern_country_df: pd.DataFrame) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    grouped = pattern_country_df.groupby(
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
                "proxy_percentile_std_across_countries": float(
                    group["median_proxy_percentile_within_country"].std(ddof=0)
                ),
                "proxy_percentile_spread_across_countries": float(
                    group["median_proxy_percentile_within_country"].max()
                    - group["median_proxy_percentile_within_country"].min()
                ),
                "countries_in_top_quartile": int(
                    (group["median_proxy_percentile_within_country"] >= 0.75).sum()
                ),
                "mean_median_engagement_percentile_within_country": float(
                    group["median_engagement_percentile_within_country"].mean()
                ),
                "highest_proxy_country": str(highest["country"]),
                "lowest_proxy_country": str(lowest["country"]),
            }
        )

    summary = pd.DataFrame.from_records(records)
    return summary.sort_values(
        ["analysis_family", "analysis_dimension", "dimension_value"],
        kind="stable",
    ).reset_index(drop=True)


def build_category_country_summary(pattern_country_df: pd.DataFrame) -> pd.DataFrame:
    category_summary = pattern_country_df.loc[
        pattern_country_df["analysis_family"] == "category"
    ].copy()
    category_summary = category_summary.rename(columns={"dimension_value": "category_id"})
    return category_summary.reset_index(drop=True)


def build_category_cross_country_summary(pattern_cross_country_df: pd.DataFrame) -> pd.DataFrame:
    category_summary = pattern_cross_country_df.loc[
        pattern_cross_country_df["analysis_family"] == "category"
    ].copy()
    category_summary = category_summary.rename(columns={"dimension_value": "category_id"})
    return category_summary.reset_index(drop=True)


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


def build_phase3_checkpoint(
    pattern_cross_country_df: pd.DataFrame,
    category_country_df: pd.DataFrame,
    category_cross_country_df: pd.DataFrame,
    output_dir: str,
    input_path: str,
) -> str:
    timing_highlights = pattern_cross_country_df.loc[
        pattern_cross_country_df["analysis_family"] == "timing"
    ].sort_values(
        ["mean_median_proxy_percentile_within_country", "markets_present", "total_video_count"],
        ascending=[False, False, False],
        kind="stable",
    )
    metadata_highlights = pattern_cross_country_df.loc[
        pattern_cross_country_df["analysis_family"] == "metadata"
    ].sort_values(
        ["mean_median_proxy_percentile_within_country", "markets_present", "total_video_count"],
        ascending=[False, False, False],
        kind="stable",
    )
    category_highlights = category_cross_country_df.sort_values(
        ["mean_median_proxy_percentile_within_country", "markets_present", "total_video_count"],
        ascending=[False, False, False],
        kind="stable",
    )
    category_spread = category_cross_country_df.sort_values(
        ["proxy_percentile_spread_across_countries", "markets_present", "total_video_count"],
        ascending=[False, False, False],
        kind="stable",
    )
    category_country_preview = category_country_df.sort_values(
        ["country", "median_proxy_percentile_within_country", "video_count"],
        ascending=[True, False, False],
        kind="stable",
    )

    timing_table = _markdown_table(
        _checkpoint_preview(
            timing_highlights,
            [
                "analysis_dimension",
                "dimension_value",
                "markets_present",
                "mean_median_proxy_percentile_within_country",
                "proxy_percentile_spread_across_countries",
            ],
            limit=8,
        )
    )
    metadata_table = _markdown_table(
        _checkpoint_preview(
            metadata_highlights,
            [
                "analysis_dimension",
                "dimension_value",
                "markets_present",
                "mean_median_proxy_percentile_within_country",
                "proxy_percentile_spread_across_countries",
            ],
            limit=8,
        )
    )
    category_table = _markdown_table(
        _checkpoint_preview(
            category_highlights,
            [
                "category_id",
                "markets_present",
                "mean_share_within_country",
                "mean_median_proxy_percentile_within_country",
                "highest_proxy_country",
                "lowest_proxy_country",
            ],
            limit=10,
        )
    )
    spread_table = _markdown_table(
        _checkpoint_preview(
            category_spread,
            [
                "category_id",
                "markets_present",
                "proxy_percentile_spread_across_countries",
                "highest_proxy_country",
                "lowest_proxy_country",
            ],
            limit=10,
        )
    )
    country_table = _markdown_table(
        _checkpoint_preview(
            category_country_preview,
            [
                "country",
                "category_id",
                "video_count",
                "share_within_country",
                "median_proxy_percentile_within_country",
            ],
            limit=12,
        )
    )

    lines = [
        "# Phase 3 Cross-Country Performance and Category Analysis",
        "",
        "This Markdown checkpoint documents the country-aware comparative outputs built from "
        f"`{input_path}`. The phase keeps `trend_days_in_country_proxy` as the primary "
        "trending-corpus outcome and uses country-normalized summaries before pooled interpretation.",
        "",
        "## Analysis artifacts",
        "",
        f"- Input artifact: `{input_path}`",
        f"- Output directory: `{output_dir}`",
        f"- Country-normalized video table: `{output_dir}/{COUNTRY_NORMALIZED_FILENAME}`",
        f"- Pattern summary by country: `{output_dir}/{PATTERN_COUNTRY_SUMMARY_FILENAME}`",
        f"- Cross-country pattern summary: `{output_dir}/{PATTERN_CROSS_COUNTRY_SUMMARY_FILENAME}`",
        f"- Category summary by country: `{output_dir}/{CATEGORY_COUNTRY_SUMMARY_FILENAME}`",
        f"- Cross-country category summary: `{output_dir}/{CATEGORY_CROSS_COUNTRY_SUMMARY_FILENAME}`",
        "",
        "## Country-normalized comparison rules",
        "",
        "- `trend_days_in_country_proxy` remains the primary association target, with log views and engagement rate kept as secondary context.",
        "- Country-normalized percentile ranks are computed inside each market before pooled interpretation so large markets do not dominate the story by raw scale alone.",
        "- Timing and metadata tables are reported as grouped association summaries, not causal claims about what makes any upload trend.",
        "- Category comparisons use raw `category_id` values until a verified label source is added to the repo.",
        "",
        "## Timing and metadata association tables",
        "",
        "Top recurring timing patterns by mean within-country proxy percentile:",
        "",
        timing_table,
        "",
        "Top recurring metadata patterns by mean within-country proxy percentile:",
        "",
        metadata_table,
        "",
        "## Category comparison tables",
        "",
        "Country-level category preview:",
        "",
        country_table,
        "",
        "Cross-country category summary:",
        "",
        category_table,
        "",
        "## Cross-country consistency notes",
        "",
        "Largest category spreads across countries show where the same `category_id` behaves differently by market:",
        "",
        spread_table,
        "",
        "Cross-country consistency should be read together with the country tables above. High mean percentile with low spread suggests a more repeatable pattern, while high spread marks market-specific behavior that should stay local in the report narrative.",
        "",
        "## Interpretation guardrails",
        "",
        "- The project still reports association inside the trending corpus, not causal effects.",
        "- `views`, `likes`, `dislikes`, and `comment_count` remain post-trending context rather than creator-controlled pre-publish drivers.",
        "- Category labels stay as raw `category_id` values until a verified mapping source is added.",
        "- Country-normalized pooling is required before any pooled category conclusion is stated in the report draft.",
        "- video duration is unavailable in the provided dataset, so this phase does not invent a duration proxy from metadata counts.",
        "",
        "## Re-run instructions",
        "",
        "Regenerate the Phase 3 comparative outputs from the repo root with:",
        "",
        "```bash",
        "python -m youtube_trends.comparative_analysis",
        "```",
        "",
        "This command reads the Phase 2 feature parquet, writes the country-normalized and summary parquets, and refreshes this checkpoint.",
    ]
    return "\n".join(lines) + "\n"


def write_comparative_analysis_artifacts(
    input_path: str = DEFAULT_INPUT_PATH,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    checkpoint_path: str = DEFAULT_CHECKPOINT_PATH,
) -> dict[str, pd.DataFrame]:
    feature_df = pd.read_parquet(input_path)
    normalized_df = build_country_normalized_frame(feature_df)
    pattern_country_df = build_pattern_country_summary(normalized_df)
    pattern_cross_country_df = build_pattern_cross_country_summary(pattern_country_df)
    category_country_df = build_category_country_summary(pattern_country_df)
    category_cross_country_df = build_category_cross_country_summary(pattern_cross_country_df)

    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    normalized_df.to_parquet(output_root / COUNTRY_NORMALIZED_FILENAME, index=False)
    pattern_country_df.to_parquet(output_root / PATTERN_COUNTRY_SUMMARY_FILENAME, index=False)
    pattern_cross_country_df.to_parquet(output_root / PATTERN_CROSS_COUNTRY_SUMMARY_FILENAME, index=False)
    category_country_df.to_parquet(output_root / CATEGORY_COUNTRY_SUMMARY_FILENAME, index=False)
    category_cross_country_df.to_parquet(output_root / CATEGORY_CROSS_COUNTRY_SUMMARY_FILENAME, index=False)

    checkpoint_text = build_phase3_checkpoint(
        pattern_cross_country_df=pattern_cross_country_df,
        category_country_df=category_country_df,
        category_cross_country_df=category_cross_country_df,
        output_dir=output_dir,
        input_path=input_path,
    )
    checkpoint_file = Path(checkpoint_path)
    checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
    checkpoint_file.write_text(checkpoint_text, encoding="utf-8")

    return {
        "country_normalized": normalized_df,
        "pattern_country_summary": pattern_country_df,
        "pattern_cross_country_summary": pattern_cross_country_df,
        "category_country_summary": category_country_df,
        "category_cross_country_summary": category_cross_country_df,
    }


def main() -> None:
    write_comparative_analysis_artifacts()


if __name__ == "__main__":
    main()