# Shipping

## Before deploying

- **A rollback plan exists before the deploy, not after.** It names the trigger (for example error rate over twice the baseline, or p95 up more than half), the exact steps, how long they take, and whether each migration can be reversed, checked rather than assumed.
- A feature flag, if used, has an owner and a removal date. Test both states. Never nest flags.
- Define "working" first: write the two to four questions someone on call will ask about this change. Every log line or metric added must help answer one.
- A critical finding from any review means no ship, unless the user accepts the risk in writing.

## Several sessions, one main branch

- **Claim main before a push-bound full test run, and release it after the push.** The others hold until "released". Two full runs were lost in one day to a session landing first and forcing a rebase and rerun.
- A version number follows push order, not the order work was claimed. A lower number landing after a higher one sends the version backwards.
- After anyone else lands, rebase and run the whole suite again before pushing. A green run on the old base proves nothing about the new one.
- Never edit, rebase or rebuild a working tree while a test run is reading it; the result then describes no tree at all. Work on the next change in a second worktree.
- A conflict where both sides added at the same place is not resolved by joining the two hunks: a hunk boundary can fall inside a function. After every resolution, compile or parse each file it touched before continuing the rebase.
- Say which shared files a change touches when claiming, so a collision is a message rather than a conflict.

## A change to connections, caching or concurrency

- Run a burst against production before calling it done: tens of uncached requests at once, counting status codes. A pooled database engine passed 1,316 tests and still failed 1 in 10 production requests under a 40-wide burst; one command found it, and a revert proved it.
- Test with the driver production uses. A suite on a different database driver says nothing about pooling, prepared statements or timeouts on the real one.
- Make sure an unhandled exception still writes a log row and serves your own error page. An exception that escapes the logging middleware is an outage nobody records.

## The first hour after

1. The health check answers 200.
2. No new error types in error monitoring.
3. Latency has not regressed against the baseline.
4. The main user flow works, done by hand on the live site.
5. Logs are flowing and readable. Force one error and find it by its request id.
6. The rollback path is ready.

## Rolling out in stages

Where there is a staged rollout:

| Signal | Advance | Hold | Roll back |
|---|---|---|---|
| Error rate | within 10% of baseline | 10% to 100% above | over 2x |
| p95 latency | within 20% | 20% to 50% above | over 50% above |
| New client error types | none | under 0.1% of sessions | over 0.1% |
