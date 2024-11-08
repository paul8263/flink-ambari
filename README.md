# Flink Ambari integration

This project enables Ambari to setup Flink cluster.

# Environment

* OS: CentOS/Redhat
* Ambari: 2.7.5
* HDP: 3.0.1.0.187
* Flink: 1.17.2

# How to use

Copy `FLINK` folder to `/var/lib/ambari-server/resources/stacks/HD/{stack_version}/services` folder in Ambari Server host and then restart Ambari Server.

Then clean the cache of all Ambari Agent by running the following:

```shell
rm -rf /var/lib/ambari-agent/cache/*
ambari-agent restart
```

# Deploy mode

By default, it only supports Flink on Yarn, thus service check and quicklinks are disabled.

You can deploy Flink as standalone mode by replacing the content of `FLINK/metainfo.xml` with `metainfo-standalone.xml`.
