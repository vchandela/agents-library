# UI quality

Every item is checked on the rendered page, at the widths the product supports, in every theme it ships. A clean linter or detector run is a floor, not proof.

## Order: judge first, then run the tools

Look at the screen and write down what is wrong before running any detector, linter or Lighthouse. A tool's output anchors judgement. Then run the tools and note what each pass caught alone.

## Evidence

- A link checker's 403, 404 or certificate error is fetched again from a real browser before it is reported. Bot walls and a missing local certificate store produced 41 false dead links in one pass; three survived the second check.

- A DOM test is not a look. Interactive overlays (tours, popovers, menus) are checked in a real browser with the real library: jsdom passed every tour test while two steps highlighted elements taller than the screen and their popovers landed in a corner.
- A screenshot is evidence only if it is not blank, shows what its name claims, and exists for every required width and theme. A width nobody captured is a width nobody inspected.
- Capture after `document.fonts.ready`, with entrance animations finished or disabled, from the top of the document. A capture taken mid-animation or before the font swap is not evidence.
- Say what produced each finding: emulated viewport, synthesized touch, real device, which browser. Say what stayed untested.

## Layout

- Squint test: with detail blurred, the primary element, the secondary element and the main groups still read in order.
- Related things sit close; separate groups sit apart. Spacing comes from the project's scale, not one-off values.
- More space above a heading than below it.
- No horizontal page scroll at the narrowest width. Nothing clipped, nothing overlapping text.
- Body text never touches the viewport edge: at least a 16px gutter.
- No cards inside cards.
- A fixed size inside a flex row says `flex:none` (or `flex-shrink:0`). Items shrink by default, so a swipe row of 150px cards renders at 68px each on a phone while every "does the page scroll sideways" check passes. Measure the narrowest item, not just the page.
- A row of items that wraps strands the last one alone, and a step diagram then reads as ending early. Balance wrapped rows (the narrowest width that needs no more rows), and switch to an even grid when an item would still be alone.
- Text with inline parts (a superscript, a link, a code span) inside a flex or grid item goes in one inline wrapper, or each part becomes its own spaced item: "e  2x" for e².
- Long unbroken text (a URL, an ID, a 60-character token) stays inside its box at 320px: text children carry `min-width: 0` and `overflow-wrap: anywhere`, and grid tracks use `minmax(0, 1fr)`. Every user or CMS string has a decided wrap, truncate or clamp.
- No button, tab or nav label wraps onto two lines at any width.
- Sticky and full-height layouts: a sticky header sets `scroll-padding-block-start` to its height, so in-page links and the focused control land below it. Use `overflow: clip` where nothing scrolls, because `overflow: hidden` silently breaks `position: sticky` inside it. Full-height sections use `svh` or `dvh`, never `vh`. Fixed bars pad by `env(safe-area-inset-*, 0px)` on phones.
- Menus, tooltips and popovers opened at the bottom and right edges of the viewport are never cut by an `overflow` ancestor. Prefer `<details>`, `<dialog>` with `showModal()` and the `popover` attribute to scripted ones, unless the reason for a library is written down.
- Keyboard and screen-reader order match the visual order.

## Typography

- Body text at least 16px on the web. Functional UI text (labels, table cells, buttons) never under 11px. Every `input`, `textarea` and `select` computes 16px or more, because iOS Safari zooms in on a smaller field. The viewport meta never sets `maximum-scale=1` or `user-scalable=no`.
- Headings use `text-wrap: balance`. Numbers in tables, timers and counters use `font-variant-numeric: tabular-nums`.
- Line length 65 to 75 characters for prose. Over about 80 is a finding.
- Body line height 1.5 to 1.7. Under 1.3 is a finding.
- Headings do not skip levels. One h1.
- No justified body text, no all-caps paragraphs, no wide letter spacing on body text.
- Run the real copy, the longest name and the longest translation at every width, plus 200% zoom.

## Colour and contrast

- Text at least 4.5:1, large text at least 3:1, controls and focus rings at least 3:1, in every theme.
- Colour is never the only signal. Grey text on a coloured surface is a finding.
- Colours come from tokens, not literals.
- The root sets `color-scheme` to match the theme, with `<meta name="color-scheme" content="light dark">`, so scrollbars and native controls turn dark too.
- Each foreground token passes its ratio on every surface token it sits on, in every theme. Check the token pairs, not only the rendered page.

## States

Every screen and control answers each of these, or says why it cannot happen: default, hover, focus, active, disabled, loading, empty, error, success, permission denied, long content, missing content, offline or slow.

- An empty state says which empty it is: first use, no results, filtered out, no permission, or failure. Each gives the next action, and suggestions match the filter the reader chose.
- Loading names the real operation. Never invent progress.
- Content is visible without JavaScript having run. Nothing sits at opacity 0 waiting for a reveal.

## Copy

- A button names its action and object: "Delete draft", not "OK".
- An error says what failed, why when known, and how to recover. No internal codes as the message.
- Prefer undo to a confirmation dialog when undo is safe.
- Labels stay visible. A placeholder is an example, not a label.
- One word per concept across the product.
- Write out each abbreviation at its first use on every page, from one list of names, rendered rather than hand-typed, and never inside a heading or a quote.
- Ask before changing factual copy or adding a claim.

## Input

- Touch targets at least 44 by 44px. **Measure the hit area by tapping, not by reading the width**: a control drawn at 38px with a centred 44px `::after` passes, and a curl-and-CSS audit reports it as failing. Probe `elementFromPoint` 2px outside each edge.
- Every action works by keyboard, with a visible focus ring. Esc closes what it opened.
- The focus ring is an `outline` on `:focus-visible`, never `outline: none`, so it survives Windows high contrast (`forced-colors: active`).
- Every overlay, opened by keyboard: focus moves in, Tab stays inside, Esc closes it, and focus returns to the trigger. One live region announces status changes. A failed submit moves focus to an error summary that links each field.
- `:hover` styles sit inside `@media (hover: hover) and (pointer: fine)`, so a tap leaves no stuck hover.
- Fields and buttons keep their size through hover, focus, active, error and disabled (compare `getBoundingClientRect` before and after). The error text has a reserved slot. No field shows an error on first load (`:user-invalid`, or after submit).
- Anything that moves on its own for more than 5 seconds has a pause control and stops on hover, focus and reduced motion.
- Drag and swipe surfaces work under real touch, not only at a narrow viewport.
- Reduced motion keeps the state change and drops the movement. Fades of opacity and colour are not motion and may stay. A global zero-duration kill that removes feedback is a finding.

## Stress inputs

Very long and very short text, emoji and right-to-left text, numbers in the millions, a thousand items, no items, offline, 4xx and 5xx responses, rate limits, two actions at once, text 30% longer for translation, 200% zoom.

## Health

- Zero console errors and warnings on load and through the main flow.
- No failed requests, no broken images.
- Animations move transform and opacity, not width, height or margins. The one exception is a disclosure animating its own height.
- axe-core reports no serious or critical issue on any state, and every control's accessible name (read from the accessibility tree) contains its visible label.

## Performance budgets (web)

Measured, never estimated from code. Label each number lab or field.

| Metric | Good | Poor |
|---|---|---|
| LCP | 2.5s or less | over 4.0s |
| INP | 200ms or less | over 500ms |
| CLS | 0.1 or less | over 0.25 |
| TTFB | under 800ms | |

The LCP image is not lazy-loaded. Every image declares width and height, with `height: auto` in the CSS so it keeps its ratio when narrowed.

Measure on a throttled phone (390px, slow 4G, 4x CPU), not a laptop. Lighthouse in the lab ranks Apple, Stripe, Linear and Vercel's own homepages at 29 to 45 for performance (October 2026): a famous site is not a performance reference, so compare against the budget, not against them.

## Loading (what the fastest sites do, and what each saved when measured)

- Every image below the fold has `loading="lazy"`; the LCP image has `fetchpriority="high"`. Off-screen eager images cost one site 32% of its LCP on slow 4G. Lazy loading appears on 4 of 5 top reference homepages.
- Serve images at the size they are shown, in AVIF or WebP, with `srcset`. A 168px JPEG shown at 48px is a finding.
- Fingerprinted file names cached a year as `immutable`; HTML short. With `max-age=0` on CSS and JS, every navigation waits on a revalidation before it paints. Stripe, Linear, Vercel and GOV.UK all do it.
- Scripts are `defer` or `type=module`, never plain tags that block parsing. The only inline script in the head is the one that must run before paint (a theme flash guard).
- Preload only what paints above the fold: usually the font of the LCP text. Preloading a font nothing above the fold uses delays the one that matters.
- No chained requests to draw one screen. If a screen needs A then B, the server returns both in A. A late second response that inserts content above what the reader is looking at is a layout shift even when CLS reads 0.
- Count bytes and time in CI: a byte ceiling per page, plus a throttled LCP check. Real-user numbers when the platform allows (GOV.UK runs RUM and synthetic budgets with alerts).

## Resilience

- The page works when a script fails, not only when JavaScript is off. Hide content for an effect only under a class the script adds after it has loaded (`.armed .reveal { opacity:0 }`), never in the base stylesheet.
- Never replace a true value with a placeholder at load for an animation. A screen reader, a search engine's renderer and a link preview read the page without scrolling: a count-up zeroed at load tells them "0". Zero it just before it scrolls into view.
- A page served from a shared cache cannot know who is reading. Write moments as `<time datetime>` in UTC and let the browser show them in the reader's zone and language. Never hard-code a time zone.
- Every element a script reads is on a page that loads that script. A hook rendered on five pages and read by a script loaded on one is a control that does nothing on four. Check it per page, not per repository.

## Sharing

- Every indexable page has its own title, description, canonical, `og:title`, `og:description`, `og:image` and `twitter:card`. Links travel through chat apps, and a page without them shares as a bare URL.
- Structured data only where a search engine still uses it; check the current rich-result eligibility before adding it.

## Taste: what separates a crafted page from a template

Measured on Apple, Linear, Stripe, Vercel and Raycast in October 2026, with GOV.UK as the plain control. Each line is a number a probe can read from computed styles, so it is checked, not argued.

| Check | Crafted sites | Finding when |
|---|---|---|
| Letter spacing on text 32px and up | -0.015 to -0.06em, tighter as it grows | 0 or positive |
| Line height on text 40px and up | 1.0 to 1.15 | 1.2 or more |
| Distinct font weights on a page | 2 or 3 | 4 or more |
| Button weight | 400 to 510 | 600 or more with a glow or a lift |
| Families | one sans, plus a mono only for code or data | a third face, or mono on labels for a non-technical reader |
| Share of text nodes in the accent colour | under 10% (Stripe 9%, Apple under 4%) | over 15%: nothing stands out |
| Neutral text colours | 3 or 4 steps | 5 or more |
| Corner radii | 2 or 3, plus a pill | 5 or more |
| Type sizes | one ratio, whole pixels | fractional sizes, ratios that jump |
| Shadows | neutral, layered, low alpha; in dark, a hairline and a top highlight | any saturated or coloured glow |
| UI transition length | 100 to 250ms, ease-out, properties listed | over 300ms, ease-in, or `transition: all` |
| Hover and press | hover raises contrast; press scales to about 0.97 | a 1px lift and nothing else |
| Content at rest | visible with no scroll and no script | sections at opacity 0 until revealed, counters at 0 |
| Browser bar colour | read from the page, follows the chosen theme | a typed hex that is right in one theme |

Two that are judgement, not probes:

- **The first screen shows the product.** Linear shows its app, Apple the phone. A heading over a gradient shows nothing that is yours.
- **The 2024 to 2026 template, all at once, is the tell**: a centred hero, a pill eyebrow in mono capitals, an italic serif accent word, a glowing pill button, a dot grid or gradient wash, an autoplaying logo or face marquee, count-up numbers, and sections alternating text left and card right. Any one can be a choice. Four together is a template.

## Severity

P0 blocks the task. P1 is a real difficulty or an accessibility failure. P2 has a workaround. P3 is polish. Unsure between two? Ask whether a user would contact support about it. If yes, it is at least P1.
