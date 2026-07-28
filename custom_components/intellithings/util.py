"""Value coercion shared by the platforms."""

from __future__ import annotations

from typing import Any

# The platform stores every value as a string and casts on read, so a boolean
# datastream can arrive as True, "1", "true" or 1 depending on how it was written.
_TRUE = {"1", "true", "on", "yes"}
_FALSE = {"0", "false", "off", "no", ""}


def to_bool(value: Any) -> bool | None:
    """None when the value is missing or not boolean-ish — never a silent False."""
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    text = str(value).strip().lower()
    if text in _TRUE:
        return True
    if text in _FALSE:
        return False
    return None


def to_float(value: Any) -> float | None:
    """None rather than an exception — a bad reading shouldn't kill the entity."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def float_or(value: Any, default: float) -> float:
    """to_float with a fallback.

    An explicit None check, not `or` — a legitimate bound of 0 must not silently
    become the default.
    """
    parsed = to_float(value)
    return default if parsed is None else parsed
