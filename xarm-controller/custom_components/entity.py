"""Base entity for XArm Controller."""

from collections.abc import Callable, Coroutine
from typing import Any, Concatenate

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity
from homeassistant.const import ATTR_SERIAL_NUMBER
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .coordinator import XArmControllerUpdateCoordinator


class XArmControllerEntity(Entity, CoordinatorEntity[XArmControllerUpdateCoordinator]):
    """Base class for XArm Controller entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
    ) -> None:
        """Initialize the XArm Controller entity."""
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.config_entry[ATTR_SERIAL_NUMBER])},
            manufacturer="UFactory",
            name=self.xarm,
            model=self.model,
            ip_address=self.config_entry["host"],
        )

    # @property
    # def device_info(self) -> DeviceInfo:
    #     """Return device information about this XArm device."""
    #     return self.coordinator.get_xarm_model()


def exception_handler[
    _EntityT: XArmControllerEntity, **_P
](
    func: Callable[Concatenate[_EntityT, _P], Coroutine[Any, Any, Any]],
) -> Callable[
    Concatenate[_EntityT, _P], Coroutine[Any, Any, None]
]:
    """Decorate XArmAPI client calls to handle exceptions.

    A decorator that wraps the passed in function, catches XarmAPI errors.
    """

    async def handler(self: _EntityT, *args: _P.args, **kwargs: _P.kwargs) -> None:
        try:
            await func(self, *args, **kwargs)
        except Exception as error:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="communication_error",
                translation_placeholders={"error": str(error)},
            ) from error

        # except AirGradientError as error:
        #     raise HomeAssistantError(
        #         translation_domain=DOMAIN,
        #         translation_key="unknown_error",
        #         translation_placeholders={"error": str(error)},
        #     ) from error

    return handler
