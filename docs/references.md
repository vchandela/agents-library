# What was taken, and what was refused

Where each idea came from, so adopting the next harness is a decision rather than a habit.

## Taken

| From | Idea |
|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | A description says when to read, never what it does. Found by testing, not taste. |
| obra/superpowers | Rationalisation tables: write down the excuse, then the rebuttal. |
| obra/superpowers | Match the form to the failure. A rule broken under pressure needs a prohibition, not guidance. |
| obra/superpowers | No skill without a failing baseline first. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | User invoked against model invoked, stated per skill. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Process, not prose. Steps, checkpoints, exit criteria. |
| addyosmani/agent-skills | Evidence requirements. "Seems right" is never sufficient. |
| [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) | Negative triggers in the description. |
| mgechev/skills-best-practices | The three step validation loop, which replaced a compliance harness. |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | Distribution. `npx skills add` already handles 80+ agents. |
| [anthropics/skills](https://github.com/anthropics/skills) | Minimal frontmatter. Two fields. |
| [Anthropic, multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Scale effort to the question; sub-agents with clear, non-overlapping boundaries; a separate citation pass. |
| [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer) | Read the user's own material first, fully, before searching. |
| [langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) | One round of clarifying questions, a written brief, stop when searches repeat. |
| [stanford-oval/storm](https://github.com/stanford-oval/storm) | Research by perspective; ask "what did we find and not use?" before writing. |
| addyosmani/agent-skills | Label what could not be verified, in the text. |
| addyosmani/agent-skills | Source authority order for a fact: official docs for the version in use first, never training data. |
| addyosmani/agent-skills | Performance as keep or revert: one change, measured the same way, and neutral is a revert. Never present a number you did not measure. |
| addyosmani/agent-skills | The reviewer gets the artifact and the contract, never the author's claim. |
| addyosmani/agent-skills | Guard the bar itself: a loosened threshold or new suppression is loud. Ratchets. Exceptions with an owner and expiry. |
| addyosmani/agent-skills | A rollback plan before any deploy, first-hour checks, staged rollout thresholds. |
| addyosmani/agent-skills | Interview with a guess attached to every question. |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Judge the screen before reading any detector output. Check the evidence before reviewing it. |
| pbakaus/impeccable | Bounded inspection rounds: one batch, one confirming round. |
| pbakaus/impeccable | The craft floor and detector thresholds as a generic UI checklist; personas; copy rules for errors and empty states. |
| [blader/humanizer](https://github.com/blader/humanizer) | One theory of machine tells, ranked by strength, with a last pass that compares facts as well as style. |
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | Pick the diagram by what the reader must understand; a complexity budget; the remove test; grammar per diagram type. |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | Map hubs and recorded why before reading; tag every relationship read, inferred or unclear; search in the repo's own words. |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | The ordered ladder before writing code, the never-cut floor, cut corners marked in code with a trigger, numbered tagged simplification findings. |
| DietrichGebert/ponytail | Change a skill against two baselines, and prefer an operation to a principle (measured 0 of 3 against 6 of 6). |
| mattpocock/skills | A red-capable loop before any hypothesis; interviews in frontier rounds; a spec axis in review; vertical slices and expand-contract; fog versus out of scope; the deletion test; no-ops. |
| [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | The pre-send deletion check; state restated every turn; name a cause only with evidence; isolated, pinned baselines; inspection is not execution. |
| obra/superpowers | Root cause before any fix, with the three-failures stop; the claim and evidence table; global constraints and produces and consumes in plans; never pre-judge the reviewer; a green baseline. |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | The six-part bar for a finding; three verdicts, with no severity on needs validation; severity capped by shown impact; the ledger as the coverage claim; a fresh verifier that tries to refute. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | One positioning doc every page skill reads first; review a page in impact order (clarity, headline, one action, proof, objections, friction); the "Now you can" test; the perception gap; the four forces of switching; activation as time to the first win, do not show, empty states that teach, started progress and peak-end; four copy tells (negation lists, pile-ons, self-answered reveals, stock pitch). |
| [RefoundAI/lenny-skills](https://github.com/RefoundAI/lenny-skills) | Positioning: the status quo is the real competitor; name the foil; win on one value vector, not "better". |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | A description names the case the model would do alone ("even when the diff is pasted inline"): 7 to 21 fires of 27 in its plugin eval. |
| [obra/superpowers](https://github.com/obra/superpowers) | A spec or plan skill ends the turn, and rationalisation rows keep their reasons (8 of 10 against 5 of 10). |
| [SkillsBench](https://arxiv.org/abs/2602.12670) | Focused skills help, comprehensive ones barely do, and four or more loaded at once hurt. |
| [good-css.com](https://good-css.com) | Inputs at 16px, hover only on hover devices, outline focus rings, `color-scheme`, `scroll-padding`, `overflow: clip`, native disclosure, dialog and popover. |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable), ui-ux-pro-max, taste-skill, hallmark | A fresh reviewer for the finished screen; keyboard and overlay mechanics; axe and the accessibility tree; long unbroken text; settled captures. |
| openai/codex, anthropics/claude-code, Anthropic memory docs | Instruction file budget: under 200 lines (Anthropic), under 32 KiB (Codex truncates silently); none of the surveyed lab repos tests the size, so add the test. |

## Refused

| From | Refused | Why |
|---|---|---|
| obra/superpowers | Nine harness plugin directories | Ship the one in use. Add another when another is actually used. |
| ECC | 286 skills, 68 agents, 94 commands | A catalogue to maintain. A small working set, each skill earning its place. |
| ECC | Auto extracted "learned" skills from transcripts | Unreviewed content writing itself is the thing a curated repo exists to prevent. |
| ECC | Per session cost tracking, desktop notifications, MCP health checks | Agency scale problems. |
| marketingskills, pm-skills, Product-Manager-Skills, lenny-skills | 272 skills between them: SWOT, PESTLE, Porter, lean canvas, OKR brainstorms, persona templates, headline formula catalogues, cold email, ads | Frameworks that produce documents rather than change what ships. One skill that judges a page and rewrites it beats forty that fill templates. |
| lenny-skills | Guest quotes as the substance of each skill | Authority by name. Kept the idea, dropped the quote. |
| ECC | The plugin bootstrap resolver | A 900 character inline resolver for marketplace installs. Not needed for a repo you clone. |
| everyone | A build step that compiles skills from fragments | Five of five hand write. Ten lines of duplication does not justify a generator and a drift test. |
| everyone | An install script | `npx skills add` exists and does symlinks properly. |
| me | A custom compliance measurement harness | Use the native `claude plugin eval` instead: isolated runs, a no-plugin baseline and graders, with no machinery to maintain. The trigger cases live in `evals/`. |
| Anthropic, agentskills.io | A description that says what the skill does, then when | A description that says what gets followed instead of the body (superpowers), and describing what the skill adds did not raise triggering (addyosmani, Sep 2026). Ours open with "Use when". |
| mattpocock/skills | "Refactoring is not part of the loop" | Conflicts with refactor only on green. |
| mattpocock/skills | One assertion per test | Conflicts with fat tests. |
| mattpocock/skills | No file paths in specs | `file:line` is how claims stay checkable. Taken only for briefs that wait days. |
| mattpocock/skills | "Prompt the positive" as a rule | Conflicts with the prohibition finding; only the pairing is taken. |
| DietrichGebert/ponytail | "Never stall on an answer you can default" | Conflicts with stop and ask after a plan is approved. Rulings are allowed only on unattended runs. |
| ponytail, i-have-adhd | Always-on persistence modes and intensity levels | A skill fires when relevant; persistence belongs in a hook. |
| obra/superpowers | "1% chance, you must" skill invocation, all caps iron laws | Anything that must always hold is a hook. Keep the content, refuse the shouting. |
| obra/superpowers | "Delete means delete" for code written before its test | Stash, confirm red, restore proves the same without throwing work away. |
| cloudflare/security-audit-skill | Artifact promotion, JSON validators, budget arithmetic | One-organisation scale. The ideas behind them are kept. |
| pbakaus/impeccable | Aesthetic bans (fonts, palettes, eyebrows) | Taste for marketing pages, not a generic floor. |
| addyosmani/agent-skills | Error-budget gates and fixed canary percentages | Assume an SLO and a flag service most repos do not have. |
| mattpocock/skills, humanizer | A retro skill and a prose detector script | Delete before adding: the checks they would run are already in testing and machine tells. |

## Own

Not found in any of the repos read.

- **Authority badges counted by organisation.** No research skill or deep-research tool read scores how widely an idea is adopted; GPT Researcher only de-duplicates URLs.
- **Separation of proposer and critic.** All five assume one agent plans, implements and reviews. The pipeline here hands off instead, with bounded rounds and a gate before implementation.
