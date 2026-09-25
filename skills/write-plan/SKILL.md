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
- Every step uses an existing repo pattern and cites it. Anything new to the repo stays out of the plan until the user confirms it; list it under "needs sign-off".

## Teach the implementation

Apply `references/visual-explanations.md`. Prefer diagrams and real examples over prose. The plan must include a diagram showing the order of components or phases and a real-looking worked example. For any non-obvious new mechanism, show the relevant call order, state or data using the clearest visual form. Pseudocode is optional and secondary; use it only when the implementer still needs to see an exact check or ordering, mark it as pseudocode, and name the files that will contain the real implementation.

## Testing

Apply `references/testing.md`. Tests are steps in the plan, interleaved with implementation, not a cleanup phase at the end.

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

## Done when

The preview in `references/preview.md` passes. Every spec invariant maps to a step, every assumption is flagged, and the testing approach matches what the repo can actually do. Next: `review-plan`, on a different agent. See `references/handoff-protocol.md`.
