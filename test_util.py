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

from util import float_or, redact_token, to_bool, to_float, validate_url


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


def test_validate_url():
    for good in (
        "https://api.example.com",
        "https://api.example.com:8443/base",
        "http://localhost:8123",
        "http://127.0.0.1",
        "http://192.168.1.10:8080",
        "http://[::1]:8123",
        "http://nas.local",
    ):
        assert validate_url(good) == good, good

    # Plain HTTP to anything not demonstrably local, malformed input, and hosts
    # that merely *start* with a local-looking name must all be rejected.
    for bad in (
        "http://api.example.com",
        "http://localhost.evil.com",
        "http://10.evil.com",
        "ftp://api.example.com",
        "api.example.com",
        "https://",
        "javascript:alert(1)",
        "https://api.example.com:notaport",
    ):
        try:
            validate_url(bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")


def test_redact_token():
    assert redact_token("Authorization: Bearer abc123") == (
        "Authorization: Bearer [REDACTED]"
    )
    assert redact_token("no token here") == "no token here"


if __name__ == "__main__":
    test_to_bool()
    test_to_float()
    test_float_or()
    test_validate_url()
    test_redact_token()
    print("ok")
