#
# SensApp::Tester
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



import requests

import json



class SensApp:

    def __init__(self, settings, registry=None, receiver=None):
        self._registry = registry or Registry(settings)
        self._receiver = receiver or Receiver(settings)


    @property
    def receiver(self):
        return self._receiver


    @property
    def registry(self):
        return self._registry



class Registry:


    URL = "http://{host}:{port}/sensapp/"


    def __init__(self, settings):
        self._host = "registry"
        self._port = 4567


    def register(self, sensor):
        json_payload = json.dumps({
            "name": sensor.name,
            "description": sensor.description,
            "unit": sensor.unit
        })

        headers = { "Content-Type": "application/json" }
        url = (self.URL + "sensors/").format(host=self._host,
                                             port=self._port)

        response = requests.post(url, data=json_payload, headers=headers)
        if response.status_code != 200:
            response.raise_for_status()
        data = json.parse(response.text)
        sensor.identifier = data["id"]


    def all_sensors(self):
        pass

    def sensor_with_id(self, sensor_id):
        pass



class Receiver:


    PUBLISH = "http://{host}:{port}/sensapp/{id}"


    def __init__(self, settings):
        self._host = "receiver"
        self._port = 3000


    def accept(self, sensor_id, data):
        json_payload = json.dumps(data)
        headers = { "Content-Type": "application/json" }
        url = self.PUBLISH.format(host=self._host,
                                  port=self._port,
                                  id=sensor_id)

        response = requests.post(url, data=json_payload, headers=headers)
        if response.status_code != 200:
            response.raise_for_status()
