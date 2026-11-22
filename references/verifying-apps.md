# Verifying an app change from the inside

An agent that changes a running app has to see the change work, not infer it from a green unit test. This is the loop for checking your own change in the real app: one loop, two project tools, and a guard that keeps the run away from production.

## Contents

- The loop
- The feature map is generated, never typed
- The CLI is thin
- The structural self-check
- Every finding becomes a test
- The production guard
- Before and after
- The upkeep cost
- What this does not replace

## The loop

1. Build one piece, small enough to run on its own.
2. Run it in the real app, through the project's browser fixture and test auth.
3. Observe what a user would see: the screen, the trace, the console, the numbers. Save the screenshot and keep the trace file.
4. Fix the difference between what you saw and what the piece was meant to do.
5. Re-run the same observation on the same input. The evidence has to change.

A loop that ends on "the test passes" is a different loop. The unit test stays; this one proves the app.

## The feature map is generated, never typed

The map is one row per reachable page: the route, what it does, how a user reaches it, the role or fixture needed to open it, and its known traps. It is built by a script from the app's own routes and pages:

- the server's route table, read with the framework's own route command or router registration;
- the file-based pages the framework serves;
- the client router's configuration.

The generator writes the map into the repo, and a `--check` mode fails when the stored map differs from what the routes and pages produce. The sweep reads its page list from the map. It never reads a hand-written list of "important pages", because that list misses the page nobody remembered and the miss is silent.

A map that drifts is worse than no map: it gives false confidence. Regenerate it in the same change that adds or removes a route.

## The CLI is thin

One small executable in the project, for example `scripts/verify-app`, wraps the project's existing browser fixture and test-auth helper. It does not reimplement login, launch or the browser driver; those already exist for the test suite.

- `doctor` checks the app URL, the browser, the auth fixture, the database host and the fixture data, and prints what is missing with the command that fixes it.
- `open <route>` opens the app authenticated at that route and waits for the page to settle.

Flags do the driving: `--click <selector>`, `--type <selector> <text>`, `--settle <selector|networkidle|ms>`, `--trace <path>`, `--screenshot <path>`, `--json`. Every mutating command supports `--dry-run`. Errors name the failing step and the fix, not a stack trace.

The CLI lives in the project because only that project knows how to boot its app. A skill uses the project's CLI or says the project has none; it never fakes verification with a curl or a unit test.

## The structural self-check

After opening each page, at every width the product supports, check structure rather than taste:

- **Sideways scroll:** `document.scrollingElement.scrollWidth > document.scrollingElement.clientWidth` beyond one pixel of rounding.
- **Clipping:** an element whose `scrollWidth > clientWidth + 1` or `scrollHeight > clientHeight + 1` while its overflow is hidden.
- **Wrapping:** a text box wider than its parent, a heading breaking mid-word, or a label running under its control.
- **Row heights:** rows in one table or list share a height, or an exception is deliberate and named in the code.
- **Overlap:** bounding boxes of siblings that intersect where the design does not allow it.

Record the numbers, not "looks fine". The same script runs before and after, so the comparison is the same measurement.

## Every finding becomes a test

A finding is not fixed until the project's own test suite fails without the fix and passes with it, through the same fixture and auth. Put the test at the seam nearest the user: a rendered page, a route response, a row in the database. If the nearest seam cannot express the finding, that is a finding about the design; write it down rather than settling for a test that cannot go red.

## The production guard

Before any connection, read the database host from the project's configuration. Proceed only when it is local: `localhost`, `127.0.0.1`, `::1`, a unix socket, or a container host mapped to this machine. Anything else exits non-zero and prints the host and the reason.

The guard is not a flag the agent can turn off. A verification run never points at production. If the project's fixture has no such guard, add it before the first run.

## Before and after

Same route, same viewport, same fixture, same input. Record the before from the unmodified app or the base branch, then the after. Take screenshots at named paths and keep both. Record numbers where the question is numeric: layout width, row height, element count, time to the first action, console errors.

A change with only an after screenshot has no comparison, and a number with no before is not a measurement of the change.

## The upkeep cost

Name what decays and who refreshes it:

- the map, regenerated when routes or pages change, with the `--check` in CI;
- the CLI, updated when the auth fixture or the launch command moves;
- the guard, never bypassed and never weakened to make a run pass;
- the captures, deleted after the pull request except the one attached as evidence.

Upkeep is part of the cost of the method. A project that will not refresh the map should not rely on the sweep.

## What this does not replace

This is the agent checking its own work. The independent review agent (`review-pr`, `qa-live-site`) stays separate and is never replaced by it. Verification shows the change does what its author intended; review finds what the author did not intend.
