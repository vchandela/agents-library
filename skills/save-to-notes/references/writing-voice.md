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

## Structure

- Problem first, solution second. State precisely what is wrong before proposing anything.
- Open on the situation every reader already agrees is fair, then say what changed, then give the answer.
- A proposal says what doing nothing costs, with a number, and why it should happen now.
- One idea per section.
- Facts with links. Numbers with their source and the window they cover.
- Tables and diagrams instead of paragraphs, wherever they carry the same content.

## Machine tells

`references/machine-tells.md` lists the patterns that make text read as generated, with a last pass to run before anything is published.

## Shape and rhythm

Detectors and readers catch the shape of a page before its words.

- **Prose for an argument, a list only for parallel items.** A doc where every section is bullets with a bold lead-in reads as generated, even when each sentence is clean. Keep bold lead-ins for at most one list in a doc, and put a sentence between a heading and any list under it.
- **Vary the length.** At least one sentence in eight has eight words or fewer, and a paragraph can be one sentence when the point needs only one. Then write the rest as the long, connected sentences people use when they explain something out loud.
- **Name the subject.** Don't open a sentence with a bare "This", "That" or "These", and never open a paragraph that way. Don't open with a count ("Two risks."). Don't give a system a person's verb ("the data tells us").
- **Don't stack the clean-model constructions.** One cleft ("What takes the time is…"), one trailing ", making it easier to…", or one "X lives in Y" is fine. Several on a page is a cadence.
- **Don't put on the costume.** Forced lowercase, staccato fragments, slang or contorted sentences that dodge a dash are their own tell. Make a real choice of words instead.
- **Check it.** Run the human-voice linter on the text (`python3 skills/human-voice/scripts/detect_ai_prose.py --register business --no-config <file>` from a clone of the repo), and fix every flagged shape. A clean score is only a floor. Statistical detectors such as Pangram still flag model-written text, so the overview, goals and asks of a doc the author sends must be in the author's own words (`references/respect-human-attention.md`).

## Before sending

Delete a closing "anything else?". Delete any "by the way" aside. Delete any hedge that adds no information, but keep one that carries real uncertainty: deleting it fakes confidence. Replace any idiom ("circle back", "on the same page") with the literal action. Then read only the first and last lines. If they do not say what happened and what to do next, rewrite them.

## Length

One or two pages. A third only if the material genuinely needs it. Being exhaustive and being long are different things: exhaustive means nothing important is missing, not that everything is included.

A page (an artifact or hosted explainer) has its own budget of about 1,100 visible words, set in `references/visuals.md` under "Length: diagrams carry the page".

## The bar

A tired engineer reads it once and understands it. No sentence should need decoding, and no cleverness should slow them down.
