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

    def on_stop(self, sensor):
        self._ui.sensor_stopped(sensor)

    def on_error(self, sensor, error):
        self._ui.sensor_error(sensor, error)


    

class SensAppTests:

    def __init__(self, settings, ui, sensapp):
        self._settings = settings
        self._ui = ui
        self._sensapp = sensapp


    def run(self):
        self._ui.welcome()
        with open(self._settings.sensors, "r") as source:
            try:
                sensors = Sensor.from_yaml(source,
                                           self._sensapp.receiver,
                                           [Reporter(self._ui)])
                self._ui.sensors_loaded(self._settings.sensors)
                
                sensors = self._classify(sensors)

                self._register_all(sensors)

                self._ui.pushing()
                wait_all(*[ each for _, each in sensors])
        
                verdict = self._check_database(sensors)
                self._ui.show_verdict(verdict)

                self._ui.goodbye()

            except Exception as error:
                self._ui.show_error(error)

                
    def _classify(self, sensors):
        return [ (each.is_registered, each) for each in sensors ]
            

        
    def _register_all(self, sensors):
        self._ui.registration()
        for is_registered, each_sensor in sensors:
            if not is_registered:
                self._sensapp.registry.register(each_sensor)
                self._ui.sensor_registered(each_sensor.about)

    
    DB_QUERY = "select * from \"sensor_{table}\";"

    def _check_database(self, sensors):
        client = InfluxDBClient(self._settings.db_host,
                                self._settings.db_port)

        client.switch_database(self._settings.db_name)

        verdict = []
        for registered, each_sensor in sensors:
            query = self.DB_QUERY.format(table=each_sensor.about.identifier)
            result = client.query(query)
            actual = len(list(result.get_points()))
            expected = each_sensor.count if not registered else 0
            verdict.append((registered, each_sensor, expected, actual))

        client.close()
        return verdict
