---
type: llm
weight: 1
---

The response passes only if ALL of these hold:
1. It names the outcome above this one crash, for example that this class of crash cannot come back unseen, not just "fix this line".
2. It lists what it would need access to in order to get there (crash reports or logs, a map from the running app version to its commit, a device or simulator to reproduce on) and asks for what is missing.
3. It does not present a bare optional-unwrapping change as the whole answer.
