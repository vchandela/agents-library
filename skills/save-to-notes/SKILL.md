---
name: save-to-notes
description: Use when something worth keeping (a video, article, thread, screenshot or book chapter) should be filed into a Zettelkasten notes vault. Not for a one-off explanation you will not keep; that is extract-insights.
---

# Save to notes

Decide whether it is worth keeping, extract it, file it, and **never write without approval**.

Vault paths and folder names come from the repo being used. Ask once if they are not obvious.

## 1. Check before extracting

**Redundancy.** Search the existing notes for the core ideas before spending effort. Search the concepts, not the title: the same idea hides under very different names. If it is already covered, say so and propose skipping it, or extracting only the new angle.

**Quality bar.** Read the vault's preferences file, if it has one, for what has been accepted and rejected before. Concrete mechanism with numbers beats survey and opinion. If a source looks like it will fail that bar, propose skipping rather than extracting anyway.

Doing this first is the whole point. Extracting and then discovering it is a duplicate wastes the expensive step.

## 2. Extract

Run `extract-insights` on the source.

**Then the thinness check.** Does this genuinely hold several distinct ideas, or really one? A tweet, a quote, a short clip often holds exactly one. If so, skip the literature note and write one permanent note. Do not manufacture a literature note around a single sentence for the sake of the pipeline.

## 3. Write

**Literature note**, for a multi-idea source. Tagged by format and topic. Opens with a source line: link, author or channel, date. Longer than a permanent note, but never repetitive.

**Permanent notes.** One idea per note, two to four for a multi-idea source, exactly one for a thin one. Title each as the claim it makes, not as a topic. Plain language, a concrete example if the idea is abstract, translate the source's jargon rather than reusing it. Link related notes to each other.

**Map of content.** Add the new notes to an existing topic map, or propose a new one grouped under a few clear headings.

Apply `references/writing-voice.md`.

## 4. Stop

**Present the full draft and wait for an explicit go-ahead.** No exceptions, however confident the extraction. Only bookkeeping files (trackers, preferences) update without asking.

## Verification

Before presenting: the redundancy check actually ran, no section repeats an idea from earlier in the same note, every jargon term is defined on first use, and every permanent note has a source line.
