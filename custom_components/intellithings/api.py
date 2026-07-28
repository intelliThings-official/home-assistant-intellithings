"""Thin HTTP client for the IntelliThings Home Assistant API.

Three endpoints, one token, no state. Kept separate from the coordinator so the
config flow can validate credentials without building a coordinator first.
"""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp

from .const import API_PREFIX, REQUEST_TIMEOUT


class IntelliThingsError(Exception):
    """The platform could not be reached, or returned something unusable."""


class IntelliThingsAuthError(IntelliThingsError):
    """The token was rejected, or the plugin is switched off for the org."""


class IntelliThingsApi:
    """Talks to one device, identified solely by its token."""

    def __init__(self, session: aiohttp.ClientSession, base_url: str, token: str) -> None:
        self._session = session
        self._base_url = base_url.rstrip("/")
        self._token = token

    async def discovery(self) -> dict[str, Any]:
        """Device metadata and the list of entities to create."""
        return await self._request("get", "/discovery")

    async def state(self) -> dict[str, Any]:
        """Current values for every exposed entity."""
        return await self._request("get", "/state")

    async def command(self, key: str, value: Any) -> dict[str, Any]:
        """Write one value back to the device."""
        return await self._request("post", "/command", json={"key": key, "value": value})

    async def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = f"{self._base_url}{API_PREFIX}{path}"
        headers = {"Authorization": f"Bearer {self._token}", "Accept": "application/json"}

        try:
            async with self._session.request(
                method,
                url,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
                **kwargs,
            ) as response:
                # 401 is a bad token; 403 is a good token whose plugin was turned
                # off, or a read-only entity. Both mean "stop and tell the user"
                # rather than "retry", so they share a class.
                if response.status in (401, 403):
                    raise IntelliThingsAuthError(await _message(response))
                if response.status >= 400:
                    raise IntelliThingsError(
                        f"{response.status} from {path}: {await _message(response)}"
                    )
                return await response.json()
        # asyncio.TimeoutError is NOT an aiohttp.ClientError — an exceeded total
        # timeout raises it bare, so catching only ClientError would let it escape
        # the coordinator as an unhandled exception rather than a clean retry.
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            raise IntelliThingsError(
                f"Cannot reach {self._base_url}: {err or type(err).__name__}"
            ) from err


async def _message(response: aiohttp.ClientResponse) -> str:
    """Best-effort error text — the body may not be JSON on a proxy error."""
    try:
        body = await response.json()
    except (aiohttp.ClientError, ValueError):
        return response.reason or "unknown error"
    if isinstance(body, dict):
        return str(body.get("message") or body.get("error") or body)
    return str(body)
