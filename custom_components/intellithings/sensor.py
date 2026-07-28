"""Read-only readings."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import entities_for
from .entity import IntelliThingsEntity, as_enum


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator, descriptions = entities_for(hass, entry, "sensor")
    async_add_entities(IntelliThingsSensor(coordinator, d) for d in descriptions)


class IntelliThingsSensor(IntelliThingsEntity, SensorEntity):
    """A datastream Home Assistant only reads."""

    def __init__(self, coordinator, description) -> None:
        super().__init__(coordinator, description)
        self._attr_native_unit_of_measurement = description.get("unit")
        self._attr_device_class = as_enum(SensorDeviceClass, description.get("device_class"))
        self._attr_state_class = as_enum(SensorStateClass, description.get("state_class"))

    @property
    def native_value(self):
        return self.native_value_raw
