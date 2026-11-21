---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?maintain-codebase"'
max: 0
min: 0
arm: both
---

A diff review belongs to `review-pr`; no maintenance lane is asked for, so `maintain-codebase` should not fire.
