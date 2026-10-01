from pathlib import Path

from repetitor.runtime_paths import default_content_dir


def test_default_content_path_is_absolute_and_present():
    path = default_content_dir()
    assert path.is_absolute()
    assert path == Path(path)
    assert (path / "module.yaml").is_file()
    assert (path / "problems.yaml").is_file()


def test_frozen_content_path_uses_meipass(monkeypatch, tmp_path):
    import sys
    from repetitor.runtime_paths import default_content_dir

    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)
    assert default_content_dir() == tmp_path / "content" / "mathematics" / "fractions" / "add_unlike"
