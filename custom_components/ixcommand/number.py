"""Number entities for iXcommand EV Charger."""

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import IXcommandApiClient
from .const import (
    PROP_BOOST_CURRENT,
    PROP_BOOST_TIME,
    PROP_MAXIMUM_CURRENT,
    PROP_TARGET_CURRENT,
)
from .controllable_entity import IXcommandControllableEntity
from .coordinator import IXcommandCoordinator
from .entity import IXcommandEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the iXcommand number entities."""
    coordinator: IXcommandCoordinator = hass.data["ixcommand"][config_entry.entry_id]["coordinator"]
    api_client: IXcommandApiClient = hass.data["ixcommand"][config_entry.entry_id]["api_client"]

    entities = [
        IXcommandTargetCurrentNumber(coordinator, config_entry, api_client, "target_current", "Target Current"),
        IXcommandBoostCurrentNumber(coordinator, config_entry, api_client, "boost_current", "Boost Current"),
        IXcommandMaximumCurrentNumber(coordinator, config_entry, api_client, "maximum_current", "Maximum Current"),
        IXcommandBoostTimeNumber(coordinator, config_entry, api_client, "boost_time", "Boost Time"),
    ]

    async_add_entities(entities)


class IXcommandTargetCurrentNumber(IXcommandControllableEntity, IXcommandEntity, NumberEntity):
    """Number entity for target charging current."""

    _attr_mode = NumberMode.SLIDER
    _attr_native_min_value = 6
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "A"
    _property_key = PROP_TARGET_CURRENT

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        api_client: IXcommandApiClient,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the number entity."""
        IXcommandEntity.__init__(self, coordinator, config_entry, entity_suffix)
        IXcommandControllableEntity.__init__(self, coordinator, api_client)

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
        await self._async_control(self._property_key, int(value))


class IXcommandBoostCurrentNumber(IXcommandControllableEntity, IXcommandEntity, NumberEntity):
    """Number entity for boost charging current."""

    _attr_mode = NumberMode.SLIDER
    _attr_native_min_value = 6
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "A"
    _property_key = PROP_BOOST_CURRENT

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        api_client: IXcommandApiClient,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the number entity."""
        IXcommandEntity.__init__(self, coordinator, config_entry, entity_suffix)
        IXcommandControllableEntity.__init__(self, coordinator, api_client)

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
        await self._async_control(self._property_key, int(value))


class IXcommandMaximumCurrentNumber(IXcommandControllableEntity, IXcommandEntity, NumberEntity):
    """Number entity for maximum allowed charging current."""

    _attr_mode = NumberMode.SLIDER
    _attr_native_min_value = 6
    _attr_native_max_value = 16
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "A"
    _property_key = PROP_MAXIMUM_CURRENT

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        api_client: IXcommandApiClient,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the number entity."""
        IXcommandEntity.__init__(self, coordinator, config_entry, entity_suffix)
        IXcommandControllableEntity.__init__(self, coordinator, api_client)

    @property
    def native_value(self) -> float | None:
        """Return the current maximum current."""
        return self.coordinator.data.get(PROP_MAXIMUM_CURRENT)

    async def async_set_native_value(self, value: float) -> None:
        """Set the maximum current."""
        await self._async_control(self._property_key, int(value))


class IXcommandBoostTimeNumber(IXcommandControllableEntity, IXcommandEntity, NumberEntity):
    """Number entity for boost time duration."""

    _attr_mode = NumberMode.SLIDER
    _attr_native_min_value = 0
    _attr_native_max_value = 86400
    _attr_native_step = 60
    _attr_native_unit_of_measurement = "s"
    _property_key = PROP_BOOST_TIME

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        api_client: IXcommandApiClient,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the number entity."""
        IXcommandEntity.__init__(self, coordinator, config_entry, entity_suffix)
        IXcommandControllableEntity.__init__(self, coordinator, api_client)

    @property
    def native_value(self) -> float | None:
        """Return the current boost time."""
        return self.coordinator.data.get(PROP_BOOST_TIME)

    async def async_set_native_value(self, value: float) -> None:
        """Set the boost time."""
        await self._async_control(self._property_key, int(value))
