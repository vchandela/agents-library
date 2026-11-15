# Every page reads the same way

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
