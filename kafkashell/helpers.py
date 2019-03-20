#  -*- coding: utf-8 -*-
#
#  Copyright 2019 Shawn Seymour. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"). You
#  may not use this file except in compliance with the License. A copy of
#  the License is located at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  or in the "license" file accompanying this file. This file is
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
#  ANY KIND, either express or implied. See the License for the specific
#  language governing permissions and limitations under the License.

from __future__ import print_function
from __future__ import unicode_literals

options_that_can_be_duplicated = [
    "--add-config",
    "--config",
    "--consumer-property",
    "--delete-config",
    "--producer-property",
    "--property",
    "--principal"
]


def exclude_options_from_removal(command_list):
    return [elem for elem in command_list if elem not in options_that_can_be_duplicated]


def cycle(my_list, start_at=None):
    index = my_list.index(start_at)
    start_at = 0 if start_at is None else index
    while True:
        start_at = (start_at + 1) % len(my_list)
        yield my_list[start_at]


def print_cluster_config(cluster):
    output = ""
    for key in cluster.keys():
        output += "{0}: {1}\n".format(key, cluster[key])
    print(output)
