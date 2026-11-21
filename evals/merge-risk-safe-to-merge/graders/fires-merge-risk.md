---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?merge-risk"'
min: 1
arm: both
---

The skill should fire: the question is a merge risk grade for a concrete PR, not a line-by-line review.
