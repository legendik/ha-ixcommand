"""Tests for constants and configuration."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import directly from the const module (avoids __init__.py which imports homeassistant)
from custom_components.ixcommand import const


class TestConstants:
    """Test cases for constants."""

    def test_domain(self):
        """Test domain constant."""
        assert const.DOMAIN == "ixcommand"

    def test_api_base_url(self):
        """Test API base URL."""
        assert const.API_BASE_URL == "https://evcharger.ixcommand.com/api/v1"

    def test_api_timeout(self):
        """Test API timeout."""
        assert const.API_TIMEOUT == 10

    def test_config_keys(self):
        """Test config entry keys."""
        assert const.CONF_API_KEY == "api_key"
        assert const.CONF_SERIAL_NUMBER == "serial_number"

    def test_update_interval(self):
        """Test update interval."""
        assert const.UPDATE_INTERVAL == 30

    def test_manufacturer(self):
        """Test manufacturer constant."""
        assert const.MANUFACTURER == "iXcommand"

    def test_model(self):
        """Test model constant."""
        assert const.MODEL == "EV Charger"

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
        assert const.CHARGING_STATUSES == expected_statuses

    def test_all_readable_properties(self):
        """Test all readable properties list."""
        assert len(const.ALL_READABLE_PROPERTIES) > 0
        for prop in const.ALL_READABLE_PROPERTIES:
            assert isinstance(prop, str)

    def test_writable_properties(self):
        """Test writable properties list."""
        assert len(const.WRITABLE_PROPERTIES) > 0
        for prop in const.WRITABLE_PROPERTIES:
            assert isinstance(prop, str)

    def test_writable_properties_are_subset_of_readable(self):
        """Test that all writable properties are also readable."""
        for prop in const.WRITABLE_PROPERTIES:
            assert prop in const.ALL_READABLE_PROPERTIES


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
