#!/bin/sh
# Copy into each skill only the shared references it needs, so each skill
# folder works on its own: copied, zipped, uploaded, or installed as a plugin.
#
# Edit only references/ at the repo root, then run this script.
# A skill gets the files its own text names, every file those point to, and the
# whole subfolder of any file or folder that lies in one (scripts/refgraph.py).
# A skill opts in with a skills/<name>/references folder:
# `mkdir skills/<name>/references` and run it.
#
#   scripts/sync-references.sh           refresh every copy
#   scripts/sync-references.sh --check   exit 1 on a missing, extra or stale copy (CI)
set -eu
cd "$(dirname "$0")/.."
exec python3 scripts/sync_references.py "$@"
