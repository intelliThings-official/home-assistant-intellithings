"""Value coercion and URL/token hygiene shared by the platforms.

Dependency-free on purpose: `test_util.py` imports this module directly, without
Home Assistant or aiohttp installed.
"""

from __future__ import annotations

import ipaddress
import re
from typing import Any
from urllib.parse import urlsplit

# Pattern to redact Bearer tokens from log and error strings.
_TOKEN_PATTERN = re.compile(r"(Bearer\s+)(\S+)", re.IGNORECASE)
_TOKEN_REPLACEMENT = r"\1[REDACTED]"


def redact_token(text: str) -> str:
    """Replace bearer tokens with [REDACTED] for safe logging."""
    return _TOKEN_PATTERN.sub(_TOKEN_REPLACEMENT, text)


def _is_local(host: str) -> bool:
    """True for loopback, link-local and RFC1918 addresses, and local host names."""
    try:
        return ipaddress.ip_address(host).is_private
    except ValueError:
        # Not an IP literal, so match on name. Exact, not prefix: "localhost.evil.com"
        # is a remote host that merely starts with "localhost".
        return host == "localhost" or host.endswith((".localhost", ".local", ".lan"))


def validate_url(url: str) -> str:
    """Return the URL, or raise ValueError if it is not usable as a server URL.

    Enforces HTTPS for remote servers. Permits HTTP only for loopback or
    private-network addresses, where TLS is often not available.
    """
    url = url.strip()
    parts = urlsplit(url)
    if (
        parts.scheme not in ("http", "https")
        or not parts.hostname
        or parts.query
        or parts.fragment
    ):
        raise ValueError(f"Invalid server URL: {redact_token(url)}")
    try:
        parts.port  # noqa: B018 — raises on a non-numeric or out-of-range port
    except ValueError as err:
        raise ValueError(f"Invalid server URL: {redact_token(url)}") from err

    if parts.scheme == "http" and not _is_local(parts.hostname):
        raise ValueError(
            "HTTP is only allowed for local or private-network addresses. "
            "Use HTTPS for remote servers."
        )

    return url

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
