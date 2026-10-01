from pathlib import Path

from PySide6.QtWidgets import QApplication

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
