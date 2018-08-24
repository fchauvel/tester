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

from io import StringIO 

from tester import __program__, __version__, __copyright__, __license__
from tester.ui import UI
from tester.sensors import SensorInfos


class UITests(TestCase):


    def setUp(self):
        self._buffer = StringIO()
        self._ui = UI(self._buffer)
        self._data = { "fields":
                         {
                             "value": 4
                         }
                     }
        self._sensor_infos = SensorInfos(1, "test", "a test", "cm")

    def test_welcome(self):
        self._ui.welcome()

        self._assert_output_includes(UI.PROGRAM,
                                     program=__program__,
                                     version=__version__,
                                     license=__license__)
        self._assert_output_includes(UI.COPYRIGHT,
                                     copyright=__copyright__)

        
    def test_sensors_loaded(self):
        sensors_config = "data/test-sensors.yml"
        self._ui.sensors_loaded(sensors_config)

        self._assert_output_includes(UI.SENSORS_LOADED,
                                     source=sensors_config)
        

    def test_registration(self):
        self._ui.registration()

        self._assert_output_includes(UI.REGISTRATION)
        self._assert_output_includes(UI.REGISTRATION_ENTRY,
                                     sensor="Sensor",
                                     identifier="ID")
        

    def test_sensor_registered(self):
        self._ui.sensor_registered(self._sensor_infos)

        self._assert_output_includes(UI.REGISTRATION_ENTRY,
                                     sensor=self._sensor_infos.name,
                                     identifier=self._sensor_infos.identifier)

    def test_pushing(self):
        self._ui.pushing()

        self._assert_output_includes(UI.PUSHING_DATA)
        self._assert_output_includes(UI.SENSOR_EVENT,
                                     sensor="Sensor",
                                     event="Action")

    
    def test_sensor_started(self):
        self._ui.sensor_started(self._sensor_infos)
        
        self._assert_output_includes(UI.SENSOR_EVENT,
                                     sensor=self._sensor_infos.name,
                                     event=UI.STARTED)

    def test_data_pushed(self):
        self._ui.data_pushed(self._sensor_infos, self._data)

        self._assert_output_includes(UI.SENSOR_EVENT,
                                     sensor=self._sensor_infos.name,
                                     event=UI.DATA_PUSHED.format(value=self._data["fields"]["value"]))

    def test_sensor_stopped(self):
        self._ui.sensor_stopped(self._sensor_infos)

        self._assert_output_includes(UI.SENSOR_EVENT,
                                     sensor=self._sensor_infos.name,
                                     event=UI.SHUTTING_DOWN)
    

    def test_goodbye(self):
        self._ui.goodbye()

        self._assert_output_includes(UI.GOODBYE)
        
        
    def _assert_output_includes(self, pattern, **values):
        self.assertIn(pattern.format(**values),
                      self._buffer.getvalue())


        
