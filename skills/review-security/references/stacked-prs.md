# Stacked PRs

## Pushing

- **Never a plain `--force`, and never amend or rewrite a pushed commit.** Fix with a new commit on the branch the fix belongs to.
- **The one allowed rewrite is a stack rebuilt onto a moved main.** Push each of your own branches with `git push --force-with-lease=<branch>:<sha you last checked> --force-if-includes`, so the push is refused if anyone else pushed since. Push only after every rebuilt commit adds and removes the same lines as the reviewed one.

## Keep every upper branch linear

- Each upper branch sits on the exact commits of the branch below, with no merge commits. When the lower branch gains commits, let the host move the stack (GitHub's stack rebase, or its retarget after the lower PR merges). Never merge the lower branch into the upper one by hand.
- **A merge commit carries nothing.** A fix or conflict resolution that exists only in a merge commit's tree is dropped when the host rebases the branch, and CI stays green because the lost lines usually have no test. Example: artemis outage-watch #1079 to #1093 went out as merge-commit tips, and every restack dropped fixes (6 files, then 3, then 2), each found only after the lower PR had merged.
- **A broken stack** (the host's rebase stopped on conflicts, or never ran): replay the upper PRs' commits onto main with `git cherry-pick`, resolving each conflict in the commit it belongs to, then push the same branches with the lease. The PRs keep their numbers and history. The reviewer reviews every conflict resolution before the merge. Example: artemis #1206 to #1215 were replayed onto main after #1222 conflicted with two of them.
- Give every review fix its own test where one can exist, so a lost line turns CI red.

## Merging

- **Before every merge, the first one included, run `references/stack-merge-check.sh <repo> <pr head> <approved previous head> <approved head>`.** It passes only when the head's tree equals the merge base with main plus the reviewed diff (applied with exact context), and no merge commit in range carries content (`git log --remerge-diff` shows no changed file). Any difference is a stop: restore the content in an ordinary commit, get the reviewer to approve it, then merge. Green CI does not show a lost line. Don't compare the new head with your own tree (it fails once main moves) or diff text (false alarms on `index` ids and `@@` numbers). Read the files it lists as changed by main too, because `git apply` places a hunk by its context.
- Before the first merge of a stack, `git rev-list --merges origin/main..<top>` must be empty or content-free; if not, rebuild with the replay remedy above before any merge.
- On GitHub, a PR inside a stack refuses `gh pr merge` and the plain merge API. Merge bottom first with `gh api -X PUT repos/<owner>/<repo>/pulls/<n>/merge-async -f merge_method=squash -f sha=<full head sha> -f commit_title="<PR title> (#<n>)"`. Without `commit_title`, a one-commit PR takes the commit subject, not the PR title. GitHub is meant to retarget the next PR and rebase the branches above.
- **Don't count on GitHub's restack.** On artemis on 2026-10-10 it never ran after a squash merge, from the PR page or `merge-async`: the PR above kept its old base and the stack still counted the merged PR. The admin override (`-F bypass_rules=true`) works only on the bottom-most unmerged PR. What worked: dissolve the stack (`POST repos/<o>/<r>/stacks/<n>/unstack`), then for each PR, bottom first, replay the remaining commits onto main, check their lines, push with the lease, point the PR at main (`gh pr edit <n> --base main`), wait for green CI, run the check, and merge with `merge-async`.
- After each merge, diff every rewritten branch against its reviewed tree (it should be empty) and wait for green CI on the new head before merging the next.
