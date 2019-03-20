# kafka-shell

[![Build Status](https://travis-ci.org/devshawn/kafka-shell.svg?branch=master)](https://travis-ci.org/devshawn/kafka-shell) [![codecov](https://codecov.io/gh/devshawn/kafka-shell/branch/master/graph/badge.svg)](https://codecov.io/gh/devshawn/kafka-shell) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A supercharged, interactive Kafka shell built on top of the existing Kafka CLI tools.

<p align="center">
    <img src="https://i.imgur.com/b1oNTZZ.png"/>
</p>

Kafka shell allows you to configure a list of clusters, and properties such as `--bootstrap-server` and `--zookeeper` for the currently selected cluster will automatically be added when the command is run. No more remembering long server addresses or ports! 

## Installation
Kafka shell requires `python` and `pip`. Kafka shell is a wrapper over the existing Kafka command-line tools, so 
those must exist within your `PATH`.

You can install kafka-shell using pip:

```bash
pip install kafka-shell
```

## Usage
Kafka shell is an interactive shell. You can run it from the terminal by:

```bash
kafka-shell
```

From here, you can start typing `kafka` and the autocomplete will kick in.

**Key Commands**
- **Change Cluster**: The selected cluster commands are run against can be cycled through by pressing `F2`.
- **Fuzzy Search**: By default, fuzzy search of commands is enabled. This can be toggled on & off by pressing `F3`.
- **In-line Help**: By default, in-line help is shown along side the drop-down suggestion list. This can be toggled on & off by pressing `F9`.
- **Exit**: The shell can be exited by pressing `F10` or by typing `exit`. 

## Configuration
Kafka shell allows you to configure settings and Kafka clusters to run commands against through a configuration file.

By default, when `kafka-shell` is first run, a directory in your home directory is generated at `~/.kafka-shell`. A configuration file called `config.yaml` is generated in that new folder. It is a YAML file containing details about clusters, `kafka-shell` configuration, and more.

See [CONFIGURATION.md][configuration] to add a cluster to your configuration or to set other `kafka-shell` settings.

## Features
Kafka shell simplifies running complex Kafka CLI commands as well as provides smart auto-completion of commands, options, and more. /Users/shawn/.kafka-shell/config.yaml

- Auto-completion of commands, options, and configurations
- Configure clusters to run commands against and switch between them
- Fish-style auto suggestions
- Command history
- Contextual help
- Toolbar options

**Completion of Configurations**

Auto completion of Kafka configuration keys and their values.

<p align="center">
    <img src="https://i.imgur.com/fkwzOkv.png"/>
</p>

**Configure Clusters, Schema Registries, & More**

Configure clusters and their properties will automatically be added to commands being run.

<p align="center">
    <img src="https://i.imgur.com/3JjIxyL.png"/>
</p>

## Supported Commands
Currently, the following commands are supported:

* `kafka-topics`
* `kafka-configs`
* `kafka-console-consumer`
* `kafka-console-producer`
* `kafka-avro-console-consumer`
* `kafka-avro-console-producer`
* `kafka-verifiable-consumer`
* `kafka-verifiable-producer`
* `kafka-broker-api-versions`
* `kafka-consumer-groups`
* `kafka-delete-records`
* `kafka-log-dirs`
* `kafka-dump-log`
* `kafka-acls`
* `ksql`

**Helper Commands**

Currently, kafka-shell has helper commands:

* `exit`: exit the shell
* `clear`: clear the shell
* `cluster-select`: select a cluster
* `cluster-describe`: describe a cluster config

In-line help for each command and option is shown by default. This can be toggled by `F9`.

## Contributing
Contributions are very welcome. See [CONTRIBUTING.md][contributing] for details.

## Acknowledgement
This project was inspired by multiple amazing shells & prompts, such as [saws][saws], [kube-shell][kube-shell], [kube-prompt][kube-prompt], [http-prompt][http-prompt], and [wharfee][wharfee]. It was built using [prompt-toolkit][prompt-toolkit]. Much ❤️ to [Apache Kafka][kafka] and [Confluent][confluent] for their helpful CLI tools. 

## License
Copyright (c) 2019 Shawn Seymour.

Licensed under the [Apache 2.0 license][license].

[saws]: https://github.com/donnemartin/saws
[kube-shell]: https://github.com/cloudnativelabs/kube-shell
[kube-prompt]: https://github.com/c-bata/kube-prompt
[http-prompt]: https://github.com/eliangcs/http-prompt
[wharfee]: https://github.com/j-bennet/wharfee
[prompt-toolkit]: https://github.com/prompt-toolkit/python-prompt-toolkit
[kafka]: https://kafka.apache.org
[confluent]: https://www.confluent.io/
[configuration]: CONFIGURATION.md
[contributing]: CONTRIBUTING.md
[license]: LICENSE
