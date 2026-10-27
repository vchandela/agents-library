# explain-simply: borrow ledger (27 Oct 2026)

Read-only research. Nothing in agents-library was edited. File references below point to `~/oss/agents-library/` (the skill's `references/` folder holds identical copies; `diff -q references/visuals.md skills/explain-simply/references/visuals.md` printed nothing, so edit `references/` and sync).

## 1. Sources read

Stars come from `gh api repos/<owner>/<repo> -q .stargazers_count` on 27 Oct 2026.

1. **HumanLayer "show-me"**: github.com/humanlayer/humanlayer, `apps/riptide-humanlayer-claude-plugin/skills/show-me/SKILL.md` (one file; the pi-extension copy is byte-identical). Repo 12,640 stars; bundled as `/hl:show-me` in their product and reused by their `describe-pr` and `create-design-discussion` skills. It answers "help me understand this" with the smallest text-native view: pseudocode, call tree, component tree, file tree with a comment per line, Mermaid, or a `diff` of any of those. Also read: `.claude/skills/grill-me/SKILL.md`, `.claude/skills/improve-writing/SKILL.md`, `create-design-discussion/references/design_discussion_template.md`.
   - "Skip the preamble and keep prose brief. Pick the smallest view that makes the key point clear."
   - "Use `diff` when the point is what changes and the surrounding shape already exists. Match the diff shape to the topic."
   - "Place each visual next to the short text it supports. Keep only the calls, files, props, states, and boundaries needed to answer the user's current question."
2. **Matt Pocock "grill-me" / "grilling"**: github.com/mattpocock/skills, `skills/productivity/grill-me/SKILL.md` (a one-line pointer), `skills/productivity/grilling/SKILL.md`, `skills/productivity/grill-me/agents/openai.yaml`, `docs/productivity/grill-me.md`. Also `grill-with-docs`, `wait-what` (skill and doc), and `teach` with all four format files. Repo 304,347 stars. Grilling interviews the user over a "design tree" in rounds; each round asks the whole "frontier" (questions whose prerequisites are settled) with a recommended answer.
   - "Word each question so 'yes' accepts your recommended answer."
   - "Finding _facts_ is your job, never the user's ... The _decisions_ are the user's."
   - "The session is done when the frontier is empty ... nothing left silently assumed."
   - Doc: "'One long form or three pages?' ... are **ungrillable**. You need something to react to." "At the end you could defend each choice to someone who wasn't there."
   - wait-what doc: "'Be concise' is an instruction about the agent's output, and the model obeys it by clipping words and losing you further. **Wait** is about *your* state."
   - teach: "For acquiring knowledge, difficulty is the enemy. It eats working memory"; glossary "Be opinionated ... list the rest as aliases to avoid"; "Lessons should be littered with citations".
3. **Anthropic doc-coauthoring**: github.com/anthropics/skills, `skills/doc-coauthoring/SKILL.md` (single file). Repo 184,077 stars. Three stages: context gathering, section-by-section drafting, then "Reader Testing" with a fresh Claude that has no context.
   - "Test the document with a fresh Claude (no context bleed) to verify it works for readers."
   - "For each question, invoke a sub-agent with just the document content and the question." Plus: "What knowledge or context does this doc assume readers already have?"
   - "Start with whichever section has the most unknowns ... Summary sections are best left for last."
4. **Anthropic internal-comms**: same repo, `skills/internal-comms/SKILL.md` and all four `examples/*.md`. Format templates for 3P updates, newsletters and FAQs. Only borrowable line: "Put the most important information first." Low signal for explainers.
5. **Anthropic community "eli5"** (by Thariq Shihipar): github.com/anthropics/claude-plugins-community (4,779 stars), `eli5/skills/eli5/SKILL.md`, `eli5/README.md`, `eli5/.claude-plugin/plugin.json`. The whole skill: "Explain like I'm someone who knows nothing about this topic, using a HTML artifact with big pictures and few words."
6. **obra/superpowers brainstorming** (Jesse Vincent): github.com/obra/superpowers (305,786 stars), `skills/brainstorming/SKILL.md`, `builder-check-prompt.md`, `visual-companion.md`, and the five `scripts/` files (server, helper, frame template, start and stop; infrastructure only, no writing rules). Also `skills/writing-skills/references/flowcharts.md`.
   - Builder check: "You will not be able to talk to the person who wrote it ... Report only the questions you'd still need answered ... places where you'd have to guess and a wrong guess would matter." Answers are sorted into "answered already", "minor" and "theirs".
   - "Play back as you go ... Only what they said goes in as theirs. Anything you filled in goes in as your proposal, with your reason."
   - "Per question, ask: would they understand this better by seeing it?"
7. **nicobailon/visual-explainer**: github.com/nicobailon/visual-explainer (10,646 stars), `plugins/visual-explainer/SKILL.md`, `references/diagrams.md`, `motion.md`, `style-guide.md`, `plans.md`, `extras.md`, commands `fact-check.md`, `compare.md`, `project-recap.md`, `plan-review.md`, `diff-review.md`, `generate-visual-plan.md`, and `eval/judge.md`, `eval/prompts.md`. The rendering kit (`kit/*.mjs`, vendor code) was not read, because it is render code with no writing rules. "The default output is one HTML page whose spine is figures; text is caption, not content."
   - "One claim per figure ... the `<figcaption>` states the claim in one sentence."
   - "A sentence that describes the picture becomes a label in it."
   - "Give every fact a place in a figure (label, edge verb, dimension, callout, caption) before it becomes a sentence."
   - "First viewport = the answer: the main idea as a picture plus one sentence."
   - "Headings state the takeaway ('Cache hits skip Postgres'), not the topic."
   - "Cases become small multiples: the same mini diagram once per case, not a table of sentences."
   - fact-check: mark each claim "verified, corrected, unsupported, or unverifiable" and add "a verification strip at the top: counts per status as chips".
8. **coleam00/excalidraw-diagram-skill**: github.com/coleam00/excalidraw-diagram-skill (5,121 stars), `SKILL.md` read in full. The `references/` files (palette, element templates, JSON schema, render script) are Excalidraw mechanics and were not read line by line. "Diagrams should ARGUE, not DISPLAY."
   - "The Isomorphism Test: If you removed all text, would the structure alone communicate the concept? If not, redesign."
   - "The Education Test: Could someone learn something concrete from this diagram, or does it just label boxes?"
   - Evidence artifacts: "show what things actually look like, not just what they're called."
   - "Position alone doesn't show relationships. If A relates to B, there must be an arrow."
9. **Simon Willison, Agentic Engineering Patterns**: simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/ and /interactive-explanations/ (a guide, not a repo).
   - Walkthrough prompt: "use showboat exec plus sed or grep or cat or whatever you need to include snippets of code you are talking about", which stops the agent retyping code and making mistakes.
   - "When we lose track of how code written by our agents works we take on cognitive debt."
   - Interactive explanations: animate the algorithm, make intermediate states visible, and give pause, speed and frame-step controls.
10. **SCQA and Minto pyramid skills**: github.com/stefan-jansen/claude-code-toolkit (90 stars), `examples/writing/skills/scqa-framework/SKILL.md` and `pyramid-principle/SKILL.md`. These were the highest-starred standalone ones found; `gh search code` found more than ten small copies.
   - SCQA: "Situation: the stable, uncontroversial starting point everyone agrees on", then the complication, the question, and the answer.
   - Pyramid: "Reader can stop at any level and still understand core idea."
11. **Writing sources these skills borrow from**:
   - Randy Olson's ABT, "[this is true] and [this is true], but [problem], therefore [how we address it]". It comes from the South Park writers' rule of replacing "and" with "but" or "therefore" between scenes (sesync.org/resources/communications-toolkit-and-therefore-statement).
   - Amazon's six-page narrative: "the narrative structure of a good memo forces better thought ... how things are related" (anecdote.com/2018/05/amazons-six-page-narrative-structure).
   - Malte Ubl, "Design Docs at Google": context and scope with a "system-context-diagram", goals and non-goals, alternatives "focus ... on the trade-offs" (industrialempathy.com/posts/design-docs-at-google).
   - Diataxis explanation: "explain *why* things are so"; "Explanation can and must consider alternatives"; "it tends to absorb other things" (diataxis.fr/explanation).

## 2. Rule-by-rule ledger

Covered means the rule already exists in the place cited. Gap means a proposed sentence follows. Refused means the rule was considered and dropped, with the reason.

### Story structure (things keep unlocking)

| Borrowable rule | Source | Status |
|---|---|---|
| Open on the situation everyone agrees with, then the complication, then the answer | SCQA, ABT | **Covered**: `references/writing-voice.md:21-22` ("Problem first", "Open on the situation every reader already agrees is fair, then say what changed, then give the answer") |
| A choice of two arcs: the destination first and then its parts, or the parts fixed one by one with the destination assembled at the end | user's ask; Minto (answer first) against bottom-up | **Gap (P1)**. Both arcs exist in pieces: map-first at `visuals.md:172` and steps-first at `visuals.md:171` / `SKILL.md:45`. But they are keyed to the reader's expertise, not named as two story shapes for the author to pick |
| Every step joins the next with "but" or "therefore", never "and then" | ABT / South Park; Amazon ("on page 2 you have a question but on page 4 that question is answered") | **Gap (P2)**. `visuals.md:167` checks "each step follows from the one before" but gives no test for it |
| End on what the facts change for the reader | Diataxis "why" | **Covered**: `SKILL.md:50` "End the walk with 'what this means'" |
| Headings state the takeaway, so the headings alone retell the story | visual-explainer; Minto | **Gap (P6)**. It conflicts with `explainer-pages.md:14`, which names sections by topic ("How code reaches prod") |
| Answer first, always | Minto pyramid | **Refused**. For a reader new to the subject it breaks `SKILL.md:45` (bottom up) and `explaining.md:10` (no summary in undefined words). The existing split at `visuals.md:171-172` already gives answer-first to readers judging a design |
| Make the complication urgent and "make readers feel the pain" | SCQA skill | **Refused**. That is persuasion. An explainer states the cost with a number and a yardstick (`explaining.md:21`) and does not dramatise it |
| Start drafting with the section that has the most unknowns, summary last | doc-coauthoring | **Covered**: `explaining.md:11` (recap at the end) |

### Third-person framing (a colleague opening it cold)

| Borrowable rule | Source | Status |
|---|---|---|
| Write for someone who cannot talk to the author | superpowers builder check; Amazon memo; doc-coauthoring | **Gap (P3)**. Only partly there: `visuals.md:164` bans "history of the conversation", and `explaining.md:45` covers a reader who will present it on. Nothing says the page must stand alone for someone arriving from a link |
| Only what the user said goes in as theirs; your fill-ins are marked as proposals | superpowers "Play it back" | **Covered** for pages: `visuals.md:184` ("mark anything not built as proposed") and `explainer-pages.md:7` (illustrative, dashed border) |
| "Could defend each choice to someone who wasn't there" | grill-me doc | **Covered**: `explaining.md:45` ("give them what they need to defend it") |

### Diagram as the core, text as satellite

| Borrowable rule | Source | Status |
|---|---|---|
| Diagrams carry the page; at most two sentences under each | visual-explainer; eli5 | **Covered**: `visuals.md:158-167`, `visuals.md:163` |
| One claim per figure, caption states it in one sentence | visual-explainer | **Gap (P4)**. Only charts have it today (`visuals.md:211`, "A chart's title says the finding"). Diagrams do not |
| A sentence that describes the picture becomes a label in it; every fact gets a place in a figure first | visual-explainer | **Gap (P4)**, same line. `visuals.md:163` cuts such sentences, but does not move the fact into the drawing |
| Isomorphism test: remove the text, and the structure still tells the story | excalidraw | **Gap (P5)**: a checklist line in `visuals.md` |
| Every arrow gets a verb; draw the mechanism, not a box with the name | visual-explainer; excalidraw | **Covered**: `visuals.md:185` ("labelled with what moves") and `visuals.md:183` |
| Draw the difference between options | visual-explainer compare | **Covered**: `explaining.md:17`, `visuals.md` "Before, Changes, After" |
| Evidence artifacts inside the diagram (real payloads, real names) | excalidraw | **Covered**: `visuals.md:185` ("with an example"), `explaining.md:16`, `SKILL.md:47` (one real example per step) |
| Cases as small multiples instead of a table of sentences | visual-explainer | **Covered enough**: `visuals.md` catalog #15 and #48 (named scenario table). No change |
| A number that measures a span gets a dimension line on the span | visual-explainer | **Refused for now**. `explaining.md:21` (yardstick) and the chart rule cover the need. A dimension line is a drawing technique worth trying later, not a rule |
| Pick the smallest view | show-me | **Refused**. It conflicts with `visuals.md:64` ("This is not a minimum viable diagram rule"). The part worth keeping is in P9 |
| Text-native views in chat: call tree, file tree with comments, `diff` of either | show-me | **Gap (P9)**. The catalog has a tree (#33) but nothing for chat, where a drawing cannot render, and no tree diff for "what changed" |
| Linked highlighting (`data-ref`), flow dots, three.js, registers and fonts | visual-explainer | **Refused**. These are build mechanics with a kit behind them. Page design is owned by `explainer-pages.md` and `ui-quality.md` |
| Step-through animation with frame controls | Simon Willison; visual-explainer motion | **Covered**: `SKILL.md:46`, `explainer-pages.md:8` |
| A live figure with a slider for a setting the reader should feel | visual-explainer; Simon Willison | **Gap, not proposed**. It is useful only rarely, and a stepper covers most cases |

### Glanceable proof

| Borrowable rule | Source | Status |
|---|---|---|
| Every claim carries its example and `file:line` | teach ("littered with citations"); visual-explainer | **Covered**: `SKILL.md:20`, `explaining.md:16` |
| Pull code and output by running the command (`sed -n`, `grep`, the query), never by retyping it | Simon Willison linear walkthroughs | **Gap (P7)** |
| Proof sits beside the claim where the eye already is, with the long form collapsed | visual-explainer; excalidraw | **Partly covered**: `visuals.md:231` collapses proof below the visual. Nothing puts a short proof chip next to the claim itself (P7) |
| A fact-check pass with each claim marked verified, corrected, unsupported or unverifiable | visual-explainer fact-check | **Covered in substance**: `SKILL.md:20-28` checks every claim and puts unknowns in a list. A visible verification strip is optional and is not proposed |

### Progressive disclosure (optional reading)

| Borrowable rule | Source | Status |
|---|---|---|
| The reader can stop at any level and still have the core idea | Minto pyramid | **Covered**: `visuals.md:165` ("Explain simply" dropdowns), `explainer-pages.md:6` (nested layers, open and close every layer) |
| The collapsed summary says what opening it shows | n/a | **Covered**: `explainer-pages.md:11` |
| The page reads end to end with every dropdown closed | visual-explainer ("Overview, then detail") | **Covered**: `visuals.md:167` |
| Raw material goes in `<details>`, but sources stay visible at the end | visual-explainer style guide | **Covered**: `SKILL.md:22` (unknowns at the end) and `visuals.md:239` ("Keep everything, show less") |

### Check before writing, and test the reader's understanding after

| Borrowable rule | Source | Status |
|---|---|---|
| Ask before writing when the reader's level is unclear | grill-me; doc-coauthoring stage 1 | **Partly covered**: `SKILL.md:32` ("ask one question before writing"). Nothing settles the page's story with the user before the drawing starts (P8) |
| Ask in rounds, each with your recommended answer; "yes" accepts it | grilling | **Covered** by `references/core.md` rule 4 (one "Waiting on you" list, with your pick). P8 reuses it |
| Facts are yours to find; only decisions go to the user | grilling | **Covered**: `SKILL.md:20`, `core.md` rule 2 |
| Ungrillable questions (layout, feel): show a draft to react to instead | grill-me doc; superpowers visual companion | **Covered**: `SKILL.md:49` (one step per message, folded into the page as agreed) |
| Cold-reader test: a fresh sub-agent gets only the page, answers the questions a reader would bring, and says what the page assumes | doc-coauthoring "Reader Testing"; superpowers builder check | **Gap (P10)**. `visuals.md:259` asks "A tired reader could explain the mechanism back" but gives no way to check it |
| Re-pitch when the reader is lost: name the listener's state, not the output | wait-what | **Covered**: `writing-voice.md:14` ("Concise, not clipped"), `SKILL.md:78` ("Too verbose means simplify, never drop") |
| Quizzes, spaced retrieval, a mission file, a learning-records workspace | teach | **Refused**. These suit learning across several sessions. A colleague reading a page once gets the cold-reader test instead |
| One question at a time | HumanLayer grill-me | **Refused** for the pre-writing check, because `core.md` rule 4 wants one list. During the walk itself, `SKILL.md:49` keeps one step per message |

### Considered and refused as a whole

1. HumanLayer improve-writing (keep off-duty asides, own the claim, write in the field's notation such as `!=`). This is a blog-voice guide. It conflicts with `writing-voice.md` (plain words, readers of any level), and its own frontmatter admits the file breaks its rules.
2. Google design doc sections (non-goals, cross-cutting concerns) and doc-coauthoring's 5 to 20 brainstormed points per section. These belong to proposals, which `write-tech-doc` owns according to the skill's description line.
3. internal-comms formats (3P, newsletter, FAQ). These are status updates, not explainers.
4. superpowers' hard gate and spike rules. They govern building, not explaining.

## 3. Proposed additions (10)

Each is one sentence in the existing voice, with no em dashes. Two of them (P6 and P10) change an existing line instead of adding one.

**P1. Two story arcs.** Where: `references/visuals.md`, "Steps first, or the map first", as a new first bullet, so that both existing bullets become the two arcs.
> Pick the page's arc before the first diagram and say it in one line: the problem, then the whole solution, then each part of it (for a reader who should see where it ends first), or the problem, then one fix per part, then the solution assembled from those fixes (for a reader who should build it up).

**P2. Every step unlocks the next.** Where: `skills/explain-simply/SKILL.md`, "Walk it step by step", after "One step, one idea".
> Join each step to the next with "but" or "therefore", never "and then": end every step on the gap or question that the next step resolves, so the reader always knows why the next section exists.

**P3. Written for a colleague opening it cold.** Where: `references/explaining.md`, "Build from the ground up", first bullet.
> Write for a colleague who opens the page from a link with no chat behind it: name people by role, never say "as you asked" or "the earlier version", and make the first screen say what the page explains and why that matters to them.

**P4. The figure carries the claim.** Where: `references/visuals.md`, "Length: diagrams carry the page", after the "One item is a heading" bullet.
> Caption every figure with its one claim as a full sentence, and give each fact a place in the drawing (a label, an arrow's verb, a callout) before it becomes a sentence; the sentences around a figure say only what the picture cannot.

**P5. Isomorphism test.** Where: `references/visuals.md`, the checklist block.
> - [ ] With all text hidden, the shapes, arrows and grouping of each diagram still show its structure; if they do not, the drawing is a list in boxes and gets redrawn.

**P6. Takeaway headings (changes an existing line).** Where: `references/explainer-pages.md:14`. Replace "Name sections for the thing, in plain words: 'How code reaches prod', not 'Deployment pipeline'" with:
> Write each heading as that section's takeaway in plain words ("A merge waits up to two hours to reach prod", not "Deployment pipeline"), so reading only the headings retells the story.

**P7. Proof at a glance, pulled not retyped.** Where: `references/explaining.md`, "Show, do not characterise", after "Every claim carries its example".
> Put each claim's proof where the eye already is, as a small chip beside it (the `file:line`, the query or the quoted log line), and paste code and output by running the command that prints them (`sed -n`, `grep`, the query), never by retyping.

**P8. Settle the story before drawing.** Where: `skills/explain-simply/SKILL.md`, "Match the reader". It replaces "If you cannot tell, ask one question before writing."
> Before the first diagram, write the page's story as one "and, but, therefore" line and name its reader, then confirm both with the user in one round of numbered questions, each with your recommended answer, and look up every fact yourself instead of asking.

**P9. Text views for chat.** Where: `references/visuals.md`, "Pick the form", after the form table.
> In chat, where a drawing cannot render, show structure as a text view (a call tree, a file tree with a comment on each line, or a `diff` of either when the point is what changed), placed next to the one sentence it supports.

**P10. Cold-reader test (changes an existing checklist line).** Where: `references/visuals.md:259`. Replace "A tired reader could explain the mechanism back without borrowing the document's jargon" with the line below. Also add "and the cold-reader test passes" to `SKILL.md` "Done when".
> - [ ] Cold-reader test: a fresh sub-agent given only the page answered the five questions a colleague would bring, plus "what does this page assume you already know?", without guessing, and every place it guessed or got wrong was fixed.

## 4. Things to decide

1. **P6 reverses a rule that exists today.** `explainer-pages.md:14` asks for headings that name the topic. Takeaway headings carry the story better, but they become stale when a finding changes. My pick is to adopt P6, because the user's ask is a story that flows, and headings are the cheapest place for one.
2. **P8 replaces the "ask one question" line.** It adds a round of questions before every page. My pick is to adopt it for pages and keep the old single question for chat answers, because a chat answer is cheap to redo.
3. **P10 adds a sub-agent run per page.** The check costs one agent call per page. My pick is to adopt it, because the existing checklist line cannot be ticked honestly without some test.
