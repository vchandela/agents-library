#!/usr/bin/env python3
"""The facts the skill gate, its installer and the audit share.

The Skill tool writes one line into the session transcript when it loads a
skill, and the gate watches the tools that change files. Both live here so
`skill-gate.py`, `setup` and `skill-audit.py` cannot drift apart.
"""

import re
from pathlib import Path

# What the Skill tool writes, for example "Launching skill: write-spec".
LAUNCH = re.compile(r"Launching skill: ([A-Za-z0-9-]+)")

# The tools whose edits the gate checks, written as a Claude Code hook matcher.
MATCHER = "Edit|Write|MultiEdit|NotebookEdit"


def find_launches(transcript: Path, wanted: set = None) -> list:
    """The skill names whose launch lines appear in a transcript, in the order they ran.

    Stops at the line that completes `wanted`, so the gate does not read a long
    transcript to its end once every skill it needs has launched.
    """
    found, seen = [], set()
    with transcript.open(encoding="utf-8", errors="replace") as lines:
        for line in lines:
            for name in LAUNCH.findall(line):
                found.append(name)
                seen.add(name)
            if wanted and wanted <= seen:
                break
    return found
