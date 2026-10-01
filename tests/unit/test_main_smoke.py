from pathlib import Path

from repetitor.__main__ import smoke_test


CONTENT = Path("content/mathematics/fractions/add_unlike")


def test_smoke_test_loads_complete_offline_runtime_content():
    assert smoke_test(CONTENT) == 0


def test_smoke_test_fails_when_sequence_skill_is_missing(tmp_path: Path):
    # The production smoke must fail closed when the packaged content root
    # cannot resolve the module's declared learner sequence.
    module_dir = tmp_path / "content" / "mathematics" / "fractions" / "add_unlike"
    module_dir.mkdir(parents=True)
    for name in ("module.yaml", "problems.yaml", "diagnostic_route.yaml", "remediation.yaml"):
        source = CONTENT / name
        (module_dir / name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    try:
        smoke_test(module_dir)
    except ValueError as exc:
        assert "unknown skill" in str(exc)
    else:
        raise AssertionError("smoke_test must fail when sequence content is missing")
