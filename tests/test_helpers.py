from __future__ import unicode_literals

import sys

import mock
import pytest

from .context import kafkashell

patch_name = "__builtin__.print" if sys.version_info[0] < 3 else "builtins.print"

exclude_options_test_data = [
    (["kafka-topics", "--property"], ["kafka-topics"]),
    (["kafka-topics", "--test"], ["kafka-topics", "--test"]),
    (["kafka-topics", "--config", "--property"], ["kafka-topics"]),
    (["kafka-topics", "--config", "--property", "--test", "--add-config"], ["kafka-topics", "--test"]),
    (["--property", "kafka-topics"], ["kafka-topics"]),
]

print_cluster_config_test_data = [
    ({"test": "test"}, "test: test\n"),
    ({"a": "a"}, "a: a\n"),
]


def test_options_that_can_be_duplicated():
    actual = kafkashell.helpers.options_that_can_be_duplicated
    expected = [
        "--add-config",
        "--config",
        "--consumer-property",
        "--delete-config",
        "--producer-property",
        "--property",
        "--principal"
    ]
    assert actual == expected


@pytest.mark.parametrize("test_input,expected", exclude_options_test_data)
def test_exclude_options_from_removal(test_input, expected):
    actual = kafkashell.helpers.exclude_options_from_removal(test_input)
    assert actual == expected


@mock.patch(patch_name, create=True)
@pytest.mark.parametrize("test_input,expected", print_cluster_config_test_data)
def test_print_cluster_config(mock_print, test_input, expected):
    kafkashell.helpers.print_cluster_config(test_input)
    mock_print.assert_called_once_with(expected)
