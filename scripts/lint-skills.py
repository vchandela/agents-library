#!/usr/bin/env python3
"""Lint every skill so a broken one fails CI instead of failing in a user's tool.

Checks, standard library only:
  - frontmatter has only `name`, `description`, `license` and `disable-model-invocation`, and parses as strict YAML would
    (a value containing ": " must be quoted);
  - `name` matches the folder and the spec's pattern; description is 1 to 1,024 characters;
  - the body stays under about 5,000 tokens (3,500 words);
  - every `references/X.md` a skill mentions exists in that skill's own folder;
  - no unescaped $ARGUMENTS, $N or ${CLAUDE_...} in a body;
  - no hidden Unicode (zero-width or bidirectional controls) and no HTML comments.

    python3 scripts/lint-skills.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
HIDDEN = re.compile("[​-‏‪-‮⁠-⁤﻿]")
MAX_WORDS = 3500

errors = []


def fail(path, msg):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
    folder = skill.parent.name
    text = skill.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if not text.startswith("---") or len(parts) < 3:
        fail(skill, "no frontmatter")
        continue
    fields = {}
    for line in parts[1].strip().splitlines():
        key, _, value = line.partition(":")
        value = value.strip()
        quoted = value[:1] in "\"'" and value[-1:] == value[:1]
        if ": " in value and not quoted:
            fail(skill, f"unquoted ': ' in {key!r} breaks strict YAML parsers")
        fields[key.strip()] = value
    extra = set(fields) - {"name", "description", "license", "disable-model-invocation"}
    if extra:
        fail(skill, f"frontmatter keys outside name, description, license and disable-model-invocation: {sorted(extra)}")
    if fields.get("name") != folder or not NAME.match(folder):
        fail(skill, f"name {fields.get('name')!r} must equal the folder {folder!r} and match {NAME.pattern}")
    if not 1 <= len(fields.get("description", "")) <= 1024:
        fail(skill, "description must be 1 to 1,024 characters")
    if len(parts[2].split()) > MAX_WORDS:
        fail(skill, f"body is {len(parts[2].split())} words; keep it under {MAX_WORDS}")
    if re.search(r"(?<!\\)\$(ARGUMENTS|[0-9]|\{CLAUDE_)", parts[2]):
        fail(skill, "$ARGUMENTS, $N or ${CLAUDE_...} in the body is replaced when the skill is invoked with arguments; escape it")
    for ref in sorted(set(re.findall(r"references/([\w.-]+\.md)", text))):
        if not (skill.parent / "references" / ref).exists():
            fail(skill, f"mentions references/{ref} but the skill folder does not ship it")

for md in sorted(list((ROOT / "skills").rglob("*.md")) + list((ROOT / "references").glob("*.md"))):
    text = md.read_text(encoding="utf-8")
    if HIDDEN.search(text):
        fail(md, "hidden Unicode (zero-width or bidirectional control)")
    if "<!--" in text:
        fail(md, "HTML comment (hidden from readers, visible to agents)")

print("\n".join(errors) or "all skills pass")
sys.exit(1 if errors else 0)
