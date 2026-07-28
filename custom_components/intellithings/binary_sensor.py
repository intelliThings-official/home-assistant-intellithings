"""Read-only on/off states."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import entities_for
from .entity import IntelliThingsEntity, as_enum
from .util import to_bool


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator, descriptions = entities_for(hass, entry, "binary_sensor")
    async_add_entities(IntelliThingsBinarySensor(coordinator, d) for d in descriptions)


class IntelliThingsBinarySensor(IntelliThingsEntity, BinarySensorEntity):
    def __init__(self, coordinator, description) -> None:
        super().__init__(coordinator, description)
        self._attr_device_class = as_enum(
            BinarySensorDeviceClass, description.get("device_class")
        )

    @property
    def is_on(self) -> bool | None:
        return to_bool(self.native_value_raw)
