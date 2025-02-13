"""Base entity for XArm Controller."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import XArmControllerCoordinator


class XArmControllerEntity(CoordinatorEntity[XArmControllerCoordinator]):
    """Base class for XArm Controller entities."""

    def __init__(
    self,
    coordinator: XArmControllerCoordinator,
  ) -> None:
        """Initialize the XArm Controller entity."""
        super().__init__(coordinator=coordinator)
        self.xarm = coordinator.xarm
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.romy.unique_id)},
            manufacturer="ROMY",
            name=self.romy.name,
            model=self.romy.model,
        )
