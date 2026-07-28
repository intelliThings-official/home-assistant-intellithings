"""Writable on/off controls."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import entities_for
from .entity import IntelliThingsEntity, as_enum
from .util import to_bool


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator, descriptions = entities_for(hass, entry, "switch")
    async_add_entities(IntelliThingsSwitch(coordinator, d) for d in descriptions)


class IntelliThingsSwitch(IntelliThingsEntity, SwitchEntity):
    def __init__(self, coordinator, description) -> None:
        super().__init__(coordinator, description)
        self._attr_device_class = as_enum(SwitchDeviceClass, description.get("device_class"))

    @property
    def is_on(self) -> bool | None:
        return to_bool(self.native_value_raw)

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.coordinator.async_send_command(self._key, True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.async_send_command(self._key, False)
