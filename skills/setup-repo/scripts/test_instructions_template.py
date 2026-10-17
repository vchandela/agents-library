"""Keep the agent instruction files small, single-sourced and true.

A template: copy it to the target repo's tests (for example
`tests/test_instructions.py`), set the budget the owner agreed, and adapt the
root path. Each test guards one way these files go wrong without anyone
noticing, because a wrong instruction file looks fine to every agent that reads
it.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"

LINE_BUDGET = 120  # the number agreed with the repo's owner
# Codex stops reading instruction files at 32 KiB in total
# (project_doc_max_bytes) and drops the rest without a warning.
BYTE_BUDGET = 28 * 1024

# A backticked repo path: contains a slash, may end in a `:symbol` or `:line`
# suffix (`app/server.py:make_guard`), no spaces. A bare file name
# (`update.sh`) names a file in context and an address (`127.0.0.1`) is not a
# path, so neither is checked.
_PATH = re.compile(r"`([A-Za-z0-9_.\-]*/[A-Za-z0-9_.\-/]*)(?::[\w.()]+)?`")


def _named_paths(text: str) -> list[str]:
    out = []
    for raw in _PATH.findall(text):
        path = raw.rstrip("/")
        if path.startswith(("http", "~", "/", "$")) or "*" in path:
            continue
        out.append(path)
    return out


def _tracked(name: str) -> list[Path]:
    """Tracked files with exactly this name. `git ls-files` skips untracked
    scratch folders, and an exact name match avoids a case-insensitive file
    system matching `claude.md` for `CLAUDE.md`."""
    out = subprocess.run(  # noqa: S603 — fixed argv, no shell
        ["git", "ls-files", f"*{name}", name],  # noqa: S607 — git on PATH
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    return [ROOT / p for p in out if Path(p).name == name]


def test_the_path_pattern_reads_a_suffixed_path() -> None:
    text = "`app/server.py:make_guard` and `db/schema.py:create_tables()`"
    assert _named_paths(text) == ["app/server.py", "db/schema.py"]
    assert _named_paths("`update.sh` on `127.0.0.1:5432`, see `docs/`") == ["docs"]


def test_agents_md_fits_the_line_budget() -> None:
    lines = len(AGENTS.read_text().splitlines())
    assert lines <= LINE_BUDGET, (
        f"AGENTS.md is {lines} lines, over the budget of {LINE_BUDGET}. Move the "
        "longest section to its own doc and leave one row in the router table."
    )


def test_agents_md_fits_what_codex_reads() -> None:
    size = len(AGENTS.read_bytes())
    assert size <= BYTE_BUDGET, f"AGENTS.md is {size} bytes; Codex stops reading at 32 KiB"


def test_every_claude_md_only_imports_its_agents_md() -> None:
    for claude in _tracked("CLAUDE.md"):
        text = claude.read_text().strip()
        assert text == "@AGENTS.md", (
            f"{claude.relative_to(ROOT)} holds its own text. Put it in AGENTS.md, so "
            "every agent reads the same instructions."
        )
        assert (claude.parent / "AGENTS.md").is_file(), f"{claude} imports a missing AGENTS.md"


def test_every_path_the_router_names_exists() -> None:
    missing = [p for p in _named_paths(AGENTS.read_text()) if not (ROOT / p).exists()]
    assert not missing, f"AGENTS.md points at paths that do not exist: {missing}"


def test_rule_links_point_inside_the_repo() -> None:
    rules = ROOT / ".claude" / "rules"
    if not rules.is_dir():
        return
    outside = [
        str(p.relative_to(ROOT))
        for p in rules.rglob("*.md")
        if ROOT not in p.resolve().parents
    ]
    assert not outside, f"Claude ignores paths: on rule links that leave the repo: {outside}"
