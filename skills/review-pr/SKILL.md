---
name: review-pr
description: Use when reviewing a pull request, yours or someone else's, or when triaging review comments left by a bot. Runs in a fresh session so the review is not reading its own reasoning.
---

# Review a pull request

You are a staff engineer. The job is not to find problems, it is to make the code simpler and more maintainable.

If you wrote this code, stop. See `references/handoff-protocol.md`.

## Order, and the order matters

**1. Design.** Does this solve the right problem? Are the abstractions well chosen? Is there a simpler shape with less surface area?

**2. Consistency.** Does it match the patterns and naming already in the codebase? Flag deviations only when they mean something.

**3. Simplicity.** Flag anything over engineered, optimised without a measured need, or complex without a clear payoff. Prefer boring and obvious.

**4. Line level, last.** Real bugs, misused APIs, missing error handling, unhandled edge cases.

Most reviews start at step 4 and never climb out. That is why the order is written down.

## Before writing any finding

Answer all four. If any answer is no, drop the finding or lower its severity.

1. Can I cite the exact file and line?
2. Can I name the concrete failure: the input, the state, and the wrong outcome?
3. Have I read the callers, the imports and the test?
4. Is the severity defensible?

A proposed fix gets the same bar: say what else it changes that people will see, and check it. "Let the bot's shadow mode join channels, joining only reads" was wrong: a Slack join posts "<bot> has joined the channel" to everyone, which made a silent mode visible.

Report what you are more than eighty percent sure about. Consolidate repeats into one finding. **Severity inflation costs more trust than a missed finding**, and a review nobody trusts is a review nobody reads.

## Re-review rounds

When the same change is reviewed again after fixes, the reader needs to see what the fixes did, not a fresh list that looks like churn.

- **Tag every finding by origin:** **new** (code added since the last round), **caused by a fix** (a fix from the last round introduced it), or **old** (the code was already there last round).
- **Hold severities steady.** An old finding moves up a level only when the reviewer shows a new, concrete failure path. A fresh reviewer rating it higher is not enough. Otherwise keep last round's level.
- **Make the trend honest.** If the count of medium or major findings rises, say in one line whether that came from new code, from fixes, or from old code seen differently.
- **Brief helpers the same way.** When reviewer subagents do the digging, give them last round's severities and tell them to keep those levels unless they can show a new failure path.
- **Pin each round to exact commits.** Fetch without hiding errors, list the head of every PR, and name those SHAs in the report. A first round once reported bugs that were already fixed, because it read an hours-old fetch. A later "nothing changed" came from a fetch whose error had been sent to `/dev/null`. If the heads have not moved, say so instead of reviewing again.
- **Reproduce what matters on the real system.** Anything medium or above gets a scratch test. Transaction, lock and cancel behaviour gets tested on the real database: a lost record after a failed COMMIT only showed up on Postgres, and the SQLite suite passed.

## When the PRs come as a set

Review related PRs, often spread across repos, as one change. Two checks catch what a per-PR review misses:

- **Follow each change into the code that reads it in the other repos.** Example: a product PR stopped honouring an environment pin on GitHub-started builds. Artemis still read that pin from the build message to decide which builds were its own, so it would reattach to the wrong build or cancel a real PR's CI. Each PR was correct alone; the pair was not.
- **A fix to a doc or a claim: grep for every copy**, including UI labels and code comments. A wrong "6 h" claim was fixed in CLAUDE.md and a docstring, while the operator-facing form label still said it.

Say which order the set should merge in, and which PRs depend on each other.

## Principles

- Favour deleting code over adding it.
- No speculative abstraction.
- If something confused you on first read, say so. Clarity is a feature.

## Triaging bot comments

Same bar. Fix what is real. For the rest, **leave a one line reason before resolving**, so the next person knows it was considered and not just cleared.

## Output

Write it in the voice of `references/writing-voice.md`. For a finding about behaviour ("what happens when..."), set up one concrete scene, then a table with before and after as columns and one row per moment, each cell a concrete outcome. End with a recap table: PR, verdict, blocking or not.

Say what you checked and found sound, as well as what you did not. A review listing only failures reads as though nothing else was examined.

## Done when

Design was considered before line level, every finding cites a line and a concrete failure, and the summary says what was checked and found sound.
