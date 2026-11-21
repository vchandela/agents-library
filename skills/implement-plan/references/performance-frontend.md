# Frontend performance

What a reader feels, measured before it is argued about. These are the numbers to hold; the per-asset technique is in the UI quality bar, under Loading.

## The numbers that matter

| Metric | Good | Poor | What it answers |
|---|---|---|---|
| LCP | 2.5 s or less | over 4.0 s | how long the screen looked empty |
| INP | 200 ms or less | over 500 ms | how long a tap waited |
| CLS | 0.1 or less | over 0.25 | how much the page moved |
| TTFB | under 800 ms | over 1.8 s | how long the server took to start the page |
| TBT (lab only) | 200 ms or less | over 600 ms | the lab stand-in for INP |

The LCP, INP and CLS ranges are the Core Web Vitals thresholds published on web.dev (INP since March 2024); the TTFB and TBT ranges are the Lighthouse ones.

Load time is not on the list. It is when the browser finishes fetching everything, which nobody feels; read it only beside the page's bytes.

## Lab or field

- Field numbers are the truth for real readers; lab numbers are how a cause is found. Label every number lab or field, because they are different numbers.
- Lab: a phone viewport (390px), slow 4G (about 1.6 Mbps down and 150 ms round trip), 4x CPU slowdown, one cold browser context per page, at least three runs, the median, and the same conditions before and after.
- Field: real-user monitoring or CrUX at the 75th percentile, per page type.

## One reading is not a verdict

- A number within about 10% of a line, or a few milliseconds on a timer, is noise. The same page can read far apart on two days because of machine load, a cold server function or the network.
- Change one thing, re-measure the same way, keep only what moves beyond noise, and record the before and after beside the change.
- Famous sites are not the reference: the lab ranks several of the best-known product sites poorly. Compare against the budget.

## Reading the numbers

- LCP good and load slow: the cost is after first paint, in fonts and scripts. Cut bytes there.
- LCP slow: the largest element arrives late. Check a lazy-loaded hero image, a font, a chained request, a client-rendered header.
- TBT or INP bad: long tasks on the main thread. Find the script, ship less of it, split it, defer it.
- CLS: images without width and height, late-injected banners, font swaps.
- TTFB slow: the server or the cache. That is a backend number.

## The byte ceiling

- Set one byte ceiling per page type from measurement and check it in CI. There is no universal figure: a page at twice the weight of the lightest page that does the same job is the first place to look.
- The cheapest page ships the least script. Price a library on the throttled phone before adding it.
- Each page's row in the report: load, LCP, TBT, CLS and KB, per width, with the method named.

## Where to start

Measure the page with the method above, name the metric that is over and the cause its row names, fix one thing, and re-measure. A spinner or a skeleton changes how a wait feels, not how long it is: fix the wait first, then decide whether feedback is still needed.
