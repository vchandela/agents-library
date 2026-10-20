---
name: analyze-agent-transcripts
description: Use when you want to know what is actually going wrong across a batch of your own Claude Code or Cowork session transcripts, before deciding what to fix. Not for turning that same data into eval items, a judge or a gated test suite; that is evals. Not for root-causing one failure you already have in hand; that is diagnose-bug. Not for mining a video, article or book for ideas; that is extract-insights.
license: Apache-2.0
---

# Analyze agent transcripts

You are reading real Claude Code or Cowork sessions — your own, run against your own work — to find out what keeps going wrong, before anyone decides what to do about it. The output is a report of failure modes. It is not an eval suite, not a root cause for one incident, and not a list of fixes.

This is a specialization of one step from `evals` (its "look at real data first" step), narrowed to transcripts and stopped before item-building. If the goal is actually to build a graded test set, a judge, or a gate on future changes, stop and use `evals` instead — do not quietly grow this skill into that one.

## 1. Gather the batch

Claude Code sessions are JSONL files, one per session, under `~/.claude/projects/<slug>/<session-id>.jsonl`, where `<slug>` is the working directory path with `/` replaced by `-`. If more than one project slug could match, or the user hasn't said which sessions, ask rather than guessing — "your last 10 sessions in this project" and "every session since Monday across all projects" are different batches with different reports.

If the user doesn't give a count or date range, default to the most recent 10–15 sessions and say so plainly at the top of the report, so the reader knows what it does and doesn't cover.

For a Cowork session, ask the user for the transcript (export, link, or file) rather than guessing a local path — Cowork sessions often don't run on the machine you're reading from.

## 2. Read each one whole

A transcript is not the chat text. Parse every line — user turns, assistant turns, tool calls, tool results — because a lot of what goes wrong lives in a tool call and its result, not in the prose around it: the wrong file edited, a retry loop that burned ten calls to do what one would, a tool error that got silently absorbed and the agent carried on as if nothing happened.

When a tool result was too large to inline, the harness saves it to a file and leaves a pointer behind (an "output saved to..." line). Open that file too. Skipping it hides exactly the long, messy steps most likely to contain something worth noting.

Do not substitute the session's own closing summary (a compaction summary, a final "here's what I did") for reading the turns. It was written by the same agent whose work is under review, and it smooths over exactly the moments this report exists to surface.

## 3. The human writes the first notes

Same rule as `evals` step 1: the human writes the notes, the agent organizes them. Read a transcript (or let the agent surface candidate moments) and write one line per moment that felt wrong, in your own words — a wrong assumption, a step repeated for no reason, a tool call that shouldn't have happened, a question that should have been asked and wasn't, output you had to push back on or re-ask for. Don't wait for the agent to pre-judge what counts; your read of "that was wrong" is the ground truth here, not a pattern match on words like "error" or "sorry."

Only after roughly five human notes point at the same kind of thing does it become a named failure mode worth searching the rest of the batch for. Before that threshold, treat it as one data point, not a trend — this is the same discipline `evals` uses and for the same reason: naming a mode too early locks in a guess instead of a pattern.

Expect the notes to drift as you go — a mode that looked distinct on session 3 might turn out to be the same thing as one from session 7, described differently. Re-group rather than forcing the first label to stick.

## 4. Stop condition

Stop reading new sessions once two sessions in a row add neither a new failure mode nor a new instance of an existing one. Record how many sessions were actually read and the date range they span — that's part of what makes the report trustworthy.

## 5. Write the report

One section per failure mode:

- The mode, named in plain words — not a category label borrowed from a bug tracker.
- Its count across the batch (e.g. "4 of 12 sessions").
- One to three concrete examples: which session, roughly where in it, and a short verbatim quote or close paraphrase of what happened.
- A one-line guess at what kind of thing it is — a prompt- or skill-wording issue, a missing check, a one-off — without turning that guess into a recommendation.

Before anything goes in the report, redact anything that looks like a secret, token, password, API key, or personal data pulled from a tool result — same rule `diagnose-bug` applies to captured requests.

Close with what the report does not cover: sessions you didn't get to, anything unreadable, anything the human didn't have time to note. A report that's honest about its own edges is more useful than one that reads as complete.

### What this report is not

- Not a list of proposed fixes, prompt patches, or skill edits. If a fix is obvious, say so in one clause inside the mode's section, but do not build it, draft it, or hand off to `diagnose-bug` as part of this skill's own output — that's a separate decision for whoever reads the report.
- Not a severity score you invented. A count and real examples let the reader judge severity themselves.
- Not an eval suite. If the next question becomes "can we measure whether this gets better or worse," that's `evals`, not this.

## Rationalizations to catch yourself in

- "The closing summary already says what happened" — it's written by the agent under review; read the turns.
- "I'll grep for 'error' or 'sorry'" — misses the failures that read as confident and correct: scope creep, redoing already-done work, answering the wrong question well.
- "I already know the modes from a past batch" — read this batch anyway; a mode can fade, a new one can appear, and the counts have to come from what's actually in front of you, not memory.
- "The agent can write the first notes, it saw the transcript too" — then it's the agent reviewing itself; the human's one-line read of "that felt wrong" is the input this skill runs on, not a thing to skip to save a round-trip.
- "One example is enough, it's obviously a pattern" — one example is one example; find the fifth before naming the mode.

## Done when

- [ ] Every session in the batch was read in full, including anything the harness saved out to a file, not just the closing summary.
- [ ] Every failure mode traces back to a human-written note, not just the agent's own read of the transcript.
- [ ] Each mode in the report shows its count and at least one example a reader could go find in the source session.
- [ ] Nothing in the report is a proposed fix, a patch, or a handoff to another skill.
- [ ] Anything skipped, unread, or redacted is stated, not left silent.
