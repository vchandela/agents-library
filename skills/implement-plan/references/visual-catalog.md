# Visual catalog

The forms an agent picks from when it explains something. Pick by the question the reader has, not by habit. `visual-explanations.md` holds the rules every form must follow (budget, grammar, captions); this file says which form fits which question and how to draw it.

## The rule: numbers and structure get a picture

- **Any set of three or more numbers that add up to a whole, or compare against each other, is a chart, not a sentence.** "14% name an id, 7% platform, 28% how-to, 16% billing, 35% other" is a bar or a waffle.
- **Any flow, boundary or ownership question is a diagram, not a list.** If the reader has to hold more than three named things in their head, draw them.
- **Try two or three forms for each data set before you pick.** Render each candidate (the chart library below makes this one field), look at the screenshots, and keep the one that answers the question at a glance. Say in one line why it won.
- A table is right when the reader looks values up, compares more than two attributes per row, or needs the exact numbers. It is wrong when the point is a shape (a share, a trend, a gap), because a table makes the reader compute the shape.

## How to draw

| Tool | Use for | How |
|---|---|---|
| Inline SVG | boxes and arrows, boundaries, swimlanes, custom layouts, small bars | Hand-written in the page, colours from the page's CSS tokens, so dark mode and phone width work. The default for diagrams. |
| Vega-Lite | every chart: bar, stacked bar, waffle, pie or donut, line, scatter, heatmap, histogram, dot plot | `https://cdn.jsdelivr.net/npm/vega@5`, `vega-lite@5`, `vega-embed@6`. A chart is one JSON spec, so trying a bar against a donut against a waffle means changing `mark` and `encoding`, then rendering all three. Read colours from the page's CSS variables at load time. |
| Mermaid | sequence, state, Gantt, simple flowcharts, mind maps, quadrant charts, Sankey | `https://cdn.jsdelivr.net/npm/mermaid@11`. Fast to write. Theme it from the page tokens, and check the layout in a screenshot because auto-layout can tangle. |
| Excalidraw | a hand-drawn sketch for a slide or a whiteboard feel | The Excalidraw connector, when it is signed in. Not for a page that must work in dark mode. |
| Grafana panel | live operational data the reader will keep watching | Link or screenshot the real panel. Never re-draw live data by hand. |

## The catalog

### How much, what share

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

### Change and time

| # | Form | Use when | Avoid when |
|---|---|---|---|
| 11 | Line chart | a value over time, one to four series | fewer than 4 points |
| 12 | Slope chart | before and after for several items | more than two moments |
| 13 | Timeline with honest spacing | events in order, with real gaps | the order is the only point (use a numbered list) |
| 14 | Gantt or span bars | who or what ran when, overlaps, waits | the spans don't overlap |
| 15 | Small multiples | the same chart per group (one sparkline per org) | the groups need exact comparison on one axis |
| 16 | Heatmap (calendar or hour × day) | when things happen, patterns by hour or weekday | few events |
| 17 | Waterfall | how a total is built up or eaten away step by step | the steps don't sum |

### Distribution and relationship

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

### Structure and flow

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

### Comparison and decision

| # | Form | Use when | Avoid when |
|---|---|---|---|
| 38 | Table | looking values up, more than two attributes per row | the point is a shape |
| 39 | Capability matrix (✅ ❌ with qualifiers) | options × capabilities | one option |
| 40 | Side-by-side panels (Now vs Fix, A vs B) | a change or a choice, drawn on the same grid | more than 3 options |
| 41 | Option ladder (pragmatic to long-term) | the same decision at two ambition levels, with what each needs | there is only one realistic path |
| 42 | Decision tree | a choice that depends on answers | the branches aren't real choices |
| 43 | Scorecard or traffic lights | status of many items against one bar | the bar is fuzzy |
| 44 | Radar chart | profiles of 2 or 3 options on 5 to 8 axes, roughly | exact values matter (use bars) |

### Explaining one real thing

| # | Form | Use when | Avoid when |
|---|---|---|---|
| 45 | Annotated screenshot | the reader must find something on a real screen | the screen is not the point |
| 46 | Annotated code or config snippet | the claim rests on one line of code | the snippet is long |
| 47 | Walked example (one real item end to end) | a system with many parts (`explaining.md`) | there is no real item to follow |
| 48 | Named scenario table | "what happens when" across moments × options | one moment |
| 49 | Before and after mock-up | a proposed artifact (the page, the card, the record) | the change is internal only |
| 50 | Glossary as a picture | several new words that nest (a tree of org, cloud, tenant) | the words don't relate |
