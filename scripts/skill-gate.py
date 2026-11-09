#!/usr/bin/env python3
"""PreToolUse hook on Edit, Write, MultiEdit and NotebookEdit: refuse an edit that
a project's map says needs a skill this session has not launched.

The map is <project>/.claude/skill-gates.json, a JSON object from a path glob to
the skills the edit needs. Globs match the path relative to the project: `*` and
`?` stay inside one path segment and `**` crosses segments, so `**/*.py` matches
a Python file at any depth. A glob may name one skill as a string or several as
a list.

    {"docs/**": ["write-tech-doc"], "**/*.py": "review-pr"}

A skill counts as launched when the transcript records a Skill call for it,
either as the tool call or as the "Launching skill: <name>" result that call
returns; text that only quotes the line, in a file read or a log, does not
count. No map, or a path no glob matches, lets the edit through. A map that is
not valid JSON, or not that shape, blocks with exit 2: a gate that cannot read
its map is off while looking on, so it says so instead.

Exit 2 blocks the edit and shows the reason to the agent, as the Claude Code
hooks docs describe for PreToolUse.
"""

from __future__ import annotations

import fnmatch
import json
import os
import sys
from pathlib import Path

from skill_hooks import MATCHER, find_launches

TOOLS = set(MATCHER.split("|"))
MAP = Path(".claude") / "skill-gates.json"


def path_matches(pattern: str, rel: str) -> bool:
    """True when the glob matches the project-relative path, with ** crossing segments."""
    return _match(pattern.split("/"), rel.split("/"))


def _match(pat: list, path: list) -> bool:
    if not pat:
        return not path
    if pat[0] == "**":
        return _match(pat[1:], path) or (bool(path) and _match(pat, path[1:]))
    return bool(path) and fnmatch.fnmatchcase(path[0], pat[0]) and _match(pat[1:], path[1:])


def parse_map(path: Path) -> list:
    """The map as (glob, skills) pairs, or ValueError naming what is wrong with it."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise ValueError(f"is not valid JSON ({err})") from err
    if not isinstance(data, dict):
        raise ValueError("must hold a JSON object from a path glob to a skill or a list of skills")
    gates = []
    for glob, value in data.items():
        skills = [value] if isinstance(value, str) else value
        if not isinstance(skills, list) or not skills or not all(isinstance(s, str) and s for s in skills):
            raise ValueError(f"maps {glob!r} to {value!r}; give it a skill name or a non-empty list of them")
        gates.append((glob, skills))
    return gates


def launched(transcript: Path, wanted: set) -> set:
    """The wanted skill names that have a launch line in the transcript."""
    return set(find_launches(transcript, wanted)) & wanted


def block(reason: str) -> int:
    print(reason, file=sys.stderr)
    return 2


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError) as err:
        print(f"skill-gate: could not read the hook event ({err}); edit allowed", file=sys.stderr)
        return 0
    if not isinstance(event, dict) or event.get("tool_name") not in TOOLS:
        return 0
    # Hooks run in the project directory; the event carries the same path.
    cwd = Path(event.get("cwd") or os.getcwd())
    map_path = cwd / MAP
    if not map_path.is_file():
        return 0
    try:
        gates = parse_map(map_path)
    except (OSError, ValueError) as err:
        return block(f"Blocked: {map_path} {err}. Fix the map, or delete it to turn the gate off.")

    tool_input = event.get("tool_input")
    raw = None
    if isinstance(tool_input, dict):
        raw = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not isinstance(raw, str) or not raw:
        # Without a path there is nothing to match, so the edit goes through; say
        # so rather than pass silently, because a missing path is how a gate hides.
        print(f"skill-gate: no file path in the {event.get('tool_name')} event; cannot check the map, edit allowed", file=sys.stderr)
        return 0
    target = Path(raw)
    if not target.is_absolute():
        target = cwd / target
    # A path spelled inside the project keeps its project-relative name, so a
    # symlinked folder inside the project cannot hide an edit from its glob. A
    # spelling that differs through a symlink, such as /tmp for /private/tmp on
    # macOS, is compared as real paths, so neither spelling slips past.
    cwd_abs = Path(os.path.abspath(cwd))
    target_abs = Path(os.path.abspath(target))
    if target_abs == cwd_abs or cwd_abs in target_abs.parents:
        rel = os.path.relpath(target_abs, cwd_abs)
    else:
        rel = os.path.relpath(os.path.realpath(target_abs), os.path.realpath(cwd_abs))
    if rel.startswith(".."):
        return 0
    rel = Path(rel).as_posix()

    required = []
    for glob, skills in gates:
        if path_matches(glob, rel):
            required += skills
    if not required:
        return 0

    transcript = event.get("transcript_path") or ""
    if not transcript or not Path(transcript).is_file():
        # A hook that cannot read the transcript must not block every edit in the
        # project; it says once that it could not check, and lets the edit through.
        print(f"skill-gate: no transcript at {transcript!r}; cannot check the launch for {rel}, edit allowed", file=sys.stderr)
        return 0
    missing = sorted(set(required) - launched(Path(transcript), set(required)))
    if not missing:
        return 0
    if len(missing) == 1:
        return block(
            f"Blocked: {rel} matches {MAP}, which requires the skill {missing[0]}. "
            f"Launch it with the Skill tool, then retry the edit."
        )
    return block(
        f"Blocked: {rel} matches {MAP}, which requires the skills {', '.join(missing)}. "
        f"Launch them with the Skill tool, then retry the edit."
    )


if __name__ == "__main__":
    sys.exit(main())
