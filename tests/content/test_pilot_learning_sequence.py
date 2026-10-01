from pathlib import Path

from repetitor.content.module import load_sequence_prerequisites, load_module_manifest, load_sequence_problems


MODULE_DIR = Path("content/mathematics/fractions/add_unlike")
CONTENT_ROOT = Path("content")


def test_pilot_learning_sequence_is_connected_and_learner_reachable():
    module = load_module_manifest(MODULE_DIR / "module.yaml")
    pools = load_sequence_problems(module, CONTENT_ROOT)

    assert tuple(pools) == module.learning_sequence
    assert len(module.learning_sequence) >= 4

    for skill_id, problems in pools.items():
        assert problems, skill_id
        learner_problems = [
            problem for problem in problems
            if problem.purpose != "prerequisite_probe"
        ]
        assert all(problem.primary_skill == skill_id for problem in learner_problems)
        assert any(problem.purpose in {"diagnostic", "guided", "independent"} for problem in learner_problems)


def test_pilot_sequence_uses_declared_prerequisite_dag():
    module = load_module_manifest(MODULE_DIR / "module.yaml")
    prerequisites = load_sequence_prerequisites(module, CONTENT_ROOT)

    assert prerequisites["math.g6.fractions.equivalent"] == ()
    assert prerequisites["math.g6.fractions.simplify"] == ("math.g6.fractions.equivalent",)
    assert "math.g6.fractions.simplify" not in prerequisites["math.g6.fractions.add_unlike"]
    assert "math.g6.fractions.simplify" in prerequisites["math.g6.fractions.subtract_unlike"]
