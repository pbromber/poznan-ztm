"""Data coordinator for Poznań Public Transport."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import PoznanTransportAPI
from .const import CONF_LINES, CONF_STOP_SYMBOL, DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class PoznanTransportCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Data coordinator for Poznań Public Transport."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.stop_symbol = entry.data[CONF_STOP_SYMBOL]
        self.lines_filter = entry.data.get(CONF_LINES, [])
        
        session = async_get_clientsession(hass)
        self.api = PoznanTransportAPI(session)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            data = await self.api.get_departures(self.stop_symbol)

            if not data:
                raise UpdateFailed("No data received from API")

            # Filter by lines if specified
            if self.lines_filter:
                times = data.get("times", [])
                filtered_times = [
                    time for time in times 
                    if time.get("line") in self.lines_filter
                ]
                data["times"] = filtered_times

            return data

        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err

