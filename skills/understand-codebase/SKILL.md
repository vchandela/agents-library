---
name: understand-codebase
description: Use when an unfamiliar repository needs to be understood by the decisions it made rather than by its file layout. Not for reviewing a change; that is review-pr.
---

# Understand a codebase

The question is not what this code does. It is **what the authors decided, and what they gave up**.

## Find the decisions

Every system makes a set of choices its authors could have made differently. Name them, and name the alternative that was rejected.

For an agent or ML system, the usual set:

- How is memory handled per session, across sessions, and per user?
- How is it evaluated, and against what?
- What is the harness: what runs the loop, what can interrupt it?
- What sandboxing, and what escapes it?
- Where are the trust boundaries?
- What is deterministic and what is left to the model?

For anything else: where state lives, what is atomic, what happens under concurrency, what happens when a dependency is down, what is cached and for how long.

Expect ten to fifteen real decisions. If you have three, look harder.

## For each one

State the decision, the alternative they rejected, and the cost they accepted. A decision with no cost was not a decision, it was a default, and defaults are worth noticing too.

## Output

One diagram (Mermaid is fine) giving the high level shape, then the decisions as a list. Crisp but complete: a reader should be able to zoom in on any one and find it explained.

Apply `references/writing-voice.md`. Define jargon the first time it appears. Analogies and concrete examples for anything abstract. Assume the reader is competent but new to this system.

## Honesty

Say which parts you could not work out. A confident account with silent gaps is worse than an incomplete one with the gaps marked.

## Done when

Each decision names the alternative rejected and the cost accepted, the diagram matches what the code does rather than what the docs claim, and the unknowns are listed.
