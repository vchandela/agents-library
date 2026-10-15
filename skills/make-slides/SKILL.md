---
name: make-slides
description: Use when someone wants a slide deck, a few slides for a meeting, or an existing deck improved, in Google Slides or any other slide tool, even when they only say "turn this doc into slides". Not for a written proposal colleagues decide on; that is write-tech-doc. Not for an explainer page; that is explain-simply.
---

# Make slides

A deck is an explanation with a speaker in front of it, so run explain-simply for the content: its read-before-you-explain, match-the-reader and no-terse-sentence rules apply to every line on a slide. Words follow `references/writing-voice.md` and `references/machine-tells.md`, pictures follow `references/visual-explanations.md`, and the render check is `references/preview.md`. This skill adds only what is particular to slides.

The rules rest on two measured findings. Slides with a full-sentence claim as the title and visual evidence as the body were understood and remembered better than topic titles with bullets (Alley and Garner, Penn State, 2013). On-screen text that repeats what the speaker says, and decoration that carries no part of the point, both lowered learning in every one of Mayer's tests. In a speaking deck the speaker says the claim out loud, so the slide keeps only a short heading and the evidence (section 5); a reading deck, read without a speaker, keeps the full-sentence title.

## 1. Is a deck the right thing?

A decision that needs real argument goes in a written doc read at the start of the meeting, through write-tech-doc, with at most a few slides to frame it. A deck is for showing a story to people in a room.

Then pick the deck type, because every size and density rule below takes its value from it:

| | Speaking deck | Reading deck |
|---|---|---|
| Used for | You present it live | People read it alone, or it is sent ahead |
| Per slide | One idea, one figure, labels of four words or fewer, no sentences | Self-contained, up to six lines, tables allowed |
| Title | 1 to 3 words naming the point; the claim is said aloud and opens the notes | A full-sentence claim, at most two lines |
| Text size | Box text 14 pt, labels 12 pt, nothing smaller | 14 pt or more |
| What you will say | Speaker notes | On the slide, in full sentences |
| Sources | Speaker notes | A short source line on the slide |

With mixed needs, pick the closer type and never invent a middle one: live persuasion is speaking, async review is reading. A speaking deck still ships a leave-behind (the doc, or a reading version) for whoever was not in the room.

## 2. Ask, gather, outline, agree

Ask in one round, each question with your guess: who is in the room, the one decision or takeaway, the deck type, the time slot, which real stories and numbers exist, and which template to use. Stories and quotes come from the user (`references/respect-human-attention.md`). One deck serves one audience and one decision.

Gather the evidence (numbers, screenshots, a real ticket, a real quote) before writing anything. Check every number at its source and every claim about what a system does in its code: a deck said "Artemis reads these pages during triage" when no triage workflow did, and a cost cell showed zero dollars because the API's cost field was unset for that workflow while a measured 7 to 13 dollars a run sat in the design doc. Then, then write the deck's message as one sentence a listener could repeat from memory. The outline is one line per slide, its title claim plus the evidence that proves it, and the user agrees to the outline before anything is built.

## 3. The story

- **A decision, update or exec deck puts the answer and the ask on the first content slide.** It says whether this is an update or a decision, what is asked and by when. A teaching talk may run in the order of discovery, but each title still states its own claim.
- **Open on the audience's own problem, with one number they recognise.** Never open with a definition or an agenda.
- **Read the titles alone, in order.** They tell the whole story, and each slide's body proves its own title.
- **Build a complex diagram over several slides**, adding a part each time, and never move anything already shown. Use separate slides rather than click animations, because the PDF export and a reader on their own lose whatever lives only in an animation.
- **Fewest slides possible.** Every slide must earn its place; cut or merge until removing one more would lose a point. A 17-slide deck lost the room after the fourth slide past the demo. Aim for 5 to 7 content slides in a 15 to 20 minute slot.
- **Lead with the arsenal.** Attention is highest in the first minutes, so the strongest evidence goes first, slide after slide (the live demo, the real result, the hardest number), and the supporting detail comes after or goes to the notes. Never warm up with background.
- **End on the ask**, with an owner and a date, or on the leave-behind link. No recap slide and no "Thank you, questions?" slide.
- **A status or proposal deck runs in an order the room finds obvious**: the problem with its number, what we built, how it works, how quality is kept, how it scales and is evaluated, how success is measured, today's numbers against those measures, what is not proven yet, the ask. Measures come before the numbers they judge.
- **Honest without self-flagellation.** Each gap sits next to its next step, and one box says what already holds, so the team can stand behind every slide. Leave low-level bug detail for the notes.

## 4. One slide

- **Title by deck type.** In a speaking deck the title is 1 to 3 words naming the point ("Eval loop", "Small diffs"), and the full-sentence claim is the first line of the speaker notes. In a reading deck the title is the claim as a full sentence. No exclamation marks either way.
- **The body is the evidence**: a diagram, a chart, a table, a screenshot, a real example or a real quote. Decoration never counts. A divider or an ask slide may be text only.
- **One level of bullets**, because deeper levels chop the reasoning into fragments. Tables have two or three columns.
- **At most three numbers on a slide.** Each number changes the audience's judgement or it goes, and each carries its unit, its window and its yardstick (`references/explaining.md`).
- **A screenshot proves the title only if the reader can find the proof in it.** Crop to the part that proves it, and mark the proof with a thin outline in the colour of the box or label that names it. Colour-matched outlines link text to evidence without arrows crossing the image.
- **Make the main item the biggest thing on the slide.** Items of unequal weight never sit in a grid of equal boxes. Emphasis appears at most once per slide.
- **One visual system for the whole deck.** The company template sets the fonts, colours and page size; take those and never its sample text. Each slide's layout follows its role (claim and diagram, comparison, number, ask).
- **Keep 0.5 in from every edge** and the same gap between blocks throughout. Body text is left aligned.
- **When it does not fit, split the slide.** Never shrink text below the floor for the deck type.

## 5. House format for speaking decks

The reference is the user's house deck, linked in their notes or memory. Copy its look; read a slide from it with the API when in doubt.

- **Nothing on the slide that the speaker will say.** No subtitles, no sentences, no bullet lists. The slide holds a 1 to 3 word heading, a diagram or a real screenshot, and labels of four words or fewer. Everything else goes in the notes.
- **Numbered steps.** A flow is boxes with a number on each step, in reading order, so the speaker can say "step 3" and the room finds it.
- **Type:** Archivo throughout. Heading 24 pt white, box text 14 pt bold white, side labels 12 pt grey (RGB 0.604).
- **Colour carries status, the same on every slide:** green for done or live (fill 0.05, 0.2, 0.12; line 0.2, 0.75, 0.45), blue for planned (fill 0.063, 0.149, 0.29; line 0.2, 0.522, 1), amber for not proven or a miss (fill 0.27, 0.19, 0.04; line 0.95, 0.7, 0.2), dark grey for neutral (fill 0.106, 0.106, 0.114; line 0.227, 0.227, 0.239). Rounded rectangles, outline 12,700 EMU (1 pt).
- **Real screenshots as evidence**, cropped, with no cursor, the proof marked by a thin outline in the status colour of the box that names it.
- **No divider slides.** A section starts on its first content slide, titled with the section's name.
- **Speaker notes per explain-simply:** crisp, plain sentences, limited to that slide. The claim first, then what to point at, then any research with one line on how it connects to this slide. Never repeat another slide's notes.

## 6. Slide tells

No accent line under a title, no coloured bars or stripes along an edge or a card, no icon-plus-heading-plus-one-line cards repeated on every slide, and no three equal boxes for things of unequal weight. The copy tells in `references/machine-tells.md` apply on slides too, and "Brief leaking into the output" is the slide-specific one: no "Option A", template name or brief note left on a slide.

## 7. Build it in Google Slides

- **Keep the deck as a text spec** (one entry per slide: title, evidence, notes), and turn it into API requests with a script, so a change is an edit and a re-run rather than hand-patching shapes.
- **Start each slide from the template's layouts**, then fill in the content. When a layout has more slots than items, delete the whole unused group, not only its text.
- **Guard every write** with `writeControl.requiredRevisionId`, read fresh just before the call, so a change someone made in the browser is never overwritten.
- **Slides stores an element's size as a fixed base with a scale.** Read the element's transform before moving it and keep its scale, or the box shrinks: a text box moved with `scaleX: 1` collapsed to a third of its width. A new shape is stored as a 3,000,000 EMU base, so resetting its scale to 1 blew a small outline up to cover the slide.
- **Putting a local screenshot in:** `createImage` needs a URL Google can fetch. In the deck's browser tab, add a file input with script, load the file into it with the browser tool's file upload, draw it to a canvas and write the PNG to the clipboard, switch slides by setting `location.hash` (a full navigation reloads the editor and drops the input), click inside the slide, paste, then place the image through the API by its new object id. Save screenshots inside the working directory, because the upload refuses other paths.
- **`replaceAllText` gives the new text the style of the text it replaced.** After replacing a heading and its subtitle together, restyle the subtitle.
- **A speaking title fits one line**, about 50 characters at 22 pt on a 10 in slide. A title that wraps pushes into the evidence below it.
- **`duplicateObject` on a slide copies its speaker notes too.** Rewrite the new slide's notes, or one slide's notes end up on another.
- **`replaceAllText` limited by `pageObjectIds` never reaches the notes pages.** Edit notes through the notes shape's own object id.
- **`createSlide` needs `insertionIndex` at most the slide count**, and `updatePageElementsZOrder` needs every element on the same page.
- **An empty table cell has no text**, so styling it fails the whole batch. Skip empty cells.
- **A link takes the default link colour.** Set the text colour again after adding the link.
- **The API accepts shapes placed off the page**, so check that every element sits inside it. Use real bullets (`createParagraphBullets`), never a typed "•".

## 8. Check every slide

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

The outline was agreed, the deck is as short as it can be with the strongest evidence first, every content slide has a title in its deck type's format and real evidence, the titles alone tell the story, every slide's thumbnail was looked at after the last change, and the user has the link plus a reminder to put the words in their own voice before presenting.
