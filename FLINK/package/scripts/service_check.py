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
import os

from resource_management import *
from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.logger import Logger
import commands



def is_job_manager_running():
    cmd = "ps -ef | grep jobmanager | grep -v grep"
    output = commands.getoutput(cmd)
    return output.strip() != ''


def is_task_manager_running():
    cmd = "ps -ef | grep taskmanager | grep -v grep"
    output = commands.getoutput(cmd)
    return output.strip() != ''


class ServiceCheck(Script):
    def service_check(self, env):
        import params
        if not params.standalone_enabled:
            raise ClientComponentHasNoStatus()
        else:
            output = commands.getoutput(os.path.join(params.FLINK_HOME, 'bin/flink') + ' run {0}'.format(os.path.join(params.FLINK_HOME, 'examples/streaming/WordCount.jar')))
            if 'The program finished with the following exception' in output:
                raise ComponentIsNotRunning()


if __name__ == "__main__":
    ServiceCheck().execute()
