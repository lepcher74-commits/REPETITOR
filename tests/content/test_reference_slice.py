from pathlib import Path

from repetitor.content import validate_reference_slice


REFERENCE = Path("content/mathematics/fractions/add_unlike")


def test_reference_slice_passes_validation():
    assert validate_reference_slice(REFERENCE) == []
