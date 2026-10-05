---
name: write-blog
description: Use when turning a system you built into a published engineering post. Not for internal docs or proposals; that is write-tech-doc.
---

# Write an engineering blog post

Clear, practical, no fluff. Readers range from junior to staff: the mechanics teach the juniors, the generalisable lessons teach the seniors.

Apply `references/writing-voice.md`.

## Ground truth first

You will be given docs, notes, code and metrics. **Code and live metrics are truth. Notes and design docs may be stale.** Where they disagree, the code wins.

## Before writing a word

1. Say in one or two lines what each input is and what it contributes.
2. Extract the five to ten key ideas: insights, decisions, tradeoffs.
3. **Fact check every number and every mechanism against the code and the metrics.** For each headline figure, name the source and the window it covers, such as "p50 over 30 days". Flag anything you cannot source. **Invent nothing.** If the code does something different from the notes, describe what the code does.
4. Propose an incident driven narrative. Real incidents, what broke, why, the fix, the lesson, wherever the material allows. Concrete beats abstract every time.

Then stop and get agreement before drafting.

## The draft

Six to eight sections, one idea each. Consolidate hard.

Arc: hook or incident, the core idea, what a developer actually sees, the tradeoffs, the payoff with numbers, a short resources section.

- **Open with three bullets**: the problem, the approach, the result. This is what gets screenshotted.
- Concrete numbers early.
- Two to five diagrams, spread through the piece, not clustered at the top. Lead with one that captures the core insight.
- One takeaway per section, the part that generalises, stated as a claim the section has not already made.
- End on the last concrete fact or consequence. Never a line that repeats the post.

## Honesty

A tradeoffs section that names real limits, including the ones a demo would hide. No vendor loyalty. Then a short next steps section: security, scale, what productising would need.

## Do not

Leak secrets, keys, project ids or signed URLs, in text or in screenshots. Flag any image needing redaction.

## Done when

Every number names its source and window, every mechanism matches the code rather than the notes, the tradeoffs section names a real limit, and nothing unsourced survived.
