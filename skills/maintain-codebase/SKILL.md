---
name: maintain-codebase
description: "Use when the work is the repository's recurring health rather than a feature: a red CI run to triage, a suite with flaky tests, dead or unused code, stale feature flags or experiments, CI cost, a slow suite, a dependency or migration chore. Not for finding the cause of one failure; that is diagnose-bug. Not for reviewing a diff; that is review-pr. Not for a planned feature; that is implement-plan."
---

# Maintain a codebase

The work is a queue of small, provable changes. Every lane ends on evidence a person can check, and the change is one small commit or one draft pull request that a human merges. A maintenance change with no evidence is a guess with a green button.

Apply `references/engineering-principles.md`, `references/testing.md`, `references/verification.md` and `references/untrusted-input.md`. The references this skill names rely on these, so read them in full too: `references/core.md`, `references/judgement.md`, `references/respect-human-attention.md`, `references/visuals.md`, `references/ambition.md`, `references/performance-backend.md`, `references/performance-frontend.md`.

## The rules that hold every lane

- **One candidate, one change.** One cleanup per pull request, small enough for a reviewer with the project's context. A mixed PR cannot be reviewed or reverted in parts.
- **The check stays.** Never skip, loosen, narrow, retry to green or delete a test, a lint rule or a required job to make a lane pass. An exception is a written row with an owner and an expiry date, never a silent edit.
- **Never change live configuration.** Read the live configuration; propose the code change. A deploy or a console edit waits for a person.
- **Keep the safeguard.** A killswitch, a permanent fallback, an operational override and a rollback path are not dead code. If an object is marked permanent, a person decides, not this skill.
- **Evidence or stop.** "It looks unused" is not evidence. Name the command, the source or the log that proves the claim, and open the file when the source is a dashboard, a ticket or a chat thread. If the evidence is missing, say what is missing and stop.
- **Start small, then expand.** One area, one candidate, one reviewed PR, then the next. A whole-repository sweep is a report to prioritize, not a reason to skip the review.
- **A person merges.** Draft the change with its evidence; the merge, the deploy and any live configuration change are a person's decision.

## 1. Triage a red CI run

The job is to get the signal back, not to make the red go away.

1. Read the first failing job and its log, from the top, before the summary. Name the failing step, the error and the first line that differs from a passing run.
2. Ask what changed: the commits since the last green run, the dependency lock, the environment, a shared fixture or cache.
3. Reproduce it once, with the same command and input. If it cannot be reproduced, name what is different (the runner, a secret, a shared service) before changing anything.
4. It is the change? Hand the job, the failing test and the log to `diagnose-bug`. It is the environment? Name the cause and fix the environment. It is the suite? Go to lane 2.
5. Never rerun to green, skip the job or loosen the check. A red run a rerun fixed is a flaky test, and it is lane 2's work.

**Done when** the first failing job is named with its log, the failure is reproduced or the environment named, and the check is unchanged.

## 2. Clear flaky tests

Ask the agent: "Look at the recent CI runs and find the tests that fail intermittently. For each, find the smallest clear cause and open one small pull request. Stop at clear fixes for simple causes; leave the rest named."

- Measure the rate before touching the test: failures over runs, with the seed, the time and the runner where it failed. A test that failed once is a data point, not a flake.
- Look for the usual causes first: shared state between tests, a missing mock, a real clock, a port, an order dependency, a fixed sleep. `references/testing.md` has the list; fix the cause, not the timeout.
- A clear fix ends in one small PR with the rate before and after, and the suite run that shows it.
- No clear cause: quarantine the test with a row that names the test, the owner, the expiry date and the tracking issue, and keep the rate measured. Never a silent skip and never a retry plugin as the fix.
- The rule from `references/testing.md` stands: fix or delete a flaky test; never retry it green.

**Done when** the rate is measured, and the test has either a fix with a before and after or a quarantine row with an owner and an expiry.

## 3. Remove dead and unused code

Name the area and the validation criterion before searching. "Payments module, nothing in the last release calls it" is a criterion; "find dead code" is not.

- Sweep every kind of reference: imports and calls, templates, routes, config strings, reflection and dynamic names, schemas, cross-service consumers. A reference reached only by a string is still a reference; grep the string too.
- Read the sources that record use: past pull requests, team chat, the project tracker, production telemetry and profiles. A path behind a feature flag is not dead; it is lane 4.
- Delete in small PRs by area. Each deletion says why it is safe, in one line, and the reviewer has the project's context.
- A broad audit prompt can work with a strong model and a per-change explanation, but it is a source of candidates, not the proof. The proof is the reference sweep and the runtime evidence.
- Apply the deletion test in `references/engineering-principles.md`: a pass-through with no caller is still a decision someone made; check why before removing it.

**Done when** the reference sweep and the runtime evidence are in the PR, and every removed symbol has its one-line reason.

## 4. Retire stale feature flags and experiments

This is the lane where labels lie. Your feature-flag or experimentation platform is the live source of truth, whether it is a vendor product or an in-house service. A stale label, an old ticket or a code comment is a claim to check.

- Read the live configuration of each object: its value, its rollout, its last evaluation and its owner. A flag labelled stale may still be evaluating in production.
- Audit every project and inventory, not only the objects labelled stale. Old projects hide the expensive ones.
- Find indirect uses before removing anything: enums, constants, wrappers, aliases, schemas, dynamically assembled names and cross-service consumers. SDK fallbacks and local overrides do not prove a production path.
- Preserve production behavior, operational safeguards and killswitches. A permanent object, a security control or a rollback switch goes to a person with the evidence.
- Rank candidates by observed cost: production telemetry, profiles and CPU. Removing a hot check is worth more than a cosmetic rename.
- One small PR per cleanup, linking the object's page in the platform (a console URL, an API URL or an export) in the summary. Never modify live configuration as part of the cleanup.

Ask the agent: "Find dead code and finished experiments behind stale flags and configs in <projects>. Verify the live configuration, check git history and overlapping pull requests, preserve production behavior, operational safeguards and killswitches, and ignore SDK fallbacks and local overrides. Reconcile every production-referenced constant, find indirect uses through enums, constants, wrappers, aliases, schemas, dynamic names and cross-service consumers, and produce one small draft pull request per cleanup with the object's platform page linked. Do not change live configuration."

A whole-repository audit is the same work at a larger scope: group the verified candidates into parallel workstreams by owner and file, with the production value, the evidence and the observed evaluation or CPU cost, and let a person prioritize. Do not stop at a conservative shortlist; do not remove from a labelled list alone.

**Done when** the live configuration was read, the indirect-use sweep is in the PR, the safeguard list was checked, and the platform page is linked.

## 5. Reduce CI and suite cost

Ask the agent: "What ideas do you have to relieve CI load in this repository? List the ideas in a table, ranked by estimated CI minutes saved per day based on this repository's own CI run history."

- Measure the before: the median and the 90th percentile CI time, the slowest jobs, the number of runs. The same command produces the after.
- A slow suite often has a missing mock, a real network call or a shared setup done per test. Fix the cause and keep every test; a deleted test is a quality change, not a speed change.
- The coverage floor stays. Do not widen timeouts, skip a job or cache a result that can go stale to make the number move.
- Apply `references/performance-backend.md` and `references/performance-frontend.md` when the cost is in the product, not the pipeline.

**Done when** the before and after are measured the same way, and no test or check was removed.

## 6. Dependencies and migrations

- One dependency or one migration per PR. Read the changelog for the exact version range, not the release notes of the latest version alone.
- Run the suite against the new version; name the rollback (the previous pin, the down migration, the backup). A dependency with a security fix goes to `review-security` as well.
- A migration states its lock, its expected duration, its backup and the deploy order. A migration that cannot be reversed needs a person's yes before it runs.

**Done when** the changelog quote, the suite result and the rollback are in the PR.

## What to hand off

- One failing test or one bug whose cause is unknown: `diagnose-bug`.
- A vulnerability in a dependency or a trust boundary: `review-security`.
- A feature the cleanup reveals: `implement-plan`, with the user's decision.
- Whether this practice is working: `evals`, with a case from the real maintenance run.

## The draft change

The PR body states what was found, the evidence command and its output, what changed, the risk, the rollback and what was not checked. One picture (a table of the candidates with their evidence and verdict) is enough; the code and the sweep are the rest. A reviewer with the project's context reads it cold.

## Rationalisations to refuse

| The excuse | What to do |
|---|---|
| "It looks unused" | Sweep the references and the runtime evidence. Look is not a check. |
| "The flag is labelled stale" | Read the live configuration and the last evaluation. The label is a claim. |
| "A rerun made it pass" | That is a flaky test; measure the rate and fix or quarantine it. |
| "The test is slow, so delete it" | Fix the cause; a deleted test hides a real defect. |
| "The upgrade is small" | Read the changelog for the range and run the suite. |
| "It is only one check" | The check is the product's safety; a weakened gate is a change nobody approved. |
| "The whole repo audit found it, so it is safe" | The audit found candidates; the reference sweep and the review are the proof. |

## Done when

- [ ] One lane, one small change, and the evidence command named with its output.
- [ ] No check, test, timeout or job was skipped, loosened or deleted; no live configuration was changed.
- [ ] The safeguard and killswitch list was checked.
- [ ] A human with the project's context can review the change from its body.
- [ ] What was not checked is written down.
