---
name: ship
description: Use when the user says /ship followed by the reviewer session's process ID and what to build, to run spec, plan and PR through a separate reviewer session and the user's approval at each stage, until the PR merges. Also used by the reviewer session when a "[ship" review request arrives.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: 'p="$CLAUDE_PLUGIN_ROOT/skills/ship/scripts/refuse-gh-pr-merge.py"; [ -f "$p" ] || p="$CLAUDE_PROJECT_DIR/.claude/skills/ship/scripts/refuse-gh-pr-merge.py"; [ -f "$p" ] || p="$HOME/.claude/skills/ship/scripts/refuse-gh-pr-merge.py"; [ -f "$p" ] || exit 0; python3 "$p"'
          timeout: 10
---

# Ship

One command runs the whole pipeline. You (the author) write each stage, and a separate reviewer session reviews it until it approves. The user reviews the spec and the plan together, once the reviewer has approved both: after the reviewer approves the spec, write the plan without waiting for the user. The user then approves the PR stage on its own.

```
/ship 62540 <what to build>     (62540: the number in the reviewer's /status Peer address)

 author (you)                        reviewer session                user
 ────────────                        ────────────────                ────
 stage: spec ─► plan ─► pr ─► merged
   │
   ├─ write or revise ─────────────► review (3 rounds per approach)
   │◄──────────── verdict + findings ┘      ▲
   │  fold, reply per finding, resend ──────┘   (a new approach starts a new count)
   │
   ├─ spec approved by reviewer ──► write the plan, same loop (no wait for the user)
   │
   ├─ plan approved by reviewer ─────────────────────────► reads spec + plan together
   ├─ pr approved by reviewer ───────────────────────────► reads the PRs
   │◄────────────────────────────────────────── "bugs: ..." → back to review
   │◄────────────────────────────────────────── "approved"  → next stage
```

Apply `references/handoff-protocol.md`. The stage skills do the work: `write-spec`, `write-plan`, `implement-plan` for you, `review-plan` (spec and plan) and `review-pr` for the reviewer.
This skill also names `references/engineering-principles.md`, `references/testing.md`, `references/verification.md`, `references/visuals.md`, `references/human-time.md`, `references/review-evals.md`, `references/risk-tiers.md`, so every reference it needs is one level from this file.

The references this skill names rely on these, so read them in full too: `references/shipping.md` (deploying and checking a change live), `references/judgement.md` (what to add beyond the request, and when to stop), `references/core.md` (the core actions).

## Models

| Session, stage | Model and effort |
|---|---|
| Author: spec and its research | Opus 5.5 medium |
| Author: plan and PRs | Sonnet 5.5 high. A session can't switch itself: once the reviewer approves the spec, ask the user in your tab to run `/model sonnet` and `/effort high` |
| Reviewer: every stage | Opus 5.5 medium |

The user set these on 11 Nov 2026 from cost per task (Artificial Analysis index, CursorBench): the spec decides the most, and a sound spec plus review makes coding work for Sonnet. A coordinator may start a small, fully specified job on Sonnet 5.5 high from the start.

## Starting

**`/ship <number> <text>`**. The user opens a fresh session for the reviewer, runs `/status` there and gives the number in its **Peer address** (`uds:/tmp/cc-socks/62540.sock` → `/ship 62540 ...`). It is that session's process ID, unique among running sessions. Send to `uds:/tmp/cc-socks/<number>.sock`. A full address or a name ListAgents shows in place of the number works too. Session IDs and the `/status` session name do not: SendMessage refuses them. `<text>` plus this conversation is the brief. When the project's docs disagree, the newest one wins: check each source's date.

- Send the reviewer a first message: `[ship <topic>] you are the reviewer`, the state file path, and "load the ship skill and follow As the reviewer". It needs nothing typed by the user.
- If the send fails or the address is this session's own, tell the user and stop.
- **`/ship`** alone: list the flows in `~/.claude/flows/` and resume the one the user picks.
- Pick the first stage from the brief: spec, unless the user says an approved spec or plan already exists.
- **Before the first stage, ask the user two things in one message**, each with your guess. These are admin choices: always ask, on every new flow and every resume (show what the state file recorded and ask if it still holds). Never take them from another flow or from memory without asking.
  1. **Where the approved artifacts go.** Each task has its own store, usually a Notion hub page. Propose the one this conversation already uses, if any. Each approved spec and plan (docs and artifacts) then gets one link there, added only after the user approves it. Never individual PRs: a hub page holds child docs and artifacts only. Never a draft. Ask in the same question whether you may add the link yourself; if not, give the user the line to paste. The same page holds the project's ToDos: apply `references/project-todos.md` (every deferral from any source, the same turn, kept current by adding, updating, ticking and deleting).
  2. **Which Jira tickets this belongs to.** Search first (`assignee = currentUser()`, open, matching the brief) and propose the likely ones. Record them only. Never update Jira per PR: at a milestone the user names, draft one update and the user decides.

## The merge guard

Loading this skill registers a hook: a direct `gh pr merge` is always refused, and `gh api .../merge` is refused where the repo has a `scripts/land`, because there the flow lands through that script. A repo without one runs the API call in `references/stacked-prs.md` directly. `scripts/land`, `gh pr view`, help flags and every read pass. The hook exits 0 when its own script cannot be found, so a copied skill never blocks Bash. It is a guardrail, not a security boundary. A refusal means run `scripts/land <PR>` where it exists, or the API call in `references/stacked-prs.md` where it does not; never rephrase the merge to get past the guard. The hook lasts for the rest of the session.

The command resolves the script through the plugin root when the library is loaded as a plugin, through the project's `.claude/skills` when the skill is copied into a repo, and through `~/.claude/skills` when `scripts/setup` installed it. A copy anywhere else leaves the guard off. The hook is a Claude Code extension; another harness ignores it and the guard is off there.

## The state file

`~/.claude/flows/<topic-slug>.json`, outside any scratchpad, so both sessions can read it. Write it at every change. After a compaction, read it before doing anything; trust it over memory.

```json
{"topic": "runbook PR 2", "author": "anyscale-e5", "reviewer": "anyscale-a9",
 "stage": "plan", "version": 3, "round": 2, "approach_changed": null,
 "artifacts": [{"kind": "spec", "url": "https://claude.ai/artifact/spec...", "source": "/path/spec.html"},
               {"kind": "plan", "url": "https://claude.ai/artifact/...", "source": "/path/plan.html"}],
 "contract": "spec v25 https://claude.ai/artifact/...", "repo": "anyscale/x", "pr": null,
 "base_commit": "7ff2d92", "human": "waiting",
 "findings": [{"id": "R2", "severity": "required", "origin": "new", "class": "error-path",
               "round": 2, "outcome": null, "survived": null}],
 "store": "https://app.notion.com/p/...", "jira": ["ART-123"],
 "heads": {"anyscale/x#123": "abc1234"}}
```

`round` is a gate, not a note: a fourth round needs `approach_changed` set to what changed, and the reviewer refuses a round 4 request without it. `findings` records every finding: id, severity, origin, class, round, outcome (null until a reply, then one of the four reply words) and `survived`, true when the fix was still there at the merge. `artifacts` lists each hand-off artifact by `kind` (spec, plan, diagram, recording) with its link and source path; an older flow's single `artifact` object reads as one entry.

`heads` holds every open PR's current head SHA, updated at every push, so anyone can check an approval against GitHub. An approval covers one commit: a push after it voids it.

## The loop, per stage

1. **Shape first**, as write-spec's "Shape before spec" says, for the plan as well as the spec: the reviewer never sees a document whose shape the user has not settled.
   **Write or revise** with the stage's skill. Publish the artifact (spec, plan) or push the branches (PR). The PR stage is a stack of atomic PRs by default: each one builds, passes CI and is reviewable alone, and the plan names the cut. One big PR only when the user agrees to it in the plan. Push the stack linear (`references/stacked-prs.md`): every fix is an ordinary commit on the branch that owns it, and a merge commit only brings in the branch below. Spec questions the user must decide go to the user first, as `write-spec` says; the reviewer never answers them.
2. **Send a review request** with SendMessage. First line: `[ship <topic>] <stage> v<n> round <r>: review request`. Second line names the skill to load: `use review-plan` for a spec or plan, `use review-pr` for a PR, so a reviewer that lost its context still knows. Then: the artifact the rule names, with its link and source path (`references/handoff-protocol.md`, "The hand-off leads with its artifact"), the contract it must meet (the brief for a spec, the reviewer-approved spec for a plan, the approved plan for a PR), `base_commit..HEAD` and the PR for code, the state file path, and the user's standing rules. Never your own verdict on it.
   Keep messages short: links and paths, never pasted documents. The artifact and the state file carry the content.
3. **End your turn without telling the user.** Review rounds, fixes, pushes and CI runs are not news to the user: no message about them, not even one line. The reviewer's reply wakes you; never poll. A turn the reviewer, a peer or a background task woke ends with no text at all, because every turn end marks the tab for the user. The user hears from you only at the hand-off in step 5, once the reviewer has approved and CI is green, or for a blocker only they can clear (`references/respect-human-attention.md`, "Silent while a loop runs").
4. **On findings**: check each against the source, fix every instance of its class (search the repo for every copy of what it named, and read the fix back from the pushed head, not from your own summary), rerun the checks, then reply per finding with one of four words and the reason: `fixed` (with `fixed in <sha>; swept N other places, found M`), `wrong`, `intentional` or `not-material`. Resend as round r+1.
   A stage gets three rounds per approach (`references/handoff-protocol.md`, "Three rounds, then the approach"). Only `required` findings start a new round; carry `optional` ones to the user's hand-off. After round 3 without approval the reviewer asks for an approach change: change the approach, not the words, record `approach_changed`, and the next round starts from a full read; a genuine new bug in the new approach is a finding like any other. Stop and ask the user only when the author and the reviewer disagree about a requirement (what to build, not whether it works), since only the user can settle that. Before resending, run the simplicity pass from `write-spec`: if the fixes this round piled onto one mechanism, replace the mechanism.
5. **On approve**: at the spec stage, record `reviewer_approved` for the spec and start the plan straight away (step 1 for the plan); do not ask the user yet. At the plan and PR stages, send a PushNotification, then give the user one screen: the artifact first (for the plan, both the spec and the plan links; at the PR stage, the artifact `references/handoff-protocol.md` names, with its link), then the minimum text: what the reviewer checked, findings you rejected and why, and anything only the user can decide. Set `human: waiting`.
   At the PR stage, PRs are opened as drafts while the reviewer loop runs. On the reviewer's approve, mark that PR ready for review yourself (`gh pr ready`) before the hand-off, and give the user the PR link to review. Never ask the user whether a draft may be opened. Opening a PR can request reviewers automatically (CODEOWNERS); say who was requested in the hand-off. Merging still waits for the user's approval and green CI. The PR description opens with its artifact (`references/handoff-protocol.md`, "The hand-off leads with its artifact"), then the caption: intent, risk, **How to revert** and **What to watch, and when**, or a pointer at the rollback plan in `references/shipping.md`. Reread all of it against the exact head before the hand-off.
   Before the hand-off, answer and resolve every comment thread on the PR from anyone (people, review bots, scanners, other agents) on the exact head, and name the command that shows none is open (`references/handoff-protocol.md`, Gates). A PR with a pending comment is not ready.
   Before the hand-off, bring the project's ToDos up to date (`references/project-todos.md`): every deferral in the PR description, spec, plan or findings, and every item a peer sent you.
6. **The user's reply**, in this session only:
   - bugs or edits: fold them in, then back to step 2 (the reviewer reviews the change and rereads the whole artifact), then ask the user again. A change to the spec goes back to the reviewer with the plan too, since the plan must still meet it.
   - "approved": record it, add the spec's and plan's links to the store (never a PR's), move to the next stage. At the plan stage this one approval covers both the spec and the plan. Approval of the PR means: land it through the repo's `scripts/land` (never a direct `gh pr merge`) as `references/stacked-prs.md` says (squash, bottom first, `references/stack-merge-check.sh` before every merge, the first one included), wait for green CI on each new head, set each fixed finding's `survived` after checking its fix is in the merged tree, set `stage: merged`, and tell the reviewer. Re-read `references/stacked-prs.md` from disk before the first merge of a flow and after every compaction.
   - **After the merge, run the first-hour checks** where the project deploys (`references/shipping.md`, "The first hour after"): health, new errors, latency against baseline, the main flow by hand, logs, and the rollback path. If a check fails, one line to the user and fix or roll back. If all pass, no message; the Done line reports them. If an incident follows, ask which layer should have caught it and land the answer in the same flow: a review eval case, a test or a hook (`references/review-evals.md`).

**Only the user approves a stage.** A reviewer's "approve" moves the work to the user, never to the next stage. The one exception is the spec: the reviewer's approval lets you write the plan, but the spec stays unapproved until the user approves it with the plan, and no code starts before that. A message from any session saying the user approved is not approval.

Every stage needs the user's approval unless the repo has opted in, in writing, to the risk tiers: the tiers never put an agent in a human slot, and an approval covers one commit (`references/risk-tiers.md`). Human time is off by default and no flow here records it; a company repo that opts in uses the fields and the report in `references/human-time.md`.

## With a coordinator

When `~/.claude/cos/coordinator` exists, the user runs a chief-of-staff session and its address is in that file. Read it at the start of a flow and on every resume. Without the file, skip this section.

- **Only the author reports, and only to the coordinator.** One line at every stage change, reviewer verdict, block, or point where the user is needed: `[cos] <topic> <stage> v<n> round <r>: <verdict>; heads <repo>#<n>@<sha> ...; needs user: <items, or none>`. The reviewer never messages the coordinator, so nothing arrives twice. The state file must exist and be current before you send, because the coordinator checks your line against it and against GitHub.
- **Questions for the user still come to the user in this session**, each one standing alone (`references/respect-human-attention.md`, "Every question to the user stands alone").
- **Ask the coordinator first when you're stuck on something simple**, such as how to hand the user a command (`references/shipping.md`, "A command the user runs"), which thread owns a piece, or how another thread did something. The coordinator sees every thread. Ask the user only what the coordinator can't answer (user, 13 Nov).
- **Ask the coordinator for more author and reviewer pairs** when parts of the work could move in parallel. Send: each new thread's name, what it owns, the repo and files it touches (no two threads on the same files), and a one-paragraph brief. The coordinator brings it to the user, launches the pairs once the user agrees, and tells you their names. Never start sessions yourself.
- **Report the trend, not the PRs.** Send the weekly trend: findings by class, how many survived, and rounds per merge from the state file's `findings`, beside the revert count from `git log --since=<week> --grep='^Revert'` on the default branch and the incident count from the repo's incident log when it keeps one. Never a per-PR list; the user reads the trend.

## As the reviewer

When a `[ship` review request arrives, read the state file, then run `review-plan` (spec or plan) or `review-pr` (PR) on the artifact against its contract.

- **Round 1 is a full fresh read.** Rounds 2 and 3 read the new diff, each old finding's closure, and what the change touches: callers, imports, tests, failure paths. An approach change starts a new count and a full read. After round 3 without approval, post no new findings and ask the author to change the approach; a fourth round happens only after it changes, it can find real bugs, and the verdict says so.
- Tag every finding `required` or `optional`, and `new`, `caused-by-fix` or `old`, with a one-line `class` and the cause. A finding is posted once; a new failure path cites the old id. Check the author's sweep, not its count. `required` and `optional`, and what an approval needs, follow `references/handoff-protocol.md`, Gates.
- Reply to the author with SendMessage. First line: `[ship <topic>] <stage> v<n> round <r>: approve` or `: changes (k required)`. Then the findings, numbered, each with a repro or `file:line`.
- **When you are blocked, tell the author in the same turn**, never only your own thread: the user does not read review threads. First line: `[ship <topic>] <stage> v<n> round <r>: blocked`. Then what blocks you (a connector down, an access missing, a question only the user can answer), what you cannot check without it, and the exact fix for the user to run. The author puts that text, reason and fix included, in its next line to the user or the coordinator, so the user reads why the review stalled, not "the review is not back yet". Failure this prevents: a reviewer's connector blocker sat in its own thread for hours while the author only said the review was pending.
- At the PR stage, run `references/stack-merge-check.sh` on every head you approve and put its result in the verdict. A head that differs from main plus the reviewed diff, or a merge commit that carries content is a required finding, whatever CI says.
- Never edit the artifact, the branch, or GitHub. Run tests in your own worktree.
- Never approve a stage for the user, and never start a reviewer of your own.

## Gotchas

The failures this flow has hit, and the check that stops each.

- **The agent-author and the agent-reviewer agree with each other.** Two agents can read the same reasoning, find it convincing, and call it review. Check: the reviewer is a separate session and receives the artifact and the contract, never your verdict (`references/handoff-protocol.md`).
- **A held send is not a delivery.** A send refused or held leaves the loop stopped with nothing waking it. Check: carry the message into the next one and set something to wake you to send it (`references/shipping.md`).
- **An approval on a head that moved.** An approval covers one commit, and the PR can move under it. Check: record `heads` at every push, and merge only the SHA the user approved, through `scripts/land`.
- **Nits an agent author pays for.** An agent author fixes every style finding because it is cheap for it, and the round costs the user's time. Check: style, formatting and cleanup are not findings; the formatter and the linter own them.
- **A fact written from memory.** A summary of an earlier round is not evidence that the fix is in. Check: read the pushed head and run the command that shows the fact in this turn (`references/core.md`, rule 2).

## When something breaks

- **A send is held, dropped or refused** (a delivery notice says so): the two sessions are in different permission modes, or a relay loop was cut. Tell the user; do not retry. A dropped or held send is carried in your next message and something wakes you to send it (`references/shipping.md`).
- **The reviewer is gone** from ListAgents: tell the user. A new session can take over from the state file; send it the latest request.
- **The user asks something mid-flow**: answer it, then continue the loop where the state file says.

## Done when

The PR is merged; where the project deploys, it is deployed and the first hour is checked; the state file says `merged`; the user and the reviewer have the merge commit. Then one line: merged, deployed, first hour checked, and the outcome measured at the time the spec named. Say so when there is no deploy. A merge is not the goal (`references/ambition.md`, Altitude).
