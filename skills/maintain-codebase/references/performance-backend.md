# Backend performance

Find the slow thing with numbers, fix the bottleneck, and prove the fix with the same numbers. The measure, keep or revert loop is in the engineering principles, "Performance: measure, keep or revert"; this guide holds the targets and the database rules.

## The numbers that matter

| Measure | Healthy | Investigate | What it is |
|---|---|---|---|
| One statement on a page path, mean | under 10 ms | over 100 ms | a query a request runs |
| All database time for one page | under 50 ms | over 200 ms | the page's statements added up |
| p99 against mean | under 10 times | over 10 times | a plan that depends on parameters or on one large tenant |
| Slow query log threshold | 100 ms in production | | what gets recorded |
| Connection pool wait | none | any sustained wait | requests queueing for a connection |
| Timeouts and aborted queries | zero | any | a slow query that fails is still a failure |

These are starting targets: set yours from a measured baseline on your own data, and revisit them when the data grows by ten times.

## Find it in the statistics, not in the code

- Rank statements by total time, not by mean. A 2 ms query called 50,000 times costs more than a 500 ms report. In Postgres, `pg_stat_statements` gives calls, mean, max and total for each normalized query.
- Read the plan with `EXPLAIN (ANALYZE, BUFFERS)` on real parameters before changing anything. A sequential scan is right on a small table, or when the filter matches a large share of the rows.
- Log slow statements: `log_min_duration_statement` at 100 ms in production, lower while profiling.
- A warm number and a cold number are different numbers: a serverless function's first request pays a cold start, and a query's first run may pay a cold cache. Compare warm to warm and cold to cold, and say which one was measured.

## Indexes: add one for a query, never for a column

- Start from the plan. An index earns its place when it removes a scan the plan shows, or the sort of a result the query orders.
- Order the columns: equality first, then range, then sort. A composite index helps only queries on its leading columns.
- Cover the hot queries: a partial index (`WHERE status = 'open'`) for a small hot subset, an `INCLUDE` column for an index-only scan.
- Skip indexes on low selectivity. A filter returning roughly more than 5 to 10% of a large table usually scans faster than it indexes.
- Every index costs writes and storage. Drop indexes with zero scans over a representative window; a fresh index on a small table may simply be waiting for traffic.
- Tiny tables need no index: the planner scans them anyway.

## Foreign keys

- The database does not index the referencing side of a foreign key for you. Every foreign key column that is joined, filtered or reached by a parent delete gets its own index, or the check becomes a scan of the child table.
- In Postgres, a delete on the parent looks for children on an unindexed column with a full scan. Add the index in the same migration as the foreign key when the child table is large.
- A foreign key enforces correctness; the index makes it cheap. Very large write paths sometimes move the check into app code, which trades correctness for speed and needs a reason.

## Queries that lie about their cost

- N+1: one query per row. Batch with a join, or one `IN` list and a map. Count the queries a request runs in a test.
- `OFFSET` pagination over depth: use keyset pagination (`WHERE (sort_key, id) < (last_sort, last_id)`) with a `LIMIT` always.
- Counting large tables on every request: keep a maintained count or cache it, as the system-design toolbox puts it under counting and aggregation.
- An upsert on every page load (`ON CONFLICT DO UPDATE`): read first, write only when missing. A row rewritten on every request is a write where a read would do.
- A scan hidden in a function, a trigger or a view that runs per row.
- A cache key that omits an input the response depends on (viewer, tenant, locale) is a security bug before it is a performance bug.

## The pool is not the fix

- Raising the pool size moves the queue to the database. Find what holds connections: a long transaction, a leaked session, a client created per request.
- Serverless: use a pooler in transaction mode, and keep the app's own pool small, because each instance holds its own.
- A sustained pool wait is the finding; a bigger pool hides it.

## Tables that grow

- Logs, events and request rows need a retention window and a prune job, plus an index on time for the prune. Decide the window when the table is created.
- Every unbounded table becomes the slowest table eventually.

## Where the structure is decided

Storage choice, normalization, keys, constraints and caching are the system-design toolbox entries on storage and counting and aggregation. This guide only makes the queries and indexes on an existing structure faster. Page budgets on the client are in the frontend performance guide.
