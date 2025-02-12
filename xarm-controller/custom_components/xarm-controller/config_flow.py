import logging
import voluptuous as vol
from typing import Any, Dict, Optional
from homeassistant import config_entries, core
from homeassistant import data_entry_flow
from homeassistant.const import CONF_HOST
import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from ping3 import ping

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)

HOST_SCHEMA = vol.Schema({vol.Required(CONF_HOST): cv.string})


async def validate_host(ip: str) -> None:
    """Validates a GitHub repo path.

    Raises a ValueError if the host name is invalid.
    """
    if len(ip.split(".")) != 4:
        raise ValueError("Bad host name.")
    try:
        ping(ip)
    except Exception as exc:
        raise exc("Something went wrong with the ping.")


class XArmControllerConfigFlow(
    config_entries.ConfigFlow,
    data_entry_flow.FlowHandler,
    domain=DOMAIN,
):
    """Github Custom config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    data: Optional[dict[str, Any]]

    async def async_step_user(
        self, user_input: Optional[dict[str, Any]] = None
    ) -> ConfigFlowResult:
        """Invoke when a user initiates a flow via the user interface."""

        VERSION = 1
        # discovered_host: str
        # discovered_device: str
        errors: dict[str, str] = {}

        if user_input is not None:
            # try:
            #     await validate_host(user_input[CONF_HOST], self.hass)
            # except ValueError:
            #     errors["base"] = "host_error"
            #     self.async_abort(reason="host_error")
            if not errors:
                # Input is valid, set data.
                self.data = user_input
                # User is done adding host name, create the config entry.
                return self.async_create_entry(title="XArm Controller", data=self.data)

        return self.async_show_form(
            step_id="user", data_schema=HOST_SCHEMA, errors=errors
        )
