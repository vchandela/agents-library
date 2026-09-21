---
name: setup-repo
description: Use when a repository needs engineering conventions applied, whether it is new or already has code and history. Detects the stack and proposes a diff. Never overwrites what is already there.
---

# Set up a repo

Two different jobs. A new repo gets files written. **An existing repo gets a proposal**, because it already has conventions and some of them are better than these.

## 1. Detect

    python3 scripts/detect.py

Reports what the repo is and what it already has. Read it before proposing anything.

## 2. Propose by layer

Only the layers that apply. A layer whose trigger is absent is skipped, not forced.

| Layer | Applies when | What it adds |
|---|---|---|
| 0 | always | An instruction file shaped as a router, not an encyclopedia. An incident log. |
| 1 | it is a git repo | Commit conventions. A version and changelog gate on push. |
| 2 | a test runner exists | Red, green, then break it and watch it fail again. A coverage floor if wanted. |
| 3 | Claude Code is used | Lifecycle hooks, one dispatcher, profiles to turn them down. |
| 4 | no test runner exists | Say so plainly, then substitute the closest real verification and map every rule to one. |

## 3. The conventions themselves

- **The instruction file is a router.** It holds what is always true and points at everything else. Anything loaded every session costs every session. A file that grows past a few hundred lines is a file nobody reads to the end, including the model.
- **A rule with no check is a rule you break yourself.** Every breach happens while doing one thing and looks right from inside it. Write the check with the rule, or write down that there is not one.
- **Facts block, judgements warn.** A path is protected or it is not. Whether a change carried a lesson is a judgement. A gate with false positives gets switched off, which is worse than no gate.
- **Keep an incident log.** One entry per real failure, with its mechanism and date. It is the cheapest document in any repo, and the one people actually reread.
- **One fact has one home.** Two documents may never disagree.

## 4. Never overwrite

For an existing repo, show the diff and wait. If the repo already has a convention that does the same job, **keep theirs**. The goal is a repo that holds its own rules, not one that matches this list.

## Done when

Every proposed file is either new or explicitly agreed, each layer applied has its trigger present, and anything skipped was skipped out loud.
