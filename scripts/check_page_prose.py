#!/usr/bin/env python3
"""Check an HTML page against explain-simply's prose rules before it is published.

Usage: check_page_prose.py page.html [--max-words 25]

Checks the visible prose only: code blocks, diagrams and inline code are skipped.
1. No sentence over the word cap (25 by default, from ASD-STE100's limit for
   descriptive text).
2. No em dash anywhere.
3. No paragraph or list item over three sentences.
4. Every open-question box (a block whose text starts with a number and a
   question mark in its first line, inside class="box wait") has a diagram
   (mermaid, a diff block, a table or an svg) and a "Why X over Y" line.

Exit 0 when clean, 1 with one line per problem otherwise.
"""

from __future__ import annotations

import argparse
import html
import re
import sys


def _visible_text(fragment: str) -> str:
    fragment = re.sub(r"<(script|style|pre)[^>]*>.*?</\1>", " ", fragment, flags=re.S)
    fragment = re.sub(r"<code>.*?</code>", "X", fragment, flags=re.S)
    fragment = re.sub(r"<(td|th|li|p|h\d|div|summary|br)[^>]*>", "\n", fragment)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return html.unescape(fragment)


def _sentences(block: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+", block.strip()) if s]


def check(page: str, max_words: int) -> list[str]:
    problems: list[str] = []
    body = page.split("</style>", 1)[-1]
    text = _visible_text(body)
    if "—" in page:
        problems.append("em dash found: use a comma, colon, semicolon or full stop")
    for block in text.split("\n"):
        sentences = _sentences(block)
        if len(sentences) > 3:
            problems.append(f"block over 3 sentences ({len(sentences)}): {block.strip()[:90]}")
        for s in sentences:
            for part in re.split(r"(?<=[:;])\s+", s):
                n = len(part.split())
                if n > max_words:
                    problems.append(f"sentence over {max_words} words ({n}): {part[:90]}")
    for box in re.findall(r'<div class="box wait">(.*?)</div>\s*(?=<div class="box wait">|<h2>|$)', body, flags=re.S):
        head = _visible_text(box).strip().split("\n", 1)[0]
        if not re.match(r"\d+\.", head) or "?" not in head:
            continue
        if not re.search(r'class="mermaid"|class="diff"|<table|<svg', box):
            problems.append(f"open question without a diagram: {head[:80]}")
        if not re.search(r"Why [^<]{1,40} over ", box):
            problems.append(f'open question without a "Why X over Y" line: {head[:80]}')
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--max-words", type=int, default=25)
    args = ap.parse_args()
    problems = check(open(args.page, encoding="utf-8").read(), args.max_words)
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
