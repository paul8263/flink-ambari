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
from resource_management.core.resources.system import File
from resource_management.core.logger import Logger
from yarn_utils import *
from flink_utils import *
import pwd,grp
import os


class FlinkSlave(Script):

    def install(self, env):
        import params

        Logger.info('Creating Flink group')

        try:
            grp.getgrnam(params.flink_group)
        except KeyError:
            Group(params.flink_group)

        Logger.info('Creating Flink user')
        try:
            pwd.getpwnam(params.flink_user)
        except KeyError:
            User(params.flink_user,
                 gid=params.flink_group,
                 groups=[params.flink_group],
                 ignore_failures=True
                 )

        Logger.info('Creating Flink install directory')
        Directory([params.stack_base_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.flink_user,
                  group=params.flink_group,
                  create_parents=True
                  )

        Logger.info('Downloading Flink binaries')
        Execute("cd {0}; wget {1} -O flink.tar.gz".format(params.stack_base_dir, params.flink_download_url),
                user=params.flink_user)

        Logger.info('Extracting Flink binaries')
        Execute("cd {0}; tar -zxvf flink.tar.gz".format(params.stack_base_dir), user=params.flink_user)
        File(os.path.join(params.stack_base_dir, "flink.tar.gz"), action='delete')

        Logger.info('Modify log folder access permissions')
        Execute("cd {0}; chmod 777 log".format(os.path.join(params.stack_base_dir, params.FLINK_DIR_NAME)), user=params.flink_user)

        Logger.info('Creating symbolic links')
        create_symbolic_link()

        self.configure(env)

        Logger.info('Flink installation completed')

    def stop(self, env):
        import params

        result = kill_yarn_application(params.flink_yarn_session_name)

        if result:
            Logger.info('Flink yarn session: {0} has been killed'.format(params.flink_yarn_session_name))
        else:
            Logger.info('Cannot not kill Flink yarn session: {0}. Maybe it is not running'.format(
                params.flink_yarn_session_name))

    def start(self, env):
        import params

        Logger.info('Updating Flink configuration')
        self.configure(env)

        Logger.info('Starting Flink yarn session')
        cmd = get_start_yarn_session_cmd(params.stack_base_dir, params.flink_yarn_session_name,
                                         params.job_manager_heap_size, params.task_manager_heap_size, params.slot_count)
        Execute(cmd, user=params.flink_user)

        Logger.info('Flink yarn session started')

    def status(self, env):
        raise ClientComponentHasNoStatus()

    def configure(self, env):
        import params
        import os

        Logger.info('Configuring Flink')
        env.set_params(params)

        File("{0}/{1}/conf/flink-conf.yaml".format(params.stack_base_dir, FLINK_DIR_NAME),
             content=Template("flink-conf.yaml.j2"),
             owner=params.flink_user,
             group=params.flink_group
             )


        if params.log4j_props is not None:
            Logger.info('log4j_props is not empty!')
            Logger.info('Creating log4j.properties')
            File(os.path.join(params.stack_base_dir, FLINK_DIR_NAME, "conf/log4j.properties"),
                 owner=params.flink_user,
                 group=params.flink_group,
                 content=params.log4j_props
                 )
        elif os.path.exists(os.path.join(params.stack_base_dir, FLINK_DIR_NAME, "conf/log4j.properties")):
            Logger.info('log4j_props is empty!')
            Logger.info('Creating log4j.properties')
            File(os.path.join(params.stack_base_dir, FLINK_DIR_NAME, "conf/log4j.properties"),
                 owner=params.flink_user,
                 group=params.flink_group
                 )

        if params.log4j_cli_props is not None:
            Logger.info('log4j_cli_props is not empty!')
            Logger.info('Creating log4j-cli.properties')
            File(os.path.join(params.stack_base_dir, FLINK_DIR_NAME, "conf/log4j-cli.properties"),
                 owner=params.flink_user,
                 group=params.flink_group,
                 content=params.log4j_cli_props
                 )
        elif os.path.exists(os.path.join(params.stack_base_dir, FLINK_DIR_NAME, "conf/log4j-cli.properties")):
            Logger.info('log4j_cli_props is empty!')
            Logger.info('Creating log4j-cli.properties')
            File(os.path.join(params.stack_base_dir, FLINK_DIR_NAME, "conf/log4j-cli.properties"),
                 owner=params.flink_user,
                 group=params.flink_group
                 )

if __name__ == '__main__':
    FlinkSlave().execute()
