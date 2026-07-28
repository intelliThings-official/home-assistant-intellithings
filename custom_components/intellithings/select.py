"""Writable mode pickers.

Home Assistant selects work in labels; the device works in values. The mapping
comes from the device template, so it is built once per entity and used in both
directions.
"""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import entities_for
from .entity import IntelliThingsEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator, descriptions = entities_for(hass, entry, "select")
    async_add_entities(
        IntelliThingsSelect(coordinator, d) for d in descriptions if d.get("options")
    )


class IntelliThingsSelect(IntelliThingsEntity, SelectEntity):
    def __init__(self, coordinator, description) -> None:
        super().__init__(coordinator, description)
        options = description.get("options") or []
        # Compared as strings both ways: the platform stores values as strings,
        # but casts them on read, so a "1" written can come back as 1.
        self._value_to_label = {str(o["value"]): o["label"] for o in options}
        self._label_to_value = {o["label"]: str(o["value"]) for o in options}
        self._attr_options = list(self._label_to_value)

    @property
    def current_option(self) -> str | None:
        raw = self.native_value_raw
        if raw is None:
            return None
        # An unmapped value means the device is in a state the template doesn't
        # describe. None shows as "unknown", which beats guessing.
        return self._value_to_label.get(str(raw))

    async def async_select_option(self, option: str) -> None:
        value = self._label_to_value.get(option)
        if value is None:
            raise HomeAssistantError(f"Unknown option {option!r} for {self.name}")
        await self.coordinator.async_send_command(self._key, value)
