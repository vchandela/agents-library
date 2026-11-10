# Functional QA

## The state grid

Before a click, list the screens' states and their elements, and write the
expected value in every cell. State means what the reader has done and what the
system holds: signed out, first visit, signed in with no data, signed in with a
session in progress, expired, error. Element means each thing the state shows:
the action button, the empty message, the price, the nav.

Work the cells in order. A cell that renders the wrong state, a state nobody
specified, or a control that goes nowhere is a finding, with the cell named.

## The flows

Walk every flow **from where the reader actually enters to where they actually
end up**, not from the first screen of it. Write the flow list down first; a
pass that skips one says so in the verdict's Not covered line. For a signed-in
product the flows typically include: first sign in, returning sign in, the
primary task start to finish, a purchase or upgrade, profile edits, sign out,
and account deletion where it exists.

For each flow record: entry point, each screen and state passed, the side effect
(a stored row, a sent request, a visible confirmation), and the end point.

## Documented error cases

The project's spec or docs hold a table of error conditions and what they
should do. If there is none, build it from the API responses the flow can
produce. Walk every row: trigger the condition, assert the exact status or
message, and record the row.

## Invariants

Write the things that must always be true, in one line each, then try to break
them directly. Typical shapes: a key is never served before the answer is
recorded; nothing is written after a deadline; one action per resource per
session; a completed thing never comes undone; every time value comes from the
server; a record is served only from a live source. Break each one with the
smallest sufficient attempt.

## Personas

Walk the primary task as two or three of these, chosen for the surface. Report
their red flags, not generic concerns.

- **Power user:** skips onboarding, wants keyboard shortcuts and bulk actions,
  hates confirmations for low-risk acts.
- **First-timer:** reads every label literally, needs the first action obvious in
  five seconds, needs to know an action succeeded.
- **Keyboard and screen-reader user:** the whole flow by Tab, state changes
  announced, nothing signalled by colour alone, works at 200% zoom.
- **Stress tester:** empty, one item, a thousand items, a 300-character name,
  emoji, refresh mid-flow, two tabs at once.
- **Distracted phone user:** one thumb, interrupted and back later, slow
  connection, primary action within reach.

## Coverage

One behaviour file per area works best: the states, the flow, the checks, and a
"how to get here" line in the reader's words. When a path cannot be reached,
name it and its blocker (an account, an entitlement, a feature flag, a native
driver) in the verdict; silently dropping it is the failure this section exists
to prevent.
