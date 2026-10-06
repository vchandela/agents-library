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

Tag every relationship you state: **read** (`file:line`), **inferred** (and from what: a shared type, naming, sitting side by side), or **unclear**. Do not invent a percentage. An arrow you did not read never goes in the diagram as solid: draw it dashed and labelled inferred, or move it to the unknowns.

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

Answer the two kinds of question in their own shape. "What is X connected to?" is a list of neighbours, each with its relation and evidence. "How does X reach Y?" is one path, hop by hop, each hop with its `file:line`.

End with three to five questions this map can now answer, each with why it is worth asking: an unclear link, a module that bridges two areas, a hub you have not explained. Offer to trace the one that crosses the most areas. List the searches that found nothing, so the next reader does not repeat them.

Apply `references/use-your-judgement.md`, `references/untrusted-input.md` and `references/writing-voice.md`. Define jargon the first time it appears.
Analogies and concrete examples for anything abstract. Assume the reader is
competent but new to this system.

## Honesty

Say which parts you could not work out. A confident account with silent gaps is worse than an incomplete one with the gaps marked.

## Done when

Each decision names the alternative rejected and the cost accepted, the diagram matches what the code does rather than what the docs claim, and the unknowns are listed. Every identifier and path you cite was grepped once more before you finished.

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
