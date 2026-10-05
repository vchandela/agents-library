---
name: diagnose-bug
description: Use when something is broken, throwing, failing, flaky or slow and the cause is not yet known, before proposing a fix. Not for a QA pass hunting new defects; that is qa-live-site. Not for reviewing someone else's diff; that is review-pr.
---

# Diagnose a bug

A loop first, a theory second, a fix last. A fix for a symptom is a guess that happened to pass.

Apply `references/testing.md` and `references/engineering-principles.md`.

## 1. Build the loop

Read the whole error and stack trace first, and check what changed: recent commits, dependencies, config, environment. Then take the first loop that reaches the bug:

1. A failing test at the seam where the bug shows.
2. A curl or HTTP script against a running instance.
3. A CLI call with a fixture input, diffed against a known good output.
4. A headless browser script that asserts on the page, the console or the network.
5. A captured real request, payload or log, replayed through the code path.
6. A bisect script, when it worked at one commit and not another (`git bisect run`).
7. A scripted person: numbered prompts for a human, answers captured as `KEY=value` lines.

Make it sharp (assert the exact symptom, not "did not crash"), deterministic (pin the clock, seed randomness) and fast. For a flaky bug, raise the failure rate (loop it 100 times, add load, narrow the timing window) until it fails often enough to work against.

**Done when** one command, already run, with its output shown, drives the real code path, asserts the reporter's exact symptom, and gives the same verdict every run. Write down the number it shows: the status, the wrong value, the exit code.

No such command, no theory. If you cannot build one, say what you tried and ask for an environment that reproduces it, a redacted capture, or permission to add temporary logging.

## 2. Reproduce, then shrink

Confirm the loop shows the failure the user described, not one nearby. Then cut inputs, callers, config and steps one at a time until removing any remaining piece turns the loop green.

## 3. Find where it breaks

- **Several components** (CI to build to deploy, API to service to database): log what enters and leaves each boundary, run once, and read which boundary first holds the wrong value.
- **Deep in a call stack:** trace the bad value backwards to where it was created. Fix there, not where it surfaced.
- **It works somewhere else:** list every difference between working and broken, however small. Do not decide in advance that one cannot matter.
- **Something appears during tests and no test owns it:** run the test files one at a time and check after each. The first one that creates it is the polluter.

## 4. Rank three to five hypotheses

Write them all before testing any; one alone anchors on the first plausible idea. Each states its prediction: "If X is the cause, changing Y makes the bug go away." Show the list to the user, who may know one is already ruled out.

## 5. Probe one variable at a time

- Debugger or REPL first, then logs at the boundaries that separate the hypotheses. Never log everything and grep.
- Prefix every debug line with one tag, for example `[DEBUG-a4f2]`, so cleanup is one grep.
- Never stack a second change on the first.

## 6. Fix the class, at the shared point

- Write the regression test first. If the only seam is too shallow to show the bug, write that down: it is a finding about the design, not a reason for a weak test.
- Grep every caller of the function you are about to change, and fix the shared function once. Then search for the same kind of mistake elsewhere: `references/engineering-principles.md`, "When it is a bug fix".
- One change, no "while I'm here" refactoring.
- Rerun the step 1 loop against the original, unshrunk case. The number has to move.

## Three failed fixes is a design problem

Count your fixes. After the third that did not hold, stop changing code. Each fix revealing a new problem elsewhere means an assumption or the structure is wrong, not the latest hypothesis. Name the assumption you are most sure of and check it directly, or bring the evidence to a person before a fourth fix.

## Report

State a cause only when the loop proves it. Otherwise write "cause not yet proven" and name the next check. When the cause is outside the code (timing, environment, a third party), list what you checked and add the logging that would catch it next time.

## Signals that you are guessing

| They say | It means |
|---|---|
| "Is that actually happening?" | You assumed without checking. |
| "Will it show us...?" | You should have added logging first. |
| "Stop guessing." | You proposed a fix without a cause. |
| "Still broken." (three times) | Stop iterating on code. Check an assumption. |

## Rationalisations to refuse

| The excuse | What to do |
|---|---|
| "I can see the bug in the code" | Build the loop anyway. Reading finds a bug, not necessarily this one. |
| "The ticket names the function" | The ticket names a symptom. Grep the callers. |
| "Several changes at once saves time" | You will not know which one worked. |
| "One more tweak" | After three, stop and check the assumption. |

## Done when

- [ ] The cause is written down with its evidence.
- [ ] The step 1 loop no longer reproduces the bug, and its number moved.
- [ ] A regression test fails without the fix and passes with it, or the missing seam is written down.
- [ ] The same kind of mistake was searched for, with what the search found.
- [ ] The debug tag greps to nothing; throwaway harnesses are deleted.
