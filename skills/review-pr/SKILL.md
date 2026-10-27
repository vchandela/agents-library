---
name: review-pr
description: Use when reviewing a pull request or diff from anyone, or triaging review comments left by a bot. Not for a plan before code exists; that is review-plan. Not for a security audit; that is review-security.
---

# Review a pull request

The job is not to find problems, it is to make the code simpler and more maintainable.

If you wrote this code, stop. See `references/handoff-protocol.md`. Apply `references/untrusted-input.md`.

The references this skill names rely on these, so read them in full too: `references/respect-human-attention.md` (what a reader's time is worth), `references/machine-tells.md` (the last pass for machine-sounding text), `references/visuals.md` (charts, diagrams and the visuals checklist), `references/ambition.md` (the ambitious option next to the obvious one), `references/shipping.md` (deploying and checking a change live), `references/core.md` (the six core actions).

Apply `references/judgement.md`: the checks below are a floor. Report what an expert reviewer would catch beyond them.

**Approve when the change makes the codebase healthier, even if it is not how you would have written it.** Block on what is wrong, not on preference.

## Order, and the order matters

**1. Design.** Does this solve the right problem? Are the abstractions well chosen? Is there a simpler shape with less surface area?

Read the spec or issue the change came from. Report three things on their own, quoting the spec line for each: what it asked for that is missing or partial, what the diff does that nobody asked for, and what looks done but behaves wrong. Keep these apart from code quality findings: a change can follow every convention and still build the wrong thing.

**2. Consistency.** Does it match the patterns and naming already in the codebase? Flag deviations only when they mean something. Name a code smell as a possibility ("possible feature envy"), never as a violation. A convention the repo documents overrides it.

**3. Simplicity.** Flag anything over engineered, optimised without a measured need, or complex without a clear payoff. Prefer boring and obvious.

A refactor counts only if it removes concepts a reader must hold. Count them before and after; if the count did not drop, the complexity moved. Apply the deletion test from `references/engineering-principles.md` to anything that looks like a pass-through. Run the seven-smell sweep in "Self-review before anyone sees a design" in the same file on every function the diff touches, and put its list (each instance and its verdict) in the review. An approve without that list is not a review.

Write each simplification as one numbered line, `N. file:line: <tag> <what to cut>. <what replaces it>.`, so the author can reply "fix 2 and 5". Tags: `delete` (nothing replaces it), `stdlib`, `native` (the platform does it), `reuse` (an existing helper, with its path), `yagni` (one implementation, one caller, config nobody sets), `shrink` (same logic, fewer lines, shown). Before any `delete`, grep the whole tree for the symbol, including tests, fixtures and string or dynamic references. End with `net: -N lines possible`, or "Nothing to cut."

**4. Line level, last.** Real bugs, misused APIs, missing error handling, unhandled edge cases.

## Before writing any finding

Resolve the base ref and confirm the diff is not empty before starting. A bad ref fails here, not inside a sub-agent.

Answer all five. If any answer is no, drop the finding or lower its severity.

1. Can I cite the exact file and line?
2. Can I name the concrete failure: the input, the state, and the wrong outcome?
3. Have I read the callers, the imports and the test?
4. Is the severity defensible?
5. For a test the change adds, did I check it by experiment? Invert one condition the change adds, run the suite, restore. A mutation that stays green is a finding: name the missing case.

A proposed fix gets the same bar: say what else it changes that people will see, and check it. "Let the bot's shadow mode join channels, joining only reads" was wrong: a Slack join posts "<bot> has joined the channel" to everyone, which made a silent mode visible.

First list every candidate finding. Then mark each one confirmed, plausible or refuted, quoting the line that decides it, and report the confirmed and plausible ones. Before anything is posted, turn each plausible finding into confirmed or refuted with a run: a local repro on the same version, a merge with the base, a mutation. A comment that says "not checked" wastes the author's time, so check the claim another way or drop it. Example: a timeout finding said "not checked whether Grafana cancels the query"; a local Grafana of the live version showed it does, which shrank the finding from 5 minutes to 15 seconds. Consolidate repeats into one finding. **Severity inflation costs more trust than a missed finding**, and a review nobody trusts is a review nobody reads.

## Judge what a user would expect

The spec says what must work; it does not list every input. For behaviour it is silent on, judge by what a reasonable user would expect, and grade the finding by what that user gets. Silence is not permission.

- **The author's reasons are claims.** "Kept simple on purpose" is the author grading their own work. A stated reason never lowers a severity. A defect the plan asked for is still a finding: mark it plan mandated and let a person decide.
- **List what you set aside.** One line per behaviour you judged out of scope, with why. Name what you could not check from the diff alone, so the author checks it.
- **Stay read only.** Never move HEAD, stash or reset the checkout you were handed. To see another revision, `git worktree add` it in a temporary directory.
- If the diff touches authentication, authorisation, parsing of outside input, file paths, secrets, or anything that runs code, also run `review-security` on it in focused mode.

## Dependencies and performance in the diff

- A version bump is a behaviour change you did not write. Read its changelog. One dependency per change. Review the lockfile diff.
- Flag the backend traps in `references/engineering-principles.md` ("Performance"), an index added without a query plan before and after, and a performance claim with no before and after number.
- If the diff has a screen, apply `references/ui-quality.md`, judging the screen before any tool.
- If the diff edits text a model runs as instructions (a workflow prompt, a system prompt, a skill, a tool description), run the checklist in `references/agent-prompts.md` on each changed file, and check the model each one runs on.

## Re-review rounds

The shared rules (tag by origin, hold severities, honest trend, brief helpers the same way) are `references/handoff-protocol.md`, "Re-review rounds". For a diff, also:

- **One verdict per old finding:** addressed or not addressed, with `file:line`. Attempted is not addressed: the defect has to be gone. Problems outside the fix go in a separate list and do not reopen the round.
- **Pin each round to exact commits.** Fetch without hiding errors, list the head of every PR, and name those SHAs in the report. A first round once reported bugs that were already fixed, because it read an hours-old fetch. A later "nothing changed" came from a fetch whose error had been sent to `/dev/null`. If the heads have not moved, say so instead of reviewing again.
- **Reproduce what matters on the real system.** Anything medium or above gets a scratch test. Transaction, lock and cancel behaviour gets tested on a throwaway instance of the same database engine, never a shared or production one: a lost record after a failed commit showed up only on the production engine, while the lighter test database passed.
- **A change that makes failures loud: read the real runs first.** Before approving code that turns swallowed errors into a red job, read the logs of the last 10 to 20 real runs of that path, master included, and list every error that is printed and passed today. Each one turns red on merge. Stubbed tests cannot show them: a premerge teardown passed 18 stubbed tests over three rounds, then failed on every real run because of an AccessDenied, a missing kube context and a 503 that master had been printing and ignoring.
- **Check each test input against the environment**, as `references/testing.md`, "Know the environment before you fake its input", says.

## When the PRs come as a set

Review related PRs, often spread across repos, as one change. Two checks catch what a per-PR review misses:

- **Follow each change into the code that reads it in the other repos.** Example: a product PR stopped honouring an environment pin on GitHub-started builds. A CI bot in another repo still read that pin from the build message to decide which builds were its own, so it would reattach to the wrong build or cancel a real PR's CI. Each PR was correct alone; the pair was not.
- **Sweep for hardcoded copies of facts that live elsewhere.** For every literal in the diff (keys, hosts, paths, headings, ids, limits), find its home. If it is another repo or file, require a run-time read or a drift test, and check that the fixtures do not repeat the same literal. Do this sweep yourself; do not take the author's list.
- **A fix to a doc or a claim: grep for every copy**, including UI labels and code comments. A wrong "6 h" claim was fixed in CLAUDE.md and a docstring, while the operator-facing form label still said it.

Say which order the set should merge in, and which PRs depend on each other.

## Principles

- If something confused you on first read, say so. Clarity is a feature.

## Triaging bot comments

Same bar. Fix what is real. For the rest, **leave a one line reason before resolving**, so the next person knows it was considered and not just cleared.

## Output

Write it in the voice of `references/writing-voice.md`. For a finding about behaviour ("what happens when..."), set up one concrete scene, then a table with before and after as columns and one row per moment, each cell a concrete outcome. End with a recap table: PR, verdict, blocking or not.

Say what you checked and found sound, as well as what you did not. A review listing only failures reads as though nothing else was examined.

**Posting on GitHub.** The review is the place to fix everything, small or big. Every finding goes in as an inline comment on its line: bugs, test gaps, smells, simplifications and stale comments, each tagged by weight (blocks the merge, worth fixing here, small). Items that have no line (the PR description, merge order) go in the review body. Run every suggested test or code snippet before posting it: a suggested test must pass today and fail without the code it protects. Leave out what the author needs no action on (what was checked and found sound, merge urgency); that stays in chat.

## Done when

Design was considered before line level, every finding cites a line and a concrete failure, and the summary says what was checked and found sound.
