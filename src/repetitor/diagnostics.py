from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def record_startup_failure(data_dir: Path, error: BaseException) -> Path | None:
    """Write minimal local diagnostics without learner/profile/content data."""
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
        path = data_dir / "startup-errors.log"
        timestamp = datetime.now(timezone.utc).isoformat()
        error_type = type(error).__name__
        with path.open("a", encoding="utf-8") as stream:
            stream.write(f"{timestamp} startup_failure {error_type}\n")
        return path
    except OSError:
        return None
