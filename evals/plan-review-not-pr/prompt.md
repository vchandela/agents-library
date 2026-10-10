---
max_turns: 4
tags: [trigger]
---

Here is my implementation plan. Tear it apart before I start coding.

1. Add a `retries` column to jobs.
2. Retry failed jobs every minute from a cron.
3. Stop after 5 retries.
