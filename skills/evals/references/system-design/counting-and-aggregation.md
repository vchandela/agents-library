# Counting and aggregation

Ask first how fresh and how exact each number must be. Exact, live and cheap rarely come together, and the answer picks the tool.

## Aggregate ahead of the read

When many readers want a costly number that may be a little stale, compute it in advance and let them fetch it. A `GROUP BY` over raw rows rescans everything per read. A batch job every few minutes is enough when minutes of lag are fine. Watch it as traffic grows, because a job that overruns its interval cascades. Serving the result from a cache is covered in [caching](caching.md).

## Windowed aggregation in a stream processor

Use a stream processor such as Flink only when counts per key must be fresh within seconds. A query polled every minute covers most needs, including alert rules (see "Every complexity earns its place" in [engineering-principles](../engineering-principles.md#every-complexity-earns-its-place)). Window by event time with a watermark for late events. Checkpoint state only when rebuilding it costs more than replaying the stream, since short windows can often just be replayed, and remember that exactly-once covers the processor's own state, not what it writes out. Build long windows from small tumbling buckets, since a long sliding window multiplies state. When counts drive money, recount raw events in a daily batch and let that batch result win, alerting on any mismatch (see [Errors never go silent](../engineering-principles.md#errors-never-go-silent)). More on streams lives in [queues and streams](queues-and-streams.md).

## Rollups at several resolutions

For long time ranges, keep raw data briefly and coarser summaries for longer, and let the query pick the resolution. Set the ladder from real query history. Store min, max, sum and count, never an average, because an average of averages is wrong. Percentiles need histogram buckets, spaced exponentially for skewed data like latency, and the error is as wide as the bucket.

## OLAP store or time-series store

The query shape decides the store, not the timestamps. Pick an OLAP store when users slice counts by many dimensions across millions of IDs. Pick a [time-series store](storage.md) when each query reads one or a few series over time. The limits of a time-series store, such as a question across every series and label cardinality, are in [storage](storage.md#time-series-database).

## Leaderboard on a sorted set

A Redis sorted set gives live top N and one player's rank in log time, where a B-tree can list rows in order but cannot cheaply say how far down one sits. The database stays authoritative and Redis may lag, so plan a rebuild. Cap the set only when you serve the top N alone, because a capped set cannot rank anyone outside it, and even millions of players fit in a few GB. Keep one set per time window. Rare filter mixes are computed on demand, and an approximate rank can come from counts per score bucket.

## Count-Min Sketch and top-K

For the most frequent items among billions of IDs, keep a small counter grid that never undercounts, plus a heap of the leaders. Estimate the distinct count first, because an exact heap on one machine may be enough. It needs leaders that win by wide margins. Keep it in checkpointed stream state rather than Redis, where sketch and heap drift apart and cannot be decremented for sliding windows.

## HyperLogLog

Use it to count distinct users or items in about a kilobyte, at a couple of percent error even for billions. Keep a real set when counts must be exact or the set is small. It is never exact.

## Bloom filter

Use one for "have I seen this?" when memory is tight and a false positive is acceptable. Prefer a hash table or an indexed column when either fits, because the saving is modest. A standard filter cannot remove items, fills up over time, and each false positive hides an item for good.
