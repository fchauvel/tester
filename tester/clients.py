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



class Receiver:

    
    PUBLISH = "http://receiver:3000/sensapp/{id}"

    
    def __init__(self, settings):
        self._host = "receiver"
        self._port = 3000


    def accept(self, sensor_id, data):
        json_payload = json.dumps(data)
        headers = { "Content-Type": "application/json" }
        url = self.PUBLISH.format(id=sensor_id)
        
        response = requests.post(url, data=json_payload, headers=headers)
        if response.status_code != 200:
            response.raise_for_status()
        
        
