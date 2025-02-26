"""Support for XArm sensor."""

from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Callable
from datetime import datetime

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorEntityDescription,
    SensorDeviceClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfLength, DEGREE
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import XArmControllerUpdateCoordinator
from .const import DOMAIN, POS_X, POS_Y, POS_Z, ROLL, PITCH, YAW, ERROR_CODE, LOGGER

# from .entity import XArmControllerEntity


@dataclass
class XArmControllerSensorEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable[..., datetime | StateType]


@dataclass
class XArmControllerSensorEntityDescription(
    SensorEntityDescription, XArmControllerSensorEntityDescriptionMixin
):
    """Sensor entity description for XArm Controller."""

    available_fn: Callable[..., bool] = lambda _: True
    exists_fn: Callable[..., bool] = lambda _: True
    extra_attributes: Callable[..., dict] = lambda _: {}
    icon_fn: Callable[..., str] = lambda _: None


SENSORS: list[XArmControllerSensorEntityDescription] = [
    XArmControllerSensorEntityDescription(
        key=ROLL,
        # device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.position.roll,
        icon="mdi:axis-x-rotate-counterclockwise",
    ),
    XArmControllerSensorEntityDescription(
        key=PITCH,
        # device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.position.pitch,
        icon="mdi:axis-y-rotate-counterclockwise",
    ),
    XArmControllerSensorEntityDescription(
        key=YAW,
        # device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.position.yaw,
        icon="mdi:axis-z-rotate-counterclockwise",
    ),
    XArmControllerSensorEntityDescription(
        key=POS_X,
        # device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.position.x,
        icon="mdi:axis-x-rotate-counterclockwise",
    ),
    XArmControllerSensorEntityDescription(
        key=POS_Y,
        # device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.position.y,
        icon="mdi:axis-y-rotate-counterclockwise",
    ),
    XArmControllerSensorEntityDescription(
        key=POS_Z,
        # device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.position.z,
        icon="mdi:axis-z-rotate-counterclockwise",
    ),
    XArmControllerSensorEntityDescription(
        key="state",
        translation_key="state",
        # device_class=SensorDeviceClass.DISTANCE,
        # state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.state.state,
        icon="mdi:state-machine",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: XArmControllerUpdateCoordinator,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    coordinator: XArmControllerUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    for sensor in SENSORS:
        LOGGER.debug(f"Adding sensor: {sensor.key}")
        async_add_entities(
            [
                XArmControllerSensor(
                    coordinator=coordinator, description=sensor, config_entry=entry
                )
            ]
        )


class XArmControllerSensor(SensorEntity):
    """Representation of a XArm sensor."""

    def __init__(
        self,
        coordinator: XArmControllerUpdateCoordinator,
        description: XArmControllerSensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.entity_description = description
        arm_info = coordinator.get_xarm_model().info
        self._attr_unique_id = f"{arm_info.serial}_{description.key}"
        # super().__init__(coordinator=coordinator)

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Xarm {self._attr_unique_id} {self.entity_description.key} Sensor"

    @property
    def available(self) -> bool:
        """Is the number available"""
        return self.coordinator.get_xarm_model().state.connected

    @property
    def connected(self):
        """Return the connection status of the sensor."""
        return self.coordinator.arm.connected

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        return self.entity_description.extra_attributes(
            self.coordinator.get_xarm_model()
        )

    @property
    def native_value(self) -> datetime | StateType:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.coordinator.get_xarm_model())

    @property
    def icon(self) -> str | None:
        """Return a dynamic icon if needed"""
        return self.entity_description.icon
