from pathlib import Path

import yaml

from repetitor.content.validator import validate_content_graph


def write_skill(root: Path, folder: str, skill_id: str, prerequisites=()):
    path = root / folder
    path.mkdir(parents=True)
    data = {
        "id": skill_id,
        "subject": "mathematics",
        "grade_band": "middle",
        "module": "test",
        "title_ru": skill_id,
        "objectives": ["test objective"],
        "prerequisites": list(prerequisites),
        "mastery_policy": "fraction_standard",
        "misconceptions": [],
        "tags": ["test"],
    }
    (path / "skill.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")


def codes(issues):
    return {issue.code for issue in issues}


def test_repository_graph_accepts_multi_skill_dag(tmp_path):
    write_skill(tmp_path, "a", "a")
    write_skill(tmp_path, "b", "b", ["a"])
    write_skill(tmp_path, "c", "c", ["a", "b"])
    assert validate_content_graph(tmp_path) == []


def test_repository_graph_rejects_unknown_prerequisite(tmp_path):
    write_skill(tmp_path, "a", "a", ["missing"])
    issues = validate_content_graph(tmp_path)
    assert "unknown_prerequisite" in codes(issues)


def test_repository_graph_rejects_cycle(tmp_path):
    write_skill(tmp_path, "a", "a", ["c"])
    write_skill(tmp_path, "b", "b", ["a"])
    write_skill(tmp_path, "c", "c", ["b"])
    issues = validate_content_graph(tmp_path)
    assert "prerequisite_cycle" in codes(issues)


def test_real_content_tree_has_resolvable_acyclic_prerequisites():
    assert validate_content_graph(Path("content")) == []
