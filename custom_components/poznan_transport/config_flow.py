"""Config flow for Poznań Public Transport integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import PoznanTransportAPI
from .const import CONF_LINES, CONF_STOP_NAME, CONF_STOP_SYMBOL, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def validate_stop(hass: HomeAssistant, stop_symbol: str) -> dict[str, str]:
    """Validate the stop symbol by making an API call."""
    session = async_get_clientsession(hass)
    api = PoznanTransportAPI(session)

    try:
        data = await api.get_departures(stop_symbol)
        
        if not data or "bollard" not in data:
            raise ValueError("Invalid stop symbol")

        bollard = data["bollard"]
        return {
            "name": bollard.get("name", "Unknown"),
            "symbol": bollard.get("symbol", stop_symbol),
        }

    except Exception as err:
        _LOGGER.error("Error validating stop: %s", err)
        raise


class PoznanTransportConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Poznań Public Transport."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            stop_symbol = user_input[CONF_STOP_SYMBOL].strip().upper()

            try:
                info = await validate_stop(self.hass, stop_symbol)
                
                # Create unique ID based on stop symbol
                await self.async_set_unique_id(stop_symbol)
                self._abort_if_unique_id_configured()

                # Parse lines filter (comma-separated)
                lines_input = user_input.get(CONF_LINES, "").strip()
                lines = [line.strip() for line in lines_input.split(",") if line.strip()]

                return self.async_create_entry(
                    title=f"{info['name']} ({stop_symbol})",
                    data={
                        CONF_STOP_SYMBOL: stop_symbol,
                        CONF_STOP_NAME: info["name"],
                        CONF_LINES: lines,
                    },
                )

            except ValueError:
                errors["base"] = "invalid_stop"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_STOP_SYMBOL): str,
                    vol.Optional(CONF_LINES, default=""): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "stop_example": "NIED01",
                "lines_example": "171, 172, 173",
            },
        )

