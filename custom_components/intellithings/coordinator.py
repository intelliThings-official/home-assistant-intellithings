"""Polling coordinator: one HTTP call per interval, shared by every entity."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import IntelliThingsApi, IntelliThingsAuthError, IntelliThingsError
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class IntelliThingsCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetches /state once per interval no matter how many entities exist."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api: IntelliThingsApi,
        device: dict[str, Any],
        config_hash: str | None,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"{DOMAIN} {device.get('name') or device.get('identifier')}",
            update_interval=UPDATE_INTERVAL,
        )
        self.api = api
        self.device = device
        # Fingerprint of the entity list as it was when these entities were
        # built. The platform returns it on every poll so a template change can
        # be noticed without refetching the whole discovery document.
        self.config_hash = config_hash
        self._reload_scheduled = False

    @property
    def device_available(self) -> bool:
        """Whether the platform says the physical device is reachable.

        Distinct from the coordinator's own success: the API can answer perfectly
        while the device behind it is offline. Entities must show unavailable in
        that case rather than a stale reading.
        """
        return bool(self.data and self.data.get("available"))

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            data = await self.api.state()
        except IntelliThingsAuthError as err:
            # Prompts the user to re-authenticate instead of retrying forever
            # against a revoked token.
            raise ConfigEntryAuthFailed(str(err)) from err
        except IntelliThingsError as err:
            raise UpdateFailed(str(err)) from err

        self._check_for_config_change(data.get("config_hash"))
        return data

    def _check_for_config_change(self, new_hash: str | None) -> None:
        """Reload the entry when the device template's entity list has changed.

        A reload rather than adding entities in place: it is a handful of lines
        instead of per-platform add/remove plumbing, and it handles removals and
        retypes as well as additions. The entity registry keys on unique_id, so
        names, areas and history survive it.
        """
        if not new_hash or self.config_hash is None or new_hash == self.config_hash:
            return

        # A reload builds a fresh coordinator, so this instance is on its way
        # out — but it may still poll once more before that happens, and
        # scheduling a second reload would restart the cycle.
        if self._reload_scheduled:
            return
        self._reload_scheduled = True

        _LOGGER.info(
            "%s: device template changed, reloading to pick up the new entities",
            self.name,
        )
        self.hass.config_entries.async_schedule_reload(self.config_entry.entry_id)

    async def async_send_command(self, key: str, value: Any) -> None:
        """Write a value, then re-read.

        The platform is the source of truth — it normalises values and may reject
        one outright — so never assume the write landed as sent.
        """
        try:
            await self.api.command(key, value)
        except IntelliThingsError as err:
            # HomeAssistantError surfaces in the UI as a failed action, which is
            # what a rejected command is. No custom exception needed.
            raise HomeAssistantError(str(err)) from err
        await self.async_request_refresh()
