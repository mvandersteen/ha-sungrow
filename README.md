# ha-sungrow

This is a [Home Assistant](https://home-assistant.io) sensor component to suuport retrieving data from Sungrow Residential inverters using modbus tcp.

A python module has also been created i nconjuction with this component that supports much more than the registers/sensors currently exposed, and will be developed further as well, is available at https://pypi.org/project/SungrowInverter/

# important notes

1. Use at your own risk.

2. I consider this in ALPHA state and will further changes will occur, not all sensors are available yet there is a bit of work still required. There should be enough to get the Home-Assistant energy configuration filled in for grid, and solar usage.

## Supported Inverters

This plugin has been tested with a Sungrow SH5K-v13 Hybrid Inverter with a LG Chem 6.5kWh battery, and is the only testing that i've been able to perform, the same modbus registers are used across the Residntial Hybrid inverter range so should work with out issue.

I added the ability to use a Sungrow Residential String Inverters as well BUT I have not been able to test these registers other than refer to the https://github.com/meltaxa/solariot project, which this sensor has been based on. 

All the SGxx type inverters seem to use the same modbus registers as well.

If you are using any other inverter, i'll resolve best i can.

### Hybrid/Storage Inverters - Ability to use a battery

SH3K6 / SH4K6 / SH5K-V13 / SH5K-20     - Residential Hybrid Single Phase Inverter for Low Voltage Battery [48V to 70V]
SH4K6-30 / SH5K-30 / SH3K6-30          - Residential Hybrid Single Phase Inverter for Low Voltage Battery [48V to 70V newer version]
SH3.6RS / SH4.6RS / SH5.0RS / SH6.0RS  - Residential Hybrid Single Phase Inverter wide battery voltage range [80V to 460V]
SH5.0RT / SH6.0RT / SH8.0RT / SH10RT   - Residential Hybrid Three Phase Inverter wide battery voltage range [80V to 460V]

### String Inverters - Solar panel and grid connection only

SG3.0RT, SG4.0RT, SG5.0RT, SG6.0RT, SG7.0RT，SG8.0RT, SG10RT, SG12RT, SG15RT, SG17RT, SG20RT
SG30KTL-M, SG30KTL-M-V31, SG33KTL-M, SG36KTL-M, SG33K3J, SG49K5J, SG34KJ, LP_P34KSG,
SG50KTL-M-20, SG60KTL, G80KTL, SG80KTL-20, SG60KU-M
SG5KTL-MT, SG6KTL-MT, SG8KTL-M, SG10KTL-M, SG10KTL-MT, SG12KTL-M, SG15KTL-M,
SG17KTL-M, SG20KTL-M,
SG80KTL-M, SG85BF, SG80HV, SG80BF, SG110HV-M, SG111HV, SG125HV, SG125HV-20
SG25CX-SA, SG30CX, SG33CX, SG40CX, SG50CX, SG36CX-US, SG60CX-US, SG75CX, SG100CX
SG100CX-JP, SG110CX, SG136TX, SG225HX, SG250HX
SG250HX-IN, SG250HX-US

Discontinued (as @ 2021-07-12):
SG30KTL, SG10KTL, SG12KTL, SG15KTL, SG20KTL, SG30KU, SG36KTL, SG36KU, SG40KTL,
SG40KTL-M, SG50KTL-M, SG60KTL-M, SG60KU

## Installing the component

Copy the following files into to it's own directory called sungrow within custom_components directory where the configuration for your installation of home assistant sits. 

The custom_components directory does not exist in default installation state and may need to be created.

```
<homeassistant-user-configuration-directory>/custom_components/sungrow/sensor.py
<homeassistant-user-configuration-directory>/custom_components/sungrow/const.py
<homeassistant-user-configuration-directory>/custom_components/sungrow/__init__.py
<homeassistant-user-configuration-directory>/custom_components/sungrow/manifest.py
```

## Configuring the sensor

```
# Example configuration.yaml entry

sensor:
  - platform: sungrow
    ip_address: 192.168.1.127
```

**Configuration variables:**

- **ip_address** (required): Only required variable to be passed to the sensor, invert type will be worked out during initialisation of the sensor.
- **port** (optional): defaults to 502 which is used by all teh supported inverters


