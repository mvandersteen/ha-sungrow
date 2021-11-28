"""The Sungrow integration."""
import voluptuous as vol

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.const import CONF_MONITORED_VARIABLES, CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, discovery
from homeassistant.helpers.typing import ConfigType

from homeassistant.const import (
    ATTR_MODEL,
    CONF_IP_ADDRESS,
    CONF_PORT,
    CONF_SLAVE,
    CONF_TIMEOUT,
    CONF_PLATFORM,
)

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SLAVE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.ensure_list,
            [
                vol.Schema(
                    {
                        vol.Required(CONF_IP_ADDRESS): cv.string,
                        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.string,
                        vol.Optional(CONF_SLAVE, default=DEFAULT_SLAVE): cv.string,
                        vol.Optional(
                            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                        ): cv.time_period,
                        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.string,
                        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                        vol.Optional(ATTR_MODEL): cv.string,
                    }
                )
            ],
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up Sungrow component."""

    for sensor_conf in config[SENSOR_DOMAIN]:
        if sensor_conf[CONF_PLATFORM] == DOMAIN:
            discovery_info = {SENSOR_DOMAIN: sensor_conf}
            hass.async_create_task(
                discovery.async_load_platform(
                    hass, SENSOR_DOMAIN, DOMAIN, discovery_info, config
                )
            )
    return True
