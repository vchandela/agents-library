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
- **Short sentences, with a hard cap.** About 20 words when it tells someone what to do, 25 when it describes something. Write in the active voice: who does what. The cap comes from ASD-STE100 Simplified Technical English. A longer sentence is two ideas: split it.
- **No pronoun the reader has to resolve.** Use "it", "this" or "that" only when its referent is in the same sentence or the one before. Otherwise repeat the noun. Never coin a label the reader has not seen, such as "the switch-back note"; use the real name or a short description (HumanLayer's prose rules). A coined word for something new is fine only with its real name in brackets, as `references/explaining.md` says.
- **Name the actor and the call.** "The queue reader stores the request on a raw event" beats "the request gets persisted". "`fast_check` calls `run_db_query`" beats "the script delegates to the gateway" (poteto's `how` skill).
- **Write for a reader who wasn't in the room.** A PR description, a Notion doc or an artifact is read by someone who missed the discussion behind it. Define every term at first use, state a rule in place of naming whose rule it is, and explain a step in place of pointing at it. Never write "as we discussed" or "you and I agreed".

Example. Terse: "One outcome per answer, ids not text." Simple: "A harmful answer is now its own outcome. Before, it was saved as wrong with a separate harmful flag. A harmful answer is a wrong answer that would make things worse if someone followed it (`vocabulary.yaml:28`)." Slides and short lines tempt compression most, so check them hardest.

Explain from first principles, with examples grounded in reality.

**The bar is hard: easy to digest without losing technical depth.** Simplifying by removing the difficult part is not this. Keep the depth, change the delivery.

Apply `references/judgement.md`, `references/writing-voice.md`, `references/explaining.md` and `references/visuals.md`. For a page, also apply `references/preview.md`. For a doc someone else will send or read critically, run the "Shape and rhythm" check in `references/writing-voice.md` before you hand it over.

The references this skill names rely on these, so read them in full too: `references/respect-human-attention.md` (what a reader's time is worth), `references/machine-tells.md` (the last pass for machine-sounding text), `references/ambition.md` (the ambitious option next to the obvious one), `references/core.md` (the six core actions).

## Read before you explain

Read the source before the first sentence: the code, the config, the Terraform, the thread. An explanation built from docs alone repeats whatever the docs got wrong.

- Verify every claim and cite `file:line` so the reader can open it. A fetch result is a lead, never a quote (`references/research-sources.md`, Access notes).
- When the docs and the code disagree, say so and trust the code. Example: the README said CI deploys every push; the live path is a scheduled workflow every two hours.
- When the source cannot settle a fact, say so in a list of unknowns at the end. A confident account with silent gaps is worse than one with the gaps marked.
- A correction to something you said earlier goes in a visible box where the topic comes up. Never bury it.
- **Test an inference against live data before presenting it as a finding.** When the claim can be checked (a build log, an API, a cluster, an audit log), check it first with read-only calls (get, describe, list, logs). Never change a live system to test a claim. Check every claim by default; an "inference" or "not checked" label is no substitute. Only when every route has failed and the access was asked for does a claim stay open, written once at the claim as a blocker with the access it needs. Example: "teardowns all fail" fell to a few hundred logs showing most succeed.
- **Recompute every number and quantifier from the data before it goes on a page.** A count, a share, or a word like "most", "only" or "all" is a claim. Run the query or script that produces it while writing that sentence, keep the script beside the data, and re-run it after any relabelling. A summary from memory of earlier analysis is not evidence. Failure this prevents: a page said 19 unclear runs "mostly need Ray logs"; a join of the label file with the notes showed 3 of 19.
- **State what happens in practice only from records of it happening.** What a flag, permission or code path allows is capability, not practice. Before saying who does something, when or why, open the records: run rows, logs, timestamps, who started each run, the team's tracker. A summary from an earlier agent or a doc is a lead to open, not evidence. When the reader draws a conclusion from your answer ("so they press Troubleshoot on each ticket"), check it before you reply, or say plainly that it is not verified. Failure this prevents: a permission flag became "engineers rerun it on live tickets"; the run records showed the opposite.
- **Cite something that breaks when the fact changes.** A Jira, Slack or BuildKite link keeps opening after the claim behind it goes stale, so it proves nothing later. Cite the code path, config key, flag or query the claim rests on, which a check can re-run. Example: "capped at 50 nodes (JIRA-123)" breaks silently when someone raises the cap; `config/autoscaler.yaml: max_nodes` is flagged by the PR that changes it.
- **Check what merged recently before proposing a fix.** Fetch the default branch and read the last few days of commits in the area. A fix designed from an old checkout may already exist (a pool backoff was merged the morning it was proposed).
- **Before listing issues or items, sweep every earlier page and doc.** A list from memory of the conversation misses what earlier work found. Read each earlier artifact's judgement boxes and "what it costs" notes, and each doc's open items, then say what was added, folded in, or left out as healthy.

## Match the reader

Find out what they already know and start there. If you cannot tell, ask one question before writing. For a page, first write its story as one "and, but, therefore" line and name its reader, then confirm both with the user in one round of numbered questions, each with your recommended answer, and look up every fact yourself rather than asking.

- Assume an intelligent reader who is new to *this* thing. Define its terms of art. Do not define general engineering terms they already use.
- Bridge from what they know, in a table. Someone who knows Kubernetes learns ECS fastest as: task definition is roughly a pod spec, a service is roughly a Deployment. Say where the analogy breaks.
- When they mention their background ("I ran Temporal on EC2"), use it: put their setup and this one side by side.
- For devices that landed with real readers (a "who does what" table, one item walked end to end, a named scenario table, a job by its inputs), see `references/explaining.md`.

## Ground every concept before you lean on it

From Matt Pocock's `writing-shape` and `writing-beats` skills. Defining terms is not enough: a sentence can lean on an idea the reader lacks with no jargon in it at all.

- **Write down the prerequisites first.** Before the first sentence, list what this reader already knows on arrival, for example "knows what a Ray cluster and Grafana are; does not know the admin zone or the learner". Confirm it with the user when a page has more than one reader. Everything not on it must be grounded before anything relies on it.
- **Keep a running grounded list while writing.** Each section either relies on concepts already grounded, or grounds a new one, landing the idea and its name together. When the next point needs an ungrounded concept, ground it first or move it to the prerequisites. Too much up front shuts readers out; too much inside drowns the opening in definitions.
- **Check every block before keeping it.** Ask "If I cut this, what breaks?" If nothing breaks, cut it. Ask "Is this sentence doing two jobs?" If yes, split it. Ask "The opening promised X; are we still on X?" If not, re-thread or change the opening.

## Walk it step by step

The default shape for anything new to the reader, done for the first time, or reworked on an existing page. An overview of boxes joined by arrows is not an explanation: the reader has to assemble the meaning from names they have not met. A walk through numbered steps in order is.

- **Every step unlocks the next.** Join steps with "but" or "therefore", never "and then": end each step on the gap or question the next one resolves, so the reader always knows why the next section exists.
- **One step, one idea, in the order the reader needs it.** For a system that is usually: why it exists (the problem), what the pieces are, how one run goes, where it breaks, how it connects to what the reader is doing next.
- **Bottom up.** Start from the smallest thing the reader can already picture (one program, one file, one person waiting), add exactly one piece per step, and arrive at the full problem last. A step never uses a piece a later step introduces.
- **Animate what changes over time.** When a step is about things that move or take turns (a queue, a lock, retries, a message in flight), show a small stepped animation: Next and Back, one change per press, a caption saying what just happened, a Reset, the end state left visible. Not autoplay; honour reduced motion. Things that do not change stay static pictures. Mechanics are in `references/explainer-pages.md`.
- **Each step has the same parts:** plain words with no system names, one small picture, one real example (a quoted line, a real date, a real row), and a one-line takeaway.
- **Names come last.** Close a step with an "in the system's words" box mapping each idea to its real name (topic = area, bookmark = watermark). Never use a name before its idea has landed.
- **In chat, one step per message**, and let the reader say "next" or ask. Fold each step into the page as it is agreed, rather than publishing the whole page first.
- **End the walk with "what this means".** After the factual steps, one last step says what those facts change for the reader's decision. Facts without it leave the reader to draw the conclusion alone.
- **When the question is who can reach what, draw the boundary.** For a sandbox, a VM, a network or any trust line, draw two boxes, put every piece on its side, and say in a caption what everything inside can touch. Failure this prevents: a design drew a helper apart from the agent it served, both root in one VM, so every check in the helper could be bypassed; a two-box picture made it obvious.
- **A diagram supports a step. It never replaces the steps.** For a reader new to the subject, an overview picture comes after the steps or inside one step. A reader judging a design gets the map first (`references/visuals.md`).

Failure this prevents: a page that led with a six-box pipeline and a glossary lost the reader; five plain steps landed.

## From research to the doc others read

A design that will be presented runs through three pages, and the second one is where it gets clear. Plan for all three from the start, so the final doc arrives in hours, not days.

1. **The research page is the author's.** Every claim with its source, every decision with its options. Nobody else reads it in full.
2. **The walkthrough page crystallises it with the reader,** one section at a time in a live artifact, in this order: how each side runs today (with real counts on the arrows), the domain's nouns defined on one real customer, one fine-grained table of what each side can reach, then 3 to 5 broad problems on one diagram, the fixes on the same grid, the order of work with what each phase does and when it is done, and the asks. Fold many issues into a few broad problems so readers do not tire: nine issues became four.
3. **The doc for the team is short and in the reader's words.** It reuses the walkthrough's diagrams and tables, and the reader writes the prose.

- **When a stakeholder names a priority, reorder; don't redraw.** The whole picture stays, and their blocker becomes the first phase. A meeting moved platform status from "last, if needed" to phase 1 without redrawing.
- **Count the whole population when it is reachable.** A sample says 8%; reading all 422 tickets said 8.5%, and the breakdown (7% workload failures, half with an id) is what explained it.
- **Use the reader's words for people and roles:** "human engineer", not "expert".

Failure this prevents: a 30-section research page went to review; only the later walkthrough produced a doc the team could read.

## Visuals and pages

Every picture follows `references/visuals.md`: the form for each question, the 50-form catalog with the chart tools, the diagram rules, and the checklist run before anything goes out. For a page, also apply `references/explainer-pages.md` (layout) and `references/preview.md` (render and look).

**For code and systems, pick the smallest code-shaped view that makes the point** (HumanLayer's `show-me`). Use one or two of these, never all:

- A call tree for runtime flow: who calls whom, indented.
- A shallow file tree with one comment per line saying what each file owns.
- A step list or a small YAML excerpt for a workflow.
- Pseudocode for a decision, marked as pseudocode.
- A sequence or flow diagram for components talking to each other.

**Show a change to an existing shape as a diff of that shape.** Use a `diff` block on the call tree, file tree, YAML or JSON the reader already knows, with `+` and `-` lines. Show the whole target shape only when most of it is new, or when a diff would hide the order. Failure this prevents: a spec said in prose a workflow "gains a fast step before the answer write"; a five-line YAML diff showed it at a glance.

**For "how does this system work", end with two small sections** (poteto's `how` skill):
- "Where things live": the five or so files a newcomer opens first, each with what it owns.
- "Gotchas": what is surprising or easy to get wrong, each with its proof.

When something is complex, say why it is complex. Don't only describe the complexity.

**When the reader says it didn't land, re-pitch it.** Don't repeat it louder. Give one line of context, use the short-sentence cap above, and use only words the page has already grounded (Matt Pocock's `wait-what`).

## Every page reads the same way

A reader should know where to look on any page we publish: a spec, a plan, a review page or an explainer. Use this order, and skip any part that would give the reader no new fact ("No fluff sections" in `references/respect-human-attention.md`):

1. The title, then one line saying who it is for.
2. The overview, in the user's voice or marked as a draft for them to rewrite.
3. "What you need to know first": the prerequisites, then a small table of terms the page uses.
4. One real item walked end to end, as a table of moments or a small diagram: the flow, so the reader can picture it.
5. The root cause and the key decisions, each with its reason, and "What changes", as diffs of the shapes the reader knows.
6. Open questions, in the format below. A real ask of the reader lives here, never in a separate list that restates the page.
7. Detail, collapsed: tables, failure cases, evidence.
8. Rules that must hold, then "Where things live" and "Gotchas".

**Each open question has the same five parts.** A reader can then answer it from the box alone:

1. The question, as a question, in one line.
2. One or two sentences of context: what the choice is about.
3. A picture of what differs between the options: a small flowchart, a diff, or a comparison table with one row per dimension.
4. Two or three option cards, each with what it is and what it costs. Your pick is marked on its card.
5. One line per losing option, starting "Why <pick> over <option>:", saying why it loses. Name where the loser wins.

Never ask a question with only one real option, and never offer an option nobody would pick (`references/respect-human-attention.md`).

**Less text, never terse.** Cut a sentence when the picture already says it. Keep every sentence that stays a full, plain sentence under the length cap.

**Run the checker before every publish.** `python3 ~/oss/agents-library/scripts/check_page_prose.py <page.html>` fails on:
- a sentence over 25 words;
- an em dash;
- a paragraph or list item over three sentences;
- an open question with no diagram, or with no "Why X over Y" line.

Fix every line it prints, then preview the page (`references/preview.md`). The checker cannot see a diagram that renders badly, so look at each one. For options side by side, draw one plain row per option in a left-to-right flowchart, each row starting with its name. Mermaid subgraphs stack vertically and can reverse order: a three-option picture once read C, B, A. Failure this prevents: a spec's open items were walls of text; the reader asked for options and diagrams.

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
| "The reader knows this term" | Check the prerequisites list. If it isn't there, ground it on the page. |
| "Prose describes the change well enough" | Show the change as a diff of the shape the reader already knows. |
| "The HTML parses, so it is fine" | That is not a preview. Render it, screenshot every section, look, fix. Never publish unpreviewed. |

## Done when

Somebody who did not already know this understands it on one read. The page follows "Every page reads the same way", `scripts/check_page_prose.py` exits 0, the prerequisites are written down, every concept is grounded before a sentence leans on it, no sentence passes the length cap, no pronoun needs resolving, every term is defined before use, every claim has its example or `file:line`, every decision is shown side by side with a verdict, every diagram element is annotated, every question the reader asked is answered where it arises, and the unknowns are listed. The visuals checklist in `references/visuals.md` passes, and for a page, so does the preview.
