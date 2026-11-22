#!/usr/bin/env python3
"""Refuse a direct merge while the ship skill is loaded.

The flow lands through the repo's scripts/land, which runs a merge inside that
command and is invisible to a hook on the outer Bash call. Every other command
passes, including `scripts/land`, `gh pr view`, a help flag and reads.

The guard is off in a repo without scripts/land, and the hook command exits 0
when it cannot find this script, so a copied skill never blocks Bash. It sees
the command Claude writes, not a different invocation form such as
`bash -c 'gh pr merge'`; it is a guardrail, not a security boundary.
"""
import json
import os
import re
import sys
from pathlib import Path

LEAD = re.compile(r"^(?:sudo\s+|command\s+|env\s+|nohup\s+|time\s+|[A-Za-z_][A-Za-z0-9_]*=\S+\s+)")
MERGE = re.compile(r"^gh\s+pr\s+merge(?:\s|$)", re.I)
API = re.compile(r"^gh\s+api\b", re.I)
MUTATING = re.compile(r"(?:-X|--method)(?:\s+|=)(?:PUT|POST|PATCH)\b", re.I)
MERGE_PATH = re.compile(r"/merge(?:-async)?(?:\s|$)", re.I)
HELP = re.compile(r"(?:^|\s)(?:--help|-h)(?:\s|$)")


def segments(command):
    """Split on ; & | and newlines outside quotes, so a quoted pipe stays one segment."""
    out, buf, quote, i = [], [], None, 0
    while i < len(command):
        ch = command[i]
        if quote:
            buf.append(ch)
            if ch == "\\" and quote == '"' and i + 1 < len(command):
                buf.append(command[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
            buf.append(ch)
        elif ch in ";&|\n":
            out.append("".join(buf))
            buf = []
            if ch == "|" and i + 1 < len(command) and command[i + 1] == "|":
                i += 1
        else:
            buf.append(ch)
        i += 1
    out.append("".join(buf))
    return out


def first_word(segment):
    """The segment with wrappers and environment assignments stripped."""
    segment = segment.strip()
    while True:
        stripped = LEAD.sub("", segment, count=1)
        if stripped == segment:
            return segment
        segment = stripped


def guard_is_on(event):
    """The repo has a scripts/land, in the working directory or above it."""
    cwd = Path(event.get("cwd") or os.getcwd())
    return any((p / "scripts" / "land").is_file() for p in (cwd, *cwd.parents))


try:
    event = json.load(sys.stdin)
except (json.JSONDecodeError, OSError):
    sys.exit(0)

if not guard_is_on(event):
    sys.exit(0)

command = (event.get("tool_input") or {}).get("command") or ""
for segment in segments(command):
    if HELP.search(segment):
        continue
    word = first_word(segment)
    if MERGE.match(word) or (API.match(word) and MUTATING.search(segment) and MERGE_PATH.search(segment)):
        print("Blocked: land through the repo's scripts/land, not a direct merge.", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
