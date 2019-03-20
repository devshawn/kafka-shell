from __future__ import unicode_literals

import mock
import pytest
from prompt_toolkit.document import Document

from tests.context import kafkashell
from tests.test_completer_data import command_test_data, option_test_data, option_value_test_data
from tests.utilities import setup_settings_for_test, setup_settings_with_real_completer_for_test

fuzzy_test_data = [
    ("kf", ["kafka"], ["kafka"], True),
    ("kaf", ["kafka"], ["kafka"], True),
    ("kf", ["kafka"], [], False),
    ("kaf", ["kafka"], ["kafka"], False),
]


def get_completions(completer, command):
    position = len(command)
    result = list(completer.get_completions(Document(text=command, cursor_position=position), None))
    return result


def verify_completions(completions, expected):
    actual = []
    for completion in completions:
        actual.append(completion.text)
    print("[\"" + "\",\"".join(actual) + "\"]")
    actual.sort()
    expected.sort()
    assert actual == expected


@mock.patch("kafkashell.settings.Settings")
@pytest.mark.parametrize("test_input,expected", command_test_data)
def test_get_completions_for_commands(mock_settings, test_input, expected):
    settings = setup_settings_with_real_completer_for_test(mock_settings)
    completer = kafkashell.completer.KafkaCompleter(settings)
    completions = get_completions(completer, test_input)
    verify_completions(completions, expected)


@mock.patch("kafkashell.settings.Settings")
@pytest.mark.parametrize("test_input,expected", option_test_data)
def test_get_completions_for_options(mock_settings, test_input, expected):
    settings = setup_settings_with_real_completer_for_test(mock_settings)
    completer = kafkashell.completer.KafkaCompleter(settings)
    completions = get_completions(completer, test_input)
    verify_completions(completions, expected)


@mock.patch("kafkashell.settings.Settings")
@pytest.mark.parametrize("test_input,expected", option_value_test_data)
def test_get_completions_for_option_values(mock_settings, test_input, expected):
    settings = setup_settings_with_real_completer_for_test(mock_settings)
    completer = kafkashell.completer.KafkaCompleter(settings)
    completions = get_completions(completer, test_input)
    verify_completions(completions, expected)


@mock.patch("kafkashell.settings.Settings")
def test_get_command_descriptions(mock_settings):
    settings = setup_settings_for_test(mock_settings)

    completer = kafkashell.completer.KafkaCompleter(settings)

    assert completer.get_command_descriptions() == {
        "clear": "Clear the screen",
        "kafka-topics": "Manage topics within a cluster."
    }


@mock.patch("kafkashell.settings.Settings")
def test_get_option_descriptions(mock_settings):
    settings = setup_settings_for_test(mock_settings)

    completer = kafkashell.completer.KafkaCompleter(settings)

    assert completer.get_option_descriptions("kafka-topics") == {
        "--alter": "Alter the number of partitions, replica assignment, and/or configuration for a topic.",
        "--config": "A topic configuration override for the topic being created or altered."
    }


@mock.patch("kafkashell.settings.Settings")
@pytest.mark.parametrize("wbc,commands,expected,enabled", fuzzy_test_data)
def test_fuzzy_enabled(mock_settings, wbc, commands, expected, enabled):
    settings = setup_settings_for_test(mock_settings)
    settings.enable_fuzzy_search = enabled

    completer = kafkashell.completer.KafkaCompleter(settings)

    assert list(completer.fuzzy(wbc, commands)) == expected


@mock.patch("kafkashell.settings.Settings")
@pytest.mark.parametrize("test_input,expected", [({}, True), (None, False), ("", True)])
def test_has_option_value_completer(mock_settings, test_input, expected):
    settings = setup_settings_for_test(mock_settings)
    completer = kafkashell.completer.KafkaCompleter(settings)
    assert completer.has_option_value_completer(test_input) == expected


@mock.patch("kafkashell.settings.Settings")
@pytest.mark.parametrize("test_input,expected",
                         [("kafka-topics ", True), ("kafka-topics --list", True), ("kafka-topics", False), ("", False)]
                         )
def test_is_not_command(mock_settings, test_input, expected):
    settings = setup_settings_for_test(mock_settings)
    completer = kafkashell.completer.KafkaCompleter(settings)
    assert completer.is_not_command(test_input) == expected
