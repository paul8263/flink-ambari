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

from resource_management import *
from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.logger import Logger
from flink_utils import *
from service_check import *


class FlinkSlave(Script):
    def install(self, env):
        install_flink(env)
        self.configure(env)

    def stop(self, env):
        Logger.info('Slave does nothing on stop.')

    def start(self, env):
        Logger.info('Slave does nothing on start.')

    def status(self, env):
        raise ClientComponentHasNoStatus()

    def configure(self, env):
        configure_flink(env)

    def status(self, env):
        if not params.standalone_enabled:
            raise ClientComponentHasNoStatus()
        elif not is_task_manager_running():
            raise ComponentIsNotRunning()


if __name__ == '__main__':
    FlinkSlave().execute()
