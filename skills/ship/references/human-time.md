# Human time

How long a flow waits on a person, and whether the waiting bought anything. For company repos that opt in. Off by default: this library's own flows do not record it, and nothing changes for them.

## Why

A flow can look fast by asking the user less, or by approving on a thinner read. The wait alone does not say which. Pair every wait number with the outcome that would show the approval was worth it.

## The fields

A repo that opts in adds one record per human touchpoint to the state file:

```json
"human_time": [
  {"stage": "plan", "asked_at": "2026-11-22T10:00:00Z",
   "answered_at": "2026-11-22T10:42:00Z", "reply": "changes"}
]
```

- `stage`: the stage the question belonged to.
- `asked_at`: when the question reached the person.
- `answered_at`: when the answer arrived. Leave it empty while the wait is open; an unanswered wait is its own signal.
- `reply`: the kind of answer (`approved`, `changes`, `rejected`, `no-reply`), never its text.

The fields are optional. A flow without them reports nothing and is not compared with one that has them.

## The report

One report per stage, over a window the repo names, so a trend is visible:

| Column | What it says |
|---|---|
| Median and p95 wait | How long the stage waits on a person |
| Approvals per PR | How many times a person was asked |
| Review comments per PR | How much reading the PR drew |
| Rounds per merge | How much author and reviewer churn preceded the merge |
| Reverts and incidents | Whether the faster flow shipped worse code |

Report the flow numbers beside the two outcome numbers for the same window, never one without the other. A per-PR report is not the unit: one PR says nothing, and a person reading each one spends the time the report was meant to save.

## The guardrail

**A fall in wait with a rise in reverts is not a win.** Neither is fewer approvals with more incidents. When the flow numbers improve and the outcome numbers do not, the report says so in one line, and a person decides whether to keep the change. The flow exists to ship working code, not to move work off a person's desk.

No aggregation script ships with this reference: median and p95 over a handful of touchpoints are read by a person, and repos define a touchpoint differently, so one script would fix one definition and hide the rest.
