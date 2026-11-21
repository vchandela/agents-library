---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?merge-risk"'
max: 0
min: 0
arm: both
---

QA on a deployed site belongs to `qa-live-site`; the ask is not a merge risk grade, so `merge-risk` should not fire.
