from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberDeviceClass,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant

from homeassistant.const import CONF_HOST, CONF_MODEL


from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .const import DOMAIN, LOGGER, POS_X, POS_Y, POS_Z, ROLL, PITCH, YAW
from .coordinator import XArmControllerCoordinator

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
        value_fn=lambda device: device.position,
        set_value_fn=lambda device, value: device.set_position(x=value),
    ),
    XArmPositionNumberEntityDescription(
        key=POS_Y,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=NumberDeviceClass.DISTANCE,
        icon="mdi:axis-y-arrow",
        mode=NumberMode.BOX,
        native_step=1,
        value_fn=lambda device: device.position,
        set_value_fn=lambda device, value: device.set_position(y=value),
    ),
    XArmPositionNumberEntityDescription(
        key=POS_Z,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=NumberDeviceClass.DISTANCE,
        icon="mdi:axis-z-arrow",
        mode=NumberMode.BOX,
        native_step=1,
        value_fn=lambda device: device.position,
        set_value_fn=lambda device, value: device.set_position(z=value),
    ),
    XArmPositionNumberEntityDescription(
        key=ROLL,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=NumberDeviceClass.DISTANCE,
        icon="mdi:axis-x-rotate-clockwise",
        mode=NumberMode.BOX,
        native_step=1,
        value_fn=lambda device: device.position,
    ),
    XArmPositionNumberEntityDescription(
        key=PITCH,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=NumberDeviceClass.DISTANCE,
        icon="mdi:axis-y-rotate-clockwise",
        mode=NumberMode.BOX,
        native_step=1,
        value_fn=lambda device: device.position,
    ),
    XArmPositionNumberEntityDescription(
        key=YAW,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=NumberDeviceClass.DISTANCE,
        icon="mdi:axis-z-rotate-clockwise",
        mode=NumberMode.BOX,
        native_step=1,
        value_fn=lambda device: device.position,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    LOGGER.debug("NUMBER::async_setup_entry")
    coordinator: XArmControllerCoordinator = hass.data[DOMAIN][entry.entry_id]

    for description in NUMBERS:
        async_add_entities([XArmControllerNumber(coordinator, description, entry)])

    LOGGER.debug("NUMBER::async_setup_entry DONE")


class XArmControllerNumber(BambuLabEntity, NumberEntity):
    """ Defined the Number"""
    entity_description: XArmPositionNumberEntityDescription

    def __init__(
        self,
        coordinator: XArmControllerCoordinator,
        description: XArmPositionNumberEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the number."""
        self.entity_description = description
        self._attr_unique_id = f"{config_entry.data[CONF_HOST]}_{config_entry.data[CONF_MODEL]}_{description.key}"
        self._attr_native_value = description.value_fn(coordinator.get_model())

        super().__init__(coordinator=coordinator)

    @property
    def available(self) -> bool:
        """Is the number available"""
        return self.coordinator.get_model().is_connected()

    @property
    def native_value(self) -> float | None:
        """Return the value reported by the number."""
        return self.entity_description.value_fn(self.coordinator.get_model())

    @native_value.setter
    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.entity_description.set_value_fn(self.coordinator.get_model())
