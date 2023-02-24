# -*- coding: utf-8 -*-
"""
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at
   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import commands
import re

INVALID_APPLICATION_ID = 'INVALID_APPLICATION_ID'


def get_yarn_application_id(yarn_application_name):
    output = commands.getoutput('yarn application -list | grep {0}'.format(yarn_application_name))
    line = output.split('\n')[-1]

    if yarn_application_name not in line:
        return INVALID_APPLICATION_ID

    return re.split(r'\s*', line)[0]


def kill_yarn_application(yarn_application_name):
    application_id = get_yarn_application_id(yarn_application_name)
    if application_id == INVALID_APPLICATION_ID:
        return False

    commands.getoutput('yarn application -kill {0}'.format(application_id))
    return True


def is_yarn_application_running(yarn_application_name):
    application_id = get_yarn_application_id(yarn_application_name)
    if application_id == INVALID_APPLICATION_ID:
        return False

    output = commands.getoutput('yarn application -status {0} | grep State'.format(application_id))
    line = output.split('\n')[-2]
    line_split = line.split(':')

    if len(line_split) < 2:
        return False
    else:
        return line_split[-1].strip() == "RUNNING"
