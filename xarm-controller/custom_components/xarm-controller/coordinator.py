"""XArmContollerCoordinator that wraps xArm Python SDK."""

from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant

from xarm.wrapper import XArmAPI


class XArmContollerCoordinator:

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the XArmControllerCoordinator."""
        self.xarm = XArmAPI(entry.data[CONF_HOST], session=async_get_clientsession(hass))
        return True
