# Daily brief

When the user asks for a summary or brief of their work ("since yesterday's sync", "what happened today"), this file sets how to build it. The user's own settings live in a private config file outside this repo (`~/.claude/cos/brief-config.md`): their name, time zone, project trackers, epics, channels, repos and the sources to read. Read it first. If it is missing, ask for those settings once and write the file.

## The window

A brief covers everything since the last brief, never a fixed number of hours. Keep the last-run time, cursors and open commitments in `~/.claude/cos/brief-state.md`. When the user names a start point ("since yesterday's morning sync"), find that meeting in the meeting notes and start right after it. Open with one line: "Covers <start> to <now>". If the gap is more than a day, say so. Update the state file only after the brief is given, so a failed run does not move the cursor.

## Read every source before writing

The registry and the threads' notices are only one source. Before the first line of the brief, read:

1. The registry and the log (what the threads did).
2. GitHub: PRs the user authored or reviewed, and CI on the default branch.
3. The tracker (Jira or similar): the user's tickets in the active sprint, grouped by epic, and what closed.
4. Chat (Slack or similar): mentions, DMs, replies to the user's questions, threads about their tickets and PRs.
5. Meeting notes: the meetings in the window, read from the transcript when the summary is thin.
6. Docs: new comments on the user's design pages.
7. Mail and calendar: only work items that need the user, and the next 7 days of meetings that need preparation.

A source that cannot be read (disconnected, expired, refused) is named at the top and the user is asked to reconnect it. Never present a brief as complete when a source was skipped.

Check each claim against its source before it goes in. Where two sources disagree (a thread's state file says "approved", the chat thread shows no approval), show both and say which one is newer.

## Scope

Only the work the user names in the config. Skip personal projects, personal meetings, newsletters and other people's merged PRs without mentioning them.

## Shape

Group by epic or project, the most blocked first. For each one, in full sentences:

- what moved (merged, approved, decided), with links;
- what is blocked, on whom, since when, with the thread or PR link;
- what is waiting on the user, each with the option you recommend.

Then the meetings ahead that need preparation, and the open questions in both directions (asked of the user, asked by the user and unanswered). Low-signal items get at most a few one-liners at the end, or are left out.

## What you never do

Read only. No posts, replies, reactions, comments, ticket changes or mail drafts in any source. The brief is a message to the user, not to their colleagues; if they will paste parts of it, remind them to rewrite it in their own voice and to share any linked doc with everyone who will read it.
