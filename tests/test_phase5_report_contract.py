from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from youtube_trends.final_report import write_final_report_artifacts

from tests.test_final_report import _write_inputs


def test_phase5_vietnamese_report_documents_limitations_without_export_section(tmp_path: Path) -> None:
    input_paths = _write_inputs(tmp_path)
    report_path = tmp_path / "reports" / "final_report_vi.md"

    write_final_report_artifacts(
        **input_paths,
        report_path=str(report_path),
        playbook_path=str(tmp_path / "reports" / "recommendation_playbook_vi.md"),
        html_path=str(tmp_path / "reports" / "output" / "final_report_vi.html"),
        css_path=str(tmp_path / "reports" / "assets" / "report.css"),
        figures_dir=str(tmp_path / "reports" / "output" / "figures"),
        export_pdf=False,
    )

    content = report_path.read_text(encoding="utf-8")

    required_headings = [
        "Mục tiêu nghiên cứu",
        "Dữ liệu và phương pháp",
        "Kết quả chính",
        "Khuyến nghị cho kênh mới",
        "Hạn chế",
        "Kết luận",
    ]

    for heading in required_headings:
        assert heading in content

    assert "trend_days_in_country_proxy" in content
    assert "category_id" in content
    assert "likely_mojibake" in content
    assert "metadata tone" in content
    assert "Quy trình tái tạo và xuất PDF" not in content
    assert "# Báo cáo đồ án cuối khóa Data Analysts" in content
    assert "## Phân tích xu hướng nội dung YouTube" in content
    assert "Ngày dựng báo cáo" not in content
    assert "mean_median_proxy_percentile_within_country" not in content
    assert "proxy_percentile_spread_across_countries" not in content
    assert "Percentile trung vị" in content
    assert "Bản báo cáo này tổng hợp toàn bộ kết quả" not in content