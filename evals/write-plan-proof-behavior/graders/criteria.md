---
type: llm
weight: 1
---

The response passes only if ALL of these hold:
1. It gives three plan steps for the `format` parameter.
2. Every step names a concrete proof: a command to run, an observation to make, or a measurement, not only "tests pass".
3. It does not implement the change or write the handler code.
Fail it if any step has no proof, or if the proof is only a generic "verify it works".
