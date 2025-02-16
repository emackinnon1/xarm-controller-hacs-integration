"""XArmConrollerCoordinator that wraps xArm Python SDK."""

from __future__ import annotations
from typing import List, Optional, Tuple
from dataclasses import dataclass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_MODEL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from xarm.wrapper import XArmAPI

from .const import DOMAIN, LOGGER, LOGGERFORHA


@dataclass
class XArmPositionalData:
    position: Tuple[int, Optional[List[int]]]
    position_x: int
    position_y: int
    position_z: int
    roll: int
    pitch: int
    yaw: int
    servo_angle: int
    angles: str
    gripper_position: int

@dataclass
class XarmStateData:
    error_code: int
    warn_code: int
    has_error: int
    has_err_warn: int
    has_warn: int
    mode: int
    state: int
    collision_sensitivity: int
    mode: int
    gripper_err_code: int
    is_moving: int
    collision_sensitivity: int
    is_connected: int


@dataclass
class XArmData:
    positional: XArmPositionalData
    state: XarmStateData


class XArmDummyAPI:
    """Dummy class to simulate xArm API."""

    def __init__(self, host: str) -> None:
        """Initialize the dummy xArm API."""
        self.host = host


class XArmControllerCoordinator(DataUpdateCoordinator[XArmData]):
    """XArmControllerCoordinator that wraps xArm client."""

    hass: HomeAssistant
    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client: XArmAPI) -> None:
        """Initialize the XArmControllerCoordinator."""

        LOGGER.debug(f"ConfigEntry.Id: {entry.entry_id}")
        self._hass = hass
        self._entry = entry
        # self.xarm = XArmAPI(entry.data[CONF_HOST])
        self.xarm = XArmDummyAPI(entry.data[CONF_HOST])
        self.model = entry.data[CONF_MODEL]
        # self.client = XArmAPI(entry.data[CONF_HOST])


    def get_xarm_device_info(self) -> DeviceInfo:
        """Return device information about this XArm device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_entry.unique_id)},
            manufacturer="UFactory",
            name=self.model,
            model=self.model,
        )
