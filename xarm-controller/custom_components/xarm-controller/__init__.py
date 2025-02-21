from homeassistant import core
from homeassistant.config_entries import ConfigType, ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import Platform

from .const import DOMAIN, LOGGER, MOVE_ARM_EVENT

from .coordinator import XArmControllerUpdateCoordinator

from xarm.wrapper import XArmAPI

type XArmConfigEntry = ConfigEntry[XArmControllerUpdateCoordinator]

PLATFORMS = [
    Platform.BINARY_SENSOR,
    # Platform.BUTTON,
    Platform.NUMBER,
    Platform.SENSOR,
]


async def async_setup_entry(
    hass: core.HomeAssistant,
    entry: XArmConfigEntry,
    # async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the xarm-controller-platform component."""

    coordinator = XArmControllerUpdateCoordinator(hass=hass, entry=entry)

    # await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    def check_service_call_payload(call: core.ServiceCall):
        LOGGER.debug(call)

        area_ids = call.data.get("area_id", [])
        device_ids = call.data.get("device_id", [])
        entity_ids = call.data.get("entity_id", [])
        label_ids = call.data.get("label_ids", [])

        # Ensure only one device ID is passed
        if not isinstance(area_ids, list) or len(area_ids) != 0:
            LOGGER.error("A single device id must be specified as the target.")
            return False
        if not isinstance(device_ids, list) or len(device_ids) != 1:
            LOGGER.error("A single device id must be specified as the target.")
            return False
        if not isinstance(entity_ids, list) or len(entity_ids) != 0:
            LOGGER.error("A single device id must be specified as the target.")
            return False
        if not isinstance(label_ids, list) or len(label_ids) != 0:
            LOGGER.error("A single device id must be specified as the target.")
            return False

        return True

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # async def move_xarm(call: core.ServiceCall):
    #     """Handle the service call."""
    #     if check_service_call_payload(call) is False:
    #         return
    #     hass.bus.fire(MOVE_ARM_EVENT, call.data)

    # Register the service with Home Assistant
    # hass.services.async_register(
    #     DOMAIN, "move_xarm", move_xarm  # Service name  # Handler function
    # )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: core.HomeAssistant, entry: XArmConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the XARM controller component from yaml configuration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_reload_entry(hass: core.HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the config entry when it changed."""
    LOGGER.debug("Async Setup Reload")
    await hass.config_entries.async_reload(entry.entry_id)
