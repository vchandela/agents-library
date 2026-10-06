---
name: write-spec
description: Use when someone wants to build something and the requirements are not pinned down yet. Not for a task whose shape is already agreed, and not for writing the implementation plan.
---

# Write a spec

Interview until the shape is agreed. Only then write.

## Size the work first

Say out loud which of three it is, so the user can overrule you.

- **Spike**: a question whose answer is the output ("can we..."). Two or three sentences on what you will try, a nod, then the answer. No spec.
- **Bounded**: a change to a flow that already exists in this repo. A short design in chat, then an explicit yes, then work. No spec file.
- **New shape**: a new project or subsystem, or an interface others depend on. The full interview and spec.

When unsure, take the heavier one. Complexity found later moves the work up a level; nothing moves it down. A yes approves only the stage that was shown. If the request is several independent subsystems, say so before the first detailed question and split it.

## Read before you ask

Before the first question, read what already exists: the owner's handover and design notes, the code being replaced, and the repo it is moving into. A good handover answers most interview questions. Spend the interview on what it leaves open.

Look for precedent in the target repo. A design that copies a pattern the team already runs is cheaper to build and much cheaper to review. Say which pattern, with the file and line.

Verify every claim against the source and cite `file:line`. When something does not exist in the repo, say so plainly. It is new work, not a port.

## Shape before spec

If the fundamental shape is undecided (where it runs, what owns state, one long process or many short ones), settle that first. A spec written for the wrong shape gets written twice.

For any real decision, decide first, then present it. Two or three options side by side, one marked recommended with its reasons, each other one with the reason it was discarded. Make the reviewer's job a yes or a no.

Follow the repo's conventions. Use first principles to check that a convention fits and to weigh the user's suggestions, not to invent new patterns. Anything new to the repo must be necessary, and the user confirms it before it goes in the spec.

Apply `references/use-your-judgement.md`: propose requirements the user did not mention but the domain needs, marked as proposals.

Apply `references/engineering-principles.md`. Every choice is a tradeoff: each piece of complexity says what it buys, or moves to a "later" list. Pragmatic, not perfect.

Be honest where a rejected option wins on some dimension. Name it, then say why it still loses overall.

Explain tradeoffs with one concrete worked example: a real-looking timeline showing where each blocker bites.

When an interface is the decision, have three sub-agents each design it under a different constraint (fewest entry points; most flexible; simplest for the most common caller), then compare what callers must learn and where change would land. When "how should it behave" is the open question, build a throwaway prototype instead of arguing, on a throwaway branch, and link it.

## Teach the design

Apply `references/visual-explanations.md`. Prefer diagrams and real examples over prose. The spec must include an end-to-end diagram of the core behaviour and a real-looking worked example. Each non-obvious new mechanism gets the clearest useful visual before the document relies on its name. The visual must stand on its own. Pseudocode is optional and secondary; include it only when the visual does not make the exact check or ordering clear.

## Interview first

Before the first question, write one line: your best guess of what the user wants, how confident you are, and what is missing.

Interview in rounds. Map the decisions as a tree: each one opens the ones that hang off it. Each round, ask every question whose prerequisites are already settled, numbered, each with your guess or recommended answer, so every reply can be a yes or a no. A question that depends on one still open waits for a later round. Look up facts yourself; ask the user only for decisions. Cover implementation, interfaces, failure behaviour, tradeoffs, and what the user is actually optimising for.

When an answer sounds like what a good answer should sound like ("scalable", "clean", "the standard way"), ask: "If you did not have to justify this to anyone, what would you actually want?"

**Do not ask obvious questions.** Ask the ones whose answers would change the design: what happens when this is called twice, when the upstream is down, which of two costs matters more.

Keep going until no branch is unvisited, nothing is silently assumed, and you can state the system back and the user agrees. Then write the file.

## The spec

**Purpose.** One paragraph. What problem, for whom.

**Interface contract.** Every input: name, type, constraints, an example value. Every output: shape, type, and what partial success looks like. The entry points.

**Behaviours.** The happy path as numbered steps. Then every error case as a condition mapped to an exact behaviour: what is returned, logged, retried, skipped.

**Invariants.** Assertions. "X must never happen." "Y must always equal Z."

**Non-functional.** Idempotency, ordering, atomicity, each yes or no and why. A performance budget if users wait on it, with the number measured today. What is logged or measured.

**How we test it for real** (when repo tests can't show it working). The real-world test from `references/testing.md`: action, exact input, expected result, what failure looks like. Prefer replaying the ask that started the work.

**Open items.** One numbered list: item, recommended answer, other options. Every assumption goes here, including ones the plan depends on. Access to external systems follows the team's existing route. Reviewers reply per number.

Split what is not being decided now in two. **Not yet specified:** in scope, but you cannot phrase the question sharply yet; revisit as decisions land. **Out of scope:** ruled beyond this spec, with one line of why; it does not come back unless the goal changes. The test is whether you can state the question precisely now, not whether you can answer it.

## The document

Apply `references/respect-human-attention.md`: the user's overview (boxed "Written by <name>"), one "AI-assisted · human-reviewed" box where agent-drafted sections begin, what stays visible versus collapsed, and open questions numbered first with options, not your picks.

2 to 3 pages, tight and complete.

- Open with the core flow in a diagram, not a compressed summary of unexplained terms.
- Cluster related material: options, tradeoffs and recommendation in one table.
- Define a term in a parenthetical where first used. No shorthand. When two words compete for one concept, pick one and list the losers: `Order` (avoid: purchase, transaction). When the user's word contradicts the code, say so and ask which is right.
- Collapse supporting detail.
- Diagrams over prose in every section, not just the opening: lifecycle as a state diagram, error cases as a flow, open items as left-versus-right cards. Plain words, no em dashes.
- No dense paragraphs, including in table cells. Use bullets, lists or small tables.
- On every revision, fold the change into its section. Never append.
- Before publishing, run a verification pass over every claim, and read it once for placeholders, sections that contradict each other, and any requirement that could be read two ways. Cut anything not needed.
- Real diagrams (Mermaid) and real tables, not monospace text blocks.
- **Preview before every publish.** Apply `references/preview.md`: parse every diagram, render a local preview, inspect it in Chrome, fix, repeat. Not optional.
- Plain words in full sentences. Cut fluff, not the words that make a sentence readable. Titles name the thing in plain terms ("How we read Slack", not "reading code").
- For review: the artifact is the document; the team's doc tool holds the links and the open items for comments.

## Done when

The preview in `references/preview.md` passes. Every error case names an exact behaviour, every invariant is falsifiable, every decision shows its discarded options, and the user has confirmed the spec back. Next: `write-plan`.
