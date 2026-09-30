from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="REPETITOR adaptive desktop tutor")
    parser.add_argument("--data-dir", type=Path, default=Path.home() / ".repetitor")
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=Path("content/mathematics/fractions/add_unlike"),
    )
    args = parser.parse_args()

    from repetitor.ui.app import run
    return run(args.data_dir, args.content_dir)


if __name__ == "__main__":
    raise SystemExit(main())
