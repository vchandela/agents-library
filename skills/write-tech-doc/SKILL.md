---
name: write-tech-doc
description: Use when a technical proposal or design doc is needed for colleagues who will read it critically. Not for a public blog post; that is write-blog.
---

# Write a technical doc

## Interview first, and do not skip it

Ask questions until you are clear on what exists today, what is being built, and why. In rounds: every question whose prerequisites are settled, numbered, each with your guess, so a reply can be a yes or a no. Every doubt goes to the author before anything is written.

**Do not touch the document until you have alignment.** A doc written from a half understood brief has to be rewritten, and the rewrite is more work than the questions.

## Shape

One page, two at most, three only if the material truly needs it. Assume a reader with no patience and real expertise.

- **Problem first.** State precisely what is wrong before proposing anything. Most weak docs start solutioning in paragraph two.
- **Then first principles.** What is fundamentally true here, what are we actually dealing with.
- **Then the solution**, concise: when it has a handful of parts, one picture of four to seven big boxes, each box a section that goes deeper layer by layer, with one real example running through every section (`references/visual-explanations.md`, "Steps first, or the map first"). A single decision or a comparison needs another shape.
- Suggest phases where the work splits into phases.
- Sections worth having: overview, design decisions, diagrams, tradeoffs, and what is knowingly left undone.

Apply `references/use-your-judgement.md` and `references/writing-voice.md`. Tables and diagrams instead of paragraphs wherever they carry the same content. Every word earns its place.

## Diagrams

One per option, where options are being compared. A diagram per option does more for a reader than three paragraphs of contrast.

Apply `references/respect-human-attention.md`, including its rules for systems: a design asks people only what a machine cannot decide.

## Be honest about tradeoffs

Name the real limits, including the ones easy to gloss over. A doc that only lists upsides reads as a pitch, and a reader who has shipped things will discount all of it.

## Done when

A colleague who has read nothing else understands the problem before the solution, can find each decision and its reason, and knows what you chose not to do.
