# Technical index

Always loaded (`~/.claude/rules/tech-index.md`), so every rule below is in view while you design, plan, build or review. Each line is the rule itself; the file in brackets has the reasons and the examples. Open that file before you put the tool or the exception in a spec, a plan or a PR. Situation first, then the rule.

## Contents

- Before any design, plan or PR
- PRs and shipping
- Tests
- Data and storage
- Reads, caches and scale
- Background work, queues and events
- Concurrency and correctness
- APIs, the edge and outside systems
- Counting, search, ML and code shape

## Before any design, plan or PR

- Any claim about code, a system or a cost -> check it in this task and cite `file:line`; no citation, no claim [engineering-principles: evidence, no citation no claim]
- Adding a table, column, queue, setting, secret, service, route, file or flag -> list what already exists for the job and reuse it; new only with a `file:line` for why each candidate fails [engineering-principles: every new resource]
- Any recommendation or "why not X?" -> grep how the repo already does it and lead with that; anything new needs the user's yes [engineering-principles: repo conventions]
- A design that is only right for the inputs we expect -> change the mechanism so the bad case can't happen (constraint, atomic op, unique name); zero, one or infinity, never an arbitrary count [engineering-principles: correct by construction]
- A number (limit, timeout, cap, size, rate) -> it carries its source beside it, or it goes; first ask if a deadline or the data already bounds it [engineering-principles: no magic numbers]
- A name for a field, function, flag or file -> plain words a newcomer reads right; a yes/no reads as a question; one idea, one word [engineering-principles: names]
- The same fact in two places (code and DDL, two configs, a fixture repeating the code's value) -> one home; a copy needs a written reason or a drift test [engineering-principles: DRY]
- Two stored fields that can never disagree -> store one, compute the other; store both only when they truly diverge [system-design/code-structure: derive or store]
- Several booleans describing one state -> one status enum; a tagged union when a state carries data [system-design/code-structure: invalid states]
- Building now vs building general -> build only what's needed, behind one clean seam (a setting, a named field, one interface) [engineering-principles: simplest thing, built to extend]
- Long-term vs pragmatic -> long-term now if cheap and already run in the company (cite it); else pragmatic behind a seam, long-term written down [engineering-principles: long-term where cheap]
- Fixes piling onto one mechanism, or a long rule list -> stop patching; find the most direct way, often one rule or one existing fact [engineering-principles: question the mechanism]
- Before anyone sees a spec, plan or PR -> run the seven-smell sweep on every touched function, as a list with a verdict per instance [engineering-principles: self-review]
  1. a fact with two homes or a fallback copy; 2. one name, two meanings; 3. a comment the code contradicts; 4. a temporary piece with no removal step; 5. a fallback, default, retry, silent cut or `|| ""` with no cited failure; 6. an error path with no class; 7. the same snippet in several files
- A review request -> carries a "Principles check": one line per rule above that the change touches, each with its verdict and `file:line`
- A step in an agent workflow -> first ask if an existing step has the inputs and tools; add one only when none can [engineering-principles: fewest workflow steps]
- A step that waits on another (`depends_on`, run after) -> name the output it reads from that step, in the spec and the PR; a wait with no output read runs in parallel, because a wait without a reason is wasted latency [engineering-principles: fewest workflow steps]
- A lock, queue or serial step -> prefer optimistic work with a conflict check; a lock only when nothing else works, with its cost in time [engineering-principles: optimistic over pessimistic]
- Anything a change creates (file, branch, row, session, cache entry) -> say who removes it and when, and what a half-done or doubled run leaves [engineering-principles: wrong paths and cleanup]
- An error -> key (loses or corrupts something relied on): record a status where the data would be, log, alert through the repo's existing route; non-key: log with context [engineering-principles: errors never go silent]
- A bug -> offer the long-term fix and the pragmatic one with trade-offs, never a patch; grep for every other instance and fix at the shared point [engineering-principles: bug fix]
- Something feels slow -> measure a baseline first, change one thing, re-measure the same way; neutral is a revert [engineering-principles: performance]
- An automatic action that could hurt availability, data or debugging -> report it and let a person decide [engineering-principles: no risky automation]
- Validation at a trust boundary, data-loss handling, security checks, accessibility -> never cut for less code [engineering-principles: never cut]

## PRs and shipping

- Sizing a PR -> under about 200 lines of production code, atomic; bigger work is a stack of vertical slices; estimate before coding [engineering-principles: pull requests]
- A PR description -> what it does now, in explain-simply voice, each decision with a before/after example; Evidence and Merge danger paragraphs; no review-fix logs [engineering-principles: pull requests]
- Anything with a shape in a PR description (a table, a flow, a lifecycle, a boundary) -> draw it: Markdown table with every column and real example rows, Mermaid flowchart or stateDiagram, ASCII in a code block; one picture per idea, at most two sentences under it, nothing the picture already shows [engineering-principles: pull requests, visuals: page brevity]
- Stacked PRs -> each upper branch sits on the exact commits below; a merge commit carries nothing; run stack-merge-check.sh before every merge; lease only for a stack rebuilt onto a moved main [stacked-prs]
- Before a deploy -> a rollback plan with a trigger, steps and time; define "working" as the two to four questions on-call will ask [shipping: before deploying]
- After anyone else lands on main -> rebase and rerun the whole suite before pushing [shipping: several sessions]
- A change to connections, caching or concurrency -> burst production with tens of uncached requests and count status codes [shipping]
- The first hour after a deploy -> health 200, no new error types, latency at baseline, main flow by hand, logs readable, rollback ready [shipping: first hour]

## Tests

- Writing code -> red first (watch it fail for the right reason), least code to green, refactor only on green; a bug fix starts with a failing reproduction [testing: the loop]
- While building -> run the fast tier (tests that read what you changed, cheap whole-repo guards); the full suite once, on the final head [testing: the loop]
- Picking test kinds -> unit, integration, contract, live read-only, mutation, static checks, failure and concurrency, security refusals, unchanged behaviour, real-world; name which and why one is left out [testing: kinds]
- A test -> one user-recognisable scenario through the public entry point; fake only network, clock, randomness; expected values typed out [testing: fat tests]
- Before done -> mutation check: flip a constant, drop a branch, put the bug back; a test must fail each time [testing: mutation]
- Faking an input -> build it from the producer's code or a real captured value, not its comment [testing: know the environment]
- Changing what stored state means -> add a test that starts from the old shape [testing: anti-patterns]
- Waiting for something -> wait on the condition with a named timeout, never a guessed sleep; long jobs run in the background and the notice wakes you [testing: anti-patterns]
- Repo tests can't show it working for real users -> one real-world test replaying the original ask, written as action, input, expected, failure [testing: real-world]
- Saying "passes", "works", "fixed" -> name the command you ran this turn and what it returned [testing: a claim and its evidence]

## Data and storage

- Rows reference each other, some writes all-or-nothing -> start with Postgres (and its JSONB, text search, PostGIS) before any second store [system-design/storage: relational first]
- Every read is one exact key at very high volume -> key-value store; if you keep adding secondary indexes, Postgres fits better [system-design/storage]
- Picking keys -> write the main queries first and give each a key; a many-to-many link is one row per link, never an array in the parent [system-design/storage: keys from the queries]
- Copying fields to speed reads -> normalise first; copy only for a measured read path, ideally into a cache or view [system-design/storage: normalise first]
- Guarding data -> let the database do it with keys, NOT NULL, UNIQUE, CHECK, foreign keys; never key on names or emails; money as integer cents [system-design/storage: constraints]
- Someone may need to prove what happened -> store each change as its own row [system-design/storage: keep the history]
- Data grows forever, reads hit recent rows -> partition by time, drop whole partitions [system-design/storage: age out]
- An index -> one per column a main endpoint filters or sorts on; read the query plan first [system-design/storage: indexes]
- Should I estimate? -> only at a real fork; one tuned Postgres node takes about 10k to 20k writes a second [system-design/numbers]

## Reads, caches and scale

- A slow read -> scale in order: index, hardware, precompute, replicas, then cache and CDN; a read that decides a purchase goes to the primary [system-design/scaling-and-partitioning]
- Caching -> only a measured expensive read; cache-aside by default; never cache what drives a correctness decision (stock, balance) [system-design/caching]
- Cache invalidation -> the writer deletes its keys after commit, a TTL catches misses; the key holds every input that changes the answer [system-design/caching]
- A hot key or stampede -> in-process cache with short TTL, or a per-key lock or early refresh with jitter [system-design/caching]
- Sharding -> only when one node can't take the writes, data or reads even with replicas; hash by default; the key is near permanent [system-design/scaling-and-partitioning]
- A query without the shard key on a common path -> denormalise or precompute instead of scatter-gather [system-design/scaling-and-partitioning]

## Background work, queues and events

- Work takes more than a few seconds -> pending row, job on a queue, return the id; a worker or trusted event marks it done [system-design/long-running-work]
- A new raise or exit inside a loop a scheduler reruns from a cursor that moves only on success -> trace it to the top: the bad item fails the run only after the good ones are done, and a stuck run re-does only unfinished work, so neither what waits nor the cost per run grows while stuck [engineering-principles: errors never go silent]
- Retries -> make the operation idempotent first, back off with jitter, fail permanent errors fast, never retry an undiagnosed failure [system-design/long-running-work]
- Waits on people, webhooks or timers for days -> a durable workflow engine; activities need idempotency [system-design/long-running-work]
- An irreversible outside call -> write "in progress" first, "done" after; on retry ask the provider; pass an idempotency key [system-design/long-running-work: side effects]
- A job queue -> managed queue (SQS) by default; Postgres SKIP LOCKED for modest volume; not Kafka [system-design/queues-and-streams]
- Consuming messages -> commit after the durable effect, handler safe to run twice, dead-letter after a few tries and watch it [system-design/queues-and-streams]
- An event must follow a state change -> transactional outbox; never write then publish [system-design/queues-and-streams]
- Rebuildable copies (search index, warehouse) -> follow the change log (CDC) and alert on lag; never dual-write from app code [system-design/search, queues-and-streams]

## Concurrency and correctness

- A rule that must hold under concurrent writes -> put it in the write (row condition, version check, unique index); zero rows updated is a conflict, not success [system-design/consistency-and-concurrency]
- A retry could charge or send twice -> idempotency key under a unique constraint, return the first result [system-design/consistency-and-concurrency]
- A Redis lock -> only to save duplicate work, never to guard money or stock [system-design/consistency-and-concurrency]
- Threads in one process -> hold one lock from check to act; bounded queues; release in finally [system-design/consistency-and-concurrency]
- Consistency per feature -> money and stock read strong; feeds and analytics can be eventual [system-design/consistency-and-concurrency]

## APIs, the edge and outside systems

- A list endpoint -> capped page plus a cursor on the last id (or timestamp plus id), never offset [system-design/api-and-edge]
- Trust -> the server takes the user from the verified token, stamps times itself, looks prices up, checks the user may touch the record [system-design/api-and-edge]
- Calling a dependency that fails -> cap in-flight calls, a circuit breaker with a fallback, self-throttle with jitter on provider limits [system-design/api-and-edge]
- Rate limits -> counters in a shared store, run increment and expiry atomically, choose fail open or closed on purpose [system-design/api-and-edge]
- Status codes -> never 200 with an error flag; a POST that moves money needs an idempotency key [system-design/api-and-edge]
- Real-time updates -> plain polling when seconds are fine; SSE when only the server sends; WebSocket only for frequent two-way [system-design/real-time-updates]
- Large files -> presigned URLs straight to storage, the row marked done from the storage event, never the client's word [system-design/large-files]

## Counting, search, ML and code shape

- A costly number many readers want, slightly stale is fine -> compute ahead in a batch; a stream processor only for seconds-fresh [system-design/counting-and-aggregation]
- Rollups -> store min, max, sum, count, never an average [system-design/counting-and-aggregation]
- Search -> Postgres (tsvector, pg_trgm, PostGIS, pgvector) before a search engine; an engine is a derived index, never the database [system-design/search]
- An ML feature -> one value at training and prediction time, one shared code path, split by time [system-design/ml-systems]
- An ML metric with rare positives -> PR-AUC and recall at the threshold, a golden set the model never influenced [system-design/ml-systems]
- A class -> only for a noun that owns changing state or enforces a rule; data rules sit with the data's owner [system-design/code-structure]
- Variation along independent axes -> composition, not inheritance; an abstraction waits for its second implementation [system-design/code-structure]
