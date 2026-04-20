from __future__ import annotations

from pathlib import Path


def test_phase1_markdown_checkpoint_documents_proxy_and_limitations() -> None:
    checkpoint_path = Path("checkpoints/01_canonical_dataset.md")
    content = checkpoint_path.read_text(encoding="utf-8")

    required_headings = [
        "Raw data inventory",
        "Canonical row-level table",
        "Video-country snapshot table",
        "Trending-corpus performance proxy",
        "Limitations",
        "Re-run instructions",
    ]

    for heading in required_headings:
        assert heading in content

    assert "trend_days_in_country_proxy" in content
    assert "association" in content
    assert "video duration is unavailable" in content
    assert "python -m youtube_trends.canonical_dataset" in content
    assert "python -m youtube_trends.performance_frame" in content
