# Handoff protocol

Who proposes, and who judges.

## Contents

- The rule
- What separation means
- The hand-off leads with its artifact
- Gates
- What the reviewer receives
- Sorting the findings
- Ending a session
- Several agents, one branch
- Re-review rounds

## The rule

**The agent that produced the work does not review the work.**

An agent reviewing its own plan re-reads its own reasoning and finds it convincing, because it is the reasoning it just chose. The bias is structural, not a matter of effort or prompting.

Never call work independently verified when the agent that produced it is the one that checked it.

## What separation means

| Step | Runs where |
|---|---|
| Write the spec | any model |
| Write the plan | any model |
| **Review the plan** | **fresh session, different model family, or a stronger model in the same family** |
| Implement | any model, after the review approves |
| **Review the code** | **fresh session, and not the one that wrote the code** |

A fresh session is the minimum. A different model family is better, because two models from one family share failure modes.

## The hand-off leads with its artifact

A PR or a hand-off opens with its artifact. The artifact is the smallest thing that lets the reader judge the change, and the reader sees it before any summary.

| The change | The artifact it opens with |
|---|---|
| **Structural:** what calls what, what moves, how the pieces fit | A diagram of the shape of the change: ASCII or mermaid, or a diff of the shape the reader already knows, with `+` and `-` lines |
| **UI:** what a user sees and does | A screen recording of the changed flow, made as `references/visuals.md`, "Recordings", says |
| **Product:** a behaviour a spec names | The spec link |

After the artifact comes the caption, in this order: what the change does and why, the risk, how to revert, and what to watch and when. Text is the caption, never a substitute for the artifact.

**Text is not banned.** Decisions, risks, exact commands, numbers and legal or finance claims stay in text, because a diagram cannot be diffed or audited. A change with no visual or structural shape stays text.

The reviewer receives the artifact and the contract it must meet. The state file records each artifact's link and source path, so the author, the reviewer and the user open the same thing.

## Gates

- **Implementation does not start until the plan review approves it.** Not "mostly fine". Approved.
- Rounds continue while each round finds a real defect, three per approach; after that the approach changes or the flow stops ("Three rounds, then the approach"). When author and reviewer disagree about a requirement, a human decides.
- **A finding is required only when it shows a failure against the contract or correctness,** with a repro or `file:line`. Anything else is optional: it goes to the user in the hand-off and never starts another round. A reviewer asked to find gaps will report some even when the work is sound, and chasing every one leads to over-engineering.
- **A PR reaches the user with no open comment threads, from anyone.** A person, a review bot, a linter or scanner bot, or another agent: every comment on the PR is the author's to answer before the hand-off, not the user's to find. For each one, fix it or decide not to, reply in its thread (`fixed in <sha>` or `not changing: why`), then resolve the thread. Check it on the exact head you hand over, with a command, and name it in the hand-off, for example `gh api graphql -f query='{repository(owner:"o",name:"r"){pullRequest(number:N){reviewThreads(first:100){nodes{isResolved}}}}}'` returning no `false`, plus no unanswered top-level review or issue comment. A comment that arrives after the hand-off reopens the loop: handle it, then hand off again. Findings you declined still go in the hand-off with their reason, so the user can overrule them. Failure this prevents: the user opened PR links marked ready, found pending comments, and sent the thread back for another round of fixes, tests and review; the user said "it's better if the threads only own this stuff" (9 Nov).
- **The Artemis review bot is optional, not a gate.** Don't wait for it to run or to re-review. The gate is the author, the reviewer and the user being satisfied. When the bot has already commented, fix what's real while you're there, then reply and resolve. A bot thread that's still open doesn't hold the hand-off; list it in the hand-off with one line on it. People's comments, scanners such as Semgrep, and CI still have to be clear (user, 13 Nov: "it's replies are good to have but author, reviewer and me being happy are enough").
- **A PR reaches the user with a description that matches its exact head.** Before the hand-off, reread the title and the whole description against the final diff, and fix anything stale: a decision reversed in review, a step, file, number, commit or base that changed, a rollout order, a "TODO" or "WIP" that no longer holds, a claim about a test or a live check. It carries **How to revert** and **What to watch, and when**, or points at the rollback plan in `references/shipping.md`. Say in the hand-off that you did. Failure this prevents: the user read descriptions that still said what earlier rounds did and had to ask the thread to correct them (user, 13 Nov: "make sure that the description is up to date and there is no stale information"). Example: #1839's rollout still told the reader to edit an SSM map that the gateway never reads.
- **Approve only on evidence about the exact head:** green CI on it, and for code that reads or writes real data, one real run or a real sample, never stubs alone.
- A human reads the plan before implementation begins. The agents check each other; they do not replace the person who knows what is wanted.

## What the reviewer receives

- **A written brief, never your session history:** what was asked, the spec or plan path, the commit range, and the project wide constraints.
- **The artifact and the contract it must meet. Never the author's conclusion.** Handing over "this is thread-safe" gets back agreement with "this is thread-safe".
- Record the starting commit before the work begins and review `start..HEAD`. `HEAD~1` silently drops every commit but the last.
- The reviewer lists what it sees in its own words before reading any summary the author wrote. A deterministic tool's output (linter, detector, scanner) reaches it after its own judgement is written, not before.
- **Never pre-judge.** A brief that says "do not flag", "at most minor" or "the plan chose this" is sparing you a review round.
- **The author's account of a fix is not evidence.** The reviewer checks the fix in the artifact itself.
- Neither the implementer nor the reviewer spawns its own reviewer. Name the model explicitly when you dispatch; an omitted model inherits the session's, which may be the wrong tier.

## Sorting the findings

Sort each finding, first match wins: the contract was unclear (fix the contract), real and must change, real but accepted as a trade-off (write it down), or noise from missing context (ask what context would have prevented it). Zero actionable findings across two rounds that each raised real issues means the author is validating, not reviewing. Stop and ask the human.

After three rounds without approval, the reviewer stops posting findings and asks for the approach to change; a fresh session on a stronger model, with the findings and what was tried, is one way to change it.

## Ending a session

Decide at the end of a phase, never in the middle of one. Take the first that fits:

| Question | If yes |
|---|---|
| Does the next phase need this session's reasoning word for word, and is there room left? | Continue |
| Is everything here disposable? | Clear |
| Is the work moving to another harness, repo or person, or splitting off a side task? | Write a handoff file |
| Can the next task run with nobody watching? | Send it to a sub-agent |
| Otherwise | Compact, saying what the next phase needs |

A handoff file goes in the OS temp directory, not the repo. It points at the spec, plan, commits and issues by path rather than restating them, names the skills the next session should load, and holds no secrets.

## Several agents, one branch

- **Claiming the branch before a push-bound run**, and the other rules for sharing one main branch: `references/shipping.md`, "Several sessions, one main branch".
- **One ledger of instructions, in a file every agent reads**, so nothing the human said lives only in one agent's context.

## Re-review rounds

When the same work is reviewed again after fixes, the reader needs to see what the fixes did, not a fresh list that looks like churn. Applied by ship, review-pr and review-plan.

### Three rounds, then the approach

A stage gets three rounds per approach; an approach change starts a new count and a full read.

- **Round 1 is a full fresh read.** List everything you can find.
- **Rounds 2 and 3 read three things:** the new diff, each old finding's closure, and what the change touches: callers, imports, tests and failure paths.
- **After round 3 without approval, post no new findings.** Ask the author to reconsider the approach, and name the evidence that the approach, not the line, keeps failing. Stop. A fourth round happens only after the approach changes, and its verdict says what changed; a genuine new bug in the new approach is a finding like any other. A different design, a fresh session or a stronger model is an approach change; another reading of the same approach is not.
- **The state file's `round` is a gate, not a note.** The author does not send round 4 until the state file records `approach_changed` with what changed, and the reviewer refuses a round 4 request without it.

### Every finding

- **Tag every finding by origin:** **new** (added since the last round), **caused by a fix** (a fix from the last round introduced it), or **old** (already there last round).
- **Give every finding a one-line `class` and its cause.** The class is the kind of failure in two or three words (`error-path`, `input-validation`, `stale-copy`); the cause is why it happened. The author fixes every instance of the class, not only the quoted line, and replies `fixed in <sha>; swept N other places, found M`. The reviewer checks the sweep, not the count.
- **A finding is posted once.** A new failure path is a new finding that cites the old id. A re-post is a reviewer defect.
- **The same class in two rounds or two PRs lands the source fix in the same flow:** a lint rule, a test, a `REVIEW.md` or doc line in the repo, or the library when the class crosses repos. A third occurrence is the reviewer's failure, not the author's.
- **Hold severities steady.** An old finding moves up a level only when the reviewer shows a new, concrete failure path. A fresh reviewer rating it higher is not enough.
- **Make the trend honest.** If the count of serious findings rises, say in one line whether that came from new work, from fixes, or from old work seen differently.
- **Brief helpers the same way.** Give reviewer sub-agents last round's severities and tell them to keep those levels unless they can show a new failure path.

### Replying to a finding

- Start every reply with one of four words and the reason: `fixed` (with the sweep), `wrong` (the line or contract that shows it), `intentional` (the contract or a written trade-off says so), or `not-material` (no user-visible failure, with the impact).
- Record every finding in the state file: id, severity, origin, class, round, outcome, and `survived`. `outcome` is null until a reply, then the reply word; `survived` is true when the fix was still there at the merge. The coordinator reports the weekly trend from these fields, never a per-PR count.
- **Style, formatting and cleanup never block and are not posted as findings.** The formatter and the linter own them; a finding is a failure of behaviour or the contract.

