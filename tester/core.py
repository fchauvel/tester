#
# SensApp::Tester
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



import pika

from influxdb import InfluxDBClient

import json

from os import listdir
from os.path import isdir, isfile, join

from time import sleep

from tester.sensors import Sensor, SensorInfos, Listener, wait_all




class Reporter(Listener):

    def __init__(self, ui):
        self._ui = ui

    def on_start(self, sensor):
        self._ui.sensor_started(sensor)

    def on_push(self, sensor, data):
        self._ui.data_pushed(sensor, data)

    def on_exit(self, sensor):
        self._ui.sensor_stopped(sensor)

    def on_error(self, sensor, error):
        self._ui.sensor_error(sensor, error)


    

class SensAppTests:

    def __init__(self, settings, ui, sensapp):
        self._settings = settings
        self._ui = ui
        self._sensapp = sensapp


    def run(self):
        sensors = Sensor.from_yaml(self._settings.sensors,
                                   self._sensapp.receiver,
                                   [Reporter(self._ui)])
        self._register_all(sensors)
        wait_all(*sensors)
        self._check_database(sensors)

        
    def _register_all(self, sensors):
        for each_sensor in sensors:
            self._sensapp.registry.register(each_sensor)

    
    DB_QUERY = "select * from {table}"

    def _check_database(self, sensors):
        client = InfluxDBClient(self._settings.db_host,
                                self._settings.db_port)
        
        client.switch_database(self._settings.db_name)

        verdict = []
        for each_sensor in sensors:
            query = self.DB_QUERY.format(table=each_sensor.about.identifier)
            result = client.query(query)
            verdict.append(sensor.name, len(result) == each.sensor.count)

        return verdict
