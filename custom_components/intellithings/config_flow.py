"""Config flow: base URL + device token, validated against /discovery."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import IntelliThingsApi, IntelliThingsAuthError, IntelliThingsError
from .const import CONF_BASE_URL, CONF_TOKEN, DOMAIN

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BASE_URL): str,
        vol.Required(CONF_TOKEN): str,
    }
)


class IntelliThingsConfigFlow(ConfigFlow, domain=DOMAIN):
    """One entry per device."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            base_url = user_input[CONF_BASE_URL].strip().rstrip("/")
            token = user_input[CONF_TOKEN].strip()

            api = IntelliThingsApi(async_get_clientsession(self.hass), base_url, token)
            try:
                discovery = await api.discovery()
            except IntelliThingsAuthError:
                errors["base"] = "invalid_auth"
            except IntelliThingsError:
                errors["base"] = "cannot_connect"
            else:
                device = discovery.get("device", {})
                identifier = device.get("identifier")
                if not identifier:
                    errors["base"] = "unknown"
                else:
                    # Keyed on the serial number, so re-adding the same device
                    # after regenerating its token updates the existing entry
                    # instead of creating a duplicate set of entities.
                    await self.async_set_unique_id(identifier)
                    self._abort_if_unique_id_configured(
                        updates={CONF_BASE_URL: base_url, CONF_TOKEN: token}
                    )
                    return self.async_create_entry(
                        title=device.get("name") or identifier,
                        data={CONF_BASE_URL: base_url, CONF_TOKEN: token},
                    )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_SCHEMA, errors=errors
        )

    async def async_step_reauth(
        self, entry_data: dict[str, Any]
    ) -> ConfigFlowResult:
        """Triggered when a token is revoked or the plugin is switched off."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        entry = self._get_reauth_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            token = user_input[CONF_TOKEN].strip()
            api = IntelliThingsApi(
                async_get_clientsession(self.hass), entry.data[CONF_BASE_URL], token
            )
            try:
                await api.discovery()
            except IntelliThingsAuthError:
                errors["base"] = "invalid_auth"
            except IntelliThingsError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_update_reload_and_abort(
                    entry, data_updates={CONF_TOKEN: token}
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({vol.Required(CONF_TOKEN): str}),
            errors=errors,
            description_placeholders={"name": entry.title},
        )
