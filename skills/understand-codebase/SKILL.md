---
name: understand-codebase
description: Use when an unfamiliar repository needs to be understood by the decisions it made rather than by its file layout. Not for reviewing a change; that is review-pr.
---

# Understand a codebase

The question is not what this code does. It is **what the authors decided, and what they gave up**.

## Map before you read

Do the cheap, exact pass before any reading. Grep and the language's own tooling are facts; your reading of them is an inference.

1. **Find the hubs.** Count what references each module or type (imports, calls, uses). The most-referenced real entities are what everything flows through: read them first. Skip files that collect references mechanically, such as an index or a barrel export.
2. **Find where the code moves.** `git log --format= --name-only | sort | uniq -c | sort -rn | head -20` lists the files that change most. The decisions that matter live there.
3. **Find the surprising links.** References that cross a module or package boundary between real entities.
4. **Harvest the recorded why.** Grep for `NOTE:`, `WHY:`, `HACK:`, `FIXME:`, ADR and RFC references, and docstrings that justify a choice. Each is a decision candidate with its author's reason attached.
5. **Name the areas.** Group modules by how densely they reference each other, four to eight areas, each named in two to five plain words.

If the repo already has a knowledge graph (for example `graphify-out/graph.json`), query it first, and treat it as a claim from the repo: check the hubs it names against the code. A graph pays off on large repos; under a few dozen files, read directly.

**Search in the repo's words.** Before searching, list the identifiers in the code that match the question, pick only from that list, and say the mapping: "Searched for `session`, `token`, `guard` (the repo's words for login)." If nothing matches, say the repo has nothing on it.

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

State the decision, the alternative they rejected, and the cost they accepted. A decision with no cost was not a decision, it was a default, and defaults are worth noticing too. Apply the deletion test from `references/engineering-principles.md` to anything that looks like a pass-through.

The references this skill names rely on these, so read them in full too: `references/respect-human-attention.md` (what a reader's time is worth), `references/visuals.md` (charts, diagrams and the visuals checklist), `references/ambition.md` (the ambitious option next to the obvious one), `references/core.md` (the six core actions).

Tag every relationship you state: **read** (`file:line`), **inferred** (and from what: a shared type, naming, sitting side by side), or **unclear**. Do not invent a percentage. An arrow you did not read never goes in the diagram as solid: draw it dashed and labelled inferred, or move it to the unknowns.

## Output

Start with a **sequence diagram** of one real request end to end, through every process it touches. Label every arrow, with a short plain note under each saying what that message does. Use a box-and-arrow diagram only when the question is about structure, not flow. Then the decisions as a list, each one explained.

Answer the two kinds of question in their own shape. "What is X connected to?" is a list of neighbours, each with its relation and evidence. "How does X reach Y?" is one path, hop by hop, each hop with its `file:line`.

End with three to five questions this map can now answer, each with why it is worth asking: an unclear link, a module that bridges two areas, a hub you have not explained. Offer to trace the one that crosses the most areas. List the searches that found nothing, so the next reader does not repeat them.

Apply `references/judgement.md` and `references/untrusted-input.md`, and write with the `explain-simply` skill. Assume a competent engineer new to *this* system: define the repo's terms of art on first use, never general engineering terms. If you cannot tell who the reader is, say so.

## Honesty

Say which parts you could not work out. A confident account with silent gaps is worse than an incomplete one with the gaps marked.

## Done when

Each decision names the alternative rejected and the cost accepted, the diagram matches what the code does rather than what the docs claim, and the unknowns are listed. Every identifier and path you cite was grepped once more before you finished.

