# Marketing pages

The rules for a page whose job is to make a stranger buy, book or believe: a company, product, shop, cafe, studio, SaaS or game site. They are not rules for an app screen; the state grid, the tokens and the app's own components still come first.

Taken from TasteSkill v2 (`Leonxlnx/taste-skill`, read on GitHub on 21 November 2026) and made generic. The vendor's art direction, its global Stop-hook gate and its shader defaults for every page were refused; what remains is the page plan, the asset discipline and the finish list.

## Contents

- The kind first
- The page plan
- The assets
- The rhythm
- The finish list

## The kind first

Write the kind on the plan's first line, because it decides the page: **place** (a cafe, bakery, guesthouse, shop, clinic people visit), **product** (a physical product or brand), **service** (people are hired: a studio, agency, law firm, trade), or **tech** (software, AI, developer tools, gaming, hardware). A maker that also opens its door or teaches is a place; its web shop becomes a goods section. A product is a product only when nothing happens at the door.

## The page plan

- **Place**: photographs lead, 12 to 20 on a full page and 8 to 12 on a compact one, the hero a photograph whenever a frame fits (a remote place gets its region's landscape), the visit block and the booking action each a screen. Flat grounds, square photographs, one button style, no effect, ground, loop, diagram or tab.
- **Product and service**: the product, the people, the rooms or the work lead, two or more photographs a screen on a product page; the product big where it stands whole, never mid-size in a grey panel; a different picture each section, never one view twice; every headline promise pictured; real icons for the tools a studio uses.
- **Tech**: the client's own subject leads at true size. Software shows its own UI as live HTML with real content, never a generic dashboard or only fragments on panels; hardware shows its photographs, else stand-in photographs of its kind; a game shows its world as full-bleed key art, else its name set large over stand-in photographs of its setting. 60 to 80 words a screen outside UI mocks.
- **Every page**: one main action a screen; equal left and right content edges; the hero alone on the first screen and one section per screen on a marketing page, so no second heading peeks in; one object never carries the page (the product or hero object leads the hero and two more sections at most); the client's own trailer, key art, screenshots or renders each get a named slot.

## The assets

- Real photographs, the product's own UI and real full-colour icons. No client photographs: licensed stand-ins of the same kind of thing, named in the report; a render only when the brief asks for 3D or a render; never a drawing, mood stock or a set of props.
- Every visual renders, never an empty ground, at 390, 1024 and 1440. Every promise is pictured. A swatch changes the picture. No captions or descriptions under any image; licence credits go in one footer line. Addresses on examples are street and district only, without a house number or postcode; contacts on `.example`.

## The rhythm

- Every hero enters once on load. Every page carries one dealt moment, two on a long page: a photograph or a type-led moment, not an effect for its own sake.
- Quiet micro-interactions: a linked card lifts 2px, a photo zooms 1.02 to 1.03 inside its frame, buttons step on hover and press on click, underlines draw. No tilt, carousels or timed tabs.
- Effects, scenes and dark heroes only where the trade has a technical subject (software, AI, developer tools, gaming, hardware). A cafe, bakery, guesthouse or shop gets photographs, not a shader.
- Plain copy in the client's voice; read it aloud. A template's voice is the defect this page kind exists to avoid.

## The finish list

A marketing page ships only when every line holds:

- Screenshots at 390, 1024 and 1440, light and dark, and every section at rest.
- Every visual renders; no empty ground; every promise pictured; no caption under an image; one footer credit line.
- Equal left and right content edges; one section per screen; no second heading peeking.
- One main action a screen, and every link, button and form works by keyboard alone.
- The browser probes in `design-ui` step 5 pass: contrast, hit areas, axe-core, console errors, a throttled Lighthouse run.
- The copy is the client's, not a template's; a fresh reviewer with no build history said ship.

`design-ui` step 5 is the browser check. This list is what to look for on a marketing page; the state grid still governs every interactive state.
