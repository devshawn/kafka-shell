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

from __future__ import unicode_literals

from fuzzyfinder import fuzzyfinder
from prompt_toolkit.completion import Completer, Completion

from kafkashell.config import get_completer
from kafkashell.helpers import exclude_options_from_removal


class KafkaCompleter(Completer):

    def __init__(self, settings):
        self.settings = settings
        self.commands = self.settings.commands

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        text_before_cursor = document.text_before_cursor
        text_list = text_before_cursor.split(" ")
        command = text_list[0]

        if self.is_not_command(document.text):
            option = text_list[-2]
            possible_option_value = text_list[-1]
            value_completer_name = self.get_completer_name_for_option(command, option)
            if self.has_option_value_completer(value_completer_name):
                for completion in self.yield_extra_completers(word_before_cursor, document, possible_option_value,
                                                              value_completer_name):
                    yield completion
            elif self.is_cluster_command(document.text):
                for completion in self.yield_clusters(word_before_cursor):
                    yield completion
            else:
                for completion in self.yield_options(word_before_cursor, document):
                    yield completion
        else:
            for completion in self.yield_commands(word_before_cursor):
                yield completion

    # yields
    def yield_commands(self, word_before_cursor):
        valid_keys = self.fuzzy(word_before_cursor, self.commands.keys())
        descriptions = self.get_command_descriptions()
        for key in valid_keys:
            display_meta = self.get_display_meta(descriptions, key)
            yield Completion(key, start_position=-len(word_before_cursor), display_meta=display_meta)

    def yield_options(self, word_before_cursor, document):
        valid_keys = self.get_valid_options(document, word_before_cursor)
        descriptions = self.get_option_descriptions(document.text.split(" ")[0]) if len(valid_keys) > 0 else {}
        for key in valid_keys:
            display_meta = self.get_display_meta(descriptions, key)
            yield Completion(key, start_position=-len(word_before_cursor), display_meta=display_meta)

    def yield_extra_completers(self, word_before_cursor, document, possible_option_value, value_completer_name):
        value_completer = get_completer(value_completer_name)["values"]

        if self.is_config_value(possible_option_value):
            key_value_array = possible_option_value.split("=")
            config_completer_name = self.get_completer_name_for_config(value_completer, key_value_array[0])
            if config_completer_name is not None:
                for completion in self.yield_config_completer(key_value_array[1], document, config_completer_name):
                    yield completion
        else:
            for completion in self.yield_option_value_completer(word_before_cursor, document, value_completer_name):
                yield completion

    def yield_option_value_completer(self, word_before_cursor, document, value_completer_name):
        option_values = get_completer(value_completer_name)["values"]
        valid_keys = self.get_valid_option_values(document, word_before_cursor, option_values, value_completer_name)
        descriptions = self.get_completer_descriptions(option_values)
        for key in valid_keys:
            display_meta = self.get_display_meta(descriptions, key)
            yield Completion(key, start_position=-len(word_before_cursor), display_meta=display_meta)

    def yield_config_completer(self, word_after_key, document, completer_name):
        config_completer = get_completer(completer_name)["values"]
        valid_keys = self.get_valid_config_values(document, word_after_key, config_completer)
        descriptions = self.get_completer_descriptions(config_completer)
        for key in valid_keys:
            display_meta = self.get_display_meta(descriptions, key)
            yield Completion(key, start_position=-len(word_after_key), display_meta=display_meta)

    def yield_clusters(self, word_before_cursor):
        clusters = self.settings.user_config["clusters"].keys()
        valid_keys = self.fuzzy(word_before_cursor, clusters)
        for key in valid_keys:
            yield Completion(u"{0}".format(key), start_position=-len(word_before_cursor), display_meta=None)

    # descriptions
    def get_display_meta(self, descriptions, key):
        return descriptions.get(key, "") if self.settings.enable_help else None

    def get_command_descriptions(self):
        return dict((x, self.commands[x]["description"]) for x in self.commands.keys())

    def get_option_descriptions(self, command):
        options_list = self.commands[command]["options"].keys()
        return dict((x, self.commands[command]["options"][x]["description"]) for x in options_list)

    @staticmethod
    def get_completer_descriptions(completer):
        return dict((x, completer[x]["description"]) for x in completer.keys())

    # helpers
    def get_valid_options(self, document, word_before_cursor):
        split_string = document.text.split(" ")
        command = split_string[0]
        try:
            valid_keys = self.fuzzy(word_before_cursor, self.commands[command]["options"].keys())
            modified_command_list = exclude_options_from_removal(split_string)
            return [elem for elem in valid_keys if elem not in modified_command_list]
        except KeyError:
            return []

    def get_valid_option_values(self, document, word_before_cursor, option_values, completer_name):
        split_string = document.text.split(" ")
        updated_keys = self.exclude_option_value_keys(document, option_values, completer_name)
        valid_keys = self.fuzzy(word_before_cursor, updated_keys)
        return [elem for elem in valid_keys if elem not in split_string]

    def get_valid_config_values(self, document, word_after_key, config_completer):
        split_string = document.text.split(" ")
        valid_keys = self.fuzzy(word_after_key, config_completer.keys())
        return [elem for elem in valid_keys if elem not in split_string]

    def exclude_option_value_keys(self, document, option_values, completer_name):
        if completer_name == "kafka-configs":
            if document.text.split(" ", 1)[0] == "kafka-topics":
                return self.handle_kafka_topics_configs(option_values)
            return self.handle_kafka_configs_completer(document, option_values)
        return option_values.keys()

    @staticmethod
    def handle_kafka_configs_completer(document, option_values):
        for entity_type in ["broker", "topic", "user", "client"]:
            if "--entity-type {0}".format(entity_type) in document.text:
                return [i for i in option_values.keys() if "{0}s".format(entity_type) in option_values[i]["types"]]
        return option_values.keys()

    @staticmethod
    def handle_kafka_topics_configs(option_values):
        return [i for i in option_values.keys() if "topics" in option_values[i]["types"]]

    def get_completer_name_for_option(self, command, option):
        try:
            return self.commands[command]["options"][option]["completer"]
        except KeyError:
            return None

    @staticmethod
    def get_completer_name_for_config(config_completer, config):
        try:
            return config_completer[config]["completer"]
        except KeyError:
            return None

    def fuzzy(self, word_before_cursor, completion_list):
        if self.settings.enable_fuzzy_search:
            return fuzzyfinder(word_before_cursor, completion_list)
        else:
            return [elem for elem in completion_list if elem.startswith(word_before_cursor)]

    @staticmethod
    def has_option_value_completer(value_completer_name):
        return value_completer_name is not None

    @staticmethod
    def is_config_value(value):
        return "=" in value

    @staticmethod
    def is_cluster_command(text):
        split_text = text.split(" ")
        return split_text[0].strip() in ["cluster-select", "cluster-describe"] and len(split_text) <= 2

    @staticmethod
    def is_not_command(text):
        return len(text.split(" ", 1)) > 1
