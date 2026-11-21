---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?merge-risk"'
max: 0
min: 0
arm: both
---

A diff review for bugs belongs to `review-pr`; the ask is not a risk grade, so `merge-risk` should not fire.
