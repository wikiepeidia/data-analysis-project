from __future__ import annotations

from pathlib import Path


def test_phase3_markdown_checkpoint_documents_country_aware_analysis() -> None:
    checkpoint_path = Path("checkpoints/03_cross_country_category_analysis.md")
    content = checkpoint_path.read_text(encoding="utf-8")

    required_headings = [
        "Analysis artifacts",
        "Country-normalized comparison rules",
        "Timing and metadata association tables",
        "Category comparison tables",
        "Cross-country consistency notes",
        "Interpretation guardrails",
        "Re-run instructions",
    ]

    for heading in required_headings:
        assert heading in content

    assert "trend_days_in_country_proxy" in content
    assert "country-normalized" in content
    assert "category_id" in content
    assert "association" in content
    assert "video duration is unavailable" in content
    assert "python -m youtube_trends.comparative_analysis" in content