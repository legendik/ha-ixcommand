"""iXcommand EV Charger integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from .api import IXcommandApiClient
from .const import CONF_API_KEY, DOMAIN
from .coordinator import IXcommandCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up iXcommand EV Charger from a config entry."""
    api_client = IXcommandApiClient(entry.data[CONF_API_KEY])

    coordinator = IXcommandCoordinator(hass, entry, api_client)

    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryAuthFailed:
        await api_client.close()
        raise
    except Exception:
        await api_client.close()
        raise

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api_client": api_client,
    }

    await hass.config_entries.async_forward_entry_setups(
        entry, ["sensor", "switch", "number"]
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(
        entry, ["sensor", "switch", "number"]
    )

    if unload_ok:
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["api_client"].close()

    return unload_ok
