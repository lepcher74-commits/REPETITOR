from pathlib import Path

from PySide6.QtWidgets import QApplication, QMessageBox

from repetitor.ui import app as ui_app


def test_run_fails_closed_when_window_initialization_fails(monkeypatch, tmp_path):
    QApplication.instance() or QApplication([])
    shown = {}

    def fail_window(data_dir: Path, content_dir: Path):
        raise RuntimeError("database unavailable")

    def record_critical(parent, title, message):
        shown["title"] = title
        shown["message"] = message
        return QMessageBox.StandardButton.Ok

    monkeypatch.setattr(ui_app, "create_window", fail_window)
    monkeypatch.setattr(QMessageBox, "critical", record_critical)

    result = ui_app.run(tmp_path, tmp_path)

    assert result == 2
    assert "ошибка запуска" in shown["title"].lower()
    assert "остановлено" in shown["message"].lower()
    assert "пустой прогресс" in shown["message"].lower()
