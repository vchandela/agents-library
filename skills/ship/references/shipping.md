# Shipping

## Before deploying

- **A diff that ships in more than one deployable unit names each one.** Map every changed file to the image, service or workflow that ships it. When there are two or more, the PR says each deploy and the safe order between them, or why any order is safe (no data or contract passes between them). Example: a fix to Pylon card reading changed the orchestrator (`deploy-app`) and the agent's Slack CLI (`deploy-agentcore`); the PR said neither, and a review bot flagged it.
- **A rollback plan exists before the deploy, not after.** It names the trigger (for example error rate over twice the baseline, or p95 up more than half), the exact steps, how long they take, and whether each migration can be reversed, checked rather than assumed.
- A feature flag, if used, has an owner and a removal date. Test both states. Never nest flags.
- Define "working" first: write the two to four questions someone on call will ask about this change. Every log line or metric added must help answer one.
- A critical finding from any review means no ship, unless the user accepts the risk in writing.

## A command the user runs

When a step needs the user's credentials (a Terraform plan or apply, a login, a write to production), hand over one line they paste after `!`, which works from any directory. It builds a fresh worktree of the exact commit at an absolute path in your scratchpad, sets every environment variable inline, runs any init quietly, and trims long output. Never assume a current directory, never send several lines, and never plan from the user's own checkout, which may hold local changes. The apply runs the plan file saved by that plan, so what the user approved is exactly what changes. Failure this prevents: a multi-line plan that assumed `deploy/terraform` as the current directory failed with "No configuration files" and cost the user a round (13 Nov).

Terraform, with the PR's resource as `-target` (drop `-target` only for a whole-root change, from main):

- Plan: `! git -C ~/code/acme-shop fetch -q origin pull/<N>/head && git -C ~/code/acme-shop worktree add -f --detach <scratchpad>/tf-<N>-<sha7> FETCH_HEAD && cd <scratchpad>/tf-<N>-<sha7>/deploy/terraform && export AWS_PROFILE=<profile> AWS_REGION=us-west-2 && terraform init -input=false >/dev/null && terraform plan -input=false -target=<resource> -out=tfplan | tail -40`
- Apply: `! cd <scratchpad>/tf-<N>-<sha7>/deploy/terraform && AWS_PROFILE=<profile> AWS_REGION=us-west-2 terraform apply -input=false tfplan`
- After main moves on, or for an untargeted plan: replace the fetch with `fetch -q origin main` and the ref with `origin/main`.
- An expired login shows as an SSO or credentials error. Prefix `aws sso login --profile <profile> && `.

Plan from the PR head only when the change must exist before the PR's code deploys (an IAM grant the new code needs), the branch contains current main for `deploy/terraform`, and the plan is targeted at the PR's own resources. Otherwise merge first and plan from `origin/main`, so the live state never runs ahead of main. Write the expected plan summary ("0 to add, 1 to change, 0 to destroy", and the resource) next to the command, so the user can check it at a glance. Delete the worktree (`git worktree remove`) once the apply is confirmed live.

## A query against production

Every query against a production datastore carries a strict time limit. Production can't hang on an analysis.

- **A time limit, set first.** On Postgres, `SET statement_timeout = '60s'` at the start of the session, 60 seconds at most for analysis. A question that needs longer is bounded by ids or a time window, or answered from a sample.
- **The read-only login, never the master one.** That is the login the project's tunnel script defaults to, such as `app_readonly`, which already carries a 60 s timeout. `--admin` is only for a write the user approved.
- **An approved write is run by the user, from one line you hand over.** The master login's password sits in a secret, and secret reads aren't an agent's to make, so the agent never runs the write itself. Get the user's yes for the exact rows first, then hand over one line in the "A command the user runs" shape. It opens the `--admin` tunnel, sets the time limit, and runs `BEGIN READ WRITE`, the statement keyed by ids, a check that the affected row count matches, then `COMMIT`, or a rollback if the count differs. Afterwards, check the result yourself with a read-only query. Example: on 13 Nov the user, not the agent, ended the two blocking connections by hand.
- **Autocommit**, so no connection sits idle in a transaction holding locks.
- **No unbounded scans of big tables** such as `transcripts`. Filter by session ids or a time window before you join.
- **No analysis while a deploy or roll is in flight.** A startup migration needs a brief exclusive lock, and a long read blocks it.
- **Know how to cancel your own query.** Closing the client or the tunnel doesn't stop a query already running on the server. Before you start, know how to find its pid and `pg_cancel_backend` it, and check that it's gone afterwards.

Failure this prevents: on 13 Nov an over-cap analysis ran about 30 minutes on the master login through the tunnel. Its open transaction held AccessShare locks on `sessions`, and the new orchestrator failed its startup `ALTER TABLE` four times, leaving production on mixed versions until the user ended the connections by hand. The user's words: "every production query especially for testing should have strict time limits ... we can't hang prod".

## Several sessions, one main branch

- **Claim main before a push-bound full test run, and release it after the push.** The others hold until "released". Two full runs were lost in one day to a session landing first and forcing a rebase and rerun.
- **What sessions share on one machine (a test lock, a database, a connection pool) has an owner and an end.** The lock records who holds it and since when; the holder enforces a maximum hold; a waiter checks that the holder is making progress (CPU time, log growth), not only that its process exists; the lock is released on exit. A tool that only prints "ask the owner" turns one stuck run into an unbounded queue: one lock was held for about 87 hours by a hung script, and two test slots held 638 and 629 minutes against a 60 minute cap (clock time; the laptop may have slept). Keep the machine awake for a long run, and check for sleep before calling a stalled run hung.
- **A send is not a delivery.** When a notice says a message was dropped or held, carry its content in your next message to that peer or to the user, and set something to wake you to send it: one approval sat 8 h 34 min after a dropped send because nothing woke the sender.
- **Files every change must edit (version, changelog, lockfile, generated output, a date that must equal the merge day) are set or regenerated by whoever merges, at merge time, never hand-merged on each branch.** A per-branch number conflicts every other open branch at every merge: one author's branch carried five different version numbers in under two hours. Where a number must be chosen per branch, it follows push order, not the order work was claimed. Say once which approved change merges first and that nothing else merges before it.
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
