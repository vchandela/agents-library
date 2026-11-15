# Making rules stick

How to write and place a rule so every session follows it, including long sessions, sessions after a compaction, and the many sessions a coordinator runs at once. It comes from a 13 Nov 2026 study of Anthropic, OpenAI, Google, Cursor, the open-source skill repos, and the papers. Two checkers re-opened the sources for 134 claims: 117 held up, 13 were corrected and 4 were dropped. The sources are linked under each rule.

## The one idea

A rule written in a file is guidance. The model may skip it, and it's likelier to skip it late in a long session or after a compaction. A rule that must hold every time belongs in code that runs: a hook, a deny rule, or a wrapper that fails closed. Anthropic's docs say exactly this on the best-practices, memory and skills pages. OpenAI, Google and Cursor all enforce their must-hold rules in the tool layer. One team audited 166 sessions and found rules kept only in docs held 25 to 40% of the time, against about 95% for blocking hooks. That figure is self-reported (https://gist.github.com/beekhof/3b0c70b7c3b2f3cbff1287d4ffcde445).

## Where a rule goes

Decide by how often the rule applies and what a miss costs. Then write it in exactly one place, and point to it from the others.

| The rule | Where it goes | Why there |
|---|---|---|
| Must never slip, and a command can check it (a production query without a time limit, a hand-off while CI is red) | A blocking hook, plus one line in the topic reference saying the hook exists | Prose fails under load. A hook runs every time. |
| How every session behaves on every turn (when to speak, evidence before a claim) | The always-loaded core rules file. It stays under about 15 short rules. | It loads in every session and comes back after a compaction. Every line added there costs adherence on all the others. |
| An engineering rule tied to a situation (a list endpoint, a retry, a migration) | One line in the always-loaded technical index, pointing to its topic reference | Loaded always, but only as a one-line index entry |
| The detail and the reasons for a rule | Its topic reference (the shipping guide, the hand-off protocol, the stacked-PR guide and so on) | Read when a skill or the index points to it |
| Steps for one kind of task | That skill's `SKILL.md`, with long parts in files beside it | Loads only when the task does |
| A fact about one repo (its commands, its accounts, its deploy order) | That repo's `CLAUDE.md` or `AGENTS.md`, aiming for about 200 lines | Repo facts don't belong in a shared library |
| Something learned about the user (a preference, a correction) | The shared memory folder | Recall, not enforcement. Codex says not to rely on memory "as the only source for rules that must always apply". |

A coordinator that's asked to "tell every thread" edits the file this table names. It never pastes the rule into messages. Sessions re-read files on their own, and a message from another session never counts as the user's approval in Claude Code (https://code.claude.com/docs/en/cross-session-messaging). If the change matters today, the coordinator messages only the threads that must act on it, in one line that names the file.

## Writing a rule

- **Say what to do, not what to avoid.** In superpowers' own tests, a ban on a behaviour did worse than no guidance at all, and a step-by-step recipe did best. A ban on one discrete act is the exception, and it works (https://github.com/obra/superpowers). For when to speak, list the allowed reasons, as Anthropic's Opus 5.5 prompting guide does with its four acceptable turn endings.
- **Give the reason and one example, in calm words.** Capitals and "MUST" added nothing measurable in superpowers' tests (issue #2377). Anthropic says emphasis now makes models apply a rule too broadly.
- **Make the rule checkable.** "No TODOs, no partial implementations" beats "remember to finish" (Cursor). A limit is a flag on the command, not a sentence: superpowers' "stay bounded" rule failed twice in prose, and only a timeout flag worked (issue #2472).
- **Put rules that fire at the end of a job in a hook.** A rule meant for the end of a response dropped by up to 50% in one study (arXiv 2603.23530).

## Keeping rules in view

- **After a compaction, add the key rules back.** Compaction kept only about 17% of the rules given during a session, and adding them back afterwards raised that above 90% ("Lost in Context Compaction", arXiv 2608.11242). Use a startup hook on the `compact` event. It fires on automatic and manual compactions, and the post-compaction hook can't change what Claude sees.
- **Keep each `SKILL.md` under 20,000 characters.** After a compaction, Claude Code keeps only the start of each skill (5,000 tokens per skill in the docs; superpowers saw the cut at exactly 20,000 characters, issue #2481). A rule past that point is gone. Put a skill's must-hold lines near the top, and move rarely needed parts into its `references/`.
- **Load fewer rules at once.** One model obeyed all of 1 instruction 94% of the time, but all of 10 only 21% (ManyIFEval, arXiv 2509.21051). Skills of standard size helped by 21.5 points, while long all-in-one guides helped by 0.7 (SkillsBench, arXiv 2602.12670; the long-guide result rests on 5 tasks). OpenAI replaced one big AGENTS.md with a map of about 100 lines (https://openai.com/index/harness-engineering/).
- **A file a skill points to isn't loaded until it's read.** Cursor says referenced files "are not inlined". Anything that must always be in view goes in the always-loaded file itself.
- **Edits reach a running session only after `/clear`, `/compact` or a restart.** So a new rule takes effect at a session's next start or compaction.
- **Use one memory folder for every session.** Set `autoMemoryDirectory` in user settings, so a session sees the same memory whatever folder it starts in. Keep `MEMORY.md` under 200 lines and 25 KB, because only that much loads.

## Many sessions

- **A worker wakes the user for only two reasons: its work is ready after review, or it needs a decision only the user can make.** Status belongs in a file the coordinator reads, not in a message (Devin, Copilot's coding agent and Claude Code's agent teams all work this way).
- **Every message wakes the session it's sent to.** An idle session starts a new, paid turn for each message, and there's no broadcast. That turn must end with some text, so each message adds a line to that tab. Message only the threads that must act.
- **Check claims by re-running them, not by reading the report.** Copilot can't approve its own PR, and Factory uses fresh validator agents. In the MAST study, failures to verify the task made up 23.5% of multi-agent failures (arXiv 2503.13657).
- **Measure over whole sessions, several times each.** In tau-bench, one model succeeded on 61% of tasks in a single try but under 25% when it had to succeed on all eight tries of the same task (arXiv 2406.12045). Test a rule with it and without it, on a few real prompts, a fresh session each time.

## Not known yet

- Whether stating the reason for a rule makes it likelier to be followed. No controlled study was found.
- Whether a stop hook fires on a turn that another session's message started.
- Whether a guard hook sees tool calls made inside subagents. A 2026 issue said it didn't (anthropics/claude-code #43612).
