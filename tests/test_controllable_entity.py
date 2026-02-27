"""Tests for controllable entity."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.ixcommand.api import IXcommandApiError
from custom_components.ixcommand.const import PROP_CHARGING_ENABLE


class TestIXcommandControllableEntity:
    """Test cases for IXcommandControllableEntity."""

    @pytest.fixture
    def controllable_entity(self):
        """Create a controllable entity for testing."""
        from custom_components.ixcommand.controllable_entity import IXcommandControllableEntity

        coordinator = MagicMock()
        coordinator.serial_number = "ABC-DEF-123"
        coordinator.data = {PROP_CHARGING_ENABLE: True}
        coordinator.async_set_updated_data = MagicMock()
        coordinator.async_request_refresh = AsyncMock()

        api_client = MagicMock()
        api_client.set_properties = AsyncMock(return_value={})

        entity = IXcommandControllableEntity.__new__(IXcommandControllableEntity)
        entity.coordinator = coordinator
        entity.api_client = api_client

        return entity

    @pytest.mark.asyncio
    async def test_async_control_success(self, controllable_entity):
        """Test successful control action."""
        with patch("custom_components.ixcommand.controllable_entity.asyncio.sleep", new_callable=AsyncMock):
            await controllable_entity._async_control(PROP_CHARGING_ENABLE, False)

            controllable_entity.api_client.set_properties.assert_called_once_with(
                "ABC-DEF-123",
                {PROP_CHARGING_ENABLE: False}
            )
            controllable_entity.coordinator.async_set_updated_data.assert_called()
            controllable_entity.coordinator.async_request_refresh.assert_called()

    @pytest.mark.asyncio
    async def test_async_control_api_error(self, controllable_entity):
        """Test control action with API error."""
        controllable_entity.api_client.set_properties = AsyncMock(
            side_effect=IXcommandApiError("API Error")
        )

        with patch("custom_components.ixcommand.controllable_entity.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(IXcommandApiError):
                await controllable_entity._async_control(PROP_CHARGING_ENABLE, False)

            controllable_entity.api_client.set_properties.assert_called_once()
            controllable_entity.coordinator.async_request_refresh.assert_not_called()

    def test_update_local_state(self, controllable_entity):
        """Test local state update."""
        controllable_entity._update_local_state(PROP_CHARGING_ENABLE, False)

        controllable_entity.coordinator.async_set_updated_data.assert_called_once()
        call_args = controllable_entity.coordinator.async_set_updated_data.call_args[0][0]
        assert call_args[PROP_CHARGING_ENABLE] is False

    def test_update_local_state_with_no_data(self, controllable_entity):
        """Test local state update with no data."""
        controllable_entity.coordinator.data = None

        controllable_entity._update_local_state(PROP_CHARGING_ENABLE, False)

        controllable_entity.coordinator.async_set_updated_data.assert_not_called()
