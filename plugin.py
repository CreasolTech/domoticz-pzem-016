#!/usr/bin/env python
"""
domoticz-pzem-016 energy meter plugin for Domoticz.
Author: Paolo Subiaco https://github.com/CreasolTech

Requirements:
    1.python module minimalmodbus -> http://minimalmodbus.readthedocs.io/en/master/
        (pi@raspberrypi:~$ sudo pip3 install minimalmodbus)
    2.USB to RS485 adapter/onverter 

Words to translate in other languages (in double quotes):
English (en)            Italian (it)            YourLanguage (??)
"Power/Energy"          "Potenza/Energia"       ""
"Voltage"               "Tensione"              ""
"Current"               "Corrente"              ""
"Frequency"             "Frequenza"             ""
"Power Factor"          "Fattore di Potenza"    ""

"""

"""
<plugin key="pzem-016" name="PZEM-016 PZEM-014 PZEM-004T energy meters"  version="1.0" author="CreasolTech" externallink="https://github.com/CreasolTech/domoticz-pzem-016">
    <description>
        <h2>Domoticz plugin for PZEM-016, PZEM-014 and PZEM-004T energy meters - Version 1.0 </h2>
        More than one meter can be connected to the same bus, specifying their addresses separated by comma, for example <tt>1,2,3,124</tt> to read energy meters with slave address 1, 2, 3, 124<br/>
        For more info please check the <a href="https://github.com/CreasolTech/domoticz-pzem-016">GitHub plugin page</a>
    </description>
    <params>
        <param field="SerialPort" label="Modbus Port" width="200px" required="true" default="/dev/ttyUSB0" />
        <param field="Mode1" label="Baud rate" width="40px" required="true" default="9600"  />
        <param field="Mode3" label="Poll interval">
            <options>
                <option label="2 seconds" value="2" />
                <option label="3 seconds" value="3" />
                <option label="4 seconds" value="4" />
                <option label="5 seconds" value="5" default="true" />
                <option label="10 seconds" value="10" />
                <option label="20 seconds" value="20" />
                <option label="30 seconds" value="30" />
            </options>
        </param>
        <param field="Mode2" label="Meter address" width="40px" required="true" default="2,3,4" />
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>

"""

import minimalmodbus    #v2.1.1
import Domoticz         #tested on Python 3.9.2 in Domoticz 2021.1 and 2023.1



LANGS=[ "en", "it" ] # list of supported languages, in DEVS dict below
DEVTYPE=0
DEVSUBTYPE=1
DEVSWITCHTYPE=2
DEVOPTIONS=3
DEVIMAGE=4
DEVLANG=5  # item in the DEVS list where the first language starts 

DEVS={ #unit:     Type,Sub,swtype, Options, Image,  "en name", "it name"  ...other languages should follow  ],
            1:  [ 243,29,0,     None,       None,   "Power/Energy",     "Potenza/Energia"   ],
            2:  [ 243,8,0,      None,       None,   "Voltage",          "Tensione"      ],
            3:  [ 243,23,0,     None,       None,   "Current",          "Corrente"      ],
            4:  [ 243,31,0,     {'Custom': '1;Hz'}, None,   "Frequency","Frequenza"     ],
            5:  [ 243,31,0,     None,       None,   "Power Factor",     "Fattore di Potenza"   ],
}

DEVSMAX=5;

class BasePlugin:
    def __init__(self):
        self.rs485 = ""
        return

    def onStart(self):
        Domoticz.Log("Starting PZEM-016 PZEM-014 plugin")
        self.pollTime=30 if Parameters['Mode3']=="" else int(Parameters['Mode3'])
        Domoticz.Heartbeat(self.pollTime)
        self.runInterval = 1
        self._lang=Settings["Language"]
        # check if language set in domoticz exists
        if self._lang in LANGS:
            self.lang=DEVLANG+LANGS.index(self._lang)
        else:
            Domoticz.Log(f"Language {self._lang} does not exist in dict DEVS, inside the domoticz-emmeti-mirai plugin, but you can contribute adding it ;-) Thanks!")
            self._lang="en"
            self.lang=DEVLANG # default: english text

        self.slaves=Parameters["Mode2"].split(',')

        # Check that all devices exist, or create them
        s=0     # s used to compute unit for each energy meter: s=0, 5, 10, 15, ... (base unit number for the current energy meter)
        for slave in self.slaves:
            for i in DEVS:
                unit=s+i
                if unit not in Devices:
                    Options=DEVS[i][DEVOPTIONS] if DEVS[i][DEVOPTIONS] else {}
                    Image=DEVS[i][DEVIMAGE] if DEVS[i][DEVIMAGE] else 0
                    Domoticz.Log(f"Creating device Name={DEVS[i][self.lang]}, Unit=unit, Type={DEVS[i][DEVTYPE]}, Subtype={DEVS[i][DEVSUBTYPE]}, Switchtype={DEVS[i][DEVSWITCHTYPE]} Options={Options}, Image={Image}")
                    Domoticz.Device(Name=DEVS[i][self.lang], Unit=unit, Type=DEVS[i][DEVTYPE], Subtype=DEVS[i][DEVSUBTYPE], Switchtype=DEVS[i][DEVSWITCHTYPE], Options=Options, Image=Image, Used=1).Create()
            s+=DEVSMAX;


    def onStop(self):
        Domoticz.Log("Stopping PZEM-016 PZEM-014 plugin")

    def onHeartbeat(self):
        s=0
        for slave in self.slaves:
            # read all registers in one shot
            try:
                self.rs485 = minimalmodbus.Instrument(Parameters["SerialPort"], int(slave))
                self.rs485.serial.baudrate = Parameters["Mode1"]
                self.rs485.serial.bytesize = 8
                self.rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
                self.rs485.serial.stopbits = 1
                self.rs485.serial.timeout = 0.5
                self.rs485.serial.exclusive = False # Fix From Forum Member 'lost'
                self.rs485.debug = True
                self.rs485.mode = minimalmodbus.MODE_RTU
                self.rs485.close_port_after_each_call = True
                register=self.rs485.read_registers(0, 9, 4) # Read all registers from 0 to 8, using function code 4
                self.rs485.serial.close()  #  Close that door !
            except:
                Domoticz.Log(f"Error reading Modbus registers from device {slave}");
            else:
                voltage=register[0]/10                          # V
                current=(register[1] + (register[2]<<16))/1000  # A
                power=(register[3] + (register[4]<<16))/10      # W
                energy=(register[5] + (register[6]<<16))        # Wh
                frequency=register[7]/10                        # Hz
                pf=register[8]/100                              # %

                if Parameters["Mode6"] == 'Debug':
                    Domoticz.Log(f"Slave={slave}, P={power}W E={energy}Wh V={voltage}V I={current}A, f={frequency}Hz PF={pf}%")
                Devices[s+1].Update(0, str(power) + ';' + str(energy))
                Devices[s+2].Update(0, str(voltage))
                Devices[s+3].Update(0, str(current))
                Devices[s+4].Update(0, str(frequency))
                Devices[s+5].Update(0, str(pf))
            s+=DEVSMAX    # Increment the base for each device unit

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log(f"Command for {Devices[Unit].Name}: Unit={Unit}, Command={Command}, Level={Level}")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)


