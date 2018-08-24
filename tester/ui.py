#!/usr/bin/env python

#
# SensApp::Tester
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from tester import __program__, __version__, __license__, __copyright__


class UI:

    
    def __init__(self, output):
        self._output = output

    def welcome(self):
        self._print(self.PROGRAM,
                    program=__program__,
                    version=__version__,
                    license=__license__)
        self._print(self.COPYRIGHT,
                    copyright=__copyright__)

    PROGRAM = "{program} v{version} ({license})\n"
    COPYRIGHT = "{copyright}\n"

    
    def sensors_loaded(self, source):
        self._print(self.SENSORS_LOADED,
                    source=source)

    SENSORS_LOADED = "\n1. LOADING SENSORS (from '{source}')\n"
    
    
    def registration(self):
        self._print(self.REGISTRATION)
        self._print(self.REGISTRATION_ENTRY,
                    sensor="Sensor",
                    identifier="ID")
        
    REGISTRATION = "\n2. REGISTERING SENSORS:\n"
    REGISTRATION_ENTRY = "{sensor:>10} {identifier:>5}\n"

    
    def sensor_registered(self, sensor):
        self._print(self.REGISTRATION_ENTRY,
                    sensor=sensor.name,
                    identifier=sensor.identifier)

    def pushing(self):
        self._print(self.PUSHING_DATA)
        self._print(self.SENSOR_EVENT,
                    sensor="Sensor",
                    event="Action")

    PUSHING_DATA = "\n3. PUSHING DATA:\n"
    
    SENSOR_EVENT = "{sensor:>10} {event:<30}\n"
        

    def sensor_started(self, sensor):
        self._print(self.SENSOR_EVENT,
                    sensor=sensor.name,
                    event=self.STARTED)
        
    STARTED = "Started!"
        

    def data_pushed(self, sensor, data):
        value = data["fields"]["value"]
        self._print(self.SENSOR_EVENT,
                    sensor=sensor.name,
                    event=self.DATA_PUSHED.format(value=value))

    DATA_PUSHED = "Pushing value '{value}'" 

    
    def sensor_stopped(self, sensor):
        self._print(self.SENSOR_EVENT,
                    sensor=sensor.name,
                    event=self.SHUTTING_DOWN)

    SHUTTING_DOWN = "Shutting down!"


    def sensor_error(self, sensor, error):
        self._print(self.SENSOR_ERROR, sensor=sensor, error=str(error))

    SENSOR_ERROR = "{sensor.name:>10} ERROR: {error}\n"
    

    def show_verdict(self, verdict):
        self._print("\n3. VERDICT (DB check):\n")
        self._print(self.ENTRY,
                    sensor = "Sensor",
                    registered = "Registered",
                    found = "Found",
                    expected="Expected",
                    verdict="Verdict")
        for registered, sensor, expected, actual in verdict:
            verdict = "PASS" if expected == actual else "FAILED"
            self._print(self.ENTRY,
                        sensor=sensor.about.name,
                        registered=str(not registered),
                        found=actual,
                        expected=expected,
                        verdict=verdict)

    ENTRY = "{sensor:>10s} {registered:>15} {found:>10} {expected:>10} {verdict:>8s}\n"


    def goodbye(self):
        self._print(self.GOODBYE)

    GOODBYE = "\nThat's all folks!\n"

    
    def show_error(self, error):
        self._print(self.UNKNOWN_ERROR, error=str(error))
        
    UNKNOWN_ERROR= "/!\ Unexpected error: {error}\n"


    def retry(self, duration):
        self._print(UI.RETRY, duration=duration)

    RETRY= "    Retrying in {duration} sec.!\n"
    
    
    def _print(self, text, **values):
        self._output.write(text.format(**values))
