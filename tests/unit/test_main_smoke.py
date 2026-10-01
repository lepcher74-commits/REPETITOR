from pathlib import Path

from repetitor.__main__ import smoke_test


CONTENT = Path("content/mathematics/fractions/add_unlike")


def test_smoke_test_loads_complete_offline_runtime_content():
    assert smoke_test(CONTENT) == 0
