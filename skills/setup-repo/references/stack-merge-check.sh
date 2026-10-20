#!/bin/bash
# Gate before merging ANY PR whose branch a tool may rebase or rewrite (GitHub stacked PRs above all).
#
#   stack-merge-check.sh <repo-dir> <pr-head> <approved-prev-head> <approved-head> [main-ref] [<lower>..<upper> ...]
#
# <approved-prev-head>..<approved-head> is the diff that was reviewed for this PR. For the bottom PR
# use the merge base it was reviewed against, not today's main (main may have moved since).
#
# (1) The PR head's tree must equal <merge-base of main and pr-head> plus the reviewed diff, applied
#     with exact context. A restack, rebase or "update branch" that dropped a fix shows up here. Green CI does NOT show it: lost lines
#     usually have no test.
# (2) For each branch ABOVE the PR (given as <lower head>..<upper head>, one per upper PR), no merge
#     commit in that range may carry content (git show --remerge-diff shows no changed file).
#     GitHub's stack restack rebases those branches after this merge and drops merge-commit content.
#     A PR's own merge commits are harmless when it is squash-merged, so they are only listed when
#     (1) fails, as a hint to where the loss came from.
#
# Exit 0 only when (1) holds and no upper range carries merge-commit content. Any STOP: restore the
# content in an ordinary commit (or rebuild the branch linear), get it reviewed, then merge.
set -uo pipefail
repo=${1:?repo dir}; head=${2:?pr head}; prev=${3:?approved previous head}; appr=${4:?approved head}
main=${5:-origin/main}; shift 4; [ $# -gt 0 ] && shift
cd "$repo" || exit 2
git fetch -q origin || { echo "fetch failed: refusing to compare against a stale $main"; exit 2; }
fail=0

carrying() { # list merge commits in range $1 whose remerge-diff is not empty
  for m in $(git rev-list --merges "$1"); do
    n=$(git show --remerge-diff --format= --name-only "$m" 2>/dev/null | grep -c .)
    [ "$n" != 0 ] && echo "${m:0:8} carries $n file(s)"
  done
}

# Compare from the point the PR branched off main: a squash merge applies only diff(base, head), so
# commits that landed on main after that point are kept and must not count as a difference.
# Rebuild what the PR should be (base plus the reviewed diff, applied with exact context and no fuzz,
# in a throwaway index) and require the PR head's tree to equal it. A line lost anywhere makes the
# trees differ. Comparing diff text instead raised false alarms on "index" blob ids and on @@ line
# numbers whenever main had also edited the same file elsewhere.
base=$(git merge-base "$main" "$head")
tmp=$(mktemp -d "${TMPDIR:-/tmp}/stack-merge-check.XXXXXX"); trap 'rm -rf "$tmp"' EXIT
echo "(1) tree of ${head:0:8} vs merge-base ${base:0:8} plus the reviewed diff ${prev:0:8}..${appr:0:8}"
git diff --binary "$prev" "$appr" > "$tmp/reviewed.diff"
if ! GIT_INDEX_FILE="$tmp/index" git read-tree "$base" || ! GIT_INDEX_FILE="$tmp/index" git apply --cached "$tmp/reviewed.diff" 2> "$tmp/apply.err"; then
  echo "    the reviewed diff does not apply to the merge base:"; sed 's/^/      /' "$tmp/apply.err"
  fail=1
else
  want=$(GIT_INDEX_FILE="$tmp/index" git write-tree)
  got=$(git rev-parse "$head^{tree}")
  if [ "$want" = "$got" ]; then
    echo "    identical"
  else
    echo "    DIFFERENT. Files that differ from base plus the reviewed diff:"
    git diff --name-only "$want" "$got" | sed 's/^/      /'
    hint=$(carrying "$base..$head"); [ -n "$hint" ] && { echo "    merge commits in this PR that carry content (likely where it came from):"; echo "$hint" | sed 's/^/      /'; }
    fail=1
  fi
  # git apply finds a hunk by its context and may place it at a shifted offset. Where main also
  # changed a file the PR changes, a person reads that file's result: the list is usually empty.
  files=$(git diff --name-only "$prev" "$appr"); shared=
  [ -n "$files" ] && shared=$(git diff --name-only "$prev" "$base" -- $files)
  [ -n "$shared" ] && { echo "    read these: main also changed them since the reviewed base"; echo "$shared" | sed 's/^/      /'; }
fi

if [ $# -gt 0 ]; then
  echo "(2) branches above: merge commits that carry content (a restack would drop them)"
  for range in "$@"; do
    c=$(carrying "$range")
    if [ -n "$c" ]; then echo "    $range:"; echo "$c" | sed 's/^/      /'; fail=1; else echo "    $range: none"; fi
  done
fi

echo "result: $([ $fail = 0 ] && echo PASS || echo STOP)"
exit $fail
