"""XArmConrollerCoordinator that wraps xArm Python SDK."""

from __future__ import annotations
from typing import List, Optional, Tuple
from dataclasses import dataclass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_MODEL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from xarm.wrapper import XArmAPI


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

    @property
    def host(self) -> str:
        """Return the host of the dummy xArm API."""
        return self._host

    @host.setter
    def host(self, host: str) -> None:
        """Set the host of the dummy xArm API."""
        self._host = host


class XArmControllerCoordinator(DataUpdateCoordinator[XArmData]):
    """XArmControllerCoordinator that wraps xArm Python SDK."""
    hass: HomeAssistant
    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client: XArmAPI) -> None:
        """Initialize the XArmControllerCoordinator."""
        self.config_entry = entry
        # self.xarm = XArmAPI(entry.data[CONF_HOST])
        self.xarm = XArmDummyAPI(entry.data[CONF_HOST])
        self.model = entry.data[CONF_MODEL]


    def _async_update_data(self) -> int:

