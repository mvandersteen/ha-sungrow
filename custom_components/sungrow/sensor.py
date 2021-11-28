"""
Support for Sungrow Inverters

Currently supported:
    Sungrow Hybrid or String Inverters (SH or SG models)

"""
from homeassistant.const import DEVICE_CLASS_FREQUENCY
from sungrowinverter import SungrowInverter

from functools import partial
import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    STATE_CLASS_TOTAL,
    STATE_CLASS_MEASUREMENT,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_BATTERY,
    ATTR_DATE,
    ATTR_TIME,
    ATTR_MODEL,
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PORT,
    CONF_SLAVE,
    CONF_TIMEOUT,
    ELECTRIC_CURRENT_AMPERE,
    ENERGY_WATT_HOUR,
    ENERGY_KILO_WATT_HOUR,
    FREQUENCY_HERTZ,
    PERCENTAGE,
    POWER_WATT,
    TEMP_CELSIUS,
    CONF_MONITORED_CONDITIONS,
    CONF_SCAN_INTERVAL,
)

from .const import (
    SUNGROW_ENERGY_GENERATION,
    SUNGROW_GRID_FREQUENCY,
    SUNGROW_ARRAY1_ENERGY_GENERATION,
    SUNGROW_ARRAY2_ENERGY_GENERATION,
    SUNGROW_DAILY_OUTPUT_ENERGY,
    SUNGROW_TOTAL_OUTPUT_ENERGY,
    SUNGROW_LOAD_POWER,
    SUNGROW_EXPORT_POWER,
    SUNGROW_DAILY_BATTERY_CHARGE_PV_ENERGY,
    SUNGROW_TOTAL_BATTERY_CHARGE_PV_ENERGY,
    SUNGROW_DAILY_BATTERY_CHARGE_GRID_ENERGY,
    SUNGROW_TOTAL_BATTERY_CHARGE_GRID_ENERGY,
    SUNGROW_DAILY_PV_ENERGY,
    SUNGROW_TOTAL_PV_ENERGY,
    SUNGROW_DAILY_DIRECT_ENERGY_CONSUMPTION,
    SUNGROW_TOTAL_DIRECT_ENERGY_CONSUMPTION,
    SUNGROW_DAILY_IMPORT_ENERGY,
    SUNGROW_TOTAL_IMPORT_ENERGY,
    SUNGROW_DAILY_BATTERY_DISCHARGE_ENERGY,
    SUNGROW_TOTAL_BATTERY_DISCHARGE_ENERGY,
    SUNGROW_DAILY_EXPORT_ENERGY_FROM_PV,
    SUNGROW_TOTAL_EXPORT_ENERGY_FROM_PV,
    SUNGROW_DAILY_EXPORT_ENERGY_FROM_BATTERY,
    SUNGROW_TOTAL_EXPORT_ENERGY_FROM_BATTERY,
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_SLAVE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
    MIN_TIME_BETWEEN_UPDATES,
)

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=SUNGROW_ENERGY_GENERATION,
        name="Energy Generation",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_ARRAY1_ENERGY_GENERATION,
        name="PV Array 1 Energy Generation",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SUNGROW_ARRAY2_ENERGY_GENERATION,
        name="PV Array 2 Energy Generation",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SUNGROW_GRID_FREQUENCY,
        name="Grid Frequency",
        native_unit_of_measurement=FREQUENCY_HERTZ,
        device_class=DEVICE_CLASS_FREQUENCY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SUNGROW_DAILY_OUTPUT_ENERGY,
        name="Daily Output Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_TOTAL_OUTPUT_ENERGY,
        name="Total Output Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_LOAD_POWER,
        name="Current Load Power",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SUNGROW_EXPORT_POWER,
        name="Current Export Power",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
        key=SUNGROW_DAILY_PV_ENERGY,
        name="Daily PV Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_TOTAL_PV_ENERGY,
        name="Total PV Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_DAILY_BATTERY_CHARGE_PV_ENERGY,
        name="Daily Battery Charge PV Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_TOTAL_BATTERY_CHARGE_PV_ENERGY,
        name="Total Battery Charge PV Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_DAILY_DIRECT_ENERGY_CONSUMPTION,
        name="Daily Direct Energy Consumption",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_TOTAL_DIRECT_ENERGY_CONSUMPTION,
        name="Total Direct Energy Consumption",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_DAILY_IMPORT_ENERGY,
        name="Daily Grid Import Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_TOTAL_IMPORT_ENERGY,
        name="Total Grid Import Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_DAILY_BATTERY_DISCHARGE_ENERGY,
        name="Daily Battery Discharge Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_TOTAL_BATTERY_DISCHARGE_ENERGY,
        name="Total Battery Discharge Energy",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_DAILY_EXPORT_ENERGY_FROM_PV,
        name="Daily Export Energy From PV",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_TOTAL_EXPORT_ENERGY_FROM_PV,
        name="Total Export Energy From PV",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_DAILY_EXPORT_ENERGY_FROM_BATTERY,
        name="Daily Export Energy From Battery",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
    SensorEntityDescription(
        key=SUNGROW_TOTAL_EXPORT_ENERGY_FROM_BATTERY,
        name="Total Export Energy From Battery",
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL,
    ),
)
SENSOR_KEYS: list[str] = [desc.key for desc in SENSOR_TYPES]
DEFAULT_MONITORED = [
    SUNGROW_ENERGY_GENERATION,
    SUNGROW_DAILY_OUTPUT_ENERGY,
    SUNGROW_DAILY_IMPORT_ENERGY,
    SUNGROW_DAILY_BATTERY_CHARGE_PV_ENERGY,
    SUNGROW_DAILY_BATTERY_DISCHARGE_ENERGY,
    SUNGROW_DAILY_EXPORT_ENERGY_FROM_PV,
]

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.WARNING)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.string,
        vol.Optional(CONF_SLAVE, default=DEFAULT_SLAVE): cv.positive_int,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(ATTR_MODEL): cv.string,
    }
)


async def async_setup_platform(
    hass, config: ConfigType, async_add_entities, discovery_info=None
):
    """Set up the Jemena Outlook sensor."""

    sungrowclient = await hass.async_add_executor_job(
        partial(
            SungrowInverter,
            ip_address=config[CONF_IP_ADDRESS],
            port=config[CONF_PORT],
            slave=config[CONF_SLAVE],
            retries=3,
            timeout=int(config[CONF_TIMEOUT]),
        )
    )
    # can preload the inverter details instead of this being done on first run
    await sungrowclient.inverter_model()

    async def async_update_data():
        await sungrowclient.async_update()
        if sungrowclient.data is None:
            raise UpdateFailed(f"Bad update of sensor {config[CONF_NAME]}")
        return sungrowclient

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=max(config[CONF_SCAN_INTERVAL], MIN_TIME_BETWEEN_UPDATES),
    )

    # monitored_conditions = config[CONF_MONITORED_CONDITIONS]
    entities = [
        SungrowSensor(sungrowclient, config[CONF_NAME], coordinator, description)
        for description in SENSOR_TYPES
    ]

    await coordinator.async_refresh()

    # if description.key in monitored_conditions
    async_add_entities(entities, True)


class SungrowSensor(CoordinatorEntity, SensorEntity):
    """Implementation of a Jemena Outlook sensor."""

    def __init__(self, client, name, coordinator, description: SensorEntityDescription):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_name = f"{name} {description.name}"

        self.client = client

        _LOGGER.info("Init data: %s", self.client)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        sensor_type = self.entity_description.key

        try:
            if sensor_type == SUNGROW_ENERGY_GENERATION:
                state = self.coordinator.data.data["total_dc_power"]
            elif sensor_type == SUNGROW_ARRAY1_ENERGY_GENERATION:
                state = (
                    self.coordinator.data.data["mppt_1_voltage"]
                    * self.coordinator.data.data["mppt_1_current"]
                )
            elif sensor_type == SUNGROW_ARRAY2_ENERGY_GENERATION:
                state = (
                    self.coordinator.data.data["mppt_2_voltage"]
                    * self.coordinator.data.data["mppt_2_current"]
                )
            else:
                state = self.coordinator.data.data[sensor_type]

        except KeyError as err:
            _LOGGER.error("Sensor lookup value is not available in data array: %s", sensor_type)
            state = None

        return state

    @property
    def should_poll(self) -> bool:
        """Return False if entity should not poll."""
        return False
