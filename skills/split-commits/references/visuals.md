# Visuals

How to show anything: the rules, which form fits which question, the tools that draw it, and the checklist that runs before a page, deck or doc goes out. A page also has layout rules and a preview step; the skill that makes the page names those files.

## Contents

- The rule: diagrams, examples, and a chart for any set of numbers
- Pick the form, including the catalog of 50 forms
- How to draw: the tools
- Length: diagrams carry the page
- Steps first, or the map first
- Budget
- Diagram quality
- Grammar
- Charts and screenshots
- Before using a term
- Code and progressive detail
- Notion pages and docs others read
- Checklist before publishing

## The rule

Prefer diagrams and concrete examples over explanatory prose. The goal is not to minimise words or draw the smallest possible diagram. The goal is that a tired reader understands the idea without decoding the surrounding text. Teach the mechanism first. Name it second.

Every spec, plan and plan review includes (each skill names what its diagram shows):

- at least one diagram showing the core flow;
- at least one real-looking worked example with concrete values.

When introducing a new mechanism or term, choose the clearest visual form:

- **Sequence diagram, first,** when several actors interact over time: it answers who calls whom, in what order, and where the loops are. Use a box-and-arrow picture only when the question is about structure, not flow.
- **Flow diagram:** when a condition sends work down different paths.
- **State diagram:** when one thing moves through a lifecycle.
- **Code or pseudocode:** only when exact ordering, checks or stored values remain unclear after the visual.
- **Concrete data example:** when defining a table, request, response or message.
- **Analogy:** when it gives the reader a familiar bridge. Follow it with the real mechanism.

Do not use all of them for every point. Prefer a diagram plus a real example. Add prose only for the facts the visual cannot carry. Plain text is enough when the idea is already obvious.

No decorative pictures. An image, icon or stock photo that carries no part of the explanation lowers understanding. Decoration never counts as the visual.

Numbers and structure get a picture:

- **Any set of three or more numbers that add up to a whole, or compare against each other, is a chart, not a sentence.** "14% name an id, 7% platform, 28% how-to, 16% billing, 35% other" is a bar or a waffle.
- **Any flow, boundary or ownership question is a diagram, not a list.** If the reader has to hold more than three named things in their head, draw them.
- **Try two or three forms for each data set before you pick.** Render each candidate (the chart library below makes this one field), look at the screenshots, and keep the one that answers the question at a glance. Say in one line why it won.
- A table is right when the reader looks values up, compares more than two attributes per row, or needs the exact numbers. It is wrong when the point is a shape (a share, a trend, a gap), because a table makes the reader compute the shape.

## Pick the form

Decide what the reader must understand first, then the picture. If a three-column table says the same thing, use the table. A one-box diagram is a sentence.

| The reader must understand | Draw |
|---|---|
| Why two similar requests ended differently | The same ordered checks as two traces side by side. Each check is PASS, FAIL, SKIPPED (bypassed on purpose) or NOT REACHED (an earlier check stopped it). Mark the first divergence. |
| What a change did to a system | Before, Changes, After. Two snapshots on the same grid, with unchanged boxes in the same place, and a short ledger between them, one line per change: ADDED, REMOVED, CHANGED (old to new), MOVED, REWIRED. |
| Why work waits | Sources fanning into one queue with its count, the capacity as a number with units (8 per hour), and both outcomes (served, deferred). |
| How one thing moves through phases, waits, retries and ends | A phase rail left to right, a separate band for waits and retries, and a separate band for endings, with cancelled and failed as different boxes. |
| What layered defences leave behind | Layers in order. Each says what it stops and what gets past. End with the risk that remains. Never imply the last layer makes risk zero. |
| Who does what across a handoff | One lane per owner. A step sits in exactly one lane. The handoffs are the arrows that matter. |
| Events over time | A timeline with honest spacing: unequal gaps are drawn unequal. |

This is not a "minimum viable diagram" rule. A tiny diagram that still requires the reader to decode a paragraph has failed. Make the visual complete enough to stand on its own.

### The catalog

#### How much, what share

| # | Form | Use when | Avoid when |
|---|---|---|---|
| 1 | Bar chart (horizontal) | comparing 3 to 15 categories, long labels | the categories are ordered in time (use a line) |
| 2 | Stacked bar, one row | parts of one whole, 2 to 6 parts ("83 of 266 clouds send logs") | more than 6 parts, or parts too small to label |
| 3 | 100% stacked bars, several rows | the same split across groups (each org's run mix) | the totals differ and the totals matter |
| 4 | Waffle (10×10 squares) | one share out of 100, felt as a count ("14 of 100 tickets") | shares under 1% |
| 5 | Pie or donut | 2 to 4 parts of one whole, where one part dominates | more than 5 parts, or comparing two pies (use stacked bars) |
| 6 | Big number with context | one headline figure plus its yardstick ("29% today, 80% to ship") | the number needs its distribution to mean anything |
| 7 | Bullet chart | a value against a target and ranges | there is no target |
| 8 | Dot plot or lollipop | many categories with values close together | the reader needs parts of a whole |
| 9 | Treemap | a hierarchy of sizes (where the tickets go, by area and sub-area) | fewer than 6 leaves (use bars) |
| 10 | Pictogram or unit chart | a count a non-technical reader should feel (each icon is a ticket) | counts over about 200 |

#### Change and time

| # | Form | Use when | Avoid when |
|---|---|---|---|
| 11 | Line chart | a value over time, one to four series | fewer than 4 points |
| 12 | Slope chart | before and after for several items | more than two moments |
| 13 | Timeline with honest spacing | events in order, with real gaps | the order is the only point (use a numbered list) |
| 14 | Gantt or span bars | who or what ran when, overlaps, waits | the spans don't overlap |
| 15 | Small multiples | the same chart per group (one sparkline per org) | the groups need exact comparison on one axis |
| 16 | Heatmap (calendar or hour × day) | when things happen, patterns by hour or weekday | few events |
| 17 | Waterfall | how a total is built up or eaten away step by step | the steps don't sum |

#### Distribution and relationship

| # | Form | Use when | Avoid when |
|---|---|---|---|
| 18 | Histogram | how values spread (run durations 87 to 307 s) | fewer than about 20 values (use a dot strip) |
| 19 | Box plot or dot strip | spread and outliers across a few groups | the audience doesn't read box plots (use a dot strip) |
| 20 | Scatter | two measures per item, looking for a relation | one measure |
| 21 | Matrix or heatmap grid | many items × many attributes with a value in each cell (access: which agent reads which store) | a few cells (use a table) |
| 22 | Quadrant (2×2) | placing options on two judgement axes (effort × value) | the axes aren't really independent |
| 23 | Venn or overlap bars | what two sets share (tickets with an obs run) | more than 3 sets (use an UpSet-style bar list) |
| 24 | Sankey or flow bands | how a quantity splits and flows through stages (301 runs to 268 hand-overs to 0 tickets) | no quantity moves |
| 25 | Funnel | drop-off across ordered stages | the stages aren't a subset of each other |

#### Structure and flow

| # | Form | Use when | Avoid when |
|---|---|---|---|
| 26 | Flowchart | steps and decisions in a process | several actors talking over time (use a sequence) |
| 27 | Sequence diagram | who calls whom, in what order | the question is structure, not order |
| 28 | Swimlane | who does which step across a hand-off | one owner |
| 29 | Boundary or zone diagram | who can reach what across a trust line (inside Anyscale vs the customer) | there is no boundary |
| 30 | Architecture or component map | what the parts are and how they connect | a reader new to the system before the steps (`explain-simply`) |
| 31 | Data-flow diagram | where data is written, copied and read | there is no data movement |
| 32 | State machine | the states one thing passes through, and what moves it | fewer than 3 states |
| 33 | Tree or hierarchy | containment (org has clouds, a cloud has tenants) | relations cross the branches |
| 34 | Network graph | many-to-many links | more than about 15 nodes (cluster first) |
| 35 | Layer diagram | stacked defences or abstraction layers | the layers don't stack |
| 36 | Mind map | the branches of a question tree | there is an order |
| 37 | Entity-relationship diagram | tables and the keys that join them | non-technical readers (use a tree or matrix) |

#### Comparison and decision

| # | Form | Use when | Avoid when |
|---|---|---|---|
| 38 | Table | looking values up, more than two attributes per row | the point is a shape |
| 39 | Capability matrix (✅ ❌ with qualifiers) | options × capabilities | one option |
| 40 | Side-by-side panels (Now vs Fix, A vs B) | a change or a choice, drawn on the same grid | more than 3 options |
| 41 | Option ladder (pragmatic to long-term) | the same decision at two ambition levels, with what each needs | there is only one realistic path |
| 42 | Decision tree | a choice that depends on answers | the branches aren't real choices |
| 43 | Scorecard or traffic lights | status of many items against one bar | the bar is fuzzy |
| 44 | Radar chart | profiles of 2 or 3 options on 5 to 8 axes, roughly | exact values matter (use bars) |

#### Explaining one real thing

| # | Form | Use when | Avoid when |
|---|---|---|---|
| 45 | Annotated screenshot | the reader must find something on a real screen | the screen is not the point |
| 46 | Annotated code or config snippet | the claim rests on one line of code | the snippet is long |
| 47 | Walked example (one real item end to end) | a system with many parts | there is no real item to follow |
| 48 | Named scenario table | "what happens when" across moments × options | one moment |
| 49 | Before and after mock-up | a proposed artifact (the page, the card, the record) | the change is internal only |
| 50 | Glossary as a picture | several new words that nest (a tree of org, cloud, tenant) | the words don't relate |

## How to draw: the tools

| Tool | Use for | How |
|---|---|---|
| Inline SVG | boxes and arrows, boundaries, swimlanes, custom layouts, small bars | Hand-written in the page, colours from the page's CSS tokens, so dark mode and phone width work. The default for diagrams. |
| Vega-Lite | every chart: bar, stacked bar, waffle, pie or donut, line, scatter, heatmap, histogram, dot plot | `https://cdn.jsdelivr.net/npm/vega@5`, `vega-lite@5`, `vega-embed@6`. A chart is one JSON spec, so trying a bar against a donut against a waffle means changing `mark` and `encoding`, then rendering all three. Read colours from the page's CSS variables at load time. |
| Mermaid | sequence, state, Gantt, simple flowcharts, mind maps, quadrant charts, Sankey | `https://cdn.jsdelivr.net/npm/mermaid@11`. Fast to write. Theme it from the page tokens, and check the layout in a screenshot because auto-layout can tangle. |
| Excalidraw | a hand-drawn sketch for a slide or a whiteboard feel | The Excalidraw connector, when it is signed in. Not for a page that must work in dark mode. |
| Grafana panel | live operational data the reader will keep watching | Link or screenshot the real panel. Never re-draw live data by hand. |

## Length: diagrams carry the page

A page is for scanning, and a long one puts the reader off before they start. Keep the visible text of a page (an artifact, a hosted explainer, a doc for colleagues) as short as it can be, not counting collapsed evidence, and let diagrams, timelines and Now versus Fix panels carry the explanation. There is no word budget, but every sentence stays complete and the explanation reads coherently from one step to the next: cut words, never the verb or the link between two steps.

- Open with the title and a one-line diagram key, or the first diagram. A lede, an "in short" box or a verdict paragraph that restates the page is cut.
- One item is a heading, one diagram (or a Now and Fix pair), and at most two sentences under it. A sentence that only describes what the diagram already shows is cut.
- No section intro that announces what follows, no closing recap, and no history of the conversation (corrections go in chat).
- Put the plain-words version of each point in a collapsed "Explain simply" dropdown (`<details>`) under it, for a reader who has never met the term: say what each thing is, give one real example, use no analogy, and keep it to about 50 to 120 words. Skip the dropdown when the visible sentences already use only plain words: a reader removed every dropdown on a page whose text already read clearly, because each one repeated its paragraph. Collapsed dropdowns and evidence keep the visible page short for a reader who knows the topic, and a reader who does not can open the explanation they need.
- Review each item before it earns a place. Merge items that one fix covers. Turn a test into a rollout line instead of a "gap". Rate each item's severity against the real stakes and demote the low ones. Drop an interim fix that saves little once you have measured it.
- Read the visible text once before publishing, without the dropdowns. Cut any sentence a diagram already shows, then check that no sentence is a fragment and that each step follows from the one before.

## Steps first, or the map first

- **A reader new to the subject** (learning how something works): numbered steps in order (why it exists, the pieces, one run, where it breaks), each with plain words, one small picture, a real example and a one-line takeaway. System names come at the end of each step. An overview of boxes and arrows goes after the steps as a recap, never in their place.
- **A reader who knows the domain and is judging a design** (a spec, a plan, a tech doc, a system page): the problem in a few lines, then one map of four to seven big boxes, then a section per box, layer by layer.

## Budget

- At most 9 boxes and 12 arrows per diagram. Highlight 1 or 2 elements. If you want to highlight 4, you have not decided what matters.
- Sequence: at most 5 participants and one branch frame (alt with at most 2 regions, or opt, or loop), never nested. Swimlane: at most 5 lanes. State: more transitions than twice the states means two machines.
- Over budget: split into an overview and a detail. Never drop a real arrow to fit.
- Before drawing, say in one line which form, and what the budget will push into a second diagram.

## Diagram quality

- Every box is a real actor, store or state, and says what it is for, not only its name.
- **Stay true to the code.** Read the workflow or code before drawing: one box per real step, in the real order, with its real name. Label each box as a script or an agent step, and an agent step with its model and effort ("agent: Claude Opus 5.5, effort xhigh"); mark anything not built as proposed. Draw the real retry and loop-back paths. An overview may group steps only if each group names the steps it stands for. Failure this prevents: a reviewer asked which boxes were scripts and which model ran the agent steps, and a seven-step workflow drawn as four could not answer.
- Every arrow is a real call, write or state change, labelled with what moves. **Annotate every element:** under each arrow's technical label, a short plain note in brackets says what the step does, with an example: `3 · start-build (AWS via OIDC)`, then `(no stored AWS keys)`.
- Show failure at the exact step where it happens.
- Show the corrected path beside or directly after the failing path.
- One example teaches one failure. Split unrelated failures.
- A diagram is not a compressed list of unexplained labels.
- Arrows bend at right angles, never diagonally. Two arrows never share a line or a point on a box. An arrow does not pass behind a box that is not one of its ends.
- An arrow's label sits beside the line with a visible gap, never on top of it.
- The legend is a strip below the diagram, never inside it, and a caption says what each colour means.
- Boxes differ by kind (store, service, person, external). Identical boxes for everything erase the hierarchy.
- **Diagrams and slides others read are as plain as possible:** each box or slide element keeps its heading and nothing else: no subheading or bracketed note under it, no code paths, no captions inside the drawing. A few numbers on the arrows are fine (each with its unit, "1,588 runs" or "142 tickets"). Everything else is said in bullets under the diagram, where the presenter explains it. This applies to Google Slides, Notion and artifact diagrams alike. Failures this prevents: a solution diagram with field lists inside boxes and three lines in a "tool layer" box ("make the diagrams as dumb as possible"); a design tree with a grey note under every box and code paths inside the leaves ("we keep the headings but remove the subheadings and keep the diagrams dumb so we can explain them ourselves").
- **Draw the problem and the fix on the same grid.** The same boxes in the same places, gaps in red and fixes in green, so the reader compares them at a glance. Put the columns the reader will compare (tools, runbooks) in labelled frames, so membership comes from the frame, not from repeated markers.
- **A numbered marker marks one thing.** Number N appears only where problem N lives. Failure this prevents: a "3" placed on two runbook arrows when 3 was the tools problem, so the reader could not tell what each number meant.
- **Draw a flow vertically when its actors form a chain** (agent, ticket, agent), and let each one branch out sideways to what it uses. A horizontal row of actors with arrows above and below crowded the page.
- The diagram's title and description say what it shows ("Requests from three teams queue at one reviewer"), not its geometry ("a box with three boxes above it").

**Remove test.** Before publishing, ask of every box: can it go, or merge with one it always travels with? Ask of every arrow: does the layout already show it? Remove those. The plain-words note under a label is not up for removal; it is how a tired reader reads the arrow.

## Grammar

- Sequence: time flows down, and no arrow points up. A reply is dashed (`-->>` in Mermaid). A fire-and-forget message has an open head (`-)`). A branch goes in a labelled frame (`alt`, `opt`, `loop`) with guards such as `[token valid]` and `[else]`. Never two loose clusters of arrows.
- State: label every transition `event [guard] / action`. A transition from any state is one note (`* to Error on timeout`), not an arrow from every box.
- Flowchart: shape carries the type (rounded for start and end, box for a step, diamond for a decision). A diamond has at most 3 exits, each labelled.
- Colour never carries meaning alone. Pair it with a word, a dash pattern or a shape, so the diagram survives print, dark mode and colour blindness.

## Charts and screenshots

- A chart's title says the finding ("Triage time halved after the page merged"), not what the axes are.
- Label the values on the chart itself. A single series has no legend, gridlines are quiet, and the colours come from the page's own tokens.
- Crop a screenshot to the part that matters and mark that part with one callout. Cut any caption that only names what the reader can already see.

## Before using a term

Bad:

> Create a durable message intent and reconcile it on retry.

Better:

> Before posting, store one row that says: `INC-712 / rollback-started / not sent`. After posting, add the Slack timestamp and mark it sent. We call this row a send record.

Never leave a noun such as version, intent, generation, reconciliation, admission or delivery policy standing on its own. Show what value it holds, who changes it and which decision reads it.

## Code and progressive detail

Pseudocode is optional and secondary. Do not add it when the diagram and example already explain the mechanism. When it is useful, keep it small and hide or place it after the primary visual. Include only the fields and branches needed to explain the decision. Mark pseudocode as pseudocode. If a call or API does not exist yet, say so; do not make invented code look real.

Keep the main visual and example visible. Collapse or move supporting proof, code and edge-case detail below them. The first screen should explain the idea, not display every piece of evidence.

## Notion pages and docs others read

The same rule applies hardest to a Notion page or a doc for the team, whether a skill or a person writes it: diagrams over text.

- **Draw the flow, don't narrate it.** A process that crosses repos, people or systems (who opens which PR, what approves it, what applies it) is an Excalidraw diagram, or a Mermaid flow or sequence diagram where the page renders one. Draw it with the Excalidraw tool and hand over the file; the author exports it into Notion.
- **Visible text is one-line points.** Supporting detail goes in a toggle whose summary is the one-line point, for example a toggle "However, this is for alerts only." that hides which folders and workflows that covers.
- **Keep everything, show less.** Collapsing is not cutting: every fact stays, under the toggle that owns it.

Failure this prevents: a PR flow told in five numbered paragraphs, which the reader asked to see as a diagram with toggles.
- **Build on a live page, ship to Notion at the end.** Iterate the diagrams on a published artifact (one step per section, checked in the browser after every change), because round trips on Excalidraw files are slow. When the reader is happy, convert every diagram to Excalidraw in one file they copy from, and put tables straight into Notion as styled tables (colour the yes, no and partial cells, grey group rows). Collapse a long reference table into a toggle heading; keep the table the reader acts on (the order of work) open.
- **Replace an SVG by its section, never by a shared attribute.** Two diagrams can share a size, so an edit anchored on `viewBox="0 0 900 400"` overwrote the wrong one. Anchor on the section id, then confirm the other diagrams are unchanged.

## Checklist before publishing

Run this before any page, deck or doc goes out, and again after each round of fixes. Copy it into your working notes and tick each line; a line that fails sends you back to fix it, then the whole list runs again.

```
Visuals checklist
- [ ] Every set of three or more numbers that compare or make a whole is a chart. List each set and the chart it became.
- [ ] Each chart was rendered in two or three forms (for example bar, stacked bar, donut) and the pick is named with a one-line reason.
- [ ] Each chart title states the finding, values are labelled on the chart, and colours come from the page's tokens.
- [ ] Every flow, boundary or ownership question is a diagram, chosen with "Pick the form".
- [ ] Each diagram is within the budget, and every box and arrow carries its plain-words note.
- [ ] A table is used only where the reader looks values up.
- [ ] A page's visible text is as short as it can be, every sentence is complete, and each step follows from the last.
- [ ] For a page or deck, the preview the skill names passed for this version.
- [ ] A tired reader could explain the mechanism back without borrowing the document's jargon.
```
