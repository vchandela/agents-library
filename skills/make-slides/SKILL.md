---
name: make-slides
description: Use when someone wants a slide deck, a few slides for a meeting, or an existing deck improved, in Google Slides or any other slide tool, even when they only say "turn this doc into slides". Not for a written proposal colleagues decide on; that is write-tech-doc. Not for an explainer page; that is explain-simply.
---

# Make slides

A deck is an explanation with a speaker in front of it, so run explain-simply for the content: its read-before-you-explain, match-the-reader and no-terse-sentence rules apply to every line on a slide. Words follow `references/writing-voice.md` and `references/machine-tells.md`, pictures follow `references/visual-explanations.md`, and the render check is `references/preview.md`. This skill adds only what is particular to slides.

The rules rest on two measured findings. Slides with a full-sentence claim as the title and visual evidence as the body were understood and remembered better than topic titles with bullets (Alley and Garner, Penn State, 2013). On-screen text that repeats what the speaker says, and decoration that carries no part of the point, both lowered learning in every one of Mayer's tests.

## 1. Is a deck the right thing?

A decision that needs real argument goes in a written doc read at the start of the meeting, through write-tech-doc, with at most a few slides to frame it. A deck is for showing a story to people in a room.

Then pick the deck type, because every size and density rule below takes its value from it:

| | Speaking deck | Reading deck |
|---|---|---|
| Used for | You present it live | People read it alone, or it is sent ahead |
| Per slide | One idea, at most three short lines, one figure | Self-contained, up to six lines, tables allowed |
| Title | One line | At most two lines |
| Body text | 18 pt or more | 14 pt or more |
| What you will say | Speaker notes | On the slide, in full sentences |
| Sources | Speaker notes | A short source line on the slide |

With mixed needs, pick the closer type and never invent a middle one: live persuasion is speaking, async review is reading. A speaking deck still ships a leave-behind (the doc, or a reading version) for whoever was not in the room.

## 2. Ask, gather, outline, agree

Ask in one round, each question with your guess: who is in the room, the one decision or takeaway, the deck type, the time slot, which real stories and numbers exist, and which template to use. Stories and quotes come from the user (`references/respect-human-attention.md`). One deck serves one audience and one decision.

Gather the evidence (numbers, screenshots, a real ticket, a real quote) before writing anything, then write the deck's message as one sentence a listener could repeat from memory. The outline is one line per slide, its title claim plus the evidence that proves it, and the user agrees to the outline before anything is built.

## 3. The story

- **A decision, update or exec deck puts the answer and the ask on the first content slide.** It says whether this is an update or a decision, what is asked and by when. A teaching talk may run in the order of discovery, but each title still states its own claim.
- **Open on the audience's own problem, with one number they recognise.** Never open with a definition or an agenda.
- **Read the titles alone, in order.** They tell the whole story, and each slide's body proves its own title.
- **Build a complex diagram over several slides**, adding a part each time, and never move anything already shown. Use separate slides rather than click animations, because the PDF export and a reader on their own lose whatever lives only in an animation.
- **End on the ask**, with an owner and a date, or on the leave-behind link. No recap slide and no "Thank you, questions?" slide.

## 4. One slide

- **The title is the slide's claim as a full sentence**, with no bare topic labels and no exclamation marks. Titles across the deck vary in length, because identical lengths read as generated.
- **The body is the evidence**: a diagram, a chart, a table, a screenshot, a real example or a real quote. Decoration never counts. A divider or an ask slide may be text only.
- **One level of bullets**, because deeper levels chop the reasoning into fragments. Tables have two or three columns.
- **At most three numbers on a slide.** Each number changes the audience's judgement or it goes, and each carries its unit, its window and its yardstick (`references/explaining.md`).
- **Make the main item the biggest thing on the slide.** Items of unequal weight never sit in a grid of equal boxes. Emphasis appears at most once per slide.
- **One visual system for the whole deck.** The company template sets the fonts, colours and page size; take those and never its sample text. Each slide's layout follows its role (claim and diagram, comparison, number, ask).
- **Keep 0.5 in from every edge** and the same gap between blocks throughout. Body text is left aligned.
- **When it does not fit, split the slide.** Never shrink text below the floor for the deck type.

## 5. Slide tells

No accent line under a title, no coloured bars or stripes along an edge or a card, no icon-plus-heading-plus-one-line cards repeated on every slide, and no three equal boxes for things of unequal weight. The copy tells in `references/machine-tells.md` apply on slides too, and "Brief leaking into the output" is the slide-specific one: no "Option A", template name or brief note left on a slide.

## 6. Build it in Google Slides

- **Keep the deck as a text spec** (one entry per slide: title, evidence, notes), and turn it into API requests with a script, so a change is an edit and a re-run rather than hand-patching shapes.
- **Start each slide from the template's layouts**, then fill in the content. When a layout has more slots than items, delete the whole unused group, not only its text.
- **Guard every write** with `writeControl.requiredRevisionId`, read fresh just before the call, so a change someone made in the browser is never overwritten.
- **Slides stores an element's size as a fixed base with a scale.** Read the element's transform before moving it and keep its scale, or the box shrinks: a text box moved with `scaleX: 1` collapsed to a third of its width.
- **An empty table cell has no text**, so styling it fails the whole batch. Skip empty cells.
- **A link takes the default link colour.** Set the text colour again after adding the link.
- **The API accepts shapes placed off the page**, so check that every element sits inside it. Use real bullets (`createParagraphBullets`), never a typed "•".

## 7. Check every slide

Run `references/preview.md` with the slide thumbnails as the render (`pages.getThumbnail`; Google's own render, so fit checks hold). Look at every slide, not only the ones changed, because one layout edit moves things nobody touched.

1. Text overflow or text cut off at a box or the page edge, checked first.
2. The glance test: give each thumbnail about three seconds and say its point. If you cannot, the title or the evidence is wrong.
3. The titles listed in order and read as one paragraph.
4. A read-back of the deck's text through the API, compared with the agreed outline, so nothing was lost or left as a placeholder (including Google's "Click to add title").
5. One pass as each named person in the room, asking what they would object to first.

## Rationalisations to refuse

Each row is a mistake made on a real deck before this skill existed.

| The excuse | What to do |
|---|---|
| "Shrink the font a little and it fits" | Split the slide. A slide that needs smaller text holds two points, and it fails the glance test at the back of the room. |
| "Three equal boxes look tidy" | Size each item by its weight. Equal boxes tell the audience the items matter equally, and the grid is a known generated-slide tell. |
| "It is only a short line at the bottom" | Short lines are where terse sentences hide. "We already have a baseline, because the learner grades Artemis" drew "what does this mean?". |
| "I only changed one slide, so I only need to look at that one" | Look at every slide. A box moved without its scale collapsed to a third of its width, and only the thumbnail showed it. |
| "Every slide needs a picture" | Every content slide needs evidence. A picture that proves nothing lowers understanding. |

## Done when

The outline was agreed, every content slide has a sentence title and real evidence, the titles alone tell the story, every slide's thumbnail was looked at after the last change, and the user has the link plus a reminder to put the words in their own voice before presenting.
