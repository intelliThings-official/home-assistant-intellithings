"""IntelliThings integration setup.

One config entry = one device. The entry stores a base URL and a device token;
everything else — which entities exist, what they are called — is fetched from
the platform at setup so a template change shows up on a reload rather than
needing a new release of this integration.
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import IntelliThingsApi, IntelliThingsAuthError, IntelliThingsError
from .const import CONF_BASE_URL, CONF_TOKEN, DOMAIN
from .coordinator import IntelliThingsCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = IntelliThingsApi(
        async_get_clientsession(hass),
        entry.data[CONF_BASE_URL],
        entry.data[CONF_TOKEN],
    )

    try:
        discovery = await api.discovery()
    except IntelliThingsAuthError as err:
        raise ConfigEntryAuthFailed(str(err)) from err
    except IntelliThingsError as err:
        raise ConfigEntryNotReady(str(err)) from err

    coordinator = IntelliThingsCoordinator(
        hass,
        entry,
        api,
        discovery.get("device", {}),
        discovery.get("config_hash"),
    )
    await coordinator.async_config_entry_first_refresh()

    entities = discovery.get("entities", [])
    if not entities:
        _LOGGER.warning(
            "%s exposes no datastreams to Home Assistant yet — map some on the "
            "device template's Datastreams tab, then reload this entry",
            coordinator.device.get("name"),
        )

    # Grouped by domain here so each platform file is a plain list comprehension.
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "entities": entities,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded


def entities_for(hass: HomeAssistant, entry: ConfigEntry, domain: str) -> tuple:
    """(coordinator, descriptions) for one entity domain."""
    stored = hass.data[DOMAIN][entry.entry_id]
    return (
        stored["coordinator"],
        [e for e in stored["entities"] if e.get("domain") == domain],
    )
