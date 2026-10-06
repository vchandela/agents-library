# agents-library

Library of skills, prompts and other best practices.

Nineteen skills for engineering work with coding agents. Portable across Claude Code, Claude Desktop, Codex and anything else that reads `SKILL.md`.

## Install

    npx skills add vchandela/agents-library

Project scope or global, symlink or copy. Or clone it and link each skill folder into `~/.claude/skills/`; never link `SKILL.md` on its own.

## What is in here

**The pipeline.** Six skills, one workflow, run in order.

| Skill | Does |
|---|---|
| `write-spec` | Interviews you, then writes the spec |
| `write-plan` | Turns a spec into an implementation plan |
| `review-plan` | Tears the plan apart. Different agent. |
| `implement-plan` | Executes an approved plan, stops when unsure |
| `split-commits` | One change becomes logical commits |
| `review-pr` | Reviews a diff, design first, line level last |

**Understanding.**

| Skill | Does |
|---|---|
| `understand-codebase` | What a repo decided, and what it gave up |
| `research-prior-art` | How others already solved it |
| `extract-insights` | Mines a talk or article for what is worth keeping |
| `save-to-notes` | Files it into a Zettelkasten vault, after you approve |

**Verifying.**

| Skill | Does |
|---|---|
| `qa-live-site` | QA a deployed app, states first, then seven phases |
| `diagnose-bug` | A loop that goes red first, then the cause, then the fix |
| `review-security` | Proves a trust boundary failure from source, or says what it could not see |
| `review-product-page` | Will a stranger get it, believe it and act? Positioning first, then the page in impact order |

**Writing.**

| Skill | Does |
|---|---|
| `write-tech-doc` | A proposal for colleagues who read critically |
| `write-blog` | A shipped system becomes a published post |
| `explain-simply` | First principles, no hand waving; also explainer pages |
| `honest-feedback` | What you actually think |

**Meta.**

| Skill | Does |
|---|---|
| `setup-repo` | Applies these conventions to another repo |

## The idea this repo is built on

**The agent that produced the work does not review the work.**

An agent reviewing its own plan re-reads its own reasoning and finds it convincing, because it is the reasoning it just chose. So the pipeline is six skills rather than one, and three of them hand off to a different session and ideally a different model family. `references/handoff-protocol.md` has the detail.

Most public skill repos let one agent plan, build and review. A few now hand review to a separate agent or provider. This pipeline makes the handoff a gate: no implementation before an independent plan review, and bounded rounds.

## Principles

1. A description says **when to read**, never what the skill does. A description containing steps gets followed instead of the skill.
2. Skills are probabilistic. They fire most of the time, not every time. Anything that must always hold is a hook or a test.
3. **A rule with no check is a rule you break yourself.**
4. Red, green, then **break the code and watch it fail again**. The third step finds tests that assert nothing.
5. Facts block. Judgements warn. A gate with false positives gets switched off.
6. Fact forcing beats self evaluation. "Did you check?" always returns yes.
7. Separate the proposer from the critic.
8. A bug report names one instance. Fix the class.
9. One fact has one home.
10. Process, not prose. Steps, checkpoints, exit criteria.
11. Evidence over claims. Every skill says what proves it worked.
12. Every complexity earns its place.

## Layout

    skills/       one folder each, SKILL.md inside
    references/   shared text the skills point at; edit it only here
    scripts/      sync-references.sh copies references/ into each skill
    docs/         what was taken from where, and what was refused

Each skill carries its own copy of `references/`, so a single skill folder still works when it is copied, zipped, uploaded or installed as a plugin. Edit the top-level `references/`, then run `scripts/sync-references.sh`. CI fails if a copy is stale.

## Writing a skill

Two frontmatter fields, `name` and `description`. The description is the whole trigger: write it as "Use when ...", and add what it is **not** for, or it fires on neighbouring work.

Keep the body short. Under 500 lines is the ceiling, under 200 words is the target for anything used often. Put long material in `references/` and point at it.

Before shipping one:

1. **Trigger test.** Paste only the frontmatter into a fresh chat. Ask for three prompts that should fire it and three that should not. If the model cannot separate them, the description is wrong.
2. **Baseline.** Run a real task without the skill and write down how it goes wrong. If nothing goes wrong, the skill has no reason to exist.
3. **Loopholes.** Run it again with the skill and note every excuse for skipping a step. Those become the rationalisation table.
4. **Match the form to the failure.**

   | The baseline went wrong by | Write | Not |
   |---|---|---|
   | Knowing the rule and breaking it under pressure | A prohibition, a rationalisation table, red flags | "Prefer" or "consider" |
   | Complying, with output of the wrong shape | The shape itself: its parts, in order | A list of don'ts |
   | Leaving out one required part | A required slot in the template it fills | A reminder near the template |
   | Behaviour that should depend on a condition | A conditional on something observable | A rule plus exceptions |

   A nuance clause ("don't X unless it matters") reopens the negotiation. Pair every prohibition with the behaviour you want instead.
5. **Micro-test the wording.** Send a tempting task five or more times with the skill and five times with no guidance. If the control does not fail, there is nothing to fix. Read every output yourself. Five different shapes across five runs means the wording does not bind yet.
6. **Change against two baselines.** Run the same task three ways: no skill, the current skill, the changed skill. Include one task the change should help and one existing task it could break. Wording that does not move the result does not ship, however reasonable it reads.
7. **Isolate the baseline.** Run every arm with your own hooks, plugins and memory switched off (`claude --setting-sources ""`), and pin the model. Two public skill repos found their baseline secretly running the skill under test through an always-on hook.
8. **Prove the check before trusting it.** Every scoring check gets one known good and one known bad answer, and must pass the first and fail the second. Check that every task can be passed at all.
9. **Prefer an operation to a principle.** "Trace the flow end to end" scored 0 of 3 in one public eval. "Grep every caller of the function you touch and fix the shared function once" scored 6 of 6.

While writing:

- **Every step ends on a check.** "Every modified model accounted for" makes the agent do the work. "Produce a change list" does not.
- **Hunt no-ops.** A sentence the model already obeys by default costs context and changes nothing. Test it by running without it, then delete it.
- **Do not restate the environment.** A line that copies `package.json` scripts or the directory layout goes stale. Write what a lookup cannot find: the reason, the gotcha, the unwritten convention.
- **Inline what every path through the skill needs; put what only some paths need in `references/`.**

## Licence

Apache 2.0.
