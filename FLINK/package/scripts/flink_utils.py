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
import os

FLINK_DIR_NAME = 'flink-1.13.2'


def get_start_yarn_session_cmd(flink_base_dir, yarn_session_name, jm_heap_size, tm_heap_size, slot_count):
    return '{0} -d -nm {1} -jm {2} -tm {3} -s {4}'.format(os.path.join(flink_base_dir, FLINK_DIR_NAME, 'bin/yarn-session.sh'), yarn_session_name, jm_heap_size, tm_heap_size, slot_count)


def create_symbolic_link():
    import params
    # Link('/bin/yarn-session', to=os.path.join(params.flink_base_dir, FLINK_DIR_NAME, 'bin/yarn-session.sh'))
    Link('/bin/flink', to=os.path.join(params.stack_base_dir, FLINK_DIR_NAME, 'bin/flink'))
