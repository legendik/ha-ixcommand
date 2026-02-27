"""Tests for constants and configuration."""

import pytest
from custom_components.ixcommand.const import (
    DOMAIN,
    API_BASE_URL,
    API_TIMEOUT,
    CONF_API_KEY,
    CONF_SERIAL_NUMBER,
    ALL_READABLE_PROPERTIES,
    WRITABLE_PROPERTIES,
    UPDATE_INTERVAL,
    MANUFACTURER,
    MODEL,
    CHARGING_STATUSES,
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
)


class TestConstants:
    """Test cases for constants."""

    def test_domain(self):
        """Test domain constant."""
        assert DOMAIN == "ixcommand"

    def test_api_base_url(self):
        """Test API base URL."""
        assert API_BASE_URL == "https://evcharger.ixcommand.com/api/v1"

    def test_api_timeout(self):
        """Test API timeout."""
        assert API_TIMEOUT == 10

    def test_config_keys(self):
        """Test config entry keys."""
        assert CONF_API_KEY == "api_key"
        assert CONF_SERIAL_NUMBER == "serial_number"

    def test_update_interval(self):
        """Test update interval."""
        assert UPDATE_INTERVAL == 30

    def test_manufacturer(self):
        """Test manufacturer constant."""
        assert MANUFACTURER == "iXcommand"

    def test_model(self):
        """Test model constant."""
        assert MODEL == "EV Charger"

    def test_charging_statuses(self):
        """Test charging status values."""
        expected_statuses = [
            "INIT",
            "IDLE",
            "CONNECTED",
            "CHARGING",
            "CHARGING_WITH_VENTILATION",
            "CONTROL_PILOT_ERROR",
            "ERROR",
        ]
        assert CHARGING_STATUSES == expected_statuses

    def test_all_readable_properties(self):
        """Test all readable properties list."""
        expected = [
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
        assert ALL_READABLE_PROPERTIES == expected

    def test_writable_properties(self):
        """Test writable properties list."""
        expected = [
            PROP_BOOST_CURRENT,
            PROP_TARGET_CURRENT,
            PROP_SINGLE_PHASE,
            PROP_BOOST_TIME,
            PROP_MAXIMUM_CURRENT,
            PROP_CHARGING_ENABLE,
        ]
        assert WRITABLE_PROPERTIES == expected

    def test_writable_properties_are_subset_of_readable(self):
        """Test that all writable properties are also readable."""
        for prop in WRITABLE_PROPERTIES:
            assert prop in ALL_READABLE_PROPERTIES


class TestPropertyKeys:
    """Test cases for property key constants."""

    def test_property_keys_are_strings(self):
        """Test that all property keys are non-empty strings."""
        properties = [
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
        for prop in properties:
            assert isinstance(prop, str)
            assert len(prop) > 0
