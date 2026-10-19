# Storage

Ask first which reads and writes the product does most, and which rows must change together. Start from a relational database and make every other store argue its way in.

## Relational database first

Use Postgres when entities point at each other and some writes must be all or nothing. Try its JSONB, text search and PostGIS before adding a second store. A document database earns its place only when the schema changes often, the data nests deeply, or records of one kind differ widely in shape. Before sharding, check the ceiling in [numbers](numbers.md#one-relational-node) and the cheaper fixes in [scaling-and-partitioning](scaling-and-partitioning.md) first.

Sources: [Data modeling](https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling), [Key technologies](https://www.hellointerview.com/learn/system-design/in-a-hurry/key-technologies), [Postgres](https://www.hellointerview.com/learn/system-design/deep-dives/postgres)

## Key-value store

Pick a key-value store such as DynamoDB when every read is one key, or one key plus a range. If you keep adding secondary indexes for new queries, Postgres fits better. It fails when load piles onto a few keys, and its global secondary indexes are only eventually consistent. Check the per-partition cost in [numbers](numbers.md#queues-and-partitioned-stores) before using it for hot counters.

Sources: [DynamoDB](https://www.hellointerview.com/learn/system-design/deep-dives/dynamodb), [Data modeling](https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling)

## Keys from the queries

In a partitioned store the keys decide which queries are cheap. Write the main queries first and give each a key, such as owner plus time. A many-to-many link gets one row per link and a reverse index, never an array in the parent. Any unplanned query becomes a full scan. A key that grows forever needs a time bucket, though everyone still reads the newest one (see [scaling-and-partitioning](scaling-and-partitioning.md)).

Sources: [Core concepts](https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts), [Cassandra](https://www.hellointerview.com/learn/system-design/deep-dives/cassandra), [Discord on ScyllaDB](https://www.hellointerview.com/learn/system-design/in-the-wild/discord-messages-scylladb)

## Log-structured store for heavy writes

Use an LSM store such as Cassandra when writes far outnumber reads and arrive as small appends keyed by one entity. Avoid it when you need transactions, strict consistency or rich queries. Heavy overwrites and deletes are cheap to write but leave compaction work and tombstones, and it fails when compaction falls behind and reads slow down. Write rates against B-tree stores are in [numbers](numbers.md#disk-and-write-engines).

Sources: [Cassandra](https://www.hellointerview.com/learn/system-design/deep-dives/cassandra), [Discord on ScyllaDB](https://www.hellointerview.com/learn/system-design/in-the-wild/discord-messages-scylladb), [Database indexing](https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing)

## Time-series database

Use one for numeric samples per series, read by narrow time ranges. Timestamps alone are not a reason. A question across all series, such as top K over millions of IDs, becomes a scan and belongs in [counting-and-aggregation](counting-and-aggregation.md). Cap label cardinality, because a user ID label multiplies series by millions and the index runs out of memory.

Sources: [Time series databases](https://www.hellointerview.com/learn/system-design/deep-dives/time-series-databases), [Metrics monitoring](https://www.hellointerview.com/learn/system-design/problem-breakdowns/metrics-monitoring), [Top K](https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k)

## Indexes

Add an index for each column a main endpoint filters or sorts on, and read the query plan first (see [engineering-principles](../engineering-principles.md)). A composite index helps only queries on its leading columns. Every write updates every index, so skip them on write-heavy tables that are rarely read.

Sources: [Database indexing](https://www.hellointerview.com/learn/system-design/core-concepts/db-indexing), [Postgres](https://www.hellointerview.com/learn/system-design/deep-dives/postgres)

## Normalise first

Keep each fact in one place, and copy data only where a measured read path needs it, ideally into a cache or view (see [caching](caching.md)). Audit logs and read indexes can start denormalised. A copy that misses one update stays quietly wrong, which is often worse than the slow join.

Sources: [Data modeling](https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling), [Core concepts](https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts)

## Keys, IDs and constraints

Let the database guard data with generated keys, NOT NULL, UNIQUE, CHECK and foreign keys. Never key on emails or names, which change. Rows ordered by time need a sortable unique ID such as UUID v7, because timestamps collide. Store money as integer cents, since floats drift. Every constraint costs a little on each write, and at very large scale some teams move foreign key checks into app code.

Sources: [Data modeling](https://www.hellointerview.com/learn/system-design/core-concepts/data-modeling), [DynamoDB](https://www.hellointerview.com/learn/system-design/deep-dives/dynamodb), [Robinhood](https://www.hellointerview.com/learn/system-design/problem-breakdowns/robinhood)

## One database or several

Start with one shared database, because transactions and joins stay simple. Split where shape, volume or consistency differ sharply. Keeping a service's data private is a real gain too, but weigh it against the joins and transactions you lose, because splitting coupled data leaves you needing distributed transactions. Size alone rarely forces a split (see [numbers](numbers.md#storage-sizing)).

Sources: [Instagram](https://www.hellointerview.com/learn/system-design/problem-breakdowns/instagram), [Numbers to know](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know), [Core concepts](https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts)

## Keep the history

Store each change as its own row when someone may need to prove what happened or rebuild state. One overwritten field leaves a bug no way back. Skip it only when nobody will ask about the past and the volume is huge, and even then keep enough to recover. Event sourcing is in [queues-and-streams](queues-and-streams.md).

Sources: [Payment system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system), [Online auction](https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-auction)

## Age out old data

When data grows forever but reads hit recent rows, partition by time and move old periods to a cheaper tier. Skip it when old data is read as often as new. Drop whole partitions instead of deleting rows, which causes vacuum pressure. Queries without a time filter still scan every partition.

Sources: [Postgres](https://www.hellointerview.com/learn/system-design/deep-dives/postgres), [Time series databases](https://www.hellointerview.com/learn/system-design/deep-dives/time-series-databases)
