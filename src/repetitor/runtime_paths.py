from __future__ import annotations

import sys
from pathlib import Path


def application_root() -> Path:
    """Return the source checkout or frozen application resource root."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parents[2]


def default_content_dir() -> Path:
    return application_root() / "content" / "mathematics" / "fractions" / "add_unlike"
