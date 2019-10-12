from __future__ import unicode_literals

from tests.context import kafkashell
from tests.utilities import validate_schema, get_test_config, validate_invalid_schema


def test_completer_commands():
    json_value = kafkashell.config.get_completer()
    validate_schema(json_value, "completer", "Commands (completer.json)")


def test_completer_kafka_configs():
    json_value = kafkashell.config.get_completer("kafka-configs")
    validate_schema(json_value, "completer-kafka-configs", "Kafka configs (completer-kafka-configs.json)")


def test_completer_reset_policies():
    json_value = kafkashell.config.get_completer("reset-policies")
    validate_schema(json_value, "completer-reset-policies", "Reset Policies (completer-reset-policies.json)")


def test_completer_resource_pattern_type():
    json_value = kafkashell.config.get_completer("resource-pattern-types")
    validate_schema(json_value, "completer-resource-pattern-types",
                    "Resource Pattern Types (completer-resource-pattern-types.json)")


def test_completer_acks():
    json_value = kafkashell.config.get_completer("acks")
    validate_schema(json_value, "completer-acks", "Acks (completer-acks.json)")


def test_completer_compression_codecs():
    json_value = kafkashell.config.get_completer("compression-codecs")
    validate_schema(json_value, "completer-compression-codecs",
                    "Compression Codecs (completer-compression-codecs.json)")


def test_completer_entity_types():
    json_value = kafkashell.config.get_completer("entity-types")
    validate_schema(json_value, "completer-entity-types", "Entity Types (completer-entity-types.json)")


def test_completer_ksql_output():
    json_value = kafkashell.config.get_completer("ksql-output")
    validate_schema(json_value, "completer-ksql-output", "KSQL Output (completer-ksql-output.json)")


def test_completer_cleanup_policy():
    json_value = kafkashell.config.get_completer("cleanup-policy")
    validate_schema(json_value, "completer-cleanup-policy", "Cleanup Policy (completer-cleanup-policy.json)")


def test_completer_booleans():
    json_value = kafkashell.config.get_completer("booleans")
    validate_schema(json_value, "completer-booleans", "Booleans (completer-booleans.json)")


def test_completer_timestamp_types():
    json_value = kafkashell.config.get_completer("timestamp-types")
    validate_schema(json_value, "completer-timestamp-types", "Timestamp Types (completer-timestamp-types.json)")


def test_default_config_schema():
    json_value = kafkashell.config.get_default_config()
    validate_schema(json_value, "shell-config", "Default user config")


def test_environment_variable_config_schema():
    json_value = get_test_config("test-environment-variables")
    validate_schema(json_value, "shell-config", "Environment variable user config")


def test_invalid_configs():
    json_value = get_test_config("test-invalid-ksql")
    message = validate_invalid_schema(json_value, "shell-config")
    assert message is not None

    json_value = get_test_config("test-invalid-schema-registry")
    message = validate_invalid_schema(json_value, "shell-config")
    assert message is not None
