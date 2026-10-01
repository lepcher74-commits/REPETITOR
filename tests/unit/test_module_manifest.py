from pathlib import Path

from repetitor.content.module import load_module_manifest


BASE = Path("content/mathematics/fractions/add_unlike")


def test_reference_module_manifest_loads():
    module = load_module_manifest(BASE / "module.yaml")
    assert module.subject.id == "mathematics"
    assert module.grade == 6
    assert module.primary_skill.id
    assert len(module.prerequisites) == 2
    assert {goal.id for goal in module.goals} == {"catch_up", "deepen", "olympiad"}
    assert module.learning_sequence == (
        "math.g6.fractions.equivalent",
        "math.g6.fractions.simplify",
        "math.g6.fractions.add_unlike",
        "math.g6.fractions.subtract_unlike",
    )
