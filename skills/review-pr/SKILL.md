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

Report what you are more than eighty percent sure about. Consolidate repeats into one finding. **Severity inflation costs more trust than a missed finding**, and a review nobody trusts is a review nobody reads.

## Principles

- Favour deleting code over adding it.
- No speculative abstraction.
- If something confused you on first read, say so. Clarity is a feature.

## Triaging bot comments

Same bar. Fix what is real. For the rest, **leave a one line reason before resolving**, so the next person knows it was considered and not just cleared.

## Output

Say what you checked and found sound, as well as what you did not. A review listing only failures reads as though nothing else was examined.

## Done when

Design was considered before line level, every finding cites a line and a concrete failure, and the summary says what was checked and found sound.
