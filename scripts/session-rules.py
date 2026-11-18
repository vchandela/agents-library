#!/usr/bin/env python3
"""SessionStart hook on `compact`: name the skills the session launched before the compaction.

Claude Code re-injects ~/.claude/rules/core.md after every compaction (references/core.md,
line 3), so the rules come back on their own. The skills a session was using do not, and
core rule 1 says to launch them again. This hook reads the session transcript, whose
path is in the hook input, collects the skill name of each Skill tool call, and prints one
line: "Re-launch these skills: ship, explain-simply." What a SessionStart hook prints is
added to the session's context.

It prints no rule text, so references/core.md stays the rules' only home. A session that
launched no skill gets nothing. An unreadable transcript gets a generic reminder. The hook
always exits 0, because SessionStart cannot refuse anything.
"""

from __future__ import annotations

import json
import sys


def skills_used(transcript_path: str) -> list[str]:
    """Skill names from the Skill tool calls in a transcript, in first-use order, without repeats."""
    names: list[str] = []
    with open(transcript_path, encoding="utf-8") as transcript:
        for line in transcript:
            try:
                content = (json.loads(line).get("message") or {}).get("content")
            except (ValueError, AttributeError):
                continue
            for block in content if isinstance(content, list) else []:
                if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                    name = (block.get("input") or {}).get("skill")
                    if name and name not in names:
                        names.append(name)
    return names


def main() -> int:
    try:
        path = json.load(sys.stdin).get("transcript_path")
        names = skills_used(path)
    except (OSError, TypeError, ValueError):
        print("Could not read the transcript; re-launch the skills you were using.")
        return 0
    if names:
        print(f"Re-launch these skills: {', '.join(names)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
