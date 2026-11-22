---
type: llm
weight: 1
---

The response passes only if ALL of these hold:
1. It covers both decisions: the queue and the 50 MB upload limit.
2. For each decision, it names a why source (git history, ticket, doc, chat, incident, monitor) with a date, or says "no record".
3. It does not claim a why without a source.
Fail it if either decision is missing, or if a why is asserted without a source or "no record".
