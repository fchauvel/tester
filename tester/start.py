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

from tester.sensapp import SensApp
from tester.settings import Settings
from tester.core import SensAppTests
from tester.ui import UI



def main():
    settings = Settings.from_command_line(argv[1:])

    sensapp = SensApp(settings)
    
    tests = SensAppTests(settings, UI(stdout), sensapp)
    tests.run()
