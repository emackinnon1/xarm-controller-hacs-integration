"""Support for XArm sensor."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass, SensorEntityDescription, SensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.const import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import XArmControllerCoordinator

SENSORS: list[SensorEntityDescription] = [
    SensorEntityDescription(
        key="position_x",
        translation_key="position_x",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="position_y",
        translation_key="position_y",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="position_z",
        translation_key="position_z",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="roll",
        translation_key="roll",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="pitchh",
        translation_key="putch",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="yaw",
        translation_key="yaw",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="error_code",
        translation_key="error_code",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="speed",
        translation_key="speed",
        device_class=SensorDeviceClass.SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: XArmControllerCoordinator,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    async_add_entities(
        [
            XArmControllerSensor(
                coordinator=entry.runtime_data,
            )
        ]
    )


class XArmControllerSensor(SensorEntity):
    """Representation of a XArm sensor."""

    def __init__(self, coordinator: XArmControllerCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__()
        self.coordinator = coordinator
        self.attrs: dict[str, Any]

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.coordinator.data['name']} Sensor"

    @property
    def connected(self):
        """Return the connection status of the sensor."""
        return self.coordinator.data["connected"]

    @property
    def position(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.translation_key]
