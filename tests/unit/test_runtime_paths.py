from pathlib import Path

from repetitor.runtime_paths import default_content_dir


def test_default_content_path_is_absolute_and_present():
    path = default_content_dir()
    assert path.is_absolute()
    assert path == Path(path)
    assert (path / "module.yaml").is_file()
    assert (path / "problems.yaml").is_file()
