---
name: analyze-agent-transcripts
description: Use when you want to know what is actually going wrong across a batch of your own Claude Code or Cowork session transcripts, before deciding what to fix. Not for turning that same data into eval items, a judge or a gated test suite; that is evals. Not for root-causing one failure you already have in hand; that is diagnose-bug. Not for mining a video, article or book for ideas; that is extract-insights.
---

# Analyse agent transcripts

You are reading real Claude Code or Cowork sessions, run against your own work, to find out what keeps going wrong before anyone decides what to do about it. The output is a report of failure modes.

## 0. Setup, on every run

Check both of these at the start of every run (two file reads) and say nothing when they are fine. If one is missing, tell the user and change a file only with their yes. Merge into existing content and keep it valid.

**Retention.** Read `cleanupPeriodDays` in `~/.claude/settings.json`. Claude Code deletes transcripts older than that, and the default is 30 days when it is unset (https://code.claude.com/docs/en/settings-reference.md#cleanupperioddays). The user's chosen value is 120, which covers a run every few months. If it is unset or lower, add `"cleanupPeriodDays": 120`.

**Usage meter.** Claude Code gives the status line the account's five-hour usage. The pacing below reads it from `~/.claude/state/usage.json`, which the status line script must write. If the user's status line script (the `statusLine` command in `~/.claude/settings.json`) lacks it, add these lines after its `jq` check, where `$input` is the JSON the script reads from stdin:

    mkdir -p "$HOME/.claude/state"
    echo "$input" | jq -c 'select(.rate_limits != null) | {at: (now | floor), rate_limits}' > "$HOME/.claude/state/usage.json.tmp.$$" 2>/dev/null \
      && [ -s "$HOME/.claude/state/usage.json.tmp.$$" ] && mv "$HOME/.claude/state/usage.json.tmp.$$" "$HOME/.claude/state/usage.json"

If the user has no status line, the meter file is simply never there, and the pacing asks for the number instead.

## Pacing: share the five-hour window, never drain it

The run may use 30% of what is left in the five-hour window when it starts, and it works in small batches so it can check.

a. **Read the meter.** Take `rate_limits.five_hour.used_percentage` from `~/.claude/state/usage.json` as the current use. If the file is missing, older than 10 minutes (`at`), lacks `five_hour`, or its `resets_at` is in the past, ask the user for the number from `/usage` instead. Read it before the run (call it `start`) and again before each batch, only after the previous batch's results are back in the main session, because the status line updates on a main session response.
b. **Stop line:** `start + 0.30 × (100 − start)`, and never above 80. Example: 70 used, stop at 79. 10 used, stop at 37. A start above 80 means no run.
c. **Batches** of about 4 sessions. After the first batch, take its cost as the rise in the meter; start another only if the current reading plus that cost is at or under the stop line.
d. **Save after each batch:** its candidate moments go to a notes file (`~/.claude/state/transcript-run-notes.md` unless the user names another), with secrets redacted as they are written, and the ledger is updated as section 6 says. The notes are the durable record, so stopping loses nothing.
e. **When the run stops,** say how many sessions are done and how many remain, and when the window resets (`resets_at` if the meter has it, else "within five hours"). The user says "continue" later; the ledger and the notes make the next run pick up where this one stopped.
f. **Subagents:** no cap is needed, because the meter is checked between batches. Launch one batch at a time and wait for it. Readers use Sonnet 5.5 and never Haiku. Synthesis stays in the main session, on whatever model it runs.

## 1. Gather the batch

Claude Code sessions are JSONL files, one per session, under `~/.claude/projects/<slug>/<session-id>.jsonl`, where `<slug>` is the working directory path with `/` replaced by `-`. If more than one project slug could match, or the user hasn't said which sessions, ask rather than guess: "your last 10 sessions in this project" and "every session since Monday across all projects" are different batches with different reports.

Read the ledger of sessions already read: `ledgers/transcripts.md` when this skill sits inside a clone of the agents library, otherwise `~/.claude/state/transcript-ledger.md` in the same format (an installed copy has no library, so no short sha and no commit). Ask which laptop section this machine is (offer the existing ones; a new laptop gets a new section). Skip every session whose id is already in that section, unless the file now has more lines than the ledger says were read: then read it in full from the line after that number. Skip a session written to in the last hour, since it is probably still live. If nothing is new, say so and stop.

With no count or date range given, take the newest unread sessions first and go as far as the pacing budget allows, and say so at the top of the report. The rest wait for the next run.

For a Cowork session, ask the user for the transcript (export, link or file) rather than guessing a local path; Cowork sessions often don't run on this machine. Cowork sessions are not entered in the ledger, since no local file exists for pruning to check.

## 2. Read each one whole

A transcript is not the chat text. Parse every line (user turns, assistant turns, tool calls, tool results), because much of what goes wrong lives in a tool call and its result: the wrong file edited, a retry loop that burned ten calls to do what one would, a tool error silently absorbed while the agent carried on.

When a tool result was too large to inline, the harness saves it to a file and leaves an "output saved to..." pointer. Open that file too; it holds the long, messy steps most likely to matter.

A script may shorten a session into a digest before a reader sees it. It keeps every user and assistant sentence, each tool call with its input shortened (the path or command), errors, timestamps and "output saved to" pointers, and replaces bulky tool results (file dumps, long logs) with `[dropped, N lines]`. The reader asks for the raw spot from that marker when it matters.

Never substitute the session's own closing summary (a compaction summary, a final "here's what I did") for the turns. The agent under review wrote it, and it smooths over exactly the moments this report exists to surface.

## 3. The human writes the first notes

The human writes the notes; the agent organises them. Read a transcript (or let the agent surface candidate moments) and write one line per moment that felt wrong, in your own words: a wrong assumption, a step repeated for no reason, a tool call that shouldn't have happened, a question that should have been asked, output you had to push back on. Your read of "that was wrong" is the ground truth, not a match on words like "error" or "sorry".

When readers work in batches, they return candidate moments, saved as candidates, never as the human's notes. The human adds their one-line reads when they review the candidates. A session counts as read in the ledger once its candidates are saved.

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

After each batch's candidates are saved (Pacing d), add or update one line per Claude Code session read in your laptop's section of the ledger, in the format at the top of that file (with the library's short git sha when it is the library ledger). Then prune: delete every line in your section whose session file no longer exists on this machine (no `~/.claude/projects/*/<session-id>.jsonl`), since nothing can match it again. Keep every line whose file exists, active or not, or that session would be read twice. Never touch the other laptops' sections, and confirm the section with the user before pruning; if most of the section's files are missing, the wrong section was probably chosen, so do not prune and ask. A batch that failed before its candidates were saved gets no ledger lines, so the next run reads it again. Commit the library ledger once at the end of the run, and push only if the user asks. The library ledger is in a public repo: ids, dates and counts only.

## Rationalisations to refuse

- "The closing summary already says what happened": the agent under review wrote it; read the turns.
- "I'll grep for 'error' or 'sorry'": that misses failures that read as confident and correct, such as scope creep, redoing finished work, or answering the wrong question well.
- "I already know the modes from a past batch": read this batch anyway; modes fade and appear, and the counts must come from what is in front of you.
- "The agent can write the first notes, it saw the transcript too": then the agent is reviewing itself; the human's one-line read is the input this skill runs on.
- "One example is enough, it's obviously a pattern": find the fifth before naming the mode.

## Done when

- [ ] Every session in the batch was read in full (from the ledger's line for a session already partly read), including anything the harness saved to a file.
- [ ] Every failure mode traces back to a human-written note, and anything still only a candidate is labelled so.
- [ ] Each mode shows its count and at least one example a reader could find in the source session.
- [ ] Nothing in the report is a proposed fix, a patch or a hand-off to another skill.
- [ ] Anything skipped, unread or redacted is stated.
- [ ] The run stayed under its stop line, checking the meter before every batch.
- [ ] The ledger lists every Claude Code session read, under the right laptop, holds no content, and has no line for a transcript that is gone.
