# Ledger: Anthropic (and OpenAI) on agent prompts and skills

Line numbers below ("README:N", "lint:N", "evals.md:N") are as of 24 Oct 2026, before this ledger's changes landed.

## Where the gaps went

- Agent prompt rules (B2, B3, B5 to B7, B9 to B13, B16, B21, B22, A1 to A10, A12, A13, A15, A16, A23 to A26, A31): `references/agent-prompts.md`, with its checklist. `review-pr`, `setup-repo` (layer 6) and `evals` point at it.
- Untrusted text tagged with a random id (B23): `references/untrusted-input.md`.
- Evals (E1 to E6): `references/evals.md`, "Grading what matters".
- Skills (S1 reconciled in Principle 1; S2 and S3 in `scripts/lint-skills.py`, which also fixed `ship`'s description; S7, S8, S13, S14, B14 in README "Writing a skill").
- Not taken now, judged harness work rather than wording: A7 continuation handling, A14 update cadence, A20 to A22 multi-session coding scaffolding, A28 to A30 cache order, effort and compaction prompts. Taken only as one line in the reference where it changes how a prompt is written (A7).


Compared against `README.md` (Principles lines 72-85, Writing a skill lines 96-132), `scripts/lint-skills.py` docstring (lines 1-19) and `references/evals.md`. "README:N" and "lint:N" and "evals.md:N" below are line numbers in those files. Everything marked "(inferred)" is my reading, not something a source says.

## Source key

All read in full on 2026-10-24.

- BEA: https://www.anthropic.com/engineering/building-effective-agents
- CE: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- WT: https://www.anthropic.com/engineering/writing-tools-for-agents
- SK: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- MA: https://www.anthropic.com/engineering/multi-agent-research-system
- CCBP: https://code.claude.com/docs/en/best-practices (the old claude-code-best-practices URL now serves this page)
- TT: https://www.anthropic.com/engineering/claude-think-tool
- EV: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (Jan 2026)
- LR: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- HD: https://www.anthropic.com/engineering/harness-design-long-running-apps (newer, found by search)
- MAG: https://www.anthropic.com/engineering/managed-agents (newer)
- CC: https://www.anthropic.com/engineering/building-c-compiler (newer)
- CX: https://www.anthropic.com/engineering/code-execution-with-mcp (newer)
- SC: https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills (Mar 2026)
- SBP: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- PBP: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- O5: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- O55: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5
- OAI55 / OAI56: https://developers.openai.com/api/docs/guides/prompt-guidance?model=gpt-5.5 and ?model=gpt-5.6

Note on O5 for Opus 5.5: O55 says "the patterns in Prompting Claude Opus 5 remain a reasonable starting point", so O5 rows apply to our Opus 5.5 steps unless O55 overrides them.

## Group 1: both (agent prompts and skills)

- **B1** Aim for the smallest set of high-signal tokens; minimal does not mean short. CE. "smallest possible set of high-signal tokens that maximize the likelihood". Both. COVERED (README:100, README:126).
- **B2** Write at the right altitude: no brittle if-else logic, no vague guidance, give heuristics. CE, MA. "instilling good heuristics rather than rigid rules". Both. GAP. Our README:83 ("Process, not prose") and README:121 ("Prefer an operation to a principle") push toward procedure and never warn against hardcoded branching. Not a contradiction (an operation can be a heuristic), but the brittle side is missing.
- **B3** Give the reason behind each instruction, so the model can generalize. PBP. "Claude can generalize from the explanation." Both. GAP. README:131 keeps reasons only for rationalisation rows.
- **B4** Say what to do instead of what not to do. PBP. "Tell Claude what to do instead of what not to do". Both. COVERED (README:116).
- **B5** Keep MUST, CRITICAL, ALWAYS and NEVER for true invariants; current models overtrigger on aggressive wording, and emphasis on many lines cancels out. PBP, CCBP, OAI55. "The fix is to soften any aggressive language." Both. GAP. Note SBP once suggests "MUST filter"; read with PBP, the rule is: absolutes only for invariants, at most one emphasized line.
- **B6** On Opus 5 and 5.5, delete generic "double-check", "verify before finishing" and "use a subagent to verify" lines; they cause over-verification. On gpt-5.6 steps, keep validation but name concrete commands. O5, PBP, OAI55. "instructions like these cause over-verification on Claude Opus 5". Both. GAP. Tension with README:84 and README:125 (inferred reconciliation: a named, runnable check such as a test command stays; a vague "re-check your work" goes).
- **B7** Do not ask the model to write out its reasoning or to "think carefully"; on Opus 5.5 this can be refused (`reasoning_extraction`) and adds latency. Prefer a general instruction over a hand-written thinking plan. PBP, O5, O55. "Remove instructions that stood in for thinking." Both. GAP.
- **B8** Separate sections with XML tags or headers, using consistent tag names. PBP, CE. "Use consistent, descriptive tag names across your prompts." Both. GAP (low, CE says formatting matters less as models improve).
- **B9** Use 3 to 5 diverse, canonical examples in `<example>` tags instead of a laundry list of edge cases. PBP, CE. "curate a set of diverse, canonical examples". Both. GAP.
- **B10** Use one term per concept throughout. SBP. "Choose one term and use it throughout the Skill". Both. GAP.
- **B11** Leave out time-sensitive facts (dates, "before August use X"); move legacy material to an "old patterns" section. SBP. "Don't include information that will become outdated". Both. GAP (README:127 covers restated environment, not dated facts).
- **B12** Give one default plus an escape hatch, not a menu of options. SBP. "Good example: Provide a default". Both. GAP.
- **B13** Match freedom to fragility: exact script for fragile or ordered operations, loose guidance where many paths work. SBP. "Match the level of specificity to the task's fragility and variability." Both. GAP (README:109-114 matches form to the failure seen, not to fragility).
- **B14** Test the prompt or skill on every model that runs it. SBP. "Test your Skill with all the models you plan to use it with." Both. GAP. README:119 pins one model; our steps run on Opus 5.5 and gpt-5.6.
- **B15** Start from a minimal prompt on the best model and add instructions only for observed failures. CE, SBP. "start by testing a minimal prompt with the best model available". Both. COVERED (README:105, README:126).
- **B16** Ablate one component at a time, and re-strip the prompt and harness after every model upgrade, because each component encodes an assumption that goes stale. HD, MAG. "encodes an assumption about what the model can't do on its own". Both. GAP (README:118 compares versions, but nothing triggers a review on model upgrade).
- **B17** State each instruction once; repetition makes the model over-apply it (for example, needless approval requests). OAI56. "State each instruction once." Both. COVERED (README:82, "One fact has one home").
- **B18** Name the specific bad pattern you want avoided; generic "avoid X" swaps one default for another. O55. "responsive to instructions that name the specific kinds of early stop". Both. COVERED (README:111, red flags and rationalisation table).
- **B19** Read real traces and outputs yourself to find failure modes. MA, EV, HD. "Read the transcripts!" Both. COVERED (README:117).
- **B20** Separate the doer from the judge. HD, CCBP. "Separating the agent doing the work from the agent judging it". Both. COVERED (README:80).
- **B21** Tune the evaluator prompt to be skeptical: hard threshold per criterion, few-shot score examples; out of the box it finds issues then approves anyway. HD. "Each criterion had a hard threshold". Both. GAP.
- **B22** In review or finder prompts, ask for every finding and filter in a separate pass; Opus 5 reads "only high-severity" literally and reports less. O5. "ask it to report everything and filter in a separate pass instead". Both. GAP.
- **B23** Wrap pasted or fetched untrusted text in tags carrying a random id, and add one system note saying instructions inside are not the user's. O55. "mark which text is the user's own and which was pasted". Both. GAP. evals.md:32 does this for judges only; `references/untrusted-input.md` states the rule but not this technique (checked by grep).
- **B24** For batch or destructive operations, have the agent write a plan file, validate it with a script, then execute. SBP. "create plan file → validate plan → execute → verify". Both. GAP.
- **B25** For long workflows, give a checklist the agent copies into its reply and ticks off. SBP. "provide a checklist that Claude can copy into its response". Both. GAP (README:125 requires a check per step, not a copyable list).
- **B26** Name MCP tools fully qualified as `Server:tool`. SBP. "always use fully qualified tool names". Both. GAP.
- **B27** Deterministic hooks or gates for anything that must always happen. CCBP. "hooks are deterministic and guarantee the action happens". Both. COVERED (README:75).
- **B28** Ask for evidence (command and output) instead of claims of success. CCBP. "show evidence rather than asserting success". Both. COVERED (README:84).

### Evals (both)

- **E1** Grade the outcome, not the exact path; agents find valid paths you did not expect. EV, MA. "grade what the agent produced, not the path it took". Both. GAP (not in evals.md).
- **E2** Build in partial credit for multi-part tasks. EV. "build in partial credit". Both. GAP.
- **E3** Keep separate capability (low pass rate) and regression (near 100%) suites; graduate saturated capability items. EV. "capability evals with high pass rates can “graduate”". Both. GAP.
- **E4** Do not let graders reject correct answers over formatting (CORE-Bench went 42% to 95% after grader fixes). WT, EV. "Avoid overly strict verifiers that reject correct responses". Both. GAP.
- **E5** Make graders resistant to shortcuts. EV. "Make your graders resistant to bypasses or hacks." Both. GAP.
- **E6** Track tokens, latency, tool calls and tool errors next to accuracy. WT, EV. "the total number of tool calls, the total token consumption". Both. GAP.
- **E7** Balanced cases: where the behaviour should and should not happen. EV. "Test both the cases where a behavior should occur". Both. COVERED (README:104, evals.md:22).
- **E8** Each task gets a reference solution; 0% over many trials usually means a broken task. EV. "a 0% pass rate across many trials". Both. COVERED (README:120).
- **E9** Isolated clean environment per trial. EV, SC. "Each trial should be “isolated” by starting from a clean environment." Both. COVERED (README:119).
- **E10** Judge gets an "Unknown" exit and one isolated judge per dimension. EV. "give the LLM a way out". Both. COVERED (evals.md:31).
- **E11** Start with 20 to 50 tasks from real failures. EV. "20-50 simple tasks drawn from real failures is a great start." Both. COVERED (evals.md:42, evals.md:15).
- **E12** pass^k for reliability. EV, TT. "pass^k measures the probability that all k trials succeed." Both. COVERED (evals.md:57).

## Group 2: agent prompts (system, workflow step, subagent, tool descriptions)

### Task framing and stopping

- **A1** Every subagent brief carries an objective, an output format, which tools and sources to use, and clear boundaries. MA. "an objective, an output format, guidance on the tools and sources". Agent-prompt. GAP.
- **A2** Put effort-scaling rules in the prompt (simple lookup: one agent, 3 to 10 calls; and so on). MA. "Simple fact-finding requires just 1 agent with 3-10 tool calls". Agent-prompt. GAP.
- **A3** Say when not to delegate; Opus 5 spawns subagents readily, including to verify itself. O5, PBP. "do not use subagents to verify or double-check your own work". Agent-prompt. GAP. (Inferred: this is about ad hoc self-checks; a deliberate separate review stage per B20 still stands.)
- **A4** Subagents return a short distilled summary (about 1,000 to 2,000 tokens), or write the artifact to a file and return the path. CE, MA. "pass lightweight references back to the coordinator". Agent-prompt. GAP.
- **A5** One autonomy block: answer, review and diagnose requests report only; change requests may edit and test locally; external writes, destructive or scope-expanding actions need confirmation. Name the safe actions, and say when an ambiguity should trigger a question. OAI56, PBP. "Require confirmation for external writes, destructive actions, purchases". Agent-prompt. GAP.
- **A6** Constrain scope on narrow tasks; Opus 5 widens or transforms tasks. O5. "Deliver what was asked, at the scope intended." Agent-prompt. GAP.
- **A7** For unattended runs, a text-only end of turn is a progress report, not completion. Keep a task checklist, send a continuation naming open items, cap at two or three continuations, and optionally add O55's system paragraph naming four early-stop patterns (only where no human is in the loop). O55. "Treat a text-only end of turn as a report rather than as proof". Agent-prompt (and harness). GAP. High relevance for workflow steps (inferred).
- **A8** Give success criteria and explicit stop rules, including a retrieval budget (when one search is enough). OAI55, MA. "Define success criteria and stopping rules". Agent-prompt. GAP (README:125 covers per-step checks, not when to stop searching).
- **A9** For gpt-5.x (codex) steps, write outcome-first: outcome, success criteria, allowed side effects, evidence rules, output shape; drop step lists unless the path matters. OAI55, OAI56. "Avoid step-by-step process guidance unless the exact path matters." Agent-prompt. GAP.
- **A10** Define missing-evidence behaviour: absence of evidence is not a "no"; ask for the smallest missing field or say what is unknown. OAI55. "Absence of evidence shouldn’t automatically become a factual “no.”" Agent-prompt. GAP. High relevance for incident triage (inferred).
- **A11** With long inputs (20k+ tokens), put the data on top and the question at the end, and ask for relevant quotes first. PBP. "Queries at the end can improve response quality by up to 30 percent". Agent-prompt. GAP.
- **A12** Forbid claims about code or systems the agent has not opened. PBP. "Never speculate about code you have not opened." Agent-prompt. GAP (README:84 is about proof of done, not about speculation).
- **A13** In multi-source work, tell the agent to look across sources the task did not name before acting; Opus 5.5 starts acting quickly. O55. "including ones the task does not explicitly mention". Agent-prompt. GAP (O55 warns to keep untrusted content out of what it searches, see B23).
- **A14** Specify update cadence and final-report shape (one line of intent, updates only on findings, lead with the outcome). On Opus 5.5, progress text comes back in thinking blocks, so a harness rendering only text blocks looks silent unless `display: "updates"` is set. O5, O55. "a client that renders only text blocks can look silent". Agent-prompt (and harness). GAP.
- **A15** Specify length and what a short answer must keep; Opus 5 writes longer documents, gpt-5.6 is already terse and "be concise" can over-shorten. O5, OAI56. "identify the information the model must preserve and the detail it can omit". Agent-prompt. GAP.
- **A16** Use structured outputs or a tool with an enum for classification and schemas, instead of describing the schema in prose. OAI55, PBP. "Remove output schema definitions from the prompt where possible." Agent-prompt. GAP.
- **A17** One-sentence role in the system prompt. PBP. "Even a single sentence makes a difference". Agent-prompt. GAP (low).

### Coding-agent specifics

- **A18** Forbid hardcoding to pass tests, and ask the agent to report tests it believes are wrong. PBP. "Tests are there to verify correctness, not to define the solution." Agent-prompt. GAP.
- **A19** Anti-overengineering block (no unrequested features, comments, fallbacks or abstractions). PBP. "Only make changes that are directly requested or clearly necessary." Agent-prompt. GAP.
- **A20** For multi-session work: a different first-session prompt, a JSON feature list with a pass field, a progress file plus git, an init script, and a start routine (pwd, progress, git log, smoke test). LR, PBP. "the model is less likely to inappropriately change or overwrite JSON files". Agent-prompt. GAP.
- **A21** Tell the agent its context will be compacted so it does not wrap up early, and to save state before the limit. PBP. "do not stop tasks early due to token budget concerns". Agent-prompt. GAP.
- **A22** Parallel tool-call instruction for independent reads. PBP. "make all of the independent tool calls in parallel". Agent-prompt. GAP (low; models already do this often).

### Tool descriptions and tool outputs

- **A23** Write tool descriptions as for a new hire: niche terms explained, unambiguous parameter names (`user_id` not `user`), examples, edge cases, boundaries from similar tools; change arguments so mistakes are hard (absolute paths). WT, BEA. "think of how you would describe your tool to a new hire". Agent-prompt. GAP.
- **A24** Keep a small, non-overlapping, namespaced tool set; consolidate chained calls. CE, WT. "If a human engineer can’t definitively say which tool should be used". Agent-prompt. GAP.
- **A25** Tool and script output: high-signal fields, readable ids, a concise/detailed switch, pagination or truncation with a hint, actionable error messages; scripts print a few lines, log the rest to a file, put ERROR and the reason on one line. WT, CC. "prompt-engineer your error responses to clearly communicate specific and actionable improvements". Agent-prompt. GAP.
- **A26** Per-tool guidance lives in the tool description; cross-cutting policy lives in the system prompt (long, complex guidance worked better in the system prompt). OAI55, TT. "Put most tool-specific guidance in the tool descriptions themselves". Agent-prompt. GAP.
- **A27** Improve tool descriptions from transcripts with an agent; a tool-testing agent cut task time 40%. MA, WT. "rewrites the tool description to avoid failures". Agent-prompt. GAP.

### Harness-side items that change how prompts are written

- **A28** Static prompt first, dynamic last; drop the current date for gpt-5.x; on Claude, keep history append-only and add standing instructions at the start of a run, since mid-run system or tool edits invalidate thinking blocks. OAI55, PBP, O55. "static parts first, dynamic parts last". Agent-prompt (harness). GAP.
- **A29** Set effort explicitly and sweep it; to reduce thinking, lower effort rather than adding prompt text; leave `max_tokens` room. O55, OAI56. "more reliably than prompt instructions do". Agent-prompt (config). GAP.
- **A30** A compaction or handoff prompt keeps completed actions, assumptions, ids, tool outcomes, blockers and the next goal; tune for recall first, then precision. CE, OAI55. "Start by maximizing recall". Agent-prompt. GAP (only if we write compaction prompts, inferred).
- **A31** Prompt changes ship while runs are in flight; roll out gradually. MA. "rainbow deployments to avoid disrupting running agents". Agent-prompt (harness). GAP (inferred relevance to 190 live prompts).
- **A32** Tell the agent when a tool is failing and let it adapt; resume from checkpoints rather than restarting. MA. "letting the agent know when a tool is failing". Agent-prompt (harness). GAP.
- **A33** Evidence for B1 and B17 on codex: leaner system prompts scored higher and cost less. OAI56. "leaner system prompts improved evaluation scores by roughly 10–15%". Agent-prompt. COVERED in principle (README:126); listed as evidence.
- **A34** Fresh-context reviewer sees only the diff and the criteria; tell it to flag only correctness or requirement gaps. CCBP. "Report gaps, not style preferences." Agent-prompt. COVERED (README:80) for the fresh context; the "flag only correctness" half pairs with B22.

### Refused

- **A35** A dedicated "think" tool. TT. "we recommend using that feature instead of a dedicated think tool". REFUSE: Opus 5.5 thinking is always on (O55).
- **A36** Thinking-disabled mitigations (tool calls as text, leaked tags). O5. REFUSE: Opus 5.5 cannot disable thinking. Removing any "do not think" rule still applies (B7).
- **A37** Chat-only items: drop "think carefully" in chat for faster first token, treat earlier answers as settled. O55. REFUSE: our steps are agentic; O55 itself says to leave the second one out where later steps can reveal earlier mistakes.
- **A38** Frontend design defaults and medication dosing blocks. PBP, O55. REFUSE: not our domain.
- **A39** Prefill migration. PBP. REFUSE unless a harness still prefills the assistant turn (inferred; check the artemis call sites).
- **A40** Programmatic Tool Calling routing and `phase` replay. OAI56, OAI55. REFUSE unless enabled; codex CLI manages response state itself (inferred, not checked).
- **A41** Context resets to cure "context anxiety". HD, MAG. REFUSE: MAG says resets "had become dead weight" on Opus 4.5.
- **A42** "/clear after two corrections" and other interactive session advice. CCBP. REFUSE: interactive use, not prompt files.

## Group 3: skills

- **S1** Description says what the skill does and when to use it, in third person, with key terms. SBP. "should include both what the Skill does and when to use it". Skill. GAP, and a conflict: README:74 says "never what the skill does". Our rule rests on our own observation that steps in a description get followed instead of the skill; SBP's examples are capability summaries, not steps (inferred reconciliation: one capability phrase with no steps is compatible with both).
- **S2** `name` is at most 64 characters and must not contain "anthropic" or "claude". SBP. "Cannot contain reserved words: \"anthropic\", \"claude\"". Skill. GAP: lint:7 checks the pattern only, not length or reserved words. No current skill name contains them (checked by grep).
- **S3** `description` must not contain XML tags. SBP. "Cannot contain XML tags". Skill. GAP: lint does not check, and `skills/ship/SKILL.md:3` contains `<reviewer process ID> <what to build>`. Whether a validator treats that as a tag is untested (inferred risk on API upload).
- **S4** Body under 500 lines; split beyond. SBP. "Keep the SKILL.md body under 500 lines". Skill. COVERED (README:100, lint:8).
- **S5** References one level deep from SKILL.md. SBP. "Keep references one level deep from SKILL.md". Skill. COVERED (lint:10-12).
- **S6** Table of contents on reference files over 100 lines. SBP. "include a table of contents at the top". Skill. COVERED (lint:13).
- **S7** Say whether a bundled script is to be run or read. SBP, SK. "Make clear in your instructions whether Claude should". Skill. GAP.
- **S8** Scripts handle errors themselves, print messages that list valid options, and justify constants. SBP. "handle error conditions rather than deferring to Claude". Skill. GAP.
- **S9** Prefer bundled scripts for deterministic work over generated code. SBP, SK. "Prefer scripts for deterministic operations". Skill. COVERED in part (README:100, "move a rule a script can check into the script").
- **S10** Descriptive file names and folders by domain. SBP. "Name files descriptively". Skill. GAP (low).
- **S11** List required packages; do not assume they are installed. SBP. "Don't assume packages are available". Skill. GAP (low).
- **S12** Evals first: three scenarios, a no-skill baseline, then minimal instructions. SBP. "Create evaluations BEFORE writing extensive documentation." Skill. COVERED (README:104-105).
- **S13** Watch how the agent navigates a skill: unexpected read order, ignored files, one file read every time (move it into SKILL.md). SBP. "If Claude never accesses a bundled file". Skill. GAP.
- **S14** Classify each skill as capability uplift or encoded preference; rerun uplift skills' evals without the skill after each model release and retire them once the base model passes. SC. "the skill's techniques may have been incorporated into the model's default behavior". Skill. GAP (README:105 asks for the baseline once, not per model release).
- **S15** Tune descriptions against sample prompts for both false triggers and misses. SC. "cut both false positives and false negatives". Skill. COVERED (README:104).
- **S16** Blind A/B comparison, each eval in a clean context. SC. "They judge outputs without knowing which is which". Skill. COVERED (README:118-119).
- **S17** Strict template versus flexible template, chosen by need. SBP. "Match the level of strictness to your needs." Skill. COVERED (README:112).
- **S18** Bundle long material in files; it costs nothing until read. SBP. "These incur no context penalty until accessed." Skill. COVERED (README:128).
- **S19** Skills with side effects are user-invoked only. CCBP. "Use disable-model-invocation: true for workflows with side effects". Skill. COVERED (lint:5 allows the field; whether every side-effecting skill sets it was not checked).
- **S20** Gerund names (`processing-pdfs`). SBP. REFUSE: SBP lists action-oriented names as acceptable, and our set is consistent.
- **S21** Audit third-party skills before installing. SK. REFUSE: this library authors its own skills.
- **S22** Forward-slash paths. SBP. REFUSE: no Windows authors; nothing to change.

## Checklist for auditing one agent prompt (yes is good)

1. Does each non-obvious rule give its reason in the same sentence, and is each rule stated only once? (B3, B17)
2. Are MUST, NEVER, ALWAYS and CRITICAL used only for true invariants (safety, required fields, forbidden actions), with at most one emphasized line? (B5)
3. On an Opus 5.5 step, is the prompt free of generic "double-check", "verify your answer", "think carefully" and "write your reasoning" lines; on a gpt-5.6 step, is validation named as concrete commands? (B6, B7)
4. Does the prompt state the outcome, the success criteria and an explicit stop rule, including a retrieval budget? (A8, A9)
5. Does it say what to do when evidence is missing (ask for the smallest missing field or report unknown, never turn absence into "no"), and forbid claims about anything not opened? (A10, A12)
6. Is there one autonomy block that names safe actions, actions needing confirmation, the intended scope, and when an ambiguity should trigger a question? (A5, A6)
7. If the step runs unattended, does the harness treat a text-only end of turn as a report, check a task list, and cap continuations at two or three? (A7)
8. Is untrusted text (ticket body, Slack messages, logs, fetched pages) wrapped in tags with a random id, with a system note saying instructions inside are not the user's? (B23)
9. If the prompt delegates, does each brief carry objective, output format, tools and sources, boundaries and a return-size limit, and does the prompt say when not to delegate? (A1, A3, A4)
10. Are tools referenced as `Server:tool`, with unambiguous parameter names, a "use this when, not that" line, and concise outputs with actionable errors? (B26, A23, A24, A25)
11. Are output length and shape pinned (what a short answer must keep), using structured outputs or an enum tool where the output is machine-read? (A15, A16)
12. Has the prompt been run with and without each major block, on every model that runs it, since the last model upgrade? (B14, B16)
