from pathlib import Path

import repetitor.__main__ as app_main


def test_build_info_reads_bundled_sha(monkeypatch, tmp_path: Path):
    (tmp_path / "build-info.txt").write_text("pilot-sha-123\n", encoding="utf-8")
    monkeypatch.setattr(app_main, "application_root", lambda: tmp_path)
    info = app_main.build_info()
    assert info.startswith("REPETITOR ")
    assert info.endswith("build pilot-sha-123")


def test_build_info_has_explicit_development_fallback(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(app_main, "application_root", lambda: tmp_path)
    assert app_main.build_info().endswith("build development")
