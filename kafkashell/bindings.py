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

from prompt_toolkit.application import current
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys


def get_bindings(settings):
    bindings = KeyBindings()

    @bindings.add(Keys.F2)
    def _(event):
        settings.set_next_cluster()

    @bindings.add(Keys.F3)
    def _(event):
        settings.set_enable_fuzzy_search(not settings.enable_fuzzy_search)

    @bindings.add(Keys.F9)
    def _(event):
        settings.set_enable_help(not settings.enable_help)

    @bindings.add(Keys.F10)
    def _(event):
        current.get_app().exit(exception=EOFError)

    return bindings
