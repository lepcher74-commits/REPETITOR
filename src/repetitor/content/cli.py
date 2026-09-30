from __future__ import annotations

import argparse
from pathlib import Path

from .validator import validate_reference_slice


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a REPETITOR reference content slice")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    issues = validate_reference_slice(args.path)
    if issues:
        for issue in issues:
            print(f"[{issue.code}] {issue.message}")
        return 1

    print("Content validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
