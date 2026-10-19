# Changelog

## [Unreleased]

### Added
- `references/system-design/`: a toolbox for picking mechanisms. `index.md` maps a design problem, written as a plain question, to an entry, and fourteen family files (storage, caching, queues and streams, long-running work, consistency and concurrency, scaling and partitioning, real-time updates, search, large files, counting and aggregation, APIs and the edge, ML systems, code structure, numbers) give each tool's use, its wrong fits, the choice it forces and how it fails, with links to the lessons it came from. `write-spec`, `write-plan` and `review-plan` point at the index.
- `make-slides`: reading or speaking deck first, an agreed outline of title claims and evidence, the answer first for an exec deck, one point per slide, split rather than shrink, Google Slides API traps, and a thumbnail check of every slide. It runs explain-simply for the content. Every rule from the eleven source files is sorted in `docs/ledgers/make-slides.md` as covered, taken or refused, with the reason.
- `ship`: one command runs spec, plan and stacked PRs, with a separate reviewer session on each stage and the user approving every stage. Rounds continue until the reviewer approves, and it stops for the user only on a disagreement about requirements. It moved here from a local copy.
- `design-ui`: the order of work for a new screen (the job, the repo's tokens, a state grid, build, a look at every width and theme), judged against `references/ui-quality.md`.
- `diagnose-bug`: a red-capable loop before any theory, ranked hypotheses, one variable at a time, the fix at the shared point, and a stop after three failed fixes.
- `review-security`: a six-part bar for a finding, three verdicts, severity capped by shown impact, and a full audit with a ledger and refuting verifiers.
- `references/machine-tells.md`, `references/ui-quality.md`, `references/shipping.md` and `references/security-attack-classes.md`.
- `references/research-sources.md`: the eight source types, engineering blogs to target, access workarounds, the sub-agent and fact-check prompts, the authority score, and the report shape.

### Changed
- `evals` checks the baseline has room to move before a comparison (micro-tested in `evals/evals-near-ceiling`: 3 of 5 runs with the skill against 1 of 5 without, Opus 5.5 on 2.1.286). `engineering-principles` links correct by construction to one status field over contradictory flags. `scripts/lint-skills.py` now checks reference paths inside subfolders, such as `references/system-design/index.md`.
- Pages (artifacts) stay tight: about 1,100 visible words, diagrams and Now versus Fix panels carry the explanation, at most two sentences under each diagram, no lede, no recap and no conversation history. Each point gets a collapsed "Explain simply" dropdown with its plain-words version (not counted in the budget), and each item is reviewed for value before it earns a place. New section "Length: diagrams carry the page" in `visual-explanations`, pointers in `writing-voice`, `explainer-pages` and `explain-simply`.
- From the make-slides ledger, shared rules go where they belong: no decorative pictures and a charts and screenshots section (`visual-explanations`), same-renderer previews and working links (`preview`), no centred paragraphs and 3:1 for meaningful graphics (`ui-quality`), two new tells (`machine-tells`), situation then change then answer, and the cost of doing nothing (`writing-voice`), bad news first and stories only from the user (`respect-human-attention`), and yardsticks and verbatim quotes (`explaining`).
- `engineering-principles`: errors never go silent. A key error records its failure where the data would have been, logs, and reaches a human through the repo's existing alert route. A non-key error only logs.
- `explain-simply`: end a step-by-step walk with what the facts mean for the decision, and draw the boundary when the question is who can reach what.
- `ui-quality` and `design-ui` add what good-css.com and seven public design skills check that ours did not: 16px inputs and no zoom lock, long unbroken text, sticky and full-height layouts, unclipped overlays and native dialog and popover, `color-scheme`, token-pair contrast, outline focus rings, keyboard overlays and live regions, hover only on hover devices, fields that keep their size, a pause control for motion, axe-core, settled captures, and a fresh reviewer for the finished screen.
- Trigger tests are measured with `claude plugin eval`: seven cases in `evals/` pit neighbouring skills against each other (design-ui, qa-live-site, review-product-page, review-pr, review-plan, explain-simply, write-tech-doc). Baseline on 2.1.286 with Opus 5.5: 21 of 21 runs right.
- README: name the case the model would do alone, end the turn where a spec or plan ends, keep the reason in every rationalisation row, put the must-survive rule first, and isolate eval runs outside any git repo.
- `use-your-judgement` and `stop-decide-hold` merge into `references/judgement.md`. Reference headers lose their "Applied by" lines, which kept going stale.
- write-spec, write-plan and review-plan point at `writing-voice` and `visual-explanations` instead of restating them. Settled: open items in a doc carry the user's preference, not the agent's pick; a working spec runs to 3 pages and the team's review page 1 to 2; an explainer walks steps first for a new reader and shows the map first to someone judging a design; a PR body is full sentences, then Evidence and Merge danger.
- The linter allows `license` and `disable-model-invocation`, and fails on an unescaped `$ARGUMENTS` in a body.
- `use-your-judgement` opens with the test every piece of work must pass: it moves the user's goal forward or removes a blocker, or it is parked.
- `references/explaining.md` is the one home for how to explain (ground up, an example per claim, decisions side by side, questions answered where they arise, and the devices that landed with real readers). `explain-simply` drops from about 2,700 words to 1,400 and `understand-codebase` loses its drifting copy of the same rules. `preview.md` says a Markdown document in a repo needs only its diagrams parsed and one rendered read.
- Every pipeline skill takes what held up from eight public skill repos: see `docs/references.md` for each idea's source and what was refused. `testing` gains a claim and evidence table; `engineering-principles` a ladder, a never-cut floor and keep or revert performance work; `handoff-protocol` what a reviewer receives; `visual-explanations` a form chooser, a budget and diagram grammar; `write-spec` interviews in rounds.
- `qa-live-site` and `split-commits` now carry `references/`.
- `respect-human-attention` covers the systems a skill designs: list every human touchpoint, ask a person only when a machine can't decide, in a place they already work, with evidence attached. `write-tech-doc` and `explain-simply` now apply it.
- `explain-simply` and `write-tech-doc` add one page shape for designs with a handful of parts: problem first, a big-box map, nested layers per part, one real case through every section, and state diagrams for lifecycles. Marked as one shape among several.
- `research-prior-art` adds an exhaustive per-company sweep (inventory every post from sitemaps, feeds and GitHub before reading, then read each in full), checks that each citation points at the right page, and ends reports with numbered references and every source grouped by company, both collapsed.
- `research-prior-art` maps a whole landscape: a confirmed brief, one parallel sub-agent per source type, merge by idea, a mandatory fact-check agent, authority badges counted by organisation, and a step-by-step report.
- Skills carry real copies of `references/` instead of symlinks, so a single skill folder works on its own. `scripts/sync-references.sh` regenerates the copies, and a CI check fails when one is stale.

## [0.1.0] - 2026-09-18

### Added
- Sixteen skills, built from prompts in daily use and generalised.
- `references/handoff-protocol.md`, the rule the pipeline is shaped around.
- `references/engineering-principles.md` and `references/writing-voice.md`, each the single home for text that was previously copied into four and six prompts.
- `docs/references.md`, recording what was taken from other harnesses and what was refused.
