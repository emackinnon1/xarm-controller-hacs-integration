from homeassistant import core
from homeassistant.config_entries import ConfigType, ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import Platform

from .const import DOMAIN

from .coordinator import XArmControllerCoordinator

from xarm.wrapper import XArmAPI

type XArmConfigEntry = ConfigEntry[XArmControllerCoordinator]

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(
    hass: core.HomeAssistant,
    entry: XArmConfigEntry,
    # async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the xarm-controller-platform component."""

    coordinator = XArmControllerCoordinator(hass=hass, entry=entry)

    # await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    async def move_axis(call: ServiceCall):
        """Handle the service call."""
        if check_service_call_payload(call) is False:
            return
        hass.bus.fire(MOVE_AXIS_BUS_EVENT, call.data)

    # Register the service with Home Assistant
    hass.services.async_register(
        DOMAIN, "move_axis", move_axis  # Service name  # Handler function
    )

    return True


async def update_listener(hass: core.HomeAssistant, entry: XArmConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: core.HomeAssistant, entry: XArmConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the XARM controller component from yaml configuration."""
    hass.data.setdefault(DOMAIN, {})
    return True
