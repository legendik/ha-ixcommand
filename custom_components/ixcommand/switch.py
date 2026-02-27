"""Switch entities for iXcommand EV Charger."""

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import IXcommandApiClient
from .const import PROP_BOOST_STATE, PROP_CHARGING_ENABLE, PROP_SINGLE_PHASE
from .controllable_entity import IXcommandControllableEntity
from .coordinator import IXcommandCoordinator
from .entity import IXcommandEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the iXcommand switches."""
    coordinator: IXcommandCoordinator = hass.data["ixcommand"][config_entry.entry_id]["coordinator"]
    api_client: IXcommandApiClient = hass.data["ixcommand"][config_entry.entry_id]["api_client"]

    entities = [
        IXcommandChargingEnableSwitch(coordinator, config_entry, api_client, "charging_enable", "Charging Enable"),
        IXcommandSinglePhaseSwitch(coordinator, config_entry, api_client, "single_phase", "Single Phase Mode"),
        IXcommandBoostStateSwitch(coordinator, config_entry, "boost_state", "Boost Mode"),
    ]

    async_add_entities(entities)


class IXcommandChargingEnableSwitch(IXcommandControllableEntity, IXcommandEntity, SwitchEntity):
    """Switch for charging enable/disable."""

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        api_client: IXcommandApiClient,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the switch."""
        IXcommandEntity.__init__(self, coordinator, config_entry, entity_suffix)
        IXcommandControllableEntity.__init__(self, coordinator, api_client)
        self._attr_name = friendly_name

    @property
    def is_on(self) -> bool | None:
        """Return true if charging is enabled."""
        return self.coordinator.data.get(PROP_CHARGING_ENABLE)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on charging."""
        await self._async_control(PROP_CHARGING_ENABLE, True)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off charging."""
        await self._async_control(PROP_CHARGING_ENABLE, False)


class IXcommandSinglePhaseSwitch(IXcommandControllableEntity, IXcommandEntity, SwitchEntity):
    """Switch for single phase mode."""

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        api_client: IXcommandApiClient,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the switch."""
        IXcommandEntity.__init__(self, coordinator, config_entry, entity_suffix)
        IXcommandControllableEntity.__init__(self, coordinator, api_client)
        self._attr_name = friendly_name

    @property
    def is_on(self) -> bool | None:
        """Return true if single phase mode is enabled."""
        return self.coordinator.data.get(PROP_SINGLE_PHASE)

    async def async_turn_on(self, **kwargs) -> None:
        """Enable single phase mode."""
        await self._async_control(PROP_SINGLE_PHASE, True)

    async def async_turn_off(self, **kwargs) -> None:
        """Disable single phase mode."""
        await self._async_control(PROP_SINGLE_PHASE, False)


class IXcommandBoostStateSwitch(IXcommandEntity, SwitchEntity):
    """Read-only switch for boost state."""

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name

    @property
    def is_on(self) -> bool | None:
        """Return true if boost mode is active."""
        return self.coordinator.data.get(PROP_BOOST_STATE)

    @property
    def available(self) -> bool:
        """Return if entity is available (read-only switch is always available if coordinator is)."""
        return super().available
