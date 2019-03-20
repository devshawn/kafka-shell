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

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory, InMemoryHistory, ThreadedHistory

from kafkashell.bindings import get_bindings
from kafkashell.completer import KafkaCompleter
from kafkashell.config import get_user_history_path
from kafkashell.executor import Executor
from kafkashell.settings import Settings
from kafkashell.style import style
from kafkashell.toolbar import Toolbar


def main():
    settings = Settings()
    bindings = get_bindings(settings)
    executor = Executor(settings)
    toolbar = Toolbar(settings)
    completer = KafkaCompleter(settings) if settings.enable_auto_complete else None
    suggester = AutoSuggestFromHistory() if settings.enable_auto_suggest else None
    history = ThreadedHistory(FileHistory(get_user_history_path())) if settings.enable_history else InMemoryHistory()
    session = PromptSession(completer=completer, style=style, bottom_toolbar=toolbar.handler,
                            key_bindings=bindings, history=history, include_default_pygments_style=False)
    while True:
        try:
            command = session.prompt([("class:operator", "> ")], auto_suggest=suggester)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            executor.execute(command)

    settings.save_settings()


if __name__ == "__main__":
    main()
