# Risk tiers

The default is strict: the user approves every stage of every change. This reference adds a door a repo may open in writing. It changes no default, and no flow here starts faster because of it.

## The tiers

The change sets the tier, never the author. The reviewer derives it from the changed paths and says which tier applied.

| Tier | What it covers |
|---|---|
| low | docs, copy, and an addition behind a flag |
| medium | an ordinary change |
| high | auth, billing, CI workflows, installers, migrations, and the paths the repo names as highest risk |

A change that touches two tiers takes the higher one. A refactor that moves a high-risk path is high, whatever its diff looks like. A label the author chose, or a small diff, never lowers a tier.

## What a repo opts in to

A repo that opts in names its tiers and who may approve a low-tier change in its own docs, with one line in `REVIEW.md` pointing at them. Without that pointer, strict applies.

| Tier | Human approvals |
|---|---|
| high | every stage, plus the rollback and watch window before merge |
| medium | the plan (with the spec) and the PR |
| low | the PR alone |

An agent never fills a human slot. A reviewer's approval moves work toward the person; it is not an approval. An approval covers one commit: a push after it voids it, and the approval is taken again on the new head.

## Low unlocks only on evidence

Low is available only when both hold:

1. An incidents eval set exists (`references/review-evals.md`).
2. The merged-PR history for the window the repo names shows the reviewer's miss rate and the revert rate flat.

Until both hold, a low change is medium. The evidence is re-read at each quarter or release, whichever the repo uses; a rise in either rate puts low back to medium until the next reading.

## Why the order is this way

The tiers move approvals away from a person only where the reading is cheapest. A docs change has little to get wrong, and an incidents set plus a flat miss rate is what shows the reviewer catches what is left. High never lowers: an auth or migration change gets more human eyes, not fewer.
