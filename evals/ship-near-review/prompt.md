---
max_turns: 4
tags: [trigger]
---

Can you review this diff before I merge it?

```diff
--- a/app/limits.py
+++ b/app/limits.py
@@
-    return n <= user.quota
+    return n < user.quota
```
