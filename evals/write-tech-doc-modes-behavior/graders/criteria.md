---
type: llm
weight: 1
---

The response passes only if ALL of these hold:
1. It names the first-run guide a tutorial, the key-rotation guide a how-to, the parameter guide a reference, and the design guide an explanation.
2. It states that one document keeps one mode, and that documents link across modes instead of absorbing them.
3. It says the README or the tutorial is written before the implementation for a new interface.
Fail it if it mixes the modes or omits what to write first.
