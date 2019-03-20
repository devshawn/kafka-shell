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

from prompt_toolkit.styles import Style

style = Style.from_dict({
    "operator": "#2196f3",
    "completion-menu.completion": "bg:#1769aa #ffffff",
    "completion-menu.completion.current": "bg:#2196f3 #000000",
    "completion-menu.meta.completion": "bg:#2196f3 #ffffff",
    "completion-menu.meta.completion.current": "bg:#4dabf5 #000000",
    "scrollbar.background": "bg:#1769aa",
    "scrollbar.button": "bg:#003333",
    "bottom-toolbar": "bg:#ffffff #1769aa",
    "bottom-toolbar-yellow": "bg:#ffff10 #1769aa",
})
