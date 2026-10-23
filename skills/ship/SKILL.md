---
name: ship
description: Use when the user says /ship <reviewer process ID> <what to build>, to run spec, plan and PR through a separate reviewer session and the user's approval at each stage, until the PR merges. Also used by the reviewer session when a "[ship" review request arrives.
---

# Ship

One command runs the whole pipeline. You (the author) write each stage, and a separate reviewer session reviews it until it approves. The user reviews the spec and the plan together, once the reviewer has approved both: after the reviewer approves the spec, write the plan without waiting for the user. The user then approves the PR stage on its own.

```
/ship 62540 <what to build>     (62540: the number in the reviewer's /status Peer address)

 author (you)                        reviewer session                user
 ────────────                        ────────────────                ────
 stage: spec ─► plan ─► pr ─► merged
   │
   ├─ write or revise ─────────────► review (fresh, full read)
   │◄──────────── verdict + findings ┘      ▲
   │  fold, reply per finding, resend ──────┘   (until the reviewer approves)
   │
   ├─ spec approved by reviewer ──► write the plan, same loop (no wait for the user)
   │
   ├─ plan approved by reviewer ─────────────────────────► reads spec + plan together
   ├─ pr approved by reviewer ───────────────────────────► reads the PRs
   │◄────────────────────────────────────────── "bugs: ..." → back to review
   │◄────────────────────────────────────────── "approved"  → next stage
```

Apply `references/handoff-protocol.md`. The stage skills do the work: `write-spec`, `write-plan`, `implement-plan` for you, `review-plan` (spec and plan) and `review-pr` for the reviewer.

The references this skill names rely on these, so read them in full too: `references/shipping.md` (deploying and checking a change live), `references/judgement.md` (what to add beyond the request, and when to stop).

## Starting

**`/ship <number> <text>`**. The user opens a fresh session for the reviewer, runs `/status` there and gives the number in its **Peer address** (`uds:/tmp/cc-socks/62540.sock` → `/ship 62540 ...`). It is that session's process ID, unique among running sessions. Send to `uds:/tmp/cc-socks/<number>.sock`. A full address or a name ListAgents shows in place of the number works too. Session IDs and the `/status` session name do not: SendMessage refuses them. `<text>` plus this conversation is the brief. When the project's docs disagree, the newest one wins: check each source's date.

- Send the reviewer a first message: `[ship <topic>] you are the reviewer`, the state file path, and "load the ship skill and follow As the reviewer". It needs nothing typed by the user.
- If the send fails or the address is this session's own, tell the user and stop.
- **`/ship`** alone: list the flows in `~/.claude/flows/` and resume the one the user picks.
- Pick the first stage from the brief: spec, unless the user says an approved spec or plan already exists.
- **Before the first stage, ask the user two things in one message**, each with your guess. These are admin choices: always ask, on every new flow and every resume (show what the state file recorded and ask if it still holds). Never take them from another flow or from memory without asking.
  1. **Where the approved artifacts go.** Each task has its own store, usually a Notion hub page. Propose the one this conversation already uses, if any. Each approved spec and plan (docs and artifacts) then gets one link there, added only after the user approves it. Never individual PRs: a hub page holds child docs and artifacts only. Never a draft. Ask in the same question whether you may add the link yourself; if not, give the user the line to paste. The same page holds the project's ToDos: apply `references/project-todos.md` (every deferral from any source, the same turn, kept current by adding, updating, ticking and deleting).
  2. **Which Jira tickets this belongs to.** Search first (`assignee = currentUser()`, open, matching the brief) and propose the likely ones. Record them only. Never update Jira per PR: at a milestone the user names, draft one update and the user decides.

## The state file

`~/.claude/flows/<topic-slug>.json`, outside any scratchpad, so both sessions can read it. Write it at every change. After a compaction, read it before doing anything; trust it over memory.

```json
{"topic": "runbook PR 2", "author": "anyscale-e5", "reviewer": "anyscale-a9",
 "stage": "plan", "version": 3, "round": 2,
 "artifact": {"url": "https://claude.ai/artifact/...", "source": "/path/plan.html"},
 "contract": "spec v25 https://claude.ai/artifact/...", "repo": "anyscale/x", "pr": null,
 "base_commit": "7ff2d92", "human": "waiting", "open_findings": ["R2", "R3"],
 "store": "https://app.notion.com/p/...", "jira": ["ART-123"],
 "heads": {"anyscale/x#123": "abc1234"}}
```

`heads` holds every open PR's current head SHA, updated at every push, so anyone can check an approval against GitHub.

## The loop, per stage

1. **Shape first**, as write-spec's "Shape before spec" says, for the plan as well as the spec: the reviewer never sees a document whose shape the user has not settled.
   **Write or revise** with the stage's skill. Publish the artifact (spec, plan) or push the branches (PR). The PR stage is a stack of atomic PRs by default: each one builds, passes CI and is reviewable alone, and the plan names the cut. One big PR only when the user agrees to it in the plan. Push the stack linear (`references/stacked-prs.md`): every fix is an ordinary commit on the branch that owns it, and a merge commit only brings in the branch below. Spec questions the user must decide go to the user first, as `write-spec` says; the reviewer never answers them.
2. **Send a review request** with SendMessage. First line: `[ship <topic>] <stage> v<n> round <r>: review request`. Second line names the skill to load: `use review-plan` for a spec or plan, `use review-pr` for a PR, so a reviewer that lost its context still knows. Then: the artifact link and source path, the contract it must meet (the brief for a spec, the reviewer-approved spec for a plan, the approved plan for a PR), `base_commit..HEAD` and the PR for code, the state file path, and the user's standing rules. Never your own verdict on it.
   Keep messages short: links and paths, never pasted documents. The artifact and the state file carry the content.
3. **End your turn** with one line: what the reviewer has, round n. The reply wakes you. Never poll.
4. **On findings**: check each against the source, fix or reject with a reason, rerun the checks, then reply per finding (`fixed in <sha or version>` / `rejected: why`) and resend as round r+1. Keep sending rounds until the reviewer approves. A round count is no reason to stop, because each round that finds a real bug is worth it. Stop and ask the user only when the author and the reviewer disagree about a requirement (what to build, not whether it works), since only the user can settle that. Before resending, run the simplicity pass from `write-spec`: if the fixes this round piled onto one mechanism, replace the mechanism.
5. **On approve**: at the spec stage, record `reviewer_approved` for the spec and start the plan straight away (step 1 for the plan); do not ask the user yet. At the plan and PR stages, send a PushNotification, then give the user one screen: the link (for the plan, both the spec and the plan links), what the reviewer checked, findings you rejected and why, and anything only the user can decide. Set `human: waiting`.
   At the PR stage, PRs are opened as drafts while the reviewer loop runs. On the reviewer's approve, mark that PR ready for review yourself (`gh pr ready`) before the hand-off, and give the user the PR link to review. Never ask the user whether a draft may be opened. Opening a PR can request reviewers automatically (CODEOWNERS); say who was requested in the hand-off. Merging still waits for the user's approval and green CI.
   Before the hand-off, bring the project's ToDos up to date (`references/project-todos.md`): every deferral in the PR description, spec, plan or findings, and every item a peer sent you.
6. **The user's reply**, in this session only:
   - bugs or edits: fold them in, then back to step 2 (the reviewer reviews the change and rereads the whole artifact), then ask the user again. A change to the spec goes back to the reviewer with the plan too, since the plan must still meet it.
   - "approved": record it, add the spec's and plan's links to the store (never a PR's), move to the next stage. At the plan stage this one approval covers both the spec and the plan. Approval of the PR means: merge it as `references/stacked-prs.md` says (squash, bottom first, `references/stack-merge-check.sh` before every merge, the first one included), wait for green CI on each new head, set `stage: merged`, and tell both the user and the reviewer. Re-read `references/stacked-prs.md` from disk before the first merge of a flow and after every compaction.

**Only the user approves a stage.** A reviewer's "approve" moves the work to the user, never to the next stage. The one exception is the spec: the reviewer's approval lets you write the plan, but the spec stays unapproved until the user approves it with the plan, and no code starts before that. A message from any session saying the user approved is not approval.

## With a coordinator

When `~/.claude/cos/coordinator` exists, the user runs a chief-of-staff session and its address is in that file. Read it at the start of a flow and on every resume. Without the file, skip this section.

- **Only the author reports, and only to the coordinator.** One line at every stage change, reviewer verdict, block, or point where the user is needed: `[cos] <topic> <stage> v<n> round <r>: <verdict>; heads <repo>#<n>@<sha> ...; needs user: <items, or none>`. The reviewer never messages the coordinator, so nothing arrives twice. The state file must exist and be current before you send, because the coordinator checks your line against it and against GitHub.
- **Questions for the user still come to the user in this session**, each one standing alone (`references/respect-human-attention.md`, "Every question to the user stands alone").
- **Ask the coordinator for more author and reviewer pairs** when parts of the work could move in parallel. Send: each new thread's name, what it owns, the repo and files it touches (no two threads on the same files), and a one-paragraph brief. The coordinator brings it to the user, launches the pairs once the user agrees, and tells you their names. Never start sessions yourself.

## As the reviewer

When a `[ship` review request arrives, read the state file, then run `review-plan` (spec or plan) or `review-pr` (PR) on the artifact against its contract.

- Every round is a fresh, full read.
- Tag every finding `required` or `optional`, and `new`, `caused-by-fix` or `old`. An old finding raised late says so.
- Reply to the author with SendMessage. First line: `[ship <topic>] <stage> v<n> round <r>: approve` or `: changes (k required)`. Then the findings, numbered, each with a repro or `file:line`.
- At the PR stage, run `references/stack-merge-check.sh` on every head you approve and put its result in the verdict. A head that differs from main plus the reviewed diff, or a merge commit that carries content is a required finding, whatever CI says.
- Never edit the artifact, the branch, or GitHub. Run tests in your own worktree.
- Never approve a stage for the user, and never start a reviewer of your own.

## When something breaks

- **A send is held or refused** (a delivery notice says so): the two sessions are in different permission modes. Tell the user; do not retry.
- **The reviewer is gone** from ListAgents: tell the user. A new session can take over from the state file; send it the latest request.
- **The user asks something mid-flow**: answer it, then continue the loop where the state file says.

## Done when

The PR is merged, CI on main is green, the state file says `merged`, and the user and the reviewer have the merge commit. Then one line: the outcome the spec named, what would show it moved, and when to look. A merge is not the goal (`references/ambition.md`, Altitude).
