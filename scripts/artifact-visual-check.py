#!/usr/bin/env python3
"""PreToolUse hook on Artifact: refuse publishing a page that has no picture
and no table.

The rule is references/respect-human-attention.md: the first screen carries one
picture and one real example. Whether a page reads well is judgment, left to the
writer and the reviewer; whether it has any diagram or table at all is a cheap,
exact fact, so it is checked here (engineering-principles, "Prompt or
deterministic check").

Only a page publish is checked: action "publish" (or none), no `asset`, and a
`file_path` ending in .html or .md. Reads, lists, asset uploads and data files
for an Artifact type pass untouched. Exit 2 blocks the publish and shows the
reason to the agent, as the Claude Code hooks docs describe for PreToolUse.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# A diagram or table in HTML: inline SVG, an image, a canvas, a table, or a
# Mermaid block (rendered from a <pre class="mermaid"> or a script that loads it).
_HTML_VISUAL = re.compile(r"<(svg|table|img|canvas)\b|mermaid", re.IGNORECASE)
# The same in Markdown: a pipe table's separator row, an image, or a mermaid fence.
_MD_VISUAL = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*\|", re.MULTILINE)
_MD_OTHER = re.compile(r"!\[[^\]]*\]\(|```mermaid", re.IGNORECASE)


def has_visual(path: Path, text: str) -> bool:
    if path.suffix.lower() == ".md":
        return bool(_MD_VISUAL.search(text) or _MD_OTHER.search(text))
    return bool(_HTML_VISUAL.search(text))


def main() -> int:
    event = json.load(sys.stdin)
    args = event.get("tool_input") or {}
    if args.get("action") not in (None, "publish") or args.get("asset"):
        return 0
    file_path = args.get("file_path")
    if not file_path or Path(file_path).suffix.lower() not in (".html", ".md"):
        return 0
    path = Path(file_path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0  # The tool itself reports a missing file.
    if has_visual(path, text):
        return 0
    print(
        f"Blocked: {path.name} has no diagram or table. Respect-human-attention asks "
        "for the ask, one picture and one real example on the first screen. Add a "
        "diagram (SVG or Mermaid) or a table with real rows, then publish again.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
