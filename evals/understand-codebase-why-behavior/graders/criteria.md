---
type: llm
weight: 1
---

The response passes only if ALL of these hold:
1. It names at least four of: git history, tickets or issues, docs or decision records, chat or review comments, incidents or postmortems, monitors or error logs.
2. For each source, it says what that source settles that the code cannot.
3. It says to date and quote each source, and to name the sources it could not get.
Fail it if it only lists sources without saying what each settles.
