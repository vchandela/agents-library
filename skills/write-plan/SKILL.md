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
- **Flag every assumption you are making that was not explicitly decided.** These are what the review will go after first.

## Testing

Decide whether this repo can run automated tests before assuming a testing approach.

**If it can** (Python, Go, TypeScript, most application code): write the failing test before the implementation, make it pass, then refactor. Every invariant and every error case in the spec gets a test. Tests are steps in the plan, interleaved with implementation, not a cleanup phase at the end.

**If it cannot** (Terraform, Helm, shell): say so and say why. Substitute the closest real verification: `terraform plan` output review, a linter, a manual checklist mapped to the spec. Every invariant still maps to a verification step, even when that step is a person reading something.

## Done when

Every spec invariant maps to a step, every assumption is flagged, and the testing approach matches what the repo can actually do. Next: `review-plan`, on a different agent. See `references/handoff-protocol.md`.
