from pathlib import Path

from PySide6.QtWidgets import QApplication

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
