"""Poznań Public Transport integration for Home Assistant."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import PoznanTransportCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Poznań Public Transport component."""
    await _async_setup_lovelace_card(hass)
    return True


async def _async_setup_lovelace_card(hass: HomeAssistant) -> None:
    """Copy Lovelace card to www folder."""
    try:
        source = Path(__file__).parent / "poznan-transport-card.js"
        target_dir = Path(hass.config.path("www/community/poznan-transport-card"))
        target = target_dir / "poznan-transport-card.js"
        
        target_dir.mkdir(parents=True, exist_ok=True)
        
        if source.exists():
            await hass.async_add_executor_job(shutil.copy2, str(source), str(target))
            _LOGGER.info("Copied Lovelace card to %s", target)
        else:
            _LOGGER.warning("Lovelace card source file not found at %s", source)
    except Exception as err:
        _LOGGER.error("Error copying Lovelace card: %s", err)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Poznań Public Transport from a config entry."""
    coordinator = PoznanTransportCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

