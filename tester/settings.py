#
# SensApp::Tester
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from argparse import ArgumentParser

from tester import __command__, __description__



SHORTCUT = 0
FULL_NAME = 1
DEFAULT = 2
HELP = 3


class Settings:

    PARAMETERS = {
        "data_directory": (
            "-d",
            "--json-data",
            "./data",
            "Set the path to the fake sensors' data"),
        "queue_host": (
            "-q",
            "--queue-host",
            "localhost",
            "Set the host where the  message queue runs"),
        "queue_port": (
            "-p",
            "--queue-port",
            5672,
            "Set the port on which the message queue is listening"),
        "queue_name": (
            "-n",
            "--queue-name",
            "SENSAPP_TASKS",
            "Set the name of the message queue to use"),
        "db_host": (
            "-o",
            "--db-host",
            "localhost",
            "Set the host name where the DB runs"),
        "db_port": (
            "-r",
            "--db-port",
            8086,
            "Set the port on which the DB is listening"),
        "db_name": (
            "-m",
            "--db-name",
            "sensapp",
            "Set the name of the DB that contains sensors' data")
    }


    def __init__(self, **kwargs):
        for key, parameter in Settings.PARAMETERS.items():
            content = kwargs.get(key, None) or parameter[DEFAULT]
            setattr(self, "_" + key, content)


    def __getattr__(self, name):
        if name in self.PARAMETERS:
            return self.__dict__["_" + name]
        else:
            raise AttributeError("Settings have no attribute '%s'" %  name)


    @staticmethod
    def from_command_line(array):
        parser = ArgumentParser(prog=__command__,
                                description=__description__)
        for key, parameter in Settings.PARAMETERS.items():
            parser.add_argument(parameter[SHORTCUT],
                                parameter[FULL_NAME],
                                dest=key,
                                help=Settings.help_message(parameter))

        arguments = parser.parse_args(array)
        return Settings(**vars(arguments))


    @staticmethod
    def help_message(parameter):
        return parameter[HELP] + " (default: {})".format(parameter[DEFAULT])
