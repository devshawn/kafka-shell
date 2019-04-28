import sys

import mock
import pytest

from tests.utilities import setup_config_path_for_test
from .context import kafkashell

patch_name = "__builtin__.print" if sys.version_info[0] < 3 else "builtins.print"

test_data = [
    ("kafka", "kafka"),
    ("kafka-topics", "kafka-topics --zookeeper localhost:2181"),
    ("  kafka-topics     ", "kafka-topics --zookeeper localhost:2181"),
    ("kafka-topics --zookeeper test:2181", "kafka-topics --zookeeper test:2181"),
    ("kafka-topics --create --topic name", "kafka-topics --create --topic name --zookeeper localhost:2181"),
    ("kafka-configs", "kafka-configs --zookeeper localhost:2181"),
    ("kafka-configs --zookeeper test:2181", "kafka-configs --zookeeper test:2181"),
    ("kafka-configs --alter", "kafka-configs --alter --zookeeper localhost:2181"),
    ("kafka-console-consumer", "kafka-console-consumer --bootstrap-server localhost:9092"),
    (
        "kafka-console-consumer --from-beginning",
        "kafka-console-consumer --from-beginning --bootstrap-server localhost:9092"
    ),
    ("kafka-console-consumer --bootstrap-server test:9092", "kafka-console-consumer --bootstrap-server test:9092"),
    ("kafka-console-producer", "kafka-console-producer --broker-list localhost:9092"),
    ("kafka-console-producer --broker-list test:9092", "kafka-console-producer --broker-list test:9092"),
    (
        "kafka-avro-console-consumer",
        "kafka-avro-console-consumer --bootstrap-server localhost:9092 --property schema.registry.url=http://localhost:8081"
    ),
    (
        "kafka-avro-console-consumer --from-beginning",
        "kafka-avro-console-consumer --from-beginning --bootstrap-server localhost:9092 --property schema.registry.url=http://localhost:8081"
    ),
    (
        "kafka-avro-console-consumer --from-beginning --bootstrap-server test:9092",
        "kafka-avro-console-consumer --from-beginning --bootstrap-server test:9092 --property schema.registry.url=http://localhost:8081"
    ),
    (
        "kafka-avro-console-consumer --from-beginning --bootstrap-server test:9092 --property schema.registry.url=test:8081",
        "kafka-avro-console-consumer --from-beginning --bootstrap-server test:9092 --property schema.registry.url=test:8081"
    ),
    (
        "kafka-avro-console-consumer --property schema.registry.url=test:8081",
        "kafka-avro-console-consumer --property schema.registry.url=test:8081 --bootstrap-server localhost:9092"
    ),
    (
        "kafka-avro-console-producer",
        "kafka-avro-console-producer --broker-list localhost:9092 --property schema.registry.url=http://localhost:8081"
    ),
    (
        "kafka-avro-console-producer --from-beginning",
        "kafka-avro-console-producer --from-beginning --broker-list localhost:9092 --property schema.registry.url=http://localhost:8081"
    ),
    (
        "kafka-avro-console-producer --from-beginning --broker-list test:9092",
        "kafka-avro-console-producer --from-beginning --broker-list test:9092 --property schema.registry.url=http://localhost:8081"
    ),
    (
        "kafka-avro-console-producer --from-beginning --broker-list test:9092 --property schema.registry.url=test:8081",
        "kafka-avro-console-producer --from-beginning --broker-list test:9092 --property schema.registry.url=test:8081"
    ),
    (
        "kafka-avro-console-producer --property schema.registry.url=test:8081",
        "kafka-avro-console-producer --property schema.registry.url=test:8081 --broker-list localhost:9092"
    ),
    (
        "kafka-verifiable-consumer",
        "kafka-verifiable-consumer --broker-list localhost:9092"
    ),
    (
        "kafka-verifiable-consumer --broker-list test:9092",
        "kafka-verifiable-consumer --broker-list test:9092"
    ),
    (
        "kafka-verifiable-consumer --topic mytopic --broker-list test:9092",
        "kafka-verifiable-consumer --topic mytopic --broker-list test:9092"
    ),
    (
        "kafka-verifiable-consumer --topic mytopic",
        "kafka-verifiable-consumer --topic mytopic --broker-list localhost:9092"
    ),
    (
        "kafka-verifiable-producer",
        "kafka-verifiable-producer --broker-list localhost:9092"
    ),
    (
        "kafka-verifiable-producer --broker-list test:9092",
        "kafka-verifiable-producer --broker-list test:9092"
    ),
    (
        "kafka-verifiable-producer --topic mytopic",
        "kafka-verifiable-producer --topic mytopic --broker-list localhost:9092"
    ),
    (
        "kafka-verifiable-producer --topic mytopic --broker-list test:9092",
        "kafka-verifiable-producer --topic mytopic --broker-list test:9092"
    ),
    (
        "kafka-consumer-groups",
        "kafka-consumer-groups --bootstrap-server localhost:9092"
    ),
    (
        "kafka-consumer-groups --list",
        "kafka-consumer-groups --list --bootstrap-server localhost:9092"
    ),
    (
        "kafka-consumer-groups --to-offset 10 --list",
        "kafka-consumer-groups --to-offset 10 --list --bootstrap-server localhost:9092"
    ),
    (
        "kafka-consumer-groups --list --bootstrap-server test:9092",
        "kafka-consumer-groups --list --bootstrap-server test:9092"
    ),
    (
        "kafka-broker-api-versions",
        "kafka-broker-api-versions --bootstrap-server localhost:9092"
    ),
    (
        "kafka-broker-api-versions --bootstrap-server broker1:9092",
        "kafka-broker-api-versions --bootstrap-server broker1:9092"
    ),
    (
        "kafka-broker-api-versions --command-config admin.properties",
        "kafka-broker-api-versions --command-config admin.properties --bootstrap-server localhost:9092"
    ),
    (
        "kafka-broker-api-versions --bootstrap-server broker2:9092 --command-config admin.properties",
        "kafka-broker-api-versions --bootstrap-server broker2:9092 --command-config admin.properties"
    ),
    (
        "kafka-delete-records",
        "kafka-delete-records --bootstrap-server localhost:9092"
    ),
    (
        "kafka-delete-records --bootstrap-server broker1:9092",
        "kafka-delete-records --bootstrap-server broker1:9092"
    ),
    (
        "kafka-delete-records --offset-json-file offsets.json",
        "kafka-delete-records --offset-json-file offsets.json --bootstrap-server localhost:9092"
    ),
    (
        "kafka-delete-records --offset-json-file offsets.json --bootstrap-server broker1:9092",
        "kafka-delete-records --offset-json-file offsets.json --bootstrap-server broker1:9092"
    ),
    (
        "kafka-log-dirs",
        "kafka-log-dirs --bootstrap-server localhost:9092"
    ),
    (
        "kafka-log-dirs --bootstrap-server test:9092",
        "kafka-log-dirs --bootstrap-server test:9092"
    ),
    (
        "kafka-log-dirs --broker-list 0,1",
        "kafka-log-dirs --broker-list 0,1 --bootstrap-server localhost:9092"
    ),
    (
        "kafka-dump-log",
        "kafka-dump-log"
    ),
    (
        "kafka-dump-log --files test,test2",
        "kafka-dump-log --files test,test2"
    ),
    (
        "kafka-dump-log --files test,test2 --index-sanity-check",
        "kafka-dump-log --files test,test2 --index-sanity-check"
    ),
    (
        "kafka-acls",
        "kafka-acls --bootstrap-server localhost:9092"
    ),
    (
        "kafka-acls --cluster --command-config admin.properties",
        "kafka-acls --cluster --command-config admin.properties --bootstrap-server localhost:9092"
    ),
    (
        "kafka-acls --cluster --command-config admin.properties --bootstrap-server test:9092",
        "kafka-acls --cluster --command-config admin.properties --bootstrap-server test:9092"
    ),
    (
        "kafka-acls --bootstrap-server my-cluster.cluster.com:9092",
        "kafka-acls --bootstrap-server my-cluster.cluster.com:9092"
    ),
    ("ksql", "ksql -- http://localhost:8088"),
    ("ksql --query-timeout 10000", "ksql --query-timeout 10000 -- http://localhost:8088"),
    ("ksql -- http://test:8088", "ksql -- http://test:8088"),
    ("ksql --query-timeout 10000 -- http://test:8088", "ksql --query-timeout 10000 -- http://test:8088"),
    ("zookeeper-shell", "zookeeper-shell localhost:2181"),
    (" zookeeper-shell    ", "zookeeper-shell localhost:2181"),
    ("zookeeper-shell test:2181", "zookeeper-shell test:2181"),
]

consumer_test_data = [
    (
        "kafka-console-consumer",
        "kafka-console-consumer --bootstrap-server localhost:9092 --consumer.config consumer.properties --property key.separator=, --property print.key=true",
        "test-consumer-settings"
    ),
    (
        "kafka-console-consumer --from-beginning --topic test",
        "kafka-console-consumer --from-beginning --topic test --bootstrap-server localhost:9092 --consumer.config consumer.properties --property key.separator=, --property print.key=true",
        "test-consumer-settings"
    ),
    (
        "kafka-console-consumer --from-beginning --topic test --consumer.config consumer.properties",
        "kafka-console-consumer --from-beginning --topic test --consumer.config consumer.properties --bootstrap-server localhost:9092 --property key.separator=, --property print.key=true",
        "test-consumer-settings"
    ),
    (
        "kafka-console-consumer --from-beginning --topic test --consumer.config reader.properties",
        "kafka-console-consumer --from-beginning --topic test --consumer.config reader.properties --bootstrap-server localhost:9092 --property key.separator=, --property print.key=true",
        "test-consumer-settings"
    ),
    (
        "kafka-avro-console-consumer",
        "kafka-avro-console-consumer --bootstrap-server localhost:9092 --property schema.registry.url=http://localhost:8081 --consumer.config consumer.properties --property key.separator=, --property print.key=true",
        "test-consumer-settings"
    ),
    (
        "kafka-avro-console-consumer --topic test",
        "kafka-avro-console-consumer --topic test --bootstrap-server localhost:9092 --property schema.registry.url=http://localhost:8081 --consumer.config consumer.properties --property key.separator=, --property print.key=true",
        "test-consumer-settings"
    ),
    (
        "kafka-avro-console-consumer --consumer.config reader.properties --topic test",
        "kafka-avro-console-consumer --consumer.config reader.properties --topic test --bootstrap-server localhost:9092 --property schema.registry.url=http://localhost:8081 --property key.separator=, --property print.key=true",
        "test-consumer-settings"
    ),
    (
        "kafka-avro-console-consumer --topic mytopic --from-beginning",
        "kafka-avro-console-consumer --topic mytopic --from-beginning --bootstrap-server localhost:9092 --property schema.registry.url=http://localhost:8081 --consumer.config consumer.properties --property key.separator=, --property print.key=true",
        "test-consumer-settings"
    ),
    (
        "kafka-verifiable-consumer",
        "kafka-verifiable-consumer --broker-list localhost:9092 --consumer.config consumer.properties",
        "test-consumer-settings"
    ),
    (
        "kafka-verifiable-consumer --topic test",
        "kafka-verifiable-consumer --topic test --broker-list localhost:9092 --consumer.config consumer.properties",
        "test-consumer-settings"
    ),
    (
        "kafka-verifiable-consumer --topic test --consumer.config config.properties",
        "kafka-verifiable-consumer --topic test --consumer.config config.properties --broker-list localhost:9092",
        "test-consumer-settings"
    ),
    (
        "kafka-verifiable-consumer --broker-list test:9092",
        "kafka-verifiable-consumer --broker-list test:9092 --consumer.config consumer.properties",
        "test-consumer-settings"
    ),
    (
        "kafka-console-consumer",
        "kafka-console-consumer --bootstrap-server localhost:9092 --consumer.config consumer.properties",
        "test-consumer-settings-without-properties"
    ),
    (
        "kafka-console-consumer --consumer.config reader.properties",
        "kafka-console-consumer --consumer.config reader.properties --bootstrap-server localhost:9092",
        "test-consumer-settings-without-properties"
    ),
    (
        "kafka-avro-console-consumer",
        "kafka-avro-console-consumer --bootstrap-server localhost:9092 --property schema.registry.url=http://localhost:8081 --consumer.config consumer.properties",
        "test-consumer-settings-without-properties"
    )
]

producer_test_data = [
    (
        "kafka-console-producer",
        "kafka-console-producer --broker-list localhost:9092 --producer.config producer.properties --property key.separator=, --property print.key=true",
        "test-producer-settings"
    ),
    (
        "kafka-console-producer --from-beginning --topic test",
        "kafka-console-producer --from-beginning --topic test --broker-list localhost:9092 --producer.config producer.properties --property key.separator=, --property print.key=true",
        "test-producer-settings"
    ),
    (
        "kafka-console-producer --from-beginning --topic test --producer.config writer.properties",
        "kafka-console-producer --from-beginning --topic test --producer.config writer.properties --broker-list localhost:9092 --property key.separator=, --property print.key=true",
        "test-producer-settings"
    ),
    (
        "kafka-avro-console-producer",
        "kafka-avro-console-producer --broker-list localhost:9092 --property schema.registry.url=http://localhost:8081 --producer.config producer.properties --property key.separator=, --property print.key=true",
        "test-producer-settings"
    ),
    (
        "kafka-avro-console-producer --topic test",
        "kafka-avro-console-producer --topic test --broker-list localhost:9092 --property schema.registry.url=http://localhost:8081 --producer.config producer.properties --property key.separator=, --property print.key=true",
        "test-producer-settings"
    ),
    (
        "kafka-avro-console-producer --topic test --producer.config tester.properties",
        "kafka-avro-console-producer --topic test --producer.config tester.properties --broker-list localhost:9092 --property schema.registry.url=http://localhost:8081 --property key.separator=, --property print.key=true",
        "test-producer-settings"
    ),
    (
        "kafka-avro-console-producer --topic mytopic --from-beginning",
        "kafka-avro-console-producer --topic mytopic --from-beginning --broker-list localhost:9092 --property schema.registry.url=http://localhost:8081 --producer.config producer.properties --property key.separator=, --property print.key=true",
        "test-producer-settings"
    ),
    (
        "kafka-verifiable-producer",
        "kafka-verifiable-producer --broker-list localhost:9092 --producer.config producer.properties",
        "test-producer-settings"
    ),
    (
        "kafka-verifiable-producer --topic test",
        "kafka-verifiable-producer --topic test --broker-list localhost:9092 --producer.config producer.properties",
        "test-producer-settings"
    ),
    (
        "kafka-verifiable-producer --topic test --producer.config tester.properties",
        "kafka-verifiable-producer --topic test --producer.config tester.properties --broker-list localhost:9092",
        "test-producer-settings"
    ),
    (
        "kafka-verifiable-producer --broker-list test:9092",
        "kafka-verifiable-producer --broker-list test:9092 --producer.config producer.properties",
        "test-producer-settings"
    ),
    (
        "kafka-console-producer",
        "kafka-console-producer --broker-list localhost:9092 --producer.config producer.properties",
        "test-producer-settings-without-properties"
    ),
    (
        "kafka-console-producer --producer.config prod.properties",
        "kafka-console-producer --producer.config prod.properties --broker-list localhost:9092",
        "test-producer-settings-without-properties"
    ),
    (
        "kafka-avro-console-producer",
        "kafka-avro-console-producer --broker-list localhost:9092 --property schema.registry.url=http://localhost:8081 --producer.config producer.properties",
        "test-producer-settings-without-properties"
    )
]

admin_client_test_data = [
    (
        "kafka-acls",
        "kafka-acls --bootstrap-server localhost:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-acls --bootstrap-server my-cluster.cluster.com:9092",
        "kafka-acls --bootstrap-server my-cluster.cluster.com:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-acls --bootstrap-server my-cluster.cluster.com:9092 --deny-host 127.0.0.1",
        "kafka-acls --bootstrap-server my-cluster.cluster.com:9092 --deny-host 127.0.0.1 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-acls --cluster --command-config admin.properties --bootstrap-server test:9092",
        "kafka-acls --cluster --command-config admin.properties --bootstrap-server test:9092",
        "test-admin-client-settings"
    ),
    (
        "kafka-acls --cluster --bootstrap-server test:9092 --command-config other.properties",
        "kafka-acls --cluster --bootstrap-server test:9092 --command-config other.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-configs",
        "kafka-configs --zookeeper localhost:2181 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-configs --zookeeper test:2181",
        "kafka-configs --zookeeper test:2181 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-configs --zookeeper test:2181 --command-config test.properties",
        "kafka-configs --zookeeper test:2181 --command-config test.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-configs --command-config test.properties",
        "kafka-configs --command-config test.properties --zookeeper localhost:2181",
        "test-admin-client-settings"
    ),
    (
        "kafka-consumer-groups",
        "kafka-consumer-groups --bootstrap-server localhost:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-consumer-groups --list",
        "kafka-consumer-groups --list --bootstrap-server localhost:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-consumer-groups --to-offset 10 --list",
        "kafka-consumer-groups --to-offset 10 --list --bootstrap-server localhost:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-consumer-groups --list --bootstrap-server test:9092",
        "kafka-consumer-groups --list --bootstrap-server test:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-consumer-groups --list --command-config test.properties",
        "kafka-consumer-groups --list --command-config test.properties --bootstrap-server localhost:9092",
        "test-admin-client-settings"
    ),
    (
        "kafka-consumer-groups --list --bootstrap-server test:9092 --command-config test.properties",
        "kafka-consumer-groups --list --bootstrap-server test:9092 --command-config test.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-broker-api-versions",
        "kafka-broker-api-versions --bootstrap-server localhost:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-broker-api-versions --bootstrap-server broker1:9092",
        "kafka-broker-api-versions --bootstrap-server broker1:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-broker-api-versions --bootstrap-server broker2:9092 --command-config test.properties",
        "kafka-broker-api-versions --bootstrap-server broker2:9092 --command-config test.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-broker-api-versions --command-config test.properties",
        "kafka-broker-api-versions --command-config test.properties --bootstrap-server localhost:9092",
        "test-admin-client-settings"
    ),
    (
        "kafka-delete-records",
        "kafka-delete-records --bootstrap-server localhost:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-delete-records --bootstrap-server broker1:9092",
        "kafka-delete-records --bootstrap-server broker1:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-delete-records --offset-json-file offsets.json",
        "kafka-delete-records --offset-json-file offsets.json --bootstrap-server localhost:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-delete-records --offset-json-file offsets.json --bootstrap-server broker1:9092",
        "kafka-delete-records --offset-json-file offsets.json --bootstrap-server broker1:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-delete-records --offset-json-file offsets.json --command-config test.properties --bootstrap-server broker1:9092",
        "kafka-delete-records --offset-json-file offsets.json --command-config test.properties --bootstrap-server broker1:9092",
        "test-admin-client-settings"
    ),
    (
        "kafka-delete-records --offset-json-file offsets.json --command-config test.properties",
        "kafka-delete-records --offset-json-file offsets.json --command-config test.properties --bootstrap-server localhost:9092",
        "test-admin-client-settings"
    ),
    (
        "kafka-log-dirs",
        "kafka-log-dirs --bootstrap-server localhost:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-log-dirs --bootstrap-server test:9092",
        "kafka-log-dirs --bootstrap-server test:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-log-dirs --broker-list 0,1",
        "kafka-log-dirs --broker-list 0,1 --bootstrap-server localhost:9092 --command-config admin.properties",
        "test-admin-client-settings"
    ),
    (
        "kafka-log-dirs --broker-list 0,1 --command-config test.properties",
        "kafka-log-dirs --broker-list 0,1 --command-config test.properties --bootstrap-server localhost:9092",
        "test-admin-client-settings"
    ),
    (
        "kafka-log-dirs --broker-list 0,1 --command-config test.properties --bootstrap-server test:9092",
        "kafka-log-dirs --broker-list 0,1 --command-config test.properties --bootstrap-server test:9092",
        "test-admin-client-settings"
    ),
]

prefix_test_data = [
    ("kafka-topics --list", "docker exec -it container-name kafka-topics --list --zookeeper localhost:2181"),
    ("ksql -- http://host:8088", "docker exec -it container-name ksql -- http://host:8088"),
    ("ksql", "docker exec -it container-name ksql -- http://localhost:8088"),
    ("   ksql   ", "docker exec -it container-name ksql -- http://localhost:8088"),
]

prefix_none_test_data = [
    ("kafka-topics --list", "kafka-topics --list --zookeeper localhost:2181"),
    ("ksql -- http://host:8088", "ksql -- http://host:8088"),
    ("ksql", "ksql -- http://localhost:8088"),
    ("   ksql   ", "ksql -- http://localhost:8088"),
]

command_prefix_test_data = [
    ({}, False),
    ({"command_prefix": ""}, False),
    ({"command_prefix": "docker"}, True),
    ({"command_prefix": " docker"}, True),
    ({"command_prefix": "docker "}, True),
    ({"command_prefix": "  docker "}, True),
]

cluster_describe_test_data = [
    ("cluster-describe", "Please enter a cluster name.", False),
    ("cluster-describe ", "Please enter a cluster name.", False),
    ("cluster-describe a", "Unknown cluster!", False),
    ("cluster-describe this-cluster-does-not-exist", "Unknown cluster!", False),
    ("cluster-describe this-cluster-does-not-exist no-command", "Too many arguments!", False),
    ("cluster-describe this-cluster-does-not-exist no-command again", "Too many arguments!", False),
    ("cluster-describe local", "", True),
    ("cluster-describe test", "", True),
]

cluster_select_test_data = [
    ("cluster-select", "Please enter a cluster name.", "local"),
    ("cluster-select ", "Please enter a cluster name.", "local"),
    ("cluster-select a", "Unknown cluster!", "local"),
    ("cluster-select this-cluster-does-not-exist", "Unknown cluster!", "local"),
    ("cluster-select this-cluster-does-not-exist no-command", "Too many arguments!", "local"),
    ("cluster-select this-cluster-does-not-exist no-command again", "Too many arguments!", "local"),
    ("cluster-select test", "Selected cluster: test", "test"),
    ("cluster-select local", "Selected cluster: local", "local"),
]

exit_test_data = ["exit", " exit", "exit    "]
clear_test_data = ["clear", " clear", "clear   "]
save_test_data = ["save", " save", "save   "]
version_test_data = [
    ("version", "0.0.1"),
    (" version", "0.0.1"),
    (" version ", "0.0.2"),
]


@mock.patch('os.system')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input,expected", test_data)
def test_executor(mock_config_path, mock_os_system, test_input, expected):
    mock_config_path.return_value = setup_config_path_for_test()

    executor = kafkashell.executor.Executor(kafkashell.settings.Settings())
    executor.execute(test_input)

    mock_os_system.assert_called_once_with(expected)


@mock.patch('os.system')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input,expected,config_file", consumer_test_data)
def test_executor_consumer_settings(mock_config_path, mock_os_system, test_input, expected, config_file):
    mock_config_path.return_value = setup_config_path_for_test(config_file)

    executor = kafkashell.executor.Executor(kafkashell.settings.Settings())
    executor.execute(test_input)

    mock_os_system.assert_called_once_with(expected)


@mock.patch('os.system')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input,expected,config_file", producer_test_data)
def test_executor_producer_settings(mock_config_path, mock_os_system, test_input, expected, config_file):
    mock_config_path.return_value = setup_config_path_for_test(config_file)

    executor = kafkashell.executor.Executor(kafkashell.settings.Settings())
    executor.execute(test_input)

    mock_os_system.assert_called_once_with(expected)


@mock.patch('os.system')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input,expected,config_file", admin_client_test_data)
def test_executor_admin_client_settings(mock_config_path, mock_os_system, test_input, expected, config_file):
    mock_config_path.return_value = setup_config_path_for_test(config_file)

    executor = kafkashell.executor.Executor(kafkashell.settings.Settings())
    executor.execute(test_input)

    mock_os_system.assert_called_once_with(expected)


@mock.patch('os.system')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input,expected", prefix_test_data)
def test_executor_command_prefix(mock_config_path, mock_os_system, test_input, expected):
    mock_config_path.return_value = setup_config_path_for_test("test-prefix")

    executor = kafkashell.executor.Executor(kafkashell.settings.Settings())
    executor.execute(test_input)

    mock_os_system.assert_called_once_with(expected)


@mock.patch('os.system')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input,expected", prefix_none_test_data)
def test_executor_command_prefix_none(mock_config_path, mock_os_system, test_input, expected):
    mock_config_path.return_value = setup_config_path_for_test("test-prefix-none")

    executor = kafkashell.executor.Executor(kafkashell.settings.Settings())
    executor.execute(test_input)

    mock_os_system.assert_called_once_with(expected)


@mock.patch('sys.exit')
@mock.patch('kafkashell.settings.Settings.save_settings')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input", exit_test_data)
def test_executor_exit(mock_config_path, mock_save_settings, mock_exit, test_input):
    mock_config_path.return_value = setup_config_path_for_test()

    executor = kafkashell.executor.Executor(kafkashell.settings.Settings())
    executor.execute(test_input)

    mock_save_settings.assert_called_once()
    mock_exit.assert_called_once_with(0)


@mock.patch('prompt_toolkit.shortcuts.clear')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input", clear_test_data)
def test_executor_clear(mock_config_path, mock_clear, test_input):
    mock_config_path.return_value = setup_config_path_for_test()

    executor = kafkashell.executor.Executor(kafkashell.settings.Settings())
    executor.execute(test_input)

    mock_clear.assert_called_once()


@mock.patch(patch_name, create=True)
@mock.patch('kafkashell.settings.Settings.save_settings')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input", save_test_data)
def test_executor_save(mock_config_path, mock_save_settings, mock_print, test_input):
    mock_config_path.return_value = setup_config_path_for_test()

    executor = kafkashell.executor.Executor(kafkashell.settings.Settings())
    executor.execute(test_input)

    mock_save_settings.assert_called_once()
    mock_print.assert_called_once_with("Saved settings!")


@mock.patch('kafkashell.settings.Settings.get_cluster_details')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input,expected", command_prefix_test_data)
def test_check_for_valid_command_prefix(mock_config_path, mock_cluster_details, test_input, expected):
    mock_config_path.return_value = setup_config_path_for_test()
    mock_cluster_details.return_value = test_input

    executor = kafkashell.executor.Executor(kafkashell.settings.Settings())
    assert executor.check_for_valid_command_prefix() == expected


@mock.patch(patch_name, create=True)
@mock.patch('kafkashell.version.get_version')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input,expected", version_test_data)
def test_executor_version(mock_config_path, mock_get_version, mock_print, test_input, expected):
    mock_config_path.return_value = setup_config_path_for_test()
    mock_get_version.return_value = expected
    executor = kafkashell.executor.Executor(kafkashell.settings.Settings())
    executor.execute(test_input)

    mock_get_version.assert_called_once()
    mock_print.assert_called_once_with(expected)


@mock.patch(patch_name, create=True)
@mock.patch('kafkashell.helpers.print_cluster_config')
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input,expected,success", cluster_describe_test_data)
def test_executor_cluster_describe(mock_config_path, mock_print_cluster, mock_print, test_input, expected, success):
    mock_config_path.return_value = setup_config_path_for_test()
    settings = kafkashell.settings.Settings()
    executor = kafkashell.executor.Executor(settings)
    executor.execute(test_input)
    if success:
        mock_print_cluster.assert_called_once_with(settings.user_config["clusters"][test_input.split(" ")[1]])
    else:
        mock_print.assert_called_once_with(expected)


@mock.patch(patch_name, create=True)
@mock.patch('kafkashell.config.get_user_config_path')
@pytest.mark.parametrize("test_input,expected,selected_cluster", cluster_select_test_data)
def test_executor_cluster_select(mock_config_path, mock_print, test_input, expected, selected_cluster):
    mock_config_path.return_value = setup_config_path_for_test()
    settings = kafkashell.settings.Settings()
    executor = kafkashell.executor.Executor(settings)
    executor.execute(test_input)

    mock_print.assert_called_once_with(expected)
    assert settings.cluster == selected_cluster
