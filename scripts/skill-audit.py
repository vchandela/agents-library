#!/usr/bin/env python3
"""Count skill launches per session in the Claude Code transcripts.

    python3 scripts/skill-audit.py [--projects DIR]

Reads every *.jsonl under ~/.claude/projects, the transcript store Claude Code
keeps per project, and counts the "Launching skill: <name>" lines in each file.
That is the same line the skill-gate hook checks, so the audit and the gate
agree on what "loaded" means. A file under a subagents/ folder is a subagent's
own transcript, not a session, so it is skipped. One row per session, newest
first, then a summary that shows how many sessions launched no skill at all.
"""

import argparse
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from skill_hooks import find_launches

DEFAULT = Path.home() / ".claude" / "projects"


def main() -> int:
    parser = argparse.ArgumentParser(description="Count skill launches per session in the Claude Code transcripts.")
    parser.add_argument("--projects", type=Path, default=DEFAULT, help=f"the transcript store (default {DEFAULT})")
    args = parser.parse_args()
    if not args.projects.is_dir():
        sys.exit(f"no transcript store at {args.projects}; pass --projects DIR")

    rows = []
    for path in args.projects.rglob("*.jsonl"):
        if "subagents" in path.parts:
            continue
        found = Counter(find_launches(path))
        date = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).date()
        rows.append((date, path.parent.name, path.stem[:8], found))
    rows.sort(key=lambda row: (row[0], row[1], row[2]), reverse=True)

    print(f"{'date':10}  {'project':36}  {'session':8}  {'launches':>8}  skills")
    for date, project, session, found in rows:
        skills = ", ".join(f"{name} x{n}" if n > 1 else name for name, n in found.most_common())
        print(f"{date.isoformat():10}  {project[:36]:36}  {session:8}  {sum(found.values()):8}  {skills}")
    total = sum(sum(found.values()) for _, _, _, found in rows)
    used = sum(1 for _, _, _, found in rows if found)
    sessions_text = f"{len(rows)} session" + ("" if len(rows) == 1 else "s")
    launches_text = f"{total} launch" + ("" if total == 1 else "es")
    print(f"\n{sessions_text} in {args.projects}: {used} launched a skill, {len(rows) - used} did not; {launches_text}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
