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
# from .entity import XArmControllerEntity


@dataclass
class XArmControllerNumberEntityMixin:
    """Mixin for XArm Controller position."""

    value_fn: Callable[..., any]
    set_value_fn: Callable[..., None]


@dataclass
class XArmControllerNumberEntityDescription(
    NumberEntityDescription, XArmControllerNumberEntityMixin
):
    """Editable (number) position entity description for XArm Controller."""


NUMBERS: tuple[XArmControllerNumberEntityDescription, ...] = (
    XArmControllerNumberEntityDescription(
        key=POS_X,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=NumberDeviceClass.DISTANCE,
        icon="mdi:axis-x-arrow",
        mode=NumberMode.BOX,
        native_step=1,
        native_min_value=0,
        native_max_value=1000,  # TODO: Determine actual limit
        value_fn=lambda device: device.position.x,
        set_value_fn=lambda device, value: device.position.set_position(x=value),
    ),
    XArmControllerNumberEntityDescription(
        key=POS_Y,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=NumberDeviceClass.DISTANCE,
        icon="mdi:axis-y-arrow",
        mode=NumberMode.BOX,
        native_step=1,
        native_min_value=0,
        native_max_value=1000,  # TODO: Determine actual limit
        value_fn=lambda device: device.position.y,
        set_value_fn=lambda device, value: device.position.set_position(y=value),
    ),
    XArmControllerNumberEntityDescription(
        key=POS_Z,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=NumberDeviceClass.DISTANCE,
        icon="mdi:axis-z-arrow",
        mode=NumberMode.BOX,
        native_step=1,
        native_min_value=0,
        native_max_value=1000,  # TODO: Determine actual limit
        value_fn=lambda device: device.position.z,
        set_value_fn=lambda device, value: device.position.set_position(z=value),
    ),
    # XArmControllerNumberEntityDescription(
    #     key=GRIPPER_SPEED,
    #     native_unit_of_measurement=UnitOfSpeed.SPEED,
    #     device_class=NumberDeviceClass.SPEED,
    #     icon="mdi:axis-z-rotate-clockwise",
    #     mode=NumberMode.BOX,
    #     native_step=5,
    #     native_min_value=0,
    #     native_max_value=5000,  # TODO: Determine actual limit
    #     value_fn=lambda device: device.position,
    #     set_value_fn=lambda device, speed: device.set_gripper_speed(speed),
    # ),
    # XArmControllerNumberEntityDescription(
    #     key=GRIPPER_POSITION,
    #     native_unit_of_measurement=UnitOfSpeed.SPEED,
    #     device_class=NumberDeviceClass.SPEED,
    #     icon="mdi:ind",
    #     mode=NumberMode.BOX,
    #     native_step=5,
    #     native_min_value=0,
    #     native_max_value=1000,  # TODO: Determine actual limit
    #     value_fn=lambda device: device.gripper.position,
    #     set_value_fn=lambda device, speed: device.set_gripper_speed(speed),
    # ),
    # XArmControllerNumberEntityDescription(
    #     key=COLLISION_SENSITIVITY,
    #     native_unit_of_measurement=UnitOfSpeed.SPEED,
    #     device_class=NumberDeviceClass.SPEED,
    #     icon="mdi:robot-dead",
    #     mode=NumberMode.BOX,
    #     native_step=1,
    #     native_min_value=1,
    #     native_max_value=5,  # TODO: Determine actual limit
    #     value_fn=lambda device: device.state.collision_sensitivity,
    #     set_value_fn=lambda device, speed: device.state.set_collision_sensitivity(speed),
    # ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    LOGGER.debug("NUMBER::async_setup_entry")
    coordinator: XArmControllerUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    for description in NUMBERS:
        async_add_entities([XArmControllerNumber(coordinator, description, entry)])

    LOGGER.debug("NUMBER::async_setup_entry DONE")


class XArmControllerNumber(NumberEntity):
    """Define the Number."""

    entity_description: XArmControllerNumberEntityDescription

    def __init__(
        self,
        coordinator: XArmControllerUpdateCoordinator,
        description: XArmControllerNumberEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the number."""
        self.coordinator = coordinator
        self.entity_description = description
        xarm_info = self.coordinator.get_xarm_model().info
        self._attr_unique_id = f"{xarm_info.serial}_{description.key}"
        self._attr_native_value = description.value_fn(coordinator.get_xarm_model())
        # super().__init__(coordinator=coordinator)

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Xarm {self._attr_unique_id} {self.entity_description.key} Number"

    @property
    def icon(self) -> str | None:
        """Return a dynamic icon."""
        return self.entity_description.icon

    @property
    def available(self) -> bool:
        """Is the number available"""
        return self.coordinator.get_xarm_model().state.connected

    @property
    def native_value(self) -> float | None:
        """Return the value reported by the number."""
        return self.entity_description.value_fn(self.coordinator.get_xarm_model())

    # @native_value.setter
    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.entity_description.set_value_fn and self.entity_description.set_value_fn(self.coordinator.get_xarm_model(), value)
