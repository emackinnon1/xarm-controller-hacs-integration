"""Base entity for XArm Controller."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import XArmControllerCoordinator


class XArmControllerEntity(CoordinatorEntity[XArmControllerCoordinator]):
    """Base class for XArm Controller entities."""

    _attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this XArm device."""
        return self.coordinator.get_device()
