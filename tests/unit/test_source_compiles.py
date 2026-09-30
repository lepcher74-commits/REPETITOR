import compileall
from pathlib import Path


def test_all_application_sources_compile():
    assert compileall.compile_dir(
        Path("src/repetitor"),
        quiet=1,
        force=True,
    )
