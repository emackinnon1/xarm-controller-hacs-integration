"""Support for XArm sensor."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import XArmContollerCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: XArmContollerCoordinator,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    async_add_entities(
        [
            XArmControllerSensor(
                coordinator=entry.runtime_data,
                translation_key="visibility",
            )
        ]
    )


class XArmControllerSensor(SensorEntity):
    """Representation of a XArm sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.coordinator.data['name']} Visibility"
    
    @property
    def connected(self):
        """Return the connection status of the sensor."""
        return self.coordinator.data["connected"]

    @property
    def position(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.translation_key]