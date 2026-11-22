---
type: llm
weight: 1
---

The response passes only if ALL of these hold:
1. It states the goal: find how export authentication works today, with file and line evidence.
2. It states constraints, including read-only access and no live testing or production writes. A statement that secrets and personal data stay out of the report also satisfies this.
3. It names the evidence path: middleware or guards, route registration, tests, configuration and recent commits.
4. It says what the agent may decide alone and what needs a person.
5. It does not give a numbered list of commands to run in order. A list of evidence sources is allowed and does not count as a step script.
Fail it only if it gives an ordered command script, omits the evidence path, or leaves no decision boundary.
