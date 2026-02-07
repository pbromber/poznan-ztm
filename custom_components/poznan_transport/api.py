"""API client for Poznań Public Transport."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp

from .const import API_TIMEOUT, API_URL

_LOGGER = logging.getLogger(__name__)


class PoznanTransportAPI:
    """API client for Poznań Public Transport."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    async def get_departures(self, stop_symbol: str) -> dict[str, Any]:
        """Get departure times for a stop."""
        headers = {
            "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        data = f'method=getTimes&p0={{"symbol":"{stop_symbol}"}}'

        try:
            async with self._session.post(
                API_URL,
                headers=headers,
                data=data,
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT),
            ) as response:
                response.raise_for_status()
                result = await response.json()

                if "success" not in result:
                    _LOGGER.error("Invalid API response: %s", result)
                    return {}

                return result["success"]

        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching data from API: %s", err)
            raise
        except Exception as err:
            _LOGGER.exception("Unexpected error: %s", err)
            raise

