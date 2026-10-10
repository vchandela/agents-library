---
name: design-ui
description: Use when a screen is being designed or built (a page, a component, a site, an artifact) and its layout, type, colour or states are still being decided. Not for a QA pass on a deployed app; that is qa-live-site. Not for whether the copy makes a stranger act; that is review-product-page.
---

# Design a UI

`references/ui-quality.md` is the bar every screen is judged against. This skill is the order of work that reaches it. Words on the screen follow `references/writing-voice.md`.

## 1. The job before the look

Write three lines before any markup:

- **Who reads it**, all of them. An internal tool is read by everyone from an intern to a manager to their agents, not by one role.
- **The one task per screen**, and what the reader does next. Everything else is secondary and looks it.
- **The real content**: the longest real name, a real error, real data. Placeholder text hides every layout bug.

Check: the three lines exist and the user has seen them.

## 2. Start from what exists

- Use the repo's components, tokens and page patterns. Name the file each one comes from. Anything new to the repo needs a reason and the user's yes.
- No system yet: write the tokens first, before any component, in one file the app already loads, with a one-line comment per role. One spacing scale, one type ratio in whole pixels, 3 or 4 neutral text colours, one accent, 2 or 3 radii, light and dark. Take the ranges from the Taste table in `references/ui-quality.md`.
- A redesign lists the routes, nav labels, form field names, ids that scripts or analytics read, and legal copy before the first edit, and diffs them after. Any change to one needs the user's yes.
- Look at two or three products that do this same task well. Note what each does for the task, not for its brand.
- Sketch the first screen as a text wireframe, and ask whether the same request for a different product would produce it. Change the parts that would repeat.

Check: every colour, size and radius in the diff is a token.

## 3. The state grid before the happy path

States down the side, elements across the top, what each cell shows written in. At least: default, empty (which empty), loading, error, long content, missing content, no JavaScript, narrowest width. Design every cell. The state nobody drew is the one users find first.

Check: no blank cells. A cell that cannot happen says why.

## 4. Build

- Semantic HTML that works before any script runs. Script adds to it.
- Third-party UI (tours, popovers, menus) runs with the real library, checked on an element taller than the screen and on a phone.
- When one element breaks, find the rule that reaches it, and narrow that rule. A one-off override fights the system: a global `.copy { position:absolute }` pulled a Copy button out of its row, and the fix was scoping the rule, not adding a third.

Check: the page reads in order with CSS and script switched off.

## 5. Look, in a real browser, every round

- Screenshot at 390px, 768px and 1280px, light and dark, and 200% zoom. Every screenshot passes the Evidence rules in `references/ui-quality.md`.
- Judge the screenshots and write down what is wrong first. Then run the probes: the Taste table from computed styles, contrast, hit areas by `elementFromPoint`, axe-core on every state, console errors, a throttled Lighthouse run.
- Work every overlay and form by keyboard alone, as `references/ui-quality.md` Input says.
- Walk the one task as two or three of the readers from step 1.
- Bounded rounds: inspect everything, fix in one batch, confirm in one more round.
- Then hand the screenshots, the three lines from step 1 and the state grid to a subagent with no build history. It returns ship or fix with at most 8 findings, and you fix only from that list.

Check: every width and theme has a screenshot you looked at.

## Report

Before and after screenshots for each change, the probe numbers, and what stayed untested.

## Done when

Every cell of the state grid was seen in a browser. Every Taste probe is in range or has a stated reason. axe-core shows nothing serious, and the fresh reviewer said ship. Nothing at P0 or P1 from `references/ui-quality.md` remains. Screenshots exist for every width and theme.
