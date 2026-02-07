"""Sensor platform for Poznań Public Transport."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_AIR_CONDITIONING,
    ATTR_BIKE,
    ATTR_DEPARTURE,
    ATTR_DIRECTION,
    ATTR_LINE,
    ATTR_LOW_FLOOR,
    ATTR_MINUTES,
    ATTR_REAL_TIME,
    ATTR_STOP_NAME,
    ATTR_STOP_SYMBOL,
    ATTR_VEHICLE,
    CONF_STOP_NAME,
    CONF_STOP_SYMBOL,
    DOMAIN,
)
from .coordinator import PoznanTransportCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Poznań Public Transport sensor based on a config entry."""
    coordinator: PoznanTransportCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            PoznanTransportNextDepartureSensor(coordinator, entry),
            PoznanTransportDeparturesSensor(coordinator, entry),
        ]
    )


class PoznanTransportNextDepartureSensor(CoordinatorEntity, SensorEntity):
    """Sensor showing the next departure."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:bus-clock"

    def __init__(
        self, coordinator: PoznanTransportCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_next_departure"
        self._attr_name = "Next Departure"
        self._stop_name = entry.data[CONF_STOP_NAME]
        self._stop_symbol = entry.data[CONF_STOP_SYMBOL]

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or "times" not in self.coordinator.data:
            return None

        times = self.coordinator.data["times"]
        if not times:
            return "No departures"

        next_departure = times[0]
        minutes = next_departure.get("minutes", 0)
        line = next_departure.get("line", "?")

        if minutes == 0:
            return f"Line {line} - Now"
        elif minutes == 1:
            return f"Line {line} - 1 min"
        else:
            return f"Line {line} - {minutes} min"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if not self.coordinator.data or "times" not in self.coordinator.data:
            return {}

        times = self.coordinator.data["times"]
        if not times:
            return {
                ATTR_STOP_NAME: self._stop_name,
                ATTR_STOP_SYMBOL: self._stop_symbol,
            }

        next_departure = times[0]

        return {
            ATTR_STOP_NAME: self._stop_name,
            ATTR_STOP_SYMBOL: self._stop_symbol,
            ATTR_LINE: next_departure.get("line"),
            ATTR_DIRECTION: next_departure.get("direction"),
            ATTR_MINUTES: next_departure.get("minutes"),
            ATTR_DEPARTURE: next_departure.get("departure"),
            ATTR_REAL_TIME: next_departure.get("realTime"),
            ATTR_VEHICLE: next_departure.get("vehicle"),
            ATTR_BIKE: next_departure.get("bike"),
            ATTR_AIR_CONDITIONING: next_departure.get("airCnd"),
            ATTR_LOW_FLOOR: next_departure.get("lowFloorBus") or next_departure.get("lfRamp"),
        }


class PoznanTransportDeparturesSensor(CoordinatorEntity, SensorEntity):
    """Sensor showing all departures."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:bus-multiple"

    def __init__(
        self, coordinator: PoznanTransportCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_departures"
        self._attr_name = "All Departures"
        self._stop_name = entry.data[CONF_STOP_NAME]
        self._stop_symbol = entry.data[CONF_STOP_SYMBOL]

    @property
    def native_value(self) -> int:
        """Return the number of departures."""
        if not self.coordinator.data or "times" not in self.coordinator.data:
            return 0

        return len(self.coordinator.data["times"])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if not self.coordinator.data or "times" not in self.coordinator.data:
            return {
                ATTR_STOP_NAME: self._stop_name,
                ATTR_STOP_SYMBOL: self._stop_symbol,
                "departures": [],
            }

        times = self.coordinator.data["times"]
        
        # Format departures for display
        departures = []
        for time in times[:10]:  # Limit to 10 departures
            departures.append({
                "line": time.get("line"),
                "direction": time.get("direction"),
                "minutes": time.get("minutes"),
                "departure": time.get("departure"),
                "real_time": time.get("realTime"),
                "vehicle": time.get("vehicle"),
                "bike": time.get("bike"),
                "air_conditioning": time.get("airCnd"),
                "low_floor": time.get("lowFloorBus") or time.get("lfRamp"),
            })

        return {
            ATTR_STOP_NAME: self._stop_name,
            ATTR_STOP_SYMBOL: self._stop_symbol,
            "departures": departures,
        }

