# Documentation modes

A reader opens a document with one of four needs: to learn, to do a task, to look something up, or to understand why. Each need has its own mode, and a document written in the wrong mode makes the reader work. The four names come from Diátaxis: tutorial, how-to, reference and explanation.

## The four modes

| Mode | The reader's need | The shape | The test |
|---|---|---|---|
| Tutorial | Learn by doing, from zero | A lesson with a runnable path, one step at a time, no choices | A beginner reaches the end without outside help |
| How-to | Get one job done | Numbered steps for a competent reader, with the decision points named | A reader who knows the domain finishes without a detour |
| Reference | Look up a fact | Complete, consistent, structured for random access | Every parameter, error and limit has one place |
| Explanation | Understand why | Discussion, context, alternatives and tradeoffs | A reader can explain the choice back |

## The map

Two axes decide the mode:

- **Practical or theoretical:** is the reader doing something, or understanding something?
- **Learning or working:** is the reader acquiring a skill, or applying one?

A tutorial is learning and practical. A how-to is working and practical. A reference is working and theoretical. An explanation is learning and theoretical.

The axes settle arguments about structure. A "how to deploy" page that spends four paragraphs teaching what deployment is has drifted into explanation. A "why we chose this queue" page that lists flags has drifted into reference.

## One document, one mode

Mixing modes breaks the reader:

- a tutorial interrupted by a reference table loses the beginner;
- a how-to that stops to teach the concept loses the competent reader;
- a reference that argues a design is no longer complete or predictable;
- an explanation that turns into steps is no longer about why.

Keep each document in one mode, and link across modes instead of absorbing them. A document that tries to be four things is four bad documents in one file.

A README is not a fifth mode. It is the front page: what the project is, who it is for, one runnable example, the state of the project, and links to the tutorial, how-to, reference and explanation. If the README grows headings for every task, it is becoming a how-to and should link to one.

## README first

When the interface is new, write the intended usage before the implementation:

1. The tutorial: what a new reader does first, in order.
2. The README: what it is, one example, where the other modes live.

Then work backwards to the implementation. The draft usage is the target and the first acceptance test. If a parameter needs a paragraph to justify its name, rename it now, while the design is still soft. If the example cannot be written without a caveat, the interface has a caveat to fix.

Diátaxis does not fix a writing order: a reference can be drafted first because it settles the interface, and that is a fair choice. What this rule adds is that the README and the tutorial for the intended usage are written before the implementation, so the usage is the target rather than a description added afterwards.

A README records intent, not proof. Its examples are run in the same change that ships the code, and the README changes in that change too. A stale README is a wrong reference, and a reader trusts it more than the code.

## Checklist

- [ ] The mode is named before drafting.
- [ ] Each document links to the other modes instead of absorbing them.
- [ ] The first screen answers: what is this, who is it for, how do I run it.
- [ ] Every example was run, not written from memory.
- [ ] Reference pages are complete and current; explanation pages say when they were written.
- [ ] The README changed in the same change as the interface.
- [ ] A newcomer can finish the tutorial without opening the source.

## Source

The four modes, the two axes and the rule against mixing them are Diátaxis (Daniele Procida, diataxis.fr), read on 22 November 2026. The README-first sequence — write the intended usage, then implement against it — was described in a public agent-skills guide the same day; the checklist and the stale-README rule are this library's.
