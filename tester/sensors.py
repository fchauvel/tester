#
# SensApp::Tester
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



import yaml

from tester import __program__

from threading import Thread, Event, Barrier

from time import sleep

from datetime import datetime



class SensorInfos:

    def __init__(self, identifier, name, description, unit):
        self._identifier = identifier
        self._name = name
        self._description = description
        self._unit = unit


    @property
    def identifier(self):
        return self._identifier


    @identifier.setter
    def identifier(self, new_identifier):
        self._identifier = new_identifier


    @property
    def name(self):
        return self._name


    @property
    def description(self):
        return self._description


    @property
    def unit(self):
        return self._unit



class Sensor:


    def __init__(self, infos, period, data_source, receiver, listeners=None):
        self._infos = infos
        self._period = period
        self._receiver = receiver
        self._data_source = data_source
        self._stopped = Event()
        self._thread = None
        self._count = 0
        self._listeners = listeners or []


    def add_listener(self, listener):
        self._listeners.append(listener)


    @property
    def count(self):
        return self._count


    @property
    def about(self):
        return self._infos


    @property
    def period(self):
        return self._period


    def start(self):
        self._thread = Thread(target=self._sense)
        self._stopped.clear()
        self._thread.start()


    def _sense(self):
        for each in self._listeners:
            each.on_start(self._infos)

        for each in self._data_source:
            if self.has_stopped:
                break

            data = [ {
                "measurement": "sensor_" + str(self._infos.identifier),
                "tags": {
                    "source": __program__
                },
                "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fields": {
                    "value": each
                }
            } ]

            try:
                self._receiver.accept(self._infos.identifier, data)
                for each in self._listeners:
                    each.on_push(self._infos, data[0])

            except Exception as error:
                for each in self._listeners:
                    each.on_error(self._infos, error)

            self._count += 1
            sleep(self._period)

        self._stopped.set()

        for each in self._listeners:
            each.on_stop(self._infos)


    @property
    def has_stopped(self):
        return not self.is_running


    @property
    def is_running(self):
        return not self._stopped.is_set()


    def wait_for_completion(self):
        self._thread.join()


    def stop(self):
        self._stopped.set()
        self._thread.join()


    @staticmethod
    def from_yaml(yamlfile, receiver, listeners):
        sensors = []
        with open(yamlfile, "r") as source:
            obj = yaml.load(source)
            for name, sensor in obj["sensors"].items():
                infos = SensorInfos(None,
                                   name,
                                   sensor["description"],
                                   sensor["unit"])
                sensor = Sensor(infos,
                                int(sensor["period"]),
                                (v for v in sensor["data"]),
                                receiver,
                                listeners)
                sensors.append(sensor)
        return sensors



class Listener:

    def on_start(self, sensor):
        pass

    def on_push(self, sensor, data):
        pass

    def on_stop(self, sensor):
        pass

    def on_error(self, sensor, error):
        pass



class BarrierListener(Listener):

    def __init__(self, barrier):
        self._barrier = barrier

    def on_stop(self, sensor):
        self._barrier.wait()



def wait_all(*sensors):
    barrier = Barrier(len(sensors)+1)
    for each_sensor in sensors:
        each_sensor.add_listener(BarrierListener(barrier))
        each_sensor.start()
    barrier.wait()
