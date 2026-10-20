# Scaling and partitioning

Every split across machines costs queries that span them and keys that run hot. Ask first whether the math says one tuned node is not enough, and whether the limit is reads, writes, storage, distance or operations.

## One node first

A single tuned database, scaled up, carries far more than people expect. Name the limit you hit, then check whether a bigger box, another engine or partitioning one huge table inside the same instance fixes it. Thresholds per store live in [storage](storage.md) and [numbers](numbers.md). Sharding early pays for a distributed system with no gain.

## Scale reads in order

Fix reads cheapest first. Index every query and sort (see [storage](storage.md#indexes)), then add hardware, then denormalise or precompute, then add read replicas, then a [cache and CDN](caching.md). Replicas lag, so a read that must see the user's own write, or that decides a purchase, goes to the primary.

## Batch, pre-aggregate and shed writes

When per-write overhead dominates, or writes are tiny increments on few keys, group them over a short window before they reach the store. Skip it when each write must be durable before the user hears back. A crash loses the in-memory batch unless a log can replay it. Under overload, decide ahead which writes to drop first (see [counting-and-aggregation](counting-and-aggregation.md)).

## Choose a shard key

Shard only when one node cannot take the writes, hold the data, or serve the reads even with replicas, and treat the key as close to permanent. Pick one with many values, an even spread and the unit that must stay consistent on one shard. A time key sends every new write to the newest shard. Hash by default. Use ranges for cheap scans, or a directory to move one heavy tenant, though a directory that is down takes everything down.

## Avoid scatter-gather

A query without the shard key asks every shard, so the slowest one sets its latency. Accept it for a rare admin report. On a common path, denormalise or precompute instead, or keep the fan-out cheap by merging a short top K from each shard.

## Consistent hashing

Use a hash ring when nodes join and leave, or a client must reach the server that holds its state. A change then moves only a neighbour's share of keys, where hash modulo N moves almost all. Skip it when the node count never changes, or a managed cluster already routes keys for you. Add virtual nodes, or a failed node dumps its load on one neighbour. During a resize, clients reconnect and state must move. An even spread of keys still leaves one popular key on one node.

## Hot partitions and hot keys

First ask whether the shard is hot for reads or for writes. Read-hot data gets copies or a cache in front (see [caching](caching.md)). Write-hot data that can be summed splits into sub-keys that readers add up, which costs every read a merge and loses per-key order. If the cause is a bad key, not popularity, change the key.

## Partition by region

When most interactions are local, give each region its own stack with servers next to their data. Do not split users who routinely act across the globe. Searches near a boundary must query both sides.

## Split services by load shape

Make a path its own service only when its volume or cost differs sharply from the rest. On a small system the split is pure overhead. Keep a must-not-drop write path apart from bursty heavy reads.

## Push work to the client

Let the device buffer or filter work when it can do so safely. Never trust it with clocks or prices. Delete local copies only after the server confirms, and do not assume one device per user.

## Cheap check first

When most candidates fail a costly check, run a cheap bound first and send only survivors on. In an exact search the bound must never drop a real match, and its answer is never the result. A learned first stage, as in a model cascade, does drop some, so it caps recall and needs watching on its own (see [ml-systems](ml-systems.md)).
