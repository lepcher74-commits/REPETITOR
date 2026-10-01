from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from repetitor.runtime_paths import application_root, default_content_dir



def build_info() -> str:
    try:
        app_version = version("repetitor")
    except PackageNotFoundError:
        app_version = "0+unknown"
    build_file = application_root() / "build-info.txt"
    build_sha = build_file.read_text(encoding="utf-8").strip() if build_file.exists() else "development"
    return f"REPETITOR {app_version} build {build_sha}"


def smoke_test(content_dir: Path) -> int:
    from repetitor.application.diagnostic import DiagnosticRouter
    from repetitor.application.remediation import load_remediations
    from repetitor.content import load_problems
    from repetitor.content.module import (
        load_module_manifest,
        load_sequence_prerequisites,
        load_sequence_problems,
    )

    module = load_module_manifest(content_dir / "module.yaml")
    problems = load_problems(content_dir / "problems.yaml")
    DiagnosticRouter.from_yaml(content_dir / module.diagnostic_route)
    load_remediations(content_dir / module.remediation_route)

    content_root = content_dir.parents[2]
    sequence_pools = load_sequence_problems(module, content_root)
    sequence_prerequisites = load_sequence_prerequisites(module, content_root)

    if not problems:
        raise RuntimeError("Pilot content contains no problems")
    if set(sequence_pools) != set(module.learning_sequence):
        raise RuntimeError("Pilot learning sequence is incomplete")
    if set(sequence_prerequisites) != set(module.learning_sequence):
        raise RuntimeError("Pilot prerequisite graph is incomplete")
    if any(not pool for pool in sequence_pools.values()):
        raise RuntimeError("Pilot learning sequence contains an empty problem pool")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="REPETITOR adaptive desktop tutor")
    parser.add_argument("--data-dir", type=Path, default=Path.home() / ".repetitor")
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=default_content_dir(),
    )
    parser.add_argument("--smoke-test", action="store_true")
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--build-info", action="store_true")
    args = parser.parse_args()

    if args.version or args.build_info:
        print(build_info())
        return 0

    if args.smoke_test:
        return smoke_test(args.content_dir)

    from repetitor.ui.app import run
    return run(args.data_dir, args.content_dir)


if __name__ == "__main__":
    raise SystemExit(main())
