from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.helpers.entity import EntityCategory
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ERROR_CODE, WARN_CODE, GRIPPER_ERROR_CODE, LOGGER
from .coordinator import XArmControllerUpdateCoordinator
from .entity import XArmControllerEntity


@dataclass
class XArmControllerBinarySensorEntityDescriptionMixIn:
    """Mixin for required keys."""

    is_on_fn: Callable[..., bool]


@dataclass
class XArmControllerBinarySensorEntityDescription(
    BinarySensorEntityDescription, XArmControllerBinarySensorEntityDescriptionMixIn
):
    """Sensor entity description for XArm Controller."""

    available_fn: Callable[..., bool] = lambda _: True
    exists_fn: Callable[..., bool] = lambda _: True
    extra_attributes: Callable[..., dict] = lambda _: {}


BINARY_SENSORS = tuple[XArmControllerBinarySensorEntityDescription, ...] = (
    XArmControllerBinarySensorEntityDescription(
        key=ERROR_CODE,
        translation_key=ERROR_CODE,
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        is_on_fn=lambda device: device.coordinator.error_code != 0,
        extra_attributes=lambda device: {
            "error_msg": device.state.error_code_msg,
            "error_code": device.state.error_code_code,
        },
    ),
    XArmControllerBinarySensorEntityDescription(
        key=WARN_CODE,
        translation_key=WARN_CODE,
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        is_on_fn=lambda device: device.coordinator.warn_code != 0,
        extra_attributes=lambda device: {
            "warn_msg": device.state.warn_code_msg,
            "warn_code": device.state.warn_code_code,
        },
    ),
    XArmControllerBinarySensorEntityDescription(
        key=GRIPPER_ERROR_CODE,
        translation_key=GRIPPER_ERROR_CODE,
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        is_on_fn=lambda device: device.gripper.error_code != 0,
        extra_attributes=lambda device: {
            "gripper_error_msg": device.gripper.error_msg,
            "gripper_error_code": device.gripper.error_code,
        },
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up XArm Controller binary sensor based on a config entry."""
    coordinator: XArmControllerUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    for sensor in BINARY_SENSORS:
        if sensor.exists_fn(coordinator):
            async_add_entities([XArmControllerBinarySensor(coordinator, sensor, entry)])


class XArmControllerBinarySensor(XArmControllerEntity, BinarySensorEntity):
    """Representation of a XArm Controller binary sensor that is updated via the XArmAPI."""

    def __init__(
        self,
        coordinator: XArmControllerUpdateCoordinator,
        description: XArmControllerBinarySensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        xarm_info = self.coordinator.get_xarm_model().info
        self._attr_unique_id = f"{xarm_info.serial}_{description.key}"

    @property
    def is_on(self) -> bool:
        """Return if binary sensor is on."""
        return self.entity_description.is_on_fn(self)

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        return self.entity_description.extra_attributes(self)
