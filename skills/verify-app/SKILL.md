---
name: verify-app
description: Use when an agent has changed a running app and must check its own work in the real thing, even when the app still has to be started or the repo opened, including driving a flow through the project's browser fixture, reproducing a finding as a test, or sweeping every page from a generated feature map. Not for an independent QA pass on a deployed site; that is qa-live-site. Not for reviewing a diff; that is review-pr. Not for finding an unknown cause; that is diagnose-bug.
---

# Verify the app change

The change is not done when the unit tests pass. It is done when the real app shows the change working, and the evidence is saved.

Apply `references/verifying-apps.md` in full. It holds the loop, the map rules, the CLI shape, the structural checks, the guard and the upkeep.

## Before the first run

Find the project's verification tooling: its generated feature map and its browser CLI (often `scripts/verify-app`). Read the project's own instructions for them. If the project has neither, say so and build the smallest pair that works before claiming anything is verified. A project with no way to drive the app has no end-to-end evidence, and that is a finding, not a reason to substitute a unit test.

Run `doctor` first. It proves the app boots, the test auth produces a session, the browser is present and the database host is local. Do not continue past a failed doctor.

## The loop

1. Build one piece.
2. Open the real route through the CLI, authenticated as the fixture user.
3. Observe the screen, the console, the network trace and the numbers. Save the screenshot and trace.
4. Fix the gap between what you saw and what the piece was meant to do.
5. Re-run the same observation on the same input and compare. The evidence has to move.

A fix with no second observation is a claim, not a verification.

## Sweep from the map

When the change touches shared layout, navigation or a global style, open every page the feature map lists, at each width the product supports. The page list comes from the map, never from memory or a hand-written list. Run the structural self-check from the reference on each page and record the numbers.

## Every finding gets a test

Turn each finding into a test in the project's own suite, at the seam nearest the user, using the same fixture and auth. Watch it fail without the fix, then pass with it. A test that cannot go red is not the proof.

## Before and after

Same route, viewport, fixture and input. Keep both screenshots at named paths; record both sets of numbers. The comparison is the evidence the change did something, and that it did not break a neighbouring state.

## Done when

- [ ] `doctor` passed on the run that produced the evidence.
- [ ] Every changed route was opened in the real app before and after.
- [ ] A sweep from the generated map ran for any shared layout, navigation or style change.
- [ ] Structural numbers were recorded, not eyeballed.
- [ ] Each finding has a test that was seen red, then green.
- [ ] The production guard was in place and never bypassed.
- [ ] The map and CLI are current, and the captures are cleaned up.

Then hand the change to the independent reviewer. This skill is not that reviewer.
