# Performance checks

Production gets single measured requests, never load. Volume, concurrency and
soak tests run against the local app and its test database, only if the target
is yours.

## Measure, do not feel

- **Resource timing, not wall clock.** Read `performance.getEntriesByType
  ("resource")` for each request: `startTime`, `duration`, `transferSize`, and
  the server timing if present. A stopwatch includes your own machine and
  connection; one pass read a collapse that was the test client's own uplink.
- **Several samples, then a median.** For a single API call, repeat it three or
  five times, a few seconds apart, and compare the median and the worst. This
  skill's rule of thumb is that a difference under about 2x is noise at this
  scale, and 10x or more is a finding. Those two numbers are a heuristic, not a
  measured constant; a project that states its own budget uses that instead.
- **Cold against warm.** For serverless or edge targets, the first request after
  a quiet minute may pay a cold start: measure the first and the second, and
  report the gap separately. Do not call a cold start a slow endpoint.

## What to check

**Slow single API calls.** From the network panel, list every XHR or fetch over
about 1 second; record method, path, duration, and payload size. Re-measure the
worst one three times. Note whether the slowness is the server (waiting) or the
transfer (size) from the resource timing phases.

**Cold starts.** First request after idle, compared with the next two. If the
target is serverless, also check a page whose function is rarely used.

**Large payloads.** Record `transferSize` for HTML, JSON and the largest asset.
A record list page that ships every field of every row is a finding; the fix is
a narrower response, not a faster wire, so say which fields were never shown.

**N+1 page loads.** Count requests for one page against what the page actually
needs. A list of N rows that fetches each row's detail is N+1; a page image that
loads the full-size original in a thumbnail is the same defect in another form.
Name the pattern, the count, and the page.

## Budgets

Write the budget down before measuring: a page's first byte, its largest content
element, and a single API call. Without a stated budget a number is neither good
nor bad. A project that already has budgets uses its numbers, not new ones.
