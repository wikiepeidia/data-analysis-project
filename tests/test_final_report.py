from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from youtube_trends.final_report import (
    build_recommendation_playbook,
    render_report_html,
    write_final_report_artifacts,
)


def _sample_snapshot_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "country": "US",
                "video_id": "v1",
                "first_trending_date_local": "2017-11-14",
                "last_trending_date_local": "2017-11-16",
            },
            {
                "country": "JP",
                "video_id": "v2",
                "first_trending_date_local": "2017-11-15",
                "last_trending_date_local": "2017-11-18",
            },
        ]
    )


def _sample_pattern_cross_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "analysis_family": "timing",
                "analysis_dimension": "publish_hour_bucket_utc",
                "dimension_value": "12-17 UTC",
                "markets_present": 10,
                "total_video_count": 100,
                "mean_share_within_country": 0.25,
                "mean_median_proxy_percentile_within_country": 0.44,
                "proxy_percentile_std_across_countries": 0.05,
                "proxy_percentile_spread_across_countries": 0.28,
                "countries_in_top_quartile": 4,
                "mean_median_engagement_percentile_within_country": 0.40,
                "highest_proxy_country": "US",
                "lowest_proxy_country": "JP",
            },
            {
                "analysis_family": "metadata",
                "analysis_dimension": "title_word_count_bucket",
                "dimension_value": "0-4 words",
                "markets_present": 10,
                "total_video_count": 90,
                "mean_share_within_country": 0.20,
                "mean_median_proxy_percentile_within_country": 0.43,
                "proxy_percentile_std_across_countries": 0.05,
                "proxy_percentile_spread_across_countries": 0.28,
                "countries_in_top_quartile": 4,
                "mean_median_engagement_percentile_within_country": 0.39,
                "highest_proxy_country": "US",
                "lowest_proxy_country": "JP",
            },
            {
                "analysis_family": "metadata",
                "analysis_dimension": "description_presence",
                "dimension_value": "description present",
                "markets_present": 10,
                "total_video_count": 95,
                "mean_share_within_country": 0.75,
                "mean_median_proxy_percentile_within_country": 0.42,
                "proxy_percentile_std_across_countries": 0.05,
                "proxy_percentile_spread_across_countries": 0.28,
                "countries_in_top_quartile": 4,
                "mean_median_engagement_percentile_within_country": 0.38,
                "highest_proxy_country": "US",
                "lowest_proxy_country": "JP",
            },
            {
                "analysis_family": "metadata",
                "analysis_dimension": "tag_count_bucket",
                "dimension_value": "11+ tags",
                "markets_present": 10,
                "total_video_count": 70,
                "mean_share_within_country": 0.31,
                "mean_median_proxy_percentile_within_country": 0.41,
                "proxy_percentile_std_across_countries": 0.05,
                "proxy_percentile_spread_across_countries": 0.28,
                "countries_in_top_quartile": 4,
                "mean_median_engagement_percentile_within_country": 0.37,
                "highest_proxy_country": "US",
                "lowest_proxy_country": "JP",
            },
        ]
    )


def _sample_category_cross_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "analysis_family": "category",
                "analysis_dimension": "category_id",
                "category_id": "10",
                "markets_present": 10,
                "total_video_count": 100,
                "mean_share_within_country": 0.08,
                "mean_median_proxy_percentile_within_country": 0.50,
                "proxy_percentile_std_across_countries": 0.05,
                "proxy_percentile_spread_across_countries": 0.42,
                "countries_in_top_quartile": 4,
                "mean_median_engagement_percentile_within_country": 0.41,
                "highest_proxy_country": "US",
                "lowest_proxy_country": "JP",
            },
            {
                "analysis_family": "category",
                "analysis_dimension": "category_id",
                "category_id": "23",
                "markets_present": 10,
                "total_video_count": 95,
                "mean_share_within_country": 0.06,
                "mean_median_proxy_percentile_within_country": 0.49,
                "proxy_percentile_std_across_countries": 0.05,
                "proxy_percentile_spread_across_countries": 0.40,
                "countries_in_top_quartile": 4,
                "mean_median_engagement_percentile_within_country": 0.40,
                "highest_proxy_country": "US",
                "lowest_proxy_country": "JP",
            },
            {
                "analysis_family": "category",
                "analysis_dimension": "category_id",
                "category_id": "30",
                "markets_present": 4,
                "total_video_count": 8,
                "mean_share_within_country": 0.001,
                "mean_median_proxy_percentile_within_country": 0.68,
                "proxy_percentile_std_across_countries": 0.15,
                "proxy_percentile_spread_across_countries": 0.62,
                "countries_in_top_quartile": 2,
                "mean_median_engagement_percentile_within_country": 0.45,
                "highest_proxy_country": "CA",
                "lowest_proxy_country": "FR",
            },
        ]
    )


def _sample_tone_cross_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "analysis_family": "tone",
                "analysis_dimension": "tag_tone_bucket",
                "dimension_value": "plain_keywords",
                "markets_present": 10,
                "total_video_count": 85,
                "mean_share_within_country": 0.11,
                "mean_median_proxy_percentile_within_country": 0.44,
                "proxy_percentile_spread_across_countries": 0.28,
                "highest_proxy_country": "US",
                "lowest_proxy_country": "JP",
            },
            {
                "analysis_family": "tone",
                "analysis_dimension": "description_text_quality",
                "dimension_value": "likely_mojibake",
                "markets_present": 4,
                "total_video_count": 40,
                "mean_share_within_country": 0.35,
                "mean_median_proxy_percentile_within_country": 0.42,
                "proxy_percentile_spread_across_countries": 0.66,
                "highest_proxy_country": "RU",
                "lowest_proxy_country": "US",
            },
        ]
    )


def _sample_tone_frame_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "country": "RU",
                "video_id": "v1",
                "description_text_quality": "likely_mojibake",
                "tag_text_quality": "likely_mojibake",
            },
            {
                "country": "RU",
                "video_id": "v2",
                "description_text_quality": "readable_multilingual",
                "tag_text_quality": "likely_mojibake",
            },
            {
                "country": "US",
                "video_id": "v3",
                "description_text_quality": "readable_multilingual",
                "tag_text_quality": "plain",
            },
            {
                "country": "JP",
                "video_id": "v4",
                "description_text_quality": "likely_mojibake",
                "tag_text_quality": "likely_mojibake",
            },
        ]
    )


def _write_inputs(tmp_path: Path) -> dict[str, str]:
    paths = {
        "snapshot_path": tmp_path / "video_country_snapshot.parquet",
        "pattern_cross_country_path": tmp_path / "pattern_cross_country_summary.parquet",
        "category_cross_country_path": tmp_path / "category_cross_country_summary.parquet",
        "tone_cross_country_path": tmp_path / "text_tone_cross_country_summary.parquet",
        "tone_frame_path": tmp_path / "multilingual_text_tone_frame.parquet",
    }
    _sample_snapshot_df().to_parquet(paths["snapshot_path"], index=False)
    _sample_pattern_cross_df().to_parquet(paths["pattern_cross_country_path"], index=False)
    _sample_category_cross_df().to_parquet(paths["category_cross_country_path"], index=False)
    _sample_tone_cross_df().to_parquet(paths["tone_cross_country_path"], index=False)
    _sample_tone_frame_df().to_parquet(paths["tone_frame_path"], index=False)
    return {key: str(value) for key, value in paths.items()}


def test_build_recommendation_playbook_emphasizes_creator_control() -> None:
    playbook = build_recommendation_playbook(
        pattern_cross_country_df=_sample_pattern_cross_df(),
        category_cross_country_df=_sample_category_cross_df(),
        tone_cross_country_df=_sample_tone_cross_df(),
        tone_frame_df=_sample_tone_frame_df(),
    )

    assert not playbook.empty
    assert (playbook["control_scope"] == "creator-controlled").all()
    assert playbook["action"].str.contains("kênh|đăng|metadata|Unicode", case=False, regex=True).any()


def test_render_report_html_links_report_assets() -> None:
    html_output = render_report_html(
        report_markdown="# Demo report\n\n## Demo subtitle\n\n## Mục tiêu nghiên cứu\n\nNội dung.",
        css_href="../assets/report.css",
        figure_cards=[{"src": "figures/demo.png", "alt": "demo", "caption": "demo caption"}],
        title="Demo report",
        subtitle="Demo subtitle",
    )

    assert "../assets/report.css" in html_output
    assert "figures/demo.png" in html_output
    assert "Demo report" in html_output
    assert "Demo subtitle" in html_output
    assert "Biểu đồ minh họa" in html_output
    assert html_output.count("<h1>") == 1
    assert "Bản trình bày tóm tắt" not in html_output


def test_write_final_report_artifacts_generates_sources(tmp_path: Path) -> None:
    input_paths = _write_inputs(tmp_path)
    report_path = tmp_path / "reports" / "final_report_vi.md"
    playbook_path = tmp_path / "reports" / "recommendation_playbook_vi.md"
    html_path = tmp_path / "reports" / "output" / "final_report_vi.html"
    css_path = tmp_path / "reports" / "assets" / "report.css"
    figures_dir = tmp_path / "reports" / "output" / "figures"

    outputs = write_final_report_artifacts(
        **input_paths,
        report_path=str(report_path),
        playbook_path=str(playbook_path),
        html_path=str(html_path),
        css_path=str(css_path),
        figures_dir=str(figures_dir),
        export_pdf=False,
    )

    assert report_path.exists()
    assert playbook_path.exists()
    assert html_path.exists()
    assert css_path.exists()
    assert (figures_dir / "timing_top_patterns.png").exists()
    assert (figures_dir / "metadata_top_patterns.png").exists()
    assert (figures_dir / "category_baselines.png").exists()
    assert (figures_dir / "category_share.png").exists()
    assert (figures_dir / "category_spread.png").exists()
    assert (figures_dir / "country_video_count.png").exists()
    assert (figures_dir / "mojibake_risk.png").exists()
    assert outputs["pdf_path"] is None