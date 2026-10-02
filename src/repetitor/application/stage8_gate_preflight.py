"""Read-only Stage 8 manual-gate completeness check; never grants approval."""
from __future__ import annotations

from pathlib import Path


MANUAL_RECORDS = (
    "docs/PILOT_MANUAL_GATE_RECORD.md",
    "docs/ACCESSIBILITY_PILOT_AUDIT_RECORD.md",
    "docs/PILOT_DATA_OPERATIONS_TEMPLATE.md",
)
UNRESOLVED = ("NOT TESTED", "[FILL]", "[ROLE OR IDENTIFIER]", "[OPERATOR TO", "[BLOCKED /", "MANUAL TESTING REQUIRED")


def manual_gate_blockers(repository_root: Path) -> list[str]:
    """Conservative textual preflight. Human review remains mandatory."""
    blockers: list[str] = []
    for relative in MANUAL_RECORDS:
        path = repository_root / relative
        if not path.is_file():
            blockers.append(f"{relative}: missing")
            continue
        content = path.read_text(encoding="utf-8")
        for marker in UNRESOLVED:
            if marker in content:
                blockers.append(f"{relative}: unresolved {marker}")
    return blockers
