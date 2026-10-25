"""The reference graph shared by the linter and the sync: which files in references/ a file points to.

A file points to a reference by a path (`references/x.md`), a relative markdown link, or a backticked
file name that exists in references/.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF_LINK = re.compile(r"references/([\w./-]+\.(?:md|sh))")
REF_DIR = re.compile(r"references/([\w-]+(?:/[\w-]+)*)/(?![\w.-])")
MD_LINK = re.compile(r"\]\(([\w./-]+\.md)(?:#[\w-]*)?\)")
BACKTICK = re.compile(r"`([\w-]+\.md)`")


def links(path):
    """Reference files (relative to references/) that a file points to."""
    text = path.read_text(encoding="utf-8")
    refs = ROOT / "references"
    found = set(REF_LINK.findall(text))
    for name in BACKTICK.findall(text):
        if (refs / name).exists():
            found.add(name)
    for rel in MD_LINK.findall(text):
        target = (path.parent / rel).resolve()
        if refs in target.parents and target.exists():
            found.add(str(target.relative_to(refs)))
    return found


def needed(skill):
    """Every file under references/ that a skill folder needs, relative to references/.

    The files its own text names, every file those point to, and the whole subfolder
    of any file or folder that lies in one, so a folder of entries is never half there.
    """
    refs = ROOT / "references"
    seeds = [p for p in skill.rglob("*") if p.is_file() and "references" not in p.relative_to(skill).parts[:1]
             and p.suffix in {".md", ".py", ".sh", ""}]
    found, todo = set(), []
    for seed in seeds:
        try:
            text = seed.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        todo += [n for n in links(seed) if (refs / n).is_file()]
        todo += [d + "/" + f.relative_to(refs / d).as_posix() for d in REF_DIR.findall(text)
                 if (refs / d).is_dir() for f in (refs / d).rglob("*") if f.is_file()]
    while todo:
        ref = todo.pop()
        if ref in found or not (refs / ref).is_file():
            continue
        found.add(ref)
        top = ref.split("/")[0]
        if "/" in ref:
            todo += [f.relative_to(refs).as_posix() for f in (refs / top).rglob("*") if f.is_file()]
        if ref.endswith(".md"):
            todo += links(refs / ref)
    return found
