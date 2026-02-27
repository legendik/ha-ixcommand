"""Constants for the iXcommand EV Charger integration."""

DOMAIN = "ixcommand"

# API Configuration
API_BASE_URL = "https://evcharger.ixcommand.com/api/v1"
API_TIMEOUT = 10

# Config entry keys
CONF_API_KEY = "api_key"
CONF_SERIAL_NUMBER = "serial_number"

# API property keys
PROP_BOOST_CURRENT = "boostCurrent"
PROP_TARGET_CURRENT = "targetCurrent"
PROP_SINGLE_PHASE = "singlePhase"
PROP_BOOST_TIME = "boostTime"
PROP_MAXIMUM_CURRENT = "maximumCurrent"
PROP_CHARGING_ENABLE = "chargingEnable"
PROP_CHARGING_CURRENT = "chargingCurrent"
PROP_BOOST_REMAINING = "boostRemaining"
PROP_CHARGING_STATE = "chargingState"
PROP_SIGNAL = "signal"
PROP_BOOST_STATE = "boostState"
PROP_TOTAL_ENERGY = "totalEnergy"
PROP_CURRENT_CHARGING_POWER = "currentChargingPower"
PROP_CHARGING_CURRENT_L2 = "chargingCurrentL2"
PROP_CHARGING_CURRENT_L3 = "chargingCurrentL3"
PROP_CHARGING_STATUS = "chargingStatus"
PROP_SSID = "ssid"
PROP_BSSID = "bssid"

# All readable properties for efficient API calls
ALL_READABLE_PROPERTIES = [
    PROP_BOOST_CURRENT,
    PROP_TARGET_CURRENT,
    PROP_SINGLE_PHASE,
    PROP_BOOST_TIME,
    PROP_MAXIMUM_CURRENT,
    PROP_CHARGING_ENABLE,
    PROP_CHARGING_CURRENT,
    PROP_BOOST_REMAINING,
    PROP_CHARGING_STATE,
    PROP_SIGNAL,
    PROP_BOOST_STATE,
    PROP_TOTAL_ENERGY,
    PROP_CURRENT_CHARGING_POWER,
    PROP_CHARGING_CURRENT_L2,
    PROP_CHARGING_CURRENT_L3,
    PROP_CHARGING_STATUS,
    PROP_SSID,
    PROP_BSSID,
]

# Writable properties
WRITABLE_PROPERTIES = [
    PROP_BOOST_CURRENT,
    PROP_TARGET_CURRENT,
    PROP_SINGLE_PHASE,
    PROP_BOOST_TIME,
    PROP_MAXIMUM_CURRENT,
    PROP_CHARGING_ENABLE,
]

# Polling interval
UPDATE_INTERVAL = 30  # seconds

# Device info
MANUFACTURER = "iXcommand"
MODEL = "EV Charger"

# Charging status values
CHARGING_STATUSES = [
    "INIT",
    "IDLE",
    "CONNECTED",
    "CHARGING",
    "CHARGING_WITH_VENTILATION",
    "CONTROL_PILOT_ERROR",
    "ERROR",
]