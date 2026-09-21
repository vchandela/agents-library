---
name: write-spec
description: Use when someone wants to build something and the requirements are not pinned down yet. Interviews first, writes the spec after. Not for a task whose shape is already agreed, and not for writing the implementation plan.
---

# Write a spec

Interview until the shape is agreed. Only then write.

## Interview first

Ask questions one at a time. Cover implementation, interfaces, failure behaviour, tradeoffs, and what the user is actually optimising for.

**Do not ask obvious questions.** "What is the deadline" teaches nobody anything. Ask the questions whose answers would change the design: what happens when this is called twice, what happens when the upstream is down, which of these two costs matters more.

Keep going until you can state the system back and the user agrees. Then write the file.

## The spec

**Purpose.** One paragraph. What problem, for whom.

**Interface contract.** Every input: name, type, constraints, an example value. Every output: shape, type, and what partial success looks like. The entry points.

**Behaviours.** The happy path as numbered steps. Then every error case as a condition mapped to an exact behaviour: what is returned, what is logged, what is retried, what is skipped. "Handle errors gracefully" is not a behaviour.

**Invariants.** Things that must always be true, written as assertions. "X must never happen." "Y must always equal Z."

**Non-functional.** Idempotency, yes or no and why. Ordering guarantees, yes or no and why. What is atomic and what is not. Performance targets if they exist. What must be logged or measured.

## Done when

Every error case names an exact behaviour, every invariant is falsifiable, and the user has confirmed the spec back. Next: `write-plan`.
