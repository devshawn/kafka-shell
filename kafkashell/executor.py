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

import os
import sys

from prompt_toolkit import shortcuts

from kafkashell import constants
from kafkashell import helpers
from kafkashell import version

valid_command_prefixes = (
    "kafka",
    "zookeeper",
    "ksql"
)


class Executor:

    def __init__(self, settings):
        self.settings = settings

    def execute(self, command):
        command = command.strip()
        if command == "exit":
            self.settings.save_settings()
            sys.exit(0)

        elif command == "clear":
            shortcuts.clear()

        elif command == "save":
            self.settings.save_settings()
            print("Saved settings!")

        elif command == "version":
            print(version.get_version())

        elif command.startswith("cluster-"):
            self.execute_cluster_command(command)

        elif command.startswith(valid_command_prefixes):
            self.execute_valid_command(command)

    def execute_valid_command(self, command):
        if command.startswith(constants.COMMAND_KAFKA_TOPICS):
            final_command = self.handle_kafka_topics_command(command)

        elif command.startswith(constants.COMMAND_KAFKA_CONFIGS):
            final_command = self.handle_kafka_configs_command(command)

        elif command.startswith(constants.COMMAND_KAFKA_CONSOLE_CONSUMER):
            final_command = self.handle_kafka_console_consumer_command(command)

        elif command.startswith(constants.COMMAND_KAFKA_CONSOLE_PRODUCER):
            final_command = self.handle_kafka_console_producer_command(command)

        elif command.startswith(constants.COMMAND_KAFKA_AVRO_CONSOLE_CONSUMER):
            final_command = self.handle_kafka_avro_console_consumer_command(command)

        elif command.startswith(constants.COMMAND_KAFKA_AVRO_CONSOLE_PRODUCER):
            final_command = self.handle_kafka_avro_console_producer_command(command)

        elif command.startswith(constants.COMMAND_KAFKA_VERIFIABLE_CONSUMER):
            final_command = self.handle_kafka_verifiable_consumer(command)

        elif command.startswith(constants.COMMAND_KAFKA_VERIFIABLE_PRODUCER):
            final_command = self.handle_kafka_verifiable_producer(command)

        elif command.startswith(constants.COMMAND_KAFKA_CONSUMER_GROUPS):
            final_command = self.handle_kafka_consumer_groups_command(command)

        elif command.startswith(constants.COMMAND_KAFKA_PREFERRED_REPLICA_ELECTION):
            final_command = self.handle_kafka_preferred_replica_election(command)

        elif command.startswith(constants.COMMAND_KAFKA_REPLICA_VERIFICATION):
            final_command = self.handle_kafka_replica_verification_command(command)

        elif command.startswith(constants.COMMAND_KAFKA_BROKER_API_VERSIONS):
            final_command = self.handle_kafka_broker_api_versions_command(command)

        elif command.startswith(constants.COMMAND_KAFKA_DELETE_RECORDS):
            final_command = self.handle_kafka_delete_records_command(command)

        elif command.startswith(constants.COMMAND_KAFKA_LOG_DIRS):
            final_command = self.handle_kafka_log_dirs_command(command)

        elif command.startswith(constants.COMMAND_KAFKA_ACLS):
            final_command = self.handle_kafka_acls_command(command)

        elif command.startswith(constants.COMMAND_KSQL):
            final_command = self.handle_ksql_command(command)

        elif command.startswith(constants.COMMAND_ZOOKEEPER_SHELL):
            final_command = self.handle_zookeeper_shell_command(command)

        else:
            final_command = command

        if self.check_for_valid_command_prefix():
            command_prefix = self.settings.get_cluster_details()["command_prefix"].strip()
            final_command = "{0} {1}".format(command_prefix, final_command)

        os.system(final_command)

    def execute_cluster_command(self, command):
        split_text = command.split(" ")
        if len(split_text) > 1:
            if len(split_text) > 2:
                print("Too many arguments!")
            else:
                if split_text[0] == "cluster-select":
                    self.handle_cluster_select(split_text)

                elif split_text[0] == "cluster-describe":
                    self.handle_cluster_describe(split_text)
        else:
            print("Please enter a cluster name.")

    # Handlers

    def handle_cluster_select(self, split_text):
        if split_text[1] in self.settings.user_config["clusters"]:
            self.settings.cluster = split_text[1]
            print("Selected cluster: {0}".format(split_text[1]))
        else:
            print("Unknown cluster!")

    def handle_cluster_describe(self, split_text):
        try:
            cluster = self.settings.user_config["clusters"][split_text[1]]
            helpers.print_cluster_config(cluster)
        except KeyError:
            print("Unknown cluster!")

    def handle_kafka_topics_command(self, command):
        command += self.handle_zookeeper_flag(command)
        return command

    def handle_kafka_configs_command(self, command):
        command += self.handle_zookeeper_flag(command)
        command += self.handle_admin_client_settings(command)
        return command

    def handle_kafka_console_consumer_command(self, command):
        command += self.handle_bootstrap_server_flag(command)
        command += self.handle_cli_settings(command, "consumer")
        return command

    def handle_kafka_console_producer_command(self, command):
        command += self.handle_broker_list_flag(command)
        command += self.handle_cli_settings(command, "producer")
        return command

    def handle_kafka_avro_console_consumer_command(self, command):
        command += self.handle_bootstrap_server_flag(command)
        command += self.handle_schema_registry_url_property(command)
        command += self.handle_cli_settings(command, "consumer")
        return command

    def handle_kafka_avro_console_producer_command(self, command):
        command += self.handle_broker_list_flag(command)
        command += self.handle_schema_registry_url_property(command)
        command += self.handle_cli_settings(command, "producer")
        return command

    def handle_kafka_verifiable_consumer(self, command):
        command += self.handle_broker_list_flag(command)
        command += self.handle_config(command, "consumer.config", "consumer")
        return command

    def handle_kafka_verifiable_producer(self, command):
        command += self.handle_broker_list_flag(command)
        command += self.handle_config(command, "producer.config", "producer")
        return command

    def handle_kafka_consumer_groups_command(self, command):
        command += self.handle_bootstrap_server_flag(command)
        command += self.handle_admin_client_settings(command)
        return command

    def handle_kafka_preferred_replica_election(self, command):
        command += self.handle_bootstrap_server_flag(command)
        command += self.handle_admin_client_settings(command)
        return command

    def handle_kafka_replica_verification_command(self, command):
        command += self.handle_broker_list_flag(command)
        return command

    def handle_kafka_broker_api_versions_command(self, command):
        command += self.handle_bootstrap_server_flag(command)
        command += self.handle_admin_client_settings(command)
        return command

    def handle_kafka_delete_records_command(self, command):
        command += self.handle_bootstrap_server_flag(command)
        command += self.handle_admin_client_settings(command)
        return command

    def handle_kafka_log_dirs_command(self, command):
        command += self.handle_bootstrap_server_flag(command)
        command += self.handle_admin_client_settings(command)
        return command

    def handle_kafka_acls_command(self, command):
        command += self.handle_bootstrap_server_flag(command)
        command += self.handle_admin_client_settings(command)
        return command

    def handle_ksql_command(self, command):
        command += self.handle_ksql_input(command)
        return command

    def handle_zookeeper_shell_command(self, command):
        command += self.handle_zookeeper_shell_input(command)
        return command

    # Helpers

    def handle_zookeeper_flag(self, command):
        if constants.FLAG_ZOOKEEPER not in command:
            zookeeper_flag = self.wrap_with_spaces(constants.FLAG_ZOOKEEPER)
            return zookeeper_flag + self.settings.get_cluster_details()["zookeeper_connect"]
        else:
            return ""

    def handle_bootstrap_server_flag(self, command):
        if constants.FLAG_BOOTSTRAP_SERVER not in command:
            bootstrap_server_flag = self.wrap_with_spaces(constants.FLAG_BOOTSTRAP_SERVER)
            return bootstrap_server_flag + self.settings.get_cluster_details()["bootstrap_servers"]
        else:
            return ""

    def handle_broker_list_flag(self, command):
        if constants.FLAG_BROKER_LIST not in command:
            broker_list_flag = self.wrap_with_spaces(constants.FLAG_BROKER_LIST)
            return broker_list_flag + self.settings.get_cluster_details()["bootstrap_servers"]
        else:
            return ""

    def handle_schema_registry_url_property(self, command):
        if constants.FLAG_SCHEMA_REGISTRY_URL not in command:
            return " {0}={1}".format(constants.FLAG_SCHEMA_REGISTRY_URL,
                                     self.settings.get_cluster_details()["schema_registry_url"])
        else:
            return ""

    def handle_ksql_input(self, command):
        return " -- " + self.settings.get_cluster_details()["ksql_server_url"] if " -- " not in command else ""

    def handle_zookeeper_shell_input(self, command):
        return " " + self.settings.get_cluster_details()["zookeeper_connect"] if len(command.split()) == 1 else ""

    def handle_admin_client_settings(self, command):
        if "admin_client_settings" in self.settings.get_cluster_details().keys():
            admin_client_option = "command-config" if constants.COMMAND_KAFKA_PREFERRED_REPLICA_ELECTION \
                                                      not in command else "admin.config"
            return self.handle_config(command, admin_client_option, "admin_client")
        else:
            return ""

    def handle_cli_settings(self, command, settings_type):
        if "{0}_settings".format(settings_type) in self.settings.get_cluster_details().keys():
            return "".join([
                self.handle_config(command, "{0}.config".format(settings_type), settings_type),
                self.handle_properties(settings_type)
            ])
        else:
            return ""

    def handle_config(self, command, config_prefix, settings_type):
        if "--{}".format(config_prefix) not in command:
            config = self.get_config_from_settings(settings_type)
            return " --{0} {1}".format(config_prefix, config) if config is not None else ""
        else:
            return ""

    def handle_properties(self, settings_type):
        properties = self.get_properties_from_settings(settings_type)
        return "".join([self.format_property(key, properties) for key in sorted(list(properties.keys()))])

    @staticmethod
    def format_property(key, properties):
        value = str(properties[key]).lower() if isinstance(properties[key], bool) else properties[key]
        return " --property {0}={1}".format(key, value)

    def get_properties_from_settings(self, settings_type):
        try:
            return self.settings.get_cluster_details()["{0}_settings".format(settings_type)]["properties"]
        except KeyError:
            return {}

    def get_config_from_settings(self, settings_type):
        try:
            return self.settings.get_cluster_details()["{0}_settings".format(settings_type)]["config"]
        except KeyError:
            return None

    def check_for_valid_command_prefix(self):
        return "command_prefix" in self.settings.get_cluster_details() \
               and \
               len(self.settings.get_cluster_details()["command_prefix"]) > 0

    @staticmethod
    def wrap_with_spaces(string):
        return " {0} ".format(string)
