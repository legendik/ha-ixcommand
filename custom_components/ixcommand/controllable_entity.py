"""Base controllable entity for iXcommand EV Charger."""

import asyncio
import logging
from typing import Any

from homeassistant.helpers.entity import Entity

from .api import IXcommandApiClient, IXcommandApiError
from .coordinator import IXcommandCoordinator

_LOGGER = logging.getLogger(__name__)

CONTROL_UPDATE_DELAY = 2


class IXcommandControllableEntity(Entity):
    """Base class for controllable entities with optimistic updates."""

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        api_client: IXcommandApiClient,
    ) -> None:
        """Initialize the controllable entity."""
        self.coordinator = coordinator
        self.api_client = api_client

    async def _async_control(
        self,
        property_name: str,
        property_value: Any,
    ) -> None:
        """Send control command and update local state optimistically."""
        serial = self.coordinator.serial_number
        try:
            _LOGGER.debug("Setting %s to %s for charger %s", property_name, property_value, serial)
            await self.api_client.set_properties(serial, {property_name: property_value})
            _LOGGER.debug("Successfully set %s, updating local state", property_name)
            self._update_local_state(property_name, property_value)
            await asyncio.sleep(CONTROL_UPDATE_DELAY)
            await self.coordinator.async_request_refresh()
        except IXcommandApiError as err:
            _LOGGER.error("Failed to set %s to %s: %s", property_name, property_value, err)
            raise

    def _update_local_state(self, property_name: str, property_value: Any) -> None:
        """Update coordinator data optimistically."""
        if self.coordinator.data:
            updated_data = self.coordinator.data.copy()
            updated_data[property_name] = property_value
            self.coordinator.async_set_updated_data(updated_data)
