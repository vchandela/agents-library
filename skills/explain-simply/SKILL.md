---
name: explain-simply
description: Use when someone wants to understand a system, a concept or a decision from first principles, in chat or as an explainer page (an artifact that teaches, such as "the infra under X" or "how X works"). It is also the one voice for anything a person reads, and every other skill writes its specs, plans, reports, PR bodies and commit messages with it. Not for a proposal that asks colleagues to decide; that is write-tech-doc. Not for mapping a whole repo by its decisions; that is understand-codebase.
---

# Explain simply

## First rule: simple sentences, never terse

This is the most common failure, so it comes before everything else. Check every sentence against it before anyone reads the text.

- **One idea per sentence, in the plain order: who does what.** Don't stack clauses, parentheses and citations into one sentence. Put a citation at the end of its sentence, or in its own sentence.
- **Never terse, even when grammatically full.** A sentence is terse when it leans on a term the reader has not met, or skips the step between its cause and its conclusion. Say what the thing is and what it does.
- **No labels in place of sentences.** A bold label followed by a compressed clause ("One outcome per answer, ids not text.") makes the reader decode it. Write the sentence the label stands for.
- **No filler either.** Simple is not padded: cut lead-ins that only announce what follows.

Example. Terse: "One outcome per answer, ids not text. A harmful answer (wrong, and following it would make things worse, `vocabulary.yaml:28`) is the outcome harmful, not wrong plus a flag." Simple: "A harmful answer is now its own outcome. Before, it was saved as wrong with a separate harmful flag. A harmful answer is a wrong answer that would make things worse if someone followed it (`vocabulary.yaml:28`)." Another: "We already have a baseline, because the learner grades Artemis on every ticket it studies" drew "what does this mean?"; the fix was "We can start measuring today, because the learner already checks whether Artemis's first answer was right on every closed ticket it studies." Slides and short lines tempt compression most, so check them hardest.

Explain from first principles, with examples grounded in reality.

**The bar is hard: easy to digest without losing technical depth.** Simplifying by removing the difficult part is not this. Keep the depth, change the delivery.

Apply `references/judgement.md`, `references/writing-voice.md`, `references/explaining.md` and `references/visuals.md`. For a page, also apply `references/preview.md`. For a doc someone else will send or read critically, run the "Shape and rhythm" check in `references/writing-voice.md` before you hand it over.

The references this skill names rely on these, so read them in full too: `references/respect-human-attention.md` (what a reader's time is worth), `references/machine-tells.md` (the last pass for machine-sounding text), `references/ambition.md` (the ambitious option next to the obvious one), `references/core.md` (the six core actions).

## Read before you explain

Read the source before the first sentence: the code, the config, the Terraform, the thread. An explanation built from docs alone repeats whatever the docs got wrong.

- Verify every claim and cite `file:line` so the reader can open it. A fetch result is a lead, never a quote (`references/research-sources.md`, Access notes).
- When the docs and the code disagree, say so and trust the code. Example: "The README says CI deploys on every push. The live path is a scheduled workflow that deploys every two hours."
- When the source cannot settle a fact, say so, in a list of unknowns at the end. A confident account with silent gaps is worse than an incomplete one with the gaps marked.
- A correction to something you said earlier goes in a visible box where the topic comes up. Never bury it.
- **Test an inference against live data before presenting it as a finding.** When the claim can be checked (a build log, an API, a cluster, an audit log), check it first, with read-only calls (get, describe, list, logs). Never change a live system to test a claim. Example: "teardowns all fail" fell to a few hundred logs showing most of them succeed. Check every claim by default; an "inference" or "not checked" label is not a substitute for the check. Only when every route has failed and the access was asked for does a claim stay open, and then it is written once, at the claim, as a blocker with the access it needs.
- **State what happens in practice only from records of it happening.** What a flag, permission or code path allows is capability, not practice. Before saying who does something, when or why, open the records: run rows, logs, timestamps, who started each run, the team's own tracker. A summary from an earlier agent or a doc is a lead to open, not evidence. When the reader draws a conclusion from your answer ("so they press Troubleshoot on each ticket"), check it before you reply, or say plainly that it is not verified. Failure this prevents: a flag that lets two engineers run the obs agent on a customer's job became "engineers rerun it on the ticket's job", and the reader concluded they investigate live tickets by hand. The run records showed the opposite: past runs graded after the ticket closed, and nobody running the agent to help support.
- **Cite something that breaks when the fact changes.** A Jira, Slack or BuildKite link keeps opening after the claim behind it goes stale, so it proves nothing later. Cite the code path, config key, flag or query the claim rests on, which a check can re-run. Example: "capped at 50 nodes (JIRA-123)" silently goes wrong when someone raises the cap; "capped at 50 nodes (`config/autoscaler.yaml: max_nodes`)" is flagged by the PR that changes it.
- **Check what merged recently before proposing a fix.** Fetch the default branch and read the last few days of commits in the area. A fix designed from an old checkout may already exist (a pool backoff proposed in the morning had been merged that day).
- **Before listing issues or items, sweep every earlier page and doc on the topic.** A list built from memory of the conversation misses what earlier work already found. Read each earlier artifact's judgement boxes and "what it costs" notes, and each doc's open items, then say which were added, which folded into existing items, and which were left out because they were judged healthy.

## Match the reader

Find out what they already know and start there. If you cannot tell, ask one question before writing. For a page, first write its story as one "and, but, therefore" line and name its reader, then confirm both with the user in one round of numbered questions, each with your recommended answer, and look up every fact yourself instead of asking.

- Assume an intelligent reader who is new to *this* thing. Define its terms of art. Do not define general engineering terms they already use.
- Bridge from what they know, in a table. Someone who knows Kubernetes learns ECS fastest as: task definition is roughly a pod spec, a service is roughly a Deployment. Say where the analogy breaks.
- When they mention their background ("I ran Temporal on EC2"), use it: put their setup and this one side by side.
- For devices that landed with real readers (a "who does what" table, one item walked end to end, a named scenario table, a job by its inputs), see `references/explaining.md`.

## Walk it step by step

The default shape for anything new to the reader, done for the first time, or reworked on an existing page. An overview of boxes joined by arrows is not an explanation: the reader has to assemble the meaning from names they have not met. A walk through numbered steps in order is.

- **Every step unlocks the next.** Join steps with "but" or "therefore", never "and then": end each step on the gap or question the next one resolves, so the reader always knows why the next section exists.
- **One step, one idea, in the order the reader needs it.** For a system that is usually: why it exists (the problem), what the pieces are, how one run goes, where it breaks, how it connects to what the reader is doing next.
- **Bottom up.** Start from the smallest thing the reader can already picture (one program, one file, one person waiting), add exactly one new piece per step, and arrive at the full problem last. A step never uses a piece that a later step introduces.
- **Animate what changes over time.** When a step is about things that move or take turns (a queue, a lock, retries, a message in flight), show it as a small stepped animation: Next and Back buttons, one change on screen per press, a caption saying what just happened, a Reset, and the end state left visible. Not autoplay, and honour reduced motion (changes appear instantly). Things that do not change stay static pictures. Mechanics are in `references/explainer-pages.md`.
- **Each step has the same parts:** plain words with no system names, one small picture, one real example (a quoted line, a real date, a real row), and a one-line takeaway.
- **Names come last.** Close a step with an "in the system's words" box that maps each idea to its real name (topic = area, bookmark = watermark). Never use a name before its idea has landed.
- **In chat, one step per message**, and let the reader say "next" or ask. Fold each step into the page as it is agreed, rather than publishing the whole page first.
- **End the walk with "what this means".** After the factual steps, one last step says what those facts change for the decision in front of the reader. Facts without it leave the reader to draw the conclusion alone.
- **When the question is who can reach what, draw the boundary.** For a sandbox, a VM, a network or any trust line, draw two boxes, put every piece on its side, and say in a caption what everything inside can touch. Failure this prevents: a design drew a helper process apart from the agent it served. Both ran as root in the same VM, so every check placed in the helper could be bypassed by the agent. A two-box picture made that obvious at once, and the reader said the explanation landed.
- **A diagram supports a step. It never replaces the steps.** For a reader new to the subject, an overview picture comes after the steps or inside one step. A reader judging a design gets the map first (`references/visuals.md`).

Failure this prevents: a page that led with a six-box pipeline and a glossary lost the reader; five plain steps landed.

## From research to the doc others read

A design that will be presented runs through three pages, and the second one is where it gets clear. Plan for all three from the start, so the final doc arrives in hours, not days.

1. **The research page is the author's.** Every claim with its source, every decision with its options. Nobody else reads it in full.
2. **The walkthrough page crystallises it with the reader,** one section at a time in a live artifact, in this order: how each side runs today (with real counts on the arrows), the domain's nouns defined on one real customer, one fine-grained table of what each side can reach, then 3 to 5 broad problems on one diagram, the fixes on the same grid, the order of work with what each phase does and when it is done, and the asks. Fold many issues into a few broad problems so readers do not get fatigue: nine issues became four (hand-off, runbooks, tools, measuring).
3. **The doc for the team is short and in the reader's words.** It reuses the walkthrough's diagrams and tables, and the reader writes the prose.

- **When a stakeholder names a priority, reorder; don't redraw.** The whole picture stays, and their blocker becomes the first phase. A meeting moved platform status from "last, only if needed" to phase 1 without changing any of the four problems.
- **Count the whole population when it is reachable.** A sample says 8%; reading all 422 tickets said 8.5%, and the breakdown (7% workload failures, half with an id) is what explained it.
- **Use the reader's words for people and roles:** "human engineer", not "expert".

Failure this prevents: a 30-section research page went to review first; only the step-by-step walkthrough built afterwards produced a doc the team could read.

## Visuals and pages

Every picture follows `references/visuals.md`: the form for each question, the 50-form catalog with the chart tools, the diagram rules, and the checklist that runs before anything goes out. For a page, also apply `references/explainer-pages.md` (layout) and `references/preview.md` (render and look).

## Rationalisations to refuse

| The excuse | What to do |
|---|---|
| "They said it was too verbose, so I cut it" | Explain it more simply. Too verbose means simplify, never drop. |
| "The diagram speaks for itself" | Annotate every arrow and box. It does not. |
| "These numbers read fine as a sentence" | Three or more numbers that compare or make a whole are a chart. Render two or three forms and keep the clearest. |
| "One overview picture covers it faster than steps" | For a reader new to it, walk it step by step. Boxes joined by arrows are a recap, not the explanation. |
| "A summary at the top helps them orient" | Only if every word in it is already defined. Otherwise it goes at the end. |
| "The docs say so" | Check the code. Cite what you checked. |
| "An example would make it longer" | The example is the explanation. Cut prose instead. |
| "The HTML parses, so it is fine" | That is not a preview. Render it, screenshot every section, look, fix. Never publish unpreviewed. |

## Done when

Somebody who did not already know this understands it on one read. Every term is defined before it is used, every claim has its example or its `file:line`, every decision is shown side by side with a verdict, every diagram element is annotated, every question the reader asked is answered where it arises, and the unknowns are listed. The visuals checklist in `references/visuals.md` passes, and for a page, so does the preview.
