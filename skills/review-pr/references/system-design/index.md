# System design toolbox

Find your problem as a plain question below, then open the entry it links. An entry for a tool says, in a few sentences of prose, when to use it, when not to, what it makes you decide and how it fails. An entry for a rule that always applies says so and says how it fails. Every entry links the lessons it came from. Read what it says about when not to use the tool and how it fails before you put the tool in a spec or a plan.

General rules (measure first, optimistic over pessimistic, errors never go silent, design the cleanup) live in [engineering-principles](../engineering-principles.md). The files here link to them rather than repeat them.

## Families

| File | Covers |
|---|---|
| [storage](storage.md) | Choosing a database, keys, indexes, history and retention |
| [caching](caching.md) | Cache-aside, invalidation, stampedes, hot keys, CDN |
| [queues-and-streams](queues-and-streams.md) | Job queues, logs like Kafka, ordering, outbox, CDC |
| [long-running-work](long-running-work.md) | Async jobs, retries, durable workflows, sagas, schedules |
| [consistency-and-concurrency](consistency-and-concurrency.md) | Contention, conditional writes, reservations, idempotency, in-process locks |
| [scaling-and-partitioning](scaling-and-partitioning.md) | When to scale out, replicas, shard keys, hot partitions |
| [real-time-updates](real-time-updates.md) | Polling, SSE, WebSockets, fan-out across servers, offline delivery |
| [search](search.md) | Text, geo and vector search, keeping an index in sync |
| [large-files](large-files.md) | Direct uploads, resumable uploads, chunked sync, streaming video |
| [counting-and-aggregation](counting-and-aggregation.md) | Counters, windows, rollups, top-K, sketches, metrics |
| [api-and-edge](api-and-edge.md) | API shape, trust, load balancers, rate limits, calling flaky services |
| [ml-systems](ml-systems.md) | Ranking funnels, embeddings, features, feedback loops, LLM serving |
| [code-structure](code-structure.md) | Where state lives in one process, and which algorithm fits a shape |
| [numbers](numbers.md) | When an estimate is worth doing, and orders of magnitude |

## Data and storage

| Your problem | Read |
|---|---|
| Rows reference each other and some writes must be all or nothing. What store do I start with? | [Relational database first](storage.md#relational-database-first) |
| Every read is one exact key at very high volume. | [Key-value store](storage.md#key-value-store) |
| How do I pick partition and sort keys in DynamoDB or Cassandra? | [Keys from the queries](storage.md#keys-from-the-queries) |
| Should I copy fields to make reads fast? | [Normalise first](storage.md#normalise-first) |
| Do I keep only the current value, or every change? | [Keep the history](storage.md#keep-the-history) |
| Data grows forever but reads hit recent rows. | [Age out old data](storage.md#age-out-old-data) |
| Should I estimate this at all? | [Estimate only to make a choice](numbers.md#estimate-only-to-make-a-choice) |
| Does one database node fit, or must I shard? | [One relational node](numbers.md#one-relational-node), then [One node first](scaling-and-partitioning.md#one-node-first) |

## Reads and load

| Your problem | Read |
|---|---|
| Many reads, few writes, and a little staleness is fine. | [Cache-aside](caching.md#cache-aside) |
| A popular key expired and every request is rebuilding it. | [Stampede protection](caching.md#stampede-protection) |
| One key or one shard gets most of the traffic. | [Hot keys](caching.md#hot-keys), [Hot partitions and hot keys](scaling-and-partitioning.md#hot-partitions-and-hot-keys) |
| Reads are outgrowing the database. What do I try first? | [Scale reads in order](scaling-and-partitioning.md#scale-reads-in-order) |
| One node can't take the writes. Which key do I shard on? | [Choose a shard key](scaling-and-partitioning.md#choose-a-shard-key) |
| Most candidates fail an expensive check. | [Cheap check first](scaling-and-partitioning.md#cheap-check-first) |

## Background and long-running work

| Your problem | Read |
|---|---|
| The work runs for minutes and the caller should not wait. | [Async job with status](long-running-work.md#async-job-with-status) |
| A worker can crash mid-job and the job must still finish. | [Visibility timeout and heartbeat](long-running-work.md#visibility-timeout-and-heartbeat) |
| Jobs need retries. SQS, Postgres, Redis or Kafka? | [Job queue choice](queues-and-streams.md#job-queue-choice) |
| A process waits on people, webhooks or timers for days. | [Durable execution](long-running-work.md#durable-execution) |
| An operation spans services and must finish or be undone. | [Saga](long-running-work.md#saga) |
| Something must run at a set future time. | [Scheduled and delayed jobs](long-running-work.md#scheduled-and-delayed-jobs) |
| Traffic spikes and the work can finish after the response. | [Queue as a buffer](queues-and-streams.md#queue-as-a-buffer) |

## Events and data flow

| Your problem | Read |
|---|---|
| Several consumers need the same events, or need to replay them. | [Log stream (Kafka, Kinesis)](queues-and-streams.md#log-stream-kafka-kinesis) |
| Events for one entity must stay in order. | [Partition key and ordering](queues-and-streams.md#partition-key-and-ordering) |
| A row change and its event must happen together or not at all. | [Transactional outbox](queues-and-streams.md#transactional-outbox) |
| A search index or warehouse must follow the database. | [Change data capture](queues-and-streams.md#change-data-capture) |

## Correctness under concurrency

| Your problem | Read |
|---|---|
| Two writers race for the last seat or the same balance. | [Conditional write or version check](consistency-and-concurrency.md#conditional-write-or-version-check) |
| A user holds something for minutes while paying. | [Reservation with expiry](consistency-and-concurrency.md#reservation-with-expiry) |
| A retry or a double click might charge or send twice. | [Idempotency keys](consistency-and-concurrency.md#idempotency-keys) |
| Many workers each claim a job, or buyers race for identical stock. | [SKIP LOCKED pool of unit rows](consistency-and-concurrency.md#skip-locked-pool-of-unit-rows) |
| Is a Redis lock enough to protect money or stock? | [Redis lock to save work, not to guard data](consistency-and-concurrency.md#redis-lock-to-save-work-not-to-guard-data) |
| Many people edit one document at once. | [Merging concurrent edits](consistency-and-concurrency.md#merging-concurrent-edits) |
| Threads check a value and then act on it in one process. | [Check and act under one lock](consistency-and-concurrency.md#check-and-act-under-one-lock) |

## Pushing updates to clients

| Your problem | Read |
|---|---|
| A few seconds of delay is fine. Is polling enough? | [Plain polling](real-time-updates.md#plain-polling) |
| Only the server sends, and it sends often. | [Server-sent events](real-time-updates.md#server-sent-events) |
| The event lands on a different server from the client's connection. | [Pub/sub to connection servers](real-time-updates.md#pubsub-to-connection-servers) |
| A client reconnects and must get what it missed. | [Event ids and gap detection](real-time-updates.md#event-ids-and-gap-detection) |
| Millions arrive at once for scarce stock. | [Waiting room for a flash crowd](real-time-updates.md#waiting-room-for-a-flash-crowd) |

## Search, files and counting

| Your problem | Read |
|---|---|
| I need word search or fuzzy names. Do I need Elasticsearch? | [Postgres search first](search.md#postgres-search-first) |
| How do I keep a search index in step with the database? | [Sync the index with CDC or an outbox](search.md#sync-the-index-with-cdc-or-an-outbox) |
| "Near me" over points that move every few seconds. | [Cell keys for moving points](search.md#cell-keys-for-moving-points) |
| Find similar items by meaning. | [Vector search in a store you run](search.md#vector-search-in-a-store-you-run) |
| Clients upload or download big files. | [Presigned URLs](large-files.md#presigned-urls), [Multipart, resumable upload](large-files.md#multipart-resumable-upload) |
| Users read counts over high-rate events. | [Aggregate ahead of the read](counting-and-aggregation.md#aggregate-ahead-of-the-read) |
| Live top N and "what is my rank". | [Leaderboard on a sorted set](counting-and-aggregation.md#leaderboard-on-a-sorted-set) |
| Distinct counts, frequent items or "seen before?" over huge sets. | [HyperLogLog](counting-and-aggregation.md#hyperloglog), [Count-Min Sketch and top-K](counting-and-aggregation.md#count-min-sketch-and-top-k), [Bloom filter](counting-and-aggregation.md#bloom-filter) |

## The edge and outside systems

| Your problem | Read |
|---|---|
| A request names a user, a price or a time. What must the server decide itself? | [Trust at the edge](api-and-edge.md#trust-at-the-edge) |
| One caller or tenant could flood the system. | [Rate limits and admission control](api-and-edge.md#rate-limits-and-admission-control) |
| A provider I call is slow or down. | [Calling dependencies that fail](api-and-edge.md#calling-dependencies-that-fail) |
| A list can grow without end. | [Pagination and bounded results](api-and-edge.md#pagination-and-bounded-results) |
| A step charges a card or calls a partner and may be retried. | [Side effects on outside systems](long-running-work.md#side-effects-on-outside-systems) |

## ML systems

| Your problem | Read |
|---|---|
| A few items from millions within milliseconds. | [Multi-stage retrieval and ranking](ml-systems.md#multi-stage-retrieval-and-ranking) |
| Great offline, worse in production. | [Training-serving consistency](ml-systems.md#training-serving-consistency) |
| The model shapes its own training data. | [Feedback loops and cold start](ml-systems.md#feedback-loops-and-cold-start) |
| Serve an LLM to many users on scarce GPUs. | [LLM serving](ml-systems.md#llm-serving) |

## Code inside one process

| Your problem | Read |
|---|---|
| Several booleans describe one status. | [Make invalid states unrepresentable](code-structure.md#make-invalid-states-unrepresentable) |
| Should this fact be stored, or computed from data I already keep? | [Derive or store a fact](code-structure.md#derive-or-store-a-fact) |
| Jobs with prerequisites on a fixed pool of workers. | [Dependency order and critical path](code-structure.md#dependency-order-and-critical-path) |
| Place items onto capacity-limited servers. | [Bin packing](code-structure.md#bin-packing) |
| Big-O looks right but the code is still slow. | [Containers that keep big-O honest](code-structure.md#containers-that-keep-big-o-honest) |

## Sources

Distilled in our own words from the [Hello Interview](https://www.hellointerview.com/learn) System Design, Low Level Design, ML System Design and AI Coding lessons. Each entry links the lessons it draws on. The lessons are worth reading in full for the reasoning behind each choice.
