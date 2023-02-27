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
from resource_management.core.resources.system import File
from resource_management.core.logger import Logger
from yarn_utils import *
import pwd,grp
import os


def install_flink(env):
    Logger.info('Creating Flink group')
    import params
    env.set_params(params)

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
    Directory([params.flink_installation_dir],
              mode=0755,
              cd_access='a',
              owner=params.flink_user,
              group=params.flink_group,
              create_parents=True
              )

    Logger.info('Check existing files')
    if os.path.exists(os.path.join(params.flink_installation_dir, 'flink.tar.gz')):
        Logger.info('Flink tarball exists. Delete it before downloading')
        Execute("rm -f {0}".format(os.path.join(params.flink_installation_dir, 'flink.tar.gz')))

    if os.path.exists(params.FLINK_HOME):
        Logger.info('Flink binary has been extracted. Delete it before installation')
        Execute("rm -rf {0}".format(params.FLINK_HOME))

    Logger.info('Downloading Flink binaries from: {0}'.format(params.flink_download_url))
    Execute("cd {0}; wget {1} -O flink.tar.gz".format(params.flink_installation_dir, params.flink_download_url),
            user=params.flink_user)

    Logger.info('Extracting Flink binaries')
    Execute("cd {0}; tar -zxvf flink.tar.gz".format(params.flink_installation_dir), user=params.flink_user)
    File(os.path.join(params.flink_installation_dir, "flink.tar.gz"), action='delete')

    Logger.info('Modify log folder access permissions')
    Execute("cd {0}; chmod 777 log".format(params.FLINK_HOME), user=params.flink_user)

    Logger.info('Delete Flink tarball')
    Execute("rm -f {0}".format(os.path.join(params.flink_installation_dir, 'flink.tar.gz')))

    Logger.info('Creating symbolic links')
    create_symbolic_link()

    Logger.info('Flink installation completed')


def configure_flink(env):
    Logger.info('Configuring Flink')
    import params
    env.set_params(params)
    flink_conf_dir = os.path.join(params.FLINK_HOME, 'conf')

    File(os.path.join(flink_conf_dir, 'flink-conf.yaml'),
         content=Template("flink-conf.yaml.j2"),
         owner=params.flink_user,
         group=params.flink_group
         )

    File(os.path.join(flink_conf_dir, "log4j.properties"),
         owner=params.flink_user,
         group=params.flink_group,
         content=params.log4j_props
         )

    File(os.path.join(flink_conf_dir, "log4j-cli.properties"),
         owner=params.flink_user,
         group=params.flink_group,
         content=params.log4j_cli_props
         )

    File(os.path.join(flink_conf_dir, "log4j-console.properties"),
         owner=params.flink_user,
         group=params.flink_group,
         content=params.log4j_console_props
         )

    File(os.path.join(flink_conf_dir, "log4j-session.properties"),
         owner=params.flink_user,
         group=params.flink_group,
         content=params.log4j_session_props
         )

    File(os.path.join(flink_conf_dir, "masters"),
         owner=params.flink_user,
         group=params.flink_group,
         content=params.masters
         )

    File(os.path.join(flink_conf_dir, "workers"),
         owner=params.flink_user,
         group=params.flink_group,
         content=params.workers
         )


def start_flink_standalone_cluster():
    Logger.info('Starting Flink standalone cluster')
    import params
    flink_bin_dir = os.path.join(params.FLINK_HOME, 'bin')
    Execute(os.path.join(flink_bin_dir, 'start-cluster.sh'))


def stop_flink_standalone_cluster():
    Logger.info('Stopping Flink standalone cluster')
    import params
    flink_bin_dir = os.path.join(params.FLINK_HOME, 'bin')
    Execute(os.path.join(flink_bin_dir, 'stop-cluster.sh'))


def start_flink_yarn_session():
    Logger.info('Starting Flink yarn session')
    import params
    flink_bin_dir = os.path.join(params.FLINK_HOME, 'bin')
    cmd = get_start_yarn_session_cmd(params.flink_yarn_session_name, params.jobmanager_memory_process_size,
                                     params.taskmanager_memory_process_size, params.slot_count)
    Execute(cmd, user=params.yarn_user)


def stop_flink_yarn_session():
    Logger.info('Stopping Flink yarn session')
    import params
    result = kill_yarn_application(params.flink_yarn_session_name)
    if result:
        Logger.info('Flink yarn session: {0} has been killed'.format(params.flink_yarn_session_name))
    else:
        Logger.info('Cannot not kill Flink yarn session: {0}. Maybe it is not running'.format(
            params.flink_yarn_session_name))


def get_start_yarn_session_cmd(yarn_session_name, jm_heap_size, tm_heap_size, slot_count):
    import params
    flink_bin_dir = os.path.join(params.FLINK_HOME, 'bin')
    return '{0} -d -nm {1} -jm {2} -tm {3} -s {4}'.format(os.path.join(flink_bin_dir, 'yarn-session.sh'), yarn_session_name, jm_heap_size, tm_heap_size, slot_count)


def create_symbolic_link():
    import params
    flink_bin_dir = os.path.join(params.FLINK_HOME, 'bin')
    # Link('/bin/yarn-session', to=os.path.join(flink_bin_dir, 'yarn-session.sh'))
    Link('/bin/flink', to=os.path.join(flink_bin_dir, 'flink'))
