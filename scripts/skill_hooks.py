#!/usr/bin/env python3
"""The facts the skill gate, its installer and the audit share.

The Skill tool records one launch in the session transcript when it loads a
skill, and the gate watches the tools that change files. Both live here so
`skill-gate.py`, `setup` and `skill-audit.py` cannot drift apart.
"""

import json
import re
from pathlib import Path

# The line the Skill tool returns, for example "Launching skill: write-spec".
# A plugin skill keeps its namespace, such as "Launching skill: anthropic-skills:chrome-browser".
LAUNCH = re.compile(r"Launching skill: ([A-Za-z0-9:_-]+)")

# The tools whose edits the gate checks, written as a Claude Code hook matcher.
MATCHER = "Edit|Write|MultiEdit|NotebookEdit"


def _launch_name(result) -> str:
    """The skill name when a tool result is nothing but a launch line, else None."""
    if isinstance(result, str):
        match = LAUNCH.fullmatch(result.strip())
        return match.group(1) if match else None
    if isinstance(result, list):
        for block in result:
            if isinstance(block, dict) and block.get("type") == "text":
                match = LAUNCH.fullmatch(str(block.get("text", "")).strip())
                if match:
                    return match.group(1)
    return None


def find_launches(transcript: Path, wanted: set = None) -> list:
    """The skill names the session launched with the Skill tool, in the order they ran.

    A launch counts from the Skill tool_use, or from the tool_result that is
    nothing but its "Launching skill: <name>" line. Text that only quotes the
    line, in a file read or a log, is not a launch. A tool_use and its result
    count once. Stops once every name in `wanted` has been seen, so the gate
    does not read a long transcript to its end once the launches it needs are in.
    """
    names, seen = [], set()
    with transcript.open(encoding="utf-8", errors="replace") as lines:
        for line in lines:
            # Cheap prefilter: only these lines can hold a Skill call or its result.
            if "Launching skill: " not in line and '"Skill"' not in line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                # The last line of a live session can be half written; skip it.
                continue
            message = event.get("message") if isinstance(event, dict) else None
            content = message.get("content") if isinstance(message, dict) else None
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                tool_id = block.get("id") or block.get("tool_use_id")
                if tool_id is not None and tool_id in seen:
                    continue
                if block.get("type") == "tool_use" and block.get("name") == "Skill":
                    tool_input = block.get("input")
                    name = tool_input.get("skill") if isinstance(tool_input, dict) else None
                elif block.get("type") == "tool_result":
                    name = _launch_name(block.get("content"))
                else:
                    continue
                if not isinstance(name, str) or not name:
                    continue
                if tool_id is not None:
                    seen.add(tool_id)
                names.append(name)
                if wanted and wanted <= set(names):
                    return names
    return names
