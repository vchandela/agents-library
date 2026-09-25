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

Start with a **sequence diagram** tracing one real request end to end, through every
process it touches. This is the single most useful picture for a system of
cooperating services, and it is the one readers ask for after being shown a
box-and-arrow architecture diagram instead. It answers, in one image, what most
of their questions turn out to be: who calls whom, in what order, which component
does the work, and where the loops are. Label every arrow, and put a short
plain-English note under each one saying what that message actually does.

Reach for a box-and-arrow diagram only when the question is genuinely about
structure rather than flow. Then the decisions as a list. Crisp but complete: a
reader should be able to zoom in on any one and find it explained.

Apply `references/writing-voice.md`. Define jargon the first time it appears.
Analogies and concrete examples for anything abstract. Assume the reader is
competent but new to this system.

## Honesty

Say which parts you could not work out. A confident account with silent gaps is worse than an incomplete one with the gaps marked.

## Done when

Each decision names the alternative rejected and the cost accepted, the diagram matches what the code does rather than what the docs claim, and the unknowns are listed.

## Voice and level

`references/writing-voice.md` covers plain English, no dashes, and tables over
paragraphs. This section adds only what that file does not.

Match the reader, and say so if you cannot tell. Assume a competent engineer who
is new to *this* system: fluent in queues, databases, distributed systems and
LLM agents, and unfamiliar with this repo's own vocabulary. Define the repo's
terms of art on first use. Do not define general engineering terms.

**Build from the ground up.** Define each term where it first appears, in order.
Never open a section with a summary that uses words the reader has not met yet;
it reads as noise and has to be decoded after the fact. A recap belongs at the
END, once every word in it means something. That is how a complex section fits
in the reader's head at once.

**Show the alternative side by side, not in prose.** A decision is a comparison,
so draw it as one: A and B next to each other, with the arrow or box that
actually differs highlighted. A paragraph that describes the current design and
then mentions what it replaced is not a comparison: the reader cannot see the
difference, they have to reconstruct it. One shared diagram per decision beats
one diagram for the whole page.

**Every claim carries its example.** "Adding a workflow is a YAML file and a
six-line class" is a characterisation; the six lines and the YAML beside them are
the explanation. Quote the real code, small enough to read in place, with its
`path:line` so the reader can open it. A decision explained without an example
is the most common failure of this skill.

**Answer each question where it arises.** A judgement about whether a design is
healthy goes in a box directly under the part that describes it, never in a
section at the end.

**Plain words means no flourish.** "Every step goes through this one call" beats
"every step crosses the one teal edge." If a sentence would sound odd read aloud
in a standup, rewrite it. When a reader says a section is too verbose, explain it
more simply; do not delete it.
