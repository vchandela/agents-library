---
name: implement-plan
description: Use when an approved plan exists and implementation is starting. Not for exploratory work with no plan, and not before the plan has been reviewed and approved.
---

# Implement a plan

Execute it precisely, completely, and in order. No shortcuts, no skipped steps.

Apply `references/engineering-principles.md` and `references/testing.md`. When the change has a screen, `references/ui-quality.md`. When it reaches users, `references/shipping.md`.

## Before writing any code

Read the entire plan. Build a mental model of what is being built, why each decision was made, and how the pieces connect.

**If anything is ambiguous or contradictory, stop and ask.** Do not assume.

**Start from a green baseline.** Run the full suite before the first change and write down what already fails. An inherited failure nobody recorded becomes a failure nobody can place later.

**Check the seams.** For every pair of steps where one produces something the next consumes (a name, a type, a file), check they agree. Raise each mismatch before starting.

## While implementing

Follow the plan's reasoning, not just its instructions. The reasoning is what tells you what to do at a point the plan did not anticipate.

**If you hit a decision the plan does not cover, stop and ask.** Do not improvise silently. Improvising silently is the failure this skill exists to prevent.

**Reread the step, not your memory of it.** What you remember is a summary; the plan has the exact values.

**Keep a progress file on a long plan.** One line per finished step: the step, the commits, the test command and what it returned. Context gets compacted; the file and `git log` do not. After a gap, trust them over your recollection.

## When the user said not to check in

Only for an unattended run the user explicitly asked for. A question becomes a ruling instead of a stall. Stop only for four things: something irreversible or destructive, something security sensitive, a side effect outside the working copy (a merge, a push to a shared branch, a publish), or a plan so broken that every path is a guess. Everything else: decide with the spec as the authority, and record `Ruling: what you decided, why, what it costs if wrong`. The final message lists every ruling, and every finding you chose not to fix.

## After each major step

Verify it works before moving on. State what you did, what you checked, what comes next, and what you left out on purpose: "skipped: retries; add when a timeout is measured." If the explanation is longer than the change, cut the explanation.

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
| "The tool or agent said it passed" | Run it yourself and read the output. |

## Review rounds on open PRs

Implementation rarely ends at the first push. Rounds of review feedback follow, and each round goes back to already-published PRs.

- **Read every comment before fixing any.** If one is unclear, ask about it before implementing the rest; they are often related.
- **Check each against the code before agreeing.** Does it break something, is there a reason for the current code, does the reviewer have the context? When asked to "do it properly", grep for callers first. If nothing calls it, propose deleting it.
- **Order:** what breaks or leaks first, then small fixes, then refactors. Test each one.
- **Answer with the fix, not with thanks.** "Fixed: X now does Y (`file:line`)." Reply in the comment's thread, not as a new top level comment.
- **Be pragmatic.** Fix what matters, and leave each minor you skip with a one-line reason. Do not chase every nit.
- **Never cut verification to save time.** Run the tests, the per-PR checks and a real-database run where the fix depends on it, however long it takes. Example: a savepoint fix that passed on SQLite was only proven by reproducing the bug on a throwaway Postgres container.
- **Never force-push, not even `--force-with-lease`.** When a stack has to be rebuilt (fixes folded into the PR they belong to, a rebase onto main), publish it as one merge commit per branch: the tree is the rebuilt, tested tip, the first parent is the remote head, and the second parent is the branch below. Every push is then a fast-forward, and each PR's diff stays its own.
- **A PR description says what the PR does now.** Run the last pass from `references/machine-tells.md` on it and keep only the final text. Fold a fix into the sentence it changes. Never append "review fixes" logs or fixed-in tables: review rounds keep coming, and the description stays for the reader who arrives later.

## Done when

Every step in the plan is done or explicitly deferred with a reason, each was verified by running something, and every question you hit was asked rather than guessed. Any real-world test from `references/testing.md` has passed on the deployed system before you call it live.
