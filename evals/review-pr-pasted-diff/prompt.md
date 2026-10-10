---
max_turns: 4
tags: [trigger]
---

Can you look over this change before I merge it?

```diff
--- a/app/limits.py
+++ b/app/limits.py
@@ -10,7 +10,7 @@ def allowed(user, n):
-    return n <= user.quota
+    return n < user.quota
```
