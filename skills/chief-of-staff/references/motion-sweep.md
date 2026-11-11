# Motion sweep

The coordinator's failure is silence with no reason: a thread stops, sends no message, and nobody notices until the user asks. On 11 November 2026 two threads (m1 and m2) sat on DeepSeek's "Enter to continue" notice; both were freed with one keystroke, but only because the admin restarted and read the panes. The user's rule, 11 November 2026: "make sure that threads are moving at optimal capacity" every so often, whether that is every 5, 10 or 100 messages or every 30 to 60 minutes.

## The rule

Run `python3 scripts/cos-sweep` at every batch and at least every 20 minutes while coordinating. Act on every ACT line in the same turn, before the next message. Clean OK lines are recorded, not relayed (the silence rule in the skill still holds).

Set the timer at takeover: `CronCreate` every 17 minutes, prompt "Run the chief-of-staff motion sweep: python3 ~/oss/agents-library/skills/chief-of-staff/scripts/cos-sweep, act on every ACT line, update ~/.claude/cos/threads.json, stay silent unless a thread needs the user or stays stuck after one action". Cron jobs are session-only and expire after seven days, so set it again after a restart.

## What it reads

- `~/.claude/cos/threads.json`: each thread's stage, `waiting_on`, `needs_user` and address.
- `~/.claude/sessions/*.json`: the live session behind each name, its status (`busy`, `idle`, `shell`, `waiting`), its tmux pane and its socket.
- The last lines of each tmux pane: a stall notice shows there even when the session emits nothing.
- Each session's transcript mtime: the last sign of activity, in minutes.

## Act on what it finds

- **Stall notice** in the pane: dismiss it with `tmux send-keys -t <pane> Enter` and leave the thread to resume. This is the failure the sweep exists for.
- **Address changed**: update the registry from the live record and re-send the thread's last instruction to the new address, because messages to the old one are lost.
- **No live session**: the thread is lost. Read its flow file for its state, mark the registry entry, and tell the user what is left and where it lives.
- **Waiting for input** in the pane: read the prompt and answer it from the registry and the flow file, or record why it waits on the user.
- **Idle or shell with no recorded wait**: ask the thread for its next step, or record the person or event it waits on. A thread with no next step and no wait is a thread to close or rename, which is a suggestion for the user.
- **Unread failed run**: a suite end line named after the thread, failed and newer than its transcript, means a background result arrived after the session's last turn and no notice woke it. Nudge with the run's name, tree, key and failing tests, then let the thread act. On 11 November 2026 m3 sat at the prompt for 22 minutes over a scoped set that failed at 20:12. Name every suite run with its thread's name so this check can find it.
- **A waiter with no positive check**: a completion notice is not guaranteed to wake an idle session, and a waiter whose process died sends nothing at all. Every background waiter names the file, line or status it will read. The sweep catches suite end lines and notices; a billing stop, a lock holder or a permission prompt needs its own check, and a thread idle with no recorded wait is a stall. On 11 November 2026 #152 sat on draft for five hours behind waiters that had died with exit 144.
- **Busy**: leave it alone, unless it has run far past its stated step; then read its flow file before nudging.

## Optimal capacity

Every thread is doing one of two things: advancing toward its next mergeable step, or waiting on a named person or event recorded in the registry with a date. A thread that is silent with no recorded wait is stalled, not idle. Idle costs nothing only when the wait is real. The sweep's job is to make the difference visible before the user has to ask.

## Failure this prevents

A message-driven admin only sees threads that speak. The threads that need help most are the ones that cannot: a session on an interactive notice, a dead address, a session that exited. On 11 November 2026 the user named this: "some thread just slept and you lost track of it, I don't like things like that."
