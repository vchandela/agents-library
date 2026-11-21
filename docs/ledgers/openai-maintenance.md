# Ledger: OpenAI, "Maintaining software with the GPT-6 family"

Source: https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family, read in full on 21 November 2026 (12,609 characters served as markdown). The page has no publication date and no byline; the author writes in the first person from OpenAI's Core Experimentation team. It describes Codex sessions on GPT-5.6 Sol, GPT-6 Astra and GPT-6.1 Sol; those model names, Codex, `/goal`, Statsig and the console are their stack, not the practice.

## What was taken, and where it went

- **The method**: start small, review, expand; ask for one instance, evidence and a small draft PR; feed review comments into the next prompt; keep prioritization and measurement because some proposals cost more than they saved. -> `skills/maintain-codebase`, "The rules that hold every lane" ("Start small, then expand", "A person merges").
- **Unused code**: an area plus a validation criterion; check past PRs, team chat, the project tracker and production profiling; confirm nothing uses it; explain each deletion; small PRs reviewed by people with project context. -> lane 3.
- **Stale experiments**: verify live configuration, not labels; check git history and overlapping PRs; preserve production behavior, safeguards and killswitches; ignore SDK fallbacks and local overrides; audit all projects and inventories; find indirect uses through enums, constants, wrappers, aliases, schemas, dynamic names and cross-service consumers; reconcile every production-referenced constant; use telemetry and CPU to prioritize; one small PR per cleanup with the object's page linked; never change live configuration; a "Permanent" flag goes to a person. -> lane 4. The vendor name Statsig and the "console link" were replaced by "your feature-flag or experimentation platform" and "the object's page in the platform".
- **Flaky tests**: recent CI runs, a clear fix for a simple issue and one PR per fix, not every flaky test. -> lane 2; the library's `references/testing.md` already says "Fix or delete; never retry them green", and the new lane adds the rate, the clear-fix scope and the quarantine row with an owner and expiry.
- **CI cost**: a table of ideas ranked by estimated CI minutes saved per day from the run history; the missing mock that cut a 63-test suite from 592.6 s to 29.8 s. -> lane 5 and the before/after rule.
- **Improving agentic context**: replay one instruction from the same repository snapshot and model, with it and without it, compare quality, behaviour, tool calls, tokens, runtime and cost, and keep the change only if it helped. -> `skills/analyze-agent-transcripts` ("Did the last changes work?") and `references/agent-prompts.md` ("After a model upgrade").
- **The measured results**, kept in this ledger and not in the generic skill: five engineers, more than 1,400 maintenance PRs, over 800k lines removed in two part-time weeks; a container image from 3.31 GB to 1.72 GB (48%); about 400 visual snapshot variants removed; hundreds of experiments and flags removed, one at 0.42% CPU saving; about 30 CI optimization PRs, median CI 10 to 4.5 minutes and the 90th percentile 12.5 to 6 minutes; the resolver suite's 63 tests from 592.6 s to 29.8 s with all retained; the model comparison: GPT-6 Astra Ultra $109.06 for 142 findings, GPT-6.1 Sol Ultra $15.12 for 131, GPT-6.1 Sol Medium $5.27 for 86.

## What was refused or not taken

- **Statsig, Codex, `/goal` and the model names** were not written into the skill. A reader's platform may be a vendor product or an in-house service; the skill names the practice and leaves the product to the repo.
- **The broad dead-code prompt as written** ("Can you help identify and clean up dead code in the repo please ... feel free to check slack, statsig ...") depends on their tools and their model; the skill carries the generic version and says a broad audit is a source of candidates, not the proof.
- **The second stale-experiment prompt is abridged by the page itself**, with an editorial omission covering the detailed verification instructions; it was not reconstructed.
- **Dependency upgrades and refactors** are not in the page. The dependency and migration lane comes from the library's own engineering rules; the page's "cleaned up or simplified" is not a refactor practice.
- **Their team workflow** (draft PRs, review comments, a visual snapshot suite) is a team's practice, not a rule; the skill keeps one small change, the evidence and a human merge.

## What the page did not contain

No publication date, no named author, no repository or service names, no exact count of experiments or flags beyond "hundreds", and no graph or table for the model benchmark beyond the caption figures. The replay prompt is the only "agentic context" material, and the page gives it as a single prompt, not as prose guidance.
