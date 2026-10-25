#!/usr/bin/env python3
"""Copy into each opted-in skill only the shared references it needs (called by sync-references.sh).

    python3 scripts/sync_references.py            refresh every copy
    python3 scripts/sync_references.py --check    exit 1 on a missing, extra or stale copy
"""
import shutil
import sys
from pathlib import Path

from refgraph import ROOT, REF_LINK, needed

REFS = ROOT / "references"
check = "--check" in sys.argv[1:]
problems = []

for skill in sorted(p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").exists()):
    dest = skill / "references"
    if not (dest.exists() or dest.is_symlink()):
        # A skill that points at references/ but has no folder works here and breaks when installed alone.
        if REF_LINK.search((skill / "SKILL.md").read_text(encoding="utf-8")):
            problems.append(f"missing: {dest.relative_to(ROOT)} (mkdir it and run scripts/sync-references.sh)")
        continue
    want = needed(skill)
    if check:
        have = set()
        if dest.is_dir() and not dest.is_symlink():
            have = {f.relative_to(dest).as_posix() for f in dest.rglob("*") if f.is_file() or f.is_symlink()}
        else:
            problems.append(f"stale: {dest.relative_to(ROOT)} is not a folder of copies")
        for name in sorted(want - have):
            problems.append(f"missing: {(dest / name).relative_to(ROOT)}")
        for name in sorted(have - want):
            problems.append(f"extra: {(dest / name).relative_to(ROOT)} (no file in this skill points to it)")
        for name in sorted(want & have):
            src, copy = REFS / name, dest / name
            if copy.is_symlink() or src.read_bytes() != copy.read_bytes() or src.stat().st_mode & 0o111 != copy.stat().st_mode & 0o111:
                problems.append(f"stale: {copy.relative_to(ROOT)}")
    else:
        shutil.rmtree(dest) if dest.is_dir() and not dest.is_symlink() else dest.unlink()
        for name in sorted(want):
            (dest / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REFS / name, dest / name)

print("\n".join(problems) + ("\nrun scripts/sync-references.sh" if problems else ""))
sys.exit(1 if problems else 0)
