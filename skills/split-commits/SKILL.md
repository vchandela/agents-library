---
name: split-commits
description: Use when finished work needs to become commits. Splits one change into a series of logical commits rather than one large one.
---

# Split into logical commits

One commit does one thing. A reviewer should be able to read each one on its own and say what it changed and why.

## How to split

Group by intent, not by file. A rename, a behaviour change and a test usually belong in different commits even when they touch one file. A change and its test usually belong in the same one.

Each commit should leave the repo working. A commit that breaks the build is a commit that cannot be reverted alone, which defeats the point of splitting.

## The message

First line says what changed, in plain words, under about seventy characters. Then a blank line, then why, if the why is not obvious.

Explain the reasoning, not the diff. The diff is already there. What it cannot show is what you decided and what you rejected.

## Done when

Each commit does one thing, each leaves the repo working, and each message would still make sense to someone reading it in a year.
