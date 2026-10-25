---
name: analyze-agent-transcripts
description: Use when you want to know what is actually going wrong across a batch of your own Claude Code or Cowork session transcripts, before deciding what to fix. Not for turning that same data into eval items, a judge or a gated test suite; that is evals. Not for root-causing one failure you already have in hand; that is diagnose-bug. Not for mining a video, article or book for ideas; that is extract-insights.
---

# Analyse agent transcripts

You are reading real Claude Code or Cowork sessions, run against your own work, to find out what keeps going wrong before anyone decides what to do about it. The output is a report of failure modes.

## 0. Setup, once per laptop

Check both of these the first time the skill runs on a laptop, tell the user what is missing, and change a file only with their yes. Merge into existing content and keep it valid.

**Retention.** Read `cleanupPeriodDays` in `~/.claude/settings.json`. Claude Code deletes transcripts older than that, and the default is 30 days when it is unset (https://code.claude.com/docs/en/settings-reference.md#cleanupperioddays). The user's chosen value is 120, which covers a run every few months. If it is unset or lower, add `"cleanupPeriodDays": 120`.

**Usage meter.** Claude Code gives the status line the account's five-hour usage. The pacing below reads it from `~/.claude/state/usage.json`, which the status line script must write. If the user's status line script (the `statusLine` command in `~/.claude/settings.json`) lacks it, add these lines after its `jq` check, where `$input` is the JSON the script reads from stdin:

    mkdir -p "$HOME/.claude/state"
    echo "$input" | jq -c 'select(.rate_limits != null) | {at: (now | floor), rate_limits}' > "$HOME/.claude/state/usage.json.tmp" 2>/dev/null \
      && [ -s "$HOME/.claude/state/usage.json.tmp" ] && mv "$HOME/.claude/state/usage.json.tmp" "$HOME/.claude/state/usage.json"

If the user has no status line, ask them to read the five-hour percentage off Claude Code (`/usage`) before each batch instead.

## 1. Gather the batch

Claude Code sessions are JSONL files, one per session, under `~/.claude/projects/<slug>/<session-id>.jsonl`, where `<slug>` is the working directory path with `/` replaced by `-`. If more than one project slug could match, or the user hasn't said which sessions, ask rather than guess: "your last 10 sessions in this project" and "every session since Monday across all projects" are different batches with different reports.

Read `ledgers/transcripts.md` in this library. Ask which laptop section this machine is (offer the existing ones; a new laptop gets a new section). Skip every session whose id is already in that section, unless the file now has more lines than the ledger says were read: then read only the lines after that number. Skip a session written to in the last hour, since it is probably still live. If nothing is new, say so and stop.

With no count or date range given, take the newest unread sessions first and go as far as the pacing budget allows, and say so at the top of the report. The rest wait for the next run.

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

## Pacing: share the five-hour window, never drain it

The run may use 30% of what is left in the five-hour window when it starts, and it works in small batches so it can check.

1. Read `used_percentage` under `rate_limits.five_hour` in `~/.claude/state/usage.json` before the run, and call it `start`. Check that `at` is recent; if it is old, ask the user for the number.
2. The run's stop line is `start + 0.30 × (100 − start)`, and never above 80. Example: 70 used, stop at 79. 10 used, stop at 37.
3. Work in batches of about 4 sessions. Before each batch read the meter again. If it is at the stop line, or under 20% of the window remains, start no batch.
4. After each batch, save its notes to a file (`~/.claude/state/transcript-run-notes.md` unless the user names another) and add the ledger lines for the sessions it read. The notes are the durable record, so stopping loses nothing.
5. When the run stops at the line, say how many sessions are done and how many remain, and when the window resets (`resets_at` in the meter file, else the five-hour mark). The user says "continue" later; the ledger and the notes make the next run pick up where this one stopped.
6. No cap on subagents is needed, because the meter is checked between batches. Launch one batch at a time and wait for it. Readers use Sonnet 5.5 and never Haiku. Synthesis stays in the main session, on whatever model it runs.
7. A script may shorten a session into a digest before a reader sees it, keeping every user and assistant sentence, tool name, error and timestamp and dropping only bulky tool output (file dumps, long logs). The raw file stays available to open at a flagged spot.

## 6. Update the ledger

After each batch's notes are saved (see Pacing), add or update one line per session read in your laptop's section of `ledgers/transcripts.md`, in the format at the top of that file, with the library's short git sha. Then prune your laptop's section: delete every line whose session file no longer exists on this machine (no `~/.claude/projects/*/<session-id>.jsonl`), since nothing can match it again. Keep every line whose file exists, active or not, or that session would be read twice. Never touch the other laptops' sections. Then commit the ledger. A batch that failed before its notes were saved gets no ledger lines, so the next run reads it again. The ledger is in a public repo: ids, dates and counts only.

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
- [ ] The run stayed under its stop line, checking the meter before every batch.
- [ ] The ledger lists every session read, under the right laptop, holds no content, and has no line for a transcript that is gone.
