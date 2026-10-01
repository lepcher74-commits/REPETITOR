from pathlib import Path

from repetitor.content.module import (
    load_module_manifest,
    load_sequence_problems,
    next_sequence_skill,
)
from repetitor.domain import KnowledgeState
from repetitor.application.next_step import select_next_activity


MODULE_DIR = Path("content/mathematics/fractions/add_unlike")
CONTENT_ROOT = Path("content")


def test_mastered_skill_advances_to_declarative_next_skill():
    module = load_module_manifest(MODULE_DIR / "module.yaml")
    pools = load_sequence_problems(module, CONTENT_ROOT)
    current = module.learning_sequence[0]
    state = KnowledgeState(
        student_id="pilot-student",
        skill_id=current,
        mastery=0.80,
        independence=0.80,
        transfer=0.70,
        retention=0.70,
        confidence=0.70,
        evidence_count=6,
    )

    activity = select_next_activity(
        current_skill_id=current,
        states={current: state},
        prerequisites={current: ()},
        due_reviews=(),
        now=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
    )
    assert activity.kind == "enrichment"

    next_skill = next_sequence_skill(module, current)
    assert next_skill == module.learning_sequence[1]
    entry = next(
        problem for problem in pools[next_skill]
        if problem.purpose == "diagnostic"
    )
    assert entry.primary_skill == next_skill


def test_unmastered_skill_does_not_advance_sequence():
    module = load_module_manifest(MODULE_DIR / "module.yaml")
    current = module.learning_sequence[0]
    state = KnowledgeState(
        student_id="pilot-student",
        skill_id=current,
        mastery=0.60,
        independence=0.60,
        transfer=0.50,
        retention=0.50,
        confidence=0.50,
        evidence_count=3,
    )
    activity = select_next_activity(
        current_skill_id=current,
        states={current: state},
        prerequisites={current: ()},
        due_reviews=(),
        now=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
    )
    assert activity.kind == "learn"
