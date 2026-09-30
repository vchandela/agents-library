---
name: implement-plan
description: Use when an approved plan exists and implementation is starting. Not for exploratory work with no plan, and not before the plan has been reviewed and approved.
---

# Implement a plan

Execute it precisely, completely, and in order. No shortcuts, no skipped steps.

Apply `references/engineering-principles.md` and `references/testing.md`.

## Before writing any code

Read the entire plan. Build a mental model of what is being built, why each decision was made, and how the pieces connect.

**If anything is ambiguous or contradictory, stop and ask.** Do not assume.

## While implementing

Follow the plan's reasoning, not just its instructions. The reasoning is what tells you what to do at a point the plan did not anticipate.

**If you hit a decision the plan does not cover, stop and ask.** Do not improvise silently. Improvising silently is the failure this skill exists to prevent.

## After each major step

Verify it works before moving on. State what you did, what you checked, and what comes next.

"Verify" means run something. A step you have not exercised is a step you have not finished.

## The standard

Production quality: clean, readable, explainable. If something feels wrong, say so.

You are not a code monkey. You are the last line of defence before this ships.

## Rationalisations to refuse

| The excuse | What to do |
|---|---|
| "The plan probably meant X" | Ask. A guess about intent is the thing that ships wrong. |
| "This step is obviously unnecessary" | Say why, out loud, and wait. It may be load bearing. |
| "I will verify at the end" | Verify now. At the end you will not know which step broke it. |
| "Close enough to what was asked" | It is not. Name the gap. |

## Review rounds on open PRs

Implementation rarely ends at the first push. Rounds of review feedback follow, and each round goes back to already-published PRs.

- **Be pragmatic.** Fix what matters, and leave each minor you skip with a one-line reason. Do not chase every nit.
- **Never cut verification to save time.** Run the tests, the per-PR checks and a real-database run where the fix depends on it, however long it takes. Example: a savepoint fix that passed on SQLite was only proven by reproducing the bug on a throwaway Postgres container.
- **Never force-push, not even `--force-with-lease`.** When a stack has to be rebuilt (fixes folded into the PR they belong to, a rebase onto main), publish it as one merge commit per branch: the tree is the rebuilt, tested tip, the first parent is the remote head, and the second parent is the branch below. Every push is then a fast-forward, and each PR's diff stays its own.
- **A PR description says what the PR does now.** Fold a fix into the sentence it changes. Never append "review fixes" logs or fixed-in tables: review rounds keep coming, and the description stays for the reader who arrives later.

## Done when

Every step in the plan is done or explicitly deferred with a reason, each was verified by running something, and every question you hit was asked rather than guessed. Any real-world test from `references/testing.md` has passed on the deployed system before you call it live.
