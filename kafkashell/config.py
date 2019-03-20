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

import json
import os
import sys

import oyaml as yaml
from jsonschema import validate, ValidationError


def get_completer(name="completer"):
    final_name = name if name == "completer" else "completer-{0}".format(name)
    data_dir = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(data_dir, "data/{0}.json".format(final_name))
    with open(data_path) as f:
        return json.load(f)


def init_config():
    shell_dir = get_kafka_shell_dir()
    config_file = get_user_config_path()

    if not os.path.exists(shell_dir):
        os.makedirs(shell_dir)

    if not os.path.isfile(config_file):
        with open(config_file, "w") as f:
            default_config = get_default_config()
            save_yaml(default_config, f)


def init_history():
    history_file = get_user_history_path()

    if not os.path.isfile(history_file):
        open(history_file, "a").close()


def get_config():
    config_file = get_user_config_path()

    with open(config_file) as f:
        return yaml.safe_load(f)


def validate_config(config):
    config_schema = get_config_schema()
    try:
        validate(instance=config, schema=config_schema)
        return config
    except ValidationError as ex:
        error_type = ", ".join(ex.path) if len(ex.path) > 0 else "root"
        print("Invalid user configuration ({0}): {1}".format(error_type, ex.message))
        sys.exit(1)


def save_config(updated_config):
    config_file = get_user_config_path()

    with open(config_file, "w") as f:
        save_yaml(updated_config, f)


def get_default_config():
    data_dir = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(data_dir, "data/shell-config.yaml")

    with open(data_path) as f:
        return yaml.safe_load(f)


def get_config_schema():
    data_dir = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(data_dir, "data/shell-config.schema")

    with open(data_path) as f:
        return json.load(f)


def save_yaml(config, f):
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def get_kafka_shell_dir():
    return os.path.expanduser("~/.kafka-shell")


def get_user_config_path():
    return os.path.expanduser("~/.kafka-shell/config.yaml")


def get_user_history_path():
    return os.path.expanduser("~/.kafka-shell/history")
