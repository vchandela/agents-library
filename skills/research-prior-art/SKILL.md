---
name: research-prior-art
description: Use when you are about to design something, or are new to a technical topic, and need to know how labs, companies, open source projects and papers already solve it and how widely each idea is used. Not for reading one specific repo; that is understand-codebase. Not for explaining a system you already have; that is explain-simply.
---

# Research prior art

Apply `references/writing-voice.md` and `references/visuals.md`. The source checklist, company targets, sub-agent prompt, authority rubric and report shape are in `references/research-sources.md`. Apply `references/judgement.md` and `references/ambition.md`: the user's list of sources and companies is a minimum. Add the slices an expert would add, and say which you added and why. For the one claim the decision rests on, reproduce it on the user's own data or a small run instead of only citing it.

The references this skill names rely on these, so read them in full too: `references/respect-human-attention.md` (what a reader's time is worth), `references/machine-tells.md` (the last pass for machine-sounding text), `references/core.md` (the six core actions).

## 1. Brief first

- Read the user's own material before searching the web: their notes, the docs and threads they pasted, their seed lists, the internal repos and tickets. It says what the team already tried and what words they use. Read it fully, in the main context.
- Ask at most one round of questions, then write a five-line brief: the question, what the answer is for, known constraints, the dimensions to cover, the date cutoff, and the stop line (the decision it feeds, the number of slices, and the budget per slice). The user confirms it.
- **Map the whole topic as one question tree, once, before any agent starts.** The user's questions are the trunk, never the boundary. Add the branches an expert would add, each with one line on why it matters, and mark each one "researching now" or "offered". The stop line applies to the whole tree. Failure this prevents: agents launched one per question as the user asked them, so each branch arrived only when the user thought to ask.
- **Check every later question against the tree.** If it was on the tree, the answer should already exist. If it wasn't, the tree missed a branch: say so, add it, and look for its siblings, instead of answering only that one question.
- Say the depth out loud. **Quick** is one agent and a handful of searches. **Comparison** is one agent per option. **Landscape** is the full fan-out below.
- Start from the problem, not the current design. If the team already assumes an architecture, list it as one option to test, not the frame.

## 2. Fan out, one slice per source type

For a landscape, launch one sub-agent per source type in `references/research-sources.md` (frontier labs, vendors, engineering blogs, open source, papers, community, talks, the user's own material), in parallel. Slice by source type, not by keyword, so slices do not overlap.

Fill in the sub-agent prompt from `references/research-sources.md` for each slice.

- Search the problem, not the product. "How X does Y" finds marketing. "Y at scale", "Y postmortem" and "Y failed" find engineering.
- Pair every "best practices" search with an "anti-patterns" or "what went wrong" search.
- Stop a slice when the last two searches repeat what is already found.
- **Say when you are blocked, at once.** A rate limit, a spent search budget, a sign-in wall or a bot block is reported to the user as soon as it happens, not worked around in silence: the user can raise a limit or retry. Every sub-agent records each page it could not open in its gaps section. After the fan-out, retry the ones that matter (a reader proxy, an archived copy), and only then ask the user to download the few that still matter most, each with its link and why it matters. Keep that list short.

### Leave no article: the per-company sweep

When the user wants it exhaustive, or a handful of companies matter most, run the per-company sweep in `references/research-sources.md` after the first pass, one agent per company plus one each for papers, open source and community.

## 3. Merge by idea, count organisations

- Merge by idea, not by URL. The same idea under two names is one idea. A repost, a summary site or a vendor quoting its customer counts once.
- Give each idea an authority badge from the number of independent organisations using it, plus its strongest evidence tag. The rubric is in `references/research-sources.md`.
- Ask before writing: what did we find and not use? What did the slices disagree on?
- Sort every idea and gap Now, Later or Drop per `references/judgement.md`. Send one follow-up round, only for gaps that block a Now decision, then stop; a second round needs the user's yes.

## 4. Fact-check, in a separate agent

Mandatory before anything reaches the reader. A fresh agent gets the findings files and the link list, not the reasoning, re-opens every cited source and marks each claim: confirmed, wrong (with the correct version), partly right, or unreachable.

- For internal claims, re-check `file:line` against the default branch, not a stale checkout, and live systems read only.
- Cut or fix every wrong claim. Label what could not be opened as unverified in the text. A sub-agent saying it read a page is not evidence.
- If the research turns up exposed secrets or other security problems in the user's material, tell the user at once, without copying the values.

## 5. Report

Follow `references/research-sources.md`, "Report shape". An empty result is information: report it as unexamined, never as validation.

When the research ends in a proposed design, mock up its real artifacts in the user's own domain: the actual file tree, one filled-in page, one example database row, one event timeline.

Discuss in chat before rewriting a page the user is reading. Answer each question with a real example, then fold the answers into the steps where they belong.

## Rationalisations to refuse

| Excuse | Answer |
|---|---|
| "Three blog posts say it, so it is standard" | Count organisations and evidence, not posts. |
| "The sub-agent said it read the page" | The fact-check agent re-opens the link. |
| "I know this from training" | Find a dated source or mark it unverified. |
| "Nothing turned up, so it is novel" | Report the empty searches. Empty means unexamined. |
| "The team already uses X, so research X" | Research the problem; X is one option to test. |
| "The aggregator summarises it well" | Link the original. |
| "One more search round" | Stop when the last two searches repeat. |

## Done when

The brief and its question tree were confirmed. The report ends with the branches not explored, each with what it would change, so the user picks the next one instead of having to think of it. Every source type was searched, or skipped with a reason. Every claim has a link that the fact-check agent re-opened, and every correction is applied. Every idea has a badge and an evidence tag. The visuals checklist in `references/visuals.md` passes. The report opens with one picture, walks the steps with real examples, and ends with what was not found.
