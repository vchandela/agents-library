---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?analyze-agent-transcripts"'
min: 1
arm: both
---

The skill should fire: the user is asking for a cross-session failure-mode read of their own Claude Code history, not a single-incident root cause or an eval suite.
