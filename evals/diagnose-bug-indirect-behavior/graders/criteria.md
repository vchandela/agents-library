---
type: llm
weight: 1
---

The response passes only if ALL of these hold:
1. It has the four sections: Goal, Constraints, Evidence path, Decision boundary.
2. The Goal is to find the cause of the 500 for that one user, with the fix left for later.
3. Constraints include read-only access and a rule that secrets and personal data stay out of the report.
4. The Evidence path names logs or the trace, recent changes, the export code path, and the user's data or request.
5. Decision boundary says what the agent may decide alone and what needs a person.
6. It does not give a numbered list of commands to run in order. A list of evidence sources is allowed and does not count as a step script.
Fail it only if a section is missing or the content is absent.