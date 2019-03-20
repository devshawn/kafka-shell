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


class Toolbar(object):

    def __init__(self, settings):
        self.handler = self._create_handler(settings)

    @staticmethod
    def _create_handler(settings):
        def get_toolbar_items():
            help_text = "ON" if settings.enable_help else "OFF"
            fuzzy_text = "ON" if settings.enable_fuzzy_search else "OFF"
            return [
                ("class:bottom-toolbar", " [F2] Cluster: "),
                ("class:bottom-toolbar-yellow", settings.cluster),
                ("class:bottom-toolbar", " "),
                ("class:bottom-toolbar", "[F3] Fuzzy: "),
                ("class:bottom-toolbar-yellow", fuzzy_text),
                ("class:bottom-toolbar", " "),
                ("class:bottom-toolbar", "[F9] In-Line Help: "),
                ("class:bottom-toolbar-yellow", help_text),
                ("class:bottom-toolbar", " "),
                ("class:bottom-toolbar", "[F10] Exit")
            ]

        return get_toolbar_items
