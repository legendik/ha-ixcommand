"""Config flow for iXcommand EV Charger integration."""

import voluptuous as vol
from homeassistant import config_entries

from .api import IXcommandApiAuthError, IXcommandApiClient, IXcommandApiError
from .const import CONF_API_KEY, CONF_SERIAL_NUMBER, DOMAIN


class IXcommandConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]
    """Handle a config flow for iXcommand EV Charger."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate the serial number format
                serial = user_input[CONF_SERIAL_NUMBER]
                if not self._validate_serial_format(serial):
                    errors[CONF_SERIAL_NUMBER] = "invalid_serial_format"
                else:
                    # Test the connection
                    api_client = IXcommandApiClient(user_input[CONF_API_KEY])
                    try:
                        await api_client.test_connection(serial)
                    finally:
                        await api_client.close()

                    # Create the config entry
                    await self.async_set_unique_id(serial)
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title=f"iXcommand Charger {serial}",
                        data={
                            CONF_API_KEY: user_input[CONF_API_KEY],
                            CONF_SERIAL_NUMBER: user_input[CONF_SERIAL_NUMBER],
                        },
                    )

            except IXcommandApiAuthError:
                errors["base"] = "invalid_auth"
            except IXcommandApiError:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_SERIAL_NUMBER): str,
                }
            ),
            errors=errors,
        )

    def _validate_serial_format(self, serial: str) -> bool:
        """Validate the serial number format (XXX-XXX-XXX)."""
        parts = serial.split("-")
        if len(parts) != 3:
            return False
        return all(len(part) == 3 and part.isalnum() for part in parts)

    async def async_step_reauth(
        self, entry_data: dict[str, str]
    ) -> config_entries.FlowResult:
        """Handle reauth flow."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, str] | None = None
    ) -> config_entries.FlowResult:
        """Handle reauth confirmation."""
        errors = {}

        if user_input is not None:
            try:
                # Test the connection with new credentials
                api_client = IXcommandApiClient(user_input[CONF_API_KEY])
                try:
                    await api_client.test_connection(self.context["serial_number"])
                finally:
                    await api_client.close()

                # Update the existing entry
                existing_entry = self.hass.config_entries.async_get_entry(
                    self.context["entry_id"]
                )
                self.hass.config_entries.async_update_entry(
                    existing_entry,
                    data={
                        **existing_entry.data,
                        CONF_API_KEY: user_input[CONF_API_KEY],
                    },
                )

                return self.async_abort(reason="reauth_successful")

            except IXcommandApiAuthError:
                errors["base"] = "invalid_auth"
            except IXcommandApiError:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "serial": self.context["serial_number"]
            },
        )
