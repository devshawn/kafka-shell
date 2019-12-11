# Configuration

Kafka shell can be configured via a YAML file. It is generated on initialization and located in `~/.kafka-shell`. 

The user configuration file is defined by a JSON schema, which can be viewed at [shell-config.schema][schema]. The user configuration is parsed and validated on initialization of `kafka-shell`. If your modified configuration is incorrect, the shell will exit and print an error message displaying the validation error, such as a missing required field. 

## Default Configuration
By default, the generated `~/.kafka-shell/config.yaml` file looks like this:

```yaml
version: 1
enable:
  history: true
  save_on_exit: true
  auto_complete: true
  auto_suggest: true
  inline_help: true
  fuzzy_search: true
cluster: local
clusters:
  local:
    bootstrap_servers: localhost:9092
    zookeeper_connect: localhost:2181
    schema_registry_url: http://localhost:8081
    ksql_server_url: http://localhost:8088
```

## Customization
One of the main benefits of utilizing `kafka-shell` instead of directly using the Kafka command-line tools is the ability to define clusters, in which commands will be run against by default. This means you no longer have to pass flags such as `--bootstrap-server`; they'll be added automatically when you run the command. The `~/.kafka-shell/config.yaml` file is where you define clusters to run against, as well as other settings for `kafka-shell`. 

In the future, we plan to add configuration via commands within the shell. For now, it must be manually done by editing the JSON file. 

### Shell Settings
There are a few top level settings to define how the shell works. Most of these can also be changed via function keys while using `kafka-shell`. Defaults for each property are shown above.

| key        | type    | description                                                    |
|------------|---------|----------------------------------------------------------------|
| `version`  | int     | Version of the configuration schema. Must be 1.                |
| `enable`   | Enable  | Enable various features within kafka-shell.                    |
| `cluster`  | string  | Default cluster to be selected on initialization.              |
| `clusters` | Cluster | Clusters that commands can run against. See below for details. |

### Enable Features
Features for `kafka-shell` can be enabled through feature flags defined in the `enable` root-level object.

| key             | type    | description                                                      |
|-----------------|---------|------------------------------------------------------------------|
| `history`       | boolean | Save command history between `kafka-shell` sessions.             |
| `save_on_exit`  | boolean | Save any settings changed by key bindings on exit.               |
| `auto_complete` | boolean | Show the command autocomplete dropdown when typing.              |
| `auto_suggest`  | boolean | Show suggestions from past commands like the fish shell.         |
| `inline_help`   | boolean | Show command and flag descriptions on the autocomplete dropdown. |
| `fuzzy_search`  | boolean | Allow fuzzy searching of autocomplete dropdown selections.       |


### Clusters
Clusters can be defined to run commands against. Commands automatically add flags such as `--bootstrap-server` to a command based on the selected `cluster`, which can be changed by `F2`. 

Each cluster should have a unique name (a key in the `clusters` root-level object). By default, the cluster `local` is added.

| key                      | type         | description                                                   |
|--------------------------|--------------|---------------------------------------------------------------|
| `bootstrap_servers`      | string       | Comma-separated `host:port` Kafka brokers to connect to.      |
| `zookeeper_connect`      | string       | Comma-separated `host:port` Zookeeper nodes to connect to.    |
| `schema_registry_url`    | string       | Schema Registry URL used when working with avro schemas.      |
| `ksql_server_url`        | string       | KSQL Server URL used when utilizing the `ksql` command.       |
| `command_prefix`         | string       | Prefix all commands with another command, i.e. 'docker exec'. |
| `command_file_extension` | string       | Add a file extension such as `sh` to commands.                |
| `consumer_settings`      | ToolSettings | Pass config and default property settings to consumer CLIs.   |
| `producer_settings`      | ToolSettings | Pass config and default property settings to producer CLIs.   |
| `admin_client_settings`  | ToolSettings | Pass config to admin clients through `--command-config`.      |


#### Tool Settings
Settings, such as a configuration properties files or default property settings, can be set for each cluster. 

See the below full config example to see how to use tool settings.

| key          | type   | description                                                |
|--------------|--------|------------------------------------------------------------|
| `config`     | string | A configuration properties file to be passed to CLI tools. |
| `properties` | object | Set default `--property` options to be passed.             |


## Full Configuration Example
The below example shows how to use some of the non-default settings. 

For example, when using cluster `docker-cluster`:
- All commands will be prefixed with `docker-exec -it kafka-tools`
- All consumer commands will add `--consumer.config consumer.properties` and `--property print.key=true`
- All producer commands will add `--producer.config producer.properties` and `--property key.separator=,`

```yaml
version: 1
enable:
  history: true
  save_on_exit: true
  auto_complete: true
  auto_suggest: true
  inline_help: true
  fuzzy_search: true
cluster: docker-cluster
clusters:
  docker-cluster:
    bootstrap_servers: docker:9092
    zookeeper_connect: docker:2181
    schema_registry_url: http://docker:8081
    ksql_server_url: http://docker:8081
    command_prefix: docker exec -it kafka-tools
    consumer_settings:
      config: consumer.properties
      properties:
        print.key: true
    producer_settings:
      config: producer.properties
      properties:
        key.separator: ","
    admin_client_settings:
      config: admin.properties
```

### Example Commands

These examples show what commands would *actually* be run based on what was typed, using the full configuration from above.

For example, if you typed the command `kafka-console-consumer --topic test`:

```bash
docker exec -it kafka-tools kafka-console-consumer --bootstrap-server docker:9092 --consumer.config consumer.properties --property print.key=true
```

For example, if you typed the command `kafka-avro-console-producer --topic test`:

```bash
docker exec -it kafka-tools kafka-avro-console-producer --broker-list docker:9092 --property schema.registry.url=http://docker:8081 --producer.config producer.properties --property key.separtor=,
```

For example, if you typed the command `kafka-broker-api-versions`:

```bash
docker exec -it kafka-tools kafka-broker-api-versions --bootstrap-server docker:9092 --command-config admin.properties
```

As you can see, you can save a ton of typing time by utilizing `kafka-shell`!

### Command File Extension

The file extension for commands such as `kafka-topics` is `null` by default. Depending on how you installed the kafka command-line tools, they may have the extension `sh` or `bat`. They may also be set this way in pre-built docker images.

You can change this, per cluster, by setting the `command_file_extension` property in the cluster config. For example:

```yaml
...
clusters:
  local:
    bootstrap_servers: localhost:9092
    zookeeper_connect: localhost:2181
    schema_registry_url: http://localhost:8081
    ksql_server_url: http://localhost:8088
    command_file_extension: sh
```

If you run `kafka-topics --list` with the above command, the following would be run:

```bash
kafka-topics.sh --list --zookeeper localhost:2181
```

Without the file extension config set, the following would be run:

```bash
kafka-topics --list --zookeeper localhost:2181
```

## Support
If you have a question on how to configure `kafka-shell`, feel free to [open a support issue][support].

[schema]: kafkashell/data/shell-config.schema
[support]: https://github.com/devshawn/kafka-shell/issues/new?assignees=&labels=support&title=
