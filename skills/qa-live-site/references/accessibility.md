# Accessibility and UI state checks

The bar is WCAG 2.1 AA. Automated checks (axe, Lighthouse) cover only the rules
they can evaluate. Keyboard flow, focus, and what a screen reader announces have
no automated check here, so the manual passes below are mandatory, not
supplementary.

## Both lenses

Check every screen at phone width (about 390px) and laptop width (about 1280px),
in day and night registers where the product has both. Report the phone and the
laptop as separate sections: on the phone, what the first screen holds and how
much scrolling stands before the first action; on the laptop, whether the width
is used. A difference between the two that the design register does not list is
a finding.

## Keyboard only

- Tab from the top of the page: every interactive thing is reachable, in an
  order that matches the visual order, and focus is always visible.
- No keyboard trap; Escape closes a dialog and returns focus to where it
  started; a modal does not let focus wander behind it.
- A skip link exists where there is repeated chrome, and it moves focus to the
  main content.
- Every action that works by click also works by Enter or Space; hover-only
  menus are reachable by focus.

## Screen reader and semantics

- One `main` landmark per page; headings in a sensible order (one h1, no level
  skipped).
- Every image that carries meaning has alt text; decorative ones are empty-alt.
- Every form control has a label tied to it; every error is announced and tied
  to its field, not only coloured.
- A state change (a validation error, a loading result, a toast) is announced;
  nothing is signalled by colour alone.
- Buttons are buttons and links are links.

## Contrast and zoom

- Body text and controls meet 4.5:1 (large text 3:1); measure against the actual
  rendered colours, not the tokens. Both registers.
- At 200% zoom, and at 400% for reflow, no content is cut off and no horizontal
  scroll appears on the page.
- Text spacing overrides (line height 1.5, paragraph spacing 2x) do not clip
  content.

## Motion and touch

- `prefers-reduced-motion` removes or simplifies non-essential animation; test
  it by emulating the setting.
- Tap targets on the phone are at least about 44 by 44 CSS pixels, with space
  between adjacent ones; nothing important sits within a thumb's width of a
  destructive neighbour.

## UI state

A screen's states are what the reader can be in, not what the code branches on.
For each state on the grid, check that it renders as specified, that an
unexpected state is impossible, and that the empty, loading, error and
permission-denied states each exist and say what the reader should do next. A
state nobody specified is a finding in its own right.
