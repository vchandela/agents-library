# Queues and streams

Ask first whether each message is a job that one worker must finish, or an event that several readers need, maybe again later. Jobs belong in a job queue, and events belong in a log stream.

## Queue as a buffer

Put a queue in front of work that comes in bursts and may finish after the response, which then promises "received", not "done". Skip it when the direct write is cheap and keeps up (see "Every complexity earns its place" in [engineering-principles](../engineering-principles.md)). A queue absorbs bursts only. Once a backlog forms every request waits behind it, so keep it off any path with a strict latency target. Bound its depth and decide what happens past the cap, such as a clear busy error or shedding low-priority work. Autoscale on depth, because CPU lags the backlog. An abusive caller should hit a [rate limit](api-and-edge.md) instead.

Sources: [Key technologies](https://www.hellointerview.com/learn/system-design/in-a-hurry/key-technologies), [Robinhood](https://www.hellointerview.com/learn/system-design/problem-breakdowns/robinhood), [Long-running tasks](https://www.hellointerview.com/learn/system-design/patterns/long-running-tasks)

## Job queue choice

Default to a managed queue such as SQS for independent jobs, because retries, visibility timeouts and dead-letter queues come built in. Know its limits too: messages of about 1MB at most, a real bill at high volume, and no replay. Kafka alone makes a poor job queue. Its offsets mark a position, not a job. Postgres with [SKIP LOCKED](consistency-and-concurrency.md) suits modest volume, though you own the retries. Redis is fast but can lose recent jobs or run out of memory under a backlog.

Sources: [Long-running tasks](https://www.hellointerview.com/learn/system-design/patterns/long-running-tasks), [Slack job queue](https://www.hellointerview.com/learn/system-design/in-the-wild/slack-job-queue), [Web crawler](https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler)

## Log stream (Kafka, Kinesis)

Use a retained log when several consumers need the same events or must replay them after a bad deploy. It cannot delay single messages or hand out the next due job first. Set retention longer than your slowest recovery. Acked writes can vanish if producers wait only for the leader, and retries duplicate if producer idempotence is turned off, though it is on by default since Kafka 3.0.

Sources: [Kafka](https://www.hellointerview.com/learn/system-design/deep-dives/kafka), [Slack job queue](https://www.hellointerview.com/learn/system-design/in-the-wild/slack-job-queue), [Payment system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system)

## Partition key and ordering

Order holds only inside one partition. Key by the entity whose events must stay in order, and never ask for global order. Size the partition count with room to grow, since extra brokers help only when topics have enough partitions. A hot key overloads one partition (see [scaling-and-partitioning](scaling-and-partitioning.md)).

Sources: [Kafka](https://www.hellointerview.com/learn/system-design/deep-dives/kafka), [Payment system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system)

## Commit after the work is done

Delivery is at least once. Commit a message only after its durable side effect, and make the handler safe to run twice with an [idempotency key](consistency-and-concurrency.md). Committing on receipt loses work in a crash. After a few failed attempts, move the message to a dead-letter queue so one poison message cannot stall a partition or crash worker after worker. Fail a known permanent error at once. A dead-letter queue nobody watches is a silent failure (see "Errors never go silent" in [engineering-principles](../engineering-principles.md)).

Sources: [Kafka](https://www.hellointerview.com/learn/system-design/deep-dives/kafka), [Long-running tasks](https://www.hellointerview.com/learn/system-design/patterns/long-running-tasks), [Web crawler](https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler)

## Separate queues per traffic class

Give urgent work its own queue, workers and slice of any downstream quota when it shares a system with bulk batches. Shared workers still let the bulk starve it, and autoscaling cannot clear the backlog in seconds. The reserved capacity sits idle on purpose. Skip it when all work has the same urgency.

Sources: [Notification system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/notification-system), [Web crawler](https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler)

## Transactional outbox

When the app decides a business event happened, write the event row in the same transaction as the state change and let a relay publish it. Writing and then publishing loses the event on a crash. Give each event a stable ID, because the relay can publish twice.

Sources: [Change data capture](https://www.hellointerview.com/learn/system-design/deep-dives/change-data-capture), [Notification system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/notification-system)

## Change data capture

Read the database's change log when other stores keep rebuildable copies, such as a [search index](search.md) or a warehouse. A cache rarely needs it (see [caching](caching.md#invalidate-on-write)). A row change looks the same whatever caused it, so use an [outbox](#transactional-outbox) when the action depends on why. Alert on CDC lag, because it stalls quietly.

Sources: [Change data capture](https://www.hellointerview.com/learn/system-design/deep-dives/change-data-capture), [Payment system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system)

## Event sourcing

Store every change as an event only when you need state at any past point, as in a ledger. Plan schema changes and snapshots, or rebuilds grow slow.

Sources: [Key technologies](https://www.hellointerview.com/learn/system-design/in-a-hurry/key-technologies), [Patterns](https://www.hellointerview.com/learn/system-design/in-a-hurry/patterns)
