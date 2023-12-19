# domoticz-pzem-016 

This is a plugin for the free open-source [Domoticz home automation system](https://www.domoticz.com) that **read one or more PZEM-014, PZEM-016, PZEM-004T energy meters by Modbus connection** (RS485 serial connection), providing the following data: 
* active power
* active energy
* voltage
* current
* frequency
* power factor

![Screenshot of devices created by domoticz-pzem-016 Domoticz plugin on smartphone](https://images.creasol.it/domoticz-pzem-016-screenshot.webp)

The following items can be configured:
* Bitrate, by default 9600 bps
* Meter address, for example 1 (only one meter with address 1) or 11,12 (two devices with address 11 and 12: address should be separated by comma)
* Poll interval, in seconds: in case of a long list of devices, don't use very short poll intervals!

![Domoticz plugin configuration](https://images.creasol.it/domoticz-pzem-016-hardware.png)

PZEM-014 and PZEM-016 have RS485 port: one or more modules can be connected together by a standard "sensor alarm cable" (2x 0.22mm² wires + shield), 
and then connected to Domoticz controller (Raspberry PI or other hardware) by using a cheap RS485/USB adapter or a RS485/net controller. Please remember
that RS485 bus should be terminated in both ends by a 120 Ohm resistor.

![PZEM-016 or PZEM-014 wiring schematic](https://images.creasol.it/PZEM-016_wiring.png)

PZEM-004T has TTL outputs, so it can be connected to the controller by a TTL to serial adapter.

## Setting a different address to a PZEM-014 or PZEM-016 meter 
From Linux it's possible to change the address of a meter (by default it's set to 1) by using the following command, that changes address from 1 to 11:
```
mbpoll -mrtu -Pnone -a1 -b9600 -0 -1 -r2 /dev/ttyUSB0 11
```
/dev/ttyUSB0 have to be replaced with the right serial port.

Using other operating systems, please use a Modbus client to set the register address 2 (base-0) to the new slave address value, using function code 6.

This plugin does not open the serial port in exclusive-mode, so it's possible to share the same serial port for many different devices; for example, it was successfully tested with 1 PZEM-016 energy meter and 1 EMMETI MIRAI heat pump (same bitrate, with different slave address of course).

![Screenshot of devices created by domoticz-pzem-016 Domoticz plugin](https://images.creasol.it/domoticz-pzem-016-screenshot1.webp)

# Installation

This plugin can be installed from [Python Plugin Manager](https://github.com/ycahome/pp-manager) or [Python Plugins Manager](https://github.com/stas-demydiuk/domoticz-plugins-manager) which also permit to update plugin easily or automatically.

Alternatively, it's possible to give the following commands from the linux shell:

```
cd ~/domoticz/plugins
git clone https://github.com/CreasolTech/domoticz-pzem-016
```

Then, in the future, to update the plugin it's possible to simply type
```
cd ~/domoticz/plugins/domoticz-pzem-016
git pull
```

It uses the python plugin module minimalmodbus , than can be installed by
```
sudo apt install pyserial
sudo pip3 install minimalmodbus
```


Restart Domoticz, then go to Setup -> Hardware and add the Emmeti Mirai heat pump plugin, specifying a name for that hardware and the serial port to connect heat pump.

**Plugin can be easily translate in other languages**: just add the language code to LANGS variable, and add a field to each device with the translated name of device. Please send a copy of the plugin.py file to linux at creasol dot it 


## Credits
Many thanks to:
* Moreno Risorti, that has tested the plugin with PZEM-004T

***


## Creasol DomBus modules
Our industrial and home automation modules are designed to be
* very low power (**around 10mW with relays OFF**)
* reliable (**no disconnections**)
* bus connected (**no radiofrequency interference, no battery to replace**).

Modules are available in two version:
1. with **DomBus proprietary protocol**, working with [Domoticz](https://www.domoticz.com) only
2. with **Modbus standard protocol**, working with [Home Assistant](https://www.home-assistant.io), [OpenHAB](https://www.openhab.org), [Node-RED](https://nodered.org)

[Store website](https://store.creasol.it/domotics) - [Information website](https://www.creasol.it/domotics)

### DomBusEVSE - EVSE module to build a Smart Wallbox / EV charging station
<a href="https://store.creasol.it/DomBusEVSE"><img src="https://images.creasol.it/creDomBusEVSE_200.png" alt="DomBusEVSE smart EVSE module to make a Smart Wallbox EV Charging station" style="float: left; margin-right: 2em;" align="left" /></a>
Complete solution to make a Smart EVSE, **charging the electric vehicle using only energy from renewable source (photovoltaic, wind, ...), or adding 25-50-75-100% of available power from the grid**.

* Single-phase and three-phases, up to 36A (8kW or 22kW)
* Needs external contactor, RCCB (protection) and EV cable
* Optional power meter to measure charging power, energy, voltage and power factor
* Optional power meter to measure the power usage from the grid (not needed if already exists)
* **Two max grid power thresholds** can be programmed: for example, in Italy who have 6kW contractual power can drain from the grid Max (6* 1.27)=7.6kW for max 90 minutes followed by (6* 1.1)=6.6kW for another 90 minutes. **The module can use ALL available power** when programmed to charge at 100%.
* **Works without the domotic controller** (stand-alone mode), and **can also work with charging current set by the domotic controller (managed mode)**

<br clear="all"/>

### DomBusTH - Compact board to be placed on a blank cover, with temperature and humidity sensor and RGW LEDs
<a href="https://store.creasol.it/DomBusTH"><img src="https://images.creasol.it/creDomBusTH6_200.png" alt="DomBusTH domotic board with temperature and humidity sensor, 3 LEDs, 6 I/O" style="float: left; margin-right: 2em;" align="left" /></a>
Compact board, 32x17mm, to be installed on blank cover with a 4mm hole in the middle, to exchange air for the relative humidity sensor. It can be **installed in every room to monitor temperature and humidity, check alarm sensors, control blind motor UP/DOWN**, send notifications (using red and green leds) and activate **white led in case of power outage**.

Includes:
* temperature and relative humidity sensor
* red, green and white LEDs
* 4 I/Os configurable as analog or digital inputs, pushbuttons, counters (water, gas, S0 energy, ...), NTC temperature and ultrasonic distance sensors
* 2 ports are configured by default as open-drain output and can drive up to 200mA led strip (with dimming function) or can be connected to the external module DomRelay2 to control 2 relays; they can also be configured as analog/digital inputs, pushbuttons and distance sensors.
<br clear="all"/>

### DomBus12 - Compact domotic module with 9 I/Os
<a href="https://store.creasol.it/DomBus12"><img src="https://images.creasol.it/creDomBus12_400.webp" alt="DomBus12 domotic module with 9 I/O" style="float: left; margin-right: 2em;" align="left" /></a>
**Very compact, versatile and cost-effective module with 9 ports**. Each port can be configured by software as:
* analog/digital inputs
* pushbutton and UP/DOWN pushbutton
* counters (water, gas, S0 energy, ...)
* NTC temperature and ultrasonic distance sensors
* 2 ports are configured by default as open-drain output and can drive up to 200mA led strip (with dimming function) or can be connected to the external module DomRelay2 to control 2 relays.
<br clear="all"/>

### DomBus23 - Domotic module with many functions
<a href="https://store.creasol.it/DomBus23"><img src="https://images.creasol.it/creDomBus23_400.webp" alt="DomBus23 domotic module with many functions" style="float: left; margin-right: 2em; vertical-align: middle;" align="left" /></a>
Versatile module designed to control **gate or garage door**.
* 2x relays SPST 5A
* 1x 10A 30V mosfet (led stripe dimming)
* 2x 0-10V analog output: each one can be configured as open-drain output to control external relay
* 2x I/O lines, configurable as analog/digital inputs, temperature/distance sensor, counter, ...
* 2x low voltage AC/DC opto-isolated inputs, 9-40V
* 1x 230V AC opto-isolated input
<br clear="all"/>

### DomBus31 - Domotic module with 8 relays
<a href="https://store.creasol.it/DomBus31"><img src="https://images.creasol.it/creDomBus31_400.webp" alt="DomBus31 domotic module with 8 relay outputs" style="float: left; margin-right: 2em; vertical-align: middle;" align="left" /></a>
DIN rail low profile module, with **8 relays and very low power consumption**:
* 6x relays SPST 5A
* 2x relays STDT 10A
* Only 10mW power consumption with all relays OFF
* Only 500mW power consumption with all 8 relays ON !!
<br clear="all"/>

### DomBus32 - Domotic module with 3 relays
<a href="https://store.creasol.it/DomBus32"><img src="https://images.creasol.it/creDomBus32_200.webp" alt="DomBus32 domotic module with 3 relay outputs" style="float: left; margin-right: 2em; vertical-align: middle;" align="left" /></a>
Versatile module with 230V inputs and outputs, and 5 low voltage I/Os.
* 3x relays SPST 5A
* 3x 115/230Vac optoisolated inputs
* Single common for relays and AC inputs
* 5x general purpose I/O, each one configurable as analog/digital inputs, pushbutton, counter, temperature and distance sensor.
<br clear="all"/>

### DomBus33 - Module to domotize a light system using step relays
<a href="https://store.creasol.it/DomBus33"><img src="https://images.creasol.it/creDomBus32_200.webp" alt="DomBus33 domotic module with 3 relay outputs that can control 3 lights" style="float: left; margin-right: 2em; vertical-align: middle;" align="left" /></a>
Module designed to **control 3 lights already existing and actually controlled by 230V pushbuttons and step-by-step relays**. In this way each light can be activated by existing pushbuttons, and by the domotic controller.
* 3x relays SPST 5A
* 3x 115/230Vac optoisolated inputs
* Single common for relays and AC inputs
* 5x general purpose I/O, each one configurable as analog/digital inputs, pushbutton, counter, temperature and distance sensor.

Each relay can toggle the existing step-relay, switching the light On/Off. The optoisolator monitors the light status. The 5 I/Os can be connected to pushbuttons to activate or deactivate one or all lights.
<br clear="all"/>

### DomBus36 - Domotic module with 12 relays
<a href="https://store.creasol.it/DomBus36"><img src="https://images.creasol.it/creDomBus36_400.webp" alt="DomBus36 domotic module with 12 relay outputs" style="float: left; margin-right: 2em; vertical-align: middle;" align="left" /></a>
DIN rail module, low profile, with **12 relays outputs and very low power consumption**.
* 12x relays SPST 5A
* Relays are grouped in 3 blocks, with a single common per block, for easier wiring
* Only 12mW power consumption with all relays OFF
* Only 750mW power consumption with all 12 relays ON !!
<br clear="all"/>

### DomBus37 - 12 inputs, 3 115/230Vac inputs, 3 relay outputs
<a href="https://store.creasol.it/DomBus37"><img src="https://images.creasol.it/creDomBus37_400.webp" alt="DomBus37 domotic module with 12 inputs, 3 AC inputs, 3 relay outputs" style="float: left; margin-right: 2em; vertical-align: middle;" align="left" /></a>
Module designed to be connected to alarm sensors (magnetc contact sensors, PIRs, tampers): it's able to monitor mains power supply (power outage / blackout) and also have 3 relays outputs.
* 12x low voltage inputs (analog/digital inputs, buttons, alarm sensors, counters, temperature and distance sensors, ...)
* 3x 115/230Vac optoisolated inputs
* 2x relays SPST 5A
* 1x relay SPST 10A
* In12 port can be used to send power supply to an external siren, monitoring current consumption
<br clear="all"/>

### DomRelay2 - 2x relays board
<a href="https://store.creasol.it/DomRelay2"><img src="https://images.creasol.it/creDomRelay22_200.png" alt="Relay board with 2 relays, to be used with DomBus domotic modules" style="float: left; margin-right: 2em; vertical-align: middle;" align="left" /></a>
Simple module with 2 relays, to be used with DomBus modules or other electronic boards with open-collector or open-drain outputs
* 2x 5A 12V SPST relays (Normally Open contact)
* Overvoltage protection (for inductive loads, like motors)
* Overcurrent protection (for capacitive laods, like AC/DC power supply, LED bulbs, ...)
<br clear="all"/>

### DomESP1 / DomESP2 - Board with relays and more for ESP8266 NodeMCU WiFi module
<a href="https://store.creasol.it/DomESP1"><img src="https://images.creasol.it/creDomESP2_400.webp" alt="Relay board for ESP8266 NodeMCU module" style="float: left; margin-right: 2em; vertical-align: middle;" align="left" /></a>
IoT board designed for NodeMCU v3 board using ESP8266 WiFi microcontroller
* 9-24V input voltage, with high efficiency DC/DC regulator with 5V output
* 4x SPST relays 5V with overvoltage protection
* 1x SSR output (max 40V output)
* 2x mosfet output (max 30V, 10A) for LED dimming or other DC loads
* 1x I²C interface for sensors, extended I/Os and more)
* 1x OneWire interface (DS18B20 or other 1wire sensors/devices)
<br clear="all"/>


