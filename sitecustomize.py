from __future__ import annotations

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parent / "src"
if SRC_ROOT.exists():
    sys.path.insert(0, str(SRC_ROOT))
