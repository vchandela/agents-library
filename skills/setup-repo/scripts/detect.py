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

# Codex stops reading instruction files past this many bytes (project_doc_max_bytes).
CODEX_LIMIT = 32 * 1024

AGENT_MARKERS = {
    "claude code": ("CLAUDE.md", ".claude"),
    "codex": ("AGENTS.md", ".codex", ".agents"),
    "cursor": (".cursor", ".cursorrules"),
    "gemini": ("GEMINI.md", ".gemini"),
}

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}


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


def nested_instruction_files() -> list[str]:
    found = []
    for name in ("AGENTS.md", "CLAUDE.md"):
        for p in ROOT.rglob(name):
            rel = p.relative_to(ROOT)
            if len(rel.parts) > 1 and not SKIP_DIRS & set(rel.parts):
                found.append(str(rel))
    return sorted(found)[:20]


def path_scoped_rules() -> list[tuple[str, bool]]:
    rules_dir = ROOT / ".claude" / "rules"
    if not rules_dir.is_dir():
        return []
    out = []
    for p in sorted(rules_dir.rglob("*.md")):
        inside = ROOT in p.resolve().parents
        out.append((str(p.relative_to(ROOT)), inside))
    return out


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
        path = ROOT / f
        text = path.read_text(errors="replace")
        lines = len(text.splitlines())
        size = len(text.encode())
        kind = ""
        if path.is_symlink():
            kind = f"  symlink -> {path.readlink()}"
        elif f == "CLAUDE.md" and text.strip() == "@AGENTS.md":
            kind = "  one-line import of AGENTS.md"
        flag = "  <-- long, likely a router job" if lines > 200 else ""
        print(f"                    {f}: {lines} lines, {size} bytes{kind}{flag}")

    agents_bytes = len((ROOT / "AGENTS.md").read_bytes()) if exists("AGENTS.md") else 0
    if agents_bytes > CODEX_LIMIT:
        print(f"                    AGENTS.md is over {CODEX_LIMIT} bytes: Codex drops the rest")
    if exists("AGENTS.md") and exists("CLAUDE.md"):
        claude = (ROOT / "CLAUDE.md").read_text(errors="replace").strip()
        if claude != "@AGENTS.md" and not (ROOT / "CLAUDE.md").is_symlink():
            print("                    CLAUDE.md and AGENTS.md both hold text: they can disagree,")
            print("                    and Claude reads only CLAUDE.md")

    nested = nested_instruction_files()
    print(f"  nested instr.   {', '.join(nested) or 'none'}")

    rules = path_scoped_rules()
    if rules:
        outside = [r for r, inside in rules if not inside]
        print(f"  claude rules    {len(rules)} in .claude/rules/"
              + (f", {len(outside)} linked from outside the repo (paths: ignored)" if outside else ""))
    else:
        print("  claude rules    none")

    skills = [d for d in (".claude/skills", ".agents/skills") if (ROOT / d).is_dir()]
    print(f"  skill folders   {', '.join(skills) or 'none'}")
    agents = [name for name, marker in AGENT_MARKERS.items() if any((ROOT / m).exists() for m in marker)]
    print(f"  agents          {', '.join(agents) or 'not detected'}")
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
    if (ROOT / ".claude").is_dir() or (ROOT / ".codex").is_dir():
        print("  3  an agent harness is in use, hooks possible")

    if len(agents) > 1:
        print("  5  several agents, one source for every rule")
    print("\nNothing was written. Propose a diff before changing anything.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
