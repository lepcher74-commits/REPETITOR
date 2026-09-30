from pathlib import Path

from PySide6.QtWidgets import QApplication

from repetitor.ui.app import RepetitorWindow


CONTENT = Path("content/mathematics/fractions/add_unlike")


def test_main_window_constructs_offscreen(tmp_path):
    app = QApplication.instance() or QApplication([])
    window = RepetitorWindow(tmp_path, CONTENT)
    assert window.windowTitle() == "REPETITOR"
    assert window.stack.count() == 4
    window.close()
