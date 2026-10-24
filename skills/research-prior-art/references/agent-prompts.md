# Agent prompts

How to write text that a model runs as instructions: a workflow step's prompt, a system prompt, a sub-agent brief, a tool description, and a skill's own body. Most of it comes from Anthropic's engineering posts and model guides, plus OpenAI's guide for the steps that run on its models. Where a rule came from our own failures, the example says so.

## Contents

- Write the rule with its reason
- Firm words only for real limits
- What each model needs
- Evidence and missing evidence
- Outcome, success and when to stop
- Scope and what the agent may do alone
- Sub-agent briefs
- Review and finder prompts
- Tools and their output
- Output shape
- After a model upgrade
- Checklist for one prompt
- Sources

## Write the rule with its reason

- **Give the reason in the same sentence.** A model that knows why a rule exists applies it to cases the rule did not name. "Never use ellipses, because a text-to-speech engine reads this aloud" beats "never use ellipses".
- **Pitch it at the right height.** Too low is brittle if-else logic that breaks on the first case nobody listed. Too high is "be thorough". Aim for a heuristic plus one real example: "once you have a cause, count what the cause touched, not only what the alert watches", followed by the case where a reply said 3 clusters and the true number was 43.
- **Say what to do, not only what to avoid.** "Write it as one paragraph" works better than "no bullet points". A prohibition gets the behaviour you want next to it.
- **State each rule once, and use one word per idea.** Repeating a rule makes the model over-apply it. Two names for one thing ("report" and "findings" for the same file) make it guess whether they differ.
- **Give one default and an escape hatch, not a menu.** "Use X. If X is unavailable, say so and use Y" is followed. A list of five equal options is not.
- **Match freedom to fragility.** An exact script for an ordered or destructive operation (a migration, a merge). Loose guidance where many paths reach the goal (an investigation).
- **Leave out facts that date.** "Before August use the old endpoint" is wrong by September. Put legacy material in a short "old patterns" section, or delete it.
- **Show, briefly.** Three to five varied, real examples teach more than a long list of edge cases.

## Firm words only for real limits

Current models follow the system prompt closely, and aggressive wording makes them overdo it: "CRITICAL: you MUST use this tool" turns into using the tool everywhere. Keep MUST, NEVER, ALWAYS and capitals for true invariants: never post, never push, never print a secret, read-only, and a fixed output contract that a parser reads. Emphasise at most one line in a prompt. When every paragraph is bold or in capitals, nothing stands out.

## What each model needs

**Claude Opus 5 and 5.5.**
- Delete generic self-checks: "double-check your work", "verify before finishing", "use a sub-agent to verify". Opus 5 verifies on its own, and these lines cause over-verification: more tokens and latency, with no gain in quality. A named, runnable check stays ("run `pytest tests/x.py`"), and so does a separate reviewer step by design (see Review and finder prompts).
- Do not ask it to write out its reasoning, or to "think step by step" in the reply. Thinking is always on in Opus 5.5. A prompt that pushes it to reproduce its reasoning in the response can be declined with the `reasoning_extraction` refusal, which the server does not retry on a fallback model. Asking for a short explanation of the answer, a cause chain or cited evidence in a report is fine.
- Pin the scope on narrow tasks. Opus 5 widens or transforms a task. Anthropic's sentence: "Deliver what was asked, at the scope intended."
- Say when not to delegate. It spawns sub-agents readily, including to check its own work.
- For long documents, say how long and what a short version must keep. Opus 5 writes longer.
- On an unattended run, a turn that ends with text and no tool call is a progress report, not "done". The harness should check the task list and send one continuation that names what is open, capped at two or three.

**OpenAI gpt-5.5 and 5.6 (codex steps).**
- Write outcome first: the outcome, what success looks like, which side effects are allowed, the evidence rules and the output shape. Drop step lists unless the path itself matters.
- Name validation as concrete commands. The opposite of Opus: here a stated check helps.
- It is already terse, so "be concise" can cut what the reader needs. Say what the short version must keep.
- Contradictions hurt it more than older models. It takes words literally and echoes the conflict back.

## Evidence and missing evidence

- **Absence of evidence is not a "no".** Say how the agent should behave when evidence is missing: report it as unknown, name the smallest missing piece, or ask. An empty query result is a finding about the query until the query is shown to measure the claim.
- **No claims about anything the agent has not opened.** Not code, not a dashboard, not a ticket. Anthropic's line: "Never speculate about code you have not opened."
- **Look across sources the task did not name.** Opus 5.5 starts acting quickly. A triage that read only the alert misses the engineer's message in the thread.
- **Every number counts what its sentence says.** Requests, queries and log lines are different counts. One triage reported one slow request when there were two, because one request ran two queries.

## Outcome, success and when to stop

Every prompt states what done looks like and when to stop. That includes a search budget for lookups: one search is enough for a fact, a few for a comparison, and many only for a landscape. Without a stop rule an agent either quits after the first plausible answer or keeps searching after the answer is in hand.

## Scope and what the agent may do alone

Put one block near the top that says:
- what the agent may do alone (read, query, run tests locally)
- what needs a person's yes (external writes, posting, destructive or scope-widening actions)
- the intended scope
- when an ambiguity should become a question rather than a guess

One block beats rules scattered across the file, because the model reads one clear boundary instead of reconciling five partial ones.

## Sub-agent briefs

Each brief carries an objective, an output format, the tools and sources to use, the boundaries (what other sub-agents cover, what not to touch) and a size for what comes back. That is about a thousand to two thousand tokens, or an artifact written to a file with only the path returned. A brief without boundaries produces overlapping work. A brief without a return size floods the coordinator's context.

## Review and finder prompts

- **Ask for every finding, then filter in a separate pass.** Opus 5 reads "report only high-severity issues" literally and reports less. Have it list everything with a severity, then a second pass (or the reader) filters.
- **A separate reviewer is a design choice, not a self-check.** A fresh session that sees only the artifact and its contract finds what the author cannot. Give it a hard threshold per criterion and an example of a failing score. Out of the box, an evaluator finds problems and then approves anyway.
- **Check the action, not only the claims.** A verifier that re-checks every number but never asks whether the recommended fix breaks the cause lets a wrong fix through. One triage named a change request as the fix, and asked later, the same bot said it would not clear the alert.

## Tools and their output

- Describe a tool as you would to a new hire: the niche terms, unambiguous parameter names (`user_id`, not `user`), one example, and a "use this when, not that" line against its nearest neighbour.
- Keep the tool set small and non-overlapping. If an engineer cannot say which tool fits, the model cannot either.
- Refer to MCP tools by their full name, `Server:tool`.
- Tool and script output is short and high-signal: readable ids, a short and a detailed mode, a hint when output was cut, and errors that say how to fix the call. A script prints a few lines, logs the rest to a file, and puts ERROR and the reason on one line.
- Per-tool guidance lives in the tool's description. Policy that cuts across tools lives in the system prompt.

## Output shape

- When a machine reads the output, use structured outputs or a tool with an enum rather than describing a schema in prose.
- When a person reads it, pin the length and say what a short answer must keep.
- With a long input (20,000 tokens or more), put the data first and the question last.

## After a model upgrade

Every line in a prompt and every step in a harness encodes an assumption about what the model cannot do alone, and an upgrade can make it dead weight. After each model change, run the prompt with and without each major block on every model that runs it, and delete what no longer moves the result. Context resets were needed on earlier models, and Anthropic found they "had become dead weight" on Opus 4.5. Ship prompt changes gradually, because runs already in flight read the old text.

## Checklist for one prompt

Copy it and tick it for each prompt you write or review. A yes is good.

1. Each non-obvious rule gives its reason in the same sentence, and each rule appears once.
2. MUST, NEVER, ALWAYS and capitals appear only for real limits, with at most one emphasised line.
3. On an Opus 5 or 5.5 step: no generic "double-check", "verify your answer", "think carefully" or "write out your reasoning". On a gpt-5.x step: validation is named as concrete commands.
4. It states the outcome, what success looks like and when to stop, including a search budget.
5. It says what to do when evidence is missing, and forbids claims about anything not opened.
6. One block names what the agent may do alone, what needs a yes, the scope, and when to ask.
7. Untrusted text (tickets, Slack, logs, fetched pages) is marked as data, following the untrusted input rules.
8. A brief to a sub-agent carries objective, output format, tools, boundaries and a return size, and the prompt says when not to delegate.
9. A review or finder prompt asks for every finding with a severity and filters afterwards.
10. Output length and shape are pinned, with structured output where a machine reads it.
11. It has been run with and without its major blocks on each model that runs it since the last model upgrade.

## Sources

Read in full on 24 Oct 2026. The rule-by-rule ledger, with what was taken, covered or refused, is `docs/ledgers/anthropic-prompting.md` in this repo.

- Anthropic: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents), [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), [Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), [Harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps), [Managed agents](https://www.anthropic.com/engineering/managed-agents)
- Anthropic docs: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [Prompting Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5), [Prompting Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5), [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- OpenAI: [Prompt guidance for gpt-5.5 and 5.6](https://developers.openai.com/api/docs/guides/prompt-guidance)
