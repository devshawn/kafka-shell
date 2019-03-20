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

import copy

from kafkashell import config
from kafkashell.helpers import cycle


class Settings:

    def __init__(self):
        config.init_config()
        self.user_config = config.validate_config(config.get_config())
        self.commands = config.get_completer()["commands"]
        self.enable = self.user_config["enable"]
        self.enable_history = self.user_config["enable"]["history"]
        self.enable_save_on_exit = self.user_config["enable"]["save_on_exit"]
        self.enable_auto_complete = self.user_config["enable"]["auto_complete"]
        self.enable_auto_suggest = self.user_config["enable"]["auto_suggest"]
        self.enable_help = self.user_config["enable"]["inline_help"]
        self.enable_fuzzy_search = self.user_config["enable"]["fuzzy_search"]
        self.cluster = self.user_config["cluster"]
        self.cluster_iterator = cycle(list(self.user_config["clusters"].keys()), self.cluster)
        self.init_history()

    def set_enable_help(self, value):
        self.enable_help = value

    def set_enable_fuzzy_search(self, value):
        self.enable_fuzzy_search = value

    def set_next_cluster(self):
        self.cluster = next(self.cluster_iterator)

    def get_cluster_details(self):
        return self.user_config["clusters"][self.cluster]

    def init_history(self):
        if self.enable_history:
            config.init_history()

    def save_settings(self):
        if self.enable_save_on_exit:
            settings = copy.deepcopy(self.user_config)
            settings["enable"]["inline_help"] = self.enable_help
            settings["enable"]["fuzzy_search"] = self.enable_fuzzy_search
            settings["cluster"] = self.cluster
            config.save_config(settings)
