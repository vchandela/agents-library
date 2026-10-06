---
name: explain-simply
description: Use when someone wants to understand a system, a concept or a decision from first principles, in chat or as an explainer page (an artifact that teaches, such as "the infra under X" or "how X works"). Not for a proposal that asks colleagues to decide; that is write-tech-doc. Not for mapping a whole repo by its decisions; that is understand-codebase.
---

# Explain simply

Explain from first principles, with examples grounded in reality.

**The bar is hard: easy to digest without losing technical depth.** Simplifying by removing the difficult part is not this. Keep the depth, change the delivery.

Apply `references/writing-voice.md` and `references/visual-explanations.md`. For a page, also apply `references/preview.md`.

## Read before you explain

Read the source before the first sentence: the code, the config, the Terraform, the thread. An explanation built from docs alone repeats whatever the docs got wrong.

- Verify every claim and cite `file:line` so the reader can open it.
- When the docs and the code disagree, say so and trust the code. Example: "The README says CI deploys on every push. The live path is a scheduled workflow that deploys every two hours."
- When the source cannot settle a fact, say so, in a list of unknowns at the end. A confident account with silent gaps is worse than an incomplete one with the gaps marked.
- A correction to something you said earlier goes in a visible box where the topic comes up. Never bury it.
- **Test an inference against live data before presenting it as a finding.** When the claim can be checked (a build log, an API, a cluster, an audit log), check it first. In one session three confident claims fell to a single lookup: a ticket's stated cause of a 404 (the code showed the user is created at deploy time), "cleanup fires after every build" (the builds had no cleanup step), and "teardowns all fail" (a few hundred logs showed most of them succeed). A claim you could not check is labelled as an inference in the text, not only in the unknowns list. Label it once, at the claim; do not hedge the sentences around it.
- **Cite something that breaks when the fact changes.** A Jira, Slack or BuildKite link keeps opening after the claim behind it goes stale, so it proves nothing later. Cite the code path, config key, flag or query the claim rests on, which a check can re-run. Example: "capped at 50 nodes (JIRA-123)" silently goes wrong when someone raises the cap; "capped at 50 nodes (`config/autoscaler.yaml: max_nodes`)" is flagged by the PR that changes it.
- **Check what merged recently before proposing a fix.** Fetch the default branch and read the last few days of commits in the area. A fix designed from an old checkout may already exist (a pool backoff proposed in the morning had been merged that day).
- **Before listing issues or items, sweep every earlier page and doc on the topic.** A list built from memory of the conversation misses what earlier work already found. Read each earlier artifact's judgement boxes and "what it costs" notes, and each doc's open items, then say which were added, which folded into existing items, and which were left out because they were judged healthy. Failure this prevents: a 19-item issue list was about to be walked one by one when the reader asked whether it included everything from the earlier decisions page; a pass found six more.

## Match the reader

Find out what they already know and start there. If you cannot tell, ask one question before writing.

- Assume an intelligent reader who is new to *this* thing. Define its terms of art. Do not define general engineering terms they already use.
- Bridge from what they know, in a table. Someone who knows Kubernetes learns ECS fastest as: task definition is roughly a pod spec, a service is roughly a Deployment. Say where the analogy breaks.
- When they mention their background ("I ran Temporal on EC2"), use it: put their setup and this one side by side.
- **When the reader will explain it on to someone else, give them what they need to defend it.** For each issue or fix they will present: the story in one line, the flow it sits in, one real timestamped example with a link, what it fixes and what it does not, and the likely cross-questions with short answers backed by evidence. A reader asked for exactly this so they could answer "any cross-questioning" from the people reviewing the work; a bare finding left them unable to.
- **Name each tool's job before the flow uses it.** When a mechanism spans several tools (a CI service, a build tool, a step runner, an in-house worker), give a "who does what" table first: what each is, where it runs, what it does in this flow, then one trace through all of them. A glossary line per tool is not enough when they hand work to each other. Failure this prevents: a CI page used the CI service, the build tool, a step runner and an in-house build worker as known words, and the reader had to ask what each one was.
- **For a system with many parts, give the cast, then walk one real item end to end.** List every piece once (what it is, where it lives, who writes and reads it), then follow one real ticket, request or job through all of them, naming what it leaves behind at each stop. Answer the reader's open questions at the stop where they arise. Failure this prevents: a support-agent design explained piece by piece (pages, records, logs, evals) drew a dozen "how does X relate to Y?" questions; one ticket walked from arrival to a graded, merged edit answered them.
- **Compare capabilities in one table.** Things side by side as columns, one row per capability, ✅ or ❌ with a short qualifier and the evidence (`file:line` or the config key) in the cell. A reader called this "lovely" for three workflows (which one reads, posts, writes code, opens a PR), with a small picture of how they connect above it.
- **For "what happens when...", use a named scenario and a row-by-row table.** Set one concrete scene with real-looking names ("you ask for branch X; the pool has p3e7a1 and p9c2d0, both on master"). Put the options as columns and the moments as rows ("building X", "X succeeds", "X fails", "only one left"), each cell a concrete outcome, then end with a two-line trade-off. A reader said this landed "in one go" after several prose explanations of the same thing had not.
- **Explain a job by its inputs, then give its laptop equivalent.** For anything that runs (a CI job, a script, a teardown), name the two or three things it needs and what each one decides, then say "it's the same as running `<command>` on your laptop", then say in one sentence what goes wrong today. Example that landed first time: "A teardown job needs two things: a copy of the app's code, because the delete script lives there (any recent copy works, and master is always there), and the name of the environment to delete, given separately as `BUILD_ID=a4c842`. It's the same as checking out master and running `BUILD_ID=a4c842 make teardown`. Today the job tries to get its copy from the run's branch, which is deleted once the PR merges, so it stops before it starts." Before that, "the id alone can't replace the branch because the job checks out code for the script" was marked as needing easier words.
- **Pick the device per concept, pragmatically.** A bare table of rules (precedence orders, naming schemes, which values a runner forwards) often goes over a reader's head. No single fix is mandatory: choose whatever makes this concept land with the least translation. Options: facts in order followed by a timestamped run of the real system (a named branch, a build number, the id it gets, the URL it hits, what breaks); a short analogy when the reader knows the analogue well and it needs no vocabulary of its own; a diagram; an A vs B table. Reject an analogy that grows its own cast (hotel rooms, desks, couriers) the reader must map back. Failures this prevents: a build-id table the reader said "went over my head", then a hotel metaphor for it that he called "too convoluted".

## Build from the ground up

Each idea rests on the one before it.

- Define each term where it first appears, in plain words, before anything relies on it. Show one instance first, then give it a name.
- Never open with a summary that uses words the reader has not met yet. It reads as noise and has to be decoded after the fact.
- A short glossary at the top is fine, because every entry defines itself. A recap goes at the END, once every word in it means something.
- The first screen explains the idea. Evidence comes after.

## Walk it step by step

The default shape for anything new to the reader, done for the first time, or reworked on an existing page. An overview of boxes joined by arrows is not an explanation: the reader has to assemble the meaning from names they have not met. A walk through numbered steps in order is.

- **One step, one idea, in the order the reader needs it.** For a system that is usually: why it exists (the problem), what the pieces are, how one run goes, where it breaks, how it connects to what the reader is doing next.
- **Each step has the same parts:** plain words with no system names, one small picture, one real example (a quoted line, a real date, a real row), and a one-line takeaway.
- **Names come last.** Close a step with an "in the system's words" box that maps each idea to its real name (topic = area, bookmark = watermark). Never use a name before its idea has landed.
- **In chat, one step per message**, and let the reader say "next" or ask. Fold each step into the page as it is agreed, rather than publishing the whole page first.
- **A diagram supports a step. It never replaces the steps.** Use an overview picture only after the steps, as a recap, or inside a step to show that step's flow.

Failure this prevents: a page about a background sync system led with a six-box pipeline, a glossary of internal names and a sequence diagram. The reader said it was "too technical with a bunch of boxes that I can't make sense of. The definitions and names are all alien." The same content as five plain steps landed at once: "I love the step-by-step explanations over what you posted in the original artifact."

## Show, do not characterise

- **Every claim carries its example.** "A merge takes up to two hours to deploy" is a claim. The cron line `13 */2 * * *` beside it is the explanation. Quote the real code or config, small enough to read in place, with its path.
- **Decisions are comparisons, drawn side by side.** A and B next to each other, as a diagram or a row-by-row table, with the part that differs made obvious. A paragraph that describes one option and then mentions another is not a comparison.
- **Every comparison ends in a verdict.** Say which wins here, and why. Name where the loser wins.
- **Read what a metric counts before quoting it.** A dashboard field's name is not its definition: open the query behind it, then say in the sentence what it includes and excludes. Failure this prevents: "the pool built 900 envs and served 4 instantly" went to a colleague, who said the numbers were wrong. `deployed` also counted runs' own deploys, and `instant` counted people only, hiding 13 instant hand-outs to automated runs.
- **Numbers show their working.** A cost is size × unit price × hours, with where the price came from, and says "estimate" when it is not the bill.
- **"When to use which" is a table**: the situation, the choice, and a real example from the system being explained.

## Diagrams

- **Sequence diagram first** when several components talk over time. It answers who calls whom, in what order, and where the loops are. Use a box-and-arrow picture only when the question is about structure, not flow.
- **Annotate every element.** Under each arrow's technical label, a short plain note in brackets saying what the step does, with an example: `3 · start-build (AWS via OIDC)`, then `(no stored AWS keys)`. Every box says what it is for, not only its name.
- Every box is a real actor, store or state. Every arrow is a real call or write.
- A caption says what each colour means.
- Diagrams work in dark mode and at phone width.

## Answer questions where they arise

- When the reader asked specific questions, quote each one in a small box at the top of the section that answers it, so they can find their answers.
- A judgement about whether a design is healthy goes in a box directly under the part that describes it, titled "Is this healthy?". Never in a section at the end.
- A risk, cost or gap the reader will ask about next gets the same inline box.

## Pages (artifacts)

An explainer page follows everything above, plus:

- **Problem, big-box map, then layers** (one shape among several: it suits a design or system with a handful of parts; a walkthrough, a comparison or a reference page needs its own). For a design or a system, open with the problem in a few lines, then one diagram of the solution as four to seven big boxes, each a link to its section. Each section shows a one-line summary, a small diagram and the running example; how it works, details, evidence and open questions sit in nested `<details>` layers the reader opens as deep as they want. Give the page "open every layer" and "close every layer" buttons. A reader called this shape "slick, punchy and modern" after a twelve-step page had grown too long to hold in one head.
- **One real case through every section.** Find a real ticket, incident or PR and show what each part does with it. Mark anything that did not happen as illustrative (a dashed border, "would"). A real case also exposes real gaps: the chosen ticket could not be graded because the thread never recorded what fixed it.
- **Lifecycles as state diagrams.** When something moves through states with loops (reopened, asked again), draw the states and the loops. A row of boxes with arrows reads as a straight line and hides the loops.
- **Tooltips on file names and key terms.** Every file path, config key and repo term in `<code>` gets a hover and keyboard-focus tooltip saying what it holds or does. Position it with one `position: fixed` element moved by script. A CSS `::after` tooltip gets clipped inside horizontally scrolling tables.
- **Collapse reference detail, keep the teaching open.** Narrative, diagrams, verdict boxes and the one key table stay visible. Full inventories, per-file tables, console paths and line-item costs go in `<details>`, with a summary saying what opening it shows. Collapsing is not cutting.
- **A table of contents** of short section links at the top.
- **No default card grid.** Three identical equal-width cards read as a template. Vary widths by weight of content, use a hairline border, no shadows.
- **One section per question the reader has.** Name sections for the thing, in plain words: "How code reaches prod", not "Deployment pipeline".
- **Fold new questions in.** When the reader asks more while you work, add the answer to the section it belongs in, or a new section in the right place. Never append a "follow-ups" section.
- **Merge as you fold, so the page stays tight.** Each new answer replaces or merges into what is already there: one table per concept, and a link where two sections would repeat each other. A reader asked for a page "as concise and tight as possible without losing any details" after three rounds of additions had left three overlapping tables (the rules, who uses which rule, who builds and deletes each kind); merged into one four-column table, it read cleanly. Tight means no repetition, not less content.
- **An issues list keeps everything about one issue in one entry.** What is wrong, the fix ideas, what a call or review said, and what is still unanswered all sit under that issue's heading. No separate "Ideas", "Open questions" or per-area sections that split one problem across the page. When walking issues one at a time, give each the same shape so it sticks: an everyday scene that maps one to one, what actually happens (a sequence diagram of one real case), today next to the fix as a table and a timeline, an "Is this healthy?" box, what could not be checked, and a recap. The reader asked for exactly this after seeing a page with 17 sections plus separate ideas and questions: "consolidate the headings and issues so we don't have multiple sections for issues".
- **Preview before every publish, non-negotiable.** Apply `references/preview.md`: screenshots of every section at desktop and phone width, light and dark, looked at and fixed before the page goes out.

Apply `references/respect-human-attention.md`, including its rules for systems: a design asks people only what a machine cannot decide.

## Words

- Plain words, short sentences, active voice. No flourish or metaphor where a plain noun works: "every step goes through this one call", not "every step crosses the one teal edge".
- No em dashes. Use a comma, a colon, a full stop or brackets.
- **One name per concept, everywhere.** The same word in the prose, the diagrams, the example data and the table or file names. A reader who met "diary" in the text and `cases` as the table asked which was which.
- **Real names in brackets.** Any casual or made-up word carries the real thing: "robot (ContextCollectionWorkflow)", or for something new, "the learner (proposed name `KbLearnerWorkflow`)". Use the system's own name, not a screen label ("Areas" was the UI screen, not the engine).
- **Heavy words get a plain meaning in brackets** the first time: "span (one timed step inside a request)". Prefer the plain phrase outright where one exists: "looks like the cause, isn't" over "pitfall".
- No hand waving. If you cannot explain how it works, say that you cannot.
- No fluff, no filler, no throat clearing.
- No skipping the hard part. The hard part is usually why they asked.

## Rationalisations to refuse

| The excuse | What to do |
|---|---|
| "They said it was too verbose, so I cut it" | Explain it more simply. Too verbose means simplify, never drop. |
| "The diagram speaks for itself" | Annotate every arrow and box. It does not. |
| "One overview picture covers it faster than steps" | Walk it step by step. Boxes joined by arrows are a recap, not the explanation. |
| "A summary at the top helps them orient" | Only if every word in it is already defined. Otherwise it goes at the end. |
| "The docs say so" | Check the code. Cite what you checked. |
| "An example would make it longer" | The example is the explanation. Cut prose instead. |
| "The HTML parses, so it is fine" | That is not a preview. Render it, screenshot every section, look, fix. Never publish unpreviewed. |

## Done when

Somebody who did not already know this understands it on one read. Every term is defined before it is used, every claim has its example or its `file:line`, every decision is shown side by side with a verdict, every diagram element is annotated, every question the reader asked is answered where it arises, and the unknowns are listed. For a page, the preview passes.
