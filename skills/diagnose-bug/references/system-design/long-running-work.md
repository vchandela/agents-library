# Long-running work

Ask first how long the work runs and what it waits on. Minutes of compute need an async job, while steps that wait on people, timers or outside systems need state that outlives any one process.

## Async job with status

When work takes more than a few seconds, write a pending row, put its ID on a [job queue](queues-and-streams.md) and return the ID at once. Keep it inline only when it finishes well inside the request timeout. The worker or a trusted event marks it done, never the client's word alone. Without a status record, failures vanish (see "Errors never go silent" in [engineering-principles](../engineering-principles.md)). A user cancel sets the record to cancelled through its own endpoint, and the worker checks between batches. A closed tab is not a cancel. Push updates are in [real-time-updates](real-time-updates.md).

Sources: [Long-running tasks](https://www.hellointerview.com/learn/system-design/patterns/long-running-tasks), [ChatGPT](https://www.hellointerview.com/learn/system-design/problem-breakdowns/chatgpt), [Dropbox](https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox)

## Worker placement

Run workers apart from the web servers. Functions suit short, spiky jobs. Pick containers for steady load, for jobs past the function time cap, and wherever a cold start breaks a start-time promise. Untrusted user code needs a sandbox with no network and a hard timeout.

Sources: [Long-running tasks](https://www.hellointerview.com/learn/system-design/patterns/long-running-tasks), [Job scheduler](https://www.hellointerview.com/learn/system-design/problem-breakdowns/job-scheduler), [LeetCode](https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode)

## Visibility timeout and heartbeat

Let the queue hide a taken message while the worker keeps extending it, so a crash makes the job reappear. A central checker costs far more and can die itself. Set the interval to the longest delay users can bear before a dead job restarts. Too short marks live jobs dead during a pause and runs them twice, so every job must be idempotent.

Sources: [Job scheduler](https://www.hellointerview.com/learn/system-design/problem-breakdowns/job-scheduler), [Long-running tasks](https://www.hellointerview.com/learn/system-design/patterns/long-running-tasks)

## Retries with backoff and jitter

Retry brief failures after a growing delay with random jitter, so clients do not retry together. Make the operation idempotent first and fail permanent errors fast. Never retry to cover a failure nobody diagnosed (see "Every complexity earns its place" in [engineering-principles](../engineering-principles.md)). Circuit breakers are in [api-and-edge](api-and-edge.md).

Sources: [Networking essentials](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials), [Web crawler](https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler)

## Durable execution

Use a workflow engine when a process spans services and waits on a person, a webhook or a deadline for minutes to months. One async step needs only a job queue. A short linear pipeline can be stages with their own queues, which pays off when one step fails far more often than the rest. Store each stage's output and pass IDs. Once the flow branches or needs undo, hand-built chains scatter state across workers, and the engine wins. Workflow code must be deterministic, and every outside call becomes an activity with its own timeout and retry. Activities can still run twice after a crash, so they need [idempotency](#side-effects-on-outside-systems).

Sources: [Temporal](https://www.hellointerview.com/learn/system-design/deep-dives/temporal), [Multi-step processes](https://www.hellointerview.com/learn/system-design/patterns/multi-step-processes), [Web crawler](https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler)

## Scheduled and delayed jobs

Store each job with a due time. For minute precision, a cron over due rows is enough. For seconds, move jobs due soon into a delay queue, since polling the whole table every few seconds means huge queries. A big fan-out needs a progress record.

Sources: [Job scheduler](https://www.hellointerview.com/learn/system-design/problem-breakdowns/job-scheduler), [Notification system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/notification-system)

## Saga

When an operation spans services and must finish or be undone, run local steps that each carry an undo. In one database, a single transaction is simpler. Sagas everywhere hint at a wrong [shard key](scaling-and-partitioning.md). Undos fail too, so they need retries and a manual way out.

Sources: [Multi-step processes](https://www.hellointerview.com/learn/system-design/patterns/multi-step-processes), [Sharding](https://www.hellointerview.com/learn/system-design/core-concepts/sharding)

## Side effects on outside systems

Before an irreversible outside call, write a record marked in progress, and mark it done after. On retry, done means skip. In progress means ask the provider first, because a timeout says nothing about whether the other side acted. Pass an [idempotency key](consistency-and-concurrency.md) it echoes back. Exactly-once delivery does not exist, so aim for an exactly-once effect.

Sources: [Payment system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system), [Robinhood](https://www.hellointerview.com/learn/system-design/problem-breakdowns/robinhood), [Multi-step processes](https://www.hellointerview.com/learn/system-design/patterns/multi-step-processes)
