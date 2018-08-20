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



class UI:


    SENSOR_REGISTERED = "Sensor '{sensor.name}' registered with ID '{sensor.identifier}'\n"
    SENSOR_STARTED = "Starting sensor '{sensor.name}' ...\n"
    SENSOR_STOPPED = "   {sensor.name:10} Shutting down ... \n"
    DATA_SENT = "   {sensor.name:10} Pushing data (value={data}) \n"
    SENSOR_ERROR = "   {sensor.name:10} ERROR: {error}\n"

    PASS = " - {name:10} OK"
    FAILED = " - {name:10} FAILED: Missing {count} entries!\n"


    def __init__(self, output):
        self._output = output


    def sensor_registered(self, sensor):
        self._print(self.SENSOR_REGISTERED, sensor=sensor)


    def sensor_starting(self):
        self._print(self.SENSOR_STARTING,)


    def sensor_started(self, sensor):
        self._print(self.SENSOR_STARTED, sensor=sensor)


    def data_pushed(self, sensor, data):
        self._print(self.DATA_SENT, sensor=sensor, data=data["fields"]["value"])


    def sensor_stopped(self, sensor):
        self._print(self.SENSOR_STOPPED, sensor=sensor)


    def sensor_error(self, sensor, error):
        self._print(self.SENSOR_ERROR, sensor=sensor, error=str(error))


    def show_verdict(self, verdict):
        self._print("Checking storage database ...\n")
        for name, count in verdict:
            if count == 0:
                self._print(self.PASS, name=name)
            else:
                self._print(self.FAILED, name=name, count=count)


    def _print(self, text, **values):
        self._output.write(text.format(**values))
