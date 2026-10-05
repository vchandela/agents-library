---
name: write-plan
description: Use when a spec exists and an implementation plan is needed before code is written. Not for writing the spec, and not for implementing the plan.
---

# Write an implementation plan

The agent implementing this has no background. Everything it needs goes in the plan.

Apply `references/engineering-principles.md`: DRY, YAGNI, KISS, SOLID, cut premature optimisation.

## Rules

- Every step is explicit and actionable.
- Explain the reasoning behind every non-obvious decision.
- When a step enforces something from the spec, say so: "This satisfies the invariant: X."
- Do not add steps that were not discussed. Do not drop ones that were.
- **Every assumption goes in the spec's open items**, not here. A step that changes under another pick says how.
- Verify every `file:line` and claim before publishing. Cut steps for work the platform already does.
- No shorthand.
- **Global constraints first.** A short section near the top lists every project wide requirement from the spec with its exact value (versions, limits, names, formats). Every step and every reviewer inherits it.
- **Each step is a vertical slice** that can be checked on its own, sized to fit one fresh session, with acceptance criteria, what is out of scope for it, and the steps that block it. A step with no open blockers can start now.
- **Each step names what it produces and consumes**: exact function names, signatures and paths a later step relies on. A later step calling `clear_layers()` when an earlier one defined `clear_full_layers()` is a bug in the plan.
- **Every command says what passing looks like.** `Run: pytest tests/test_x.py::test_y` then `Expected: FAIL, name 'y' is not defined`. The implementer compares, rather than judges.
- A step that will wait days before anyone picks it up names the interface and the behaviour it changes, not a line number, because lines move. A step done now keeps `file:line`.
- Every step uses an existing repo pattern and cites it. Anything new to the repo stays out of the plan until the user confirms it; list it under "needs sign-off".

## Teach the implementation

Apply `references/visual-explanations.md`. Prefer diagrams and real examples over prose. The plan must include a diagram showing the order of components or phases and a real-looking worked example. For any non-obvious new mechanism, show the relevant call order, state or data using the clearest visual form. Pseudocode is optional and secondary; use it only when the implementer still needs to see an exact check or ordering, mark it as pseudocode, and name the files that will contain the real implementation.

## Testing

Apply `references/testing.md`. Tests are steps in the plan, interleaved with implementation, not a cleanup phase at the end. If the spec has a real-world test, the last step runs it, run against the deployed system, and it gates announcing the change as live. If the change reaches users, the last steps are the rollback plan and the first-hour checks from `references/shipping.md`.

**Name the inputs nobody tested.** List up to five inputs or failure modes the spec implies but no planned test exercises (empty, duplicate, concurrent, partial failure, a user doing the reasonable unexpected thing), most likely first. Add a test for each to the step that owns the code. The spec's silence about an input is not permission for it to break.

## Grounding

Carry the spec's decisions forward as settled. Do not reopen a choice the spec made and the user confirmed; reference it.

Every step names the files it touches, with `file:line` for anything that already exists. Where the spec copies a repo precedent, the step points at the precedent's code so the implementer copies it rather than reinventing it.

## The document

Apply `references/respect-human-attention.md`: an "AI-assisted · human-reviewed" box at the top, steps collapsed to one line and a test, reference tables (spec coverage) collapsed. Anything that asks a reader to decide goes in the spec.

Same discipline as the spec. The user reviews it, then a teammate, before any code is written.

- Open with the order of work in a diagram, not a dense phase summary.
- Cluster by component, not by the order things came up in conversation.
- A small diagram per phase. Each step shows one line and its test; the rest is collapsed.
- Real diagrams and tables, not monospace text blocks.
- **Preview before every publish.** Apply `references/preview.md`. Not optional.
- Plain words in full sentences; cut fluff, not the words that make a sentence readable.
- On every revision, fold the change into the step it affects. Never append.
- Plain words, no em dashes.

## Folding in plan review

Vivek's instruction for review feedback: "be pragmatic in incorporating them". Treat each finding as a claim to check, not an order.

- Open every `file:line` the reviewer cites before accepting. On ARTM-309 a reviewer said a harvest prompt reads "20 incident threads"; the prompt only says "follow the most relevant threads one hop", so the plan said that instead.
- When a finding contradicts the repo's docs, the code wins. A CLAUDE.md line said each step owns its microVM; `server.mjs` showed a wave shares one, so the finding held. Report the stale doc line to the user as a separate one-line fix; don't fix it in this plan.
- Fold each accepted fix into the step it changes, then reply with one row per finding: accepted, modified or rejected, and what changed.

## Done when

The preview in `references/preview.md` passes. Every spec invariant maps to a step, every assumption is flagged, and the testing approach matches what the repo can actually do. No step decides nothing (TBD, TODO, "handle edge cases"). Names and types match across steps. The plan is not longer than the code it describes: a plan full of finished function bodies has written the code instead of deciding it. Next: `review-plan`, on a different agent. See `references/handoff-protocol.md`.
