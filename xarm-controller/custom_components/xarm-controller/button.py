from dataclasses import dataclass
from collections.abc import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory

from homeassistant.components.button import (
    ButtonEntity,
    ButtonEntityDescription,
    ButtonDeviceClass,
)
from .const import DOMAIN, LOGGER
from .coordinator import XArmControllerUpdateCoordinator


@dataclass
class XArmControllerButtonEntityMixin:
    """Mixin for XArm Controller button."""

    action_fn: Callable[..., None]


@dataclass
class XArmControllerButtonEntityDescription(
    ButtonEntityDescription, XArmControllerButtonEntityMixin
):
    """Button entity description for XArm Controller."""


BUTTONS: tuple[XArmControllerButtonEntityDescription, ...] = (
    XArmControllerButtonEntityDescription(
        key="emergency_stop_button",
        name="Emergency Stop",
        icon="mdi:alert-octagon",
        action_fn=lambda device: device.emergency_stop(),
        entity_category=EntityCategory.CONFIG,
    ),
    XArmControllerButtonEntityDescription(
        key="go_home_button",
        name="Go Home",
        icon="mdi:home-import-outline",
        action_fn=lambda device: device.go_home(),
        entity_category=EntityCategory.CONFIG,
    ),
    XArmControllerButtonEntityDescription(
        key="clear_errors_button",
        name="Clear Errors",
        icon="mdi:alert-circle-check-outline",
        action_fn=lambda device: device.clear_errors(),
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    LOGGER.debug("BUTTON::async_setup_entry")
    coordinator: XArmControllerUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    for description in BUTTONS:
        async_add_entities([XArmControllerButton(coordinator, description, entry)])

    LOGGER.debug("BUTTON::async_setup_entry DONE")


class XArmControllerButton(ButtonEntity):
    """Define the Button."""

    entity_description: XArmControllerButtonEntityDescription
    coordinator: XArmControllerUpdateCoordinator

    def __init__(
        self,
        coordinator: XArmControllerUpdateCoordinator,
        description: XArmControllerButtonEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        self.coordinator = coordinator
        self.entity_description = description
        xarm_info = self.coordinator.get_xarm_model().info
        self._attr_unique_id = f"{xarm_info.serial}_{description.key}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._attr_unique_id} {self.entity_description.name} Button"

    @property
    def icon(self) -> str | None:
        """Return a dynamic icon."""
        return self.entity_description.icon

    @property
    def device_class(self) -> str:
        return self.entity_description.device_class

    @property
    def available(self) -> bool:
        return self.coordinator.get_xarm_model().state.connected

    async def async_press(self) -> None:
        """Pause the Print on button press"""
        LOGGER.debug(f"Button Pressed: {self.entity_description.key}")
        self.entity_description.action_fn(self.coordinator.get_xarm_model())
        # await self.coordinator.async_request_refresh()
