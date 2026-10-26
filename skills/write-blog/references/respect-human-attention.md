# Respect human attention

The person who sends a document is accountable for all of it, whatever produced it. The reader must never spend more effort decoding it than the sender spent producing it. The more a document asks for someone's judgment, the more of it must be the sender's own.

## Who writes what

| Part | Who owns the words |
|---|---|
| Overview, goals, high-level approach, and any recommendation a reader is asked to weigh in on | **The user, in their own voice.** Draft these only when asked, mark the draft as a draft, and ask the user to rewrite or confirm it. Never present your draft as their reasoning. |
| Detailed sections (behaviour, errors, data, steps, tests) | Written with the agent, then edited down for density. |
| Stories, anecdotes and first-hand quotes | **The user.** Ask for them. Never invent one or fill the gap with a made-up example presented as real. |
| Raw output kept for reference (logs, full analyses) | Allowed, inside a clearly labelled block, never passed off as the user's words. |

**Anything the user will send to other people** (a chat message, meeting notes, a tracker sheet, a doc) gets two things from you before it leaves. First, your own consolidation pass: merge items that say the same thing, cut what nobody acts on, and lead with the actions. Second, an explicit closing line telling the user to rewrite it in their own words before sending. People forget under time pressure, and agent-written text sent as is costs them credibility. Example: a meeting backlog went out with three rows that were one request and the meeting summary pasted unedited; the reviewer replied "noise to signal ratio is high... human pass is needed".

## Systems you design respect attention too

The same rule covers what a design asks of people once it runs, not only what a document asks of its readers. People care about outcomes and want few touchpoints.

- **List every human touchpoint** in the design (reviews, grading, labelling, digests, alerts, approvals) with who, how often and how long it takes, then cut or shrink each one before proposing it.
- **Ask a person only when a machine can't decide**, in a place they already work (a field at ticket close, a PR approval, an issue assigned through CODEOWNERS), with the evidence attached. No new channels and no daily digests nobody acts on.
- **Machines check, people decide.** A reviewer approves a PR whose claims are already verified, with evidence inline; they tick only what the machine could not verify.
- Example: a knowledge-base design first had a daily "guard digest" message and owners ticking every claim. Both were cut: the guard now asks for a fix PR that the owner only approves, and only unverified claims need a tick.

## Rules for the document

- **Label where the agent's work begins.** One plain line at the boundary, for example: "Detail below drafted with an AI agent and reviewed by <name>." A reader must always know which parts carry the user's judgment.
- **Bad news goes first.** The first lines say what happened, what it costs and the plan, before the reader hears it anywhere else.
- **The skim test.** A reader should get the point, and what is asked of them, from the first screen. Everything else is there for whoever needs it.
- **Edit for density.** Three bullets where three do the job, not ten. No raw dumps, no emoji. Supporting detail still has to be easy to read.
- **Bullets, not walls, in specs and plans.** A reviewer reads a spec item by item, so write it that way. Each bullet holds one fact or one decision, in a full sentence, with its `file:line` at the end of that bullet. A paragraph longer than three sentences, or one carrying more than two citations, becomes a bullet list under a one-line lead. Proof that only a checker needs (line numbers, commit compares, version probes) goes in a collapsed "Evidence" toggle under the bullets. Failure this prevents: a 400-word spec item mixing four topics, which the reviewer asked to split into bullets.
- **Every claim is checked** before the user sends it, because they answer for it.
- **A reply leads with the decision.** The reader already has the thread. Keep only the reasoning that would change whether they agree, usually one fact they lack and the link they need to act. The diagnosis and the proof go in the ticket or doc that follows. A reviewer raising a topic is not asking for the full write-up.
- **Every question to the user stands alone.** A question asked after a stretch of other work must not send the user scrolling back. Restate the context in the same message: what it is about, the options with what each one means, your recommendation and why, and what the answer unblocks, in explain-simply's voice. Example: a thread explained two options, worked for an hour, then asked "option 1 or 2?"; the user had to scroll back to find what the options were. The step is `references/core.md` rule 4.
- **Messages asking for a decision** (a Slack post, a review request) carry the user's reasoning. Draft for the user to post, in their voice, and keep it short.
- **A shared doc is written item by item, in the user's words.** For a page teammates will read (a tech-debt list, an issues page), draft each entry in chat, 2 to 4 lines, and write to the doc only the text the user approved, one item at a time. The long explanation, diagrams and evidence go in a linked page, not the doc, so readers only read a little. Example: a 17-section tech-debt page cleared back to one heading, each issue then drafted, approved and added.

## Progress messages

- **Lead with what changed or what the reader can do.** Context comes after, if at all.
- **Silent while a loop runs.** Review rounds, fixes, pushes, CI runs and reruns are not news. Send nothing about them, not even one line. Come back once, when the work is ready for the user: the PR link after the reviewer approved and CI is green, with what was checked and anything only they can decide. Interrupt earlier only for a blocker only they can clear. Failure this prevents: a PR thread filled with "round 2 sent", "CI rerunning", "the reviewer found a bug" messages; the user said: "Just share the PR link with me once all review rounds and CI checks are done, and I'll review it. Don't pollute the thread with so many messages."
- **When the user asked, or is waiting on you, say where the work stands.** "Step 3 of 5 done: schema updated. Next: backfill the column." The reader cannot hold the count between messages.
- **Show a win with how to try it.** "Login works with magic links. Try: open `/login`." Not "I made some changes to auth."
- **Estimates in units, with their condition.** "About 15 minutes if tests cover it, an afternoon if not." Never "some work".
- **Errors as location, cause, fix.** "Fails at `auth.spec.ts:42`: expected 200, got 401." Name the cause only when the evidence shows it. Otherwise say it is unknown and give the next check.
- **At most five items per group, ranked.** Keep the rest and show them when asked. This shapes the display, never the analysis.
- **End with one next action that takes under two minutes.**

## Authorship boxes

- The user's own overview gets a small box: **"Written by <name>"**.
- Agent-drafted sections start with one box: **"AI-assisted · human-reviewed"**, naming who reviewed it. Put it where the agent's part begins, covering every section it drafted.
- Never label something "written by" the user until the words are theirs.

## What stays visible, what collapses

| Keep visible | Collapse (one click away) |
|---|---|
| The user's overview and the ask of the reader ("Asked of you: …") | Comparison tables for choices already settled |
| The case for the change (one worked example) | File-by-file "what moves" tables |
| Core design diagrams and the key safety mechanisms | Data tables with example rows |
| Guarantees (invariants), rollout gates | Rules carried over unchanged from an existing system |
| Open questions | Failure catalogues, evidence, settled decisions with what was rejected |

## Open questions

- Number the open questions first (1 to N) and settled ones after, so "#3" always means something a reviewer can answer.
- Show options side by side with their costs. Mark your pick on one option with its reason, labelled as yours; label the user's view "<name>'s preference" when they have one.
- Settled decisions go in one collapsed table: chosen, rejected, and why.
- **Before a question reaches a person, try to answer it yourself.** Check the vendor's docs, the dashboard, the code, or run a spike. Only what truly belongs to someone else stays: access they grant, a setting they own, a policy call. Send those once, together, after testing. Example: "is there a read-only WorkOS role?" and "can agent logins use the WorkOS MCP?" were both drafted for the WorkOS owner, and both were answered by the WorkOS docs (Support Viewer; the MCP only supports a normal login).
- **A question going to someone else, answered later,** becomes a short document. Order questions most important first, since you may get one pass. One idea per question, with space for the answer under it. Say that partial answers and "I don't know" help. End with "Anything we did not ask?"
- **A technical choice that evidence can settle is not a question.** "MCP or CLI?" was settled by spiking both. The team gets the outcome and the reason, not a vote.

## Review docs versus working docs

- A doc for reviewers is short (one to two pages), in the team's doc tool, and written or heavily edited by the user. A long spec or plan is the author's working document, not the review doc.
- Ask reviewers only about changes a user or stakeholder would see. Internal choices are the owner's call; state them, don't ask.
- Never offer an option nobody would pick, and never place the answer below the question where a top-down reader meets the question first.
- Give the migration and rollout real detail (what each mode produces, how it is compared, cutover, rollback); leave low-level architecture out, since it is configuration.

## Rules for reviews

- Judge the work, not whether an agent helped. Say why something is hard to read: it buries the point, it is too long, it makes claims the reader can't check.
- Coach, don't call out: show how you would tighten it.
