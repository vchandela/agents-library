#!/usr/bin/env python3
"""Test the ship merge guard: the hook command and its script, end to end.

    python3 scripts/test-ship-hook.py

Reads the command from skills/ship/SKILL.md so the test cannot drift from the
frontmatter. Runs it in a throwaway project with a scripts/land, and checks the
missing-script and no-land fallbacks never block.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "ship" / "SKILL.md"
GUARD = ROOT / "skills" / "ship" / "scripts" / "refuse-gh-pr-merge.py"
COMMAND = re.search(r"^\s*command:\s*'(.*)'\s*$", SKILL.read_text(encoding="utf-8"), re.M)
if not COMMAND:
    sys.exit("could not find the hook command in skills/ship/SKILL.md")
COMMAND = COMMAND.group(1)

ACTIVE = [
    ("gh pr merge 42 --squash", 2),
    ("gh pr merge 42 # --help", 2),
    ("scripts/land 42", 0),
    ("gh pr view 42", 0),
    ("cat README.md", 0),
    ("gh pr merge --help", 0),
    ('git commit -m "note | gh pr merge"', 0),
    ("echo hi && gh pr merge 42", 2),
    ("gh pr merge 42\n", 2),
    ("FOO=1 sudo gh pr merge 42", 2),
    ("gh api -X PUT repos/o/r/pulls/1/merge", 2),
    ("gh api -XPUT repos/o/r/pulls/1/merge", 2),
    ("gh api -X PUT repos/o/r/pulls/1/merge?foo=1", 2),
    ("gh api -X PUT 'repos/o/r/pulls/1/merge'", 2),
    ('gh api -X PUT "repos/o/r/pulls/1/merge"', 2),
    ("gh api repos/o/r/pulls/1/merge", 0),
]

NO_LAND = [
    ("gh pr merge 42", 2),
    ("gh api -X PUT repos/o/r/pulls/1/merge", 0),
]


def run(command, cwd, env):
    event = {"cwd": str(cwd), "tool_input": {"command": command}}
    return subprocess.run(
        ["sh", "-c", COMMAND],
        input=json.dumps(event),
        text=True,
        capture_output=True,
        env=env,
        check=False,
    ).returncode


failures = 0
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    project = tmp / "project"
    (project / "scripts").mkdir(parents=True)
    (project / "scripts" / "land").write_text("#!/bin/sh\n", encoding="utf-8")
    home = tmp / "home"
    home.mkdir()
    env = {
        "PATH": "/usr/bin:/bin:/usr/local/bin",
        "CLAUDE_PLUGIN_ROOT": str(ROOT),
        "CLAUDE_PROJECT_DIR": str(project),
        "HOME": str(home),
    }
    for command, want in ACTIVE:
        got = run(command, project, env)
        ok = got == want
        failures += not ok
        print(f"{'ok' if ok else 'FAIL'}  exit {got}, want {want}: {command!r}")

    without = tmp / "without-land"
    without.mkdir()
    for command, want in NO_LAND:
        got = run(command, without, env)
        ok = got == want
        failures += not ok
        print(f"{'ok' if ok else 'FAIL'}  exit {got}, want {want} (no scripts/land): {command!r}")

    missing = tmp / "missing"
    missing.mkdir()
    broken = dict(env, CLAUDE_PLUGIN_ROOT=str(missing), CLAUDE_PROJECT_DIR=str(missing), HOME=str(missing))
    got = run("gh pr merge 42", project, broken)
    ok = got == 0
    failures += not ok
    print(f"{'ok' if ok else 'FAIL'}  exit {got}, want 0 (guard script missing): gh pr merge 42")

total = len(ACTIVE) + len(NO_LAND) + 1
print(f"\n{total - failures} of {total} cases pass")
sys.exit(1 if failures else 0)
