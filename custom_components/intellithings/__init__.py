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
from homeassistant.exceptions import (
    ConfigEntryAuthFailed,
    ConfigEntryError,
    ConfigEntryNotReady,
)
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import (
    IntelliThingsApi,
    IntelliThingsAuthError,
    IntelliThingsError,
    IntelliThingsUrlError,
)
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
    try:
        api = IntelliThingsApi(
            async_get_clientsession(hass),
            entry.data[CONF_BASE_URL],
            entry.data[CONF_TOKEN],
        )
        discovery = await api.discovery()
    except IntelliThingsUrlError as err:
        # Reconfiguring is the only way out, so do not retry.
        raise ConfigEntryError(str(err)) from err
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

    _prune_removed_entities(hass, entry, coordinator.device.get("identifier"), entities)

    # Grouped by domain here so each platform file is a plain list comprehension.
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "entities": entities,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


def _prune_removed_entities(
    hass: HomeAssistant, entry: ConfigEntry, identifier: str, entities: list[dict]
) -> None:
    """Delete registry entries for datastreams the platform no longer exposes.

    Home Assistant keeps a registry entry after the entity stops being provided
    and shows it as unavailable forever, so un-exposing a datastream would leave
    a dead row behind that only a manual delete clears. Discovery is the
    authority on what exists, so anything it omits goes.

    Safe to run on every setup: a failed discovery raises ConfigEntryNotReady
    above and never reaches here, so an empty list means genuinely nothing is
    exposed rather than a request that did not land.
    """
    registry = er.async_get(hass)
    # Same unique_id IntelliThingsEntity builds — the one identity both sides agree on.
    live = {f"{identifier}_{e['key']}" for e in entities}

    for stale in [
        r
        for r in er.async_entries_for_config_entry(registry, entry.entry_id)
        if r.unique_id not in live
    ]:
        _LOGGER.info("Removing %s — no longer exposed by the platform", stale.entity_id)
        registry.async_remove(stale.entity_id)


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
