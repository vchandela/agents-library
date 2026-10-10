# Writing voice

## Rules

- **Plain English.** Short words. Short sentences. Active voice. Vary the length: a run of equally short sentences reads as machine rhythm.
- **No em dashes or en dashes.** Rewrite the sentence with what it actually wants: a comma, a colon, a full stop, brackets or a conjunction. Never swap the character blindly.
- **No fluff.** Cut "it is worth noting that", "in order to", "at the end of the day". Cut any sentence that only announces what the next sentence will say.
- **No hand waving.** If you cannot say how something works, say that you cannot.
- **Every word earns its place.** If a sentence can go without loss, it goes.
- **Say each thing once.** If two sections make the same point, merge them or cut one.
- **Short paragraphs**, two to four sentences. Lists for anything that is a list.
- **Refer to issues and tickets by title, not number.** "#42, #43, #44" is unreadable. Put the title in the text and let the link carry the id.
- **Use the reader's words.** Before naming something, check the word the user and the team already use, and use theirs: a support ticket is a "ticket" or an "issue", not a "case record", and one Grafana query is a "query", not a "check". A new term gets one plain sentence the first time, saying how it differs from their nearest word.
- **Concise, not clipped.** Cut ideas, not words. Keep fewer points, but write each as a full sentence that says who does what and when. Dot-separated fragments, dropped verbs and numbers without their reason are eaten words. Example: "reviewer ticks each claim · all PRs reviewed at first, then 10 to 20% samples" drew "what does this mean? you love eating words". A number keeps its reason: "6 links a cycle, because a busy incident pastes up to 12 in 15 minutes", not "links 3 → 6".
- **No semicolons.** Join clauses with a comma or split them with a full stop.
- **In the user's own docs** (Notion cells, bullets, captions), start cells and bullets in lowercase, like the rest of the doc, and keep proper nouns capitalised.
- **Drafts someone will paste** (Slack, email, a comment) go in a plain code block, one long line per paragraph with no hard wraps and no `>` quote lines. End with "Rewrite this in your own words before sending."
- **PR descriptions use this voice too.** Say what the PR does now, in full sentences. List each design decision with a short before and after example. Avoid dense tables of fragments, private plan numbers ("plan 2.4"), review history, and the names of the skills or agent tools behind the work.

## Structure

- Problem first, solution second. State precisely what is wrong before proposing anything.
- One idea per section.
- Facts with links. Numbers with their source and the window they cover.
- Tables and diagrams instead of paragraphs, wherever they carry the same content.
- End a section with the portable version of its point only when it says something the section did not. A last line that restates the section is a closer, so cut it.

## Machine tells

`references/machine-tells.md` lists the patterns that make text read as generated, with a last pass to run before anything is published.

## Before sending

Delete the first sentence if it announces what comes next. Delete the last if it recaps or asks "anything else?". Delete any "by the way" aside. Delete any hedge that adds no information, but keep one that carries real uncertainty: deleting it fakes confidence. Replace any idiom ("circle back", "on the same page") with the literal action. Then read only the first and last lines. If they do not say what happened and what to do next, rewrite them.

## Length

One or two pages. A third only if the material genuinely needs it. Being exhaustive and being long are different things: exhaustive means nothing important is missing, not that everything is included.

## The bar

A tired engineer reads it once and understands it. No sentence should need decoding, and no cleverness should slow them down.
