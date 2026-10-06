# Handoff protocol

Who proposes, and who judges. The pipeline skills reference this.

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

## Gates

- **Implementation does not start until the plan review approves it.** Not "mostly fine". Approved.
- Review rounds are bounded. Up to five passes of back and forth, then a human decides. If five rounds have not converged, the disagreement is about the requirements, not the plan.
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

After three rounds where the same implementer fails to close a finding, hand the task to a fresh session on a stronger model, with the findings and what was tried. The five-round bound still holds.

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

## Why bounded

Unbounded review finds infinite issues, because any plan can be criticised forever. Five rounds is enough to catch what matters and short enough to finish.

## Several agents, one branch

- **Claiming the branch before a push-bound run**, and the other rules for sharing one main branch: `references/shipping.md`, "Several sessions, one main branch".
- **One ledger of instructions, in a file every agent reads**, so nothing the human said lives only in one agent's context.

## Re-review rounds

When the same work is reviewed again after fixes, the reader needs to see what the fixes did, not a fresh list that looks like churn. Applied by review-pr and review-plan.

- **Tag every finding by origin:** **new** (added since the last round), **caused by a fix** (a fix from the last round introduced it), or **old** (already there last round).
- **Hold severities steady.** An old finding moves up a level only when the reviewer shows a new, concrete failure path. A fresh reviewer rating it higher is not enough.
- **Make the trend honest.** If the count of serious findings rises, say in one line whether that came from new work, from fixes, or from old work seen differently.
- **Brief helpers the same way.** Give reviewer sub-agents last round's severities and tell them to keep those levels unless they can show a new failure path.

