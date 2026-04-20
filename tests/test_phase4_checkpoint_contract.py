from __future__ import annotations

from pathlib import Path


def test_phase4_markdown_checkpoint_documents_multilingual_handling_limits() -> None:
    checkpoint_path = Path("checkpoints/04_multilingual_text_tone_analysis.md")
    content = checkpoint_path.read_text(encoding="utf-8")

    required_headings = [
        "Analysis artifacts",
        "Multilingual handling rules",
        "Description tone tables",
        "Tag tone tables",
        "Text-quality and coverage notes",
        "Interpretation guardrails",
        "Re-run instructions",
    ]

    for heading in required_headings:
        assert heading in content

    assert "likely_mojibake" in content
    assert "description_tone_bucket" in content
    assert "tag_tone_bucket" in content
    assert "metadata tone" in content
    assert "video duration is unavailable" in content
    assert "python -m youtube_trends.text_tone_analysis" in content