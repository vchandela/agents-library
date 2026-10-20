# Caching

Every cache is a second copy of a fact, so it buys speed with a stale window and an invalidation job. Ask first which measured read path is too slow, and how stale its answer may be.

## Decide whether to cache

Cache a read that is expensive or repeated often enough to eat database CPU, and measure it first (see "Performance: measure, keep or revert" in [engineering-principles](../engineering-principles.md)). Skip a simple indexed lookup. Skip a value every write would invalidate, or an entry read too rarely to be hit again, such as one user's feed page in a shared cache, because the hit rate collapses. If the whole working set fits in one cache node at a fair price, cache all of it and skip any selective scheme. Otherwise cache what is read often, changes rarely and costs a lot to rebuild.

Sources: [Caching](https://www.hellointerview.com/learn/system-design/core-concepts/caching), [Numbers to know](https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know)

## Cache-aside

Cache-aside is the default. Read the cache, and on a miss read the database and store the answer. Use it when reads far outnumber writes and a short stale window is fine. Never cache a value that drives a correctness decision, such as stock or a balance. Read those from the database (see [consistency-and-concurrency](consistency-and-concurrency.md)). Write-through suits reads that must see the latest write, but it fills the cache with data nobody reads. Write-behind fits only writes you can afford to lose, never payments. A cache is not a system of record.

Sources: [Caching](https://www.hellointerview.com/learn/system-design/core-concepts/caching), [Redis](https://www.hellointerview.com/learn/system-design/deep-dives/redis), [DynamoDB](https://www.hellointerview.com/learn/system-design/deep-dives/dynamodb)

## Invalidate on write

When the writer knows which keys it touched, it deletes them after the commit, and a TTL clears anything it missed. Delete too early and a reader caches the old value again. When a change must show everywhere at once, build keys from a version bumped in the same transaction. A cache rarely needs the change stream, because the writer already knows its keys. Use it when writers you do not control share the rows, and alert when it lags past your bound.

Sources: [Scaling reads](https://www.hellointerview.com/learn/system-design/patterns/scaling-reads), [Meta ZGateway](https://www.hellointerview.com/learn/system-design/in-the-wild/meta-zgateway-zippydb), [Change data capture](https://www.hellointerview.com/learn/system-design/deep-dives/change-data-capture)

## Cache keys

A key must hold every input that changes the answer, such as tenant, viewer, locale or each search parameter. Miss one and the answer is wrong, not slow. Cached search results have no link back from a changed record, so they lean mostly on a TTL, with tags on entries when you must clear them by record.

Sources: [Connect Four](https://www.hellointerview.com/learn/ai-coding/problem-breakdowns/connect-four), [Ticketmaster](https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster)

## Stampede protection

Protect a popular key that is costly to rebuild when the database is sized far below cache traffic. Pick a per-key lock, early refresh or a background refresh before expiry, and add TTL jitter. Slow rebuilds strand waiters. When no stale answer is allowed, coalesce instead: identical requests in flight share one fetch and no copy is kept, so there is nothing to invalidate.

Sources: [Scaling reads](https://www.hellointerview.com/learn/system-design/patterns/scaling-reads), [Discord](https://www.hellointerview.com/learn/system-design/in-the-wild/discord-messages-scylladb)

## Hot keys

More nodes do not help one hot key, because it still lives on one node. Put a small in-process cache with a short TTL in front of it, the same tool you would use for flags and config that every request reads but that rarely change. If one node still cannot serve it, store a few copies under suffixed names and read one at random. A key hot for writes needs split keys instead (see [scaling-and-partitioning](scaling-and-partitioning.md)).

Sources: [Redis](https://www.hellointerview.com/learn/system-design/deep-dives/redis), [Scaling reads](https://www.hellointerview.com/learn/system-design/patterns/scaling-reads), [Distributed cache](https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-cache)

## Precompute into the cache

When the result is expensive, latency is tight and some staleness is fine, a job writes answers ahead so reads never compute. Skip it when the result space is too big, like arbitrary time ranges. Let entries outlive a late job, and make a stalled job alert (see "Errors never go silent" in [engineering-principles](../engineering-principles.md)).

Sources: [Top-K](https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k), [Metrics monitoring](https://www.hellointerview.com/learn/system-design/problem-breakdowns/metrics-monitoring)

## CDN

Use edge servers when many far-away users fetch the same bytes, since distance is the latency. Do not put per-user responses there, or anything that must change everywhere at once. Purges spread slowly.

Sources: [Scaling reads](https://www.hellointerview.com/learn/system-design/patterns/scaling-reads), [Caching](https://www.hellointerview.com/learn/system-design/core-concepts/caching)

## Survive a cache outage

If the database cannot take full traffic alone, plan for the cache to vanish. Shed load with a circuit breaker and fall back to a degraded mode. Otherwise the database falls too.

Sources: [Caching](https://www.hellointerview.com/learn/system-design/core-concepts/caching), [Core concepts](https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts)
