from pathlib import Path

from repetitor.content.module import load_module_manifest, load_sequence_problems


MODULE_DIR = Path("content/mathematics/fractions/add_unlike")
CONTENT_ROOT = Path("content")


def test_pilot_learning_sequence_is_connected_and_learner_reachable():
    module = load_module_manifest(MODULE_DIR / "module.yaml")
    pools = load_sequence_problems(module, CONTENT_ROOT)

    assert tuple(pools) == module.learning_sequence
    assert len(module.learning_sequence) >= 4

    for skill_id, problems in pools.items():
        assert problems, skill_id
        assert all(problem.primary_skill == skill_id for problem in problems)
        assert any(problem.purpose in {"diagnostic", "guided", "independent"} for problem in problems)
