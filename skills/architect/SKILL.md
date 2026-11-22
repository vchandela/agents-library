---
name: architect
description: Use when a change spans call sites, such as a new or changed interface, type, schema or shared function that many callers depend on, including a new interface whose implementers do not exist yet, and the shape has to be chosen before an implementation plan, even when the work first looks like a migration or a refactor, or the repository is unfamiliar and reading it feels like the first step. Not for surveying how others solve it; that is research-prior-art. Not for the tactical plan once the shape is agreed; that is write-plan. Not for criticising a plan; that is review-plan.
---

# Architect a change that spans call sites

A design is not a plan. This skill settles the shape every caller will live with; `write-plan` turns the agreed shape into steps.

Apply `references/agent-prompts.md` for the candidate briefs and `references/engineering-principles.md` for the design floor. The references this skill names rely on these, so read them in full too: `references/handoff-protocol.md`, `references/shipping.md`, `references/core.md`, `references/testing.md`, `references/verification.md`, `references/respect-human-attention.md`, `references/visuals.md`.

## 1. Ground the brief

The brief is a set of facts, not a proposed solution.

- **The change in one sentence.** What will be true after it that is not true now.
- **Every call site, from a search.** Grep each name that changes, ask the type checker for references, read route and handler registrations. Write the list with `file:line`; a call site from memory is a call site that will break.
- **The constraints.** Compatibility with what exists, migration and deploy order, data that cannot be rewritten, the consumers outside this repo, the performance budget.
- **The why sources.** Git history, tickets, docs, incidents and monitors, as `understand-codebase` reads them. A design that ignores why the current shape won is likely to recreate the problem it solved.
- **What must not change.** Name the behaviour, contract or caller that is out of bounds, so a candidate cannot quietly widen the job.
- **The judge's tie-break order**, fixed before any candidate runs: call-site fit, then interface depth, then blast radius, then reversibility, then testability, then repo fit. The judge uses it only when two scores are equal.
- **The model and family** each candidate and the judge will run on, or the fact that only one family is available.

If the brief has an open question only the user can answer, ask it now, in one numbered list, with your recommendation. A candidate design built on a guess is a candidate built on the wrong problem.

## 2. Run independent candidates

Two or three designers work in parallel, each with the whole brief and no sight of the others. Use different model families where the setup allows, because two candidates from one family tend to share the same blind spot. At least one candidate is the ambitious option: the one that changes more of the shape if the evidence supports it, with its cost. Record the model and family each candidate ran on. If only one family is available, say so in the output and name what the missing cross-family check could not catch.

Brief each designer indirectly: the goal, the constraints, the tools and sources, the evidence path, the output shape, the return size (a file path or a token cap), and what it may decide alone (`references/agent-prompts.md`, Indirect prompts). Do not hand it a step script; the route is the work.

Each candidate returns a design package:

- the call-site sketch: before and after for every call site in the brief;
- the core types and public signatures, with one real call written out;
- what stays put, and why changing it is not worth the blast radius;
- the failure modes and the migration order;
- the red flags: every place a caller needs a cast, an optional flag, a wrapper, or knowledge of an internal detail.

No candidate sees another package. A candidate that asks a question gets the answer in the brief for everyone, not in a private side channel.

## 3. Cross-judge

A judge on a different agent, and a different model family where possible, scores every package against the same rubric before discussing any of them. Record the judge's model and family. The brief fixed the tie-break order before the candidates ran; the judge uses it only when two scores are equal. The rubric:

1. **Call-site fit:** how many callers change, and how mechanical each change is.
2. **Interface depth:** one call hides the mechanism, versus many knobs the caller must understand.
3. **Blast radius:** what breaks if the design is wrong, and how far the break reaches.
4. **Reversibility:** the cost of going back after the first slice ships.
5. **Testability:** the smallest test that proves a call site works, and whether it can go red.
6. **Repo fit:** the existing pattern it follows, cited `file:line`.

Scores carry reasons. The judge names one winner and what would change the verdict. A tie that the brief's tie-break order does not resolve is a failed judgement: ask the judge again with the order restated. The judge is a proposal to the user, not a decision; say where its reasoning is thin.

## 4. Sketch the call sites and types

This is the document the implementer will follow.

- A before-and-after row for every call site found in grounding. Re-run the search after the design, because a changed type reveals callers the first search missed.
- The exact signatures, with argument and return types, and one real call site written end to end.
- Every new name defined once, in the sense a newcomer reads right the first time.
- The states and errors the caller must handle, at the call site, not in a glossary.
- What the design deliberately does not do.

If a call site cannot be written without a workaround, the design is not finished. Fix the design before writing the plan.

## 5. Order the implementation

- **First slice:** move one real call site through the new shape, end to end, before converting the rest. It proves the design is buildable.
- **Second:** the call site most likely to disprove the design, because a wrong shape should fail early, not after ten mechanical conversions.
- Then the mechanical ones.
- Keep the main branch green at every step, with the expand-contract or parallel-run pattern the repo already uses.
- Every step names its proof: the command, the observation, or the measurement that shows it worked.

Hand the agreed shape, the order and the red flags to `write-plan` for the tactical plan.

## 6. Scrap when the evidence says so

Forced casts, `any`, optional flags threaded through layers that do not use them, and a wrapper around one caller are not implementation details. They are evidence that the interface is wrong.

Count them. One workaround is a smell; two independent workarounds at different call sites mean stop and redesign. Record what the implementation taught you, delete the sketch, and restart at step 2. A design kept because of the work already spent is the most expensive design in the repo.

## Output

One design decision record:

- the question, the brief and the constraints;
- the candidates, their models and families, and the judge's model and scores;
- the winner and the reasons;
- the call-site sketch and the signatures;
- the implementation order and the first slice;
- the triggers that would make the design scrap;
- the open items for the user.

Write it with the `explain-simply` skill. A reader who was not in the candidate round must be able to follow one call site from the old shape to the new one.

## Boundaries

- `research-prior-art` surveys how others solve it. Run it in the grounding step when the design has no precedent in the repo.
- `prototype` answers a question by building. Run it before this skill when the open question is empirical rather than structural.
- `write-plan` writes the steps for the agreed shape.
- `review-plan` is the adversarial critic of that plan.

## Done when

- [ ] Every call site in the brief has a `file:line`, and the search was rerun after the design.
- [ ] The brief fixed the tie-break order before the candidates ran.
- [ ] Two or three independent candidates existed, with no shared sight, and at least one was the ambitious option.
- [ ] Every candidate and the judge name their model and family, and a single-family run says what it could not check.
- [ ] A different judge scored them against the same rubric and named one winner.
- [ ] The winner has a call-site sketch, exact signatures and one real call written out.
- [ ] The implementation order starts with one real call site and names the scrap triggers.
- [ ] The user has the record and the open items; no code is written in this turn.
