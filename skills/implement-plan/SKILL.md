---
name: implement-plan
description: Use when an approved plan exists and implementation is starting. Not for exploratory work with no plan, and not before the plan has been reviewed and approved.
---

# Implement a plan

Execute it precisely, completely, and in order. No shortcuts, no skipped steps.

Apply `references/engineering-principles.md` and `references/testing.md`. Before opening each PR, and again before each review round, run the "Self-review before anyone sees a design" sweep on every function the diff touches, and put its list in the review request. When a step builds a screen, follow the design-ui skill for that step, judged against `references/ui-quality.md`. When it reaches users, `references/shipping.md`.

The references this skill names rely on these, so read them in full too: `references/respect-human-attention.md` (what a reader's time is worth), `references/visuals.md` (charts, diagrams and the visuals checklist), `references/core.md` (the six core actions).

## Before writing any code

Read the entire plan. Build a mental model of what is being built, why each decision was made, and how the pieces connect.

**If anything is ambiguous or contradictory, stop and ask.** Do not assume.

**Start from a green baseline.** Run the full suite before the first change and write down what already fails. An inherited failure nobody recorded becomes a failure nobody can place later.

**Check the seams.** For every pair of steps where one produces something the next consumes (a name, a type, a file), check they agree. Raise each mismatch before starting.

## While implementing

Follow the plan's reasoning, not just its instructions. The reasoning is what tells you what to do at a point the plan did not anticipate.

**If you hit a decision the plan does not cover, stop and ask.** Do not improvise silently. Improvising silently is the failure this skill exists to prevent. Before asking, finish the work the answer cannot change; ask once, with your recommended answer; never end a turn on "next I will".

**Reread the step, not your memory of it.** What you remember is a summary; the plan has the exact values.

**Keep a progress file on a long plan.** One line per finished step: the step, the commits, the test command and what it returned. Context gets compacted; the file and `git log` do not. After a gap, trust them over your recollection.

## When the user said not to check in

Only for an unattended run the user explicitly asked for. A question becomes a ruling instead of a stall. Stop only for four things: something irreversible or destructive, something security sensitive, a side effect outside the working copy (a merge, a push to a shared branch, a publish), or a plan so broken that every path is a guess. Everything else: decide with the spec as the authority, and record `Ruling: what you decided, why, what it costs if wrong`. The final message lists every ruling, and every finding you chose not to fix.

## After each major step

Verify it works before moving on. State what you did, what you checked, what comes next, and what you left out on purpose: "skipped: retries; add when a timeout is measured." If the explanation is longer than the change, cut the explanation.

"Verify" means run something. A step you have not exercised is a step you have not finished.

Run the fast tier as you go and the full suite once, on the final head (`references/testing.md`, "The loop").

Start a long job once in the background, check that it started, then end the turn and let the completion notice wake you (`references/testing.md`, "Anti-patterns").

Read the real exit status. In `uv run ruff check . | tail -1 && git commit`, the `&&` tests `tail`, so a lint failure committed anyway; `grep -v` exits 1 when it prints nothing, so a push that worked looked like a failure. Check each command on its own line, or test its output, before chaining the next step.

## The standard

Production quality: clean, readable, explainable. If something feels wrong, say so.

Check your own diff before handing it on. A later review does not excuse an unchecked change.

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
- **Reply on GitHub only when the fix is clear and done in full.** Anything partial, deferred, rejected or a judgement call goes to the user first, as options with your pick, and the reply is posted only after they decide. The user tends to resolve a comment once it has a reply, so a reply posted without asking settles the question for them. Failure this prevents: a bot flagged a lookup that read every row on each poll, the author replied "left it, it's cheap", and the user would have asked for an index.
- **Never cut verification to save time.** Run the tests, the per-PR checks and a real-database run where the fix depends on it, however long it takes. Example: a savepoint fix that passed on SQLite was only proven by reproducing the bug on a throwaway Postgres container.
- **Stacks: apply `references/stacked-prs.md`.** Never a plain `--force` and never amend a pushed commit. The lease is only for a stack rebuilt onto a moved main, and every merge passes `references/stack-merge-check.sh` first.
- **A PR description** follows `references/engineering-principles.md`, "Pull requests". Write it with the `explain-simply` skill and keep only the final text.

## Done when

Every step in the plan is done or explicitly deferred with a reason, each was verified by running something, and every question you hit was asked rather than guessed. Any real-world test from `references/testing.md` has passed on the deployed system before you call it live.
