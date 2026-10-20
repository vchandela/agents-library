# Evals reference

The detail behind the evals skill: what one item holds, how to keep a model judge honest, and the arithmetic for comparing two versions.

## One item

Every eval item carries the same fields, whatever the agent. A support ticket, a pull request and an alert differ only in what goes in them.

```yaml
id: ticket-1042                      # stable, never reused
input: <the first message, as it read at T>
t: 2026-09-21T10:22:00Z              # the moment the item is frozen at
answer_key:
  value: "head node ran out of memory"
  source: confirmed cause at ticket close   # from the world, never a model
  confirmed_by: engineer, head memory chart
frozen:
  tool_results: [s3://.../call-1.json, ...] # what the agent saw at T
  context: {prompt: <commit>, runbook_page: <commit>}
  not_recordable: [cluster state]            # what can't be rebuilt, said out loud
source: customer-a                   # for clustering and per-source splits
flags: {seed_of: [page-x], negative: false, hard: true}
split: holdout                       # train | selection | holdout, by date when the world moves
```

The same shape for other agents: a code review item is a merged PR, its answer key is the line a later fix changed (walk back from the fix with `git blame`), and it freezes the diff and the repo at merge time. An alert item is the alert, the confirmed cause from the incident record, and the metric and log results at T.

## Grader hygiene

- The judge is a different model from the one under test, at temperature 0 with a fixed seed where the API allows. Both model versions are pinned and recorded.
- One judge per failure mode, one yes/no question each, with an "unknown" answer that maps to unscored.
- The graded output goes inside clear delimiters, and any delimiter inside it is neutralised, so the output can't instruct the judge.
- Parse the judge's last verdict line, not the first match.
- A judge call that errors, times out or returns no verdict is unscored, never a pass.
- In a side-by-side comparison, randomise which output comes first, and grade each pair in both orders when the result is close.
- A panel of several judges with a majority vote is worth it only when one judge's rates miss the bar; log every vote.

## Checking a judge

Treat the judge as a classifier against human labels.

1. Label items by hand, 30 to 50 to start. At least 10 of each verdict in the dev set to start; about 50 of each per failure mode before the judge gates anything.
2. Split train, dev and test. Iterate the judge prompt on train and dev. Run test once, and report from test only.
3. Report two rates, each with a Wilson interval:
   - **catches failures**: of the items people marked fail, the share the judge marks fail
   - **passes good answers**: of the items people marked pass, the share the judge marks pass
4. Gate at 0.8 on both. Below that the judge is advisory.
5. **Correcting a pass rate for a known judge.** On a uniform random sample, if the judge reports a pass rate `p`, with `a` = passes good answers and `b` = catches failures, the corrected rate is `(p + b - 1) / (a + b - 1)`. This is the Rogan-Gladen estimator. It is only valid on a random sample, not on items chosen because they looked wrong, and it falls apart as `a + b` nears 1.

## Arithmetic for comparing versions

- **Interval on one rate**: use a Wilson interval, not the normal approximation, below a few hundred items. Example: 40 passes out of 50 gives about 67% to 89%.
- **Noise, roughly**: with n items near a 50% pass rate, a 95% band is about ±1/√n. 100 items, about ±10 points; 400 items, about ±5.
- **Paired comparison**: count `fixed` (fails in the old arm, passes in the new) and `broke` (the reverse). Ignore items where both agree. Test `fixed` against `broke` with an exact binomial test at 0.5 (McNemar). Example: 29 fixed and 11 broke is a real change; 23 and 17 is not.
- **How many items for a given change**, paired, 80% power, 5% significance, with about 20% of items flipping between versions: about 155 for a 10-point change, about 625 for 5 points, around 1,000 or more for 2 to 3 points. These are this library's own calculation, not a cited figure. The detectable change shrinks with the square root of the item count: four times the items halves it.
- **Clustered intervals**: when items share a source (a customer, a repo, a conversation), compute the interval over sources, not items. Anthropic found clustered errors can be more than three times the naive ones.
- **Reliability**: pass^k is the chance all k runs pass. At 90% per run, pass^3 is about 73% and pass^8 about 43%.
- **Duplicates**: items that share both a source and a root cause teach one lesson. Count them as one between them, so one source can't decide the score.

