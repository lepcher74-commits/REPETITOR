"""Print unresolved Stage 8 manual-evidence markers without claiming approval.

Run from repository root: python scripts/stage8_manual_status.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from repetitor.application.stage8_gate_preflight import manual_gate_blockers


def main() -> int:
    blockers = manual_gate_blockers(ROOT)
    if blockers:
        print("Stage 8 manual evidence is INCOMPLETE:")
        for blocker in blockers:
            print(f"- {blocker}")
        print("Human review and Controller approval are always required.")
        return 1
    print("No unresolved text markers found. Human review and Controller approval still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
