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

# from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *
# from resource_management.core.logger import Logger
import os
import repoin

config = Script.get_config()

# env settings

FLINK_TAR_NAME = 'flink.tar.gz'
STACK_VERSION = '3.0.1.0-187'
FLINK_DIR_NAME = 'flink-1.13.2'

flink_conf = config['configurations']['flink-conf']

flink_user = flink_conf['flink_user']
flink_group = flink_conf['flink_group']

flink_download_url = os.path.join(repoin.baseurl, 'flink', FLINK_TAR_NAME)

stack_root = Script.get_stack_root()

stack_base_dir = "{0}/{1}/flink".format(stack_root, STACK_VERSION)

# Common

jobmanager_rpc_address = flink_conf['jobmanager_rpc_address']
jobmanager_rpc_port = flink_conf['jobmanager_rpc_port']
jobmanager_heap_size = flink_conf['jobmanager_heap_size'] + 'm'
taskmanager_heap_size = flink_conf['taskmanager_heap_size'] + 'm'
taskmanager_numberOfTaskSlots = flink_conf['taskmanager_numberOfTaskSlots']
parallelism_default = flink_conf['parallelism_default']
fs_default_scheme = flink_conf['fs_default_scheme']

# High Availability
high_availability = flink_conf['high_availability']
high_availability_storageDir = flink_conf['high_availability_storageDir']
high_availability_zookeeper_quorum = flink_conf['high_availability_zookeeper_quorum']
high_availability_zookeeper_client_acl = flink_conf['high_availability_zookeeper_client_acl']

# Fault tolerance and checkpointing
state_backend = flink_conf['state_backend']
state_checkpoints_dir = flink_conf['state_checkpoints_dir']
state_savepoints_dir = flink_conf['state_savepoints_dir']
state_backend_incremental = flink_conf['state_backend_incremental']

# Rest & web frontend

rest_port = flink_conf['rest_port']
rest_address = flink_conf['rest_address']
rest_bind_port = flink_conf['rest_bind_port']
rest_bind_address = flink_conf['rest_bind_address']
web_submit_enable = flink_conf['web_submit_enable']
io_tmp_dirs = flink_conf['io_tmp_dirs']
taskmanager_memory_preallocate = flink_conf['taskmanager_memory_preallocate']
classloader_resolve_order = flink_conf['classloader_resolve_order']
taskmanager_network_memory_fraction = flink_conf['taskmanager_network_memory_fraction']
taskmanager_network_memory_min = flink_conf['taskmanager_network_memory_min']
taskmanager_network_memory_max = flink_conf['taskmanager_network_memory_max']

# Flink Cluster Security Configuration
security_kerberos_login_contexts = flink_conf['security_kerberos_login_contexts']
security_kerberos_login_use_ticket_cache = flink_conf['security_kerberos_login_use_ticket_cache']
security_kerberos_login_keytab = flink_conf['security_kerberos_login_keytab']
security_kerberos_login_principal = flink_conf['security_kerberos_login_principal']

# History server

jobmanager_archive_fs_dir = flink_conf['jobmanager_archive_fs_dir']
historyserver_web_address = flink_conf['historyserver_web_address']
historyserver_web_port = flink_conf['historyserver_web_port']
historyserver_archive_fs_dir = flink_conf['historyserver_archive_fs_dir']
historyserver_archive_fs_refresh_interval = flink_conf['historyserver_archive_fs_refresh_interval']

# Custom properties
custom_properties = flink_conf['custom_properties']

# log4j.properties
log4j_props = config['configurations']['flink-log4j']['content']

# log4j-cli.properties
log4j_cli_props = config['configurations']['flink-log4j-cli']['content']
