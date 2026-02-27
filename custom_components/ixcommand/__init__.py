"""iXcommand EV Charger integration."""

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from .api import IXcommandApiClient, IXcommandApiAuthError
from .coordinator import IXcommandCoordinator
from .const import DOMAIN, CONF_API_KEY


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up iXcommand EV Charger from a config entry."""
    # Create API client
    api_client = IXcommandApiClient(entry.data[CONF_API_KEY])

    # Create coordinator
    coordinator = IXcommandCoordinator(hass, entry, api_client)

    try:
        # Test the initial connection and fetch data
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryAuthFailed:
        # Close the API client if setup fails
        await api_client.close()
        raise
    except Exception:
        # Close the API client if setup fails
        await api_client.close()
        raise

    # Store the coordinator and API client in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api_client": api_client,
    }

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(
        entry, ["sensor", "switch", "number"]
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    unload_ok = await hass.config_entries.async_forward_entry_unload(
        entry, ["sensor", "switch", "number"]
    )

    if unload_ok:
        # Clean up coordinator and API client
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["api_client"].close()

    return unload_ok