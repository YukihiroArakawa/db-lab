# etcd raft test

## setup environments

```
$ docker compose up -d

# show docker logs
$ docker logs -f etcd1
$ docker logs -f etcd2
$ docker logs -f etcd3

# or visualize logs by lazydocker
$ lazydocker
```

## first leader election

```
$ docker logs etcd1 | grep leader

{"level":"info","ts":"2025-07-26T06:38:20.745271Z","logger":"raft","caller":"v3@v3.6.0/raft.go:970","msg":"99eab3685d8363a1 became leader at term 2"}
{"level":"info","ts":"2025-07-26T06:38:20.745299Z","logger":"raft","caller":"v3@v3.6.0/node.go:370","msg":"raft.node: 99eab3685d8363a1 elected leader 99eab3685d8363a1 at term 2"}

```

## log replication

```
$ docker exec etcd1 etcdctl put mykey hello_raft
OK

$ docker exec etcd1 etcdctl get mykey
mykey
hello_raft

$ docker exec etcd2 etcdctl get mykey
mykey
hello_raft

$ docker exec etcd3 etcdctl get mykey
mykey
hello_raft
```

## leader election from stopping the leader node

```
$ docker exec etcd1 etcdctl endpoint status --write-out=table
+----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT    |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
| 127.0.0.1:2379 | 99eab3685d8363a1 |   3.6.4 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         2 |          9 |                  9 |        |                          |             false |
+----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+

$ docker stop etcd1

$ docker logs etcd2 | tail -n 10

{"level":"info","ts":"2025-07-26T06:56:04.309392Z","logger":"raft","caller":"v3@v3.6.0/node.go:376","msg":"raft.node: dcb68c82481661be lost leader 99eab3685d8363a1 at term 3"}
{"level":"info","ts":"2025-07-26T06:56:04.310250Z","logger":"raft","caller":"v3@v3.6.0/node.go:370","msg":"raft.node: dcb68c82481661be elected leader 876043ef79ada1ea at term 3"}

{"level":"warn","ts":"2025-07-26T06:56:04.409714Z","caller":"rafthttp/stream.go:420","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"dcb68c82481661be","remote-peer-id":"99eab3685d8363a1","error":"EOF"}
{"level":"warn","ts":"2025-07-26T06:56:04.410580Z","caller":"rafthttp/stream.go:420","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"dcb68c82481661be","remote-peer-id":"99eab3685d8363a1","error":"EOF"}
{"level":"warn","ts":"2025-07-26T06:56:04.412267Z","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"99eab3685d8363a1","error":"failed to dial 99eab3685d8363a1 on stream MsgApp v2 (peer 99eab3685d8363a1 failed to find local node dcb68c82481661be)"}
{"level":"warn","ts":"2025-07-26T06:56:09.981970Z","caller":"rafthttp/stream.go:193","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","local-member-id":"dcb68c82481661be","remote-peer-id":"99eab3685d8363a1"}
{"level":"warn","ts":"2025-07-26T06:56:09.982105Z","caller":"rafthttp/stream.go:193","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"dcb68c82481661be","remote-peer-id":"99eab3685d8363a1"}
{"level":"warn","ts":"2025-07-26T06:56:25.006319Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_RAFT_MESSAGE","remote-peer-id":"99eab3685d8363a1","rtt":"1.470376ms","error":"dial tcp: lookup etcd1 on 127.0.0.11:53: server misbehaving"}
{"level":"warn","ts":"2025-07-26T06:56:25.006239Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_SNAPSHOT","remote-peer-id":"99eab3685d8363a1","rtt":"505.634µs","error":"dial tcp: lookup etcd1 on 127.0.0.11:53: server misbehaving"}


$ docker exec etcd2 etcdctl endpoint status --write-out=table
+----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT    |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
| 127.0.0.1:2379 | dcb68c82481661be |   3.6.4 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         11 |                 11 |        |                          |             false |
+----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+

$ docker exec etcd3 etcdctl endpoint status --write-out=table
+----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT    |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
| 127.0.0.1:2379 | 876043ef79ada1ea |   3.6.4 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         3 |         11 |                 11 |        |                          |             false |
+----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
```


## cleanup environments

```
$ docker compose down
```
