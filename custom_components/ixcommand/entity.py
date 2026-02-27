"""Base entity for iXcommand EV Charger."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_SERIAL_NUMBER, DOMAIN, MANUFACTURER, MODEL
from .coordinator import IXcommandCoordinator


class IXcommandEntity(CoordinatorEntity[IXcommandCoordinator]):
    """Base entity for iXcommand EV Charger."""

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        entity_suffix: str,
    ) -> None:
        """Initialize the entity."""
        # Set up unique_id BEFORE super().__init__
        serial = config_entry.data[CONF_SERIAL_NUMBER]
        self._attr_unique_id = f"{DOMAIN}_{serial}_{entity_suffix}"
        self._attr_object_id = f"{DOMAIN}_{serial}_{entity_suffix}"
        self._attr_has_entity_name = True
        self._attr_name = entity_suffix.replace('_', ' ').title()

        # Set up device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial)},
            name=f"iXcommand Charger {serial}",
            manufacturer=MANUFACTURER,
            model=MODEL,
            sw_version="1.0.0",
        )

        # Call super last
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.entity_suffix = entity_suffix

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self.coordinator.data is not None
