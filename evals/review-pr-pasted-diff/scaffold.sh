#!/bin/sh
# The pasted diff must correspond to the checkout, or the model reviews it
# directly and explains that the repo does not match. Keep the changed line at
# line 10, under `def allowed`, as the hunk header says.
set -eu
mkdir -p app
cat > app/limits.py <<'PY'
"""Per-user request limits."""

DEFAULT_QUOTA = 100


def quota_for(user):
    return user.quota or DEFAULT_QUOTA

def allowed(user, n):
    return n <= user.quota


def remaining(user, n):
    # requests left after this one
    return max(user.quota - n, 0)

PY
git init -q
git add app/limits.py
git -c user.name=eval -c user.email=eval@example.com commit -qm 'limits: quota check'
