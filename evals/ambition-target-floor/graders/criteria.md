---
type: llm
weight: 1
---

The response passes only if ALL of these hold:
1. It aims at, or explicitly offers as an option, a result materially better than the 5 second ask (for example well under a second), instead of stopping at "under 5 seconds".
2. It says plainly that this beats or goes beyond what was asked, and what it costs or needs (an index, a cache, a query change).
3. It names a concrete way to measure the result that does not rely on its own judgement (a timing run, a profiler, a load test with numbers).
Fail it if it only removes the per-row queries and says that should get under 5 seconds with no better target and no measurement.
