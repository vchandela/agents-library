# Numbers that change a design

Ask first which choice a number would change, such as one database or several shards. If none, skip the maths and build the simple version.

## Estimate only to make a choice

Estimate only at a real fork, such as shard or not, or a queue or a direct write. Skip it when real traffic or a load test exists, because measured numbers beat every figure here (see [engineering-principles](../engineering-principles.md)). Design for the peak. Take the peak factor from your own traffic shape, because lessons range from 10 to 100 times the average, and a factor means something only when it comes from a real event, such as a known campaign. Read-to-write ratios run from about 10 to 1 up past 100 to 1 for feeds, and near 1 to 1 a cache gains little. Keep every figure's unit straight, per core, per node or per partition.

Sources: [Delivery](https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery), [Numbers to know](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know), [Scaling reads](https://www.hellointerview.com/learn/system-design/patterns/scaling-reads)

## One relational node

One tuned Postgres node takes about 10k to 20k simple writes a second and up to about 50k indexed reads. Managed engines store up to about 64 TiB. Past about 100M rows, think about table partitioning, but treat it as a soft signal. Lessons put the shard trigger anywhere from 10k to 50k sustained writes, or from tens to hundreds of TB. Below that, measure your node and try the fixes in [scaling-and-partitioning](scaling-and-partitioning.md) first.

Sources: [Numbers to know](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know), [Sharding](https://www.hellointerview.com/learn/system-design/core-concepts/sharding), [Postgres](https://www.hellointerview.com/learn/system-design/deep-dives/postgres)

## One cache node

One Redis node answers in under a millisecond and handles about 100k to 200k operations a second. It holds up to about 1TB of memory. A check that takes several operations, such as a rate limit, gets about 50k to 100k a second. Scale out near those limits, or when the hit rate drops below about 80% (see [caching](caching.md)). Size on both memory and operations, because either can run out first.

Sources: [Rate limiter](https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-rate-limiter), [Redis](https://www.hellointerview.com/learn/system-design/deep-dives/redis), [Numbers to know](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know)

## One app or connection server

An app server runs out of CPU first, so scale out when CPU stays above about 70% to 80%. A connection server runs out of sockets. Plan on tens of thousands of long-lived connections per host, even though tuned hosts have held 100k to about 2 million (see [real-time-updates](real-time-updates.md)). Use the low figure until you have measured.

Sources: [Numbers to know](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know), [WhatsApp](https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp), [Online chess](https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-chess)

## Queues and partitioned stores

Divide the rate by the per-partition ceiling to get the count (see [queues-and-streams](queues-and-streams.md)). A Kafka broker handles up to about a million messages a second, with messages under about 1MB. A Kinesis shard takes about 1MB or 1,000 records a second. A DynamoDB partition serves about 1,000 write units and 3,000 read units a second.

Sources: [Kafka](https://www.hellointerview.com/learn/system-design/deep-dives/kafka), [DynamoDB](https://www.hellointerview.com/learn/system-design/deep-dives/dynamodb), [Ad click aggregator](https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator)

## Disk and write engines

Disks favour sequential appends over random in-place updates. For the same work per write, an append-only store takes roughly ten times the writes of a B-tree database. Absolute figures depend on that work, so compare like with like. A B-tree copes with thousands of random writes and tops out near 100k. Past that, pick a [log-structured store](storage.md#log-structured-store-for-heavy-writes). Never compare a per-core figure with a per-instance one.

Sources: [Scaling writes](https://www.hellointerview.com/learn/system-design/patterns/scaling-writes), [Database indexing](https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing), [Time series databases](https://www.hellointerview.com/learn/system-design/deep-dives/time-series-databases)

## Latency by distance

Each dependent round trip pays the full distance again. Memory takes about 100ns and SSD about 0.1ms. A hop inside a zone is under 1ms, across zones 1 to 2ms, and across regions 50 to 150ms. Standard object storage takes tens of milliseconds per request, so a chain of reads costs more than the bytes. Under about 200ms feels instant, so one cross-region trip fits in a hot path but a chain of them does not.

Sources: [Numbers to know](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know), [Spotify data lake](https://www.hellointerview.com/learn/system-design/in-the-wild/spotify-data-lake-point-queries), [FB live comments](https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments)

## Storage sizing

Size data as rows times bytes, plus indexes and replicas, and it usually comes out smaller than feared. A few TB fit one node comfortably, and data that is rarely read again can move to a cheaper tier (see [storage](storage.md#age-out-old-data)). Files over about 10MB belong in object storage (see [large-files](large-files.md)). An index can grow nearly as large as its table. Throughput, not storage, is often the real limit.

Sources: [Bitly](https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly), [Numbers to know](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know), [Instagram](https://www.hellointerview.com/learn/system-design/problem-breakdowns/instagram), [Large blobs](https://www.hellointerview.com/learn/system-design/patterns/large-blobs)
