from pathlib import Path

from PySide6.QtWidgets import QApplication, QPushButton

from repetitor.ui.app import RepetitorWindow


CONTENT = Path("content/mathematics/fractions/add_unlike")


def make_window(tmp_path):
    QApplication.instance() or QApplication([])
    return RepetitorWindow(tmp_path, CONTENT)


def test_primary_inputs_have_accessible_names(tmp_path):
    window = make_window(tmp_path)
    assert window.subject.accessibleName() == "Предмет"
    assert window.grade.accessibleName() == "Класс"
    assert window.goal.accessibleName() == "Цель обучения"
    assert window.answer.accessibleName() == "Ответ на текущую задачу"
    assert window.remediation_answer.accessibleName() == "Ответ на восстановительную задачу"
    window.close()


def test_learning_inputs_accept_keyboard_focus(tmp_path):
    window = make_window(tmp_path)
    assert window.answer.focusPolicy().value != 0
    assert window.remediation_answer.focusPolicy().value != 0
    window.close()


def test_empty_answer_announces_feedback_without_stealing_focus(tmp_path, monkeypatch):
    from repetitor.ui import app as ui_app

    events = []
    monkeypatch.setattr(ui_app.QAccessible, "updateAccessibility", lambda event: events.append(event))
    window = make_window(tmp_path)
    window.show()
    QApplication.processEvents()
    window._start_diagnostic()
    window.answer.setFocus()
    QApplication.processEvents()
    assert window.answer.hasFocus()
    window.answer.setText("")
    window._submit()
    assert window.feedback.accessibleDescription() == "Сначала введи ответ."
    assert len(events) == 2, "Answer feedback must generate announcement and alert accessibility events"
    assert window.answer.hasFocus()
    window.close()


def test_remediation_incorrect_answer_announces_feedback(tmp_path, monkeypatch):
    from repetitor.ui import app as ui_app

    events = []
    monkeypatch.setattr(ui_app.QAccessible, "updateAccessibility", lambda event: events.append(event))
    window = make_window(tmp_path)
    window._start_remediation("math.prereq.lcm")
    window.remediation_answer.setText("not a fraction")
    window._submit_remediation()
    assert "Пока не получилось" in window.remediation_feedback.accessibleDescription()
    assert events
    window.close()


def test_all_action_buttons_have_text_and_accept_keyboard_focus(tmp_path):
    window = make_window(tmp_path)
    buttons = window.findChildren(QPushButton)
    assert buttons, "Learner UI must expose actionable buttons"
    for button in buttons:
        assert button.text().strip(), "Every learner-facing action button needs visible text"
        assert button.focusPolicy().value != 0, f"{button.text()!r} must accept keyboard focus"
    window.close()


def test_correct_answer_announces_feedback_without_stealing_focus(tmp_path, monkeypatch):
    from repetitor.ui import app as ui_app

    events = []
    monkeypatch.setattr(ui_app.QAccessible, "updateAccessibility", lambda event: events.append(event))
    window = make_window(tmp_path)
    window.show()
    QApplication.processEvents()
    window._start_diagnostic()
    window.answer.setFocus()
    QApplication.processEvents()
    assert window.answer.hasFocus()
    window.answer.setText("5/6")
    window._submit()
    assert window.feedback.accessibleDescription().startswith("Верно.")
    assert events, "Correct-answer feedback must emit accessibility events"
    assert window.answer.hasFocus()
    window.close()
