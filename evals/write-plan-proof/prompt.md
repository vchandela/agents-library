---
max_turns: 1
tags: [trigger]
---

Here is the approved spec: the export endpoint gets a `format` query parameter, `csv` or `json`; an unknown value returns 400; both formats read the same row query. Write the implementation plan, with how each step will be checked.
