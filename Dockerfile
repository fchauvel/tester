#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

FROM python:3.5-alpine

LABEL maintainer "franck.chauvel@sintef.no"

WORKDIR /tester
COPY . /tester

# Install sensapp tester
RUN pip install -r requirements.txt
RUN pip install .

# Run sensapp-tester
CMD ["sensapp-tester", "-q", "task-queue", "-n", "SENSAPP_TASK"]
