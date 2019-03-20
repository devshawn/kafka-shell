from __future__ import unicode_literals

import json
import os

import oyaml as yaml
import pytest
from jsonschema import validate, ValidationError


def setup_settings_for_test(mock_settings):
    with open("tests/data/test-completer.json") as f:
        settings = mock_settings.return_value
        settings.selected_cluster = "local"
        settings.enable_help = True
        settings.enable_fuzzy_search = True
        settings.commands = json.load(f)["commands"]
        return settings


def setup_settings_with_real_completer_for_test(mock_settings):
    with open("kafkashell/data/completer.json") as f:
        with open("kafkashell/data/shell-config.yaml") as fc:
            settings = mock_settings.return_value
            settings.selected_cluster = "local"
            settings.enable_help = True
            settings.enable_fuzzy_search = True
            settings.user_config = yaml.safe_load(fc)
            settings.commands = json.load(f)["commands"]
            return settings


def setup_config_path_for_test(config_name="test"):
    data_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.realpath(os.path.join(data_dir, "../tests/data/{0}-config.yaml".format(config_name)))


def get_schema(schema_name):
    data_dir = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.realpath(os.path.join(data_dir, "../kafkashell/data/{0}.schema".format(schema_name)))
    with open(data_path) as f:
        return json.load(f)


def get_test_config(config_name="test"):
    data_dir = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.realpath(os.path.join(data_dir, "../tests/data/{0}-config.yaml".format(config_name)))
    with open(data_path) as f:
        return yaml.safe_load(f)


def validate_schema(actual, schema_name, message):
    schema = get_schema(schema_name)
    assert actual is not None
    try:
        validate(instance=actual, schema=schema)
    except ValidationError as ex:
        pytest.fail(make_schema_error_message(ex, message))


def validate_invalid_schema(actual, schema_name):
    schema = get_schema(schema_name)
    assert actual is not None
    try:
        validate(instance=actual, schema=schema)
    except ValidationError as ex:
        return make_schema_error_message(ex)


def make_schema_error_message(ex, message="Schema"):
    error_type = ", ".join(ex.path) if len(ex.path) > 0 else "root"
    return "{0} does not conform to schema ({1}): {2}".format(message, error_type, ex.message)
