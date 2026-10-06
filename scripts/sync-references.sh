#!/bin/sh
# Copy the shared references/ into every skill that uses them, so each skill
# folder works on its own: copied, zipped, uploaded, or installed as a plugin.
#
# Edit only references/ at the repo root, then run this script.
# A skill uses the shared references when it has a skills/<name>/references
# entry; to opt a new skill in, `mkdir skills/<name>/references` and run it.
#
#   scripts/sync-references.sh           refresh every copy
#   scripts/sync-references.sh --check   exit 1 if any copy is stale (CI)
set -eu
cd "$(dirname "$0")/.."

status=0
# A skill that points at references/ but has no copy works in this repo and
# breaks the moment it is installed on its own.
for dir in skills/*/; do
  if grep -q 'references/' "${dir}SKILL.md" && [ ! -e "${dir}references" ]; then
    echo "missing: ${dir}references (mkdir it and run scripts/sync-references.sh)"
    status=1
  fi
done
for dir in skills/*/; do
  dest="${dir}references"
  [ -e "$dest" ] || [ -L "$dest" ] || continue
  if [ "${1:-}" = --check ]; then
    if [ -L "$dest" ] || ! diff -r references "$dest" >/dev/null; then
      echo "stale: $dest (run scripts/sync-references.sh)"
      status=1
    fi
  else
    rm -rf "$dest"
    cp -R references "$dest"
  fi
done
exit "$status"
