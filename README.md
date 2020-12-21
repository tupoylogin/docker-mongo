Mongo Sharded Cluster with Docker Compose
=========================================
A simple sharded Mongo Cluster with a replication factor of 2 running in `docker` using `docker-compose`.

DON'T USE THIS IN PRODUCTION!

### Mongo Components

* Config Server (3 member replica set): `mongo-1-1`,`mongo-1-2`,`mongo-1-3`
* 1 Shard (each a 3 member replica set):`mongo-cfg-1-1`,`mongo-cfg-1-2`,`mongo-cfg-1-3`
* 1 Router (mongos): `mongo-router`
* (TODO): perform components scaling iside entrypoint

### First Run (initial setup)
**Start all of the containers in detach mode**

```
docker-compose up -d
```

**Initialize the replica sets and router. Perform data aggregation**

```
sh entrypoint.sh
```

This script has a `sleep 15` to wait for the config server and shards to elect their primaries before initializing the router. For the sake of consistency of choosing primary node, first node of each replSet has the highest priority


### Resetting the Cluster
To remove all data and re-initialize the cluster, make sure the containers are stopped and then:

```
docker-compose down --remove-orphans
```

Execute the **First Run** instructions again.
