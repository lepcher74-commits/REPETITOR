from datetime import datetime, timezone
from pathlib import Path

from PySide6.QtWidgets import QApplication

from repetitor.persistence import StudentProfile
from repetitor.ui.app import RepetitorWindow


CONTENT = Path("content/mathematics/fractions/add_unlike")


def window(tmp_path):
    QApplication.instance() or QApplication([])
    return RepetitorWindow(tmp_path, CONTENT)


def test_empty_answer_does_not_create_learning_state(tmp_path):
    w = window(tmp_path)
    w.stack.setCurrentWidget(w.diagnostic)
    w.answer.setText("")
    w._submit()
    assert "Сначала введи ответ" in w.feedback.text()
    assert w.learning.get_state("local-student", w.module.primary_skill.id) is None
    w.close()


def test_revealing_hint_is_recorded_as_non_independent_evidence(tmp_path):
    w = window(tmp_path)
    w._start_diagnostic()
    w.problem = w.problem_by_id["frac.add.guided.001"]
    w.problem_label.setText(w.problem.prompt_ru)
    while w.hint_level != 4:
        w._hint()
    w.answer.setText(str(w.problem.verifier["expected"]))
    w._submit()
    state = w.learning.get_state("local-student", w.module.primary_skill.id)
    assert state is not None
    assert state.independence == 0.0
    assert "с подсказкой" in w.feedback.text()
    assert "решил эту задачу самостоятельно" not in w.feedback.text()
    w.close()


def test_remediation_resumes_with_first_unattempted_problem(tmp_path):
    from datetime import datetime, timezone
    from repetitor.domain import AttemptEvidence

    w = window(tmp_path)
    step = w.remediations["math.prereq.lcm"]
    first = step.problems[0]
    w.learning.add_attempt(AttemptEvidence(
        id="seen-lcm-guided",
        student_id="local-student",
        problem_id=first.id,
        skill_id=first.primary_skill,
        occurred_at=datetime.now(timezone.utc),
        correct=True,
        purpose=first.purpose,
    ))
    w._start_remediation("math.prereq.lcm")
    assert w.remediation_prompt.text() == step.problems[1].prompt_ru
    w.close()


def test_gui_restores_saved_learning_problem_after_restart(tmp_path):
    first = window(tmp_path)
    first.profiles.save(StudentProfile("local-student", "mathematics", 6, "catch_up"))
    target = first.problem_by_id["frac.add.independent.002"]
    first._save_session(phase="learning", problem_id=target.id)
    first.close()

    reopened = window(tmp_path)
    assert reopened.problem.id == target.id
    assert reopened.problem_label.text() == target.prompt_ru
    reopened.close()


def test_gui_ignores_stale_session_problem_after_restart(tmp_path):
    first = window(tmp_path)
    first.profiles.save(StudentProfile("local-student", "mathematics", 6, "catch_up"))
    first.learning.save_session_state(
        "local-student",
        first.module.id,
        "removed.problem",
        "learning",
        None,
        datetime.now(timezone.utc),
    )
    first.close()

    reopened = window(tmp_path)
    assert reopened.problem.id == reopened.router.start_problem_id
    reopened.close()
