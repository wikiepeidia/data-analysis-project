from __future__ import annotations

import json
from pathlib import Path


def test_phase1_notebook_documents_proxy_and_limitations() -> None:
    notebook_path = Path("notebooks/01_canonical_dataset.ipynb")
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    combined_source = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
    )

    required_headings = [
        "Raw data inventory",
        "Canonical row-level table",
        "Video-country snapshot table",
        "Trending-corpus performance proxy",
        "Limitations",
        "Re-run instructions",
    ]

    for heading in required_headings:
        assert heading in combined_source

    assert "trend_days_in_country_proxy" in combined_source
    assert "association" in combined_source
    assert "video duration is unavailable" in combined_source
    assert "python -m youtube_trends.canonical_dataset" in combined_source
    assert "python -m youtube_trends.performance_frame" in combined_source
