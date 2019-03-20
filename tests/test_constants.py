from .context import kafkashell


def test_constants():
    assert kafkashell.constants.COMMAND_KAFKA_TOPICS == "kafka-topics"
    assert kafkashell.constants.COMMAND_KAFKA_CONFIGS == "kafka-configs"
    assert kafkashell.constants.COMMAND_KAFKA_CONSOLE_CONSUMER == "kafka-console-consumer"
    assert kafkashell.constants.COMMAND_KAFKA_CONSOLE_PRODUCER == "kafka-console-producer"
    assert kafkashell.constants.COMMAND_KAFKA_AVRO_CONSOLE_CONSUMER == "kafka-avro-console-consumer"
    assert kafkashell.constants.COMMAND_KAFKA_AVRO_CONSOLE_PRODUCER == "kafka-avro-console-producer"
    assert kafkashell.constants.COMMAND_KAFKA_VERIFIABLE_CONSUMER == "kafka-verifiable-consumer"
    assert kafkashell.constants.COMMAND_KAFKA_VERIFIABLE_PRODUCER == "kafka-verifiable-producer"
    assert kafkashell.constants.COMMAND_KAFKA_BROKER_API_VERSIONS == "kafka-broker-api-versions"
    assert kafkashell.constants.COMMAND_KAFKA_DELETE_RECORDS == "kafka-delete-records"
    assert kafkashell.constants.COMMAND_KAFKA_LOG_DIRS == "kafka-log-dirs"
    assert kafkashell.constants.COMMAND_KAFKA_ACLS == "kafka-acls"
    assert kafkashell.constants.COMMAND_KSQL == "ksql"
    assert kafkashell.constants.COMMAND_ZOOKEEPER_SHELL == "zookeeper-shell"
    assert kafkashell.constants.FLAG_ZOOKEEPER == "--zookeeper"
    assert kafkashell.constants.FLAG_BOOTSTRAP_SERVER == "--bootstrap-server"
    assert kafkashell.constants.FLAG_BROKER_LIST == "--broker-list"
    assert kafkashell.constants.FLAG_SCHEMA_REGISTRY_URL == "--property schema.registry.url"
