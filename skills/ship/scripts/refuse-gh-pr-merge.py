#!/usr/bin/env python3
"""Refuse a direct `gh pr merge` while the ship skill is loaded.

The flow lands through the repo's scripts/land, which runs the merge inside
that command and is invisible to a hook on the outer Bash call. Every other
command passes, including `scripts/land`, `gh pr view` and reads.

A hook is a guardrail, not a security boundary: it sees the command Claude
writes, not a different invocation form such as `bash -c 'gh pr merge'`.
"""
import json
import re
import sys

LEAD = re.compile(r"^(?:sudo\s+|command\s+|env\s+|[A-Za-z_][A-Za-z0-9_]*=\S+\s+)")
MERGE = re.compile(r"^gh\s+pr\s+merge(?:\s|$)")


def first_word(segment: str) -> str:
    """The segment with wrappers and environment assignments stripped."""
    while True:
        stripped = LEAD.sub("", segment, count=1)
        if stripped == segment:
            return segment
        segment = stripped


try:
    event = json.load(sys.stdin)
except (json.JSONDecodeError, OSError):
    sys.exit(0)

command = (event.get("tool_input") or {}).get("command") or ""
for segment in re.split(r"&&|\|\||[;|\n]", command):
    if MERGE.match(first_word(segment.strip())):
        print("Blocked: run the flow's scripts/land, not gh pr merge directly.", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
