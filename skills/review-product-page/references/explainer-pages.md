# Explainer pages

A page follows everything in the skill, plus:

- **Stay inside the length budget** in `references/visuals.md`, "Length: diagrams carry the page". Where this file's layers would push a page past it, collapse the detail into `<details>` or cut it.
- **Problem, big-box map, then layers** (`references/visuals.md`, "Steps first, or the map first"), for a design or system with a handful of parts. Each box links to its section. Each section shows a one-line summary, a small diagram and the running example; how it works, details, evidence and open questions sit in nested `<details>` layers the reader opens as deep as they want. Give the page "open every layer" and "close every layer" buttons.
- **One real case through every section.** Find a real ticket, incident or PR and show what each part does with it. Mark anything that did not happen as illustrative (a dashed border, "would"). A real case also exposes real gaps: the chosen ticket could not be graded because the thread never recorded what fixed it.
- **Steppers for anything that moves.** One small script holds the frames as data (who holds what, what the clock reads, the caption). Next, Back and Reset buttons move through them; the caption sits in an `aria-live` region; the page does not autoplay and shows each change instantly under `prefers-reduced-motion`. State is never carried by colour alone (add a word or an icon), and the stepper works at phone width and in dark mode. In the preview, step through every frame and look at each one.
- **Lifecycles as state diagrams.** When something moves through states with loops (reopened, asked again), draw the states and the loops. A row of boxes with arrows reads as a straight line and hides the loops.
- **Tooltips on file names and key terms.** Every file path, config key and repo term in `<code>` gets a hover and keyboard-focus tooltip saying what it holds or does. Position it with one `position: fixed` element moved by script. A CSS `::after` tooltip gets clipped inside horizontally scrolling tables.
- **Collapse reference detail, keep the teaching open.** Narrative, diagrams, verdict boxes and the one key table stay visible. Full inventories, per-file tables, console paths and line-item costs go in `<details>`, with a summary saying what opening it shows. Collapsing is not cutting.
- **A table of contents** of short section links at the top.
- **No default card grid.** Three identical equal-width cards read as a template. Vary widths by weight of content, use a hairline border, no shadows.
- **One section per question the reader has.** Name sections for the thing, in plain words: "How code reaches prod", not "Deployment pipeline".
- **Fold new questions in.** When the reader asks more while you work, add the answer to the section it belongs in, or a new section in the right place. Never append a "follow-ups" section.
- **Merge as you fold, so the page stays tight.** Each new answer replaces or merges into what is already there: one table per concept, and a link where two sections would repeat each other. Tight means no repetition, not less content.
- **An issues list keeps everything about one issue in one entry.** What is wrong, the fix ideas, what a call or review said, and what is still unanswered all sit under that issue's heading. No separate "Ideas", "Open questions" or per-area sections that split one problem across the page. When walking issues one at a time, give each the same shape so it sticks: an everyday scene that maps one to one, what actually happens (a sequence diagram of one real case), today next to the fix as a table and a timeline, an "Is this healthy?" box, what could not be checked, and a recap.
- **Preview before every publish.** Apply `references/preview.md`: screenshots of every section at desktop and phone width, light and dark, looked at and fixed before the page goes out.

Apply `references/respect-human-attention.md`, including its rules for systems: a design asks people only what a machine cannot decide.

