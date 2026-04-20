from __future__ import annotations

from pathlib import Path


def test_phase2_markdown_checkpoint_documents_feature_layer_guardrails() -> None:
    checkpoint_path = Path("checkpoints/02_feature_layer.md")
    content = checkpoint_path.read_text(encoding="utf-8")

    required_headings = [
        "Feature table artifact",
        "Timing features",
        "Metadata features",
        "Engagement context features",
        "Interpretation guardrails",
        "Re-run instructions",
    ]

    for heading in required_headings:
        assert heading in content

    assert "video_country_features.parquet" in content
    assert "publish_hour_utc" in content
    assert "engagement_rate_vs_first_trending_views" in content
    assert "post-trending context" in content
    assert "video duration is unavailable" in content
    assert "python -m youtube_trends.feature_layer" in content