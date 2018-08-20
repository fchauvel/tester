#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

FROM python:3.4-slim

LABEL maintainer "franck.chauvel@sintef.no"

# Update the dist and install needed tools
RUN apt-get -qq update
RUN apt-get -qq -y install git python3-dev

# Fetch, build and install sensapp-storage
RUN git clone https://github.com/fchauvel/tester.git
WORKDIR tester
RUN pip install -r requirements.txt
RUN pip install .

# Run sensapp-storage
CMD ["sensapp-tester", "-q", "task-queue", "-n", "SENSAPP_TASK"]
