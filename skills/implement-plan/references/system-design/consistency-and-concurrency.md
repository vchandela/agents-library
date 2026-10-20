# Consistency and concurrency

Ask first where the rule you protect lives. If it lives in a database, let the database enforce it, and if it lives in one process's memory, guard it with one lock.

## Consistency per feature

Decide for each feature whether a reader must see the latest write. Money and stock need strong reads, while feeds and analytics can be eventual. One model everywhere either oversells or slows everything. It fails when the cheap browsing path answers the critical question, or a failover during replication lag drops confirmed writes.

## Conditional write or version check

Put the rule into the write, as a row condition, a version check or a unique index, and try it first (see "Optimistic over pessimistic" in [engineering-principles](../engineering-principles.md)). When the app decides from what it read and clashes are common, lock the rows with SELECT FOR UPDATE, or use SERIALIZABLE when you can't name them. Lock in one order and keep payment calls outside the transaction. It fails when zero updated rows counts as success.

## SKIP LOCKED pool of unit rows

Store each unit or job as a row and let each transaction claim a free one with FOR UPDATE SKIP LOCKED. It suits buyers racing for identical stock, or workers claiming jobs, once one conditional update can't keep up. Decide how a background job refills the pool. The database still has a ceiling, so load test it.

## Reservation with expiry

When a hold outlasts a transaction, store it as a row with an owner and a deadline, checked in one short transaction. A Redis TTL fits only if the database still guards the final write. Set the deadline generously, or extend it when payment starts, and refund the loser if a payment still lands after the hold has gone.

## Redis lock to save work, not to guard data

A Redis lock stops two servers doing the same work when a rare double grant only wastes effort. A pause or a failover can grant it twice, so it never guards money or stock. Correctness stays in the database. No transaction spans Redis and a database, so keep every record a check depends on in one store, and prefer co-located data or a [saga](long-running-work.md) to two-phase commit.

## Idempotency keys

Give each operation a stable id whenever a retry could charge or send twice. Store it under a unique constraint and return the first result to duplicates. Keep keys longer than your longest replay path. For a send, check the key first and record it once the provider accepts, so a crash between the two risks a rare repeat rather than a lost message. For a charge, see [long-running work](long-running-work.md#side-effects-on-outside-systems).

## One owner per hot entity

When an entity is too hot for locks, change the problem first if you can. Otherwise send every update to one owner that applies them in order. How to route to the owner, and how it fails, is in [real-time updates](real-time-updates.md#route-each-key-to-one-owner-server).

## Merging concurrent edits

When many people edit one document, send small operations, not snapshots. Use operational transforms behind a central server, a CRDT for offline work, or last write wins per property. Rare conflicts, as in file sync, need only last write wins with saved versions. Transforms are hard to get right, and CRDTs keep growing.

The entries above cover distributed state, and the two below cover threads sharing memory in one process, where a short lock is cheap and the simplest correct lock wins.

## Check and act under one lock

Hold one lock from checking a value until you finish acting on it. An atomic is enough only when one value changes alone. Async code still races at each await. Start coarse and split only when contention is measured (see [engineering-principles](../engineering-principles.md)). Take locks in one order and keep slow work outside them.

## Bounded queue and workers

Hand work between threads through a fixed-size queue and decide what a full one does. Cap calls to a service with a semaphore and share costly objects through a pool. A semaphore bounds what is in flight, not a rate per second, so take a rate limit from [api-and-edge](api-and-edge.md). Work that must survive a crash needs a durable queue (see [queues-and-streams](queues-and-streams.md)). An unbounded queue grows until the process dies. Release in a finally block.
