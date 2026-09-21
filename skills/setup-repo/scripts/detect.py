#!/usr/bin/env python3
"""What this repo is, and what it already has.

Detection only. It writes nothing and changes nothing, because deciding what a
repo should adopt is a judgement and this is the half that is not.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

LANGUAGES = {
    "python": ("pyproject.toml", "setup.py", "requirements.txt"),
    "javascript / typescript": ("package.json",),
    "go": ("go.mod",),
    "rust": ("Cargo.toml",),
    "java / kotlin": ("pom.xml", "build.gradle", "build.gradle.kts"),
    "ruby": ("Gemfile",),
    "terraform": ("main.tf", "versions.tf"),
    "helm": ("Chart.yaml",),
}

TEST_RUNNERS = {
    "pytest": ("pytest.ini", "pyproject.toml", "tox.ini"),
    "go test": ("go.mod",),
    "cargo test": ("Cargo.toml",),
    "jest / vitest": ("package.json",),
}

INSTRUCTION_FILES = ("CLAUDE.md", "AGENTS.md", ".cursorrules", "GEMINI.md")


def exists(*names: str) -> list[str]:
    return [n for n in names if (ROOT / n).exists()]


def git_facts() -> dict:
    def run(*args):
        try:
            out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                                 text=True, timeout=10)
            return out.stdout.strip() if out.returncode == 0 else ""
        except OSError:
            return ""

    is_repo = run("rev-parse", "--is-inside-work-tree") == "true"
    if not is_repo:
        return {"repo": False}
    return {
        "repo": True,
        "commits": run("rev-list", "--count", "HEAD") or "0",
        "hooks_path": run("config", "core.hooksPath") or "(default)",
        "has_githooks_dir": (ROOT / ".githooks").is_dir(),
    }


def has_tests() -> bool:
    for pattern in ("test_*.py", "*_test.py", "*_test.go", "*.test.ts", "*.spec.ts"):
        if next(ROOT.rglob(pattern), None):
            return True
    return (ROOT / "tests").is_dir() or (ROOT / "test").is_dir()


def main() -> int:
    print(f"REPO  {ROOT.name}\n")

    langs = [name for name, files in LANGUAGES.items() if exists(*files)]
    print(f"  language        {', '.join(langs) or 'not detected'}")

    runners = [name for name, files in TEST_RUNNERS.items() if exists(*files)]
    print(f"  test runner     {', '.join(runners) or 'none found'}")
    print(f"  tests present   {'yes' if has_tests() else 'no'}")

    g = git_facts()
    if g["repo"]:
        print(f"  git             {g['commits']} commits, hooksPath {g['hooks_path']}")
    else:
        print("  git             not a git repo")

    instr = exists(*INSTRUCTION_FILES)
    print(f"  instructions    {', '.join(instr) or 'none'}")
    for f in instr:
        lines = len((ROOT / f).read_text(errors="replace").splitlines())
        flag = "  <-- long, likely a router job" if lines > 300 else ""
        print(f"                    {f}: {lines} lines{flag}")

    print(f"  claude code     {'yes' if (ROOT / '.claude').is_dir() else 'no .claude/'}")
    print(f"  changelog       {'yes' if exists('CHANGELOG.md') else 'no'}")
    print(f"  incident log    {'yes' if exists('docs/incidents.md', 'INCIDENTS.md') else 'no'}")

    print("\nLAYERS THAT APPLY")
    print("  0  always")
    if g["repo"]:
        print("  1  git repo")
    if runners or has_tests():
        print("  2  test runner present")
    else:
        print("  4  no test runner, substitute verification")
    if (ROOT / ".claude").is_dir():
        print("  3  claude code in use")

    print("\nNothing was written. Propose a diff before changing anything.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
