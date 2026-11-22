# Review evals

A reviewer that finds nothing looks the same every week. A set of frozen bugs, replayed on the reviewer, is what tells a good review from a quiet one, and it turns every incident into a case the next review must catch.

**Real bugs first, rounds second.** The measure is the defects caught, not the round count; a reviewer that catches the real bug in round 1 beats one that needs three.

## The set

`review-evals/incidents/`: 5 to 10 cases at a time, each a bug this repo shipped or nearly shipped. Fewer does not separate a reviewer from luck; more is expensive to replay and goes stale.

- **A frozen patch, never a branch.** A branch moves; the patch is the exact change the reviewer will see.
- **One line on the bug**, the `file:line` where it lived, and who confirmed it. A candidate is not a case until a person has seen the failure on a real run or a real sample.
- **A base commit.** A patch that no longer applies is stale: drop the case or refreeze it, never edit the patch to fit.

Each case is a folder:

    review-evals/incidents/<case>/
      case.md     # base, bug, where, confirmed by
      patch.diff  # the frozen change, applied at base

    base: <sha>
    bug: <one line>
    where: <file>:<line>
    confirmed by: <name or session id>

`review-evals/clean/` is the same shape with sound changes. It measures noise: a reviewer that posts a finding on a clean patch is failing. Use it only when the reviewer changes (`review-pr`, "Review evals") or the repo opts in.

## The run

Hand the reviewer only the patch, the contract and the repo. Never the labeled bug, the case folder or the results file.

1. Stage a throwaway worktree at the case's base commit and apply its patch. Remove `review-evals/` from that worktree, so the label is not in the material the reviewer can read.
2. Start the repo's reviewer the way the repo starts it: a fresh session with `review-pr`, the configured review bot, or the vendor's runner. Give it the repo, the contract and the change (`git diff` at the worktree head), nothing else.
3. Record one line per case: `caught` (the first-round report names the failure at the labeled line, or an equivalent concrete failure), `missed` (it does not), or `noise` (a clean case that drew a finding a person judges wrong). Keep the reviewer's finding ids beside the verdict.
4. Report `caught x of n` and `noise y of m`. A rising miss rate or a rising noise rate is a regression, whatever the round count did.

The staging commands, for a Claude Code session:

    git -C <repo> worktree add --detach <tmp>/<case> <base>
    git -C <tmp>/<case> apply <repo>/review-evals/incidents/<case>/patch.diff
    rm -rf <tmp>/<case>/review-evals

No runner script ships with this reference. A script can stage the worktree and apply the patch in three lines; it cannot make the caught, missed or noise call, and a wrapper that also started the reviewer would own the prompt, which is half of what the eval measures. The commands are the runner, and a person reads the report.

**When to run it:** whenever the reviewer's prompt, tools or model change, and at company scale weekly is enough. Run the same set before and after the change; a difference inside the noise of a handful of cases is not a result.

## What an incident adds

An incident review asks which layer should have caught the failure. The answer is a case here when a review should have caught it, a test when the suite should have, and a hook when a person or an agent should have been stopped before acting. One incident lands one of the three in the same flow, as the handoff protocol's "Every finding" says.
