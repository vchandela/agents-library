---
name: analyze-agent-transcripts
description: Use when you want to know what is actually going wrong across a batch of your own Claude Code or Cowork session transcripts, before deciding what to fix. Not for turning that same data into eval items, a judge or a gated test suite; that is evals. Not for root-causing one failure you already have in hand; that is diagnose-bug. Not for mining a video, article or book for ideas; that is extract-insights.
---

# Analyse agent transcripts

You are reading real Claude Code or Cowork sessions, run against your own work, to find out what keeps going wrong before anyone decides what to do about it. The output is a report of failure modes.

## 1. Gather the batch

Claude Code sessions are JSONL files, one per session, under `~/.claude/projects/<slug>/<session-id>.jsonl`, where `<slug>` is the working directory path with `/` replaced by `-`. If more than one project slug could match, or the user hasn't said which sessions, ask rather than guess: "your last 10 sessions in this project" and "every session since Monday across all projects" are different batches with different reports.

Before choosing, read `ledgers/transcripts.md` in this library. Ask which laptop section this machine is (offer the existing ones; a new laptop gets a new section). Skip every session whose id is already in that section, unless the file now has more lines than the ledger says were read: then read only the lines after that number. Skip a session written to in the last hour, since it is probably still live. If nothing is new, say so and stop.

With no count or date range given, take the newest unread sessions, at most 15 per run, and say so at the top of the report. The rest wait for the next run.

For a Cowork session, ask the user for the transcript (export, link or file) rather than guessing a local path; Cowork sessions often don't run on this machine.

## 2. Read each one whole

A transcript is not the chat text. Parse every line (user turns, assistant turns, tool calls, tool results), because much of what goes wrong lives in a tool call and its result: the wrong file edited, a retry loop that burned ten calls to do what one would, a tool error silently absorbed while the agent carried on.

When a tool result was too large to inline, the harness saves it to a file and leaves an "output saved to..." pointer. Open that file too; it holds the long, messy steps most likely to matter.

Never substitute the session's own closing summary (a compaction summary, a final "here's what I did") for the turns. The agent under review wrote it, and it smooths over exactly the moments this report exists to surface.

## 3. The human writes the first notes

The human writes the notes; the agent organises them. Read a transcript (or let the agent surface candidate moments) and write one line per moment that felt wrong, in your own words: a wrong assumption, a step repeated for no reason, a tool call that shouldn't have happened, a question that should have been asked, output you had to push back on. Your read of "that was wrong" is the ground truth, not a match on words like "error" or "sorry".

Only after roughly five human notes point at the same kind of thing does it become a named failure mode worth searching the rest of the batch for. Before that, it is one data point; naming a mode too early locks in a guess.

Expect the notes to drift: a mode from session 3 may turn out to be one from session 7, described differently. Regroup rather than forcing the first label to stick.

## 4. Stop condition

Stop reading new sessions once two in a row add neither a new failure mode nor a new instance of an existing one. Record how many sessions were read and the date range they span.

## 5. Write the report

One section per failure mode:

- The mode, named in plain words, not a category label borrowed from a bug tracker.
- Its count across the batch (for example "4 of 12 sessions").
- One to three concrete examples: which session, roughly where in it, and a short verbatim quote or close paraphrase.
- A one-line guess at what kind of thing it is (a prompt or skill wording issue, a missing check, a one-off), without turning it into a recommendation.

Redact anything that looks like a secret, token, password, API key or personal data pulled from a tool result before it goes in the report.

Close with what the report does not cover: sessions you didn't get to, anything unreadable, anything the human didn't have time to note.

### What this report is not

- Not a list of fixes, prompt patches or skill edits. If a fix is obvious, say so in one clause inside the mode's section, but do not build it, draft it or hand it to `diagnose-bug`.
- Not a severity score you invented. A count and real examples let the reader judge severity.
- Not an eval suite. "Can we measure whether this gets better or worse" is `evals`.

## 6. Update the ledger

Only after the report is written, add or update one line per session read in your laptop's section of `ledgers/transcripts.md`, in the format at the top of that file, with the library's short git sha. Then prune your laptop's section: delete every line whose session file no longer exists on this machine (no `~/.claude/projects/*/<session-id>.jsonl`), since nothing can match it again. Keep every line whose file exists, active or not, or that session would be read twice. Never touch the other laptops' sections. Then commit the ledger. If the run failed halfway, the ledger stays as it was and the next run reads those sessions again. The ledger is in a public repo: ids, dates and counts only.

## Rationalisations to refuse

- "The closing summary already says what happened": the agent under review wrote it; read the turns.
- "I'll grep for 'error' or 'sorry'": that misses failures that read as confident and correct, such as scope creep, redoing finished work, or answering the wrong question well.
- "I already know the modes from a past batch": read this batch anyway; modes fade and appear, and the counts must come from what is in front of you.
- "The agent can write the first notes, it saw the transcript too": then the agent is reviewing itself; the human's one-line read is the input this skill runs on.
- "One example is enough, it's obviously a pattern": find the fifth before naming the mode.

## Done when

- [ ] Every session in the batch was read in full, including anything the harness saved to a file.
- [ ] Every failure mode traces back to a human-written note.
- [ ] Each mode shows its count and at least one example a reader could find in the source session.
- [ ] Nothing in the report is a proposed fix, a patch or a hand-off to another skill.
- [ ] Anything skipped, unread or redacted is stated.
- [ ] The ledger lists every session read, under the right laptop, holds no content, and has no line for a transcript that is gone.
