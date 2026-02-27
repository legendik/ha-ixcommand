"""Pytest fixtures for iXcommand tests."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    with patch("custom_components.ixcommand.api.IXcommandApiClient") as mock:
        client = MagicMock()
        client.get_properties = AsyncMock(return_value={
            "chargingCurrent": 16,
            "targetCurrent": 16,
            "maximumCurrent": 16,
            "chargingEnable": True,
            "singlePhase": False,
            "boostState": False,
            "boostCurrent": 16,
            "boostTime": 0,
            "boostRemaining": 0,
            "totalEnergy": 12345,
            "currentChargingPower": 0,
            "chargingCurrentL2": 0,
            "chargingCurrentL3": 0,
            "chargingStatus": "IDLE",
            "signal": -50,
            "ssid": "TestNetwork",
            "bssid": "00:11:22:33:44:55",
        })
        client.set_properties = AsyncMock(return_value={})
        client.test_connection = AsyncMock(return_value=True)
        client.close = AsyncMock()
        mock.return_value = client
        yield client


@pytest.fixture
def mock_coordinator():
    """Create a mock coordinator."""
    with patch("custom_components.ixcommand.coordinator.DataUpdateCoordinator") as mock:
        coordinator = MagicMock()
        coordinator.data = {
            "chargingCurrent": 16,
            "targetCurrent": 16,
            "maximumCurrent": 16,
            "chargingEnable": True,
            "singlePhase": False,
            "boostState": False,
            "boostCurrent": 16,
            "boostTime": 0,
            "boostRemaining": 0,
            "totalEnergy": 12345,
            "currentChargingPower": 0,
            "chargingCurrentL2": 0,
            "chargingCurrentL3": 0,
            "chargingStatus": "IDLE",
            "signal": -50,
            "ssid": "TestNetwork",
            "bssid": "00:11:22:33:44:55",
        }
        coordinator.serial_number = "ABC-DEF-123"
        coordinator.async_request_refresh = AsyncMock()
        coordinator.async_set_updated_data = MagicMock()
        mock.return_value = coordinator
        yield coordinator


@pytest.fixture
def mock_config_entry():
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.data = {
        "api_key": "test_api_key",
        "serial_number": "ABC-DEF-123",
    }
    return entry


@pytest.fixture
def mock_hass():
    """Create a mock hass object."""
    hass = MagicMock()
    hass.data = {}
    return hass
