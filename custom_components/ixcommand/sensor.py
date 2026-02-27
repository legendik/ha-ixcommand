"""Sensor entities for iXcommand EV Charger."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CHARGING_STATUSES,
    PROP_BOOST_REMAINING,
    PROP_BSSID,
    PROP_CHARGING_CURRENT,
    PROP_CHARGING_CURRENT_L2,
    PROP_CHARGING_CURRENT_L3,
    PROP_CHARGING_STATUS,
    PROP_CURRENT_CHARGING_POWER,
    PROP_SIGNAL,
    PROP_SSID,
    PROP_TOTAL_ENERGY,
)
from .coordinator import IXcommandCoordinator
from .entity import IXcommandEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the iXcommand sensors."""
    coordinator: IXcommandCoordinator = hass.data["ixcommand"][config_entry.entry_id]["coordinator"]

    entities = [
        # Power and energy sensors
        IXcommandPowerSensor(coordinator, config_entry, "current_charging_power", "Current Charging Power"),
        IXcommandEnergySensor(coordinator, config_entry, "total_energy", "Total Energy"),

        # Current sensors
        IXcommandCurrentSensor(coordinator, config_entry, "charging_current_l1", "Charging Current L1", PROP_CHARGING_CURRENT),
        IXcommandCurrentSensor(coordinator, config_entry, "charging_current_l2", "Charging Current L2", PROP_CHARGING_CURRENT_L2),
        IXcommandCurrentSensor(coordinator, config_entry, "charging_current_l3", "Charging Current L3", PROP_CHARGING_CURRENT_L3),

        # Other sensors
        IXcommandDurationSensor(coordinator, config_entry, "boost_remaining", "Boost Remaining"),
        IXcommandSignalStrengthSensor(coordinator, config_entry, "wifi_signal", "WiFi Signal"),
        IXcommandChargingStatusSensor(coordinator, config_entry, "charging_status", "Charging Status"),
        IXcommandTextSensor(coordinator, config_entry, "wifi_ssid", "WiFi SSID", PROP_SSID),
        IXcommandTextSensor(coordinator, config_entry, "wifi_bssid", "WiFi BSSID", PROP_BSSID),
    ]

    async_add_entities(entities)


class IXcommandPowerSensor(IXcommandEntity, SensorEntity):
    """Sensor for current charging power."""

    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "W"
    _attr_suggested_display_precision = 0

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name

    @property
    def native_value(self) -> float | None:
        """Return the current charging power."""
        return self.coordinator.data.get(PROP_CURRENT_CHARGING_POWER)


class IXcommandEnergySensor(IXcommandEntity, SensorEntity):
    """Sensor for total energy consumption."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = "Wh"
    _attr_suggested_display_precision = 0

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name

    @property
    def native_value(self) -> int | None:
        """Return the total energy consumption."""
        return self.coordinator.data.get(PROP_TOTAL_ENERGY)


class IXcommandCurrentSensor(IXcommandEntity, SensorEntity):
    """Sensor for charging current."""

    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "A"
    _attr_suggested_display_precision = 1

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        entity_suffix: str,
        friendly_name: str,
        property_key: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name
        self._property_key = property_key

    @property
    def native_value(self) -> float | None:
        """Return the charging current."""
        return self.coordinator.data.get(self._property_key)


class IXcommandDurationSensor(IXcommandEntity, SensorEntity):
    """Sensor for boost remaining time."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "s"
    _attr_suggested_display_precision = 0

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name

    @property
    def native_value(self) -> int | None:
        """Return the boost remaining time."""
        return self.coordinator.data.get(PROP_BOOST_REMAINING)


class IXcommandSignalStrengthSensor(IXcommandEntity, SensorEntity):
    """Sensor for WiFi signal strength."""

    _attr_native_unit_of_measurement = "%"
    _attr_suggested_display_precision = 0

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name

    @property
    def native_value(self) -> int | None:
        """Return the WiFi signal strength."""
        return self.coordinator.data.get(PROP_SIGNAL)


class IXcommandChargingStatusSensor(IXcommandEntity, SensorEntity):
    """Sensor for charging status."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = CHARGING_STATUSES

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        entity_suffix: str,
        friendly_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name

    @property
    def native_value(self) -> str | None:
        """Return the charging status."""
        return self.coordinator.data.get(PROP_CHARGING_STATUS)


class IXcommandTextSensor(IXcommandEntity, SensorEntity):
    """Sensor for text values like SSID/BSSID."""

    def __init__(
        self,
        coordinator: IXcommandCoordinator,
        config_entry: ConfigEntry,
        entity_suffix: str,
        friendly_name: str,
        property_key: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, entity_suffix)
        self._attr_name = friendly_name
        self._property_key = property_key

    @property
    def native_value(self) -> str | None:
        """Return the text value."""
        return self.coordinator.data.get(self._property_key)
