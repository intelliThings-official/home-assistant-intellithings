"""Diagnostics for IntelliThings integration.

Sensitive values such as access tokens and authorization headers are redacted
before being exposed through the Home Assistant diagnostics interface.
"""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .const import DOMAIN

REDACT = "**REDACTED**"


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry.

    Tokens and other sensitive data are redacted before returning.
    """
    data = dict(entry.data)
    # Redact the access token
    if CONF_TOKEN in data:
        data[CONF_TOKEN] = REDACT

    stored = hass.data.get(DOMAIN, {}).get(entry.entry_id, {})
    coordinator = stored.get("coordinator")
    device_info = {}
    if coordinator:
        device_info = {
            "device_available": getattr(coordinator, "device_available", None),
            "device": {
                k: v
                for k, v in (getattr(coordinator, "device", {}) or {}).items()
                if k in ("name", "identifier", "model", "manufacturer")
            },
        }

    return {
        "entry_id": entry.entry_id,
        "entry_data": data,
        "device_info": device_info,
        "entity_count": len(stored.get("entities", [])),
    }


async def async_get_device_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry, device: DeviceEntry
) -> dict[str, Any]:
    """Return diagnostics for a device entry."""
    return await async_get_config_entry_diagnostics(hass, entry)