"""Base entity: identity, device grouping and availability in one place."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import IntelliThingsCoordinator


class IntelliThingsEntity(CoordinatorEntity[IntelliThingsCoordinator]):
    """Everything every platform needs, so the platform files stay tiny."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: IntelliThingsCoordinator, description: dict[str, Any]) -> None:
        super().__init__(coordinator)
        self._description = description
        self._key: str = description["key"]

        identifier = coordinator.device.get("identifier")
        # Must survive restarts and renames, so it is built from the device's
        # serial number and the datastream's machine name — never from anything
        # a user can edit.
        self._attr_unique_id = f"{identifier}_{self._key}"
        self._attr_name = description.get("name") or self._key

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, identifier)},
            name=coordinator.device.get("name"),
            model=coordinator.device.get("model"),
            manufacturer=coordinator.device.get("manufacturer"),
            serial_number=identifier,
        )

    @property
    def available(self) -> bool:
        """Available only when the poll worked AND the device itself is online."""
        return super().available and self.coordinator.device_available

    @property
    def native_value_raw(self) -> Any:
        """This entity's value from the last poll, or None if absent."""
        return (self.coordinator.data or {}).get("state", {}).get(self._key)


def as_enum(enum_cls: Any, value: Any) -> Any:
    """Coerce a string to an enum member, or None if Home Assistant doesn't know it.

    The platform stores device classes as free text so it can carry classes newer
    than this integration. Passing an unknown one straight through would make
    Home Assistant reject the whole entity, so unknown values are simply dropped.
    """
    if not value:
        return None
    try:
        return enum_cls(value)
    except ValueError:
        return None
