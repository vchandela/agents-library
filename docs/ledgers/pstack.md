# pstack rule ledger

Every distinct rule in pstack Part 1 and Part 2, sorted against this library. The sources are Lauren Tan's public threads, [Part 1](https://x.com/poteto/article/2094457600259842065) and [Part 2](https://x.com/poteto/status/2097732320606507506), read on 22 November 2026, with two independent write-ups used to check the reading. A row says what the source claims, how strong the evidence is, and where it landed here.

Totals: 51 rows. TAKEN 31, COVERED 6, GAP 1, REFUSE 13.

Key to the columns:

- **source**: p1 = Part 1, p2 = Part 2, trial = the internal trial run that proved the method and supplied the one must-fix.
- **evidence**: measured (numbers published with a method), described (a write-up or method, no numbers), claimed (an assertion with no method), added (this library's own addition from the trial).
- **verdict**: TAKEN (in a new or edited file here), COVERED (already in the library), GAP (worth having, not built), REFUSE (left out, with the reason).
- **where**: the file and section that carries it.

pstack calls its reusable playbooks "playbooks"; this library calls them skills, and the ledger uses the library's word.

---

## 1. Part 1, verification

| # | rule | source | evidence | verdict | where |
|---|---|---|---|---|---|
| V1 | Faster generation moves the bottleneck to verification, so the agent needs hands and eyes: it must run the app and see its change. | p1 | described | TAKEN | `references/verifying-apps.md`, opening and The loop. |
| V2 | The verification skill is project-local and maintained, not rebuilt per task. | p1 | described | TAKEN | `skills/verify-app/SKILL.md`, Before the first run. |
| V3 | Build the lever: one small CLI reused by every run, instead of one-off scripts. | p1 | described | TAKEN | `references/verifying-apps.md`, The CLI is thin. |
| V4 | The CLI exposes doctor, open, snapshot, screenshot, click, type, press and wait-settle as composable commands. | p1 | described | TAKEN | Same section, as `doctor`, `open` and `snapshot`, with click, type, press, settle, trace and screenshot flags. |
| V5 | A deep command surface hides the browser, auth and launch machinery; the agent keeps the judgement. | p1 | described | COVERED | `references/engineering-principles.md`, "Deep modules". |
| V6 | Destructive commands support a dry run; output has a machine mode and errors name the fix. | p1 | described | TAKEN | `references/verifying-apps.md`, The CLI is thin (`--dry-run`, `--json`, errors name the failing step). |
| V7 | The feature map carries, per feature, what it does, how a user reaches it, how to drive it and its traps. | p1 | described | TAKEN | `references/verifying-apps.md`, The feature map is generated, never typed: the route, what it does, how a user reaches it, the CLI command and flags that open and drive it, the role or fixture and its traps. |
| V8 | The map is materialised memory: a compact projection of the codebase that saves tokens. | p1 | described | TAKEN | Same section: the map is a compact copy of the app's surface, kept because reading every route and page on each run costs more than keeping the map current. |
| V9 | Keep the map current on a regular cadence. | p1 | described | TAKEN | Same section and The upkeep cost, without the source's daily cadence. |
| V10 | Run verification with cloud agents because worktrees stop scaling after about ten on one laptop. | p1 | claimed | REFUSE | Vendor and a number. This library isolates in worktrees and stays host-neutral. |
| V11 | Use a browser debug protocol for web and a simulator for iOS. | p1 | described | REFUSE | Vendor and platform specifics; the skill says "the project's browser fixture". |
| V12 | Add formal verification with a state model, model checker and statechart. | p1 | described | REFUSE | A second method with its own tooling; out of scope for the first version. |
| V13 | Verification lets non-engineers check that a change works. | p1 | claimed | REFUSE | A benefit, not an action an agent can take. |
| V14 | The method supports 2,000 pull requests a month (elsewhere 2,500). | p1 | claimed | REFUSE | No method, and the figures disagree. Recorded in `docs/references.md`, Refused. |
| V15 | If the runtime is thin, build debugging tools or choose a stack that already provides them. | p1 | described | TAKEN | `skills/verify-app/SKILL.md`, Before the first run: if the project has no tooling, say so and build the smallest pair. |

## 2. Part 2, research and planning

| # | rule | source | evidence | verdict | where |
|---|---|---|---|---|---|
| A1 | Two failures dominate: underspecified intent and missing context. | p2 | described | COVERED | `references/agent-prompts.md`, Outcome and Evidence sections. |
| A2 | Indirect prompting: ask the agent to restate the problem in its own words before it writes code. | p2 | described | TAKEN | `references/agent-prompts.md`, Indirect prompts. |
| A3 | The restatement compresses a noisy thread and exposes a misunderstanding at the cheapest point. | p2 | described | TAKEN | Same section. |
| A4 | Trace how a subsystem works before designing around it, in parallel for a system that spans services. | p2 | described | COVERED | `understand-codebase`, Map before you read and Output. |
| A5 | Search the why in git history, pull-request comments, tickets, docs, chat, monitors and error logs. | p2 | described | TAKEN | `understand-codebase`, Find the why beyond the code. |
| A6 | Teach the result back, so the human and the agent share a model. | p2 | described | TAKEN | `write-plan`, Teach the implementation; `review-plan`, Follow it cold. |
| A7 | Reload context from past transcripts so a fresh agent can continue. | p2 | described | COVERED | `analyze-agent-transcripts`. |
| A8 | Write the intended usage (README or tutorial) before the implementation, then work backwards. | p2 | described | TAKEN | `references/diataxis.md`, README first. |
| A9 | Separate tutorial, how-to, reference and explanation, and do not mix them. | p2 | described | TAKEN | `references/diataxis.md`, the whole reference. |
| A10 | For an open design question, build two or three throwaway variants behind a switcher. | p2 | described | TAKEN | `skills/prototype/SKILL.md`, Two or three variants. |
| A11 | Drive each variant with the verification skill, capture screenshots and measure timing or layout. | p2 | described | TAKEN | `prototype`, Build where you can see it. |
| A12 | The two mistakes are accepting the first design and over-elaborating an abstract plan without evidence. | p2 | described | TAKEN | `prototype`, Rationalisations to refuse. |
| A13 | Ground a cross-cutting design in how the affected systems work and why they are shaped that way. | p2 | described | TAKEN | `skills/architect/SKILL.md`, Ground the brief. |
| A14 | Run candidate designers in parallel, from different model families where possible. | p2 | described | TAKEN | `architect`, Run independent candidates. |
| A15 | Each candidate drafts call-site usage, core types, public signatures and its rationale. | p2 | described | TAKEN | Same section, the design package. |
| A16 | A judge on a different model scores the candidates against a strict rubric. | p2 | described | TAKEN | `architect`, Cross-judge. |
| A17 | Implement against the sketch and surface every mismatch between sketch and code. | p2 | described | TAKEN | `architect`, Sketch the call sites and types and Order the implementation. |
| A18 | Repeated workarounds, `any` or forced casts are evidence the architecture is wrong; scrap and restart. | p2 | described | TAKEN | `architect`, Scrap when the evidence says so. |
| A19 | Write the multi-phase plan after the design settles; every task names its proof; work is verified after the code runs. | p2 | described | TAKEN | `write-plan`, Every step names its proof. |
| A20 | The plan is deleted when the work lands. | p2 | described | TAKEN | `write-plan`, the Temporary plan rule, with a date or trigger instead of "when it lands". |
| A21 | Deliver in small, reviewable pull requests, item by item. | p2 | described | COVERED | `split-commits` and `references/shipping.md`. |
| A22 | An automated script checks the plan's structure. | p2 | described | GAP | No plan linter here; the lint checks skills, not plans. A candidate for a later tool. |
| A23 | Avoid adversarial review of abstract plans, because agents invent theoretical risks. | p2 | claimed | REFUSE | This library keeps `review-plan` by design; the real fix is to prototype before the plan, which is taken in A10. |
| A24 | Playbooks are reference files inside a router and load conditionally; there were 23 at one version. | p2 | described | REFUSE | The library's unit is a skill with references; a router layer and a count are not portable rules. |
| A25 | A pinned mode keeps the router always applied. | p2 | described | REFUSE | Persistence belongs in a hook; a skill fires when relevant. |
| A26 | The router invokes playbooks automatically. | p2 | described | REFUSE | Skill descriptions are the trigger here; no router. |
| A27 | The workflow supports 2,500 pull requests a month, and trust unlocks volume. | p2 | claimed | REFUSE | An unverified volume claim; the library measures evidence per change, not volume. |
| A28 | Vendor choices: named cloud agents, chat bots, editors and model slugs. | p2 | described | REFUSE | Host-specific. "A different model family where the setup allows" keeps the idea portable. |
| A29 | "I don't believe in planning." | p2 | claimed | REFUSE | As stated it conflicts with the pipeline. What survives is plan-through-code: prototype and architect before `write-plan`. |
| A30 | Optimise cost per unit of intelligence, assuming tokens get cheaper. | p2 | claimed | REFUSE | An economic forecast, not an action. |
| A31 | Use evals to shorten a skill, moving explicit commands into the CLI. | p2 | described | COVERED | `evals` and the README's writing-a-skill process. |

## 3. Added from the trial run

| # | rule | source | evidence | verdict | where |
|---|---|---|---|---|---|
| T1 | The feature map is generated from the app's routes and pages, never hand-typed, and the sweep's page list comes from the map. | trial | added | TAKEN | `references/verifying-apps.md`, The feature map is generated, never typed. This was the trial's one must-fix. |
| T2 | A structural self-check covers sideways scroll, clipping, wrapping, row heights and overlap at every supported width. | trial | added | TAKEN | Same reference, The structural self-check. |
| T3 | Every finding becomes a test that is seen red without the fix and green with it. | trial | added | TAKEN | Same reference, Every finding becomes a test. |
| T4 | Before any connection, refuse to run unless every declared integration, including the database, is local; scan the app's config keys, and treat an undeclared key or integration as production. | trial | added | TAKEN | Same reference, The production guard: an integration manifest plus a config-key scan, the app launched from the checked environment, and no bypass flag. |
| T5 | Record before and after on the same route, viewport, fixture and input; name the upkeep cost of the map, CLI and guard. | trial | added | TAKEN | Same reference, Before and after and The upkeep cost. |

## Sources

- [pstack Part 1, Verification Is All You Need](https://x.com/poteto/article/2094457600259842065), Lauren Tan, read 22 November 2026.
- [pstack Part 2 thread](https://x.com/poteto/status/2097732320606507506), Lauren Tan, read 22 November 2026.
- Independent write-ups used to check the reading: [Barnaby Robson's catalog](https://barnabyrobson.org/on-pstack/) and [the Part 2 thread mirror](https://threadnavigator.com/thread/2097732320606507506/).
