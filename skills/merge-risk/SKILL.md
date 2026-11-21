---
name: merge-risk
description: "Use when deciding how much to review, verify or trust before merging a pull request: a risk grade across alignment, impact, verification, rollback cost and error detection. Not for reviewing the diff line by line; that is review-pr. Not for deciding whether to build the change; that is review-plan. Not for QA on a deployed site; that is qa-live-site."
---

# Merge risk

The question is not whether the code is correct. It is how much risk the merge carries and what evidence would lower it. A grade a person can act on decides how deep the review goes and whether the merge waits.

Apply `references/engineering-principles.md`, `references/verification.md` and `references/shipping.md`. The references this skill names rely on these, so read them in full too: `references/core.md`, `references/judgement.md`, `references/respect-human-attention.md`, `references/visuals.md`, `references/ambition.md`, `references/testing.md`, `references/performance-backend.md`, `references/performance-frontend.md`.

## 1. Read the change before grading

Read the PR title, description and linked issue, then the diff, the files it touches and the tests. The description is the claim; the evidence is the commands, the screenshots, the recordings and the logs. Link every claim to `file:line` or to the evidence. Write down what you could not open.

## 2. The five axes

Each axis gets a verdict, the evidence behind it and the gaps that raise the risk. The verdicts are the ones below; the evidence decides them.

### Alignment: good, decent or poor

Does the code do what the description and the linked issue say, and nothing else? A drive-by, an assumption or a behavior change that is not in the description is a gap, even when it is an improvement. A mismatch between the title and the diff is a gap.

### Impact: small, medium or large (double weight)

What is the blast radius? Count the surfaces: pages, endpoints, consumers, stored data, jobs, configuration. Layout shift, a changed API shape, a mobile break and a widened permission all count. **Sensitive areas carry outsized risk whatever the diff size**: auth, permissions, payments, personal data, secrets, data migrations, dependency bumps and infrastructure or configuration changes. Name every one the diff touches and call out anything that widens access, weakens validation or logs sensitive data.

### Verification: good, decent or poor (double weight)

Is the behavior proven where it can be? A change to what a person sees **needs end-to-end proof**: screenshots or a recording, at the widths and themes that ship, before and after. A change that can affect performance **needs a profile**. Edge cases are tested, or the gap is named. Unit coverage is not end-to-end proof for a screen; a green suite with no screen evidence is a gap. Prefer before-and-after evidence to a standalone screenshot.

### Rollback cost: low, medium or high (one and a half weight)

How cheap is the revert once it is shipped? A two-way door is walked back with the revert. A one-way door is not: a data migration or backfill, a destructive action, a sent message or a payment, a public URL that other systems now call, an external effect. Say what the rollback costs in data, time and coordination, not only whether a revert commit exists.

### Error detection: good, decent, poor or not applicable

If this breaks in production, will someone know before a user reports it? Look for the critical flow's monitoring or alert, a swallowed exception, a fallback that hides a failure, a log nobody reads and an empty error path. A docs-only change is not applicable.

## 3. The grade

Weights: impact and verification double, rollback cost one and a half, alignment and error detection single. The verdicts score 1 (good, small, low), 2 (decent, medium) and 3 (poor, large, high); not applicable for error detection scores 1. The weighted mean is the internal score; do not put the arithmetic in the output.

- **Low** (below 1.5): merge. A light review is enough.
- **Medium** (1.5 to below 2.25): merge after the named gaps are closed or carded with an owner, or wait for the one missing piece of evidence the gaps name.
- **High** (2.25 and above): hold. Name the missing evidence, and put the sensitive area in front of a person before any merge.

The grade is a decision aid, not a guarantee. A high grade with all evidence present can still merge after the person accepts the risk; a low grade never skips the review of the diff.

## 4. The output

    **Merge risk: low | medium | high**

    **Alignment:** <verdict>. <one line of evidence, with file:line>.
    - <the gap that raises the risk, or "no gap">

    **Impact:** <verdict>. <the surfaces and the sensitive areas the diff touches>.
    - <gap>

    **Verification:** <verdict>. <the evidence and where it is>.
    - <gap: the screen without a screenshot, the performance change without a profile>

    **Rollback cost:** <verdict>. <the door and what the revert costs>.
    - <gap>

    **Error detection:** <verdict>. <the monitoring, the swallowed path or not applicable>.
    - <gap>

    **Action:** merge, merge after <X>, hold for <Y>, or do not merge. **Not checked:** <what you could not open>.

A category with no evidence is a gap, not a pass. A sentence that says only "looks fine" is not evidence.

## Rationalisations to refuse

| The excuse | What to do |
|---|---|
| "The tests pass" | Unit coverage is not end-to-end proof for a screen or a migration. Show the screen, the profile or the run. |
| "It is a small diff" | A small diff in auth, payments, personal data or a migration carries outsized risk. Grade the area, not the line count. |
| "We can revert it" | Say what the revert costs. A migration, a sent message and a payment are one-way doors. |
| "The error is logged" | Say who alerts and whether a person sees it before a user does. |
| "The PR description says it works" | The description is the claim. The evidence is the proof. |
| "A high grade blocks the merge" | The grade informs a person; it does not decide for them. Name the gaps and the action. |

## Done when

- [ ] All five axes have a verdict, with evidence or a named gap.
- [ ] Every sensitive area the diff touches is named.
- [ ] The screen or performance change has before-and-after evidence, or its absence is the gap.
- [ ] The rollback is a door with a cost, not a hope.
- [ ] The error path is monitored, or the swallowed path is named.
- [ ] The action and the not-checked list are written.
