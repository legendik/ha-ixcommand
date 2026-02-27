"""Number entities for iXcommand EV Charger."""

import asyncio
import logging
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import IXcommandApiError
from .const import (
    PROP_TARGET_CURRENT,
    PROP_BOOST_CURRENT,
    PROP_MAXIMUM_CURRENT,
    PROP_BOOST_TIME,
)
from .coordinator import IXcommandCoordinator
from .entity import IXcommandEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the iXcommand number entities."""
    coordinator: IXcommandCoordinator = hass.data["ixcommand"][config_entry.entry_id]["coordinator"]
    api_client = hass.data["ixcommand"][config_entry.entry_id]["api_client"]

    entities = [
        IXcommandTargetCurrentNumber(coordinator, config_entry, api_client, "target_current", "Target Current"),
        IXcommandBoostCurrentNumber(coordinator, config_entry, api_client, "boost_current", "Boost Current"),
        IXcommandMaximumCurrentNumber(coordinator, config_entry, api_client, "maximum_current", "Maximum Current"),
        IXcommandBoostTimeNumber(coordinator, config_entry, api_client, "boost_time", "Boost Time"),
    ]

    async_add_entities(entities)


class IXcommandTargetCurrentNumber(IXcommandEntity, NumberEntity):
    """Number entity for target charging current."""

    _attr_mode = NumberMode.SLIDER
    _attr_native_min_value = 6
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "A"

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        api_client,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name
        self.api_client = api_client

    @property
    def native_max_value(self) -> float:
        """Return the maximum allowed current based on maximum_current setting."""
        max_current = self.coordinator.data.get(PROP_MAXIMUM_CURRENT, 16)
        return float(max_current)

    @property
    def native_value(self) -> float | None:
        """Return the current target current."""
        return self.coordinator.data.get(PROP_TARGET_CURRENT)

    async def async_set_native_value(self, value: float) -> None:
        """Set the target current."""
        try:
            _LOGGER.debug("Setting target current to %s for charger %s", value, self.coordinator.serial_number)
            await self.api_client.set_properties(
                self.coordinator.serial_number, {PROP_TARGET_CURRENT: int(value)}
            )
            _LOGGER.debug("Successfully set target current, updating local state")
            # Optimistically update coordinator data
            updated_data = self.coordinator.data.copy()
            updated_data[PROP_TARGET_CURRENT] = int(value)
            self.coordinator.async_set_updated_data(updated_data)
            # Also refresh from API to confirm
            await asyncio.sleep(2)
            await self.coordinator.async_request_refresh()
        except IXcommandApiError as err:
            _LOGGER.error("Failed to set target current to %s: %s", value, err)
            raise


class IXcommandBoostCurrentNumber(IXcommandEntity, NumberEntity):
    """Number entity for boost charging current."""

    _attr_mode = NumberMode.SLIDER
    _attr_native_min_value = 6
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "A"

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        api_client,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name
        self.api_client = api_client

    @property
    def native_max_value(self) -> float:
        """Return the maximum allowed current based on maximum_current setting."""
        max_current = self.coordinator.data.get(PROP_MAXIMUM_CURRENT, 16)
        return float(max_current)

    @property
    def native_value(self) -> float | None:
        """Return the current boost current."""
        return self.coordinator.data.get(PROP_BOOST_CURRENT)

    async def async_set_native_value(self, value: float) -> None:
        """Set the boost current."""
        try:
            _LOGGER.debug("Setting boost current to %s for charger %s", value, self.coordinator.serial_number)
            await self.api_client.set_properties(
                self.coordinator.serial_number, {PROP_BOOST_CURRENT: int(value)}
            )
            _LOGGER.debug("Successfully set boost current, updating local state")
            # Optimistically update coordinator data
            updated_data = self.coordinator.data.copy()
            updated_data[PROP_BOOST_CURRENT] = int(value)
            self.coordinator.async_set_updated_data(updated_data)
            # Also refresh from API to confirm
            await asyncio.sleep(2)
            await self.coordinator.async_request_refresh()
        except IXcommandApiError as err:
            _LOGGER.error("Failed to set boost current to %s: %s", value, err)
            raise


class IXcommandMaximumCurrentNumber(IXcommandEntity, NumberEntity):
    """Number entity for maximum allowed charging current."""

    _attr_mode = NumberMode.SLIDER
    _attr_native_min_value = 6
    _attr_native_max_value = 16
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "A"

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        api_client,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name
        self.api_client = api_client

    @property
    def native_value(self) -> float | None:
        """Return the current maximum current."""
        return self.coordinator.data.get(PROP_MAXIMUM_CURRENT)

    async def async_set_native_value(self, value: float) -> None:
        """Set the maximum current."""
        try:
            _LOGGER.debug("Setting maximum current to %s for charger %s", value, self.coordinator.serial_number)
            await self.api_client.set_properties(
                self.coordinator.serial_number, {PROP_MAXIMUM_CURRENT: int(value)}
            )
            _LOGGER.debug("Successfully set maximum current, updating local state")
            # Optimistically update coordinator data
            updated_data = self.coordinator.data.copy()
            updated_data[PROP_MAXIMUM_CURRENT] = int(value)
            self.coordinator.async_set_updated_data(updated_data)
            # Also refresh from API to confirm
            await asyncio.sleep(2)
            await self.coordinator.async_request_refresh()
        except IXcommandApiError as err:
            _LOGGER.error("Failed to set maximum current to %s: %s", value, err)
            raise


class IXcommandBoostTimeNumber(IXcommandEntity, NumberEntity):
    """Number entity for boost time duration."""

    _attr_mode = NumberMode.SLIDER
    _attr_native_min_value = 0
    _attr_native_max_value = 86400  # 24 hours in seconds
    _attr_native_step = 60  # 1 minute steps
    _attr_native_unit_of_measurement = "s"

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        api_client,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name
        self.api_client = api_client

    @property
    def native_value(self) -> float | None:
        """Return the current boost time."""
        return self.coordinator.data.get(PROP_BOOST_TIME)

    async def async_set_native_value(self, value: float) -> None:
        """Set the boost time."""
        try:
            _LOGGER.debug("Setting boost time to %s seconds for charger %s", value, self.coordinator.serial_number)
            await self.api_client.set_properties(
                self.coordinator.serial_number, {PROP_BOOST_TIME: int(value)}
            )
            _LOGGER.debug("Successfully set boost time, updating local state")
            # Optimistically update coordinator data
            updated_data = self.coordinator.data.copy()
            updated_data[PROP_BOOST_TIME] = int(value)
            self.coordinator.async_set_updated_data(updated_data)
            # Also refresh from API to confirm
            await asyncio.sleep(2)
            await self.coordinator.async_request_refresh()
        except IXcommandApiError as err:
            _LOGGER.error("Failed to set boost time to %s: %s", value, err)
            raise