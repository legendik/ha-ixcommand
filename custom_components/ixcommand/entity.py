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
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.entity_suffix = entity_suffix

        # Set up device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.data[CONF_SERIAL_NUMBER])},
            name=f"iXcommand Charger {config_entry.data[CONF_SERIAL_NUMBER]}",
            manufacturer=MANUFACTURER,
            model=MODEL,
            sw_version="1.0.0",
        )

        # Set up entity ID with domain prefix for uniqueness across multiple chargers
        self._attr_unique_id = f"{DOMAIN}_{config_entry.data[CONF_SERIAL_NUMBER]}_{entity_suffix}"

        # Set up entity name (simple name, device provides context)
        self._attr_name = f"{entity_suffix.replace('_', ' ').title()}"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self.coordinator.data is not None
