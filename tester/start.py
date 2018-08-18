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



from sys import stdout, argv

from tester.settings import Settings
from tester.core import SensAppTests
from tester.ui import UI
from tester.clients import Receiver



def main():
    settings = Settings.from_command_line(argv[1:])
    tests = SensAppTests(settings, UI(stdout), Receiver(settings))
    tests.run()
