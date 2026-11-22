---
name: prototype
description: Use when a design question about a flow, layout, interaction or mechanism is still open and a quick disposable build would settle it faster than more reading or argument, even when the question sounds like architecture or a performance benchmark. Not for the craft of designing a screen; that is design-ui. Not for the implementation plan once the shape is agreed; that is write-plan. Not for reviewing a plan or a diff; that is review-plan or review-pr.
---

# Prototype

A prototype is a question with a build around it. It is not the first draft of the product, and it is not a demo.

Apply `references/verifying-apps.md` for the loop, the project's CLI and the evidence. Use the `verify-app` skill when the project has a browser fixture.

## Name the question and the decision

Write two sentences before any code: the question the prototype answers, and the decision it feeds. "Can a single scrolling settings page carry every section without a second level of navigation?" feeds "the settings page shape". If no decision changes with the answer, stop. You are building a demo.

Turn each option into a hypothesis with a measurable prediction: "one page will reach the save button in fewer clicks", "the queue design will survive a retry without duplicating". A prediction lets the evidence settle the argument; "it felt better" does not.

## Two or three variants, never one

- Each variant tests a different hypothesis, not the same screen in three colours.
- Include the obvious option as the control and one ambitious alternative. The obvious one may win; then the evidence says so in one run.
- Build the smallest fake that answers the question. Hard-code the data, stub the network, skip the empty states. The parts outside the question are allowed to be ugly.
- Put the variants behind one switcher or in one scratch folder or branch. Never put them in the product path.
- A switcher is a query parameter, a development-only environment value, or a separate entry route. It leaves with the prototype.

Two variants is the floor. One variant is a demo; four is a comparison nobody can hold.

## Build where you can see it

Drive each variant with the project's own browser fixture, not a separate harness. Open the route, perform the action a user performs, settle, then capture.

Collect at least one kind of evidence:

- a screenshot at every width the product supports;
- a trace of the network, console and render;
- a number the question names: time to first action, clicks to the goal, layout width, row height, payload size, error count;
- the diff size and the number of call sites each variant would touch.

Choose the measure before you look at the variants, so the measure is not picked to fit the result.

## Pick with reasons

Write one short note:

- the question and the decision;
- each variant and its evidence;
- the pick;
- what the runner-up did better, named honestly;
- what evidence would change the pick;
- the real cost of the winner: files, API changes, migrations, tests.

The pick is a proposal to the person who owns the decision, not a silent rewrite. If the evidence is a tie, say it is a tie and name the constraint that should decide.

## Clean up

Delete the scratch branch or folder, the switcher, the flag and the hard-coded data. Keep only the evidence and the pick note.

Then prove the cleanup: `git diff` against the base branch shows the product path untouched, and the project's checks pass with the prototype gone. A prototype that survives becomes the product by accident, and that is the failure this step prevents.

## Rationalisations to refuse

| The excuse | What to do |
|---|---|
| "The first design is obviously right." | Build it as the control and one alternative. You may be right; one run proves it. |
| "We do not have time for three variants." | Two is the floor: the control and one alternative. |
| "We will clean it up later." | Cleanup is a step in this skill, not a later task. Delete it now. |
| "It is basically the real thing already." | Then it is an implementation. Stop, write the plan, and build it with tests. |
| "The prototype needs real auth and data to be realistic." | Fake everything the question does not touch; use the fixture for the part it does. |
| "The measurement is obvious from the screenshot." | A screenshot is one width, one state. Record the number the question names. |

## Done when

- [ ] The question and the decision are written down.
- [ ] Two or three variants existed, each a different hypothesis.
- [ ] Each variant ran in the real app and has named evidence.
- [ ] The pick note names the runner-up's advantage and what would change the pick.
- [ ] The prototype is deleted, and the diff proves the product path untouched.
- [ ] The evidence and the pick note remain, ready for `write-plan`.
