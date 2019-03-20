import json
import os
import sys

import mock
import pytest

from tests.context import kafkashell

open_patch_name = "__builtin__.open" if sys.version_info[0] < 3 else "builtins.open"
print_patch_name = "__builtin__.print" if sys.version_info[0] < 3 else "builtins.print"

test_config_data = [
    ("{}", {}),
    ("{\"test\": \"testing\"}", {"test": "testing"})
]

test_completer_data = [
    ("completer", "{}", {}),
    ("kafka-configs", "{\"test\": \"testing\"}", {"test": "testing"})
]


@mock.patch(open_patch_name, create=True)
@mock.patch("os.makedirs")
@mock.patch("os.path.exists")
@mock.patch("os.path.isfile")
@mock.patch("os.path.expanduser")
def test_init_config_file_exists(mock_expanduser, mock_isfile, mock_exists, mock_makedirs, mock_open):
    mock_config_file = "/tmp/.kafka-shell/config.yaml"
    mock_dir = "/tmp/.kafka-shell"
    mock_expanduser.side_effect = [mock_dir, mock_config_file]
    mock_isfile.return_value = True
    mock_exists.return_value = True

    kafkashell.config.init_config()

    mock_exists.assert_called_once_with(mock_dir)
    mock_makedirs.assert_not_called()
    mock_isfile.assert_called_once_with(mock_config_file)
    mock_open.assert_not_called()


@mock.patch("os.makedirs")
@mock.patch("os.path.exists")
@mock.patch("os.path.isfile")
@mock.patch("os.path.expanduser")
@mock.patch("oyaml.dump")
def test_init_config_dir_exists_but_file_does_not_exist(mock_dump, mock_expanduser, mock_isfile, mock_exists,
                                                        mock_makedirs):
    with mock.patch(open_patch_name, mock.mock_open(read_data="{}")) as mock_open:
        mock_dir = "/tmp/.kafka-shell"
        mock_config_file = "/tmp/.kafka-shell/config.yaml"
        mock_expanduser.side_effect = [mock_dir, mock_config_file]
        mock_isfile.return_value = False
        mock_exists.return_value = True
        data_dir = os.path.dirname(os.path.realpath(__file__))
        expected_path = os.path.realpath(os.path.join(data_dir, "../kafkashell/data/shell-config.yaml"))

        kafkashell.config.init_config()

        mock_exists.assert_called_once_with(mock_dir)
        mock_makedirs.assert_not_called()
        mock_isfile.assert_called_once_with(mock_config_file)
        mock_open.assert_any_call(mock_config_file, "w")
        mock_open.assert_any_call(expected_path)
        mock_dump.assert_called_once_with({}, mock_open.return_value, default_flow_style=False, sort_keys=False)


@mock.patch("os.makedirs")
@mock.patch("os.path.exists")
@mock.patch("os.path.isfile")
@mock.patch("os.path.expanduser")
@mock.patch("oyaml.dump")
def test_init_config_dir_and_file_does_not_exist(mock_dump, mock_expanduser, mock_isfile, mock_exists,
                                                 mock_makedirs):
    with mock.patch(open_patch_name, mock.mock_open(read_data="{}")) as mock_open:
        mock_dir = "/tmp/.kafka-shell"
        mock_config_file = "/tmp/.kafka-shell/config.yaml"
        mock_expanduser.side_effect = [mock_dir, mock_config_file]
        mock_isfile.return_value = False
        mock_exists.return_value = False
        data_dir = os.path.dirname(os.path.realpath(__file__))
        expected_path = os.path.realpath(os.path.join(data_dir, "../kafkashell/data/shell-config.yaml"))

        kafkashell.config.init_config()

        mock_exists.assert_called_once_with(mock_dir)
        mock_makedirs.assert_called_once_with(mock_dir)
        mock_isfile.assert_called_once_with(mock_config_file)
        mock_open.assert_any_call(mock_config_file, "w")
        mock_open.assert_any_call(expected_path)
        mock_dump.assert_called_once_with({}, mock_open.return_value, default_flow_style=False, sort_keys=False)


@mock.patch(open_patch_name, create=True)
@mock.patch("os.path.isfile")
@mock.patch("os.path.expanduser")
def test_init_history_file_exits(mock_expanduser, mock_isfile, mock_open):
    mock_history_file = "/tmp/.kafka-shell-history"
    mock_expanduser.return_value = mock_history_file
    mock_isfile.return_value = True

    kafkashell.config.init_history()

    mock_isfile.assert_called_once_with(mock_history_file)
    assert not mock_open.called


@mock.patch("os.path.isfile")
@mock.patch("os.path.expanduser")
def test_init_history_file_does_not_exist(mock_expanduser, mock_isfile):
    with mock.patch(open_patch_name, mock.mock_open(read_data="{}")) as mock_open:
        mock_history_file = "/tmp/.kafka-shell-history"
        mock_expanduser.return_value = mock_history_file
        mock_isfile.return_value = False

        kafkashell.config.init_history()

        mock_isfile.assert_called_once_with(mock_history_file)
        mock_open.assert_any_call(mock_history_file, "a")


@mock.patch("os.path.expanduser")
@pytest.mark.parametrize("test_input,expected", test_config_data)
def test_get_config(mock_expanduser, test_input, expected):
    with mock.patch(open_patch_name, mock.mock_open(read_data=test_input)) as mock_open:
        mock_config_file = "/tmp/.kafka-shell"
        mock_expanduser.return_value = mock_config_file

        config = kafkashell.config.get_config()

        assert config == expected
        mock_open.assert_called_once_with(mock_config_file)


@mock.patch(print_patch_name)
@mock.patch("sys.exit")
@pytest.mark.parametrize("test_input,expected", test_config_data)
def test_validate_config_invalid(mock_exit, mock_print, test_input, expected):
    with open("tests/data/test-config.yaml") as f:
        config = json.load(f)
        returned_config = kafkashell.config.validate_config(config)

        assert config == returned_config
        assert not mock_print.called
        assert not mock_exit.called


@mock.patch(print_patch_name)
@mock.patch("sys.exit")
@pytest.mark.parametrize("test_input,expected", test_config_data)
def test_validate_config_invalid(mock_exit, mock_print, test_input, expected):
    config = {}
    kafkashell.config.validate_config(config)

    error_type = "root"
    error_message = "'version' is a required property"
    compatible_error_message = "u{0}".format(error_message) if sys.version_info[0] < 3 else error_message
    final_error_message = "Invalid user configuration ({0}): {1}".format(error_type, compatible_error_message)

    mock_print.assert_called_once_with(final_error_message)
    mock_exit.assert_called_once_with(1)


@mock.patch("oyaml.dump")
@mock.patch("os.path.expanduser")
@pytest.mark.parametrize("test_input,expected", test_config_data)
def test_save_config(mock_expanduser, mock_dump, test_input, expected):
    with mock.patch(open_patch_name, mock.mock_open(read_data=test_input)) as mock_open:
        mock_config_file = "/tmp/.kafka-shell"
        mock_expanduser.return_value = mock_config_file

        kafkashell.config.save_config(expected)

        mock_open.assert_called_once_with(mock_config_file, "w")
        mock_dump.assert_called_once_with(expected, mock_open.return_value, default_flow_style=False, sort_keys=False)


@pytest.mark.parametrize("test_input,expected", test_config_data)
def test_get_default_config(test_input, expected):
    with mock.patch(open_patch_name, mock.mock_open(read_data=test_input)) as mock_open:
        data_dir = os.path.dirname(os.path.realpath(__file__))
        expected_path = os.path.realpath(os.path.join(data_dir, "../kafkashell/data/shell-config.yaml"))

        assert kafkashell.config.get_default_config() == expected
        mock_open.assert_called_once_with(expected_path)


@pytest.mark.parametrize("test_input,expected", test_config_data)
def test_get_config_schema(test_input, expected):
    with mock.patch(open_patch_name, mock.mock_open(read_data=test_input)) as mock_open:
        data_dir = os.path.dirname(os.path.realpath(__file__))
        expected_path = os.path.realpath(os.path.join(data_dir, "../kafkashell/data/shell-config.schema"))

        assert kafkashell.config.get_config_schema() == expected
        mock_open.assert_called_once_with(expected_path)


@pytest.mark.parametrize("name,test_input,expected", test_completer_data)
def test_get_completer(name, test_input, expected):
    with mock.patch(open_patch_name, mock.mock_open(read_data=test_input)) as mock_open:
        data_dir = os.path.dirname(os.path.realpath(__file__))
        expected_name = name if name == "completer" or name is None else "completer-{0}".format(name)
        expected_path = os.path.realpath(os.path.join(data_dir, "../kafkashell/data/{0}.json".format(expected_name)))

        assert kafkashell.config.get_completer(name) == expected
        mock_open.assert_called_once_with(expected_path)


def test_get_kafka_shell_dir():
    assert kafkashell.config.get_kafka_shell_dir() == os.path.expanduser("~/.kafka-shell")


def test_get_user_config_path():
    assert kafkashell.config.get_user_config_path() == os.path.expanduser("~/.kafka-shell/config.yaml")


def test_get_user_history_path():
    assert kafkashell.config.get_user_history_path() == os.path.expanduser("~/.kafka-shell/history")
