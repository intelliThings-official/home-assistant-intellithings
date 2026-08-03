"""Read-only readings."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from . import entities_for
from .entity import IntelliThingsEntity, as_enum

# Home Assistant stores a state in a 255-character column and drops the update
# outright when it overflows, taking the whole entity with it.
MAX_STATE_LENGTH = 255


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
        value = self.native_value_raw
        if value is None:
            return None

        # A timestamp or date sensor has to hand Home Assistant a real datetime
        # object. The platform sends ISO text, and passing that straight through
        # kills the entity with an AttributeError on .tzinfo. Unparseable text
        # becomes None — unknown, rather than a crashed platform.
        if self._attr_device_class is SensorDeviceClass.TIMESTAMP:
            parsed = dt_util.parse_datetime(str(value))
            # Firmware usually sends "2026-08-03 14:30:00" with no offset, and HA
            # refuses a timestamp it cannot place. as_utc reads a naive value in
            # the HA instance's own timezone rather than dropping the reading.
            return dt_util.as_utc(parsed) if parsed else None
        if self._attr_device_class is SensorDeviceClass.DATE:
            return dt_util.parse_date(str(value))

        if isinstance(value, str) and len(value) > MAX_STATE_LENGTH:
            # ponytail: truncate, not reject — a clipped reading is still worth
            # showing. Move to an attribute if long text ever matters here.
            return value[:MAX_STATE_LENGTH]

        return value
