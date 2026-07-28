"""Self-check for the value coercion the entities depend on.

The platform stores every value as a string and casts on read, so a boolean can
arrive as True, "1", "true" or 1, and a number can arrive as "23.5". Getting this
wrong shows up as a switch stuck off or a sensor stuck unknown — silent, and
annoying to trace back from Home Assistant. Hence one runnable check.

    python3 home-assistant/test_util.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "custom_components" / "intellithings"))

from util import float_or, to_bool, to_float  # noqa: E402


def test_to_bool():
    # Every shape the platform can hand back for a boolean datastream.
    for truthy in (True, 1, 1.0, "1", "true", "True", " on ", "yes"):
        assert to_bool(truthy) is True, truthy
    for falsy in (False, 0, 0.0, "0", "false", "off", "no", ""):
        assert to_bool(falsy) is False, falsy

    # Missing and nonsense must be None, never a silent False — a switch showing
    # "off" when the truth is "we don't know" is a lie the user acts on.
    assert to_bool(None) is None
    assert to_bool("banana") is None


def test_to_float():
    assert to_float("23.5") == 23.5
    assert to_float(0) == 0.0
    assert to_float(-4) == -4.0
    assert to_float(None) is None
    assert to_float("") is None
    assert to_float("n/a") is None


def test_float_or():
    """A legitimate bound of 0 must survive, not fall through to the default."""
    assert float_or(0, 100.0) == 0.0
    assert float_or("0", 100.0) == 0.0
    assert float_or(None, 100.0) == 100.0
    assert float_or("junk", 100.0) == 100.0


if __name__ == "__main__":
    test_to_bool()
    test_to_float()
    test_float_or()
    print("ok")
