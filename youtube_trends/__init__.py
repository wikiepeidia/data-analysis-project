from __future__ import annotations

from pathlib import Path

_src_package_dir = Path(__file__).resolve().parent.parent / "src" / "youtube_trends"
if _src_package_dir.exists():
    __path__.append(str(_src_package_dir))
