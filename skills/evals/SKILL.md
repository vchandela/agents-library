---
name: evals
description: Use when you need to know whether an LLM agent, a prompt, a model swap, a judge or a skill is good, or whether a change made it better or worse, before trusting or shipping it. Covers building the test set, grading, checking the grader, comparing versions and gating changes. Not for ordinary code tests with exact outputs; that is the testing reference in implement-plan. Not for finding why one run failed; that is diagnose-bug.
---

# Evals

An eval is a measurement, so it can lie in all the ways a measurement can: the wrong sample, a broken ruler, an answer key that copies the thing it grades, a difference smaller than the noise. Every step below closes one of those.

Apply `references/evals.md` (item format, grader hygiene, judge checking, statistics), `references/engineering-principles.md`, `references/judgement.md`, `references/testing.md` and `references/untrusted-input.md`. Build the simplest eval that answers the question, with seams for the next one.

The references this skill names rely on these, so read them in full too: `references/respect-human-attention.md` (what a reader's time is worth), `references/machine-tells.md` (the last pass for machine-sounding text), `references/visuals.md` (charts, diagrams and the visuals checklist), `references/ambition.md` (the ambitious option next to the obvious one), `references/writing-voice.md` (plain, warm sentences).

## 0. Size it

Write three lines before anything else, and show them to the user:

- **What is under test**: a prompt change, an agent, a model swap, a judge, or a skill.
- **The question it answers**, as a decision: "ship the new page or not", "which model, at what cost".
- **The pass rule, written now**: the threshold or the comparison, and what result means "don't ship". A rule written after the results is a story, not a test.

Then pick the depth: a **smoke check** (10 to 20 real cases, one arm, read every output), a **comparison** (two arms on the same cases), or a **standing suite** (gated in CI, kept alive). Build only what the depth needs: a smoke check is steps 1 and 2 plus reading the outputs, with no judge and no statistics; a comparison adds steps 3 to 5; only a standing suite needs step 6. Start each piece in its simplest working form behind a seam (stored results before live fallback, a query before a dataset tool, a spreadsheet before an annotation app), and grow it only when a measured number says the simple form is failing.

## 1. Look at real data first

No grader, metric or synthetic case before a person has read real outputs.

- Pull 30 to 100 real traces, sampled at random plus the known failures. Read each one whole: the input, every tool call and result, the answer.
- **The human writes the notes; the agent organises them.** One line per failure, in the human's words. The agent may group notes into failure modes and search for more examples of a mode only after about five human notes on it. Agents left to label on their own paraphrase instead of analysing and cover a fraction of the data; they reuse labels well only against a fixed category list.
- Stop when new traces stop adding failure modes. The modes, with counts, are the eval's scope: each gets a check in step 3, or a stated reason it doesn't.
- Expect the criteria to move while you read ("criteria drift"). That is the point of reading first.

## 2. Build items with an honest answer key

One item is one input, its answer key, and everything frozen with it. The full format is in `references/evals.md`.

- **The answer key comes from the world, never from a model's output**: a confirmed root cause at ticket close, the commit that fixed the bug, a database state, a policy document. An answer key a model wrote grades the model against itself.
- **Freeze the item as it was at time T**: the input as first seen, with everything written after T stripped (later replies, the fix, the close reason); the tool results the agent saw; the version of every context file (prompt, runbook page, repo commit). What can't be rebuilt is recorded as such.
- **Three traps, each with its check:**
  1. *The answer key copies the agent.* An engineer may adopt the agent's answer as the confirmed cause. Hand-check a sample, and keep items from before the agent existed.
  2. *Seed items are open-book.* A page or prompt written from an item already holds its answer. Mark each item that seeded a change, and report results on items after the change separately.
  3. *No negatives.* Include items where nothing fits (no known cause, a clean PR), and check the agent says so instead of forcing a match.
- Report ordinary and hard items separately, and a split by source (customer, repo, team) when one source dominates.
- **A failing item is often a broken item.** Before blaming the agent, check the item.

## 3. Grade

- **Code checks first**, wherever the property is exact: a value, a state, a schema, a tool called with the right arguments. Cheap, exact, never drift.
- **Otherwise one yes/no judge per failure mode**, asking about checkable claims ("names the head node as the cause", "cites a query result"), never a 1 to 5 score. A scale is only for comparing two outputs side by side. A multi-part answer gets several yes/no checks, not partial credit.
- **Grade the outcome first**: the final answer, the end state. Check the path only when the path is the requirement, and then check tool choice, arguments, result and resulting state separately.
- **Three result states**: pass, fail, unscored. A grader error or an infra failure is unscored: counted and reported, never a pass and never a fail. An agent that runs out of its own time or turn budget failed; that is the agent's result, not the harness's.
- **No regex on prose.** A pattern match on free text fails correct answers and passes wrong ones; in one audit three of four regex graders were wrong on the first real run. Use exact checks only on exact things, and a judge for prose.
- **A check that inspects nothing fails.** A rule like "X before Y" also passes when X never happened, so pair it with a check that X happened.
- **Keep the grader out of the agent's view**: answer keys, grader files, even their names. In one audit, models read grader file names in a directory listing and treated them as instructions. Then check it held: search the transcripts of every arm, the baseline included, for the answer key, the grader's file names and the skill's path.

Grader hygiene for model judges is in `references/evals.md`.

## 4. Trust the judge

A model judge is a classifier, and an unchecked one makes every score fiction.

- **Label first, then build the judge, and check it as `references/evals.md`, "Checking a judge", says.** Report the two rates in plain words, never raw percent agreement. Below 0.8 on either, the judge is advisory: it reports, it never blocks.
- Freeze the judge's prompt, model and parser together. A change to any of them is a new judge, rechecked.
- **Measure the judge's own noise**: grade the same outputs several times. Identical text has scored 0.40, 1.00, 0.60 and 1.00 from one judge; temperature 0 does not make it stable.
- **Watch its biases**: it favours longer answers, the first of a pair, and its own model's style. Keep answers in comparable shapes and use a different model family.
- **Name the labellers and the tie rule.** Say who labels, how many per item, and what happens when they disagree; human agreement is the ceiling for any judge.
- **Health check before every new pipeline**: push a known-right answer and an empty answer through the whole thing. The right one must pass, the empty one must fail. If more than one in ten failures turn out to be grader errors, fix the grader first.
- **Two sign-offs from a person before any paid run**: the items (after reading about five pilot transcripts) and the grading method.

## 5. Run and compare

- **Always two arms on the same items**: the change and the baseline (the old version, or no skill, no page, no prompt change). A score without a baseline answers nothing.
- **Repeat each item**, 3 runs by default. Temperature 0 is not deterministic. Report reliability as pass^k (all k runs pass), not only one-run accuracy.
- **Know the noise before reading the result.** The ±1/√n rule in `references/evals.md` is a floor; measure the real noise by rerunning the unchanged baseline, which once showed a 7-point spread where the formula said under 2. A difference inside the noise is "no change", and the advice is not to ship.
- **Paired, by item**: count what the new arm fixed and what it broke, not two averages.
- **Report what got worse**, every metric, not only the one that improved. Accuracy, cost per task and p95 latency travel together.
- Drop items that pass in both arms from the comparison; they carry no signal about the change.

## 6. Gate and keep it alive

- **Regression or capability.** Run a new item 5 times. 5 of 5 passes makes it a regression item: any failure blocks the change. Anything less makes it a capability item: reported, never blocking.
- **Never rerun a failure until it passes.** A failure that goes away on rerun is a flake to fix or an unscored result, never a pass.
- **Read the winning change before trusting its score.** An optimiser rewarded on correctness alone once produced a prompt that pasted in the reference answer.
- **The holdout is sacred.** Whatever optimises (a person, a hillclimbing agent, a learner) sees the training items only, never the holdout, and never edits the evaluator, the items or the thresholds. Pick the winning version on a separate selection set; run the holdout once to report it.
- **Split by time when the world moves**: the newest items are the holdout, and the window rolls forward.
- **Every production failure becomes an item**, with its answer key from the world.

## 7. When it applies

- **Safety, for an agent that reads untrusted text**: plant fake secrets (canary strings) and injected instructions inside tool outputs, check none leak or get obeyed, and report usefulness under attack beside attack success. A fixed attack set catches regressions only, not a determined attacker.
- **Cost**: choose models from the accuracy-for-cost frontier. Cache agent outputs only when changing the grader, never when measuring the agent.
- **Simulated users make their own errors**. When a real conversation exists, replay its prefix and test only the next turn.
- **Evaluating a skill**: test triggering apart from behaviour, with near-miss prompts a neighbouring skill owns, and watch whether it actually loads. Then compare with no skill, and run a guidance-deletion test (the skill loaded, its guidance removed) to show the gain comes from what it says, not from loading it. A "don't do X" rule helps when the agent knows a rule and skips it under pressure; it backfires when the problem is the shape of the output, where a positive example works better.

## Rationalisations to refuse

| The excuse | What to do |
|---|---|
| "The model can write the expected answers" | The answer key comes from the world. A model's answer grades the model against itself. |
| "The judge looks right on a few examples" | Measure both rates on held-out labels. |
| "It's 3 points better" | Compute the noise. Inside it, it's no change. |
| "Rerun the failure, it was flaky" | Unscored or a flake to fix. Never a pass. |
| "Tune on the whole set, we have so few items" | Then there's no test. Keep a holdout, however small, and say how small. |
| "The agent can do the error analysis" | It can organise a human's notes. It can't replace reading them. |

## Done when

The three lines from step 0 exist and the user saw them. Real traces were read and the failure modes counted. Every item has an answer key from the world and a frozen input, with seed items and "nothing fits" items marked. The judge, if any, has both rates on a held-out test with intervals. The result compares two arms on the same items with repeats, states the noise, and reports what got worse. Regression and capability items are separated, and the holdout was never seen by whatever optimised.
