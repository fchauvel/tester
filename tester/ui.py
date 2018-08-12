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



class UI:

    TESTING_FILE = "Testing with content from '{file}' ... "
    PASS = "[ OK ]\n"
    FAILED = "[ FAILED ]\n"

    def __init__(self, output):
        self._output = output


    def show_testing(self, file_name):
        self._print(self.TESTING_FILE, file=file_name)


    def show_verdict(self, verdict):
        if verdict:
            self._print(self.PASS)
        else:
            self._print(self.FAILED)


    def _print(self, text, **values):
        self._output.write(text.format(**values))
