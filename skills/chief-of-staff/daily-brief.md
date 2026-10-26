# Daily brief

When the user asks for a summary or brief of their work ("since yesterday's sync", "what happened today"), this file sets how to build it. The user's own settings live in a private config file outside this repo (`~/.claude/cos/brief-config.md`): their name, time zone, project trackers, epics, channels, repos and the sources to read. Read it first. If it is missing, ask for those settings once and write the file.

## The window

A brief covers everything since the last brief, never a fixed number of hours. Keep the last-run time, cursors and open commitments in `~/.claude/cos/brief-state.md`. When the user names a start point ("since yesterday's morning sync"), find that meeting in the meeting notes and start right after it. Open with one line: "Covers <start> to <now>". If the gap is more than a day, say so. Update the state file only after the brief is given, so a failed run does not move the cursor.

## Reconnect sessions first

Read the tail of `~/.claude/state/rc-reconnect.log` before anything else (SKILL.md, "Keep every session reachable"): the daily timer runs the reconnect, so you do not. Sessions it reconnected are not mentioned; any FAILED or NOT IN TMUX line in the latest run goes under "Needs you" with the line to type. Run `scripts/rc-reconnect` yourself only after an account switch or when a session shows disconnected.

## Read every source before writing

The registry and the threads' notices are only one source. Before the first line of the brief, read:

1. The registry and the log (what the threads did). Then ask every open thread for its pending items, each with what it is, who it waits on (the user, a teammate or the thread) and since when, and wait for the replies. This is on top of your own sweep of the sources below, never in place of it, so nothing waits for days without the user seeing it.
2. GitHub: PRs the user authored or reviewed, and CI on the default branch.
3. The tracker (Jira or similar): the user's tickets in the active sprint, grouped by epic, and what closed.
4. Chat (Slack or similar): mentions, DMs, replies to the user's questions, threads about their tickets and PRs.
5. Meeting notes: the meetings in the window, read from the transcript when the summary is thin.
6. Docs: new comments on the user's design pages.
7. Mail and calendar: only work items that need the user, and the next 7 days of meetings that need preparation.

## Everything waiting on the user

Every brief carries a full inventory of what waits on the user, swept fresh from each source, never only from the threads' notices. Threads report what they work on; a PR or ticket no thread owns still waits on the user. Failure this prevents: open PRs and review requests went unseen because the brief was built from the registry.

1. GitHub, in every repo the config names: open PRs the user authored (with review state, CI, draft, and whether it is approved and waiting only on their merge); PRs requesting the user's review by name (team requests are left out: the user is not the reviewer there); PRs where someone asked the user a question in a comment. Sessions push under the user's account, so "authored by the user" includes every thread's PRs.
2. The tracker: tickets assigned to the user and not done, in or out of the sprint; tickets where the user is mentioned or asked something since the last brief; tickets whose status no longer matches the PR state.
3. Chat: unanswered DMs and mentions, and questions the user asked that got a reply.
4. The registry: every thread's needs-user items, checked against GitHub so a merged PR does not stay listed.

List each item once, with its link, how long it has waited and the one action needed. Give the exact queries in the config so every brief runs the same sweep.

A source that cannot be read (disconnected, expired, refused) is named at the top and the user is asked to reconnect it. Never present a brief as complete when a source was skipped.

Check each claim against its source before it goes in. Where two sources disagree (a thread's state file says "approved", the chat thread shows no approval), show both and say which one is newer.

## Keep the user's ToDo page

The user keeps a daily ToDo page (Notion or similar), and you maintain it, because they cannot. On the first brief, ask them for its link and save it in the config. With every morning brief, tick each item from earlier days that is done, citing the evidence you checked (a merged PR, a closed ticket, the thread's report), and leave anything you could not check unticked and ask about it once. Then add today's dated section at the top, in the page's own style, holding every open item from "Needs you".

## Scope

Only the work the user names in the config. Skip personal projects, personal meetings, newsletters and other people's merged PRs without mentioning them.

## Shape

The reader has a few minutes and one question: what do I have to do, and what could hurt my projects? So the brief is grouped by what the reader does with an item, not by project, and each item names its project in a short tag. Sections in this order, each left out when empty:

1. **Needs you.** Only what the user can unblock: an action only they can take (a merge, an apply, a review asked of them by name, a decision within their project), or a person they should ask who has not been asked yet. Before listing an ask, search chat and the PR for whether the user already asked or the other person already answered; if so, it moves to "Blocked on others" with that message linked. Each item carries its context in one or two sentences: what it is, why only the user can do it, what it unblocks, and how long it has waited. An item the reader cannot act on from the brief alone ("say who owns the drift", "yes or no on a note") is not ready: get the context from the thread first.
   Not the user's to decide: other teams' work, risks someone else owns, and deferrals. Deferrals go to the project's ToDos page (`references/project-todos.md`); risks owned elsewhere go under "At risk" with who owns them. Tell the thread that raised it, so it fixes its own list.
2. **At risk.** Anything that can quietly break or stall a project, even when every PR looks done. Merged but not live is the main case: Terraform not applied, an image not rebuilt or rolled, a deploy not run since the merge, a pin bumped in the repo while the running service is on the old one. Also drift someone else left in a shared Terraform root, failing CI on the default branch, an access or token about to expire, and a ticket whose status contradicts its PRs. For merged-not-live, check the deploy runs and, when credentials allow, the live system; say which it was.
3. **Blocked on others.** Who, since when, what they said they would do and by when ("Aman will review on Monday"), with links to the PR and to the message. Flag anything waiting more than two working days past their own date.
4. **Done since the last brief.** Outcomes, not PR lists: one bullet per thing that now works, in plain words, and how it moves the project's goal ("the investigators no longer guess a default datasource, so a log query that names no data is refused instead of answering from the wrong place"). Several PRs that deliver one outcome are one bullet. No PR links here; the reader will not open them. Other people's work is left out.
5. **Meetings ahead** that need preparation, and open questions in both directions.

Rules for every item: in the sections the reader acts on (needs you, at risk, blocked), every PR, ticket, doc or thread gets its own link, never a range like "#45564 to #45594"; an item appears once, in the first section it fits; a full sentence per item, no more. Status that changes nothing for the reader (a thread still working, a draft still in review) is left out. Put the window line and any unread source at the top.

## What you never do

Read only. No posts, replies, reactions, comments, ticket changes or mail drafts in any source. The brief is a message to the user, not to their colleagues; if they will paste parts of it, remind them to rewrite it in their own voice and to share any linked doc with everyone who will read it.
