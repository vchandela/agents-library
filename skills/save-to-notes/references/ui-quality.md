# UI quality

Applied by qa-live-site, review-pr and implement-plan, only when the change has a screen. Every item is checked on the rendered page, at the widths the product supports, in every theme it ships. A clean linter or detector run is a floor, not proof.

## Order: judge first, then run the tools

Look at the screen and write down what is wrong before running any detector, linter or Lighthouse. A tool's output anchors judgement. Then run the tools and note what each pass caught alone.

## Evidence

- A screenshot is evidence only if it is not blank, shows what its name claims, and exists for every required width and theme. A width nobody captured is a width nobody inspected.
- Say what produced each finding: emulated viewport, synthesized touch, real device, which browser. Say what stayed untested.

## Layout

- Squint test: with detail blurred, the primary element, the secondary element and the main groups still read in order.
- Related things sit close; separate groups sit apart. Spacing comes from the project's scale, not one-off values.
- More space above a heading than below it.
- No horizontal page scroll at the narrowest width. Nothing clipped, nothing overlapping text.
- Body text never touches the viewport edge: at least a 16px gutter.
- No cards inside cards.
- Keyboard and screen-reader order match the visual order.

## Typography

- Body text at least 16px on the web. Functional UI text (labels, table cells, buttons) never under 11px.
- Line length 65 to 75 characters for prose. Over about 80 is a finding.
- Body line height 1.5 to 1.7. Under 1.3 is a finding.
- Headings do not skip levels. One h1.
- No justified body text, no all-caps paragraphs, no wide letter spacing on body text.
- Run the real copy, the longest name and the longest translation at every width, plus 200% zoom.

## Colour and contrast

- Text at least 4.5:1, large text at least 3:1, controls and focus rings at least 3:1, in every theme.
- Colour is never the only signal. Grey text on a coloured surface is a finding.
- Colours come from tokens, not literals.

## States

Every screen and control answers each of these, or says why it cannot happen: default, hover, focus, active, disabled, loading, empty, error, success, permission denied, long content, missing content, offline or slow.

- An empty state says which empty it is: first use, no results, filtered out, no permission, or failure. Each gives the next action.
- Loading names the real operation. Never invent progress.
- Content is visible without JavaScript having run. Nothing sits at opacity 0 waiting for a reveal.

## Copy

- A button names its action and object: "Delete draft", not "OK".
- An error says what failed, why when known, and how to recover. No internal codes as the message.
- Prefer undo to a confirmation dialog when undo is safe.
- Labels stay visible. A placeholder is an example, not a label.
- One word per concept across the product.
- Ask before changing factual copy or adding a claim.

## Input

- Touch targets at least 44 by 44px.
- Every action works by keyboard, with a visible focus ring. Esc closes what it opened.
- Drag and swipe surfaces work under real touch, not only at a narrow viewport.
- Reduced motion keeps the state change and drops the movement. A global zero-duration kill that removes feedback is a finding.

## Stress inputs

Very long and very short text, emoji and right-to-left text, numbers in the millions, a thousand items, no items, offline, 4xx and 5xx responses, rate limits, two actions at once, text 30% longer for translation, 200% zoom.

## Health

- Zero console errors and warnings on load and through the main flow.
- No failed requests, no broken images.
- Animations move transform and opacity, not width, height or margins.

## Performance budgets (web)

Measured, never estimated from code. Label each number lab or field.

| Metric | Good | Poor |
|---|---|---|
| LCP | 2.5s or less | over 4.0s |
| INP | 200ms or less | over 500ms |
| CLS | 0.1 or less | over 0.25 |
| TTFB | under 800ms | |

The LCP image is not lazy-loaded. Every image declares width and height.

## Severity

P0 blocks the task. P1 is a real difficulty or an accessibility failure. P2 has a workaround. P3 is polish. Unsure between two? Ask whether a user would contact support about it. If yes, it is at least P1.
