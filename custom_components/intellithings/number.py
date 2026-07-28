"""Writable numeric setpoints."""

from __future__ import annotations

from homeassistant.components.number import NumberDeviceClass, NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import entities_for
from .entity import IntelliThingsEntity, as_enum
from .util import float_or, to_float


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator, descriptions = entities_for(hass, entry, "number")
    async_add_entities(IntelliThingsNumber(coordinator, d) for d in descriptions)


class IntelliThingsNumber(IntelliThingsEntity, NumberEntity):
    def __init__(self, coordinator, description) -> None:
        super().__init__(coordinator, description)
        self._attr_native_unit_of_measurement = description.get("unit")
        self._attr_device_class = as_enum(NumberDeviceClass, description.get("device_class"))
        # The template supplies these, but fall back to sane defaults rather than
        # crashing if an older platform version omits them.
        self._attr_native_min_value = float_or(description.get("min"), 0.0)
        self._attr_native_max_value = float_or(description.get("max"), 100.0)
        self._attr_native_step = float_or(description.get("step"), 1.0)

    @property
    def native_value(self) -> float | None:
        return to_float(self.native_value_raw)

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_send_command(self._key, value)
