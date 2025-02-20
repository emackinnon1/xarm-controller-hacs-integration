from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberDeviceClass,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfSpeed, UnitOfLength
from homeassistant.core import HomeAssistant

from homeassistant.const import CONF_HOST, CONF_MODEL


from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .const import (
    DOMAIN,
    LOGGER,
    GRIPPER_SPEED,
    GRIPPER_POSITION,
    POS_X,
    POS_Y,
    POS_Z,
    COLLISION_SENSITIVITY,
)
from .coordinator import XArmControllerUpdateCoordinator
from .entity import XArmControllerEntity


@dataclass
class XArmControllerPositionEntityMixin:
    """Mixin for XArm Controller position."""

    value_fn: Callable[..., any]
    set_value_fn: Callable[..., None]


@dataclass
class XArmPositionNumberEntityDescription(
    NumberEntityDescription, XArmControllerPositionEntityMixin
):
    """Editable (number) position entity description for XArm Controller."""


NUMBERS = tuple[XArmPositionNumberEntityDescription, ...] = (
    XArmPositionNumberEntityDescription(
        key=POS_X,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=NumberDeviceClass.DISTANCE,
        icon="mdi:axis-x-arrow",
        mode=NumberMode.BOX,
        native_step=1,
        native_min_value=0,
        native_max_value=1000,  # TODO: Determine actual limit
        value_fn=lambda device: device.position.x,
        set_value_fn=lambda device, value: device.set_position(x=value),
    ),
    XArmPositionNumberEntityDescription(
        key=POS_Y,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=NumberDeviceClass.DISTANCE,
        icon="mdi:axis-y-arrow",
        mode=NumberMode.BOX,
        native_step=1,
        native_min_value=0,
        native_max_value=1000,  # TODO: Determine actual limit
        value_fn=lambda device: device.position.y,
        set_value_fn=lambda device, value: device.set_position(y=value),
    ),
    XArmPositionNumberEntityDescription(
        key=POS_Z,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=NumberDeviceClass.DISTANCE,
        icon="mdi:axis-z-arrow",
        mode=NumberMode.BOX,
        native_step=1,
        native_min_value=0,
        native_max_value=1000,  # TODO: Determine actual limit
        value_fn=lambda device: device.position.z,
        set_value_fn=lambda device, value: device.set_position(z=value),
    ),
    XArmPositionNumberEntityDescription(
        key=GRIPPER_SPEED,
        native_unit_of_measurement=UnitOfSpeed.SPEED,
        device_class=NumberDeviceClass.SPEED,
        icon="mdi:axis-z-rotate-clockwise",
        mode=NumberMode.BOX,
        native_step=5,
        native_min_value=0,
        native_max_value=5000,  # TODO: Determine actual limit
        value_fn=lambda device: device.position,
        set_value_fn=lambda device, speed: device.set_gripper_speed(speed),
    ),
    XArmPositionNumberEntityDescription(
        key=GRIPPER_POSITION,
        native_unit_of_measurement=UnitOfSpeed.SPEED,
        device_class=NumberDeviceClass.SPEED,
        icon="mdi:ind",
        mode=NumberMode.BOX,
        native_step=5,
        native_min_value=0,
        native_max_value=1000,  # TODO: Determine actual limit
        value_fn=lambda device: device.gripper.position,
        set_value_fn=lambda device, speed: device.set_gripper_speed(speed),
    ),
    XArmPositionNumberEntityDescription(
        key=COLLISION_SENSITIVITY,
        native_unit_of_measurement=UnitOfSpeed.SPEED,
        device_class=NumberDeviceClass.SPEED,
        icon="mdi:robot-dead",
        mode=NumberMode.BOX,
        native_step=1,
        native_min_value=1,
        native_max_value=5,  # TODO: Determine actual limit
        value_fn=lambda device: device.state.collision_sensitivity,
        set_value_fn=lambda device, speed: device.state.set_collision_sensitivity(speed),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    LOGGER.debug("NUMBER::async_setup_entry")
    coordinator: XArmControllerUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    for description in NUMBERS:
        async_add_entities([XArmControllerNumber(coordinator, description, entry)])

    LOGGER.debug("NUMBER::async_setup_entry DONE")


class XArmControllerNumber(XArmControllerEntity, NumberEntity):
    """Defined the Number"""

    entity_description: XArmPositionNumberEntityDescription

    def __init__(
        self,
        coordinator: XArmControllerUpdateCoordinator,
        description: XArmPositionNumberEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the number."""
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        xarm_info = self.coordinator.get_xarm_model().info
        self._attr_unique_id = f"{xarm_info.serial}_{description.key}"
        self._attr_native_value = description.value_fn(coordinator.get_xarm_model())

    @property
    def available(self) -> bool:
        """Is the number available"""
        return self.coordinator.get_xarm_model().connected

    @property
    def native_value(self) -> float | None:
        """Return the value reported by the number."""
        return self.entity_description.value_fn(self.coordinator.get_xarm_model())

    @native_value.setter
    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.entity_description.set_value_fn(self.coordinator.get_xarm_model(), value)
