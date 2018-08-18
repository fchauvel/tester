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


class SensAppTests:

    def __init__(self, settings, ui, receiver):
        self._settings = settings
        self._ui = ui
        self._receiver = receiver


    def run(self):
        data = self._fetch_json_from(self._settings.data_directory)
        for file_name, content in data:
            self._ui.show_testing(file_name)
            self._send_to_receiver(content)
            self._wait_for(3)
            verdict = self._check_database(content)
            self._ui.show_verdict(verdict)


    @staticmethod
    def _fetch_json_from(directory):
        json_files = []
        for any_entry in listdir(directory):
            full_path = join(directory, any_entry)
            if isfile(full_path) and any_entry.endswith(".json"):
                json_files.append((full_path, SensAppTests._content_of(full_path)))
            elif isdir(full_path):
                files_subdirectory = SensAppTests._fetch_json_from(full_path)
                json_files.extends(files_in_subdirectory)
        return json_files


    @staticmethod
    def _content_of(file_name):
        with open(file_name, "r") as data :
            text = data.read()
            return json.loads(text)

    def _send_to_receiver(self, data):
        sensor_id = data[0]["measurement"] 
        self._receiver.accept(sensor_id, data)
        

    def _send_to_message_queue(self, data):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._settings.queue_host))

        channel = connection.channel()
        channel.queue_declare(queue=self._settings.queue_name,
                              durable=True)

        json_payload = json.dumps(data)
        channel.basic_publish(
            exchange='',
            routing_key=self._settings.queue_name,
            body=json_payload,
            properties=pika.BasicProperties(delivery_mode = 2))

        connection.close()


    def _wait_for(self, duration):
        sleep(duration)


    def _check_database(self, data):
        client = InfluxDBClient(self._settings.db_host,
                                self._settings.db_port)
        client.switch_database(self._settings.db_name);

        query = "select * from {table} WHERE time = '{time}'".format(table=data[0]["measurement"],
                                                                   time=data[0]["time"])
        result = client.query(query)
        return len(result) == 1
