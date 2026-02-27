"""Tests for the iXcommand API client."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.ixcommand.api import (
    IXcommandApiClient,
    IXcommandApiError,
    IXcommandApiAuthError,
)
from custom_components.ixcommand.const import (
    PROP_CHARGING_ENABLE,
    PROP_TARGET_CURRENT,
    PROP_SINGLE_PHASE,
)


class TestIXcommandApiClient:
    """Test cases for IXcommandApiClient."""

    @pytest.fixture
    def client(self):
        """Create a client with mocked session."""
        with patch("aiohttp.ClientSession") as mock_session:
            mock_session.return_value.request = AsyncMock()
            client = IXcommandApiClient("test_api_key")
            client._session = MagicMock()
            yield client

    @pytest.mark.asyncio
    async def test_get_headers(self, client):
        """Test that headers are correctly generated."""
        headers = client._get_headers()
        assert headers["X-API-KEY"] == "test_api_key"
        assert headers["Content-Type"] == "application/json"

    @pytest.mark.asyncio
    async def test_get_properties_success(self, client):
        """Test successful get_properties call."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "chargingEnable": True,
            "targetCurrent": 16,
        })
        client._session.request = AsyncMock(return_value=mock_response)

        result = await client.get_properties("ABC-DEF-123", ["chargingEnable", "targetCurrent"])

        assert result == {"chargingEnable": True, "targetCurrent": 16}
        client._session.request.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_properties_auth_error(self, client):
        """Test get_properties with authentication error."""
        mock_response = AsyncMock()
        mock_response.status = 401
        mock_response.text = AsyncMock(return_value="Unauthorized")
        client._session.request = AsyncMock(return_value=mock_response)

        with pytest.raises(IXcommandApiAuthError, match="Invalid API key"):
            await client.get_properties("ABC-DEF-123", ["chargingEnable"])

    @pytest.mark.asyncio
    async def test_get_properties_api_error(self, client):
        """Test get_properties with API error."""
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.text = AsyncMock(return_value="Internal Server Error")
        client._session.request = AsyncMock(return_value=mock_response)

        with pytest.raises(IXcommandApiError):
            await client.get_properties("ABC-DEF-123", ["chargingEnable"])

    @pytest.mark.asyncio
    async def test_set_properties_success(self, client):
        """Test successful set_properties call."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"success": True})
        client._session.request = AsyncMock(return_value=mock_response)

        result = await client.set_properties(
            "ABC-DEF-123",
            {PROP_CHARGING_ENABLE: True, PROP_TARGET_CURRENT: 16}
        )

        assert result == {"success": True}
        client._session.request.assert_called_once()

        call_args = client._session.request.call_args
        assert call_args.kwargs["json"] == {PROP_CHARGING_ENABLE: True, PROP_TARGET_CURRENT: 16}

    @pytest.mark.asyncio
    async def test_set_properties_readonly_error(self, client):
        """Test set_properties with read-only property."""
        with pytest.raises(ValueError, match="Cannot set read-only properties"):
            await client.set_properties("ABC-DEF-123", {"totalEnergy": 1000})

    @pytest.mark.asyncio
    async def test_set_properties_invalid_property(self, client):
        """Test set_properties with invalid property."""
        with pytest.raises(ValueError, match="Cannot set read-only properties"):
            await client.set_properties("ABC-DEF-123", {"invalidProperty": "value"})

    @pytest.mark.asyncio
    async def test_test_connection_success(self, client):
        """Test successful connection test."""
        client.get_properties = AsyncMock(return_value={"chargingEnable": True})

        result = await client.test_connection("ABC-DEF-123")

        assert result is True
        client.get_properties.assert_called_once()

    @pytest.mark.asyncio
    async def test_test_connection_failure(self, client):
        """Test failed connection test."""
        client.get_properties = AsyncMock(side_effect=IXcommandApiError("Connection failed"))

        result = await client.test_connection("ABC-DEF-123")

        assert result is False

    @pytest.mark.asyncio
    async def test_close(self, client):
        """Test close method."""
        client._session.close = AsyncMock()
        await client.close()
        client._session.close.assert_called_once()


class TestIXcommandApiExceptions:
    """Test cases for API exceptions."""

    def test_auth_error_inheritance(self):
        """Test that IXcommandApiAuthError inherits from IXcommandApiError."""
        assert issubclass(IXcommandApiAuthError, IXcommandApiError)

    def test_auth_error_can_be_caught_as_api_error(self):
        """Test that IXcommandApiAuthError can be caught as IXcommandApiError."""
        with pytest.raises(IXcommandApiError):
            raise IXcommandApiAuthError("Auth failed")
