#!/usr/bin/env python3
"""PreToolUse hook on SendMessage: refuse a ship review request that has no
principles check.

A review request is a message whose first line starts with "[ship" and says
"review request". It passes only when it has a "Principles check" section that
cites at least one file:line, the rule in references/tech-index.md ("A review
request -> carries a Principles check"). Every other message passes untouched.

Exit 2 blocks the send and shows the reason to the agent, as the Claude Code
hooks docs describe for PreToolUse.
"""

from __future__ import annotations

import json
import re
import sys

_REQUEST = re.compile(r"^\[ship [^\]]*\].*review request", re.IGNORECASE)
_SECTION = re.compile(r"principles check", re.IGNORECASE)
# A file:line citation such as repos.py:13502 or postgres.py:1462, 1499.
_CITATION = re.compile(r"[\w./-]+\.\w+:\d+")


def main() -> int:
    event = json.load(sys.stdin)
    message = str((event.get("tool_input") or {}).get("message") or "")
    first_line = message.strip().splitlines()[0] if message.strip() else ""
    if not _REQUEST.search(first_line):
        return 0
    found = _SECTION.search(message)
    if found and _CITATION.search(message[found.end():]):
        return 0
    print(
        "Blocked: a ship review request needs a 'Principles check' section with one "
        "line per rule from references/tech-index.md that the change touches, each "
        "with its verdict and a file:line citation. Add it and send again.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
