import logging
import voluptuous as vol
from typing import Any, Dict, Optional
from homeassistant import config_entries, core
from homeassistant.const import CONF_HOST
import homeassistant.helpers.config_validation as cv
from ping3 import ping

from .const import DOMAIN



_LOGGER = logging.getLogger(__name__)

HOST_SCHEMA = vol.Schema(
    {vol.Required(CONF_HOST): cv.string}
)


async def validate_host(ip: str) -> None:
    """Validates a GitHub repo path.

    Raises a ValueError if the path is invalid.
    """
    if len(ip.split(".")) != 4:
        raise ValueError("bad host name")
    try:
      ping(ip)
    except Exception as exc:
      raise exc("Something went wrong with the ping")


class XArmControllerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
  """Github Custom config flow."""
  
  VERSION = 1
  CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

  data: Optional[Dict[str, Any]]

  async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
      """Invoked when a user initiates a flow via the user interface."""

      errors: Dict[str, str] = {}
      if user_input is not None:
          try:
              await validate_host(user_input[CONF_HOST], self.hass)
          except ValueError:
              errors["base"] = "host_error"
          if not errors:
              # Input is valid, set data.
              self.data = user_input
              # User is done adding repos, create the config entry.
              return self.async_create_entry(title="XArm Controller", data=self.data)

      return self.async_show_form(
          step_id="user", data_schema=HOST_SCHEMA, errors=errors
      )