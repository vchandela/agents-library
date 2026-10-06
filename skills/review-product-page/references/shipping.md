# Shipping

Applied by write-plan, implement-plan and qa-live-site, whenever a change reaches real users.

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
- Say which shared files a change touches when claiming, so a collision is a message rather than a conflict.

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
