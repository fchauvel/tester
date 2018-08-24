#
# SensApp::Tester
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from unittest import TestCase
from unittest.mock import MagicMock

from threading import enumerate

from tester.sensors import Sensor, SensorInfos, wait_all, Listener



def make_sensor(index=1, data=None, receiver=None, listeners=None):
    infos = SensorInfos(None, "sensor_%d" % index, "test sensor", "cm")
    return Sensor(infos,
                  period=0,
                  data_source = data or range(10),
                  receiver = receiver or MagicMock())


class FiniteSensorTests(TestCase):


    def setUp(self):
        self.data = range(20)
        self.receiver = MagicMock()
        self.sensor = make_sensor(1, self.data, self.receiver)


    def test_sensor_push_all_its_data(self):
        self.sensor.start()
        self.sensor.wait_for_completion()
        self.assertEqual(len(self.data), self.receiver.accept.call_count)


        
class SensorFromYAMLTests(TestCase):

    def test_all_sensors_are_read(self):
        with open("./data/sensors.yml", "r") as source:
            sensors = Sensor.from_yaml(source,
                                       MagicMock(),
                                       [MagicMock()])
                
            self.assertEqual(len(sensors), 3)
            for each in sensors:
                self.assertEqual(1, len(each._listeners))

    def test_loading_sensor_that_are_not_registered(self):
        receiver = MagicMock()
        text = ("sensors:\n"
                "   test:\n"
                "      id: 1001\n"
                "      period: 2\n"
                "      data: [1, 2, 3, 4]\n"
                "      description: A test sensor that is registered\n"
                "      unit: km/h\n")

        sensors = Sensor.from_yaml(text, receiver, None)

        self.assertEqual(1, len(sensors))
        self.assertEqual(1001, sensors[0].about.identifier)
        

        
class WaitAllTests(TestCase):

    def test_all_sensors_stop(self):
        listeners = [ MagicMock(Listener) ]
        receiver = MagicMock()
        sensors = [ make_sensor(i, range(10), receiver, listeners) for i in range(5) ]

        wait_all(*sensors)

        for each in sensors:
            self.assertFalse(each.is_running)

        self.assertEqual(1, len(enumerate()))
        self.assertEqual(5 * 10, receiver.accept.call_count)
