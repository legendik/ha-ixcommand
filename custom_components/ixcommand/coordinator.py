"""Data coordinator for iXcommand EV Charger."""

from datetime import timedelta
import logging
from typing import Any, Dict

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry

from .api import IXcommandApiClient, IXcommandApiAuthError, IXcommandApiError
from .const import (
    CONF_API_KEY,
    CONF_SERIAL_NUMBER,
    UPDATE_INTERVAL,
    ALL_READABLE_PROPERTIES,
)

_LOGGER = logging.getLogger(__name__)


class IXcommandCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Data coordinator for iXcommand EV Charger."""

    def __init__(
        self, hass: HomeAssistant, config_entry: ConfigEntry, api_client: IXcommandApiClient
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"iXcommand {config_entry.data[CONF_SERIAL_NUMBER]}",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.api_client = api_client
        self.serial_number = config_entry.data[CONF_SERIAL_NUMBER]

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from the API."""
        try:
            _LOGGER.debug("Fetching data for charger %s", self.serial_number)
            data = await self.api_client.get_properties(
                self.serial_number, ALL_READABLE_PROPERTIES
            )
            _LOGGER.debug("Successfully fetched %d properties for charger %s", len(data), self.serial_number)
            return data
        except IXcommandApiAuthError as err:
            # This will trigger a config entry reauth flow
            _LOGGER.error("Authentication failed for charger %s: %s", self.serial_number, err)
            raise UpdateFailed("Authentication failed") from err
        except IXcommandApiError as err:
            _LOGGER.error("Error communicating with API for charger %s: %s", self.serial_number, err)
            raise UpdateFailed(f"Error communicating with API: {err}") from err