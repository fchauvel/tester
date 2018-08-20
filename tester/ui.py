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

    SENSOR_STARTED = "{sensor.name:>10} | Starting ...\n"
    SENSOR_STOPPED = "{sensor.name:>10} | Stopped!\n"
    DATA_SENT = "{sensor.name:>10} | Pushing data (value={data})!\n"
    SENSOR_ERROR = "{sensor.name:>10} | ERROR: {error}\n"

    PASS = "[ OK ]\n"
    FAILED = "[ FAILED ]\n"

    def __init__(self, output):
        self._output = output

    def sensor_started(self, sensor):
        self._print(self.SENSOR_STARTED, sensor=sensor)

    def data_pushed(self, sensor, data):
        self._print(self.DATA_SENT, sensor=sensor, data=data["fields"]["value"])

    def sensor_stopped(self, sensor):
        self._print(self.SENSOR_STOPPED, sensor=sensor)

    def sensor_error(self, sensor, error):
        self._print(self.SENSOR_ERROR, sensor=sensor, error=str(error))


    def show_verdict(self, verdict):
        if verdict:
            self._print(self.PASS)
        else:
            self._print(self.FAILED)


    def _print(self, text, **values):
        self._output.write(text.format(**values))
