from __future__ import annotations

import html
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib
import pandas as pd
from markdown import markdown

matplotlib.use("Agg")

from matplotlib import pyplot as plt

DEFAULT_SNAPSHOT_PATH = "data/processed/video_country_snapshot.parquet"
DEFAULT_PATTERN_CROSS_COUNTRY_PATH = "data/processed/phase3_analysis/pattern_cross_country_summary.parquet"
DEFAULT_CATEGORY_CROSS_COUNTRY_PATH = "data/processed/phase3_analysis/category_cross_country_summary.parquet"
DEFAULT_TONE_CROSS_COUNTRY_PATH = "data/processed/phase4_analysis/text_tone_cross_country_summary.parquet"
DEFAULT_TONE_FRAME_PATH = "data/processed/phase4_analysis/multilingual_text_tone_frame.parquet"

DEFAULT_REPORT_PATH = "reports/final_report_vi.md"
DEFAULT_PLAYBOOK_PATH = "reports/recommendation_playbook_vi.md"
DEFAULT_HTML_PATH = "reports/output/final_report_vi.html"
DEFAULT_PDF_PATH = "reports/output/final_report_vi.pdf"
DEFAULT_CSS_PATH = "reports/assets/report.css"
DEFAULT_FIGURES_DIR = "reports/output/figures"
DEFAULT_REPORT_TITLE = "Báo cáo đồ án cuối khóa Data Analysts"
DEFAULT_REPORT_SUBTITLE = "Phân tích xu hướng nội dung YouTube"

DEFAULT_BROWSER_CANDIDATES = [
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe",
]

SNAPSHOT_REQUIRED_COLUMNS = {
    "country",
    "video_id",
    "first_trending_date_local",
    "last_trending_date_local",
}
PATTERN_REQUIRED_COLUMNS = {
    "analysis_family",
    "analysis_dimension",
    "dimension_value",
    "markets_present",
    "mean_median_proxy_percentile_within_country",
    "proxy_percentile_spread_across_countries",
}
CATEGORY_REQUIRED_COLUMNS = {
    "category_id",
    "markets_present",
    "mean_share_within_country",
    "mean_median_proxy_percentile_within_country",
    "proxy_percentile_spread_across_countries",
}
TONE_CROSS_REQUIRED_COLUMNS = {
    "analysis_dimension",
    "dimension_value",
    "markets_present",
    "mean_share_within_country",
    "mean_median_proxy_percentile_within_country",
    "proxy_percentile_spread_across_countries",
}
TONE_FRAME_REQUIRED_COLUMNS = {
    "country",
    "video_id",
    "description_text_quality",
    "tag_text_quality",
}


def _validate_columns(frame: pd.DataFrame, required: set[str], label: str) -> None:
    missing_columns = required.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns for {label}: {sorted(missing_columns)}")


def _format_decimal(value: Any, digits: int = 3) -> str:
    if pd.isna(value):
        return "n/a"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_Không có dữ liệu._"

    columns = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(_format_decimal(value) for value in row) + " |")
    return "\n".join(lines)


def _report_table(frame: pd.DataFrame, column_labels: dict[str, str]) -> str:
    return _markdown_table(frame.rename(columns=column_labels))


def _top_rows(frame: pd.DataFrame, count: int) -> pd.DataFrame:
    return frame.head(count).reset_index(drop=True)


def _build_text_quality_country_coverage(tone_frame_df: pd.DataFrame) -> pd.DataFrame:
    _validate_columns(tone_frame_df, TONE_FRAME_REQUIRED_COLUMNS, "tone frame")

    coverage = tone_frame_df.copy()
    coverage["description_missing_flag"] = coverage["description_text_quality"].eq("missing")
    coverage["description_likely_mojibake_flag"] = coverage["description_text_quality"].eq("likely_mojibake")
    coverage["tags_missing_flag"] = coverage["tag_text_quality"].eq("missing")
    coverage["tags_likely_mojibake_flag"] = coverage["tag_text_quality"].eq("likely_mojibake")

    summary = (
        coverage.groupby("country", dropna=False)
        .agg(
            video_count=("video_id", "size"),
            description_missing_share=("description_missing_flag", "mean"),
            description_likely_mojibake_share=("description_likely_mojibake_flag", "mean"),
            tags_missing_share=("tags_missing_flag", "mean"),
            tags_likely_mojibake_share=("tags_likely_mojibake_flag", "mean"),
        )
        .reset_index()
        .sort_values(
            ["description_likely_mojibake_share", "tags_likely_mojibake_share", "country"],
            ascending=[False, False, True],
            kind="stable",
        )
        .reset_index(drop=True)
    )
    return summary


def _default_report_css() -> str:
    return """
:root {
  --paper: #f6f2e9;
  --ink: #1f1d1a;
  --muted: #6a6255;
  --accent: #8d4f2b;
  --accent-soft: #d8b79a;
  --line: #d9cdbc;
  --card: #fffaf1;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: linear-gradient(180deg, #efe6d6 0%, #f8f4eb 100%);
  color: var(--ink);
  font-family: "Segoe UI", "Noto Sans", sans-serif;
  line-height: 1.65;
}

.page {
  max-width: 980px;
  margin: 0 auto;
  padding: 32px 28px 56px;
}

.hero {
  background: radial-gradient(circle at top left, #fff7ea 0%, #f0dcc4 45%, #ead2b4 100%);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 28px 30px;
  box-shadow: 0 18px 40px rgba(79, 52, 23, 0.08);
}

.hero h1 {
  margin: 0 0 10px;
  font-size: 32px;
  line-height: 1.2;
}

.hero p,
.hero ul {
  margin: 0;
}

.meta {
  margin-top: 14px;
  color: var(--muted);
  font-size: 14px;
}

.content {
  margin-top: 28px;
  background: rgba(255, 250, 241, 0.92);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 14px 30px rgba(79, 52, 23, 0.05);
}

h2,
h3,
h4 {
  color: #5e3118;
  margin-top: 28px;
  margin-bottom: 12px;
}

h2 {
  font-size: 24px;
  border-bottom: 1px solid var(--accent-soft);
  padding-bottom: 8px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 18px 0 22px;
  background: var(--card);
  font-size: 14px;
}

th,
td {
  border: 1px solid var(--line);
  padding: 10px 12px;
  text-align: left;
  vertical-align: top;
}

th {
  background: #efe2d0;
}

code,
pre {
  font-family: "Cascadia Code", "Consolas", monospace;
}

pre {
  background: #2c241d;
  color: #f8f1e7;
  padding: 16px;
  border-radius: 14px;
  overflow-x: auto;
}

.figure-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  margin-top: 26px;
}

.figure-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 14px;
}

.figure-card img {
  width: 100%;
  display: block;
  border-radius: 12px;
}

.figure-card figcaption {
  margin-top: 10px;
  color: var(--muted);
  font-size: 13px;
}

.note {
  background: #fff4e0;
  border-left: 4px solid var(--accent);
  padding: 12px 14px;
  border-radius: 10px;
}

@media print {
  body {
    background: #ffffff;
  }

  .page {
    max-width: none;
    padding: 0;
  }

  .hero,
  .content,
  .figure-card {
    box-shadow: none;
  }
}

@media (max-width: 760px) {
  .page {
    padding: 18px 14px 36px;
  }

  .content,
  .hero {
    padding: 20px;
  }

  .figure-grid {
    grid-template-columns: 1fr;
  }
}
""".strip() + "\n"


def _save_bar_chart(
    frame: pd.DataFrame,
    label_column: str,
    value_column: str,
    title: str,
    output_path: Path,
    xlabel: str = "Proxy percentile trung vị theo thị trường",
    color: str = "#8d4f2b",
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    chart_frame = frame.copy()
    chart_frame[label_column] = chart_frame[label_column].astype(str)

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.barh(chart_frame[label_column], chart_frame[value_column], color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--", alpha=0.35)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _save_coverage_chart(coverage_df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    chart_frame = coverage_df.copy()

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar(chart_frame["country"].astype(str), chart_frame["description_likely_mojibake_share"], color="#b5672f")
    ax.set_title("Tỷ lệ likely_mojibake theo thị trường")
    ax.set_ylabel("Tỷ lệ mô tả bị lỗi mã hóa")
    ax.set_ylim(0, max(1.0, float(chart_frame["description_likely_mojibake_share"].max()) * 1.1))
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _prepare_report_inputs(
    snapshot_df: pd.DataFrame,
    pattern_cross_country_df: pd.DataFrame,
    category_cross_country_df: pd.DataFrame,
    tone_cross_country_df: pd.DataFrame,
    tone_frame_df: pd.DataFrame,
) -> dict[str, Any]:
    _validate_columns(snapshot_df, SNAPSHOT_REQUIRED_COLUMNS, "snapshot")
    _validate_columns(pattern_cross_country_df, PATTERN_REQUIRED_COLUMNS, "pattern cross-country summary")
    _validate_columns(category_cross_country_df, CATEGORY_REQUIRED_COLUMNS, "category cross-country summary")
    _validate_columns(tone_cross_country_df, TONE_CROSS_REQUIRED_COLUMNS, "tone cross-country summary")
    _validate_columns(tone_frame_df, TONE_FRAME_REQUIRED_COLUMNS, "tone frame")

    snapshot_dates = pd.to_datetime(snapshot_df["first_trending_date_local"], errors="coerce")
    last_dates = pd.to_datetime(snapshot_df["last_trending_date_local"], errors="coerce")

    timing_top = (
        pattern_cross_country_df.loc[pattern_cross_country_df["analysis_family"] == "timing"]
        .sort_values(
            ["mean_median_proxy_percentile_within_country", "markets_present"],
            ascending=[False, False],
            kind="stable",
        )
        .reset_index(drop=True)
    )
    metadata_top = (
        pattern_cross_country_df.loc[pattern_cross_country_df["analysis_family"] == "metadata"]
        .sort_values(
            ["mean_median_proxy_percentile_within_country", "markets_present"],
            ascending=[False, False],
            kind="stable",
        )
        .reset_index(drop=True)
    )
    all_market_categories = (
        category_cross_country_df.loc[category_cross_country_df["markets_present"] >= 10]
        .sort_values(
            ["mean_median_proxy_percentile_within_country", "mean_share_within_country"],
            ascending=[False, False],
            kind="stable",
        )
        .reset_index(drop=True)
    )
    sparse_categories = (
        category_cross_country_df.loc[category_cross_country_df["markets_present"] < 10]
        .sort_values(
            ["mean_median_proxy_percentile_within_country", "markets_present"],
            ascending=[False, False],
            kind="stable",
        )
        .reset_index(drop=True)
    )
    tone_highlights = (
        tone_cross_country_df.sort_values(
            ["mean_median_proxy_percentile_within_country", "markets_present"],
            ascending=[False, False],
            kind="stable",
        )
        .reset_index(drop=True)
    )
    coverage_df = _build_text_quality_country_coverage(tone_frame_df)

    return {
        "snapshot_rows": int(len(snapshot_df)),
        "country_count": int(snapshot_df["country"].nunique()),
        "period_start": snapshot_dates.min(),
        "period_end": last_dates.max(),
        "country_distribution": (
            snapshot_df.groupby("country", dropna=False)
            .size()
            .reset_index(name="video_count")
            .sort_values(["video_count", "country"], ascending=[False, True], kind="stable")
            .reset_index(drop=True)
        ),
        "timing_top": timing_top,
        "metadata_top": metadata_top,
        "all_market_categories": all_market_categories,
        "sparse_categories": sparse_categories,
        "tone_highlights": tone_highlights,
        "coverage_df": coverage_df,
    }


def build_recommendation_playbook(
    pattern_cross_country_df: pd.DataFrame,
    category_cross_country_df: pd.DataFrame,
    tone_cross_country_df: pd.DataFrame,
    tone_frame_df: pd.DataFrame,
) -> pd.DataFrame:
    context = _prepare_report_inputs(
        snapshot_df=pd.DataFrame(
            {
                "country": [],
                "video_id": [],
                "first_trending_date_local": [],
                "last_trending_date_local": [],
            }
        ),
        pattern_cross_country_df=pattern_cross_country_df,
        category_cross_country_df=category_cross_country_df,
        tone_cross_country_df=tone_cross_country_df,
        tone_frame_df=tone_frame_df,
    )
    timing_top = context["timing_top"]
    metadata_top = context["metadata_top"]
    all_market_categories = context["all_market_categories"]
    sparse_categories = context["sparse_categories"]
    coverage_df = context["coverage_df"]

    timing_best = timing_top.iloc[0]
    short_titles = metadata_top.loc[metadata_top["analysis_dimension"] == "title_word_count_bucket"].reset_index(drop=True)
    title_best = short_titles.iloc[0] if not short_titles.empty else metadata_top.iloc[0]
    description_present = metadata_top.loc[
        metadata_top["dimension_value"] == "description present"
    ].reset_index(drop=True)
    description_best = description_present.iloc[0] if not description_present.empty else metadata_top.iloc[0]
    tag_best = metadata_top.loc[metadata_top["analysis_dimension"] == "tag_count_bucket"].reset_index(drop=True)
    tag_best_row = tag_best.iloc[0] if not tag_best.empty else metadata_top.iloc[0]
    stable_category_ids = all_market_categories.head(3)["category_id"].astype(str).tolist()
    sparse_category_ids = sparse_categories.head(2)["category_id"].astype(str).tolist()
    risky_markets = coverage_df.head(4)["country"].astype(str).tolist()

    records = [
        {
            "priority": 1,
            "action": f"Ưu tiên A/B test lịch đăng quanh {timing_best['dimension_value']} và nhóm ngày giữa tuần.",
            "evidence": (
                f"Cụm {timing_best['dimension_value']} có proxy percentile trung vị khoảng "
                f"{_format_decimal(timing_best['mean_median_proxy_percentile_within_country'])} trên {int(timing_best['markets_present'])} thị trường."
            ),
            "why_it_matters": "Lịch đăng là biến người làm kênh có thể chủ động điều chỉnh sớm nhất trước khi video lên xu hướng.",
            "risk_note": "Giờ đăng vẫn đang ở UTC; cần quy đổi và kiểm chứng lại theo thị trường mục tiêu của kênh.",
            "control_scope": "creator-controlled",
        },
        {
            "priority": 2,
            "action": (
                "Giữ tiêu đề ngắn, rõ hook, ưu tiên khoảng 4-8 từ thay vì dàn trải quá dài."
            ),
            "evidence": (
                f"Nhóm tiêu đề {title_best['dimension_value']} đang dẫn đầu với proxy percentile trung vị khoảng "
                f"{_format_decimal(title_best['mean_median_proxy_percentile_within_country'])}."
            ),
            "why_it_matters": "Tiêu đề là tín hiệu metadata nổi bật nhất mà kênh mới có thể tối ưu ngay trong bước xuất bản.",
            "risk_note": "Đây là quan hệ mô tả trong tập trending, không phải quy tắc nhân quả tuyệt đối cho mọi video.",
            "control_scope": "creator-controlled",
        },
        {
            "priority": 3,
            "action": "Điền mô tả đầy đủ và dùng tag có chủ đích; tránh để trống metadata quan trọng.",
            "evidence": (
                f"Nhóm '{description_best['dimension_value']}' và cụm tag '{tag_best_row['dimension_value']}' đều có tín hiệu tốt hơn mức thiếu dữ liệu."
            ),
            "why_it_matters": "Kênh mới có thể kiểm soát trực tiếp cấu trúc mô tả và tag, trong khi các chỉ số tương tác chỉ xuất hiện sau khi video đã được phân phối.",
            "risk_note": "Không nên nhồi tag vô nghĩa; dữ liệu chỉ gợi ý rằng metadata đầy đủ thường đi cùng kết quả tốt hơn trong tập trending.",
            "control_scope": "creator-controlled",
        },
        {
            "priority": 4,
            "action": (
                f"Khi benchmark nội dung, bắt đầu từ các nhóm category_id {', '.join(stable_category_ids)} trước; "
                f"không lấy {', '.join(sparse_category_ids) if sparse_category_ids else 'các nhóm quá hiếm'} làm chuẩn mặc định cho kênh mới."
            ),
            "evidence": "Một số category_id có percentile cao nhưng xuất hiện ở rất ít thị trường, nên khó xem là baseline ổn định cho chiến lược mới.",
            "why_it_matters": "Nhóm xuất hiện ở đủ nhiều thị trường giúp kênh mới có điểm chuẩn thực tế hơn cho thử nghiệm chủ đề.",
            "risk_note": "Repo chưa có mapping nhãn danh mục đã kiểm chứng, nên phải giữ category_id ở dạng số trong báo cáo.",
            "control_scope": "creator-controlled",
        },
        {
            "priority": 5,
            "action": (
                f"Giữ workflow Unicode-safe cho metadata, đặc biệt nếu nhắm các thị trường {', '.join(risky_markets)}."
            ),
            "evidence": "Phase 4 cho thấy `likely_mojibake` cao ở một số thị trường, nên text analysis chỉ nên đọc theo metadata tone thay vì sentiment toàn cầu.",
            "why_it_matters": "Lỗi mã hóa làm giảm khả năng đọc và có thể phá hỏng tag hoặc mô tả khi kênh mở rộng ra nhiều ngôn ngữ.",
            "risk_note": "Không diễn giải `metadata tone` như cảm xúc người xem; đây chỉ là sắc thái của tiêu đề, tag và mô tả.",
            "control_scope": "creator-controlled",
        },
    ]
    return pd.DataFrame.from_records(records)


def _build_playbook_markdown(playbook_df: pd.DataFrame) -> str:
    playbook_table = playbook_df.rename(
        columns={
            "priority": "Ưu tiên",
            "action": "Hành động",
            "evidence": "Bằng chứng dữ liệu",
            "why_it_matters": "Vì sao nên làm",
            "risk_note": "Rủi ro cần kiểm soát",
        }
    )[["Ưu tiên", "Hành động", "Bằng chứng dữ liệu", "Vì sao nên làm", "Rủi ro cần kiểm soát"]]

    lines = [
        "# Recommendation Playbook cho kênh mới",
        "",
        "Tài liệu này tách riêng các hành động ưu tiên để người làm kênh có thể áp dụng nhanh sau khi đọc báo cáo chính.",
        "",
        "## Bảng hành động ưu tiên",
        "",
        _markdown_table(playbook_table),
        "",
        "## Cách dùng",
        "",
        "1. Chọn 1-2 hành động ưu tiên cao nhất để thử trước trong 2-4 tuần.",
        "2. Theo dõi kết quả theo cùng logic thị trường mục tiêu, không trộn lẫn tất cả thị trường vào một kết luận.",
        "3. Nếu kênh làm nội dung đa ngôn ngữ, cần kiểm tra encoding của title, tags và description trước khi suy luận từ text.",
    ]
    return "\n".join(lines) + "\n"


def _build_report_markdown(context: dict[str, Any], playbook_df: pd.DataFrame) -> str:
    timing_table = _report_table(
        _top_rows(
            context["timing_top"][[
                "analysis_dimension",
                "dimension_value",
                "markets_present",
                "mean_median_proxy_percentile_within_country",
                "proxy_percentile_spread_across_countries",
            ]],
            6,
        ),
        {
            "analysis_dimension": "Nhóm tín hiệu",
            "dimension_value": "Giá trị",
            "markets_present": "Số thị trường",
            "mean_median_proxy_percentile_within_country": "Percentile trung vị",
            "proxy_percentile_spread_across_countries": "Độ chênh giữa thị trường",
        },
    )
    metadata_table = _report_table(
        _top_rows(
            context["metadata_top"][[
                "analysis_dimension",
                "dimension_value",
                "markets_present",
                "mean_median_proxy_percentile_within_country",
                "proxy_percentile_spread_across_countries",
            ]],
            8,
        ),
        {
            "analysis_dimension": "Nhóm tín hiệu",
            "dimension_value": "Giá trị",
            "markets_present": "Số thị trường",
            "mean_median_proxy_percentile_within_country": "Percentile trung vị",
            "proxy_percentile_spread_across_countries": "Độ chênh giữa thị trường",
        },
    )
    category_table = _report_table(
        _top_rows(
            context["all_market_categories"][[
                "category_id",
                "markets_present",
                "mean_share_within_country",
                "mean_median_proxy_percentile_within_country",
                "proxy_percentile_spread_across_countries",
            ]],
            6,
        ),
        {
            "category_id": "category_id",
            "markets_present": "Số thị trường",
            "mean_share_within_country": "Tỷ trọng TB",
            "mean_median_proxy_percentile_within_country": "Percentile trung vị",
            "proxy_percentile_spread_across_countries": "Độ chênh giữa thị trường",
        },
    )
    sparse_category_table = _report_table(
        _top_rows(
            context["sparse_categories"][[
                "category_id",
                "markets_present",
                "mean_share_within_country",
                "mean_median_proxy_percentile_within_country",
                "proxy_percentile_spread_across_countries",
            ]],
            4,
        ),
        {
            "category_id": "category_id",
            "markets_present": "Số thị trường",
            "mean_share_within_country": "Tỷ trọng TB",
            "mean_median_proxy_percentile_within_country": "Percentile trung vị",
            "proxy_percentile_spread_across_countries": "Độ chênh giữa thị trường",
        },
    )
    tone_table = _report_table(
        _top_rows(
            context["tone_highlights"][[
                "analysis_dimension",
                "dimension_value",
                "markets_present",
                "mean_share_within_country",
                "mean_median_proxy_percentile_within_country",
                "proxy_percentile_spread_across_countries",
            ]],
            8,
        ),
        {
            "analysis_dimension": "Nhóm tín hiệu",
            "dimension_value": "Giá trị",
            "markets_present": "Số thị trường",
            "mean_share_within_country": "Tỷ trọng TB",
            "mean_median_proxy_percentile_within_country": "Percentile trung vị",
            "proxy_percentile_spread_across_countries": "Độ chênh giữa thị trường",
        },
    )
    coverage_table = _report_table(
        _top_rows(
            context["coverage_df"][[
                "country",
                "video_count",
                "description_missing_share",
                "description_likely_mojibake_share",
                "tags_missing_share",
                "tags_likely_mojibake_share",
            ]],
            10,
        ),
        {
            "country": "Thị trường",
            "video_count": "Số video",
            "description_missing_share": "% mô tả thiếu",
            "description_likely_mojibake_share": "% mô tả lỗi mã hóa",
            "tags_missing_share": "% tag thiếu",
            "tags_likely_mojibake_share": "% tag lỗi mã hóa",
        },
    )
    playbook_table = _markdown_table(
        playbook_df.rename(
            columns={
                "priority": "Ưu tiên",
                "action": "Hành động",
                "evidence": "Bằng chứng",
                "risk_note": "Rủi ro",
            }
        )[["Ưu tiên", "Hành động", "Bằng chứng", "Rủi ro"]]
    )

    period_start = pd.to_datetime(context["period_start"]).date()
    period_end = pd.to_datetime(context["period_end"]).date()

    lines = [
        f"# {DEFAULT_REPORT_TITLE}",
        "",
        f"## {DEFAULT_REPORT_SUBTITLE}",
        "",
        "## Mục tiêu nghiên cứu",
        "",
        "Câu hỏi nghiên cứu trung tâm của đồ án là: *Làm thế nào để một kênh YouTube mới có thể tối ưu hóa lượt xem dựa trên dữ liệu xu hướng thực tế?*",
        "",
        "Báo cáo này trình bày lại các kết quả chính từ những bước phân tích trước. Từ đó, em rút ra một số điểm có thể áp dụng cho kênh YouTube mới như thời điểm đăng, cách viết metadata và lưu ý khi làm nội dung đa ngôn ngữ.",
        "",
        "## Dữ liệu và phương pháp",
        "",
        f"- Tập phân tích mặc định có **{context['snapshot_rows']}** cặp `country + video_id` trên **{context['country_count']}** thị trường.",
        f"- Giai đoạn quan sát trong snapshot chạy từ **{period_start}** đến **{period_end}**.",
        "- Biến kết quả chính là `trend_days_in_country_proxy`, tức số lần một video xuất hiện trong dữ liệu trending của từng thị trường.",
        "- Báo cáo chỉ diễn giải **association** trong tập video đã lên xu hướng, không suy luận nhân quả cho toàn bộ video trên YouTube.",
        "- Ở bước 3, dữ liệu được chuẩn hóa theo từng thị trường trước khi gộp; ở bước 4, báo cáo dùng `metadata tone` thay cho sentiment toàn cầu khi dữ liệu text bị lỗi mã hóa.",
        "",
        "## Kết quả chính",
        "",
        "### 1. Tín hiệu về thời điểm đăng",
        "",
        "Kết quả lặp lại rõ nhất nằm quanh khung `12-17 UTC` và các ngày giữa tuần đến đầu cuối tuần. Đây có thể xem là điểm bắt đầu hợp lý để thử lịch đăng, nhưng vẫn cần quy đổi theo nhóm người xem mà kênh muốn hướng tới.",
        "",
        timing_table,
        "",
        "### 2. Tín hiệu về tiêu đề, mô tả và tag",
        "",
        "Hai điểm dễ áp dụng nhất là tiêu đề ngắn gọn và metadata đầy đủ. Dữ liệu cho thấy nhóm tiêu đề rất ngắn (`0-4 words`) hoặc ngắn vừa (`5-8 words`) có percentile tốt hơn nhóm dài. Ngoài ra, video có mô tả và bộ tag rõ ràng cũng nhỉnh hơn nhóm thiếu metadata.",
        "",
        metadata_table,
        "",
        "### 3. So sánh nhóm nội dung theo `category_id`",
        "",
        "Do repo chưa có mapping danh mục đã kiểm chứng, báo cáo giữ `category_id` ở dạng số. Với mục tiêu tham khảo cho kênh mới, điều quan trọng không chỉ là percentile cao mà còn là mức độ lặp lại trên nhiều thị trường. Vì vậy, các nhóm xuất hiện ở đủ 10 thị trường phù hợp hơn để làm mốc so sánh ban đầu so với các nhóm rất hiếm nhưng percentile cao.",
        "",
        "Nhóm category_id xuất hiện trên toàn bộ 10 thị trường và có percentile khá tốt:",
        "",
        category_table,
        "",
        "Nhóm category_id có percentile cao nhưng quá hiếm, nên chỉ xem như tín hiệu tham khảo cho nhóm nội dung hẹp chứ không nên dùng làm chuẩn mặc định:",
        "",
        sparse_category_table,
        "",
        "### 4. Text đa ngôn ngữ và `metadata tone`",
        "",
        "Ở phần phân tích text, báo cáo không dùng sentiment toàn cầu vì dữ liệu ở nhiều thị trường có tỷ lệ lỗi mã hóa cao. Thay vào đó, báo cáo dùng `metadata tone` để đọc cách viết của title, tags và description. Cách làm này phù hợp hơn với dữ liệu hiện có và tránh diễn giải quá mức.",
        "",
        tone_table,
        "",
        "Bảng dưới đây cho thấy mức độ `likely_mojibake` theo thị trường. Các thị trường có tỷ lệ lỗi cao cần được đọc thận trọng hơn khi diễn giải text:",
        "",
        coverage_table,
        "",
        "## Khuyến nghị cho kênh mới",
        "",
        "Khuyến nghị dưới đây chỉ giữ lại các hành động mà người làm kênh có thể kiểm soát trực tiếp trước khi video được phân phối.",
        "",
        playbook_table,
        "",
        "Bản playbook đầy đủ nằm ở file `reports/recommendation_playbook_vi.md`.",
        "",
        "## Hạn chế",
        "",
        "- Dữ liệu chỉ gồm các video đã lên trending, nên không thể trả lời câu hỏi nhân quả kiểu 'làm gì để chắc chắn lên xu hướng'.",
        "- `category_id` vẫn ở dạng số vì repo chưa có nguồn mapping nhãn danh mục đã xác minh.",
        "- `video duration is unavailable` trong dataset gốc, nên báo cáo không thể kết luận trực tiếp về độ dài video.",
        "- Một số thị trường có `likely_mojibake` cao, vì vậy kết quả text chỉ nên đọc như `metadata tone`, không phải cảm xúc người xem hay sentiment toàn cầu.",
        "- Các biến như views, likes, comment_count vẫn là bối cảnh hậu trending, không phải biến đầu vào do creator kiểm soát.",
        "",
        "## Kết luận",
        "",
        "Tóm lại, nếu áp dụng vào một kênh mới, em sẽ ưu tiên ba việc: thử lịch đăng quanh 12-17 UTC, giữ metadata ngắn gọn nhưng đầy đủ, và kiểm tra kỹ lỗi mã hóa khi làm nội dung đa ngôn ngữ. Đây là ba điểm rõ nhất mà dữ liệu hiện có đang cho thấy.",
    ]
    return "\n".join(lines) + "\n"


def render_report_html(
    report_markdown: str,
    css_href: str,
    figure_cards: list[dict[str, str]] | None = None,
    title: str = DEFAULT_REPORT_TITLE,
    subtitle: str = DEFAULT_REPORT_SUBTITLE,
) -> str:
    figure_cards = figure_cards or []
    lines = report_markdown.splitlines()
    if lines and lines[0].strip() == f"# {title}":
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    if lines and lines[0].strip() == f"## {subtitle}":
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    content_html = markdown("\n".join(lines), extensions=["tables", "fenced_code"])
    figures_html = ""
    if figure_cards:
        cards = []
        for card in figure_cards:
            cards.append(
                "<figure class=\"figure-card\">"
                f"<img src=\"{html.escape(card['src'])}\" alt=\"{html.escape(card['alt'])}\">"
                f"<figcaption>{html.escape(card['caption'])}</figcaption>"
                "</figure>"
            )
        figures_html = (
            "<section class=\"content\">"
            "<h2>Biểu đồ minh họa</h2>"
            "<div class=\"figure-grid\">"
            + "".join(cards)
            + "</div></section>"
        )

    return (
        "<!DOCTYPE html>"
        "<html lang=\"vi\">"
        "<head>"
        "<meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{html.escape(title)} - {html.escape(subtitle)}</title>"
        f"<link rel=\"stylesheet\" href=\"{html.escape(css_href)}\">"
        "</head>"
        "<body><main class=\"page\">"
        "<section class=\"hero\">"
        f"<h1>{html.escape(title)}<br>{html.escape(subtitle)}</h1>"
        "</section>"
        f"<section class=\"content\">{content_html}</section>"
        f"{figures_html}"
        "</main></body></html>"
    )


def _write_css_asset(css_path: str) -> Path:
    css_file = Path(css_path)
    css_file.parent.mkdir(parents=True, exist_ok=True)
    if not css_file.exists():
        css_file.write_text(_default_report_css(), encoding="utf-8")
    return css_file


def _build_figure_cards(output_dir: Path, figures_dir: Path) -> list[dict[str, str]]:
    relative_root = figures_dir.relative_to(output_dir)
    return [
        {
            "src": str((relative_root / "timing_top_patterns.png").as_posix()),
            "alt": "Biểu đồ timing",
            "caption": "Nhóm khung giờ và ngày đăng có percentile tốt nhất trong Phase 3.",
        },
        {
            "src": str((relative_root / "metadata_top_patterns.png").as_posix()),
            "alt": "Biểu đồ metadata",
            "caption": "Nhóm tiêu đề và metadata có tín hiệu tốt hơn trong tập trending.",
        },
        {
            "src": str((relative_root / "category_baselines.png").as_posix()),
            "alt": "Biểu đồ category",
            "caption": "Các category_id có độ lặp lại tốt nhất trên toàn bộ 10 thị trường.",
        },
        {
            "src": str((relative_root / "category_share.png").as_posix()),
            "alt": "Biểu đồ tỷ trọng category",
            "caption": "Tỷ trọng trung bình của các category_id ổn định nhất trong mỗi thị trường.",
        },
        {
            "src": str((relative_root / "category_spread.png").as_posix()),
            "alt": "Biểu đồ độ phân tán category",
            "caption": "Độ phân tán giữa các thị trường của những category_id có mặt ở đủ nhiều nơi.",
        },
        {
            "src": str((relative_root / "country_video_count.png").as_posix()),
            "alt": "Biểu đồ số video theo thị trường",
            "caption": "Quy mô dữ liệu snapshot theo từng thị trường trong báo cáo.",
        },
        {
            "src": str((relative_root / "mojibake_risk.png").as_posix()),
            "alt": "Biểu đồ mojibake",
            "caption": "Tỷ lệ likely_mojibake theo thị trường, dùng để kiểm soát diễn giải text đa ngôn ngữ.",
        },
    ]


def _find_browser_executable(browser_path: str | None = None) -> Path | None:
    if browser_path:
        candidate = Path(browser_path)
        return candidate if candidate.exists() else None

    for candidate in DEFAULT_BROWSER_CANDIDATES:
        if candidate.exists():
            return candidate

    for binary in ["msedge", "chrome"]:
        resolved = shutil.which(binary)
        if resolved:
            return Path(resolved)
    return None


def export_html_to_pdf(html_path: str, pdf_path: str, browser_path: str | None = None) -> Path:
    html_file = Path(html_path).resolve()
    pdf_file = Path(pdf_path).resolve()
    pdf_file.parent.mkdir(parents=True, exist_ok=True)

    browser = _find_browser_executable(browser_path)
    if browser is None:
        raise FileNotFoundError("No Chromium-based browser was found for PDF export.")

    command = [
        str(browser),
        "--headless",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        html_file.as_uri(),
    ]
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(
            "PDF export failed: " + (completed.stderr.strip() or completed.stdout.strip() or str(completed.returncode))
        )
    if not pdf_file.exists():
        raise RuntimeError("PDF export command finished without creating the PDF artifact.")
    return pdf_file


def write_final_report_artifacts(
    snapshot_path: str = DEFAULT_SNAPSHOT_PATH,
    pattern_cross_country_path: str = DEFAULT_PATTERN_CROSS_COUNTRY_PATH,
    category_cross_country_path: str = DEFAULT_CATEGORY_CROSS_COUNTRY_PATH,
    tone_cross_country_path: str = DEFAULT_TONE_CROSS_COUNTRY_PATH,
    tone_frame_path: str = DEFAULT_TONE_FRAME_PATH,
    report_path: str = DEFAULT_REPORT_PATH,
    playbook_path: str = DEFAULT_PLAYBOOK_PATH,
    html_path: str = DEFAULT_HTML_PATH,
    pdf_path: str = DEFAULT_PDF_PATH,
    css_path: str = DEFAULT_CSS_PATH,
    figures_dir: str = DEFAULT_FIGURES_DIR,
    export_pdf: bool = False,
    browser_path: str | None = None,
) -> dict[str, Any]:
    snapshot_df = pd.read_parquet(snapshot_path)
    pattern_cross_country_df = pd.read_parquet(pattern_cross_country_path)
    category_cross_country_df = pd.read_parquet(category_cross_country_path)
    tone_cross_country_df = pd.read_parquet(tone_cross_country_path)
    tone_frame_df = pd.read_parquet(tone_frame_path)

    context = _prepare_report_inputs(
        snapshot_df=snapshot_df,
        pattern_cross_country_df=pattern_cross_country_df,
        category_cross_country_df=category_cross_country_df,
        tone_cross_country_df=tone_cross_country_df,
        tone_frame_df=tone_frame_df,
    )
    playbook_df = build_recommendation_playbook(
        pattern_cross_country_df=pattern_cross_country_df,
        category_cross_country_df=category_cross_country_df,
        tone_cross_country_df=tone_cross_country_df,
        tone_frame_df=tone_frame_df,
    )

    report_file = Path(report_path)
    playbook_file = Path(playbook_path)
    html_file = Path(html_path)
    css_file = _write_css_asset(css_path)
    figure_root = Path(figures_dir)

    report_file.parent.mkdir(parents=True, exist_ok=True)
    playbook_file.parent.mkdir(parents=True, exist_ok=True)
    html_file.parent.mkdir(parents=True, exist_ok=True)
    figure_root.mkdir(parents=True, exist_ok=True)

    timing_chart_df = _top_rows(
        context["timing_top"].assign(
            chart_label=lambda frame: frame["dimension_value"].astype(str) + " | " + frame["analysis_dimension"].astype(str)
        )[["chart_label", "mean_median_proxy_percentile_within_country"]],
        6,
    )
    metadata_chart_df = _top_rows(
        context["metadata_top"].assign(
            chart_label=lambda frame: frame["dimension_value"].astype(str) + " | " + frame["analysis_dimension"].astype(str)
        )[["chart_label", "mean_median_proxy_percentile_within_country"]],
        6,
    )
    category_chart_df = _top_rows(
        context["all_market_categories"].assign(
            chart_label=lambda frame: "category_id " + frame["category_id"].astype(str)
        )[["chart_label", "mean_median_proxy_percentile_within_country"]],
        6,
    )
    category_share_chart_df = _top_rows(
        context["all_market_categories"].assign(
            chart_label=lambda frame: "category_id " + frame["category_id"].astype(str)
        )[["chart_label", "mean_share_within_country"]],
        6,
    )
    category_spread_chart_df = _top_rows(
        context["all_market_categories"].assign(
            chart_label=lambda frame: "category_id " + frame["category_id"].astype(str)
        )[["chart_label", "proxy_percentile_spread_across_countries"]],
        6,
    )
    country_count_chart_df = context["country_distribution"][["country", "video_count"]].head(10).rename(
        columns={"country": "chart_label"}
    )

    _save_bar_chart(
        timing_chart_df,
        label_column="chart_label",
        value_column="mean_median_proxy_percentile_within_country",
        title="Tín hiệu thời điểm đăng nổi bật",
        output_path=figure_root / "timing_top_patterns.png",
    )
    _save_bar_chart(
        metadata_chart_df,
        label_column="chart_label",
        value_column="mean_median_proxy_percentile_within_country",
        title="Tín hiệu metadata nổi bật",
        output_path=figure_root / "metadata_top_patterns.png",
    )
    _save_bar_chart(
        category_chart_df,
        label_column="chart_label",
        value_column="mean_median_proxy_percentile_within_country",
        title="Các category_id có độ lặp lại tốt nhất",
        output_path=figure_root / "category_baselines.png",
    )
    _save_bar_chart(
        category_share_chart_df,
        label_column="chart_label",
        value_column="mean_share_within_country",
        title="Tỷ trọng trung bình của các category_id ổn định",
        output_path=figure_root / "category_share.png",
        xlabel="Tỷ trọng trung bình trong từng thị trường",
        color="#a15d38",
    )
    _save_bar_chart(
        category_spread_chart_df,
        label_column="chart_label",
        value_column="proxy_percentile_spread_across_countries",
        title="Độ phân tán category giữa các thị trường",
        output_path=figure_root / "category_spread.png",
        xlabel="Mức chênh lệch percentile giữa các thị trường",
        color="#6f3e22",
    )
    _save_bar_chart(
        country_count_chart_df,
        label_column="chart_label",
        value_column="video_count",
        title="Quy mô snapshot theo thị trường",
        output_path=figure_root / "country_video_count.png",
        xlabel="Số cặp country + video_id",
        color="#bf7b42",
    )
    _save_coverage_chart(context["coverage_df"], figure_root / "mojibake_risk.png")

    report_markdown = _build_report_markdown(context, playbook_df)
    playbook_markdown = _build_playbook_markdown(playbook_df)

    report_file.write_text(report_markdown, encoding="utf-8")
    playbook_file.write_text(playbook_markdown, encoding="utf-8")

    css_href = Path("../assets/report.css").as_posix()
    html_text = render_report_html(
        report_markdown=report_markdown,
        css_href=css_href,
        figure_cards=_build_figure_cards(output_dir=html_file.parent, figures_dir=figure_root),
        title=DEFAULT_REPORT_TITLE,
        subtitle=DEFAULT_REPORT_SUBTITLE,
    )
    html_file.write_text(html_text, encoding="utf-8")

    pdf_file = None
    if export_pdf:
        pdf_file = export_html_to_pdf(str(html_file), pdf_path, browser_path=browser_path)

    return {
        "report_path": report_file,
        "playbook_path": playbook_file,
        "html_path": html_file,
        "pdf_path": pdf_file,
        "css_path": css_file,
        "figures_dir": figure_root,
        "playbook": playbook_df,
    }


def main() -> None:
    write_final_report_artifacts(export_pdf=True)


if __name__ == "__main__":
    main()