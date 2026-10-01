from pathlib import Path

from repetitor.content.module import load_module_manifest, next_sequence_skill


BASE = Path("content/mathematics/fractions/add_unlike")


def test_sequence_transition_is_generic_and_terminates():
    module = load_module_manifest(BASE / "module.yaml")
    sequence = module.learning_sequence

    for current, expected in zip(sequence, sequence[1:]):
        assert next_sequence_skill(module, current) == expected

    assert next_sequence_skill(module, sequence[-1]) is None
    assert next_sequence_skill(module, "unknown.skill") is None
