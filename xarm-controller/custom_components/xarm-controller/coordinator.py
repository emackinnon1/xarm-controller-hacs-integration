"""XArmConrollerCoordinator that wraps xArm Python SDK."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_SERIAL_NUMBER,
    CONF_HOST,
    CONF_MODEL,
    EVENT_HOMEASSISTANT_STOP,
    Platform,
)
from homeassistant.core import HomeAssistant, Event, callback
from homeassistant.helpers import device_registry
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .models import XArmData

from xarm.wrapper import XArmAPI

from .const import (
    DOMAIN,
    LOGGER,
    LOGGERFORHA,
    API_ERRORS,
    GRIPPER_ERROR_CODES,
    WARN_CODES,
    MODES,
    STATES,
    MOVE_ARM_EVENT
)
from .dummy import XArmDummyAPI


class XArmControllerUpdateCoordinator(DataUpdateCoordinator[XArmData]):
    """XArmControllerUpdateCoordinator that wraps xArm client."""

    hass: HomeAssistant
    config_entry: ConfigEntry
    _updatedDevice: bool

    def __init__(
        self, hass: HomeAssistant, *, entry: ConfigEntry
    ) -> None:
        """Initialize the XArmControllerUpdateCoordinator."""

        LOGGER.debug(f"ConfigEntry.Id: {entry.entry_id}")
        self._entry = entry
        config = entry.data.copy()
        # self.xarm = XArmAPI(entry.data[CONF_HOST])

        self._updatedDevice = False
        self._shutdown = False
        # self.data = self.get_xarm_model()
        # Pass LOGGERFORHA logger into HA as otherwise it generates a debug output line every single time we tell it we have an update
        # which fills the logs and makes the useful logging data less accessible.
        super().__init__(hass=hass, config_entry=entry, logger=LOGGERFORHA, name=DOMAIN)

        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self._async_shutdown)
        self.xarm_client = XArmDummyAPI(self)
        self.xarm_data_model = XArmData(xarm_client=self.xarm_client, callback=self.event_handler)

    def get_xarm_model(self) -> XArmData:
        """Return the XArm device."""
        return self.xarm_data_model

    def get_xarm_model_info(self) -> DeviceInfo:
        """Return device information about this XArm device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_entry[ATTR_SERIAL_NUMBER])},
            manufacturer="UFactory",
            name=self.xarm,
            model=self.model,
            ip_address=self.config_entry["host"],
        )

    @callback
    def _async_shutdown(self, event: Event) -> None:
        """Call when Home Assistant is stopping."""
        LOGGER.debug(f"HOME ASSISTANT IS SHUTTING DOWN")
        self.shutdown()

    def shutdown(self) -> None:
        """Halt the MQTT listener thread"""
        self._shutdown = True
        self.xarm_client.disconnect()

    def _service_call_is_for_me(self, data: dict) -> bool:
        """Check if the service call is for this device."""
        dev_reg = device_registry.async_get(self.hass)
        hadevice = dev_reg.async_get_device(identifiers={(DOMAIN, self.get_xarm_model().info.serial)})
        device_id = data.get("device_id", [])
        if len(device_id) != 1:
            LOGGER.error("Invalid skip objects data payload: {data}")
            return False

        return device_id[0] == hadevice.id

    def event_handler(self, event: dict) -> None:
        """Handle events having to do with the xArm."""
        LOGGER.debug(f"Event: {event.__str__()}")
        if self._shutdown:
            # Handle race conditions when the integration is being deleted by re-registering and existing device.
            return

        # The callback comes in on the XArm thread. Need to jump to the HA main thread to guarantee thread safety.
        self._eventloop.call_soon_threadsafe(self.event_handler_internal, event)

    def event_handler_internal(self, event: dict) -> None:
        """Handle state change events of xArm."""

        LOGGER.debug(f"Internal handler called with event: {event.__str__()}")
        if self._shutdown:
            # Handle race conditions when the integration is being deleted by re-registering and existing device.
            return

        if "cartesian" in event or "joints" in event:
            self._update_position_data()

        elif "error_code" in event or "warn_code" in event:
            self._update_error_data()

        elif "state" in event or "temperatures" in event or "mode" in event:
            self._update_state_data()

        elif "gripper_position" in event or "gripper_err_code" in event:
            self._update_gripper_data()

        elif "collision_sensitivity" in event:
            self._update_state_data()

    def update_method(self) -> None:
        """Update the device data of the xArm."""
        device = self.get_xarm_model()
        try:
            # use parent class method to update data
            self.async_set_updated_data(device)
        except Exception as e:
            LOGGER.error("An exception occurred calling async_set_updated_data():")
            LOGGER.error(f"Exception type: {type(e)}")
            LOGGER.error(f"Exception data: {e}")

    def _update_position_data(self) -> None:
        """Update the position data of the xArm."""
        self.get_model().position.update()
        self.update_method()

    def _update_state_data(self) -> None:
        """Update the position data of the xArm."""
        self.get_model().position.update()
        self.update_method()

    def register_callbacks(self) -> None:
        """Register the callbacks for the xArm."""
        self.xarm.register_event_callback(self.event_handler)
