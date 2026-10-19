# Scaling and partitioning

Every split across machines costs queries that span them and keys that run hot. Ask first whether the math says one tuned node is not enough, and whether the limit is reads, writes, storage, distance or operations.

## One node first

A single tuned database, scaled up, carries far more than people expect. Name the limit you hit, then check whether a bigger box, another engine or partitioning one huge table inside the same instance fixes it. Thresholds per store live in [storage](storage.md) and [numbers](numbers.md). Sharding early pays for a distributed system with no gain.

Sources: [Numbers to know](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know), [Sharding](https://www.hellointerview.com/learn/system-design/core-concepts/sharding), [Scaling writes](https://www.hellointerview.com/learn/system-design/patterns/scaling-writes)

## Scale reads in order

Fix reads cheapest first. Index every query and sort (see [storage](storage.md#indexes)), then add hardware, then denormalise or precompute, then add read replicas, then a [cache and CDN](caching.md). Replicas lag, so a read that must see the user's own write, or that decides a purchase, goes to the primary.

Sources: [Scaling reads](https://www.hellointerview.com/learn/system-design/patterns/scaling-reads), [Postgres](https://www.hellointerview.com/learn/system-design/deep-dives/postgres), [Patterns](https://www.hellointerview.com/learn/system-design/in-a-hurry/patterns)

## Batch, pre-aggregate and shed writes

When per-write overhead dominates, or writes are tiny increments on few keys, group them over a short window before they reach the store. Skip it when each write must be durable before the user hears back. A crash loses the in-memory batch unless a log can replay it. Under overload, decide ahead which writes to drop first (see [counting-and-aggregation](counting-and-aggregation.md)).

Sources: [Scaling writes](https://www.hellointerview.com/learn/system-design/patterns/scaling-writes), [Metrics monitoring](https://www.hellointerview.com/learn/system-design/problem-breakdowns/metrics-monitoring), [Postgres](https://www.hellointerview.com/learn/system-design/deep-dives/postgres)

## Choose a shard key

Shard only when one node cannot take the writes, hold the data, or serve the reads even with replicas, and treat the key as close to permanent. Pick one with many values, an even spread and the unit that must stay consistent on one shard. A time key sends every new write to the newest shard. Hash by default. Use ranges for cheap scans, or a directory to move one heavy tenant, though a directory that is down takes everything down.

Sources: [Sharding](https://www.hellointerview.com/learn/system-design/core-concepts/sharding), [Scaling writes](https://www.hellointerview.com/learn/system-design/patterns/scaling-writes), [Robinhood](https://www.hellointerview.com/learn/system-design/problem-breakdowns/robinhood)

## Avoid scatter-gather

A query without the shard key asks every shard, so the slowest one sets its latency. Accept it for a rare admin report. On a common path, denormalise or precompute instead, or keep the fan-out cheap by merging a short top K from each shard.

Sources: [Sharding](https://www.hellointerview.com/learn/system-design/core-concepts/sharding), [Top-K](https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k), [Data modeling](https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling)

## Consistent hashing

Use a hash ring when nodes join and leave, or a client must reach the server that holds its state. A change then moves only a neighbour's share of keys, where hash modulo N moves almost all. Skip it when the node count never changes, or a managed cluster already routes keys for you. Add virtual nodes, or a failed node dumps its load on one neighbour. During a resize, clients reconnect and state must move. An even spread of keys still leaves one popular key on one node.

Sources: [Consistent hashing](https://www.hellointerview.com/learn/system-design/core-concepts/consistent-hashing), [Redis](https://www.hellointerview.com/learn/system-design/deep-dives/redis), [Online chess](https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-chess)

## Hot partitions and hot keys

First ask whether the shard is hot for reads or for writes. Read-hot data gets copies or a cache in front (see [caching](caching.md)). Write-hot data that can be summed splits into sub-keys that readers add up, which costs every read a merge and loses per-key order. If the cause is a bad key, not popularity, change the key.

Sources: [Scaling writes](https://www.hellointerview.com/learn/system-design/patterns/scaling-writes), [Kafka](https://www.hellointerview.com/learn/system-design/deep-dives/kafka), [Discord](https://www.hellointerview.com/learn/system-design/in-the-wild/discord-messages-scylladb)

## Partition by region

When most interactions are local, give each region its own stack with servers next to their data. Do not split users who routinely act across the globe. Searches near a boundary must query both sides.

Sources: [Networking essentials](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials), [Uber](https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber), [Gopuff](https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff)

## Split services by load shape

Make a path its own service only when its volume or cost differs sharply from the rest. On a small system the split is pure overhead. Keep a must-not-drop write path apart from bursty heavy reads.

Sources: [Bitly](https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly), [Online auction](https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-auction), [Yelp](https://www.hellointerview.com/learn/system-design/problem-breakdowns/yelp)

## Push work to the client

Let the device buffer or filter work when it can do so safely. Never trust it with clocks or prices. Delete local copies only after the server confirms, and do not assume one device per user.

Sources: [Strava](https://www.hellointerview.com/learn/system-design/problem-breakdowns/strava), [Uber](https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber), [WhatsApp](https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp)

## Cheap check first

When most candidates fail a costly check, run a cheap bound first and send only survivors on. In an exact search the bound must never drop a real match, and its answer is never the result. A learned first stage, as in a model cascade, does drop some, so it caps recall and needs watching on its own (see [ml-systems](ml-systems.md)).

Sources: [Gopuff](https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff), [Spell checker](https://www.hellointerview.com/learn/ai-coding/problem-breakdowns/spell-checker), [Bot detection](https://www.hellointerview.com/learn/ml-system-design/problem-breakdowns/bot-detection)
