"""Base entity for XArm Controller."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity
from homeassistant.const import ATTR_SERIAL_NUMBER

from .const import DOMAIN
from .coordinator import XArmControllerUpdateCoordinator


class XArmControllerEntity(Entity, CoordinatorEntity[XArmControllerUpdateCoordinator]):
    """Base class for XArm Controller entities."""

    _attr_has_entity_name = True

    def __init__(self,) -> None:
        """Initialize the XArm Controller entity."""
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.config_entry[ATTR_SERIAL_NUMBER])},
            manufacturer="UFactory",
            name=self.xarm,
            model=self.model,
            ip_address=self.config_entry["host"],
        )

    # @property
    # def device_info(self) -> DeviceInfo:
    #     """Return device information about this XArm device."""
    #     return self.coordinator.get_xarm_model()
