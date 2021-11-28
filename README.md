# ha-sungrow

This is a [Home Assistant](https://home-assistant.io) sensor component to suuport retrieving data from Sungrow Residential inverters using modbus tcp.

A python module has also been created for the purpose of providing access to the registers within the sungrow inverters, and will be developed further as time permits. It is available at https://pypi.org/project/SungrowInverter/ and in current form supports hybrid and string inverters however this integration only supports hybrid for the moment, see below for supported hybrid inverters.

Your inverter will need a network connection, so either an ethernet connection or wifi dongle; this solution does not support rs485 modbus.

# Important notes

1. Use at your own risk.

2. I consider this in ALPHA state and there will be further changes, not all sensors are available yet there is a bit of work still required. There should be enough to get the Home-Assistant energy configuration filled in for grid, and solar usage.

## Supported Inverters

This plugin has been tested with a Sungrow SH5K-v13 Hybrid Inverter with a LG Chem 6.5kWh battery, and is the only testing that i've been able to perform so far, the same modbus registers are used across the Residntial Hybrid inverter range so should work with out issue.

I added the ability to use a Sungrow Residential String Inverters as well BUT I have not been able to test these registers other than refer to the https://github.com/meltaxa/solariot project, which this sensor has been based on. 

All the SGxx type inverters can be supported as well but i have not set the sensor to read those values as yet. Will get to taht soon.

If you are using any other inverter, i'll resolve best i can.

### Hybrid/Storage Inverters - inverter that support a battery

Residential Hybrid Single Phase Inverter for Low Voltage Battery [48V to 70V]

SH3K6 / SH4K6 / SH5K-V13 / SH5K-20 / SH4K6-30 / SH5K-30 / SH3K6-30

Residential Hybrid Single Phase Inverter wide battery voltage range [80V to 460V]

SH3.6RS / SH4.6RS / SH5.0RS / SH6.0RS

Residential Hybrid Three Phase Inverter wide battery voltage range [80V to 460V]

SH5.0RT / SH6.0RT / SH8.0RT / SH10RT

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


