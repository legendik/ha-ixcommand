"""API client for iXcommand EV Charger."""

import asyncio
import logging
from typing import Any

import aiohttp

from .const import (
    ALL_READABLE_PROPERTIES,
    API_BASE_URL,
    API_TIMEOUT,
    WRITABLE_PROPERTIES,
)

_LOGGER = logging.getLogger(__name__)


class IXcommandApiError(Exception):
    """Exception raised when API call fails."""


class IXcommandApiAuthError(IXcommandApiError):
    """Exception raised when authentication fails."""


class IXcommandApiClient:
    """API client for iXcommand EV Charger."""

    def __init__(self, api_key: str, session: aiohttp.ClientSession | None = None) -> None:
        """Initialize the API client."""
        self._api_key = api_key
        self._session = session or aiohttp.ClientSession()

    async def close(self) -> None:
        """Close the HTTP session."""
        if self._session:
            await self._session.close()

    def _get_headers(self) -> dict[str, str]:
        """Get headers for API requests."""
        return {
            "X-API-KEY": self._api_key,
            "Content-Type": "application/json",
        }

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | list[tuple[str, str]] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to the API."""
        url = f"{API_BASE_URL}{endpoint}"

        try:
            async with self._session.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                json=data,
                params=params,
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT),
            ) as response:
                if response.status == 401:
                    raise IXcommandApiAuthError("Invalid API key")
                elif response.status != 200:
                    raise IXcommandApiError(
                        f"API request failed with status {response.status}: {await response.text()}"
                    )

                return await response.json()

        except aiohttp.ClientError as err:
            raise IXcommandApiError(f"HTTP client error: {err}") from err
        except asyncio.TimeoutError as err:
            raise IXcommandApiError("Request timeout") from err

    async def get_properties(
        self, serial_number: str, properties: list[str] | None = None
    ) -> dict[str, Any]:
        """Get properties from a thing (charger)."""
        if properties is None:
            properties = ALL_READABLE_PROPERTIES

        # Send keys as multiple query parameters (array format)
        # Each property becomes a separate "keys" parameter
        params = [("keys", prop) for prop in properties]
        endpoint = f"/thing/{serial_number}/properties"

        return await self._make_request("GET", endpoint, params=params)

    async def set_properties(
        self, serial_number: str, properties: dict[str, Any]
    ) -> dict[str, Any]:
        """Set properties on a thing (charger)."""
        # Validate that only writable properties are being set
        invalid_props = set(properties.keys()) - set(WRITABLE_PROPERTIES)
        if invalid_props:
            raise ValueError(f"Cannot set read-only properties: {invalid_props}")

        _LOGGER.debug("Setting properties for charger %s: %s", serial_number, properties)
        endpoint = f"/thing/{serial_number}/properties"
        result = await self._make_request("PATCH", endpoint, data=properties)
        _LOGGER.debug("Successfully set properties for charger %s", serial_number)
        return result

    async def test_connection(self, serial_number: str) -> bool:
        """Test the connection to the API by fetching basic properties."""
        try:
            # Test with a few basic properties
            await self.get_properties(
                serial_number,
                [ALL_READABLE_PROPERTIES[0]]  # Just test with first property
            )
            return True
        except IXcommandApiError:
            return False
