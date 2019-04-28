from __future__ import unicode_literals

command_test_data = [
    (
        "",
        ["version", "cluster-select", "cluster-describe", "exit", "clear", "kafka-acls", "kafka-avro-console-consumer",
         "kafka-avro-console-producer", "kafka-replica-verification", "kafka-preferred-replica-election",
         "kafka-broker-api-versions", "kafka-configs", "kafka-console-consumer", "kafka-console-producer",
         "kafka-consumer-groups", "kafka-delete-records", "kafka-dump-log", "kafka-log-dirs", "kafka-topics",
         "kafka-verifiable-consumer", "kafka-verifiable-producer", "ksql", "zookeeper-shell"]
    ),
    (
        "kafka",
        ["kafka-acls", "kafka-avro-console-consumer", "kafka-avro-console-producer", "kafka-broker-api-versions",
         "kafka-configs", "kafka-console-consumer", "kafka-console-producer", "kafka-consumer-groups",
         "kafka-delete-records", "kafka-dump-log", "kafka-log-dirs", "kafka-topics", "kafka-verifiable-consumer",
         "kafka-verifiable-producer", "kafka-replica-verification", "kafka-preferred-replica-election"]
    ),
    (
        "k",
        ["ksql", "kafka-acls", "kafka-avro-console-consumer", "kafka-avro-console-producer",
         "kafka-broker-api-versions", "kafka-replica-verification", "kafka-preferred-replica-election",
         "kafka-configs", "kafka-console-consumer", "kafka-console-producer", "kafka-consumer-groups",
         "kafka-delete-records", "kafka-dump-log", "kafka-log-dirs", "kafka-topics", "kafka-verifiable-consumer",
         "kafka-verifiable-producer", "zookeeper-shell"]
    ),
    (
        "ksq",
        ["ksql"]
    ),
    (
        "zookeeper",
        ["zookeeper-shell"]
    ),
    (
        "kafka-topics",
        ["kafka-topics"]
    ),
    (
        "cluster-",
        ["cluster-select", "cluster-describe"]
    ),
    (
        "this-command-does-not-exist",
        []
    )
]

option_test_data = [
    (
        "kafka-topics ",
        ["--alter", "--config", "--create", "--delete", "--delete-config", "--describe", "--disable-rack-aware",
         "--exclude-internal", "--force", "--help", "--if-exists", "--if-not-exists", "--list", "--partitions",
         "--replica-assignment", "--replication-factor", "--topic", "--topics-with-overrides",
         "--unavailable-partitions", "--under-replicated-partitions", "--zookeeper"]
    ),
    (
        "kafka-configs ",
        ["--add-config", "--alter", "--bootstrap-server", "--command-config", "--delete-config", "--describe",
         "--entity-default", "--entity-name", "--entity-type", "--force", "--help", "--zookeeper"]
    ),
    (
        "kafka-console-consumer ",
        ["--bootstrap-server", "--consumer-property", "--consumer.config", "--enable-systest-events", "--formatter",
         "--from-beginning", "--group", "--isolation-level", "--key-deserializer", "--max-messages", "--offset",
         "--partition", "--property", "--skip-message-on-error", "--timeout-ms", "--topic", "--value-deserializer",
         "--whitelist"]
    ),
    (
        "kafka-console-consumer --group test ",
        ["--bootstrap-server", "--consumer-property", "--consumer.config", "--enable-systest-events", "--formatter",
         "--from-beginning", "--isolation-level", "--key-deserializer", "--max-messages", "--offset",
         "--partition", "--property", "--skip-message-on-error", "--timeout-ms", "--topic", "--value-deserializer",
         "--whitelist"]
    ),
    (
        "kafka-console-consumer --group test --consumer-property print.key=true ",
        ["--bootstrap-server", "--consumer-property", "--consumer.config", "--enable-systest-events", "--formatter",
         "--from-beginning", "--isolation-level", "--key-deserializer", "--max-messages", "--offset",
         "--partition", "--property", "--skip-message-on-error", "--timeout-ms", "--topic", "--value-deserializer",
         "--whitelist"]
    ),
    (
        "kafka-console-consumer --group test --consumer-property print.key=true --for",
        ["--formatter"]
    ),
    (
        "ksql ",
        ["--", "--config-file", "--help", "--output", "--query-row-limit", "--query-timeout"]
    ),
    (
        "zookeeper-shell ",
        []
    ),
    (
        "cluster-select l",
        ["local"]
    ),
    (
        "cluster-describe ",
        ["local"]
    )
]

option_value_test_data = [
    (
        "kafka-configs --add-config ",
        ["SCRAM-SHA-256", "SCRAM-SHA-512", "advertised.listeners", "background.threads", "cleanup.policy",
         "compression.type", "consumer_byte_rate", "delete.retention.ms", "file.delete.delay.ms", "flush.messages",
         "flush.ms", "follower.replication.throttled.rate", "follower.replication.throttled.replicas",
         "index.interval.bytes", "leader.replication.throttled.rate", "leader.replication.throttled.replicas",
         "listener.security.protocol.map", "listeners", "log.cleaner.backoff.ms", "log.cleaner.dedupe.buffer.size",
         "log.cleaner.delete.retention.ms", "log.cleaner.io.buffer.load.factor", "log.cleaner.io.buffer.size",
         "log.cleaner.io.max.bytes.per.second", "log.cleaner.min.cleanable.ratio", "log.cleaner.min.compaction.lag.ms",
         "log.cleaner.threads", "log.cleanup.policy", "log.flush.interval.messages", "log.flush.interval.ms",
         "log.index.interval.bytes", "log.index.size.max.bytes", "log.message.downconversion.enable",
         "log.message.timestamp.difference.max.ms", "log.message.timestamp.type", "log.preallocate",
         "log.retention.bytes", "log.retention.ms", "log.roll.jitter.ms", "log.roll.ms", "log.segment.bytes",
         "log.segment.delete.delay.ms", "max.connections.per.ip", "max.connections.per.ip.overrides",
         "max.message.bytes", "message.downconversion.enable", "message.format.version", "message.max.bytes",
         "message.timestamp.difference.max.ms", "message.timestamp.type", "metric.reporters",
         "min.cleanable.dirty.ratio", "min.compaction.lag.ms", "min.insync.replicas", "num.io.threads",
         "num.network.threads", "num.recovery.threads.per.data.dir", "num.replica.fetchers", "preallocate",
         "principal.builder.class", "producer_byte_rate", "request_percentage", "retention.bytes", "retention.ms",
         "sasl.enabled.mechanisms", "sasl.jaas.config", "sasl.kerberos.kinit.cmd",
         "sasl.kerberos.min.time.before.relogin", "sasl.kerberos.principal.to.local.rules",
         "sasl.kerberos.service.name", "sasl.kerberos.ticket.renew.jitter", "sasl.kerberos.ticket.renew.window.factor",
         "sasl.login.refresh.buffer.seconds", "sasl.login.refresh.min.period.seconds",
         "sasl.login.refresh.window.factor", "sasl.login.refresh.window.jitter", "sasl.mechanism.inter.broker.protocol",
         "segment.bytes", "segment.index.bytes", "segment.jitter.ms", "segment.ms", "ssl.cipher.suites",
         "ssl.client.auth", "ssl.enabled.protocols", "ssl.endpoint.identification.algorithm", "ssl.key.password",
         "ssl.keymanager.algorithm", "ssl.keystore.location", "ssl.keystore.password", "ssl.keystore.type",
         "ssl.protocol", "ssl.provider", "ssl.secure.random.implementation", "ssl.trustmanager.algorithm",
         "ssl.truststore.location", "ssl.truststore.password", "ssl.truststore.type", "unclean.leader.election.enable"]
    ),
    (
        "kafka-configs --entity-type ",
        ["broker", "client", "topic", "user"]
    ),
    (
        "kafka-configs --entity-type broker --add-config ",
        ["advertised.listeners", "background.threads", "compression.type", "follower.replication.throttled.rate",
         "leader.replication.throttled.rate", "listener.security.protocol.map", "listeners", "log.cleaner.backoff.ms",
         "log.cleaner.dedupe.buffer.size", "log.cleaner.delete.retention.ms", "log.cleaner.io.buffer.load.factor",
         "log.cleaner.io.buffer.size", "log.cleaner.io.max.bytes.per.second", "log.cleaner.min.cleanable.ratio",
         "log.cleaner.min.compaction.lag.ms", "log.cleaner.threads", "log.cleanup.policy",
         "log.flush.interval.messages", "log.flush.interval.ms", "log.index.interval.bytes", "log.index.size.max.bytes",
         "log.message.downconversion.enable", "log.message.timestamp.difference.max.ms", "log.message.timestamp.type",
         "log.preallocate", "log.retention.bytes", "log.retention.ms", "log.roll.jitter.ms", "log.roll.ms",
         "log.segment.bytes", "log.segment.delete.delay.ms", "max.connections.per.ip",
         "max.connections.per.ip.overrides", "message.max.bytes", "metric.reporters", "min.insync.replicas",
         "num.io.threads", "num.network.threads", "num.recovery.threads.per.data.dir", "num.replica.fetchers",
         "principal.builder.class", "sasl.enabled.mechanisms", "sasl.jaas.config", "sasl.kerberos.kinit.cmd",
         "sasl.kerberos.min.time.before.relogin", "sasl.kerberos.principal.to.local.rules",
         "sasl.kerberos.service.name", "sasl.kerberos.ticket.renew.jitter", "sasl.kerberos.ticket.renew.window.factor",
         "sasl.login.refresh.buffer.seconds", "sasl.login.refresh.min.period.seconds",
         "sasl.login.refresh.window.factor", "sasl.login.refresh.window.jitter", "sasl.mechanism.inter.broker.protocol",
         "ssl.cipher.suites", "ssl.client.auth", "ssl.enabled.protocols", "ssl.endpoint.identification.algorithm",
         "ssl.key.password", "ssl.keymanager.algorithm", "ssl.keystore.location", "ssl.keystore.password",
         "ssl.keystore.type", "ssl.protocol", "ssl.provider", "ssl.secure.random.implementation",
         "ssl.trustmanager.algorithm", "ssl.truststore.location", "ssl.truststore.password", "ssl.truststore.type",
         "unclean.leader.election.enable"]
    ),
    (
        "kafka-configs --entity-type broker --delete-config ",
        ["advertised.listeners", "background.threads", "compression.type", "follower.replication.throttled.rate",
         "leader.replication.throttled.rate", "listener.security.protocol.map", "listeners", "log.cleaner.backoff.ms",
         "log.cleaner.dedupe.buffer.size", "log.cleaner.delete.retention.ms", "log.cleaner.io.buffer.load.factor",
         "log.cleaner.io.buffer.size", "log.cleaner.io.max.bytes.per.second", "log.cleaner.min.cleanable.ratio",
         "log.cleaner.min.compaction.lag.ms", "log.cleaner.threads", "log.cleanup.policy",
         "log.flush.interval.messages", "log.flush.interval.ms", "log.index.interval.bytes", "log.index.size.max.bytes",
         "log.message.downconversion.enable", "log.message.timestamp.difference.max.ms", "log.message.timestamp.type",
         "log.preallocate", "log.retention.bytes", "log.retention.ms", "log.roll.jitter.ms", "log.roll.ms",
         "log.segment.bytes", "log.segment.delete.delay.ms", "max.connections.per.ip",
         "max.connections.per.ip.overrides", "message.max.bytes", "metric.reporters", "min.insync.replicas",
         "num.io.threads", "num.network.threads", "num.recovery.threads.per.data.dir", "num.replica.fetchers",
         "principal.builder.class", "sasl.enabled.mechanisms", "sasl.jaas.config", "sasl.kerberos.kinit.cmd",
         "sasl.kerberos.min.time.before.relogin", "sasl.kerberos.principal.to.local.rules",
         "sasl.kerberos.service.name", "sasl.kerberos.ticket.renew.jitter", "sasl.kerberos.ticket.renew.window.factor",
         "sasl.login.refresh.buffer.seconds", "sasl.login.refresh.min.period.seconds",
         "sasl.login.refresh.window.factor", "sasl.login.refresh.window.jitter", "sasl.mechanism.inter.broker.protocol",
         "ssl.cipher.suites", "ssl.client.auth", "ssl.enabled.protocols", "ssl.endpoint.identification.algorithm",
         "ssl.key.password", "ssl.keymanager.algorithm", "ssl.keystore.location", "ssl.keystore.password",
         "ssl.keystore.type", "ssl.protocol", "ssl.provider", "ssl.secure.random.implementation",
         "ssl.trustmanager.algorithm", "ssl.truststore.location", "ssl.truststore.password", "ssl.truststore.type",
         "unclean.leader.election.enable"]
    ),
    (
        "kafka-configs --entity-type topic --add-config ",
        ["cleanup.policy", "compression.type", "delete.retention.ms", "file.delete.delay.ms", "flush.messages",
         "flush.ms", "follower.replication.throttled.replicas", "index.interval.bytes",
         "leader.replication.throttled.replicas", "max.message.bytes", "message.downconversion.enable",
         "message.format.version", "message.timestamp.difference.max.ms", "message.timestamp.type",
         "min.cleanable.dirty.ratio", "min.compaction.lag.ms", "min.insync.replicas", "preallocate", "retention.bytes",
         "retention.ms", "segment.bytes", "segment.index.bytes", "segment.jitter.ms", "segment.ms",
         "unclean.leader.election.enable"]
    ),
    (
        "kafka-configs --entity-type user --add-config ",
        ["SCRAM-SHA-256", "SCRAM-SHA-512", "consumer_byte_rate", "producer_byte_rate", "request_percentage"]
    ),
    (
        "kafka-configs --entity-type client --add-config ",
        ["consumer_byte_rate", "producer_byte_rate", "request_percentage"]
    ),
    (
        "kafka-configs --entity-type client --delete-config ",
        ["consumer_byte_rate", "producer_byte_rate", "request_percentage"]
    ),
    (
        "kafka-topics --config ",
        ["cleanup.policy", "compression.type", "delete.retention.ms", "file.delete.delay.ms", "flush.messages",
         "flush.ms", "follower.replication.throttled.replicas", "index.interval.bytes",
         "leader.replication.throttled.replicas", "max.message.bytes", "message.downconversion.enable",
         "message.format.version", "message.timestamp.difference.max.ms", "message.timestamp.type",
         "min.cleanable.dirty.ratio", "min.compaction.lag.ms", "min.insync.replicas", "preallocate", "retention.bytes",
         "retention.ms", "segment.bytes", "segment.index.bytes", "segment.jitter.ms", "segment.ms",
         "unclean.leader.election.enable"]
    ),
    (
        "kafka-topics --delete-config ",
        ["cleanup.policy", "compression.type", "delete.retention.ms", "file.delete.delay.ms", "flush.messages",
         "flush.ms", "follower.replication.throttled.replicas", "index.interval.bytes",
         "leader.replication.throttled.replicas", "max.message.bytes", "message.downconversion.enable",
         "message.format.version", "message.timestamp.difference.max.ms", "message.timestamp.type",
         "min.cleanable.dirty.ratio", "min.compaction.lag.ms", "min.insync.replicas", "preallocate", "retention.bytes",
         "retention.ms", "segment.bytes", "segment.index.bytes", "segment.jitter.ms", "segment.ms",
         "unclean.leader.election.enable"]
    ),
    (
        "kafka-configs --add-config cleanup.polic",
        ["cleanup.policy", "log.cleanup.policy"]
    ),
    (
        "kafka-configs --add-config cleanup.policy=",
        ["compact", "delete"]
    ),
    (
        "kafka-configs --add-config log.cleanup.policy=",
        ["compact", "delete"]
    ),
    (
        "kafka-configs --add-config log.cleanup.policy=comp",
        ["compact"]
    ),
    (
        "kafka-configs --add-config ssl.protocol=",
        []
    ),
    (
        "kafka-configs --add-config log.message.timestamp.type=",
        ["CreateTime", "LogAppendTime"]
    ),
    (
        "kafka-configs --add-config log.message.timestamp.type=Create",
        ["CreateTime"]
    ),
    (
        "kafka-configs --add-config log.message.timestamp.type=asdf",
        []
    ),
    (
        "kafka-configs --add-config compression.type=",
        ["gzip", "lz4", "none", "snappy", "zstd"]
    ),
    (
        "kafka-configs --delete-config compression.type=",
        ["gzip", "lz4", "none", "snappy", "zstd"]
    ),
    (
        "kafka-configs --add-config compression.type=z",
        ["zstd", "gzip", "lz4"]
    ),
    (
        "kafka-topics --config compression.type=",
        ["gzip", "lz4", "none", "snappy", "zstd"]
    ),
    (
        "kafka-topics --config message.timestamp.type=",
        ["CreateTime", "LogAppendTime"]
    ),
    (
        "kafka-topics --delete-config message.timestamp.type=",
        ["CreateTime", "LogAppendTime"]
    ),
    (
        "ksql --output ",
        ["JSON", "TABULAR"]
    ),
    (
        "ksql --output JS",
        ["JSON"]
    ),
    (
        "kafka-console-producer --request-required-acks ",
        ["-1", "0", "1", "all"]
    ),
    (
        "kafka-avro-console-producer --request-required-acks ",
        ["-1", "0", "1", "all"]
    ),
    (
        "kafka-verifiable-producer --acks ",
        ["-1", "0", "1", "all"]
    ),
    (
        "kafka-verifiable-consumer --reset-policy ",
        ["earliest", "latest", "none"]
    ),
    (
        "kafka-acls --resource-pattern-type ",
        ["ANY", "LITERAL", "MATCH", "PREFIXED"]
    ),
    (
        "kafka-console-producer --compression-codec ",
        ["gzip", "lz4", "none", "snappy", "zstd"]
    ),
    (
        "kafka-configs --add-config unclean.leader.election.enable=",
        ["true", "false"]
    ),
    (
        "kafka-configs --delete-config unclean.leader.election.enable=fal",
        ["false"]
    ),
    (
        "kafka-topics --config unclean.leader.election.enable=",
        ["true", "false"]
    ),
    (
        "kafka-topics --delete-config unclean.leader.election.enable=",
        ["true", "false"]
    ),
    (
        "kafka-configs --add-config log.preallocate=",
        ["true", "false"]
    ),
    (
        "kafka-configs --delete-config log.preallocate=tr",
        ["true"]
    ),
    (
        "kafka-topics --config preallocate=",
        ["true", "false"]
    ),
    (
        "kafka-topics --delete-config preallocate=",
        ["true", "false"]
    ),
    (
        "kafka-configs --add-config log.message.downconversion.enable=",
        ["true", "false"]
    ),
    (
        "kafka-topics --config message.downconversion.enable=",
        ["true", "false"]
    )
]
