"""Constants for the Sungrow component."""
from __future__ import annotations

from datetime import timedelta

# Common
DOMAIN = "sungrow"
DEFAULT_NAME = "Sungrow"
DEFAULT_PORT = 502
DEFAULT_SLAVE = 0x01
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_TIMEOUT = 3

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

SUNGROW_ENERGY_GENERATION = "energy_generation"
SUNGROW_ENERGY_CONSUMPTION = "energy_consumption"

SUNGROW_ARRAY1_ENERGY_GENERATION = "array1_energy_generation"
SUNGROW_ARRAY1_VOLTAGE = "array1_voltage"
SUNGROW_ARRAY1_CURRENT = "array1_current"

SUNGROW_ARRAY2_ENERGY_GENERATION = "array2_energy_generation"
SUNGROW_ARRAY2_VOLTAGE = "array2_voltage"
SUNGROW_ARRAY2_CURRENT = "array2_current"

SUNGROW_LOAD_POWER = "load_power"
SUNGROW_EXPORT_POWER = "export_power"

SUNGROW_DAILY_IMPORT_ENERGY = "daily_import_energy"
SUNGROW_TOTAL_IMPORT_ENERGY = "total_import_energy"

# Battery charged from PV
SUNGROW_DAILY_BATTERY_CHARGE_PV_ENERGY = "daily_battery_charge_energy_from_pv"
SUNGROW_TOTAL_BATTERY_CHARGE_PV_ENERGY = "total_battery_charge_energy_from_pv"

# Battery charged from GRID
SUNGROW_DAILY_BATTERY_CHARGE_GRID_ENERGY = "daily_charge_energy"
SUNGROW_TOTAL_BATTERY_CHARGE_GRID_ENERGY = "total_charge_energy"

SUNGROW_DAILY_BATTERY_DISCHARGE_ENERGY = "daily_battery_discharge_energy"
SUNGROW_TOTAL_BATTERY_DISCHARGE_ENERGY = "total_battery_discharge_energy"

SUNGROW_INVERTER_EFFICENCY = "inverter_efficency"

SUNGROW_DAILY_OUTPUT_ENERGY = "daily_output_energy"
SUNGROW_TOTAL_OUTPUT_ENERGY = "total_output_energy"

SUNGROW_GRID_FREQUENCY = "grid_frequency"

SUNGROW_DAILY_PV_ENERGY = "daily_pv_generation"
SUNGROW_TOTAL_PV_ENERGY = "total_pv_generation"

SUNGROW_DAILY_DIRECT_ENERGY_CONSUMPTION = "daily_direct_energy_consuption"
SUNGROW_TOTAL_DIRECT_ENERGY_CONSUMPTION = "total_direct_energy_consuption"

SUNGROW_DAILY_EXPORT_ENERGY_FROM_PV = "daily_export_power_from_pv"
SUNGROW_TOTAL_EXPORT_ENERGY_FROM_PV = "total_export_power_from_pv"

SUNGROW_DAILY_EXPORT_ENERGY_FROM_BATTERY = "daily_export_energy"
SUNGROW_TOTAL_EXPORT_ENERGY_FROM_BATTERY = "daily_export_energy"
