# evals rule ledger

Every distinct rule or idea in the research for the evals skill, sorted against our material in `~/oss/agents-library`. The inputs were the research files `hamel.md`, `labs.md`, `repos.md` (which holds parts A to D in full; the four part files add no line that is not in it), `frameworks.md` and `branches.md`. The fact-check files `factcheck-1.md` and `factcheck-2.md` override them: where a fact-check corrected a finding, the row uses the corrected version and says so.

Totals: 846 rule rows, plus 30 rows of contradictions between sources (section 9). COVERED 79, TAKEN 481, GAP 89, REFUSE 197. Of the GAP rows, 42 say "Merged into" another row, so the skill lacks 47 distinct rules; 11 of those have measured evidence and are listed at the end. Two COVERED rows are merges too.

Key to the columns:

- **sources**: hamel = Hamel Husain (blog, FAQ, evals-skills, cartwheel course), shreya = Shreya Shankar (papers and blog), parlance = the Parlance Labs auto-evals study (Saha and Husain), anth = Anthropic (blog, docs, claude-api eval guides, `claude plugin eval`, skill-creator), oai = OpenAI, google = Google ADK and Vertex, tob = trailofbits/skills, sp = obra/superpowers and superpowers-evals, wsh = wshobson/agents, asio = agentskills.io, aws = aws-samples skill eval, lf = Langfuse, opik = Opik, dd = Datadog, arize = Arize, bt = Braintrust, ls = LangSmith, nb = nullbench, edd = eval-driven-development, lat = Latitude, smash = smashilp, sf = SkillForge, neo = NeoLab, sman = simple-man, he = harness-evolver, esk = eskill, sky = skystmm, notion = openai/skills notion evaluations, cct = cc-thinking-skills, oj = OpenJudge, n8n = n8n, day = daymade, must = mustflow, gepa = GEPA, rsc = rsc-harness, novu = novu, mcpj = MCPJam, cal = Calibre reforge, bdf = bdfinst, ecc = affaan-m/ECC, inspect = UK AISI Inspect, promptfoo, deepeval, ragas, mlflow, tau = tau-bench and tau2-bench, swe = SWE-bench, stats = the statistics papers (Anthropic Nov 2024, Miller, Bowyer et al., Thinking Machines), mon = monitoring sources, safety = safety sources (AgentDojo, Nasr et al., OWASP, Willison), cost = cost sources (Kapoor, HAL, Thakur, Verga, provider docs).
- **evidence**: measured (numbers published), described (a write-up or method, no numbers), claimed (an assertion with no method). This follows `references/research-sources.md` "Authority score". A row takes the strongest evidence among its sources.
- **verdict**:
  - **COVERED**: already in a reference that existed before this work (`testing.md`, `judgement.md`, `engineering-principles.md`, `research-sources.md`, `untrusted-input.md`, `security-attack-classes.md`).
  - **TAKEN**: in the new `skills/evals/SKILL.md` or `references/evals.md`. "Partly" says which half is in.
  - **GAP**: not in our material and not refused. A candidate for the next edit; the "where" column proposes the place.
  - **REFUSE**: left out, with the reason.
- **where**: SKILL means `skills/evals/SKILL.md`, REF means `references/evals.md`. A `§` number is the SKILL step, and `L` is the line in the file today.

A rule found in several sources gets one row, in the section of its first or strongest source, and the sources column lists all of them. When a later source repeats a rule already listed, its section names the row it merged into instead of repeating it.

---

## 1. Hamel Husain and Shreya Shankar (hamel.md)

### 1.1 Error analysis

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H1 | Error analysis comes before any evaluator; it decides what to measure. | hamel, opik, lat, ls, oai | measured (Nurture Boss, H23) | TAKEN | SKILL §1 L24: "No grader, metric or synthetic case before a person has read real outputs." |
| H2 | Open coding: a domain expert writes free-text notes on each trace, with no categories yet. | hamel, opik, lf | described | TAKEN | SKILL §1 L27: "The human writes the notes ... One line per failure, in the human's words." |
| H3 | Note only the first upstream failure in a trace, because later errors cascade from it. | hamel, opik, lat, mcpj | claimed | GAP | SKILL §1, as one clause. Cheap, and it keeps counts honest; see H19 for the counting side. |
| H4 | Axial coding groups the notes into failure modes, then counts each mode. | hamel, wsh | described | TAKEN | SKILL §1 L27-28: "group notes into failure modes ... The modes, with counts, are the eval's scope." |
| H5 | The human annotates at least 30 traces before the agent suggests anything, so its guesses cannot bias the human. | hamel (FAQ) | claimed | TAKEN | SKILL §1 L27 took the course skill's gate (about five notes per mode) instead. See X1. |
| H6 | Review at least about 100 traces, and keep going while you are still learning. | hamel, opik, wsh | claimed | TAKEN | Partly. SKILL §1 L26 says 30 to 100 and stops at saturation (L28) rather than at a floor. See X2. |
| H7 | Stop rule: about 100 traces reviewed and no new failure type in the last 20. | hamel, opik, lat | claimed | TAKEN | SKILL §1 L28: "Stop when new traces stop adding failure modes." The numbers were not copied. |
| H8 | Course stop check: count new consequential modes in a final uniform batch of 15. | hamel (HW4) | described | REFUSE | A second wording of the saturation rule in SKILL §1 L28; one rule is enough. |
| H9 | Course sampling recipe for 100 traces (15 random, 15 cluster representatives, 30 on one dimension, 25 from depth searches, 15 random). | hamel (HW4) | described | REFUSE | A course recipe. SKILL §1 L26 keeps the general rule: random plus the known failures. |
| H10 | Two notes are one mode if one fix corrects both, and two modes if the fixes differ. | hamel (review-loop L37), lat ("cluster by cause") | described | GAP | SKILL §1, as the merge test for grouping notes. |
| H11 | Write observations, not explanations ("SQL missed the budget constraint", not "the model didn't understand"). | hamel, opik, lf | claimed | GAP | SKILL §1 L27, one clause in the note rule. |
| H12 | Record every problem that makes the product less useful, even when it is not the model's fault. | hamel | claimed | TAKEN | Implied: SKILL §1 L27 asks for one line per failure, with no limit to model failures. |
| H13 | Aim for 5 to 10 failure categories (course 5 to 8, wshobson 4 to 8, Latitude 3 to 8). | hamel, opik, wsh, lat | claimed | REFUSE | An arbitrary count, against `engineering-principles.md` L7 (zero, one or infinity). The count is whatever saturation gives (SKILL §1 L28). |
| H14 | Each mode has a definition contract: a name, a yes/no definition, 3 or more positives, 3 or more close negatives, the boundary against its nearest mode, the evaluator type and the spec line. | hamel (HW4), neo (contrast pairs) | described | GAP | REF, a short "One failure mode" block next to "One item". The close negatives and the boundary are what make a judge checkable. |
| H15 | Agents group only what the human wrote, never add a mode from their own reading, and record which notes each mode came from. | hamel (cartwheel review-loop, a reference file per factcheck-1 #33) | described | TAKEN | SKILL §1 L27. |
| H16 | Breadth then depth: after about 5 annotated records, one sub-agent per mode scans all records for more examples (the gate was lowered from 10 to 5 in commit 9f3b835). | hamel (evals-skills review-loop L41) | described | TAKEN | SKILL §1 L27: "search for more examples of a mode only after about five human notes on it." |
| H17 | Agent suggestions favour recall; the human accepts or dismisses each one, and a suggestion is never a label until accepted. | hamel | claimed | TAKEN | Implied by SKILL §1 L27 ("The human writes the notes; the agent organises them"). |
| H18 | Report both first-failure counts and any-instance counts, because first-failure counting undercounts late modes. | hamel (cartwheel review-loop L71) | described | GAP | SKILL §1 L28, with H3. |
| H19 | Fractions from an enriched sample are sample fractions, not prevalence. | hamel (HW4, HW7) | claimed | TAKEN | Partly. REF "Checking a judge" item 5 says the corrected rate holds only on a random sample; the general warning about counts is not written out. |
| H20 | Fix obvious problems (spec gaps, prompt gaps, missing tools, bugs) before building an evaluator; only failures that persist get one. | hamel, opik, lat | claimed | TAKEN | Partly. SKILL §1 L28 lets a mode go without a check given "a stated reason it doesn't"; "fix it first" is not said. |
| H21 | Re-run error analysis after every significant change; 100 fresh traces every 2 to 4 weeks and 10 to 20 outliers weekly. | hamel, opik | claimed | REFUSE | The cadence numbers are guesses. `judgement.md` L22 sizes passes to the decision; SKILL §6 L82 keeps production failures flowing in. |
| H22 | Nurture Boss: three issues were over 60% of problems, and date handling went from 33% to 95%. | hamel | measured (one case, no method) | TAKEN | Supports H1. The number is not cited: one case without a method, while SKILL cites Shankar and Shopify. |

### 1.2 Automating error analysis

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H23 | One-shot automated error analysis recovers most human-flagged failures (recall 74.4 to 87.2%, precision 77.4 to 91.0% on 100 traces with 39 labelled failures) but misses failures that need product context. Authors are Saha and Husain; one dataset cannot rank vendors. | parlance | measured | TAKEN | SKILL §1 L27 and the rationalisation row L100 ("It can organise a human's notes. It can't replace reading them."). |
| H24 | Every tool missed the same class (objection handling, Markdown in SMS, interruptions, missed handoffs): failures not visible in the trace alone. | parlance | measured | TAKEN | Same place as H23. |
| H25 | What would have helped most was the tool interviewing the human for context. | parlance | described | TAKEN | Superseded by design: in SKILL §1 the human reads the traces, so the context is there. |
| H26 | Agents doing open coding paraphrase: codes per tweet tracked tweet length at rho 0.81 in exp1, but only 0.15 when the human gave free-text memos. Codes were nearly all single-use in free conditions, but only 4.5% single-use against a predefined category set (corrected per factcheck-1 #35). | shreya | measured (451 tweets, one author, a blog post) | TAKEN | SKILL §1 L27: "Agents left to label on their own paraphrase ... they reuse labels well only against a fixed category list." |
| H27 | Agents stop early: coverage was 67.8% at best, 5.5% at worst, and 25.3 to 30.6% in the rest. The "68% of 451" quote is a paraphrase. | shreya | measured | TAKEN | SKILL §1 L27: "cover a fraction of the data". |
| H28 | New feedback should trigger re-coding of earlier items under the new reading ("You've found 3 new failure modes since you reviewed records 0 through 5. Worth a second pass."). | shreya, hamel (review-loop L65) | described | GAP | SKILL §1 L29, next to criteria drift: when a new mode appears, recheck the traces read before it. |
| H29 | Axial taxonomies differ across runs, and vague categories are unfalsifiable. | shreya | described | TAKEN | Implied: SKILL §3 L47 asks every check to be a checkable claim. |
| H30 | People tire after about 10 items per review round; highlighting a phrase is easier than naming a code. | shreya | described (n=1) | REFUSE | One person's experience, about review-tool ergonomics. |
| H31 | Never delegate initial open coding, taxonomy validation, ground-truth labels or root-cause analysis to a model. | hamel, smash, lf | claimed | TAKEN | SKILL §1 L27 and §2 L35. |
| H32 | Hamel's review of Anthropic's eval workflows: it starts with an eval before looking at data, labels in chat or Markdown, and one evaluator bundled four failures. The real commands are `/claude-api build-eval` and `/claude-api hillclimb` (factcheck-1 #7). | hamel | described (one livestream) | TAKEN | SKILL order: data first (§1), then one judge per mode (§3 L47). |
| H33 | Chat and Markdown files are the wrong place to label; build a web app. | hamel | claimed | REFUSE | A tool choice. The rule underneath (read the whole trace with its context) is SKILL §1 L26. |
| H34 | Be wary of an agent that writes the rubric and then scores against it. | hamel, nb (graders from treatment answers) | claimed | TAKEN | SKILL §2 L35 (answer key from the world) and §4 L59 (label first, then build the judge). |
| H35 | In a non-interactive run, never claim the review loop ran. | hamel | described | COVERED | `testing.md` L93: "List only commands you ran." `engineering-principles.md` L99: "Never present a number you did not measure." |

### 1.3 Shape of the failure taxonomy

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H36 | Categories are grounded in the application ("missing query constraints"), never generic ("helpfulness", "coherence"); generic metrics only sort traces to read. | hamel, opik, edd, lat, dd | claimed | TAKEN | SKILL §3 L47 (checkable claims per failure mode) and §1. |
| H37 | One yes/no column per mode per trace. | hamel | described | TAKEN | SKILL §3 L47. |
| H38 | The agent keeps a running taxonomy file with counts, example ids, quotes and source notes. | hamel | described | REFUSE | A file format. SKILL §1 L28 keeps the modes with counts; the rest is tooling. |
| H39 | Worked support-agent mode `unconfirmed_write`: the reply says a write succeeded but the last tool result does not confirm it. | hamel (HW4) | described | REFUSE | A domain example. REF "One item" carries our own examples. |
| H40 | Compare with a published taxonomy only after yours stabilises, and add a mode only if your traces show it. | hamel (HW4) | claimed | REFUSE | Optional extra. SKILL §1 already takes modes only from the traces read. |

### 1.4 Yes/no versus scales

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H41 | Yes/no over a 1 to 5 scale: it forces a decision, and scale midpoints hide doubt and need more samples. | hamel, wsh, opik, oj, smash, arize, cal, he | claimed | TAKEN | SKILL §3 L47: "never a 1 to 5 score". |
| H42 | Track gradual progress with several yes/no sub-checks ("4 of 5 expected facts"), not a scale. | hamel, smash | claimed | TAKEN | SKILL §3 L47: "A multi-part answer gets several yes/no checks, not partial credit." |
| H43 | For severity, use several yes/no judges ("factually wrong", "dangerously wrong"), not an ordinal scale. | hamel, opik | claimed | TAKEN | Implied by SKILL §3 L47 (one judge per failure mode). |
| H44 | Combine checks into a "passes every check" rate with drill-down, and group by severity (release-blocking or tolerable); aggregation follows the question. | hamel, anth (eval-audit L165), oj (gate aggregator), must | described | TAKEN | Partly. SKILL §6 L78 makes any failure on a regression item block. A written "aggregate by fail-on-any for high-stakes modes" is not there; see V34. |
| H45 | A 1 to 5 scale is fine for fuzzy ranking during dataset curation. | hamel (evaluate-rag) | claimed | REFUSE | A curation helper, not a measurement. |
| H46 | Attune: for tasks that are scores by nature, pairwise comparison plus derived rules gives more consistent scores than pointwise prompts (3 to 17 points over a GEPA-tuned baseline). | shreya | measured (user studies n=12 and n=8) | TAKEN | SKILL §3 L47: "A scale is only for comparing two outputs side by side." |
| H47 | Abstention is yes/no too: a balanced set of answerable and unanswerable questions, and a pass needs both behaviours. | hamel, anth, ls | described | TAKEN | SKILL §2 L40, trap 3 ("No negatives"). |

### 1.5 Judge design

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H48 | One failure mode per judge; the most common mistake is a judge that checks many things. | hamel, anth, opik, dd, ragas, smash, lat, ls | described | TAKEN | SKILL §3 L47; REF "Grader hygiene" L31. |
| H49 | Exhaust code checks first; many "subjective" modes reduce to keywords, a regex or an API call once you know the domain. | hamel, anth, opik, dd, bt, lat, cal, oj | claimed | TAKEN | SKILL §3 L46: "Code checks first, wherever the property is exact." |
| H50 | A judge prompt has four parts: the one criterion, written pass and fail definitions, a few labelled examples from the train split (one pass, one fail, one borderline), and structured output with the reasoning before the verdict. | hamel, opik, oj, lat, ls, cal, rsc, arize | claimed (the 15 to 25% gains quoted by Hamel and NeoLab have no data) | GAP | REF "Grader hygiene", one bullet. Today REF has the yes/no question and the "unknown" exit but not the definitions, examples or reasoning field. See X22 for the borderline-example dispute. |
| H51 | Critiques should be detailed enough for a new employee to follow. | hamel | claimed | REFUSE | Style advice, folded into H50. |
| H52 | Example critiques in the prompt raise judge agreement by 15 to 20%. | hamel | claimed ("I've found", no data) | REFUSE | No data shown; not cited. |
| H53 | Give each judge only the parts of the trace it needs (extra context causes context rot), and calibrate it on exactly the inputs it will get when deployed; a judge fitted on evidence the deployed one cannot reach scores well locally and is useless. | hamel, opik, deepeval, neo, smash, lf, dd (fidelity gap) | described | GAP | REF "Checking a judge", one item: the judge's inputs are part of what is frozen and checked. |
| H54 | The graded output can't instruct the judge: tell it not to follow instructions quoted in the trace. | hamel, dd, inspect | described | TAKEN | REF "Grader hygiene" L32 (delimiters, neutralised); `untrusted-input.md` L3. |
| H55 | Keep human labels, reviewer notes and scenario metadata out of the judge's input; they leak the answer. | hamel, dd, smash, lf | described | GAP | REF "Grader hygiene", one bullet. SKILL §3 L51 keeps keys from the agent, not labels from the judge. |
| H56 | Start with the most capable judge model; the same model as the app is fine as judge. | hamel, opik | claimed | REFUSE | The same-model half conflicts with REF L30 (a different model from the one under test), which rests on ToB's self-preference rule, Inspect and the Anthropic platform docs. See X11. |
| H57 | Pin dated model snapshots for judges, never a floating alias. | hamel, wsh, lat, anth, oj, lf | claimed | TAKEN | SKILL §6 L83; REF "Grader hygiene" L30. |
| H58 | A different model behind the same prompt is a different judge; re-validate it. | hamel, smash, ls, cal | claimed | TAKEN | SKILL §4 L63: "A change to any of them is a new judge, rechecked." |
| H59 | Read the disagreements by hand before any automated prompt tuning. | hamel | claimed | GAP | Merged into H72. |
| H60 | "Find all errors and keep improving" is too vague for an agent tuning a judge. | hamel | claimed | TAKEN | Implied by SKILL §0 L18 (the pass rule is written first). |
| H61 | Stop tuning the judge prompt after a couple of revisions with no gain, and collect more labels or widen the search instead (Hamel: two revisions; EDD: two on the same red judge; OpenJudge: three with no kappa gain above 0.03). | hamel, edd, oj | described | COVERED | `judgement.md` L30: stop when "the last two searches, reads or passes changed no decision". The fixed counts were not copied. |
| H62 | Treat any evaluator, a model or not, as a classifier. | hamel | claimed | TAKEN | SKILL §4 L57; REF "Checking a judge" L40. |
| H63 | Developers trust model-based assertions less than code ones and want to read the code (EvalGen). | shreya | measured (qualitative, n=9) | TAKEN | Supports SKILL §3 L46. |

### 1.6 Checking a judge against people

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H64 | Split the labels train 10 to 20%, dev 40 to 45%, test 40 to 45%, with balanced classes even when production is skewed. | hamel, opik, smash | described | TAKEN | SKILL §4 L60 takes the three-way split; the percentages were not copied. See X6. |
| H65 | Run the test set once; dev numbers are optimistic, and overfitting happens even when dev items never enter the prompt. | hamel, opik, wsh, dd | claimed | TAKEN | SKILL §4 L60; REF "Checking a judge" item 2. |
| H66 | Report the two rates, never raw accuracy or Cohen's kappa for judge against truth; kappa is for two humans. | hamel, opik, wsh, smash, oj | claimed | TAKEN | SKILL §4 L61: "Never raw percent agreement." REF items 3 and 4. |
| H67 | Acceptance bar: both rates above 90% (80% minimum). The course says "Do not require numerical acceptance targets." | hamel | claimed | TAKEN | At 0.8 on both, advisory below (SKILL §4 L62). See X4. |
| H68 | How many labels: 20 and 20, about 50 and 50, 100 to 200 per mode, or at least 30 and 30, depending on the file. | hamel | claimed | TAKEN | At 10 per verdict in dev to start and about 50 of each per mode to gate (SKILL §4 L59). See X5. |
| H69 | Report Wilson 95% intervals on both rates: 16 of 20 is 0.80, with an interval of about 0.58 to 0.92. | hamel (HW5), dd | described (worked arithmetic, rechecked here) | TAKEN | SKILL §4 L61; REF "Checking a judge" item 3. |
| H70 | Correct an observed pass rate for a known judge with Rogan-Gladen, clip to 0..1, treat it as invalid when the two rates sum near 1, and add a bootstrap interval. | hamel, opik, wsh, lat | described (standard statistics) | TAKEN | REF "Checking a judge" item 5. Clipping and the bootstrap were not copied; the `judgy` package is tool-specific. |
| H71 | "Improving TPR narrows the confidence interval more than improving TNR." | hamel (validate-evaluator L206), opik | claimed | REFUSE | Not general (factcheck-1, section H): the denominator is symmetric in the two rates, and which one's error dominates depends on prevalence. |
| H72 | For each judge-human disagreement, decide which is wrong: the judge (fix the prompt), the label (fix it and recompute), or the definition (sharpen the boundary). Group debatable labels for the user to revisit. | hamel, oj, dd, lat, lf, cal, smash | described | GAP | SKILL §4, one bullet after the split. Today the skill measures the rates but says nothing on what to do with each miss. |
| H73 | Alignment stalls: both rates low means a better model; both plateau means decompose the criterion; inconsistent labels means fix the rubric. | hamel | claimed | GAP | Merged into H72. |
| H74 | One expert labels (a "benevolent dictator"). With several labellers, measure their agreement on 20 to 50 shared traces and resolve contested rows rather than averaging or taking the newest. | hamel, lat, opik, dd | measured (Shopify's experts agreed at kappa 0.69; Nova Escola's labellers agreed less often than chance) | GAP | SKILL §4 L59: say who labels, and that labellers who disagree are a finding about the criterion. |
| H75 | Honeycomb: three prompt iterations to over 90% agreement with the expert. | hamel | measured (one case) | REFUSE | Not cited: one case. SKILL cites Shopify (§4 L57). |
| H76 | Agreement is specific to each criterion; people want a different false-fail limit per criterion (EvalGen). | shreya | measured (qualitative) | TAKEN | SKILL §4 L59: the bar and the label count are per failure mode. |
| H77 | EvalGen, where a human picks the criteria, beat fully automatic SPADE: fewer assertions, and coverage from 49% to 73% on one pipeline. | shreya | measured (2 pipelines) | TAKEN | Supports SKILL §1 (the human sets the modes). |

### 1.7 Synthetic data

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H78 | Define dimensions from failure hypotheses, not arbitrary variation; start with about 3. | hamel, opik | claimed | REFUSE | Synthetic generation is left out on purpose: our agents (tickets, PRs, alerts) have real records with answer keys from the world (SKILL §2 L35). Add it when a team has no data (`engineering-principles.md` L12, YAGNI). |
| H79 | Write 20 tuples by hand before scaling with a model. | hamel, opik, smash | claimed | REFUSE | Same reason as H78. |
| H80 | Generate in two steps: tuples first, then one separate call per tuple for the query. | hamel, opik, smash | claimed | REFUSE | Same reason as H78. |
| H81 | Cross product then filter (covers edge cases) versus direct generation (realistic, misses rare cases). | hamel, wsh | claimed | REFUSE | Same reason as H78. |
| H82 | Generate inputs, never outputs or labels: the expected result comes from authoritative data (SQL, an eligibility function, a policy), never a model's answer. | hamel, oj, lf, bt, cal, rsc | claimed (correct by construction) | TAKEN | SKILL §2 L35: "The answer key comes from the world, never from a model's output." |
| H83 | Keep the answer key away from the model that writes the user's message. | hamel (cartwheel scenarios) | described | TAKEN | Implied by SKILL §3 L51 (keep the grader and keys out of view). |
| H84 | Keep a coverage pool and a challenge pool and report them apart, because the routine majority hides failures at the edges. | hamel | described | TAKEN | SKILL §2 L41: "Report ordinary and hard items separately." |
| H85 | Choose hard items because a human judged them hard, not because today's model failed them, and never split or select items by score (that measures regression to the mean). | anth (A1 post, eval-audit L187), hamel (synthetic-scenarios L64) | described | GAP | SKILL §2 L41 and REF "One item" (`flags.hard` set by a person). |
| H86 | One model call per synthetic conversation, run concurrently, then an independent critic call per conversation. | hamel | claimed | REFUSE | Same reason as H78. |
| H87 | Scripted follow-ups must make sense whatever the agent replied. | hamel | described | REFUSE | Simulated users are row F20 (GAP); this detail goes with it if it is taken. |
| H88 | Scenarios that change state target distinct records, and state is reset before each run. | hamel | described | GAP | Merged into A20 (isolate each run). |
| H89 | A pilot of about 30 scenarios must show at least 5 confirmed failures; if not, use a weaker model from the same provider. | hamel | described | REFUSE | Course numbers. The general rule is headroom (A1). |
| H90 | The human names at least two dimensions first, approves them, and reads a sample of conversations before any run. | hamel | described | TAKEN | SKILL §4 L65 (two sign-offs before any paid run). |
| H91 | Known limits: synthetic users are too cooperative, challenge enrichment inflates failure rates, scripted follow-ups cannot react. | hamel | claimed | TAKEN | Partly: enrichment is H19; simulated users are F20. |
| H92 | Synthetic data cannot tell how common a failure is in production; avoid it for specialist documents, rare languages and high stakes. | hamel | claimed | TAKEN | Implied by SKILL §1 and §2 (real data first). |
| H93 | Develop the eval with a small, cheap agent model in a synthetic world, because frontier models rarely fail there. | hamel (cartwheel README) | described | REFUSE | Specific to the course world. Headroom (A1) is the general rule. |

### 1.8 Criteria drift

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H94 | Criteria drift: people need criteria to grade outputs, and grading outputs is how they find the criteria (5 of 9 changed criteria while grading). | shreya (EvalGen), mon | measured (qualitative, n=9) | TAKEN | SKILL §1 L29. |
| H95 | Do not write a rubric before reviewing examples (at Nova Escola most rubric criteria never appeared as failures). | hamel, lat | claimed | TAKEN | SKILL §1 L24. |
| H96 | Prompt optimisers refine known failures but cannot discover new ones. | hamel | claimed | TAKEN | Implied: SKILL §1 takes modes from reading, and §6 L82 feeds production failures in. |

### 1.9 Keeping the set alive

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H97 | Retire or run less often an eval that always passes, but first try to make it harder. | hamel | claimed | TAKEN | Partly: SKILL §5 L74 drops items that pass in both arms. Making the eval harder is A1. |
| H98 | Be wary of a 100% pass rate; you are not challenging the system. | hamel, smash | claimed | GAP | Merged into A1 (headroom). |
| H99 | Scores from different versions of the item set or grader are not comparable: version the items and grader together, run against a pinned version, and make a new version instead of rewriting in place. | hamel, anth (eval-audit L121), wsh, edd, rsc, lf, ls, must | described | GAP | REF "One item": a set version recorded with every result, beside the model versions in SKILL §6 L83. |
| H100 | Prove a feared error can be triggered (red-team it once) before writing its eval. | hamel | claimed | COVERED | `testing.md` L5 (watch the test fail for the reason you expect) and `engineering-principles.md` L12 (no guard for a failure nobody has shown can happen). |
| H101 | Re-validate judges after a prompt or model change, or when production intervals widen. | hamel | claimed | TAKEN | SKILL §4 L63. |
| H102 | Drift check by adversarial validation: if a classifier tells eval data from production data at AUC 0.60 or more, the set has drifted. | hamel (2024 post) | described | REFUSE | Tooling for big sets. SKILL §6 L81 (split by time, newest items as holdout) handles a moving world at our size. |

### 1.10 CI and regression

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H103 | CI sets are small and curated and favour code checks; production uses sampled judges with intervals. | hamel | claimed | TAKEN | SKILL §3 L46 and §0 L20 (standing suite). Production sampling is M4. |
| H104 | Every new production failure becomes a case in the set. | hamel, smash, sky, ls, anth, bt, mon | claimed | TAKEN | SKILL §6 L82. |
| H105 | Run a new case 5 times: 5 of 5 makes it a regression case (any failure blocks), anything less a capability case (reported, never blocks). | hamel (HW6) | described | TAKEN | SKILL §6 L78. |
| H106 | Report pass@k for capability and pass^k for reliability. | hamel, anth, tau, must, ecc, edd | described | TAKEN | Partly: SKILL §5 L70 reports pass^k; pass@k is not named. |
| H107 | Never rerun a failed case until it passes; a completed failure is evidence. | hamel | claimed | TAKEN | SKILL §6 L79; `testing.md` L53. |
| H108 | Never change a case's class to get a wanted mix; infra errors are fixed and rerun, not classified. | hamel | described | TAKEN | SKILL §3 L49 (infra is unscored) and §6 L79. |
| H109 | Prove the gate works with a deliberate regression, then revert it. | hamel, anth (eval-audit L189), tob | described | COVERED | `testing.md` L83 ("The regression test works: It failed with the fix reverted") and L46 (mutation check). |
| H110 | Only an already checked, frozen judge runs in CI; never a new judge. | hamel | described | TAKEN | SKILL §4 L62 (below the bar a judge is advisory) and L63. |
| H111 | Check that pass@k is stable between 10 and 15 runs before trusting it. | hamel | described | REFUSE | Course-specific. SKILL §5 L71 (know the noise) covers when to trust a number. |
| H112 | Before any paid run, show the model, task count, agent runs and judge calls, and wait for approval. | hamel, anth, mcpj, bdf, tob | described | TAKEN | SKILL §4 L65 (two sign-offs before any paid run); `judgement.md` L22 (budget; going past it needs the user's yes). |
| H113 | Level 1 assertions on every change, level 2 people and models on a cadence, level 3 A/B tests after big changes. | hamel (2024) | described | TAKEN | SKILL §0 L20 (smoke check, comparison, standing suite). |
| H114 | One production example: a daily suite over 2% of traffic. | hamel | described | REFUSE | One team's setup; see M4. |
| H115 | Monitoring: estimate rates only from the uniform random sample, inspect risk groups but never use them for rates, and choose the alert threshold before looking. | hamel (HW7) | described | TAKEN | Partly: SKILL §0 L18 (the rule is written before the results) and REF item 5 (random sample). Monitoring itself is M4. |

### 1.11 Agents and multi-step runs

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H116 | End-to-end task success first (did it meet the user's goal), then step-level checks for the workflows that fail most. | hamel, oai, anth | claimed | TAKEN | SKILL §3 L48: "Grade the outcome first." |
| H117 | Step-level checks: tool choice, parameters, error handling, kept constraints, efficiency. | hamel | claimed | TAKEN | SKILL §3 L48. |
| H118 | Check tool name, arguments, result and resulting state as separate code checks, plus authorisation and preconditions. | hamel | claimed | TAKEN | Partly: SKILL §3 L48 lists the four; authorisation and preconditions are not named. |
| H119 | Transition failure matrix: rows are the last good state, columns the first failure (GenSQL to ExecSQL 12 failures, DecideTool to PlanCal 2). | hamel (FAQ) | described | REFUSE | A diagnosis tool; the skill's description sends "why did it fail" to diagnose-bug. |
| H120 | Process failures are more deterministic, so fix them first; early failures matter more. | hamel | claimed | REFUSE | Diagnosis priority, out of scope. |
| H121 | Multi-turn: pass or fail the whole session first; reproduce in a single turn to rule out conversation context. | hamel | claimed | TAKEN | Partly: session outcome is SKILL §3 L48; the single-turn repro is diagnosis. |
| H122 | N-1 testing (a real conversation prefix, test the next turn) often beats a fully simulated user. | hamel | claimed | GAP | Merged into F20 as the preferred alternative. |
| H123 | Handoffs: the trace continues until the user's need is met; log the decision, reason, context passed and wait. | hamel | claimed | REFUSE | Product logging design, out of scope. |
| H124 | Ask experts about outcomes ("Has an appointment been made?"), not implementation ("Did the tool call succeed?"). | hamel | claimed | TAKEN | SKILL §3 L48. |
| H125 | Put validators as probes at each node of a pipeline. | shreya (2024) | claimed | REFUSE | Runtime guardrail design, not an eval rule. |
| H126 | A case that changes data runs 5 times, because one success does not show reliable action. | hamel (HW8) | described | TAKEN | SKILL §5 L70 and §6 L78. |
| H127 | Coding agents: a private task suite with an environment and code tests, plus checks for over-engineering. | hamel | claimed | TAKEN | Partly: REF "One item" gives the code shape; over-engineering checks come from error analysis. |
| H128 | Data agents (DAB): the best agent reached 57% pass@1, and agents stuck to a plan after the data contradicted it. | hamel, shreya | measured (104 queries) | REFUSE | A finding about agents, not an eval method. |
| H129 | Search agents: correct runs need fewer rounds, and the retriever limits accuracy more than the model (14.6% with BM25 against 93.5% with gold documents). | hamel | measured (reported) | REFUSE | Retrieval-specific finding. |
| H130 | Design the product so outputs can be verified; "hard to eval" is a product smell. | hamel | claimed | REFUSE | Product design advice. |

### 1.12 to 1.16 RAG, review tools, cost, skill writing, improvement loops

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H131 | RAG: analyse end to end first, then grade retrieval and generation apart, fix retrieval first, pick a retrieval metric per query type, grid-search chunking, and count the model's own correct facts as hallucinations. | hamel, opik, oj, shreya (RAGGY, qualitative) | described | REFUSE | Domain-specific. Add a RAG reference when a RAG system is under test (YAGNI). |
| H132 | Build a custom annotation tool; teams with one iterate about 10x faster. | hamel | claimed | REFUSE | A tool build with an unmeasured claim. SKILL §1 needs whole traces read, not a particular tool. |
| H133 | Review interface spec: one trace at a time, pass, fail, defer, shortcuts, auto-save, sanitised HTML, no failure-mode dropdowns in the first build. | hamel | described | REFUSE | A UI spec. Its security half is `untrusted-input.md` L3. |
| H134 | Never mute content by role: system and tool messages can hold the bug; group multi-turn traces by session. | hamel | claimed | TAKEN | SKILL §1 L26: "Read each one whole: the input, every tool call and result, the answer." |
| H135 | Write labels back to the trace store and keep a committed local mirror. | hamel | described | REFUSE | Tool-specific (Langfuse). |
| H136 | Keep review tooling minimal. | hamel | claimed | COVERED | `engineering-principles.md` L8 and L17 (fewest moving parts). |
| H137 | Error analysis and evaluation took 60 to 80% of development time. | hamel | described | REFUSE | An observation, not a rule. |
| H138 | Cost order: assertions are cheap; judges need 100 or more labels and weekly upkeep. | hamel, anth (cookbook) | claimed | TAKEN | SKILL §3 L46. |
| H139 | Set how often each eval runs from its cost, saturation and the business value of the error. | hamel | described | COVERED | `judgement.md` L7: every piece of work must move the goal or remove a blocker. |
| H140 | Model cascades for judges (BARGAIN up to 86% more savings; Task Cascades 36% against model cascades in the paper and 48.5% against BARGAIN-style cascades in Hamel's note, different baselines per factcheck-1). The cascade target is agreement with the big model, not with people. | hamel, shreya | measured | REFUSE | An optimisation for high-volume judging; YAGNI at our volume. |
| H141 | Report the agent's cost and the judge's cost separately and never sum them. | hamel, anth (eval-audit L129-139) | described | GAP | SKILL §5 L73, one clause. |
| H142 | Fewer input tokens do not always mean lower cost; every cost suggestion needs a measured cost and the check command. | hamel, anth (cost-hillclimb) | described | COVERED | `engineering-principles.md` L99: "Never present a number you did not measure." |
| H143 | Skills: "directives, not wisdom"; cut motivation and citations. | hamel (meta-skill.md) | claimed | REFUSE | Conflicts with our writing rule to say why in the same sentence; skill-creator also says "explain the why". |
| H144 | Skills: one-line anti-patterns. | hamel | claimed | TAKEN | SKILL "Rationalisations to refuse" L91-100. |
| H145 | Skills: the simplest correct default first, prerequisites for the advanced parts. | hamel | claimed | COVERED | `engineering-principles.md` L8. |
| H146 | Skills under 500 lines, references one level deep, a router skill that only routes. | hamel | claimed | REFUSE | Skill authoring, not evals. A router adds a part (`engineering-principles.md` L17); our skill is one file plus a reference. |
| H147 | Test a skill with a fresh agent on a realistic task. | hamel | described | TAKEN | SKILL §7 L89. |
| H148 | Optimiser loop: one small change at a time, keep only if the keep rule holds, otherwise revert, and log every attempt. | hamel, anth, dd, oj | described | COVERED | `engineering-principles.md` L93-96: change one thing, neutral is a revert, log every attempt kept and reverted. |
| H149 | The optimiser never edits the evaluator, tests, held-out cases, budget, timeouts, seeds or sample sizes, and never weakens a safety check. | hamel, wsh, dd, sf, tob | claimed | TAKEN | SKILL §6 L80: "never edits the evaluator, the items or the thresholds." |
| H150 | Stop after two changes in a row that did not help, or when the budget is spent. | hamel | described | COVERED | `judgement.md` L30-31. |
| H151 | Treat a small gain with suspicion; on a small set, rerun a promising change before keeping it. | hamel | claimed | TAKEN | SKILL §5 L71. |
| H152 | Make the dev and test split once and never redo it; compare configurations on a frontier of score against cost. | hamel (HW8), dd | described | TAKEN | SKILL §6 L80 and §7 L88. |

### 1.17 Their "do not" list, items not already above

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| H153 | Do not use ROUGE, BERTScore or cosine similarity as the main generation metric. | hamel, opik | claimed | TAKEN | Implied by SKILL §3 L47 (yes/no judges on checkable claims). |
| H154 | Do not practise eval-driven development, except for known hard constraints ("never mention competitors"). | hamel | claimed | TAKEN | Both sides are kept: modes come from data (§1), and capability items may exist ahead of the ability (§6 L78). See X16. |
| H155 | Do not jump to switching models as the first fix. | hamel | claimed | REFUSE | Diagnosis, out of scope. |
| H156 | Do not fine-tune judges by default. | hamel | claimed | REFUSE | Out of scope (YAGNI). |
| H157 | Do not use off-the-shelf guardrails without reading their prompts. | hamel | claimed | REFUSE | Runtime guardrails, out of scope. |
| H158 | Prompt diffs suggest assertions (SPADE: 35% structural and 65% content edits over 19 pipelines). | shreya | measured (a taxonomy of edits) | REFUSE | What was measured is the kind of prompt edits, not whether the generated assertions catch failures. SKILL §1 takes checks from read outputs. |

---

## 2. Anthropic (labs.md)

What "auto-evals" is: there is no Anthropic product of that name. Hamel's post titled it; Parlance's July study used it for third-party trace reviewers. The Anthropic release is two guided workflows in the claude-api skill, `/claude-api build-eval` and `/claude-api hillclimb` (PR #1930, merged 2026-09-29), bundled with Claude Code and also offered as a plugin (factcheck-1 #1, #2).

### 2.1 Posts, docs and `claude plugin eval`

Merged elsewhere: "test where a behaviour should and should not happen" is H47; "prefer deterministic graders" is H49; "grade the outcome, not the path" is H116; "one isolated judge per dimension" is H48; "pin the model and judge in CI" is H57; pass@k and pass^k are H106 and F23; the simulated user is F20; the statistics post is B1 to B7; "use a different model to judge" is X11; "grading cost recurs" is H138.

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| A1 | Headroom: the best model at the highest effort should score well below 100%. About 95% or more cannot discriminate, about 0% means a bug, and a saturated eval ends up measuring format quirks. A 100% pass rate means the set is not challenging the system. | anth (A1 post, eval-audit L75-77), hamel, smash, bdf, gepa | described | GAP | SKILL §0 or §5: check the baseline's pass rate before the comparison; outside roughly 10% to 90% the eval can't show a change. Today §5 L74 handles this per item only. |
| A2 | Never paste failures into the prompt. | anth (A1 post) | described | TAKEN | SKILL §6 L80 (the optimiser sees training items only) and `engineering-principles.md` L83 (a patch makes one instance pass). |
| A3 | Keep the answers structurally out of the model's reach; a run cannot read the eval directory. | anth (A1 post, plugin eval L506, eval-audit L157, hillclimb L215) | described | TAKEN | SKILL §3 L51. |
| A4 | Results in the announcement: a 44-ticket support benchmark went from 74.4% to 98.9% on train and from 78.6% to 90.5% on the 14-case held-out test, partly through model and effort swaps rather than prompt changes alone; the claude-api skill went from 66.1% to 87.9% over 24 rounds, partly by fixing graders (factcheck-1 #8, #9). | anth | measured (14 test cases, a wide interval) | TAKEN | Evidence for SKILL §6 L80 (report the holdout) and §2 L42 (broken items). Numbers not cited. |
| A5 | Report the with-minus-without difference: a case that scores 1.0 with and without the plugin shows the plugin is not why it passed. | anth (plugin eval L50), tob, nb, asio | described | TAKEN | SKILL §5 L69 and L74. |
| A6 | Each case runs 3 times by default, because one run of a nondeterministic agent tells you little. | anth (plugin eval L44), dd, oj, promptfoo | described | TAKEN | SKILL §5 L70. See X18. |
| A7 | Give each case one grader on the result and one on the steps taken. | anth (plugin eval) | described | TAKEN | Partly. SKILL §3 L48 grades the outcome first and the path only when the path is the requirement (a destructive command, for example, T20). |
| A8 | Judges have known biases beyond position: longer answers score higher (a model judge "differs more the longer the text it has to read"), and a judge shown the app's answer tends to agree with it. Check the correlation between length and score, keep vocabulary and confidence out of the criteria, and do not show the judge the answer under review as if it were a reference. | anth (plugin eval L226, eval-audit L173-179), oai, oj, neo, sman, dd, nb | measured (simple-man's own judge preferred the longer control answers) | GAP | REF "Grader hygiene", one bullet beside the position rule (L35). |
| A9 | Suspect the judge before the plugin when a "skill fired" grader passes but the difference is negative. | anth (plugin eval L230) | described | TAKEN | SKILL §2 L42 and §4. |
| A10 | Exclude graders that cannot pass without the plugin from both arms (unless every grader in the case would be excluded; `--ablation none` excludes nothing). | anth (plugin eval L245-255) | described | REFUSE | Tool-specific. The idea (trigger checks never move the score) is in C8. |
| A11 | Mock MCP servers with `expect:` input guards; a violated guard aborts the run with score 0. | anth (plugin eval) | described | REFUSE | Tool-specific. Freezing tool results (REF "One item" L18) is our version. |
| A12 | Adopt the vocabulary: task, trial, grader, transcript, outcome, evaluation harness, agent harness, suite. | anth (Demystifying) | described | REFUSE | We use plain words (item, run, grader) per the writing rules; no new terms. |
| A13 | Start small: 20 to 50 simple tasks drawn from real failures. | anth (Demystifying), ls (10 to 20), sky (10 to 20) | claimed | TAKEN | SKILL §0 L20 (smoke check of 10 to 20) and §1 L26 (30 to 100 traces). See X2. |
| A14 | A good task is one where two experts would independently reach the same verdict; a criterion that two reviewers apply differently is not ready. | anth (Demystifying, eval-audit L55), lat | described | GAP | SKILL §2, as a fourth trap ("the item is ambiguous") or REF "One item". |
| A15 | Every task has a reference solution that passes every grader; run an oracle and a null (empty) answer through the whole pipeline first. | anth (Demystifying, eval-audit L57, L123), ls ("write the oracle before anything else") | described | TAKEN | SKILL §4 L64: "push a known-right answer and an empty answer through the whole thing." |
| A16 | Give the judge a way out: an "Unknown" answer. | anth | described | TAKEN | REF "Grader hygiene" L31 ("unknown" maps to unscored). |
| A17 | Read the transcripts; you won't know the graders work otherwise, and the only way to trust a model grader is to try it and read samples. | anth (Demystifying, cookbook), edd, sp | described | TAKEN | SKILL §4 L65 (pilot transcripts) and §1 L26. |
| A18 | Failures should seem fair: it is clear what the agent got wrong and why. | anth | described | TAKEN | Implied by SKILL §2 L42 (check the item before blaming the agent). |
| A19 | Capability evals start low; regression evals sit near 100%; capability items "graduate" into the regression suite. | anth, edd, must, ecc | described | TAKEN | SKILL §6 L78. |
| A20 | Isolate each run: a clean environment and a fresh context every time, state reset between runs, no shared caches, no machine-specific installs, and no installed copy of the skill or instruction file in the control arm. | anth (Demystifying, eval-audit L99), inspect, esk, asio, bdf, sp, tob, hamel, nb | described | GAP | SKILL §5, one bullet before "Repeat each item". Today the skill freezes inputs (§2 L36) but says nothing about the run's own environment. See T8 for the measured contamination case. |
| A21 | Grader bugs can dominate the score: on CORE-Bench, Opus 4.5 went from 42% to 95% after fixing bugs and loosening the scaffold, including a grader that rejected "96.12" for "96.124991" (factcheck-1 #28: not from grader fixes alone). | anth | measured | TAKEN | SKILL §2 L42 makes the same point with the SWE-bench Verified case. |
| A22 | Eval-driven development: build evals for planned capabilities before the agent can do them. | anth, ecc | described | TAKEN | SKILL §6 L78 (capability items, never blocking). See X16. |
| A23 | Do not take scores at face value; the most surprising results usually turn out to be bugs in the eval. | anth (Demystifying, eval-audit L5) | described | TAKEN | SKILL §2 L42. |
| A24 | The people closest to the product and its users (PMs, support, sales) should define success. | anth | claimed | TAKEN | Partly: SKILL §0 L14 shows the three lines to the user. |
| A25 | Swiss cheese: automated evals, production monitoring, A/B tests, user feedback, transcript review and human studies each catch different failures. | anth | described | REFUSE | A survey of layers. This skill is the offline layer; monitoring is M4. |
| A26 | Report the standard error of the mean beside each score. | anth (Nov 2024), stats | described | TAKEN | REF "Arithmetic" L52 (a Wilson interval below a few hundred items). |
| A27 | Prefer volume: more questions with slightly noisier automatic grading beat fewer hand-graded ones. | anth (platform docs) | claimed | REFUSE | Conflicts with SKILL §1 (read real outputs first) and §4 L65 (sign-offs). See X15. |
| A28 | Success criteria are specific, measurable, achievable and relevant, across several dimensions (fidelity, consistency, tone, privacy, latency, price). | anth (platform docs) | described | TAKEN | SKILL §0 L17-18 and §5 L73. |
| A29 | The platform's grading options include a 1 to 5 model scale, cosine similarity and ROUGE-L. | anth (platform docs), anth (Console Evaluate, 5-point scale) | described | REFUSE | Conflicts with SKILL §3 L47. |
| A30 | A pass needs positive evidence: the grader earns "satisfied" by citing it (a fetched page, a file and line), ambiguous evidence goes to the lower verdict, and no penalty may make "do nothing" the best policy. "The default failure mode is a grader that approves everything." | anth (cookbook outcome grader, eval-audit L167), asio, anth (skill-creator grader L39-40, L99), tob ("positive evidence of analysis"), day ("silence is not consent"), neo | described | GAP | REF "Grader hygiene", one bullet. SKILL §3 L50 covers checks that inspect nothing, not a judge that gives the benefit of the doubt. |
| A31 | No rubric yet? Hand the model a known-good example and ask what makes it good. | anth (cookbook) | claimed | REFUSE | Conflicts with SKILL §1: criteria come from read failures, not from a model's reading of one good example. |
| A32 | Eval tasks should need many tool calls, even dozens. | anth (writing tools) | described | REFUSE | Specific to evaluating tool design; our items come from real records (§2). |
| A33 | Graders must be neither too strict nor too lenient: normalise both sides the same way, accept equivalent wording, don't assert counts that depend on mocks, and make a wrong but plausible answer fail. | anth (writing tools, eval-audit L151-153, Demystifying CORE-Bench), wsh, n8n, nb ("sloppy verifiers distort in both directions"), promptfoo | measured (CORE-Bench, A21) | GAP | SKILL §3, one bullet; the health check (§4 L64) gains a confident wrong answer that must fail (AX29). |
| A34 | Collect per-task metrics: accuracy, runtime, tool calls, tokens and tool errors. | anth (writing tools) | described | TAKEN | SKILL §5 L73. |
| A35 | Let the model read transcripts to find tool problems. | anth (writing tools) | described | REFUSE | Conflicts with SKILL §1 L27: the human reads first and the agent organises. |
| A36 | Add multi-step complexity only when measurement shows simpler fails. | anth (building effective agents) | claimed | COVERED | `engineering-principles.md` L8, L12 and L51-53. |
| A37 | An evaluator-optimiser loop works only with clear criteria. | anth | claimed | TAKEN | SKILL §0 L18. |
| A38 | Managed Agents "Outcomes" runs a grader agent after each writer turn, up to `max_iterations` (default 3, max 20). | anth | described | REFUSE | A platform feature. |

### 2.2 claude-api `eval-audit.md`

Merged elsewhere: L5 is A23; L55 is A14; L57 and L123 are A15; L65 is AX8; L67, L69, L87 and L204 are AX3; L75-77 is A1; L81 is H47; L147 and L149 are H116 and T2; L151-153 are A33; L157 is A3; L161 is D23; L163 is H48; L165 is H44; L167 is A30; L173-179 is A8 and AX29; L187 is H85.

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| AX1 | Every audit check is a build requirement for a new eval and a verification pass on an old one; rerun it before the first paid pass and before round 1. | anth (L3) | described | TAKEN | SKILL §4 L64: "Health check before every new pipeline." |
| AX2 | Before auditing, run the eval end to end on a handful of cases. | anth (L9), tob, n8n, edd, bt | described | TAKEN | SKILL §0 L20 (smoke check) and §4 L65 (pilot). |
| AX3 | Audit the items before trusting results: programmatic checks over all, a close read of 20 to 50 stratified items, and per-item flags for an ambiguous task, a suspect answer key, an answer the model knows from memory, difficulty from wording rather than the problem, a grader too strict or too lenient, a cheatable item, and a stale key. A strong model can look for label disagreements now and then. | anth (L17-48, L67, L69, L87, L204), opik ("audit it first"), dd | described | GAP | SKILL §2, after the three traps: "Audit before trusting" with the flag list. Today §2 L38 hand-checks a sample for one trap only. |
| AX4 | A reference answer must exist and pass the grader; a 0% pass rate across all variants usually means a broken item. | anth (L57) | described | TAKEN | SKILL §4 L64 and §2 L42. |
| AX5 | Re-derive 10 labels yourself. | anth (L59) | described | TAKEN | SKILL §2 L38: "Hand-check a sample." |
| AX6 | Record where the ground truth came from, and never use model A's outputs as gold for an A versus B question. | anth (L61) | described | TAKEN | SKILL §2 L35; REF "One item" `answer_key.source`. |
| AX7 | For an agent that classifies or flags (triage, review), report the confusion matrix, recall and precision separately, and a majority or constant baseline; a trivial baseline (one sentence of "be concise", or always the majority class) must not score well. "A judge that cannot beat the constant baseline has learned nothing." | anth (L63, L79, build-eval L76), tob (recall and precision per case), dd, sman | described | GAP | SKILL §5, one bullet; REF "Arithmetic". Today the two-rate rule exists only for judges (§4 L61). |
| AX8 | Check for label leakage in the prompt, few-shot examples, tools or files. | anth (L65) | described | TAKEN | SKILL §3 L51 and §2 L39 (seed items are open-book). |
| AX9 | For agentic items, give the symptom, not the investigation. | anth (L71), n8n ("keep it in the user's voice") | described | TAKEN | SKILL §2 L36: freeze the input as first seen, with the fix and close reason stripped. |
| AX10 | Match production's distribution and interaction shape (single turn or multi-turn). | anth (L73) | described | TAKEN | SKILL §1 L26 and §2. |
| AX11 | Test one capability per item when diagnosis matters. | anth (L83) | described | REFUSE | Diagnosis. One check per mode (§3 L47) already says which mode moved. |
| AX12 | If a weaker variant beats a stronger one on an item, suspect a bug. | anth (L85) | described | TAKEN | Implied by SKILL §2 L42. |
| AX13 | For generated items, fix the generator, not the filter. | anth (L89) | described | REFUSE | Synthetic generation is out (H78). |
| AX14 | Keep infra failures out of results in a sidecar with a failure class; mark truncation (max tokens, context limits, silently cut tool output) as its own status; count refusals as their own metric. | anth (L95, L107, L169), day (truncated output is void), inspect (exec output silently incomplete) | described | TAKEN | Partly. SKILL §3 L49 makes grader errors, timeouts and infra failures unscored; truncation and refusals are not named. |
| AX15 | "No answer" is not a negative answer (a crash is not "no issues found"). | anth (L97), smash, nb | described | TAKEN | SKILL §3 L49. |
| AX16 | Make sure the environment is complete: the agent has the tools and data the task needs. | anth (L101) | described | TAKEN | REF "One item" L17-20 (frozen tool results and context, and what can't be rebuilt said out loud). |
| AX17 | Make setup deterministic: seeds, ordering, sampling parameters. | anth (L103) | described | TAKEN | Partly: REF L30 fixes the judge's temperature and seed; the agent side is not said. |
| AX18 | Separate scaffold limits from model limits. | anth (L105) | described | REFUSE | Diagnosis. |
| AX19 | Retry infra errors with jittered backoff and record the retries; a case that passes only on retry counts as a fail. | anth (L109, build-eval L107-112) | described | TAKEN | SKILL §6 L79: "A failure that goes away on rerun is a flake to fix or an unscored result, never a pass." |
| AX20 | Set a hard wall-clock ceiling per item; a timeout goes to errors, not to a zero. | anth (L111) | described | TAKEN | SKILL §3 L49. Inspect and wshobson score a hit limit as a failure instead; see X13 and F25. |
| AX21 | Assert the served model from the response, not the requested name. | anth (L113) | described | TAKEN | SKILL §6 L83 (record the versions with every result). |
| AX22 | Run the real agent through its real entry point with production's prompt, tools and model config, imported from the app rather than copied; if a proxy hides the model or usage, propose a small additive change. | anth (L115, build-eval L27, L165-169), bt, inspect (agent bridge) | described | GAP | SKILL §2 or REF "One item": the item records the agent's entry point and config at T. |
| AX23 | Save every per-item trajectory plus the grader's inputs and outputs ("the single highest-leverage habit"), so a grader change can rescore without rerunning the agent. | anth (L117), inspect (separate scoring step), smash (cache key) | described | TAKEN | Partly: SKILL §7 L88 caches agent outputs when only the grader changes; saving the grader's inputs and outputs is not said. |
| AX24 | Grade only what the task asked for: a check on a name, metric or mechanism the prompt never asked for scores a hidden preference, and an artifact a correct run never reaches is never graded. | anth (L145), ls, n8n ("if the conversation specified it, pin it"), tob | described | GAP | SKILL §3, one clause in the checkable-claims bullet. |
| AX25 | Graders resist cheating: hard-coded answers, reading the keys, injecting the judge. | anth (L155), edd | described | TAKEN | Partly: SKILL §3 L51 and REF L32. Reading the winner for hacks is D84. |
| AX26 | Spot-check failures; if more than about 1 in 10 are grader errors, fix the grader first. | anth (L159) | described | TAKEN | SKILL §4 L64. |
| AX27 | Run the grader twice on the same output to measure grader variance. | anth (L161) | described | GAP | Merged into D23. |
| AX28 | Penalties must not make "do nothing" the best policy. | anth (L167) | described | GAP | Merged into A30. |
| AX29 | Before trusting a judge, check it fails an empty answer, "I don't know", an answer to a different question, and a confident wrong answer, and that an induced API error lands as an error. | anth (L179, build-eval L175) | described | GAP | SKILL §4 L64 has the empty answer only; add the other three negatives and the induced error. |
| AX30 | Compare the noise floor (about 1/√(n·R)) with the headroom and the smallest change worth acting on, before running. | anth (L185, hillclimb L211: 25 items at 2 repeats is about ±14 points) | described | TAKEN | REF "Arithmetic" L53 and SKILL §5 L71. |
| AX31 | Show the mechanism is wired: disable it and confirm the score drops. | anth (L189), tob (gate case) | described | TAKEN | SKILL §7 L89 (guidance-deletion test); `testing.md` L83. |
| AX32 | Recompute the headline from the raw rows, and read the written row rather than the printed number. | anth (L191, build-eval L171), sman, opik, dd | described | COVERED | `engineering-principles.md` L99 and `testing.md` L87 ("Run it, then say what it returned"). |
| AX33 | Report audit findings as observations, severity first, with evidence; say when things are fine; offer to fix. | anth (L195-202) | described | REFUSE | Report style; it belongs to the shared writing references, not the evals skill. |

### 2.3 claude-api `build-eval.md`

Merged elsewhere: L54 is A13 and X2; L76 is AX7; L81 is REF L35 (randomise order); L82 is X8 and X11; L91 and L95-99 are AX2; L165-169 is AX22; L171 is AX32; L175 is AX29.

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| AB1 | The goal is a runnable eval the user trusts: inputs, a runner and a grader; fit the codebase, never impose a framework, and reuse what exists. | anth (L3-7, L45), smash, neo | described | COVERED | `engineering-principles.md` L26-34 (the ladder: reuse what is in the codebase first); SKILL L10 (the simplest eval). |
| AB2 | Ask questions with a recommended option first, batched, in short messages. | anth (L9-11), oj | described | COVERED | `judgement.md` L40: bring options with a recommendation, never a bare question. |
| AB3 | Two hard sign-offs, on the inputs and on the grading method; "mostly, but" means fix and show again. | anth (L13, L64), lf, n8n | described | TAKEN | SKILL §4 L65. |
| AB4 | One flow per eval; no grand unified benchmark; pick one decision point observable in traces. | anth (L25), bt | described | TAKEN | SKILL §0 L16-17. |
| AB5 | An eval run never writes, sends or spends in production: use fixtures for live external state, stub only the side-effecting tools and grade their calls, use read-only mounts and dummy keys, and run any code a grader executes in an isolated sandbox (a timeout is not a security boundary). | anth (L29), opik, promptfoo, wsh, tob | described | GAP | SKILL §2 or §5, one bullet; `engineering-principles.md` L22 (least privilege) is the principle behind it. |
| AB6 | Ask what each request carries besides text; for multi-turn, grade the conversation's outcome by default. | anth (L33-35) | described | TAKEN | SKILL §3 L48. |
| AB7 | Source priority: production transcripts, then tickets and bug reports, then 5 to 10 hand-written seeds, then synthesis anchored on real examples. | anth (L47-52) | described | TAKEN | SKILL §1 L26 and §2 L35. |
| AB8 | Scrub personal data (and customer names) from traces before they go into items, judge prompts or files; check retention, store ids where you can. | anth (L47-52), dd, cal, n8n | described | GAP | REF "One item", one line. Nothing in our material covers personal data in eval items. |
| AB9 | Use 15 to 100 items, and size for the noise floor if you will hill-climb. | anth (L54) | described | TAKEN | SKILL §1 L26; REF "How many items" L55. |
| AB10 | Show the user all inputs; prefer their own viewer; never hand-roll HTML from untrusted item text. | anth (L58, L148-161) | described | COVERED | `untrusted-input.md` L3; SKILL §4 L65. |
| AB11 | When asking for a label, quote the item's lines. | anth (L62) | described | REFUSE | An interaction detail. |
| AB12 | Offer a menu of side metrics: length, tool calls, refusals, max tokens hit, format, cost, latency. | anth (L70-74) | described | TAKEN | SKILL §5 L73. |
| AB13 | Use the cheapest grader that truly measures the property; for agents, a programmatic end-state check plus a no-op detector, and transcript grading only for process guardrails. | anth (L78-80) | described | TAKEN | SKILL §3 L46 and L48; the no-op half is A30. |
| AB14 | Pairwise blind comparison: randomise A and B, allow "tie" and "both bad", treat candidates as untrusted, freeze the reference outputs. | anth (L81) | described | TAKEN | Partly: REF L35 randomises order and grades both orders; "tie" and "both bad" are not named. |
| AB15 | Pointwise rubrics: the user picks the judge, the judge is never the model under test, outputs are structured, and criteria are checkable claims, not 1 to 5 scales. | anth (L82) | described | TAKEN | SKILL §3 L47; REF L30. |
| AB16 | Show the criteria left out and why; don't score the same thing twice. | anth (L87) | described | TAKEN | SKILL §1 L28 ("or a stated reason it doesn't"). |
| AB17 | Report absolute numbers first: counts and n beside every rate, the dataset version, never a rate without its denominator. | anth (L89), smash ("84% on golden-v3, n=120"), day | described | GAP | SKILL §5, one clause; REF "Arithmetic" already writes "40 passes out of 50" but does not ask for it. |
| AB18 | Pilot-grade about 5 items; the user reads the transcripts and is asked "Would you have scored any of these differently?" until there is no disagreement. | anth (L91, L95-99) | described | TAKEN | SKILL §4 L65. |
| AB19 | Runner mechanics: write rows as they finish, resume on (item, repeat), concurrency, file contracts, variant folders, a bundled report builder, and a question about what to commit. | anth (L105-117, L144-161, L211-217), inspect (resume, do not rerun) | described | REFUSE | Tooling. The repo's own runner and conventions decide (`engineering-principles.md` L29). |
| AB20 | A harness-integrity gate: the user approves the harness hash, never the agent. | anth (L146) | described | TAKEN | The idea is SKILL §6 L80 (the optimiser never edits the evaluator); the hash mechanism is tooling. |
| AB21 | Run the full baseline yourself, verify the report, and hand over one path and a one-line headline. | anth (L195-205) | described | REFUSE | Workflow style; `testing.md` L87 covers saying what a run returned. |
| AB22 | Named failure modes of eval building: skipping sign-offs, running before a yes, reimplementing the app, guessing cost, trusting a zero, ignoring data handling, over-trusting the judge, a grand eval. | anth (L225-233) | described | TAKEN | Spread across SKILL §0 to §4 and the rationalisation table. |

### 2.4 claude-api `eval-hillclimb.md` and `cost-hillclimb.md`

Merged elsewhere: hillclimb L211 is AX30; L215 is A3; L231 and L233 are `engineering-principles.md` L83 and L93 (H148); L269 is T8; L271 and L80 are C8; cost-hillclimb L369-370 is H148.

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| AH1 | The number that matters is the held-out difference, measured once at the end on the baseline and the winner. | anth (hillclimb L7), dd, opik, gepa (winner's curse) | described | TAKEN | SKILL §6 L80. |
| AH2 | A runnable eval comes before any hill-climbing ("editing and hoping" otherwise), capturing transcript, model, usage and grade from the same call. | anth (L21-25) | described | TAKEN | SKILL §0 and §6. |
| AH3 | Measure the noise directly before the loop: rerun the unchanged baseline (an A/A run) to get the real run-to-run spread, and when the scored thing is itself generated (a page, a prompt, a skill), regenerate it too. One measured case had 7 points of build spread against ±1.4 points of rescoring noise. | anth (hillclimb L41, cost-hillclimb L351-357), dd (derive the threshold from measured noise) | measured | GAP | SKILL §5 L71 and REF "Arithmetic": the formula (±1/√n) is a floor; the measured A/A spread is the noise to beat. |
| AH4 | Spend tokens on the slice with the most signal per token. | anth (L45-49) | described | REFUSE | Optimisation detail. SKILL §5 L74 already drops items with no signal. |
| AH5 | Name one goal (raise a metric, cut cost or latency, migrate model); everything else is a guardrail. | anth (L55-64) | described | TAKEN | SKILL §0 L17 and §5 L73. |
| AH6 | Scope what may change, what is off limits, and the harness paths. | anth (L66-78), dd | described | TAKEN | SKILL §6 L80; `judgement.md` L14. |
| AH7 | Plateau: stop after K of 3 or more flat rounds ("two flat rounds is too few"), and only count a change above the noise floor. | anth (L88-97), dd, he, oj | described | COVERED | `judgement.md` L30 stops after two passes that changed nothing. The two disagree on the count; see X19. |
| AH8 | Use the same set every round and never subset it silently; budget the loop as (N+1) × R × cost. | anth (L101-110) | described | TAKEN | SKILL §5 L69; `judgement.md` L22. |
| AH9 | Small sets: no split, use repeats and call the result "directional"; at 40 rows or fewer, Datadog says report in-sample. | anth (L205-211), dd | described | REFUSE | Conflicts with SKILL L99: "Keep a holdout, however small, and say how small." See X6. |
| AH10 | Run the baseline arm in the same window as the change and record an environment fingerprint; never compare with a baseline measured days ago, because the model and world drift ("a comparison for one model at one time"). | anth (L219), tob, day ("identical conditions, ideally the same time window"), opik | described | GAP | SKILL §5 L69, one clause: "run both arms in the same window." |
| AH11 | Only training transcripts are read; a fresh analyser each round; the outer session sees scores only. | anth (L225-229), dd | described | TAKEN | SKILL §6 L80. |
| AH12 | Analyser steers toward generalising, not memorising, and names the regressions it expects. | anth (L231), bt ("helps one or two rows: overfitting"), dd ("never a rule that names rows") | described | COVERED | `engineering-principles.md` L83 (a patch makes this instance pass and leaves the cause). |
| AH13 | Keep or revert: train up and test flat, revert; train down, revert; on ties prefer the later round. | anth (L273) | described | COVERED | `engineering-principles.md` L95: "Neutral is a revert." |
| AH14 | Classify each failure before fixing anything: a real agent failure, a broken item, a grader error, the environment (every item failing the same way), or noise (rerun to see). Change only the layer the verdict points to: never fix the agent to satisfy a broken grader, and never loosen a grader to hide a real regression. | anth (L281-300), novu, n8n, edd, oj, ls, mcpj | described | GAP | SKILL §2 L42 starts this ("check the item"); a short triage order would finish it. |
| AH15 | Final report: the held-out difference with intervals, "recommend not merging" when inside the noise, before and after transcript pairs, and what to try next. | anth (L306-316) | described | TAKEN | SKILL §5 L71: "the advice is not to ship." |
| AH16 | Loop tooling: background runs, state files, analyser prompt templates, a de-fluff pass, status tables and narrative files. | anth (L13, L126-195, L237-263) | described | REFUSE | Tooling for that workflow. |
| AC1 | Pre-register three adoption gates: a quality band, a cost margin, and the predicted mechanism showing up in the measurements. | anth (cost-hillclimb L331-342) | described | TAKEN | SKILL §0 L18 (pass rule) and §7 L89 (show the gain comes from what changed). |
| AC2 | The split that picks winners each round is a selection set, even if a guide calls it "test"; a joint confirm on untouched data is the headline. | anth (cost-hillclimb L344, L357-358) | described | TAKEN | SKILL §6 L80. Other Anthropic material disagrees; see X7. |
| AC3 | Put cost in the objective: one quality-only climb raised cost per deliverable by 75%. | anth (L366-368) | measured | TAKEN | SKILL §5 L73 and §7 L88. |
| AC4 | The optimiser predicts a point estimate, an 80% interval and what would prove it wrong, before measuring. | anth (L371-378), nb (per-task predictions) | described | TAKEN | Partly: SKILL §0 L18 pre-registers the pass rule, not a prediction per change. |
| AC5 | Audit graders before believing failures that persist: re-grading shrank a claimed +9 points to +3. | anth (L384-386) | measured | TAKEN | SKILL §2 L42 and §4 L64. |
| AC6 | Cost comes from extra actions, not prompt length: "Verify twice" cost 48% more and "be maximally thorough" 39% more. | anth (L394-414), tob ("do not add verification scaffolding") | measured (Claude-specific) | REFUSE | A prompt-writing finding, not an eval rule. The eval rule it supports (measure cost, H142) is covered. |
| AC7 | Prompt wins arrive in rounds 1 and 2; cap at 3 to 4 rounds per model; effort cuts need overall non-inferiority. | anth (L429-442) | described | REFUSE | Specific to that loop; `judgement.md` L27-31 stops the general case. |
| AC8 | The report schema's paired difference uses a Wald interval over per-item differences. | anth (SCHEMA L132-148) | described | TAKEN | REF "Arithmetic" L54 uses the exact McNemar test instead, which holds at small n. |
| AC9 | Runner outputs are model-influenced, so treat them as untrusted (no symlink writes, strip terminal escapes). | anth (runner scaffold) | described | COVERED | `untrusted-input.md` L3. |

### 2.5 skill-creator

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| SC1 | Loop: draft, run test prompts, evaluate, rewrite, repeat, grow the set. | anth (SKILL L14-19) | described | COVERED | `testing.md` L3-10 (red, green, refactor). |
| SC2 | Suggest test cases for skills with verifiable output and maybe none for subjective ones; the user decides. | anth (L54), sp ("don't test pure reference skills") | described | REFUSE | Every skill in this library carries evals (`evals/` folders); we do not exempt subjective skills. |
| SC3 | Interview about edge cases, formats and success criteria before writing prompts. | anth (L58) | described | TAKEN | SKILL §0. |
| SC4 | Make descriptions "pushy" because Claude under-triggers. | anth (L67) | described | REFUSE | Skill authoring, not evals. |
| SC5 | Start with 2 to 3 realistic prompts; prompts first, assertions after seeing outputs. | anth (L143-145), asio | described | TAKEN | Partly: assertions after outputs is SKILL §1 L24; the size is X2. |
| SC6 | Run the with-skill arm and the baseline together; the baseline is no skill for a new skill and the old snapshot for an edit. | anth (L169-186, L313), asio | described | TAKEN | SKILL §5 L69 and §7 L89. |
| SC7 | Give each eval a descriptive name. | anth (L188) | described | REFUSE | Trivial; REF "One item" has a stable id. |
| SC8 | Assertions are objectively checkable with descriptive names; don't force them onto subjective output. | anth (L199-203) | described | TAKEN | SKILL §3 L47. |
| SC9 | Capture tokens and duration per run as they arrive. | anth (L209-219), asio | described | TAKEN | SKILL §5 L73. |
| SC10 | A grader sub-agent with text, passed and evidence fields; a script for anything programmatically checkable. | anth (L225) | described | TAKEN | SKILL §3 L46. |
| SC11 | Aggregate as mean ± standard deviation and the difference of means, with no interval. | anth (L227-231, aggregate_benchmark.py) | described | REFUSE | Conflicts with REF "Arithmetic" (paired test, Wilson interval). |
| SC12 | Analyst pass: assertions that never discriminate, flaky evals, time and token trade-offs. | anth (L234) | described | TAKEN | SKILL §5 L74 and §6 L78. |
| SC13 | Generate the human viewer before judging outputs yourself; empty feedback means fine. | anth (L236-251, L282, L451) | described | TAKEN | The human-first half is SKILL §1; the viewer is tooling. |
| SC14 | Generalise from feedback; no overfitted changes or rigid MUSTs; explain the why; keep the prompt lean; bundle repeated helper scripts. | anth (L298-304) | described | REFUSE | Skill authoring, not evals. The overfitting half is `engineering-principles.md` L83. |
| SC15 | Stop when the user is happy, feedback is empty, or there is no progress. | anth (L318-321) | described | COVERED | `judgement.md` L27-31. |
| SC16 | The judge is blind: unlabelled, order-shuffled outputs, never told which arm produced which, never shown the skill, the generator's identity, its reasoning or the author's expectations. | anth (L327, comparator L7), sf, nb, esk, must | described | GAP | REF "Grader hygiene" L35: today it randomises order; add that the judge never sees arm labels or the skill. |
| SC17 | Trigger evals: about 20 queries, half should trigger and half should not, realistic and detailed, the negatives near-misses; one-step queries never trigger a skill whatever its description; the user reviews the set. | anth (L339-358, L373, L398-400) | described | GAP | Merged into C8. |
| SC18 | The description-tuning loop splits 60/40, runs each query 3 times, iterates up to 5 times and keeps the best by test score. | anth (L394, run_loop.py L216-217) | described | REFUSE | Selects on the test set, against SKILL §6 L80. See X7. |
| SC19 | In Claude.ai without sub-agents, skip baselines and benchmarks. | anth (L424-434) | described | REFUSE | Conflicts with SKILL §5 L69 (always two arms). |
| SC20 | The grader also critiques the evals: flag assertions that would pass for a wrong output, outcomes no assertion covers, and unverifiable assertions ("a passing grade on a weak assertion is worse than useless"). | anth (grader L9, L68-79), asio, opik ("would have failed on the bad trace"), n8n, cal | described | COVERED | `testing.md` L37: "Name the break ... If no change would fail it, delete it." |
| SC21 | Inspect the output files themselves, not the transcript's claims about them; extract implicit claims and verify them. | anth (grader L30, L45-59) | described | TAKEN | SKILL §3 L48 (end state); `testing.md` L84. |
| SC22 | No partial credit. | anth (grader L223) | described | TAKEN | SKILL §3 L47. Demystifying disagrees; see X9. |
| SC23 | The comparator scores content and structure rubrics 1 to 5, decides on rubric score first, says ties are rare and to "be decisive". | anth (comparator L39-58, L77-85) | described | REFUSE | Conflicts with SKILL §3 L47 and REF L35 (grade both orders when close). |
| SC24 | The post-hoc analyser scores instruction following 1 to 10 and makes suggestions by category. | anth (analyzer L5-85) | described | REFUSE | A scale; conflicts with SKILL §3 L47. |
| SC25 | Benchmark patterns: passes in both arms (no signal), fails in both (broken), passes only with the skill (value), fails only with it (harm), high variance (flaky). | anth (analyzer L189-247) | described | TAKEN | SKILL §5 L72-74 and §2 L42. |
| SC26 | `run_eval.py` counts a failed query as "not triggered" (L225, not L240), so infra errors become negatives. | anth (factcheck-1 #19) | described | TAKEN | As the anti-pattern SKILL §3 L49 prevents. |
| SC27 | `schemas.md` names the field `expectations` while SKILL.md calls it `assertions`. | anth (factcheck-1 #17) | described | COVERED | `engineering-principles.md` L10 (one fact, one home). |
| SC28 | The plugin eval format and skill-creator's `evals.json` do not read each other's files. | anth (plugin eval L19) | described | REFUSE | Tool detail; our skill is harness-neutral (SKILL L10). |

### 2.6 OpenAI and Google

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| O1 | Evaluate early and often, log as you develop to mine cases, calibrate automatic scoring with human feedback, and run evals on every change. | oai | described | TAKEN | SKILL §6 and §4. |
| O2 | Anti-pattern: "it seems like it's working" as the evaluation strategy. | oai | claimed | COVERED | `testing.md` L87: "'Should', 'probably' and 'seems to' in a status line mean the check has not run." |
| O3 | Checks by architecture: instruction following for one turn, each step for workflows, tool selection and data precision for agents, handoff accuracy for multi-agent. | oai | described | TAKEN | SKILL §3 L48. |
| O4 | Judges: pairwise or pass/fail for reliability, and control for response length. | oai | described | TAKEN | SKILL §3 L47; the length half is A8. |
| O5 | The OpenAI graders catalogue (string check, text similarity, score model, label model, python, multi). | oai | described | REFUSE | Platform-specific. |
| O6 | "Produce a smooth score, not a pass/fail stamp" (for reinforcement fine-tuning), guard against reward hacking, balance labels. | oai | described | REFUSE | Aimed at training rewards; conflicts with SKILL §3 L47 for measurement. See X26. |
| O7 | Grade traces to debug first, then move to repeatable datasets. | oai | described | TAKEN | SKILL §1 then §2. |
| O8 | The OpenAI Evals platform is deprecated: notice on June 3, 2026, read-only on Oct 31, 2026, shut down on Nov 30, 2026, Promptfoo as the migration path, and graders part of the transition (not Datasets, per factcheck-1 #30). openai/evals is in maintenance. | oai | described | REFUSE | Not a dependency: the skill is harness-neutral (SKILL L10). |
| O9 | Tie eval metrics to the cost of each error: ask the user what a false pass and a false fail each cost, define the decision loss before choosing the grader, and set the judge's bar from that rather than by habit. | oai (receipt cookbook, illustrative), dd ("a product question only the user can answer"), must | described | GAP | SKILL §0 L18 (the pass rule) and §4 L62 (the 0.8 bar becomes the default when the costs are equal). |
| O10 | Google ADK: unit-test files and eval sets, tool trajectory match (exact, in order, any order; default 1.0), ROUGE-1 response match at 0.8, LLM criteria. | google | described | REFUSE | Tool-specific; a ROUGE threshold conflicts with SKILL §3 L47. |
| O11 | Vertex adaptive rubrics: the service writes per-prompt pass/fail rubric tests, then checks the response against each. | google | described | REFUSE | Model-written criteria conflict with SKILL §1 (criteria from human-read failures) and §2 L35. |

---

## 3. Skill-eval repos (repos.md part A)

### 3.1 trailofbits/skills

Merged elsewhere: rule 8 (pilot one case) is AX2; rule 15 (ground truth never in the fixture) is A3; rules 29 and 31 are AX24 and T18; rule 33 and 57 (throwaway repo, isolation preflight) are A20; rule 36 (the difference drifts with the model) is AH10; rule 38 (same bare prompt with and without) is A5; rule 63 (baseline failures are the point) is A5; rules 50, 53 and 58 (trigger graders, case shape, discovery canary) are C8; rule 72 (non-hermetic installs) is A20.

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| T1 | A checker that inspects zero items must fail, not pass: exit non-zero on a zero count, and keep a fixture proving it still detects its target. | tob (AGENTS.md L339), sp, n8n, bdf | described | TAKEN | SKILL §3 L50; `testing.md` L59 (a probe that never checks each page loaded). |
| T2 | Grade the artifact or the executed tool calls, never the response text: a grader that judged the prose passed a run that skipped the work. | tob (AGENTS.md, code-improver, git-cleanup, goal-prompt), sp, ls | described (an incident) | TAKEN | SKILL §3 L48: "Grade the outcome first: the final answer, the end state." |
| T3 | Do not add verification scaffolding to prompts; it causes over-verification on current models. | tob (AGENTS.md) | described | REFUSE | A prompt-writing rule (with AC6), not an eval rule. |
| T4 | Do not tell a reviewer to pre-filter; ask for everything with a severity and filter in a separate pass. | tob (AGENTS.md) | described | REFUSE | Prompt design for review agents, not an eval method. |
| T5 | Start at the highest effort, then sweep down on your own evals. | tob (AGENTS.md) | described | REFUSE | Model configuration. The eval half is the cost frontier, SKILL §7 L88. |
| T6 | The judge model must differ from the model the cases run on (self-preference). | tob (code-improver L22), oj, inspect, anth, edd, lat, wsh, must | described | TAKEN | REF "Grader hygiene" L30. |
| T7 | Expect two or three calibration pilots per new rubric: three pilots found five failures where the model was right and the grader wrong (two mislabelled fixtures, three rubric defects). | tob (variant-analysis L51, code-improver) | measured | TAKEN | SKILL §4 L64 (grader errors first) and L65 (pilot transcripts). |
| T8 | Verify isolation, don't assume it: build fixtures inside the run's workspace, scan every baseline transcript for the skill's path, grader file names and answer-key phrases, fail the gate when it has nothing to scan, and rerun the scan whenever the numbers look too good. In one version-comparison run the old-plugin arm listed the grafted eval tree and read grader file names as instructions in 10 of 15 runs; contaminated baselines elsewhere scored up to 1.00 (factcheck-2 #1). A jump bigger than the change explains is a reason to look. | tob (code-improver L60-63, goal-prompt L37, check_contamination.py), nb (failure 5), anth (hillclimb L269), he | measured | GAP | SKILL §3 L51 says keep keys out of view; add "and check that they stayed out: scan the baseline transcripts before reading the scores". |
| T9 | Prove every counting grader against a known-bad and a known-good specimen: the bad review must fail every criterion and the good one pass every criterion. | tob (code-improver, writing-lean-proofs), bt, ls, cal, oj | described | TAKEN | SKILL §4 L64; `testing.md` L46 (mutation check). |
| T10 | Weight LLM rubrics 2 and mechanical checks 1. | tob | described | REFUSE | Arbitrary weights (`engineering-principles.md` L7); our results stay per check, not a weighted sum. |
| T11 | "Measured, not assumed: record the numbers here." | tob | described | COVERED | `engineering-principles.md` L99. |
| T12 | Print metrics that can't be rebuilt as UNAVAILABLE, never as zeros; an unscorable iteration is "no change", never 0. | tob (ablation), dd | described | TAKEN | SKILL §3 L49; REF "One item" `not_recordable`. |
| T13 | The scorecard fails loudly if an arm contributes zero runs. | tob (ablation) | described | TAKEN | SKILL §3 L50. |
| T14 | Report every metric for both arms, including the ones where the new arm loses; no pre-filtering. | tob (ablation), must, bt | described | TAKEN | SKILL §5 L73: "Report what got worse." |
| T15 | Set success thresholds before running, coarse on purpose. | tob, nb, day, esk, edd, ecc | described | TAKEN | SKILL §0 L18. |
| T16 | Record cost per run and pilot with one run before the paid suite. | tob (ablation, variant-analysis) | described | TAKEN | SKILL §5 L73 and §0 L20. |
| T17 | Never regex a command or claim in prose: a regex cannot tell a recommendation from a mention. A `regex_present` grader failed the plugin for obeying its own safety gate, three of four `regex_absent` graders were false positives on the first real run, and one produced a fake +0.20 uplift. Template echoes and quoted counter-examples also pass as hits. | tob (git-cleanup L42, L49-66), sp, he, promptfoo (exact match on agent prose) | measured | GAP | SKILL §3 L46: name prose as not exact, so a code check reads the executed tool call or the artifact and a judge reads the prose. |
| T18 | A case whose expected output is an absence gets a matching positive grader in the same commit. | tob (git-cleanup) | described | TAKEN | SKILL §3 L50. |
| T19 | Name the confounds you accept on purpose ("a real confound, and it is accepted deliberately"). | tob (git-cleanup) | described | COVERED | `judgement.md` L15: say what you could not check. |
| T20 | Each failure mode gets an artifact check and a behavioural one, because either alone is fooled: a run that wrote a careful safe analysis and also ran `git branch -D` fails. | tob (git-cleanup) | described (an incident) | TAKEN | SKILL §3 L48: when the path is the requirement (a destructive command), check it separately. |
| T21 | Treat a single run as a sample; rerun before concluding a change caused a regression. | tob (git-cleanup), edd, novu | described | TAKEN | SKILL §5 L70. Reruns measure; they never replace a failure (X20). |
| T22 | Share the grader library on purpose: a self-test that reimplemented the graders would prove only that two copies agree. | tob (git-cleanup) | described | COVERED | `engineering-principles.md` L10-11 (one fact, one home) and `testing.md` L40. |
| T23 | The judge must be strong enough to follow the graders' scoping (the default small judge could not). | tob (goal-prompt L20, variant-analysis) | described | TAKEN | Caught by SKILL §4 (a weak judge fails its held-out rates). |
| T24 | Keep mechanical criteria out of the LLM rubric, so the judge does not penalise correct output on format. | tob (review-walkthrough), lat (rule first) | described | TAKEN | SKILL §3 L46-47. |
| T25 | Tell the model to report a missing fixture and stop, so an invented repository can't earn credit. | tob (review-walkthrough) | described | REFUSE | Prompt design for the agent under test. |
| T26 | When the environment failed, say "no passing result is claimed for this revision". | tob (review-walkthrough), ls ("flakiness is unmeasured") | described | COVERED | `testing.md` L93: "A check you skipped is named, with the reason." |
| T27 | Keep an all-negatives case: the only one that punishes over-reporting. | tob (variant-analysis) | described | TAKEN | SKILL §2 L40. |
| T28 | Build cases where a literal, no-generalisation run scores above zero but wrong. | tob (variant-analysis) | described | REFUSE | A case-design detail for that plugin. |
| T29 | A grader no arm can fail is worth deleting, not reweighting; remove assertions that always pass in both arms. | tob (variant-analysis, yara), asio | described | TAKEN | SKILL §5 L74; `testing.md` L37. |
| T30 | A saturated difference can only go down: the case becomes a precision-regression guard. | tob (variant-analysis) | described | TAKEN | SKILL §6 L78 (regression items). |
| T31 | Fixtures carry planted flaws and known non-flaws (correct code that folk advice wrongly flags). | tob (writing-lean-proofs) | described | TAKEN | SKILL §2 L40 (negatives). |
| T32 | A must-flag criterion names the declaration, explains why and proposes a fix. | tob (writing-lean-proofs) | described | REFUSE | Domain-specific. |
| T33 | For a review-only task, check the fixture files are byte-identical afterwards. | tob (writing-lean-proofs) | described | TAKEN | SKILL §3 L48 (end state). |
| T34 | The judge returns exactly one JSON array whose ids match the rubric in order; missing evidence is rejected. | tob (writing-lean-proofs) | described | TAKEN | REF L33-34 (parse the last verdict; no verdict is unscored). |
| T35 | Judge the transcript only; no credit for problems the judge can see but the review does not mention. | tob (grade-prompt), nb | described | TAKEN | SKILL §3 L47 (checkable claims in the output). |
| T36 | Hedged notes marked optional or minor do not fail the criterion. | tob (grade-prompt) | described | REFUSE | Domain detail of that rubric. |
| T37 | An accidental error in a fixture is fixture debt: fix the fixture, not the rubric. | tob (writing-lean-proofs), novu | described | TAKEN | SKILL §2 L42. |
| T38 | Guidance-deletion test: delete the skill's guidance and re-measure; in yara two cases kept 0.94 to 1.00 with the guidance gone (the gain came from loading the skill) while one dropped from 1.00 to 0.60. | tob (yara L51-62) | measured | TAKEN | SKILL §7 L89. |
| T39 | Prefer cases that only this plugin's content can satisfy, checked mechanically. | tob (yara) | described | TAKEN | Partly: SKILL §7 L89. |
| T40 | Anchor regex graders to non-comment lines, so a comment cannot satisfy them. | tob (yara) | described | REFUSE | Detail of T17. |
| T41 | A grader aimed at a file fails when the file is missing; it never passes vacuously. | tob (yara) | described | TAKEN | SKILL §3 L50. |
| T42 | Graders on one case must agree on what is allowed (a conflict gave PASS, FAIL, FAIL on identical runs). | tob (yara) | measured (one incident) | REFUSE | One yes/no check per mode with a written boundary (H14) prevents it; no separate rule. |
| T43 | Before reinstating a band check, confirm real runs land on both sides of it. | tob (yara) | described | COVERED | `testing.md` L37 (name the break). |
| T44 | Keep case names stable so stored results line up. | tob (yara) | described | TAKEN | REF "One item" L10: "stable, never reused". |
| T45 | Relay "capped, NOT converged" when a loop hit its cap; do not present it as success. | tob (skill-improver), sp | described | COVERED | `testing.md` L93 and `engineering-principles.md` L99. |
| T46 | Do not improvise the improvement loop inline: an inline fallback "fixed" a finding by weakening the guarantee. | tob (skill-improver) | described | TAKEN | SKILL §6 L80 (never edits the evaluator, items or thresholds). |
| T47 | Rejected findings are not re-litigated without new evidence. | tob (skill-improver) | described | COVERED | `judgement.md` L45. |

### 3.2 obra/superpowers and superpowers-evals

Fact-check note (factcheck-2 #3): the "prohibitions backfire" finding is scoped to shaping failures (wrong-shaped output); for discipline failures (the agent knows the rule and skips it under pressure) the same file recommends a prohibition plus a rationalisation table plus red flags. Our skill keeps that scope.

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| S1 | No skill without a failing test first, for new skills and edits: if you didn't watch an agent fail without the skill, you don't know it prevents the right failures; if the control doesn't fail, there is nothing to fix. | sp (testing-skills L11, writing-skills L582), sf | described | TAKEN | SKILL §7 L89 (compare with no skill); `testing.md` L5. |
| S2 | In the failing run, record the agent's rationalisations word for word. | sp | described | REFUSE | Skill authoring, not measurement. |
| S3 | Write just enough to address the failures seen, nothing for hypothetical cases. | sp | described | COVERED | `engineering-principles.md` L12 (YAGNI). |
| S4 | The best tests for discipline skills combine three or more pressures (time, sunk cost, authority, exhaustion). | sp (testing-skills L140) | described | GAP | SKILL §7 L89: when evaluating a discipline skill, the items put the agent under pressure, or the baseline never fails. |
| S5 | Scenarios force a choice, use real paths, make the agent act, leave no easy outs, and feel like real work, not a quiz. | sp, esk, n8n | described | TAKEN | SKILL §2 L35-36 (real items as first seen). |
| S6 | Meta-test the skill text; it is not bulletproof while the agent finds new rationalisations; don't test pure reference skills; test types per skill type. | sp | described | REFUSE | Skill authoring guidance. |
| S7 | Match the form of guidance to the failure: prohibitions produced clearly more of the unwanted content than a positive recipe (fully separated distributions) on shaping failures; discipline failures take a prohibition plus a rationalisation table. | sp (writing-skills L463-482), sf | measured | TAKEN | SKILL §7 L89, with the scope corrected by factcheck-2 #3. |
| S8 | No nuance clauses: one appended nuance clause took a recipe from consistent to noisy; exemption clauses don't scope. | sp (L475-476) | measured (within its skills) | REFUSE | A skill-writing finding, not an eval rule. |
| S9 | Micro-test with one fresh-context sample per call and the realistic full system prompt. | sp | described | GAP | Merged into A20. |
| S10 | Always include a no-guidance control. | sp (L582) | described | TAKEN | SKILL §5 L69. |
| S11 | Five or more repeats per variant; single samples lie. | sp (L583) | described | TAKEN | At 3 by default and 5 to classify a new item (SKILL §5 L70, §6 L78). See X18. |
| S12 | Read every flagged match by hand: template echoes and quoted counter-examples pass as hits. | sp | described | GAP | Merged into T17. |
| S13 | Variance is a metric: five interpretations across five repeats means the wording isn't binding. | sp, asio, edd | described | TAKEN | SKILL §5 L70 (pass^k shows unreliability). |
| S14 | The description must not summarise the workflow, or agents follow the description instead of the skill (tested). | sp | described | REFUSE | Skill authoring. |
| S15 | If a rule is enforceable with a regex or a validator, automate it. | sp | described | TAKEN | SKILL §3 L46. |
| S16 | Keep code tests and live model evals apart; only static gates run in public CI, live sweeps nightly or on demand. | sp (docs/testing.md), smash | described | TAKEN | SKILL description L3 (not for ordinary code tests) and §0 L20; the cadence is the repo's choice. |
| S17 | Delete an old test only when a scenario verifiably covers every assertion it makes. | sp | described | COVERED | `testing.md` L61 (layered tests after a refactor). |
| S18 | Re-scope honestly when the feared failure does not reproduce (25 of 25 baseline runs refused); fixture "tells" (fabricated hashes, mismatched counts) invalidate the baseline; a scenario passing 5 of 5 without the skill needs a human before any edit. | sp (sdd eval results) | measured | COVERED | `testing.md` L5: watch it fail "for the reason you expect". |
| S19 | Read the table honestly: the raw tool-call count did not drop (9.6 against 9.0). | sp | measured | COVERED | `engineering-principles.md` L95 (neutral is a revert). |
| S20 | The simulated user never sees the acceptance criteria or the checks; a fresh assessor gets the private criteria and indexed evidence; the user role stops on a rule that does not depend on the verdict, or it leads the witness. | sp (scenario-authoring) | described | GAP | Merged into F20. |
| S21 | Three verdicts: pass, fail, indeterminate ("could not support a grade"); a failed pre-check is indeterminate. | sp, inspect, day, must, nb, ls | described | TAKEN | SKILL §3 L49. |
| S22 | Acceptance criteria name the exact evidence and the file path for the grader, allow legitimate harness variants and close rationalisation escape hatches by name. | sp | described | TAKEN | SKILL §3 L47-48. |
| S23 | Acceptance criteria distinguish a partial pass. | sp | described | REFUSE | No partial credit (SKILL §3 L47). |
| S24 | Fence every turn of the agent under test; an unfenced grader prompt contaminates the experiment. | sp | described | TAKEN | REF L32 (delimiters, neutralised). |
| S25 | Hand-written ("elicited") fixtures run about 2x costlier and overstate the baseline. | sp (scenario-authoring L660-670 area) | measured (roughly) | TAKEN | Supports SKILL §2 L35 (items from the world). |
| S26 | Belt and braces: assert the same fact with a judge and a code check; disagreement is a triage flag. | sp | described | REFUSE | Doubles grading. SKILL §3 L46 picks code where the property is exact and a judge otherwise (`engineering-principles.md` L17). |
| S27 | Cost scenarios are measurement instruments; the criteria certify comparability, not a dollar threshold. | sp | described | TAKEN | SKILL §5 L73. |
| S28 | Put the trigger where the skill keys off (conversation or repo state). | sp | described | GAP | Merged into C8. |
| S29 | Probe the component you care about directly; an end-to-end check passes symptom patches. | sp | described | REFUSE | Conflicts with SKILL §3 L48 (outcome first); a component probe is diagnosis. |
| S30 | "X before Y" passes when Y is absent: pair it with a positive check; a negative check treats an empty capture as fail or indeterminate. | sp (scenario-authoring) | described | TAKEN | SKILL §3 L50. |
| S31 | Tiers: a cheap sentinel smoke, a full run, ad hoc runs. | sp | described | TAKEN | SKILL §0 L20. |

### 3.3 wshobson/agents, agentskills.io, AWS

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| P1 | No eval harness, no fine-tune. | wsh | claimed | REFUSE | Fine-tuning is out of scope. |
| P2 | Open-code at least 100 traces into 4 to 8 buckets; fewer means too shallow, more means merge; a single-surface task may have 1 or 2. | wsh | claimed | REFUSE | The count is what saturation gives (H13). |
| P3 | One grader per bucket; a blended score hides which bucket regressed. | wsh | claimed | TAKEN | SKILL §3 L47. |
| P4 | Pin the judge snapshot and recalibrate on a judge change and quarterly regardless (Latitude: every 4 to 6 weeks). | wsh, lat | claimed | TAKEN | The pin and the recheck on change are SKILL §4 L63 and §6 L83. The calendar recheck is refused: a pinned judge does not change on a calendar. |
| P5 | The judge comes from a different model family. | wsh | claimed | TAKEN | Partly: REF L30 asks for a different model. See X11. |
| P6 | Below the bar the judge is advisory and never gates; never lower the bar to pass it. | wsh | claimed | TAKEN | SKILL §4 L62 and §6 L80. |
| P7 | A common starting bar is 0.85 on both rates. | wsh | claimed | TAKEN | At 0.8 (X4). |
| P8 | An all-code harness says "Judge calibration: N/A" rather than inventing a subjective criterion. | wsh | described | COVERED | `testing.md` L93. |
| P9 | The baseline file is the gate: no baseline, no comparison. | wsh | described | TAKEN | SKILL §5 L69. |
| P10 | Never let a run script write into the eval folder (a fixed measuring stick against disposable runs). | wsh | described | TAKEN | SKILL §6 L80. |
| P11 | Every holdout id stays out of the training data, by id. | wsh | described | TAKEN | SKILL §6 L80; REF `split`. |
| P12 | Rerun the same harness on the new checkpoint, not a looser one. | wsh | described | TAKEN | SKILL §5 L69 and §4 L63. |
| P13 | Timeouts and non-zero exits are both failures; never treat a hung process as a pass. | wsh | described | TAKEN | Partly: never a pass agrees with SKILL §3 L49; failure against unscored is X13. |
| P14 | Score multiple-choice drift items by log-probabilities rather than generate and extract. | wsh | described | REFUSE | Fine-tuning tooling. |
| P15 | Disclose when a judge or simulation layer is not validated against human labels; a triggering judge that predicts its own outcome, "activation" counted as any non-empty reply, and a trigger set with no negatives are anti-patterns. | wsh (plugin-eval) | described | TAKEN | SKILL §4 L62 (an unchecked judge is advisory) and §2 L40; the trigger half is C8. |
| P16 | agentskills.io: start with 2 to 3 cases; run with and without the skill (or the old version); a clean context per run; snapshot before editing; record tokens and duration; add assertions after the first outputs; require concrete evidence for a pass; review the assertions; blind comparison; remove assertions that always pass and investigate ones that always fail. | asio | described | TAKEN | Spread: A5, SC6, SC9, A20 (GAP), A30 (GAP), SC16 (GAP), T29. The `evals/evals.json` layout is refused as a file format. |
| P17 | AWS: four dimensions (safety, quality, triggering, cost) combined with weights 40, 40 and 20. | aws | described | REFUSE | A weighted composite hides which part moved (P3); the CLI is tool-specific. |

---

## 4. Vendor eval skills (repos.md part B)

Opik's error-analysis, eval-audit, validate-evaluator, write-judge-prompt and synthetic-data references are a port of the Hamel and Shankar skills, so their rules are merged into section 1 (repos.md's Opik rows 18 to 61 map to H rows) and do not count as independent evidence.

### 4.1 Langfuse and Opik

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| V1 | Never implement from memory; fetch the current docs first. | lf | described | COVERED | `research-sources.md` L127-141 (source authority). |
| V2 | Act as PM, analyst and teacher before executor; build only once the right solution is clear. | lf | described | COVERED | `judgement.md` L40 and SKILL §0. |
| V3 | Ask whether the user wants online or offline evaluation, and which decision it feeds; a useful metric names an observable behaviour, is measurable and changes a decision; challenge vague metrics. | lf | described | TAKEN | SKILL §0 L17 and §3 L47. |
| V4 | With no metrics online, run the user-feedback workflow first; present the metric set as one table and wait for confirmation. | lf | described | REFUSE | Tool workflow; SKILL §0's three lines are the lighter version. |
| V5 | Do not default to an LLM judge. | lf | described | TAKEN | SKILL §3 L46. |
| V6 | Before creating an online evaluator, fetch the matched observations and confirm none are scored twice; enforce scope with filters and sampling, not the judge prompt. | lf, ls | described | REFUSE | Online rule mechanics, tool-specific. |
| V7 | Name the score after what is measured ("refusal"), not the evaluator; name it for the user-facing concern ("ticket-grounding", not "Faithfulness"). | lf, dd, edd, lat | described | TAKEN | SKILL §3 L47 ("names the head node as the cause"). |
| V8 | Calibration data includes every outcome, including the known failures that prompted the calibration. | lf | described | TAKEN | SKILL §4 L59 (at least 10 of each verdict). |
| V9 | Leave a new judge's rule inactive until the user approves it; deploy only after approval, and confirm model, mappings, output definition and filters match what was calibrated. | lf, dd, bt | described | TAKEN | SKILL §4 L62-63; `engineering-principles.md` L21 (no risky automation). |
| V10 | Treat 85% overall accuracy as good if every category is acceptable. | lf | claimed | REFUSE | Conflicts with SKILL §4 L61 (two rates, never raw agreement). |
| V11 | Show all judge mistakes in a table of input, expected and actual. | lf | described | REFUSE | Presentation detail. |
| V12 | Show the prompt change before applying it; repeat until the user approves the judge. | lf | described | TAKEN | SKILL §4 L65. |
| V13 | The user does the open coding and supplies labels; do not do it on their behalf. | lf | described | TAKEN | SKILL §1 L27. |
| V14 | Run tool interactions yourself rather than telling the user to. | lf | described | COVERED | `judgement.md` L17 (be proactive). |
| V15 | Tool details: annotate the generation span under OpenTelemetry, one dataset per judge, exact-match boolean evaluators, versioned prompts. | lf | described | REFUSE | Tool-specific. |
| V16 | The smallest complete dataset version first, usually 5 to 12 high-signal items. | lf | described | TAKEN | SKILL §0 L20 (smoke check). |
| V17 | Model-generated expected outputs are not ground truth. | lf, bt, cal, dd | described | TAKEN | SKILL §2 L35. |
| V18 | Do not change the live dataset until the user approves its goal, source mix, schema and first draft; keep input, expected output and metadata apart. | lf | described | TAKEN | SKILL §4 L65; REF "One item". |
| V19 | In CI, ask which regression thresholds the user wants, and verify by running the new check. | lf | described | TAKEN | SKILL §0 L18; `testing.md` L80. |
| V20 | A dataset with no run, a judge with no scores, or a plan in prose is not success. | opik | described | COVERED | `testing.md` L76-93 (a claim and its evidence). |
| V21 | Stop at the first real blocker and return exactly one next step. | opik, lat | described | REFUSE | Interaction style. |
| V22 | Change no application code; the only file written is a runner outside the repo. | opik | described | REFUSE | Our standing suites live in the repo and gate CI (SKILL §0 L20). |
| V23 | Store inputs verbatim and keep the source trace id; paraphrasing the input is an anti-pattern. | opik, lf | described | TAKEN | REF "One item" L11 (`input` as it read at T) and L21 (`source`). |
| V24 | A missing judge key gave every item 0 with `scoring_failed`: a blocker, not a result. | opik | described (observed) | TAKEN | SKILL §3 L49 and §4 L64. |
| V25 | Name the worst items and the mode each hit. | opik, day ("report the failure mode, not just the rate") | described | TAKEN | SKILL §1 L28 and §5 L72. |
| V26 | Sampling mix: random, outliers, failure-driven, uncertain, stratified; combine error sampling with random sampling so the base rate stays visible. | opik, smash | described | TAKEN | SKILL §1 L26 (random plus known failures). See X25. |
| V27 | Flag few-shot examples drawn from the data used to measure the judge. | opik, cal, lat | described | TAKEN | SKILL §4 L60 (tune on train and dev, test once). |
| V28 | One or two yes/no assertions that would have failed on the bad trace and pass on a correct one. | opik (opik-test) | described | COVERED | `testing.md` L83 ("The regression test works: It failed with the fix reverted"). |
| V29 | Phrase judge questions positively: small judge models misread negatives. | opik (observed) | described | GAP | REF "Grader hygiene", one clause. |
| V30 | Dedupe on the source trace before inserting a regression case. | opik | described | TAKEN | REF "Arithmetic" L58 (same source and root cause count as one). |
| V31 | Do not report success from the insert call; read the item back. | opik, bt | described | COVERED | `testing.md` L84. |
| V32 | Aggregate scores alone are not a comparison: ask in order whether the runs are comparable, what broke, what got fixed, the net per metric, the worst rows, whether it is the app or the judge, cost, flakiness. | opik (opik-compare), arize | described | TAKEN | SKILL §5 L72-73. |
| V33 | Same suite, version, judge model and runs per item as the baseline; vary only the thing under test; with no prior run, this run is the baseline. | opik | described | TAKEN | SKILL §5 L69; `engineering-principles.md` L93. |
| V34 | A safety regression blocks with no exceptions, even on thin evidence; never fold a hard requirement (safety, privacy, legal) into a weighted or averaged score. | opik (opik-verify), oj | described | GAP | SKILL §6 L78: make a safety mode a regression item from day one, so the noise rule (§5 L71) can never wave it through. |
| V35 | Verdicts are `ship`, `hold`, `needs_review` or `insufficient_evidence`, from a versioned policy file with defaults (10 items minimum, 0 regressions, cost and latency +25%). | opik | described | REFUSE | Extra vocabulary and a policy file add parts (`engineering-principles.md` L17); the defaults are arbitrary. SKILL §0 L18 and §5 L71 give the same decision. |
| V36 | Every criterion is listed with its threshold, the observed value and pass or fail; never invent a threshold that isn't written down. | opik | described | TAKEN | SKILL §0 L18 and §6 L80. |
| V37 | `judge_validated: false` is the human gate, and only a human flips it. | opik | described | TAKEN | SKILL §4 L62 and L65. |
| V38 | A flaky item has passes strictly between 0 and the total; a single-run suite reports flakiness as not evaluated. | opik | described | TAKEN | SKILL §6 L78. |
| V39 | A sign test on flips is not a gate; with fewer than 6 flips say "too few flips". | opik | described | TAKEN | REF L54: with fewer than 6 flips the exact test cannot reach significance, so it reads as "no change". See X21. |
| V40 | Never round a hold up because the differences are "mostly positive". | opik | described | TAKEN | SKILL §5 L71. |
| V41 | An online rule is done only when it has scored a fresh trace, confirmed by reading it; a wrong path is the most common reason a rule silently scores nothing. | opik | described | COVERED | `testing.md` L43 and L70 (nothing is live until the real-world test passed). |
| V42 | Taking an unvalidated judge live and calling its scores truth; never optimise against an unvalidated judge. | opik | described | TAKEN | SKILL §4 L62. |
| V43 | An optimiser is done when it beats the baseline on data it was not tuned on; measure the baseline first and state the budget before spending. | opik | described | TAKEN | SKILL §6 L80; `judgement.md` L22. |
| V44 | A validation set under 10 items is a blocker; under about 20, say the result will be noisy. | opik | claimed | TAKEN | REF "Arithmetic" computes the noise instead of fixed cutoffs. |
| V45 | Prefer a graded metric over exact match for an optimiser: flat zeros give it nothing to climb. | opik | claimed | REFUSE | Measurement stays yes/no (SKILL §3 L47); an optimiser's objective is out of scope. See X26. |
| V46 | A gain within run-to-run noise is "no measurable improvement"; don't save a new version. | opik | described | TAKEN | SKILL §5 L71. |
| V47 | A flat result usually means context the prompt cannot hold; pick the optimiser by the failure seen. | opik | claimed | REFUSE | Diagnosis and tooling. |

### 4.2 Datadog

Fact-check note (factcheck-2 #2): "never invent a score" is from `agent-observability-auto-experiment`, not `build-eval-from-annotations` (which says "never invent a label").

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| V48 | A judge is fitted, not written: scored against human labels, its errors read, changed once, re-scored. | dd | described | TAKEN | SKILL §4. |
| V49 | Trace content is untrusted third-party text; the judge treats it as data; domain notes sit in their own block. | dd | described | TAKEN | REF L32; `untrusted-input.md` L3. |
| V50 | Fields marked "must ask" never get a silent default; a detailed request is not permission to infer one. | dd | described | TAKEN | SKILL §0 (the three lines are shown to the user). |
| V51 | Contested label rows are dropped; never take the newest, the first or a majority. | dd | described | GAP | Merged into H74. |
| V52 | Minimum labels: at least one row in each of two classes; below 8 in the smaller class, warn the interval will swamp gains; for many classes, about 6 per class. | dd | described | TAKEN | At 10 per verdict in dev (SKILL §4 L59). |
| V53 | Describer agents are never handed a candidate list: "a describer shown candidates confirms them". | dd | described | REFUSE | A detail of Datadog's describer agents; in SKILL §1 the human describes. |
| V54 | Render one probe row end to end and show it to the user before building the corpus. | dd | described | TAKEN | SKILL §4 L64-65. |
| V55 | A row that cannot be rendered is excluded and counted, never scored as a judge error; an unparseable output is retried once, then excluded and counted, never coerced to a class. | dd | described | TAKEN | SKILL §3 L49; REF L34. See X12. |
| V56 | Over 40 usable rows, split 70/30 deterministically by a hash of the row id; at 40 or fewer, no split and say the score is in-sample. | dd | described | TAKEN | Partly: a fixed split is SKILL §4 L60; the no-split rule is refused (AH9, X6). |
| V57 | Three judge framings (replicator, grader, corrector); never infer the framing from the label name; a corrector shown the app's answer tends to agree with it. | dd | described | GAP | Merged into A8. |
| V58 | Never assume accuracy: for skewed yes/no labels use balanced accuracy or minority F1; categorical labels macro-F1 or kappa; numeric labels MAE or Spearman. | dd | described | TAKEN | The yes/no half is SKILL §4 L61 (two rates); our judges are yes/no, so the rest does not apply. |
| V59 | Report the confusion matrix, Wilson interval, flip rate, constant-class baseline and confidence calibration; a judge that cannot beat the constant baseline has learned nothing. | dd | described | TAKEN | Partly: Wilson and two rates are SKILL §4 L61; the constant baseline is AX7 and the flip rate D23. |
| V60 | Judge output `{label, reasoning, confidence}`; confidence is reported, never used to decide, and anchored or the judge says 95 to everything. | dd | described | REFUSE | A confidence field adds nothing to yes/no plus "unknown" (REF L31). |
| V61 | Run each row an odd number of times (default 3) at temperature 0; the majority is the prediction and disagreement is the flip rate. | dd | described | GAP | Merged into D23. |
| V62 | One focused change at the largest bucket per round; keep it only if the headline improves and a mechanism audit passes (gained more than lost, gain in the targeted bucket, no class collapsed). McNemar labels confidence; it is not the keep gate. | dd | described | TAKEN | SKILL §5 L72 (fixed against broke) and `engineering-principles.md` L93. The McNemar point is X21. |
| V63 | `min_delta = max(0.02, 0.5 × run_stdev)`. | dd | claimed | REFUSE | An arbitrary constant; REF computes the noise. |
| V64 | Stop on max iterations, three worse in a row, the ceiling, or three unscorable runs; plateau on three non-significant or five "no change" rounds. | dd | described | COVERED | `judgement.md` L27-31. See X19. |
| V65 | The holdout is opened exactly once and is the headline; say plainly if it is materially worse. | dd | described | TAKEN | SKILL §6 L80. |
| V66 | State what the judge still gets wrong, in the humans' terms. | dd | described | TAKEN | SKILL §4 L61 ("in plain words"). |
| V67 | Never write a judge rule that names specific rows. | dd | described | COVERED | `engineering-principles.md` L83. |
| V68 | A judge prediction that disagrees with the human label is wrong; flag suspect labels as findings. | dd | described | GAP | Merged into H72. |
| V69 | A dataset's `expected_output` is not ground truth (an identical output and expected were marked fail by a reviewer); production outputs are a behaviour baseline, never truth; never write predictions back into the label queue. | dd | described | TAKEN | SKILL §2 L35 and L38. |
| V70 | Categorical equality is set equality; partial credit only through a match mode the user chose. | dd | described | REFUSE | No partial credit (SKILL §3 L47). |
| V71 | Report the "fidelity gap" between the judge measured locally and the one deployed (template variables can drop evidence); probe that the target has live traffic before promising an online evaluator. | dd | described | GAP | Merged into H53. |
| V72 | Every score comes from running the code; inventing scores is forbidden; never fabricate outputs instead of calling the real model. | dd (auto-experiment), arize, bt | described | COVERED | `engineering-principles.md` L99. |
| V73 | Running `claude -p` at 12 workers used 62 GB of RAM; cap at 4 to 6. | dd | measured (one incident) | REFUSE | Tool-specific. |
| V74 | A single run is a noisy estimate: report mean ± standard deviation over R runs, test on the standard error of the difference, never on a raw standard-deviation band. | dd | described | TAKEN | SKILL §5 L70; REF L54 (paired test). |
| V75 | Score every scoreable trace; never subsample; exclude non-target traces rather than score them 0. | dd | described | TAKEN | SKILL §3 L49. |
| V76 | Split once per run, never re-split, and assert validation plus test equals the corpus. | dd | described | TAKEN | SKILL §6 L80. |
| V77 | Failure census in two phases (describe without vocabulary, then group), recording how many failures exist and how many were described. | dd | described | TAKEN | SKILL §1 L27-28. |
| V78 | Every iteration names the bucket it targets; an unreachable dominant bucket is a finding; probe cheaply that a lever can move a failing item before the full run. | dd | described | COVERED | `engineering-principles.md` L92 (find the bottleneck, not the suspect). |
| V79 | Prefer a deterministic ground-truth metric to a judge; human labels beat judges. | dd | described | TAKEN | SKILL §3 L46. |
| V80 | A judge used as the scorer runs 5 or more times, pinned; its default model is the session's model. | dd | described | REFUSE | Using the session's model conflicts with REF L30 when that model is under test. The pin is TAKEN in H57. |
| V81 | Build the harness once and reuse it verbatim; no score literals in the file; never edit outside the files to optimise; never invent, extend or narrow the metric. | dd | described | TAKEN | SKILL §6 L80. |
| V82 | Denominator guard: a higher mean from fewer scored items is an artifact (an observed +0.1). | dd | described (observed) | TAKEN | SKILL §5 L69 and L72 (paired on the same items) and §3 L49 (unscored counted). |
| V83 | Quartiles by nearest rank, with counts of n, zero and perfect. | dd | described | REFUSE | A statistics detail with no decision behind it. |
| V84 | Cost estimates come from data and live price pages, never from memory; if nothing beat the baseline, do not fabricate an improvement. | dd | described | COVERED | `research-sources.md` L127-141 and `engineering-principles.md` L99. |
| V85 | Map existing eval coverage before proposing new evaluators. | dd | described | COVERED | `engineering-principles.md` L29 (is it already in this codebase?). |
| V86 | Aim for 8 to 15 evaluators and let the user curate (the old cap of 4 to 6 was "too tight"). | dd (eval-bootstrap) | claimed | REFUSE | One check per observed mode, no count (SKILL §1 L28). See X23. |
| V87 | Scope test: span only if no other span could change the verdict, otherwise trace, and session only when a probe shows sessions span traces. | dd, arize, bt | described | REFUSE | Tracing-tool scope; our items are whole runs (REF "One item"). |
| V88 | Write criteria that generalise beyond the sampled traces; under 5 supporting traces an evaluator is tentative; every evaluator cites a trace. | dd | described | TAKEN | SKILL §1 L27 (about five notes before searching) and L28. |
| V89 | Scrub personal data from trace content in judge prompts or files. | dd | described | GAP | Merged into AB8. |
| V90 | Never auto-advance between phases. | dd | described | TAKEN | SKILL §4 L65. |
| V91 | Classify metrics as always zero, perfect, saturated or struggling before analysis; never infer a metric's meaning from its name. | dd | described | TAKEN | SKILL §5 L74 and §2 L42. |
| V92 | Datadog's own analyser judge scores 0 to 10 on three dimensions. | dd | described | REFUSE | A counter-example to the yes/no rule; conflicts with SKILL §3 L47. |

### 4.3 Arize, Braintrust and LangSmith

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| V93 | With no evaluator type given, sample real spans and propose 1 to 3 evaluator ideas, each with a yes/no label pair; the user picks. | arize | described | TAKEN | SKILL §1 and §3. |
| V94 | Validate a new evaluator on a small backfill (about 100 historical spans) before continuous monitoring. | arize | described | TAKEN | SKILL §4. |
| V95 | Don't guess field paths; pull a sample and inspect what is actually there; use more than one sample, because projects have several schemas and errored runs. | arize, ls | described | COVERED | `testing.md` L43 (build fakes from a real captured value). |
| V96 | Keep temperature low; include explanations during setup to check the judge's reasoning. | arize | described | TAKEN | REF L30; the reasoning half is H50. |
| V97 | Never read `.env` files or search the filesystem for credentials. | arize | described | COVERED | `research-sources.md` L89 (never print secrets) and `engineering-principles.md` L22. |
| V98 | Arize tool details: label-only output, generic variables wired by mapping, a 1 to 2 hour index lag, prompt optimisation that never adds placeholders. | arize | described | REFUSE | Tool-specific. |
| V99 | Overfitting appears only in troubleshooting ("make few-shot examples synthetic"). | arize | described | REFUSE | Weak; SKILL §6 L80 covers holdouts. |
| V100 | Look for latent failures in tool outputs (exit codes, "not found", retry loops) when there are no scores yet. | bt | described | TAKEN | SKILL §1 L26 (read every tool call and result). |
| V101 | Taxonomy buckets: hard failures, soft inefficiencies, and non-quality failures to exclude; each entry becomes the spec for a scorer. | bt | described | TAKEN | SKILL §1 L28. |
| V102 | Each row holds everything needed to replay offline, with the baseline output and source trace id in metadata; never eval against live mutable data as the main loop. | bt | described | TAKEN | REF "One item" (frozen) and SKILL §2 L36. |
| V103 | Share one `categorize` function between the dataset pipeline and the scorers. | bt | described | REFUSE | The answer key and the grader then agree by construction; `testing.md` L40 (expected values typed out, never recomputed). See X29. |
| V104 | Scorer set: a yes/no hard-quality north star, an issue count, beats-baseline, avoids-primary-issue, soft efficiency; never trade the hard score for the soft one. | bt | described | TAKEN | Partly: SKILL §5 L73 (report what got worse); an issue-count score is refused (not yes/no). |
| V105 | Normalise mid-conversation histories (orphan tool results) before replay. | bt | described | REFUSE | Tool detail. |
| V106 | A bounded smoke run first; the full run once it is directionally better. | bt | described | TAKEN | SKILL §0 L20. |
| V107 | When you add a prompt rule, add or adjust the category that detects its violations. | bt | described | TAKEN | SKILL §6 L82. |
| V108 | Only after the offline loop is healthy, add online scorers and feed flagged traces back. | bt | described | TAKEN | SKILL §6 L82; monitoring is M4. |
| V109 | Read-only discovery before clarifying questions. | bt | described | COVERED | `judgement.md` L17 and L40. |
| V110 | Default to cheaper judge models and escalate if they are inaccurate. | bt | claimed | TAKEN | Neither default: any judge model is allowed and must pass §4's two rates. See X11. |
| V111 | Return classes from the judge, not numbers, and map classes to scores. | bt | described | TAKEN | SKILL §3 L47. |
| V112 | Test the evaluator before saving and again after; activation and historical rewind are separate authorisations; estimate the volume first. | bt | described | COVERED | `testing.md` L84 and `engineering-principles.md` L21. |
| V113 | Compute a pattern's frequency against a separately defined comparable population, excluding evaluator-generated traces. | bt | described | TAKEN | Partly: REF item 5 (rates from a random sample). |
| V114 | Each evaluator returns one metric. | ls | described | TAKEN | SKILL §3 L47. |
| V115 | Offline evaluators see the run and the reference; online there is no reference, so production needs referenceless checks. | ls, deepeval | described | GAP | Merged into M4. |
| V116 | Capture the tool name at execution time, not definition time; match run output to the dataset schema. | ls | described | REFUSE | Tool detail. |
| V117 | A passing test proves the evaluator runs; calibration shows it measures the right thing. | ls | described | TAKEN | SKILL §4. |
| V118 | Monitor and tell apart evaluator bugs, wrong filters, judge ambiguity, app failures and infra failures; never relabel an evaluator defect as a product failure. | ls | described | GAP | Merged into AH14. |
| V119 | Recheck calibration after prompt, model, mapping or traffic-schema changes. | ls | described | TAKEN | SKILL §4 L63. The traffic-schema half is H53. |
| V120 | "When in doubt, start with an LLM judge." | ls | claimed | REFUSE | Conflicts with SKILL §3 L46. See X10. |
| V121 | Skill evals: write the oracle before anything else; a reference solution that cannot pass proves the checks are wrong; run it twice. | ls (HANDOFF.md L62) | described | TAKEN | SKILL §4 L64. |
| V122 | Treat the auto-invocation gate as the main signal and the reward as a correctness canary. | ls (L71-72) | described | GAP | Merged into C8. See X17. |
| V123 | Never infer an infrastructure fault from timing or by scanning the agent's text; identify it from the exception type or the error field. | ls (L73), he | described | GAP | SKILL §3 L49, one clause on how a run is judged unscored. |
| V124 | Verifiers score from live system state only, never from a regex over the source. | ls | described | TAKEN | SKILL §3 L48. |
| V125 | Design the fixture so any sensible metric must rank the wrong case lowest, and assert the ordering, not a metric. | ls (task.toml) | described | REFUSE | Specific to evaluating an eval-building skill. |
| V126 | Keep a table of reward hacks per task and where each one dies (hand-written results, a constant-score evaluator, fixing the app). | ls (task.toml) | described | GAP | Merged into D84. |
| V127 | An infra failure is an invalid run (exit 3), not reward 0. | ls | described | TAKEN | SKILL §3 L49. The exit codes are tooling. |
| V128 | When the fixture is the skill's own example, the task rewards recall, not transfer. | ls | described | TAKEN | SKILL §2 L39 (seed items are open-book). |

---

## 5. Community eval skills (repos.md part C)

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| C1 | Declare tasks, repeats and per-task predictions before you run. | nb | described | TAKEN | Partly: SKILL §0 L18 pre-registers the pass rule; per-task predictions are not asked (AC4). |
| C2 | A negative-control ("harm") task is required: without it, the cheapest way for a skill to pass is to fire on everything; both arms are needed, because a harness that always reports null passes the placebo arm. | nb, mcpj ("cannot distinguish chose correctly from always calls something") | described | TAKEN | SKILL §2 L40 and §5 L69. |
| C3 | Never print a per-task difference without its interval (Wilson per arm, Newcombe on the difference). | nb | described | TAKEN | REF "Arithmetic" (Wilson; the paired exact test instead of Newcombe). |
| C4 | Never average over tasks at ceiling: "+26.7 points is (80 + 0 + 0) / 3"; no average over fewer than two discriminating tasks. | nb (failure 10) | measured (a worked case) | TAKEN | SKILL §5 L74. |
| C5 | A verifier pattern lifted verbatim from the skill's own text is caught at preflight; graders built from the treatment arm's answers measure whether that arm can read. | nb (failure 1) | described | TAKEN | SKILL §2 L39 (seed items are open-book) applied to graders. |
| C6 | Report classes CONFIRMATORY, EXPLORATORY and VOID; exploratory is not a failure. | nb | described | REFUSE | Extra vocabulary; SKILL §5 L71 ("no change") does the job. |
| C7 | A result is VOID when a cell has fewer than max(3, 80% of repeats) graded runs. | nb | described | TAKEN | Partly: SKILL §3 L49 counts and reports unscored runs, and §4 L64 fixes the grader past 1 in 10; no void threshold. |
| C8 | Evaluate triggering apart from behaviour, because a skill can give excellent advice and never activate. Build the trigger set from real requests with near-miss negatives (prompts written from the description measure string similarity), hold some positives out, observe actual loading (not "would you load this skill?"), and keep trigger checks from moving the behaviour score. In Trail of Bits' variant-analysis evals the skill fired on 0 of 3 inline-panel cases and on 2 of 3 and 3 of 3 cases with files on disk: case shape decides triggering. | nb (README, failure 6), tob (variant-analysis, yara), anth (skill-creator L339-400, hillclimb L80, L271), sf, ls, rsc, sky, wsh, sp, cct | measured | GAP | SKILL §7 L89, under "Evaluating a skill": one bullet on triggering. Today the skill evaluates a skill only once it is loaded. See X17. |
| C9 | The judge is never told which arm produced the reply and never sees the skill; it does not reward vocabulary, framework names, formatting or confidence. | nb | described | GAP | Merged into SC16 and A8. |
| C10 | "Failed" means no answer, not a wrong answer: the run leaves the denominator; dead runs counted as failures are a fabricated observation. | nb (failure 8), he | described | TAKEN | SKILL §3 L49. |
| C11 | An unparseable judge output is a graded FAIL, so a judge that reliably waffles cannot shrink the batch. | nb, sf ("fail closed") | described | REFUSE | Conflicts with REF L34 (unscored). Our guard against a shrinking batch is C7 and SKILL §4 L64. See X12. |
| C12 | Known-pass and known-fail canaries before any real run, using the registered rubric (never a copy), one sandbox per canary call. | nb | described | TAKEN | SKILL §4 L64. |
| C13 | You cannot write a canary for a mistake you would also make (a same-family judge); this is open. | nb (failure 3) | described | TAKEN | Partly: REF L30 asks for a different model. See X11. |
| C14 | Publish the judge's misgrade rate rather than assume it away: 1 in 40 live misgrades against 0 in 63 canaries. | nb (failure 4) | measured | TAKEN | SKILL §4 L61 (report both rates on held-out labels). The numbers show canaries alone overrate a judge. |
| C15 | An effect that shrinks as power rises is the signature of noise (−25 points at n=8, −5 points at n=20). | nb (failure 7) | measured | TAKEN | SKILL §5 L71. |
| C16 | A cell that matters should agree across two batches before it is published (open). | nb (failure 9) | described | TAKEN | SKILL §5 L70-71 (repeats and noise). |
| C17 | Pre-registration freezes the criterion but cannot supply the judgement. | nb (failure 12) | described | TAKEN | SKILL §0 L18 and §4 L65 (a person signs off). |
| C18 | Every run appends one entry to a git-tracked ledger, including voided and flat runs. | nb (failure 13), sman ("what did not ship, published") | described | COVERED | `engineering-principles.md` L96: "Log every attempt, kept and reverted." |
| C19 | Deterministic graders where possible, model graders where necessary, human graders to validate. | edd | described | TAKEN | SKILL §3 L46 and §4. |
| C20 | Tool-call presence is fair game; tool-call ordering usually isn't; don't force one exact sequence when several safe paths work. | edd, must, ls, promptfoo | described | TAKEN | SKILL §3 L48. |
| C21 | Dimensions come from the agent's promises: one line per surface, "what it promises, the observable signal"; every scenario hits a named promise. | edd | described | TAKEN | Partly: SKILL §0 L17 states the question; modes still come from read failures (§1). See X30. |
| C22 | Decide up front whether 0 means "failed" or "failed or not applicable". | edd | described | TAKEN | SKILL §3 L49: not applicable or unscored is its own state, never a 0. |
| C23 | Picking the evaluator after the experiment runs is an anti-pattern. | edd | described | TAKEN | SKILL §0 L18. |
| C24 | Fixed scenario counts (5 to 8 baseline scenarios; a mix of 30 happy, 20 wording, 15 edge, 15 adversarial, 10 multi-turn, 10 negatives). | edd | claimed | REFUSE | Arbitrary mixes (`engineering-principles.md` L7). |
| C25 | Reject unbounded plurals ("all", "every") in scenarios; cap every list-returning query. | edd | described | REFUSE | Domain detail. |
| C26 | Keep intents stable and generate several phrasings per intent; aggression levels matched to the change. | edd | described | REFUSE | Synthetic generation (H78). |
| C27 | Write messages as a real user would type them, not as a test engineer would. | edd, esk | described | TAKEN | SKILL §2 L36 (the input as first seen). |
| C28 | Smoke-check that judges "land" on 3 to 5 traces before scaling: "Judges that don't land on 5 traces won't land on 500". | edd | described | TAKEN | SKILL §4 L65. |
| C29 | One red is not a confirmed failure; rerun the same scenarios once before acting; deltas are more reliable than absolutes. | edd | described | TAKEN | SKILL §5 L69-70. See X20. |
| C30 | Filing a judge as miscalibrated on one trace is an anti-pattern; it takes at least 3. | edd | claimed | REFUSE | SKILL §4 measures the judge's rates on held-out labels, not by counting anecdotes. |
| C31 | A symptom-to-fix table (an empty search leads to hallucination: fix the tool's docstring). | edd | described | REFUSE | Diagnosis. |
| C32 | "Hand-curated golden outputs" are an anti-pattern; use real traces. | edd | claimed | TAKEN | SKILL §2 L35 (answer key from the world). See X14. |
| C33 | Reuse evaluators before creating them, matching by rubric, not by name. | edd | described | COVERED | `engineering-principles.md` L29. |
| C34 | Seven steps in order: annotate, discover issues, pick eval type, build judge, align, golden set, regression run. | lat | described | TAKEN | SKILL §1 to §6 follow the same order. |
| C35 | "Don't sample randomly": prioritise flagged outputs, edge cases and hedged answers. | lat | claimed | REFUSE | Conflicts with SKILL §1 L26 and REF item 5 (rates need a random sample). See X25. |
| C36 | The reasoning is worth more than the score; investigate reviewer disagreement, never average it. | lat | claimed | TAKEN | SKILL §1 L27; the disagreement half is H74. |
| C37 | Flag when over 30% of annotations lack reasoning or 80% share one score; analyse up to 200 entries for 3 to 8 issues; warn when over 30% of logs are multi-turn. | lat | claimed | REFUSE | Arbitrary thresholds. |
| C38 | Cluster by cause, not symptom; name issues like bugs; mark issue lists written only by a model as unvalidated. | lat | claimed | TAKEN | SKILL §1 L27; the merge test is H10. |
| C39 | "If you can explain the check to a regex, use a rule; if you'd have to explain it to a person, use a judge"; rules can't measure meaning. | lat, cal ("words like 'correctly' need a judge") | claimed | TAKEN | SKILL §3 L46-47. |
| C40 | Composite check: run the rule first and the judge only if the rule flags. | lat | described | REFUSE | A cost shortcut that misses what the rule doesn't flag; YAGNI. |
| C41 | Use the smallest prompt edit that addresses the root cause; don't rewrite the whole judge prompt. | lat, cal | claimed | COVERED | `engineering-principles.md` L93 (change one thing). |
| C42 | "Generic evals are worse than no evals." | lat | claimed | TAKEN | SKILL §3 L47 (checkable claims per mode). |
| C43 | Inspect before advising; every finding cites an artifact actually read. | lat, opik | claimed | COVERED | `engineering-principles.md` L69. |
| C44 | Golden-set entries need explicit developer approval; passing evals are necessary but not sufficient. | lat | claimed | TAKEN | SKILL §4 L65; `testing.md` L63-70 (the real-world test). |
| C45 | Coverage before volume: common cases, edge cases, fixed failures, rare high-stakes cases. | lat | claimed | TAKEN | SKILL §2 L40-41. |
| C46 | Regressions are the only hard stop; one pass-to-fail flip means "do not deploy". | lat | claimed | TAKEN | Partly: SKILL §6 L78 blocks on regression items; a single flip elsewhere is noise (§5 L71). |
| C47 | Updating the baseline is a deliberate decision, made in the PR that means to move it. | lat, rsc | described | GAP | SKILL §6, one clause: a standing suite's baseline changes only in a change that says so. |
| C48 | "Measurement errors first, then product errors": while the measurement lies, every product finding is a phantom; the ground truth is suspect too. | smash | claimed | TAKEN | SKILL §2 L38 and L42, §4 L64. |
| C49 | A missing key or a timeout must never look like "nothing found". | smash | claimed | TAKEN | SKILL §3 L49. |
| C50 | Deterministic parts of a hybrid pipeline get a 100% bar; thresholds only for the model stages. | smash | described | COVERED | `testing.md` (ordinary tests) and SKILL description L3. |
| C51 | Store raw events, not rebuilt ones; mark reconstructions as synthetic. | smash | described | TAKEN | REF "One item" L20 (`not_recordable`). |
| C52 | "Forbidden" values are often a sturdier contract than exact values. | smash | claimed | REFUSE | A negative check needs its positive partner (SKILL §3 L50); no separate rule. |
| C53 | Start with one judge per business decision; split only when alignment stalls or consequences differ. | smash | claimed | REFUSE | Conflicts with SKILL §3 L47 (one judge per failure mode). |
| C54 | Aggregate several judges deterministically in code; never a mega-judge with five scores. | smash | claimed | TAKEN | SKILL §3 L47. |
| C55 | Fill the human label column before generating or viewing the judge's column. | smash | described | TAKEN | SKILL §4 L59 (label first, then build the judge). |
| C56 | Drift attribution: re-score a fixed human-labelled anchor set; if the anchor holds the system drifted, if it moves the judge drifted. | smash | described | REFUSE | Pinned judge versions (SKILL §6 L83) remove judge drift; a change is rechecked (§4 L63). |
| C57 | Every judge upgrade is a baseline reset. | smash, must ("eval migrations") | claimed | TAKEN | SKILL §4 L63. |
| C58 | Include prompt-injection cases for user-facing systems. | smash | claimed | TAKEN | SKILL §7 L87. |
| C59 | Model judges are too slow for synchronous guardrails; use a regex or classifier to block. | smash | claimed | REFUSE | Runtime guardrails, out of scope. |
| C60 | A result cache keyed on rubric version, item id and a hash of the output. | smash | described | TAKEN | Partly: SKILL §7 L88 (cache when only the grader changes); the key design is tooling, and `engineering-principles.md` L101 warns about keys that omit an input. |
| C61 | Gate on regression against a baseline, not an absolute floor ("absolute floors age"). | smash, rsc | described | TAKEN | SKILL §5 L69. |
| C62 | Two unverified claims in smashilp's tooling notes: Promptfoo is part of OpenAI, and OpenAI's Evals platform shuts down at the end of 2026. | smash | claimed | REFUSE | The first is unverified; the second is confirmed with exact dates in O8. Neither is a rule. |
| C63 | A skill is done when a fresh agent demonstrably does better with it than without it. | sf | described | TAKEN | SKILL §7 L89. |
| C64 | Baseline failures become the skill's test cases; generate the skill in a fresh context from only the spec and those failures. | sf | described | REFUSE | Skill authoring. |
| C65 | Green gate: no run with the skill shows a baseline failure; never weaken the scenario to pass. | sf, n8n ("sharpen assertions, never dull them") | described | TAKEN | SKILL §6 L78 and L80. |
| C66 | Ship the new version only if it wins or ties on every scenario and wins at least one. | sf | claimed | REFUSE | Ignores noise; conflicts with SKILL §5 L71-72 (paired test on fixed against broke). |
| C67 | Don't convene approval panels: same-model unanimity measures nothing; several similar judges are correlated evidence. | sf, must | described | TAKEN | REF L36 (a panel only when one judge misses the bar). |
| C68 | The live trigger check asks the model "Would you load this skill?". | sf | described | REFUSE | A self-report, not observed loading (C8). |
| C69 | Stratify the test set from simple to very complex. | neo | described | TAKEN | SKILL §2 L41 (ordinary and hard). |
| C70 | Direct scoring for objective criteria, pairwise for preferences; always swap positions and call a disagreement a tie; identical outputs in both slots must tie. | neo, rsc | described | TAKEN | REF L35. |
| C71 | Systematic disagreement patterns matter more than high overall agreement. | neo | claimed | TAKEN | SKILL §4 L61 (two rates show the direction). |
| C72 | Unsourced figures: reasoning first "improves reliability by 15 to 25%"; rubrics cut variance "by 40 to 60%" (repeated by harness-evolver). | neo, he | claimed | REFUSE | No source found. |
| C73 | Write the criteria before judging, give the judge the spec exactly, and reuse the same spec across retries ("changing criteria invalidates the comparison"). | neo | described | TAKEN | SKILL §0 L18 and §4 L63. |
| C74 | Never give the judge the score threshold. | neo | claimed | REFUSE | Unmeasured (nobody tested it); our yes/no judges have no threshold to give. |
| C75 | Anchor-relative rubrics: a failing and a passing excerpt that differ on one axis, bad first; drop any dimension the two score the same on. | neo | described | GAP | Merged into H14. |
| C76 | The judge drafts its own reference answer before reading the agent's work. | neo | described | REFUSE | A model-written reference conflicts with SKILL §2 L35. |
| C77 | "You have NO default score" (the newer judge) against "DEFAULT SCORE IS 2" (the older one); ambiguous evidence gets the lower placement. | neo | described | GAP | Merged into A30. |
| C78 | Use only the project's own build, test and lint commands; no inline verification scripts. | neo | described | COVERED | `engineering-principles.md` L29. |
| C79 | Debate among three judges for up to three rounds; agents agree too easily ("sycophancy in debate"); at most three retries, then escalate. | neo | described | REFUSE | Adds parts; REF L36 keeps panels to when one judge misses the bar. |
| C80 | Judge prompts that threaten the model ("you will be killed"). | neo | claimed | REFUSE | Unmeasured, and against our writing rules. |
| C81 | Pre-registered gates, hidden validators and a blind holdout wave written by people who never saw earlier results. | sman | described | TAKEN | SKILL §0 L18 and §6 L80-81 (the newest items as holdout). |
| C82 | Every number is rebuilt from raw records in CI. | sman | described | COVERED | Merged with AX32. |
| C83 | Output-token savings are not session savings; measure real sessions (81 paired sessions, with an interval). | sman | measured | COVERED | `engineering-principles.md` L99 (lab and field numbers are different; label which). |
| C84 | Rate-limited runs are infrastructure failures and are not scored. | he | described | TAKEN | SKILL §3 L49. |
| C85 | Pin the rubric text in each score comment; use human corrections as few-shot examples. | he | described | REFUSE | Tool detail; the frozen judge (SKILL §4 L63) does the pinning. |
| C86 | Choose the winner on held-out data. | he | described | REFUSE | Selecting on the holdout makes it a selection set (SKILL §6 L80). |
| C87 | Efficiency gate: reject when tokens more than double and the gain is under 2%; "stable" when the standard deviation is under 0.05. | he | claimed | REFUSE | Arbitrary numbers; the cost frontier (SKILL §7 L88) and pass^k replace them. |
| C88 | The same model family proposes and judges (a weakness). | he | described | TAKEN | REF L30, as the thing to avoid. |
| C89 | Rubric types: artifact, string or regex, behaviour or exit code, model judge; the grading agent must not know the author's expectations. | esk | described | TAKEN | SKILL §3 L46-48; the blind half is SC16. |
| C90 | Passing only with leaked context means the skill is not good enough. | esk | described | TAKEN | SKILL §3 L51. |
| C91 | Done: main, error and quick cases at 100%, trigger edge cases at 80% or more, no drop from the previous run. | esk | claimed | REFUSE | Arbitrary thresholds. |
| C92 | A forward test is a simulated demo and never replaces real use; feed real findings back. | esk | described | COVERED | `testing.md` L63-70 (the real-world test). |
| C93 | The harness refuses to finish with pending cases or cases without a rubric. | esk | described | TAKEN | SKILL §3 L50. |
| C94 | Four goal types: outcome, process, style, efficiency; deterministic checks first, then rubric, then build and runtime. | sky | described | TAKEN | SKILL §3 L46-48 and §5 L73. |
| C95 | Criteria are specific and testable ("creates good documentation" is not); keep process apart from outcome; include unclear and minimal-context edge cases. | notion | described | TAKEN | SKILL §3 L47-48 and §2 L40-41. |
| C96 | Structural checks measure conformance, not whether a skill improves reasoning; public claims need machine-linked artifacts. | cct | described | TAKEN | SKILL §7 L89; `engineering-principles.md` L99. |

---

## 6. Long-tail eval skills (repos.md part D)

Merged elsewhere: OpenJudge's RAG skill is H131; its four judge-prompt components are H50; its disagreement classes are H72; its "system, metric or data problem" split is AH14; its policy-first red-team rule is Y1.

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| D1 | No route without knowing the data form and label status; give a provisional recommendation at once; ask all the questions together; recommend exactly one next workflow. | oj (00-meta-eval) | described | COVERED | `judgement.md` L40 (options with one pick). The router is refused with H146. |
| D2 | Never call anything production-ready without labels and a checked judge; mark a first grader "UNVERIFIED". | oj (00, 08) | described | TAKEN | SKILL §4 L62. |
| D3 | Don't recommend a prompt-regression comparison until both the baseline and the candidate have run. | oj | described | TAKEN | SKILL §5 L69. |
| D4 | Strata of easy 50 to 60%, boundary 25 to 35% and adversarial 10 to 15%, at least 10 per stratum (30 in production), four quadrants per dimension, fewer than 5 per dimension flagged. | oj (01, coverage_check.py) | claimed | REFUSE | Arbitrary mixes (`engineering-principles.md` L7). The ordinary and hard split is SKILL §2 L41. |
| D5 | Template diversity: 5 prompts with 10 outputs each beat 1 prompt with 50, because outputs of one prompt are correlated. | oj | claimed | TAKEN | REF L56 (clustered intervals) and L58 (duplicates count as one). |
| D6 | Adversarial items come as near-misses, confounders and distribution shifts. | oj | described | TAKEN | Partly: SKILL §2 L40 (negatives); near-miss trigger items are C8. |
| D7 | A grader decision tree where the first match wins: a deterministic rule, a built-in model grader, an agent grader, code execution, an agentic grader. | oj (02) | described | TAKEN | SKILL §3 L46-47 keeps the order (code first); the five-level tree is not copied. |
| D8 | Anti-pattern scan: block a 1 to 5 scale, missing examples, missing output format, or a judge that is the target model; warn on a judge covering 3 or more dimensions, or pass and fail definitions under 20 words or using "good" or "quality". | oj (02) | described | TAKEN | Partly: scale, same model and many dimensions are SKILL §3 L47 and REF L30; examples and definitions are H50. |
| D9 | Don't use equal weights: set weights from prevalence and business impact. | oj (02) | claimed | REFUSE | We don't use weighted sums (SKILL §3 L47); hard requirements are V34. |
| D10 | Calibrated only at both rates of at least 0.8, both rates of at least 0.6 on the boundary stratum, at least 10 dev items per class, and a test-set drop under 10%. | oj (03 HARD-GATE, factcheck-2 #26) | described | TAKEN | SKILL §4 L59 and L62 (0.8 on both, 10 per class). The boundary-stratum and test-drop rules are not taken. |
| D11 | No reduction of human review without kappa of at least 0.6, overall and on boundary items; a four-phase roadmap from advisory to autonomous. | oj (03) | described | REFUSE | Human-reduction planning is out of scope; the advisory start is SKILL §4 L62. |
| D12 | Don't hand-write the statistics: run bundled, self-tested scripts (Wilson, paired test, pass^k, corrected rate) and report the numbers they return. The audit found "the methodology layer was sound; the audit just hadn't been run against the code". | oj (03, tests/eval_pipeline_skill_audit.md), stats (open question in branches.md) | described | GAP | A small self-tested helper next to REF (about 40 lines), so the agent runs the arithmetic instead of re-deriving it. |
| D13 | Report Gwet's AC1 beside kappa when classes are imbalanced. | oj | described | REFUSE | We report two rates for judges, not kappa. |
| D14 | Five judge-bias checks with thresholds: position (difference over 0.05), verbosity (correlation over 0.3), self-enhancement, progress illusion, label drift. | oj (03) | claimed (thresholds) | GAP | Merged into A8; the thresholds are not taken. |
| D15 | Self-evaluation inflates the true-positive rate by 3 to 8%. | oj (03) | claimed (no citation) | REFUSE | Uncited. The rule it supports is REF L30. |
| D16 | No recommendation without statistical evidence; no trend without at least two data points. | oj (04) | described | TAKEN | SKILL §5 L71. |
| D17 | Maturity is the minimum across dimensions (the weakest link). | oj (04) | described | TAKEN | Partly: H44 (fail-on-any for regression items); no maturity score. |
| D18 | Never declare a candidate better without a position-debiased (swapped) comparison and a bootstrap interval, with at least 10 samples per axis; verdicts BETTER, WORSE, TIED, INSUFFICIENT_EVIDENCE, INCONCLUSIVE. | oj (06, pairwise.py) | described | TAKEN | REF L35 and "Arithmetic". The verdict vocabulary is refused (V35). |
| D19 | Never report attack success without the paired over-refusal rate. | oj (07) | described | TAKEN | SKILL §7 L87: "report usefulness under attack beside attack success." |
| D20 | The attack generator and the safety judge are independent. | oj (07) | described | TAKEN | REF L30, by the same reasoning. |
| D21 | No principle without a source label saying where it came from. | oj (08) | described | COVERED | `engineering-principles.md` L69 and `research-sources.md` L59. |
| D22 | Skills are tested by an actor model following the skill and a separate, stronger judge model; actor and judge differ on purpose. Measured before and after (factcheck-2 #8): the 8-case smoke set went from 5 pass, 2 partial, 1 fail to 8 of 8; the 18-case suite at 3 repeats went from 16, 2, 0 to 17, 1, 0 after one fix. | oj (README, tests) | measured | TAKEN | SKILL §7 L89 and REF L30; this library's `evals/` folders. |
| D23 | Measure the judge's own variance: grade the same output 3 or more times and read the majority. Identical text scored 0.40, 1.00, 0.60 and 1.00 across runs; temperature 0 "reduces, but does not always eliminate" disagreement (Inspect). Flips on an unchanged output with a wavering reason are the judge, not the app. | oj (README L140, audit L88), anth (eval-audit L161), inspect, dd (flip rate), opik, neo, gepa | measured | GAP | REF "Grader hygiene" L30: temperature 0 and a seed are not enough; check flips on repeated grading during §4, and use a majority of 3 if they flip. |
| D24 | Ask the target and the autonomy level first, in one message, never defaulting silently; four gates (selection, shape, calibration, push); verdicts that flip a case's meaning are surfaced. | n8n | described | TAKEN | SKILL §4 L65 (sign-offs). |
| D25 | Share links, never bare ids, in anything a person reads. | n8n | described | REFUSE | Writing style, not an eval rule. |
| D26 | The strongest cases encode a real failure, not an invented premise. | n8n | described | TAKEN | SKILL §1 and §2 L35. |
| D27 | Write expectations from intent, then calibrate against a real build; transcribing one observed build into assertions overfits. | n8n | described | TAKEN | SKILL §2 L35 (the key never copies the agent's output). |
| D28 | Keep the conversation in the user's voice; naming the implementation in the prompt makes the expectations tautological. | n8n | described | TAKEN | SKILL §2 L36 and AX9. |
| D29 | Trim to the smallest multi-turn conversation that reproduces the issue, and note the trim. | n8n | described | REFUSE | Conflicts with SKILL §2 L36 (freeze the input as first seen). |
| D30 | Smoke-test the environment with one case before any batch. | n8n | described | TAKEN | SKILL §0 L20. |
| D31 | Calibrate by sharpening assertions, never by dulling them; if you can't picture a plausible wrong build that turns the case red, it is too loose. | n8n | described | COVERED | `testing.md` L37 (name the break); SKILL §6 L80. |
| D32 | Confirm the precondition fired, not just the green: negative and conditional assertions pass when the tool was never called. Three of five tool-misuse cases scored 100% on their first calibration run because the tool was never called. | n8n (SKILL.md L343-346) | measured | TAKEN | SKILL §3 L50. |
| D33 | First reproduce, then reclassify: a green on a sourced failure usually means the case never set up the situation. | n8n | described | COVERED | `testing.md` L5 and L9 (reproduce the bug in a failing test first). |
| D34 | Read the assistant text right before the failing call to find the real precondition ("find the turn, not the topic"). | n8n | described | REFUSE | Diagnosis. |
| D35 | Move the assertion to the first call, so a later self-correction does not hide the defect. | n8n | described | REFUSE | Conflicts with SKILL §3 L48 (grade the outcome first); checking the path is only for when the path is the requirement. |
| D36 | Cap the effort at about three attempts, then write the negative result into the case. | n8n | described | COVERED | `judgement.md` L31 (budget spent: write up what you have). |
| D37 | A red is signal: surface it, don't work around it, never weaken what the case checks; classify each red (capability gap, harness limit, real nondeterminism) and annotate kept reds with a greppable prefix. | n8n, novu | described | TAKEN | SKILL §6 L79-80. The classification is AH14. |
| D38 | Rule out the environment first: every case failing the same way is a broken environment. | n8n | described | GAP | Merged into AH14. |
| D39 | For a capability gap, propose a ticket, don't create one, and reproduce first. | n8n | described | REFUSE | An admin choice, out of scope for the skill. |
| D40 | Describe what each external service returns, not internal state; don't assert exact counts that depend on mock generation. | n8n | described | GAP | Merged into A33 (too strict). |
| D41 | Outcome expectations judge the artifact; process expectations judge the transcript; keep expectations free of internal mechanics (sub-agents, tool names, call counts). | n8n | described | TAKEN | SKILL §3 L48. |
| D42 | Size a check so every correct build passes and a wrong or lazy build fails (the substitution test); a behaviour case is worth shipping only if it would fail on the misbehaviour. | n8n | described | COVERED | `testing.md` L37. |
| D43 | If the conversation specified it, pin it; a check is too tight only when it pins what the user left open; negative scenarios assert graceful handling only where the prompt implied it. | n8n | described | GAP | Merged into AX24. |
| D44 | Calibration steps are run notes, not expectations; a verifier's failure category is a hint, not ground truth; write a targeted expectation even when an always-on check nominally covers it. | n8n | described | TAKEN | SKILL §2 L42 and §3 L47. |
| D45 | Under concurrency, attribute results by parsing the JSON results, not the interleaved log. | n8n | described | COVERED | Merged with AX32 (read the written rows). |
| D46 | Verify a finding from the trace analyser before trusting it: of 131 flagged candidates, 18 held up once paired with a "bad" verdict. | n8n (sourcing-cases.md) | measured | TAKEN | SKILL §1 L27 (the agent organises; the human decides) and `engineering-principles.md` L71. |
| D47 | Scrub real workflows into synthetic seeds, written not copied, with no customer names. | n8n | described | GAP | Merged into AB8. |
| D48 | Classify a timeout before blaming the case; rerun it alone. | n8n | described | GAP | Merged into V123 and AH14. |
| D49 | Don't run every probe by ritual; pick what answers the user's question; availability and fidelity before speed. | day | described | TAKEN | SKILL §0 L17 and §4 L64. |
| D50 | Pass API keys by environment variable name, never the value on the command line; keep private cases outside the skill bundle. | day | described | COVERED | `research-sources.md` L89 and `engineering-principles.md` L22. |
| D51 | Probabilistic features get repeats (default 10) and a three-state verdict: delivered, intermittent (k of N), not delivered. | day | described | TAKEN | SKILL §6 L78 and §5 L70. |
| D52 | Collect, then judge independently; never let the model grade itself. | day | described | TAKEN | REF L30. |
| D53 | Three blind judges, each told it judges in isolation, with a majority to pass. | day | described | REFUSE | A default panel; REF L36 uses one only when one judge misses the bar. |
| D54 | Compute precision per category: one category at 12.5% exposed a systematic misclassification. | day | measured (one case) | TAKEN | SKILL §2 L41 (split by source) and §3 L47 (a result per mode). |
| D55 | Silence is not consent: only an explicit verdict counts; an empty answer scores 0 and the judge may not abstain. | day | described | TAKEN | Partly: REF L31 ("unknown" is unscored, never a pass). "May not abstain" is X12. |
| D56 | Human-confirmed labels are never overwritten by a model; report the share not yet confirmed. | day | described | TAKEN | SKILL §2 L35. |
| D57 | Freeze category ids; only add new ones; never reuse a retired id. | day | described | TAKEN | REF L10. |
| D58 | When the rubric changes, re-judge only the plausibly affected cases and carry the rest forward (about a fifth of the cost). | day | described | REFUSE | Conflicts with SKILL §4 L63 (a changed judge is a new judge) and H99 (scores across grader versions do not compare). |
| D59 | Separate measured from inferred; an impossible number is an artifact; a negative claim needs an exhaustive search. | day | described | COVERED | `engineering-principles.md` L69 and L99; `research-sources.md` L59. |
| D60 | Output that hit the token limit is truncated, and its numbers are void. | day | described | GAP | Merged into AX14. |
| D61 | Identical conditions for comparisons, ideally the same time window; interleave the control inside the failure window. | day | described | GAP | Merged into AH10. |
| D62 | Calibrate the meter on the exact dimension you will read; the probe is a suspect too, so run it on a known-good control first. | day | described | TAKEN | SKILL §4 L64. |
| D63 | Canary facts must be neutral and external; a single time slice is not a steady state; averages flatten time structure. | day | described | REFUSE | Endpoint-probing details. |
| D64 | Change one axis at a time; a single-axis test rules out only that axis. | day | described | COVERED | `engineering-principles.md` L93. |
| D65 | Pass, fail and error are three states, and only a fail pages a person. | day, must | described | TAKEN | SKILL §3 L49. |
| D66 | Pre-register the verdict thresholds before the batch; an adversarial counter-review before sending; confidence tiers in reports. | day | described | TAKEN | Partly: SKILL §0 L18. The counter-review belongs to the review skills, and the tiers to `engineering-principles.md` L69. |
| D67 | Evaluate an agent as an asymmetric evidence cascade: deterministic hard rules first, then an independent semantic verifier, then an adjudicator, or hold. | must | described | TAKEN | Partly: SKILL §3 L46-47; the repair stage is an agent loop, not measurement. |
| D68 | Score the final environment state before the final text, and the trajectory as a separate dimension. | must | described | TAKEN | SKILL §3 L48. |
| D69 | Verdicts: a pass needs every hard gate and no confirmed violation; a fail needs a reproducible violation; everything else is held. | must | described | TAKEN | SKILL §3 L49 (three states). |
| D70 | Never let the generator certify its own repair; track false rejections and escaped defects separately. | must | described | TAKEN | REF L30 and SKILL §4 L61. |
| D71 | Three dataset roles kept apart (fixed regression, recent replay, generated exploration); never average an easy set over a regression in another. | must | described | TAKEN | SKILL §2 L41 and §6 L78. |
| D72 | Minimal contrast pairs and matched distractor pairs; hold out whole compositions. | must | described | REFUSE | Synthetic design detail (H78). |
| D73 | Promote a failure to regression only after a deterministic counterexample, independent confirmation or human review; quarantine flaky cases rather than weaken the gate. | must | described | TAKEN | SKILL §6 L78 and L82. |
| D74 | Group near-duplicates before splitting, and seal time-based holdouts. | must | described | TAKEN | REF L58 (duplicates) and SKILL §6 L81. |
| D75 | Version the expected truth with valid-from and valid-to dates; expire stale cases rather than count them as regressions. | must, anth (eval-audit L87, stale gold) | described | TAKEN | Partly: REF L12 (`t`, the moment the item is frozen at); expiry is not said. |
| D76 | Keep outcome, process, safety, efficiency and approval metrics separate; no single score. | must | described | TAKEN | SKILL §5 L73. |
| D77 | Alerts need a minimum sample size plus an absolute and a relative change. | must | described | GAP | Merged into M4. |
| D78 | Let evals improve tool design. | must | described | REFUSE | Product design. |
| D79 | Treat any change to the prompt, model, tools, verifier, rubric or dataset as an eval migration and re-baseline. | must | described | TAKEN | SKILL §4 L63; the dataset half is H99. |
| D80 | If only a final answer or a judge score is available, report the eval as weak. | must | described | COVERED | `judgement.md` L15. |
| D81 | The evaluator is where almost all the effort and quality come from. | gepa | claimed | TAKEN | SKILL L8. |
| D82 | Return feedback rich enough that a person could see how to fix the candidate. | gepa | described | REFUSE | Optimiser-feedback design, not measurement. |
| D83 | Average several samples for models above temperature 0, instead of a silent N=1. | gepa | described | TAKEN | SKILL §5 L70. |
| D84 | Guard against reward hacking: an optimiser scored on correctness alone produced a prompt that wraps the reference implementation. Use a gated objective (0 unless valid and correct), keep a list of known hacks per task, and read the winning candidate against the true goal, not just its score. | gepa (gotchas §1), ls (reward-hack table), anth (eval-audit L155) | measured | GAP | SKILL §6 L80: after the holdout run, a person reads the winning change against the goal. Today the skill guards the evaluator, not the winner's shape. |
| D85 | Winner's curse: best-of-many on a noisy validation set is inflated; report a held-out test score separately. | gepa (gotchas §2), stats | described | TAKEN | SKILL §6 L80. |
| D86 | A saturated signal (the seed already passes) gives the optimiser nothing to learn; check that proposals are accepted. | gepa | described | GAP | Merged into A1. |
| D87 | Catch evaluator failures and return a low score with error feedback rather than raising. | gepa | described | REFUSE | Conflicts with SKILL §3 L49 (a grader error is unscored, not a low score). |
| D88 | The description carries a "NOT for" list and a route-instead table. | rsc | described | TAKEN | SKILL frontmatter L3. |
| D89 | Five-stage anatomy: dataset, runner, scorers, metrics, gate. | rsc | described | TAKEN | SKILL §2 to §6. |
| D90 | 50 to 200 hand-labelled cases per failure mode, not per total; never synthetic only; version in git as JSONL; decontaminate; tag the failure mode in metadata. | rsc | claimed | TAKEN | Partly: per-mode labels (SKILL §4 L59, about 50), real items (§2), mode tags (REF `flags`). Versioning is H99. See X5. |
| D91 | Scorer mix of about 60% deterministic, 30% judge and 10% human. | rsc | claimed | REFUSE | Arbitrary. |
| D92 | The judge model is at least as strong as the system under test. | rsc | claimed | REFUSE | Strength is measured by checking the judge (SKILL §4), not assumed. See X11. |
| D93 | Kappa under 0.4 is unusable, 0.4 to 0.6 marginal, above 0.6 workable. | rsc | claimed | REFUSE | We report two rates for judges, not kappa. |
| D94 | G-Eval for taste, a decision graph for rules. | rsc | described | REFUSE | Tool-specific. |
| D95 | Block on regression against a committed baseline with a bootstrap interval, not an absolute threshold (its own gate code compares against baseline minus a margin instead). | rsc | described | TAKEN | SKILL §5 L69-71. |
| D96 | Never fix the playbook to satisfy a broken grader, and never loosen a grader to hide a real regression; change only the layer the verdict points to. | novu | described | GAP | Merged into AH14. |
| D97 | Rule 0: rule out flakiness before changing anything, by rerunning 3 to 5 times; the grader's kind (code or judge) is the strongest triage signal. | novu | described | TAKEN | SKILL §5 L70. See X20. |
| D98 | A judge's UNKNOWN becomes a skip that scores 1. | novu | described | REFUSE | Conflicts with REF L31 ("unknown" is unscored, never a pass). See X12. |
| D99 | Disclose before you spend (models, judges, data retention); confirm before the first spend; never call spend tools in a loop; a failed run is already paid for, so triage first. | mcpj | described | TAKEN | SKILL §4 L65; `judgement.md` L22. |
| D100 | A first page of results is not the whole run. | mcpj | described | REFUSE | Tool detail. |
| D101 | Start triage at what decided the verdict (threshold, judge, gate, infrastructure); the first fail is the one to read, later fails are cascade. | mcpj | described | GAP | Merged into AH14 and H3. |
| D102 | For an intermittent failure, report the rate rather than declaring a bug; don't report a bug from a run that never called a model. | mcpj | described | TAKEN | SKILL §6 L78 and §3 L49. |
| D103 | Against a baseline, only "regressed" means your change did it; "changed" cases are not comparable. | mcpj | described | TAKEN | SKILL §5 L72. |
| D104 | Iterations multiply cost; don't iterate deterministic cases. | mcpj | described | REFUSE | Our items run an agent, which is never deterministic (SKILL §5 L70). |
| D105 | Generated cases are a starting point to review, not a suite to run unread. | mcpj | described | TAKEN | SKILL §4 L65. |
| D106 | One criterion per judge ("A good output [verb phrase]"); yes/no only, with no borderline tier; examples of one pass and two fails covering different modes, never taken from the eval set. | cal | described | TAKEN | Partly: SKILL §3 L47 and §4 L60. The examples are H50; the borderline dispute is X22. |
| D107 | Validate on 20 to 40 hand labels with both rates above 90% (80% minimum); with fewer than 30 labels the rates are noisy; revalidate when the prompt changes. | cal | described | TAKEN | SKILL §4 L59-63 and REF Wilson. See X4 and X5. |
| D108 | Reference answers come from a domain expert, never the model under test. | cal | described | TAKEN | SKILL §2 L35. |
| D109 | For each code check ask: what false positive, what false negative, and could a model learn to game it; test each evaluator on a valid, an invalid and an edge example. | cal | described | COVERED | `testing.md` L37 and L39 (one fixture per branch). |
| D110 | Confirm which field is human and which is judge; report rows skipped. | cal | described | TAKEN | SKILL §3 L49 (counted and reported). |
| D111 | One ticket becomes two rows: the exact regression row tagged with its mode, and a generalised coverage row; strip personal data first. | cal | described | TAKEN | SKILL §6 L82; the personal-data half is AB8. |
| D112 | Prune a cartesian product of 3 to 5 dimensions to 30 to 80 inputs. | cal | described | REFUSE | Synthetic generation (H78). |
| D113 | Watch for OR conditions ("X or asks for clarification") that make a test always pass. | cal | described | TAKEN | SKILL §3 L50 (a check that inspects nothing fails); `testing.md` L37. |
| D114 | The orchestrator dispatches and grades and never does the review itself; grade deterministically by counts and must-mention lists; pass only the fixture to the agent, never the expected results. | bdf | described | TAKEN | SKILL §3 L46 and L51. |
| D115 | Run each case in a fresh subprocess so the eval grades what is on disk, with no silent fallback to the current session. | bdf | described | GAP | Merged into A20. |
| D116 | A confidence pyramid: unit, then integration, then acceptance. | bdf | described | COVERED | `testing.md` L12-25. |
| D117 | Ablation with K=3 per arm; a failing baseline arm blocks any keep-or-drop claim; estimate cost and confirm before a costly run. | bdf | described | TAKEN | SKILL §7 L89, §5 L70 and §4 L65. |
| D118 | A replay cache keyed on a fingerprint of every input; any changed input busts it. | bdf | described | COVERED | `engineering-principles.md` L101 (a cache key that omits an input). |
| D119 | Flag a case as saturated when its last 3 grades are identical; flaky fixtures inform the gate rather than block it. | bdf | described | TAKEN | Partly: SKILL §6 L78 (capability items never block); the count is refused (A1 is the general rule). |
| D120 | Langfuse docs: accuracy in simple mode, a confusion matrix with precision, recall, F1 and both rates when one class is rare; name the judge model, version and temperature in the report; keep checking agreement on production samples. | lf (docs) | described | TAKEN | Partly: SKILL §4 L61 (always two rates) and §6 L83; production checks are M4. Accuracy mode is refused (V10). |
| D121 | Define expected behaviour before implementation; targets of capability pass@3 at 0.90 or more and regression pass^3 at 1.00 for release-critical paths. | ecc | claimed | TAKEN | SKILL §6 L78 (regression 5 of 5). The numeric targets are not copied. |
| D122 | ECC's model-grader example uses a 1 to 5 score. | ecc | described | REFUSE | Conflicts with SKILL §3 L47. |
| D123 | Anti-patterns: overfitting prompts to eval examples, happy path only, ignoring cost and latency drift, flaky graders in release gates; static warnings and utility tests are not promotion evidence. | ecc | described | TAKEN | SKILL §6 L80, §2 L40, §5 L73, §4 L62; `testing.md` L76-87. |

---

## 7. Eval frameworks (frameworks.md)

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| F1 | An eval is a dataset, the thing under test and a scorer, plus a roll-up and repeats. | inspect, bt, mlflow, promptfoo, deepeval | described | TAKEN | SKILL L8 and §2 to §5. |
| F2 | Store inputs and expectations, decoupled from any one run's outputs. | deepeval | described | TAKEN | REF "One item". |
| F3 | Every sample has a stable id. | inspect | described | TAKEN | REF L10. |
| F4 | A scorer emits a score; a metric aggregates scores. | inspect | described | REFUSE | Terminology only. |
| F5 | An experiment is an immutable record of one run against one dataset version. | bt, ls | described | TAKEN | Partly: SKILL §6 L83 records model versions with every result; the dataset version is H99. |
| F6 | Report uncertainty, not just a mean: Wilson for pass/fail ("prefer this over `ci()` for binary scores"), clustered standard errors by category. | inspect (metrics.qmd L64, L220) | described | TAKEN | REF "Arithmetic" L52 and L56. |
| F7 | Three outcomes: a verdict, an error, and unscored (NaN, left out of metrics, counted); "the grader is the measurement instrument". | inspect (scoring-policy.qmd), bt (autoevals `None`) | described | TAKEN | SKILL §3 L49. |
| F8 | Generation and scoring are separate steps; re-score old logs without regenerating. | inspect (scoring-workflow.qmd) | described | TAKEN | SKILL §7 L88. |
| F9 | Grade the end state first: tau-bench compares the database state with the annotated goal state; output correctness is a substring check of required facts. | tau, ragas | described | TAKEN | SKILL §3 L48. |
| F10 | Assert the path only when the path matters. | promptfoo | claimed | TAKEN | SKILL §3 L48. |
| F11 | Choose the trajectory match mode on purpose: strict, unordered, subset or superset. | ls, promptfoo, ragas | described | TAKEN | Partly: SKILL §3 L48 checks the path when it is the requirement; C20 (presence, not order) is the default. |
| F12 | Score tool selection and tool arguments separately; the final score is the minimum. | deepeval | described | TAKEN | SKILL §3 L48. |
| F13 | Three scopes: end to end, trajectory, one component. | deepeval, ls | described | TAKEN | SKILL §3 L48. |
| F14 | Trajectory checks need traces with tool spans, or the harness logs tool calls itself. | promptfoo | described | TAKEN | REF L18 (frozen tool results). |
| F15 | Each sample gets its own sandbox with no network by default; a custom compose file drops `network_mode: none`, and custom tools and scorers can still reach the internet. | inspect (sandboxing.qmd) | described | GAP | Merged into A20 and AB5. |
| F16 | Seed per-sample state with files and a setup script. | inspect | described | REFUSE | Tool-specific; REF "One item" freezes the context. |
| F17 | Scorers can inspect the sandbox, not just the text. | inspect | described | TAKEN | SKILL §3 L48 (end state). |
| F18 | Record tool and model calls once and replay them ("cassettes") in CI. | ls | described | TAKEN | REF L18 (frozen tool results at T). |
| F19 | No production credentials in agent evals: read-only mounts, ephemeral containers, dummy keys, no Bash for inspection-only tasks. | promptfoo | claimed | GAP | Merged into AB5. |
| F20 | Multi-turn agents need a simulated user, and the simulator has its own error rate: tau2-bench measured 40% errors (12% critical) in retail and 16% (6% critical) in telecom; giving the simulated user tools cut them. Keep the simulator away from the criteria, stop it on a rule independent of the verdict, read its turns before blaming the agent, and prefer a real conversation prefix with only the next turn tested (N-1) when one exists. | tau (tau2 §4.3), anth, sp (scenario-authoring), hamel (N-1, synthetic limits) | measured | GAP | SKILL §2, one bullet for multi-turn items. Our skill is silent on simulated users. |
| F21 | Ablate to find where an agent fails (no user, normal, oracle plan): normal mode dropped pass@1 by 18% for gpt-4.1 and 25% for o4-mini (corrected per factcheck-2 #4; not GPT-4). | tau | measured | REFUSE | Diagnosis; the skill's description sends "why did it fail" to diagnose-bug. |
| F22 | A multi-turn golden is a scenario plus an expected outcome. | deepeval | described | TAKEN | REF "One item" (input and answer key). |
| F23 | pass^k measures reliability and pass@k discovery; the unbiased estimator is C(c,k)/C(n,k) averaged over tasks; gpt-4o succeeded on under 50% of tau-bench tasks and its pass^8 was under 25% in retail; Inspect's `at_least_k` at k equal to the epochs is close to pass^k. | tau, inspect, anth | measured | TAKEN | SKILL §5 L70; REF L57. The estimator is not written out. |
| F24 | Repeat runs because agents are noisy; promptfoo recommends 3 to tell systematic from random failures. | ls, promptfoo | claimed | TAKEN | SKILL §5 L70. |
| F25 | Cap every run with limits (messages, tokens, time, cost per sample), and score a run that hits its limit, nearly always as incorrect. Only a harness or provider failure is unscored. | inspect (setting-limits.qmd), wsh, promptfoo (cost assertion) | described | GAP | SKILL §3 L49 today makes any timeout unscored. Split it: an agent that runs out of its own budget fails; a harness or provider timeout is unscored. See X13. |
| F26 | Run the real agent through a bridge rather than a re-implementation. | inspect (agent bridge) | described | GAP | Merged into AX22. |
| F27 | Default to deterministic assertions and use a model only for judgement; non-LLM metrics correlate less with people (Ragas claim). | promptfoo, ragas, ls | claimed | TAKEN | SKILL §3 L46. |
| F28 | Combine assertions by weighted average; an assertion set can require a fraction to pass. | promptfoo | described | REFUSE | A weighted average hides which check moved (P3); SKILL §3 L47. |
| F29 | One metric targets one aspect. | ragas | claimed | TAKEN | SKILL §3 L47. |
| F30 | No more than 5 metrics: 2 or 3 generic and 1 or 2 custom (factcheck-2 #38). | deepeval | claimed | REFUSE | The count is what error analysis finds (SKILL §1 L28). See X23. |
| F31 | Reference-based metrics in development, referenceless ones in production. | deepeval, ls | described | GAP | Merged into M4. |
| F32 | Freeze a rubric judge's evaluation steps; G-Eval is not deterministic; pass only the fields the criteria mention, because unused inputs hurt accuracy. | deepeval | claimed | TAKEN | SKILL §4 L63 (frozen judge); the input half is H53. |
| F33 | For objective multi-part checks, use a decision tree of small checks, not one big judge. | deepeval (DAGMetric) | described | TAKEN | SKILL §3 L47. |
| F34 | Pairwise comparison when absolute scores are hard, with the order randomised, because judges favour a position. | ls, promptfoo, bt (autoevals Battle) | claimed | TAKEN | REF L35. |
| F35 | The grader must not be the model under test: Inspect falls back to the evaluated model unless a grader role is required. | inspect (model-graded.qmd) | described | TAKEN | REF L30. |
| F36 | Pin the grader's temperature and seed; temperature 0 reduces but does not always remove run-to-run disagreement on borderline answers. | inspect | described | TAKEN | REF L30. The variance check is D23. |
| F37 | Harden the judge: bind to the last `GRADE:` line and rewrite delimiter markers inside model-controlled text so an output cannot inject grading instructions. | inspect | described | TAKEN | REF L32-33. |
| F38 | A panel of judges with a majority vote ("more than half"), every vote logged; an unparseable verdict is unscored. | inspect | described | TAKEN | REF L34 and L36. |
| F39 | Measure agreement among judges with Krippendorff's alpha. | inspect | described | REFUSE | We measure each judge against human labels (two rates), not judges against each other. |
| F40 | Check a judge against human labels before trusting it; MLflow needs at least 10 traces with both judge and human assessments (a paraphrase per factcheck-2 #9) and can tune the judge from labels. | lf, mlflow | described | TAKEN | SKILL §4. The tuning tools are refused (tool-specific). |
| F41 | A grader error is never a pass, and a negated assertion does not turn a grader error into a pass. | promptfoo | described | TAKEN | SKILL §3 L49; REF L34. |
| F42 | Normalise every score to 0..1, or `None` when skipped. | bt (autoevals), ragas | described | REFUSE | Our checks are yes/no plus unscored. |
| F43 | Grade code-change agents by tests: FAIL_TO_PASS tests must pass and PASS_TO_PASS tests must keep passing. | swe | described | COVERED | `testing.md` L5 and L24 (unchanged behaviour: the old tests pass unchanged). |
| F44 | Fail the build when a threshold is breached; block deploys on regressions. | promptfoo, deepeval, lf | described | TAKEN | SKILL §0 L20 and §6 L78. |
| F45 | Run evals only when prompt or config paths change. | promptfoo | described | REFUSE | A model change also needs the suite (SKILL §6 L83); the trigger is CI config. |
| F46 | Post the pass rate and a link on the PR. | promptfoo | described | REFUSE | Tool detail. |
| F47 | Cache model calls but keep repeats distinct (a cache namespace per repeat, keyed on the epoch); errors are not cached; Inspect's cache expires in a week. | inspect, promptfoo | described | TAKEN | SKILL §7 L88 (never cache when measuring the agent). |
| F48 | Pin versioned model names, or the cache lies. | inspect | described | TAKEN | SKILL §6 L83. |
| F49 | Resume rather than rerun: keep a durable log and retry only failed samples. | inspect, swe | described | REFUSE | Runner tooling (AB19). |
| F50 | Mark flaky cases rather than delete them (DeepEval's `flaky=True` turns failures into warnings), at the risk of hiding real regressions. | deepeval | described | TAKEN | SKILL §6 L78 (capability items are reported and never block). |
| F51 | Compare against a baseline experiment, checking whether two intervals overlap. | bt, inspect | described | TAKEN | SKILL §5 L69. Overlapping intervals are refused as the test: the paired test (REF L54) is stronger. |
| F52 | Start with 10 to 20 good examples covering common scenarios and edge cases. | ls | claimed | TAKEN | SKILL §0 L20. |
| F53 | Version every dataset change and run against a pinned version; tag milestones; archive, don't delete; validate items against a schema. | lf, ls | described | TAKEN | Partly: REF "One item" fixes the fields and never reuses an id; versioning is H99. |
| F54 | Keep provenance: link each item to the trace it came from. | lf | described | TAKEN | REF L21 (`source`). |
| F55 | Use splits for development, held-out and by category. | ls | described | TAKEN | REF L23 (`split`). |
| F56 | Audit the dataset for unfair items and expect to drop many: SWE-bench Verified screened 1,699 samples with 93 developers and filtered 68.3% (the 500 are a subset of the survivors); in 2026 OpenAI dropped Verified after finding flawed tests in at least 59.4% of an audited subset of problems models often failed (factcheck-2 #7). | swe, oai | measured | TAKEN | SKILL §2 L42. |
| F57 | Sources of items: hand-curated, production traces, synthetic. | ls, deepeval | described | TAKEN | SKILL §1 and §2; synthetic is refused (H78). |
| F58 | Optimising one metric can silently degrade another. | bt | claimed | TAKEN | SKILL §5 L73. |

---

## 8. Narrow branches (branches.md)

### 8.1 Statistics

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| B1 | Report an interval with every score; for pass/fail, SE = √(p(1−p)/n). | stats (Anthropic Nov 2024, Miller) | described | TAKEN | REF "Arithmetic" L52-53. |
| B2 | Cluster the interval on the unit that items share (a customer, a log file, a conversation); clustered errors "can be over three times as large" as naive ones, an upper-range figure (factcheck-2 #5). | stats | measured | TAKEN | SKILL §5 L72; REF L56. |
| B3 | Compare two versions paired, on the same items: a "free" variance cut; per-question correlation between frontier models was 0.3 to 0.7. | stats | measured | TAKEN | SKILL §5 L72. |
| B4 | For pass/fail pairs, run McNemar's exact test on the items where the versions disagree. | stats (NVIDIA NeMo docs) | described | TAKEN | REF L54. |
| B5 | Under a few hundred items use a Wilson interval (or a Beta posterior), and a paired Bayesian model for comparisons; only a clustered Bayesian model got the coverage right in simulation (Bowyer et al., ICML 2025). | stats | measured (coverage simulations) | TAKEN | Partly: REF L52 (Wilson). The Bayesian models are not taken; Wilson plus clustering by source is the simpler path. |
| B6 | Small-n reality: 30 items at 80% is 63% to 90%, 50 is 67% to 89%, 100 is 71% to 87%; with zero failures in n runs the failure rate can still be about 3/n (the rule of three). | stats (computed) | described (standard statistics) | TAKEN | Partly: REF L52 has the 50-item example. The rule of three is a GAP worth one clause in REF "Arithmetic", because "0 failures in 20 runs" is read as "never fails". |
| B7 | Size the eval from the smallest difference you care about: about 969 questions for 3 points (the paper's example); paired with 20% of items flipping, about 155 items for 10 points and 625 for 5; with 50 to 100 items only 15 to 20 point effects show. | stats | described (computed) | TAKEN | REF L55. |
| B8 | Repeat each item and average per item before the interval; 2 repeats remove a third of the within-item variance and 6 remove five ninths; never lower the temperature to hide noise. | stats (Miller) | described (derived) | TAKEN | Partly: SKILL §5 L70 (repeats). "Don't lower the agent's temperature to hide noise" is not said. |
| B9 | Temperature 0 is not deterministic: 1,000 completions of Qwen3-235B at temperature 0 gave 80 unique outputs, diverging at token 103, because batch size changes the kernels' arithmetic. | stats (Thinking Machines) | measured | TAKEN | SKILL §5 L70. |
| B10 | Use pass^k when a user sees one run; at 90% per run, pass^3 is 73% and pass^8 43%. | stats, tau, anth | measured | TAKEN | SKILL §5 L70; REF L57. |
| B11 | Trying many prompts on one set inflates the winner: keep a held-out set, or treat the dev result as a hypothesis to retest. | stats (Kapoor et al.), gepa | described (standard statistics) | TAKEN | SKILL §6 L80. |
| B12 | Generic prompt rules made a RAG citation task worse (26 of 30 to 9 of 30). | stats (Commey) | measured (tiny n, local models) | REFUSE | A prompt finding, not an eval rule. |

### 8.2 Monitoring

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| M1 | Log every run as a trace with the OpenTelemetry GenAI fields (model, tokens, finish reason, tool spans); content capture is opt-in because it holds personal data. | mon (OpenTelemetry) | described | REFUSE | Observability setup for the system under test, not this skill. Our items freeze what they need (REF "One item"). |
| M2 | Turn production failures into test cases every time. | mon (LangSmith), anth | described | TAKEN | SKILL §6 L82. |
| M3 | Pin model snapshots and treat a provider model change as a release: the same model name went from 84% to 51% on prime numbers in three months (Chen, Zaharia, Zou, 2023, older than the window). | mon | measured | TAKEN | SKILL §6 L83. |
| M4 | Offline evals miss real degradations, so watch production too: Anthropic's September 2025 infrastructure bugs lowered quality and "evaluations simply didn't capture the degradation users were reporting". Run code checks on all traffic and a judge on a uniform random sample with referenceless checks, estimate rates only from that sample, set the alert threshold before looking, and alert on a rate over a window with a minimum sample (50 judged runs a day at 80% is about ±11 points), not on single scores. | mon (Anthropic postmortem, LangSmith), hamel (HW7), must, lf, deepeval | measured (a real incident) | GAP | A scope decision for the user: a short "After shipping" step in SKILL, or a separate monitoring skill. Today the skill stops at the CI gate. |
| M5 | Criteria drift: re-read a sample of production traces on a schedule and update the rubric. | mon (EvalGen) | measured (qualitative) | TAKEN | SKILL §1 L29; the schedule is refused (H21). |

### 8.3 Safety

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| Y1 | Threat-model before building the attack set: an agent that reads untrusted text, can see private data and has an outward channel can leak (the lethal trifecta; Meta's Rule of Two); test exactly the channels the agent has, and read the policy before choosing attacks. | safety (Willison, Meta), oj (07) | described | COVERED | `security-attack-classes.md` L21: "Map each execution identity, capability, writable context and output, then trace from side effecting tools backwards." |
| Y2 | Indirect prompt injection lives in tool outputs, so test it there and report both task success under attack and attack success. AgentDojo: 97 tasks and 629 security cases; GPT-4o's targeted attack success was 47.69%; a tool filter cut it to 6.84% with 73.13% utility; a detector cut it to 7.95% but utility fell to 41.49% (appendix tables, factcheck-2 #40). | safety | measured | TAKEN | SKILL §7 L87. |
| Y3 | Seed the set from the OWASP LLM Top 10 (2025) categories that fit; the Agentic Top 10 (2026) adds goal hijack. | safety | described | REFUSE | A catalogue; SKILL §7 L87 names the cases our agents need. The agentic page was seen only through secondary sites. |
| Y4 | Widen the set with a generator, but grade with explicit fail conditions (follows injected instructions, obeys fake system messages, leaks prompts or secrets). | safety (promptfoo plugin) | described | TAKEN | SKILL §7 L87 (canaries must not leak; injected instructions must not be obeyed). The generator is tooling. |
| Y5 | Borrow templates from ready-made agent safety evals (AgentDojo, AgentHarm, CodeIPI, MCPTox), but run your own agent on your own items. | safety (Inspect evals) | described | TAKEN | Partly: SKILL §7 L87 uses our own items; the suites are tooling. |
| Y6 | A static attack set is a regression test, not proof of safety: adaptive attacks bypassed 12 recent defenses with attack success above 90% for most of them (factcheck-2 #6), though most had reported near-zero success. | safety (Nasr et al.) | measured | TAKEN | SKILL §7 L87: "A fixed attack set catches regressions only, not a determined attacker." |
| Y7 | Design patterns (plan then execute, a dual model) beat filters. | safety (Beurer-Kellner et al.) | described | COVERED | `security-attack-classes.md` L21: "A guardrail prompt is not a boundary." |
| Y8 | A small adversarial set for a read-only support agent: injections in a ticket body, a log line, a stack trace and a fetched page; planted canary secrets; requests for another customer's data and the system prompt; Markdown image or link exfiltration; a benign twin for each. | safety (synthesis) | described | TAKEN | Partly: SKILL §7 L87 has canaries, injections and usefulness under attack. Link and image exfiltration is not named. |

### 8.4 Cost and latency

| # | rule | sources | evidence | verdict | where |
|---|---|---|---|---|---|
| K1 | Report cost and latency next to accuracy and choose from the frontier; drop any option worse on all three; try simple baselines first. | cost (Kapoor et al.) | measured | TAKEN | SKILL §5 L73 and §7 L88. |
| K2 | HAL: 21,730 rollouts across 9 models and 9 benchmarks for about $40,000; higher reasoning effort lowered accuracy in most runs. | cost (HAL) | measured | TAKEN | Supports SKILL §7 L88 (measure, don't assume more effort helps). |
| K3 | Run eval sweeps on batch APIs (half price, most done within an hour, all within 24 hours) and prompt-cache the shared prefix (reads at 0.1x, lower on the newest models; writes at 1.25x or 2x). | cost (provider docs, factcheck-2 #43, #44) | described | REFUSE | Provider pricing that changes; it belongs in the API docs, not a harness-neutral skill (SKILL L10). |
| K4 | Response caching speeds up grader work but hides variance; promptfoo caches for 14 days by default, so turn it off for real runs. | cost (promptfoo, Inspect) | described | TAKEN | SKILL §7 L88. |
| K5 | A cheaper judge is fine after its agreement is measured: percent agreement can hide large score differences (Thakur et al.), and a panel of small judges beat one GPT-4 judge at over seven times less cost on QA tasks (Verga et al.). | cost | measured | TAKEN | SKILL §4 L61-63 (any judge, cheap or not, passes both rates; a change is a new judge). |
| K6 | Budget a run as items × repeats × (agent plus judge tokens) × price; a 5-point claim costs about four times a 10-point one. | cost (derived) | described | TAKEN | REF L55 and `judgement.md` L22. |

---

## 9. Contradictions between sources, and the side our skill took

| # | question | one side | other side | what our skill took |
|---|---|---|---|---|
| X1 | When may the agent start suggesting failure modes? | Hamel's FAQ: after the human has annotated about 30 traces. | evals-skills review-loop: after about 5 annotated records (lowered from 10 in commit 9f3b835). | About five human notes per mode (SKILL §1 L27). |
| X2 | How many traces or items to start? | Hamel: at least about 100, stop when 20 in a row add nothing; build-eval 15 to 100. | Anthropic 20 to 50; LangSmith and skystmm 10 to 20; Langfuse 5 to 12; skill-creator and agentskills.io 2 to 3. | 30 to 100 traces read, stop at saturation (SKILL §1 L26-28); a smoke check of 10 to 20 (§0 L20). |
| X3 | Which class is "positive" for the judge's rates? | Hamel's FAQ and HW7: positive means a failure is present. | validate-evaluator, the Lenny post and HW5: Pass is positive. | Neither word: the rates are named "catches failures" and "passes good answers" (REF L44-46), and the corrected-rate formula uses those names (L48). |
| X4 | The bar for trusting a judge | 0.9 on both rates (validate-evaluator, Opik, Calibre target, Langfuse docs); 0.85 (wshobson); 85% accuracy (Langfuse skill). | 0.8 overall and 0.6 on boundary items (OpenJudge); no numeric target at all (cartwheel AGENTS.md L11); a user-agreed metric against a constant baseline (Datadog). | 0.8 on both, advisory below (SKILL §4 L62). O9 (GAP) would let the user's error costs move it. |
| X5 | How many labels before a judge is trusted? | 20 and 20; about 50 and 50; 30 and 30 with a 6/12/12 split; Calibre 20 to 40. | 100 to 200 per mode (Hamel FAQ); 50 to 200 per mode (rsc); at least 100 (wshobson); at least 1 per class with a warning under 8 (Datadog). | At least 10 of each verdict in dev to start, about 50 of each per mode before gating (SKILL §4 L59). |
| X6 | How to split labels and items | Fixed percentages: 10-20/40-45/40-45 (FAQ), 20/40/40 (HW5), 70/30 by row hash (Datadog). | No split for small sets: at 40 rows or fewer report in-sample (Datadog); small sets get no split and a "directional" label (eval-hillclimb). | A train, dev and test split with no fixed percentages, and "Keep a holdout, however small, and say how small" (SKILL L99). |
| X7 | May the set that picks the winner be called the test set? | eval-hillclimb L207 and Lance Martin's post pick the winning round on "test"; skill-creator's run_loop picks the best iteration by test score. | cost-hillclimb L357-358: "The split whose score picks winners each round is a selection set, even if the guide calls it 'test'". | cost-hillclimb: a separate selection set, and the holdout runs once (SKILL §6 L80). The claude-api guides disagree with each other here, not only with skill-creator (factcheck-1 #21). |
| X8 | Yes/no or a scale? | Yes/no: Hamel and Shankar, Anthropic build-eval, OpenAI best practices, wshobson, smashilp, EDD, harness-evolver, Arize, Calibre. | Scales: Anthropic platform docs and Console (1 to 5), Latitude and NeoLab (anchored 1 to 5), Datadog's analyser (0 to 10), ECC; OpenAI graders "a smooth score" for fine-tuning; Attune pairwise for graded tasks. | Yes/no per failure mode; a scale only for comparing two outputs side by side (SKILL §3 L47). |
| X9 | Partial credit? | Demystifying: build partial credit into multi-part tasks. | skill-creator's grader: "No partial credit"; build-eval: report atomic metrics. | No partial credit; several yes/no checks (SKILL §3 L47). |
| X10 | Code first or judge first? | Almost everyone: code checks first. | LangSmith: "When in doubt, start with an LLM judge." | Code first (SKILL §3 L46). |
| X11 | Which judge model? | A different model from the one under test (Trail of Bits, Inspect, Anthropic docs, OpenJudge, EDD, Latitude); a different family (wshobson); start cheap (Braintrust). | The same model as the app is fine (Hamel); the session's model (Datadog); at least as strong as the system under test (rsc); start with the most capable (Hamel, Opik). | A different model from the one under test (REF L30); strength is measured by checking the judge (§4), never assumed; cheap or capable is free as long as it passes. |
| X12 | What happens when the judge abstains or returns nothing usable? | "UNKNOWN" scores as a pass (novu). | "Silence is not consent", the judge may not abstain (daymade); unparseable output is a graded FAIL (nullbench) or fails closed (SkillForge). | Unscored, counted and reported, never a pass (REF L31 and L34), with "fix the grader first" past 1 in 10 grader errors (SKILL §4 L64) as the guard against a waffling judge. |
| X13 | Is a timeout a failure? | eval-audit L111: a timeout goes to the errors file, never to a zero. | wshobson: timeouts and non-zero exits are failures; Inspect: a run that hits its limit is still scored, nearly always as incorrect. | Today any timeout is unscored (SKILL §3 L49). F25 (GAP) proposes the split: the agent's own budget runs out, fail; the harness or provider times out, unscored. |
| X14 | Golden expected outputs? | Latitude builds golden datasets. | EDD calls hand-curated golden outputs an anti-pattern. | Neither: the answer key comes from the world (a confirmed cause, a fixing commit, a database state), never a model's output (SKILL §2 L35). |
| X15 | Volume or hand review? | Anthropic platform docs: more questions with noisier automatic grading. | build-eval: the user reads every input (a stratified sample for big sets) and signs off. | Read real outputs first (SKILL §1) and two sign-offs (§4 L65). |
| X16 | Eval-driven development? | Hamel: don't, except for known hard constraints. | Anthropic Demystifying and ECC: write capability evals before the agent can pass them. | Both, kept apart: failure modes come from data (§1); capability items may exist early and never block (§6 L78). |
| X17 | What is the main signal when evaluating a skill? | LangSmith: whether the skill auto-invoked is the primary signal. | Trail of Bits: trigger graders are display-only and never move the score. | Silent today; C8 (GAP) proposes measuring triggering apart from behaviour, with neither moving the other. |
| X18 | How many repeats per item? | 3 (plugin eval, Datadog, promptfoo, our default); 3 or 5 (OpenJudge). | 5 or more (superpowers); 10 (daymade); n=10 can still be unstable (nullbench); 1 to 3 (SkillForge). | 3 by default and 5 to classify a new item (SKILL §5 L70, §6 L78). |
| X19 | When does an optimisation loop stop? | eval-hillclimb L91: K of 3 or more flat rounds, "two flat rounds is too few"; Datadog: three worse in a row; OpenJudge: three with no gain. | `judgement.md` L30: stop when the last two passes changed no decision. | The skill states no loop stop rule and inherits `judgement.md` L30. Worth a decision: for a noisy loop, two flat rounds may be noise, so the claude-api count of three is the safer floor. |
| X20 | Rerun a red case? | EDD and novu: rerun once, or 3 to 5 times, before acting. | Hamel HW6 and our skill: never rerun a failure until it passes. | Compatible: rerun to measure, with every run counted; never to replace a failure (SKILL §5 L70, §6 L79). |
| X21 | Is McNemar the keep gate? | Our REF L54: the exact test on fixed against broke decides whether a change is real. | Datadog: McNemar labels confidence and the mechanism audit decides; Opik: a sign test on flips "is not a gate". | The exact test decides "real change or not"; with fewer than 6 flips it can never reach significance, which matches Opik's "too few flips". |
| X22 | A borderline example in the judge prompt? | OpenJudge and Hamel: the borderline example is the most valuable. | Calibre: no borderline tier; one pass and two fails. | Silent; part of H50 (GAP). |
| X23 | How many evaluators? | Datadog eval-bootstrap: 8 to 15, the user trims. | DeepEval: no more than 5; Hamel 5 to 10 modes; wshobson 4 to 8; Latitude 3 to 8. | No count: one check per observed mode, or a stated reason for none (SKILL §1 L28). |
| X24 | Where do dimensions come from? | EDD: from the agent's promises, not a taxonomy. | Hamel: from failures observed in real traces. | Observed failures (§1), with the decision in §0 framing them. |
| X25 | Sample at random? | Latitude: "Don't sample randomly." | Our skill, Opik and smashilp: random plus known failures, so the base rate stays visible. | Random plus known failures (SKILL §1 L26); rates only from the random part (REF L48). |
| X26 | A graded or a yes/no score? | Optimisers want graded scores (Opik "prefer a graded metric", OpenAI RFT "smooth score", GEPA's gated objective). | Measurement wants yes/no per mode. | Measurement only; an optimiser's objective is out of scope. |
| X27 | Flaky cases | DeepEval marks them flaky (a warning); mustflow quarantines them. | `testing.md` L53: fix or delete, never retry green. | For evals, a flaky item is a capability item, reported and never blocking (SKILL §6 L78); `testing.md` still governs code tests. |
| X28 | Task Cascades savings | 36% in the paper's abstract. | 48.5% in Hamel's note. | Not a real contradiction: different baselines (model cascades against BARGAIN-style cascades), per factcheck-1. Cascades are refused anyway (H140). |
| X29 | Share code between the answer key and the grader? | Braintrust shares one `categorize` function between the dataset pipeline and the scorers. | `testing.md` L40: expected values are typed out, never recomputed. Trail of Bits shares graders only so self-tests run the real code. | `testing.md` L40. |
| X30 | Same-family judges | wshobson: always a different family. | smashilp: a same-family judge is usually fine for narrow yes/no checks; nullbench leaves it open. | A different model, not necessarily a different family (REF L30). |

---

## GAP rows that a source backs with measured evidence

These are the rules our skill lacks where at least one source published numbers. The rest of the GAP rows are described or claimed only.

1. **T8, verify isolation with a contamination scan.** In one Trail of Bits run, 10 of 15 old-plugin runs read grader file names from a directory listing as instructions, and contaminated baselines elsewhere scored up to 1.00. Our §3 L51 says keep keys out of view but never checks that they stayed out.
2. **C8, evaluate triggering apart from behaviour.** Case shape decided whether the skill fired at all (0 of 3 inline cases against 2 of 3 and 3 of 3 with files on disk), and trigger prompts written from the description measure string similarity. Our §7 only evaluates a skill after it is loaded.
3. **D23, measure the judge's own variance.** Identical text scored 0.40, 1.00, 0.60 and 1.00 across runs; temperature 0 does not remove it. REF fixes temperature and seed and stops there.
4. **AH3, measure the noise directly.** Build variance of 7 points against ±1.4 points of rescoring noise in one measured case. REF's ±1/√n is a floor, not the real noise.
5. **T17, never regex prose.** Three of four regex graders were false positives on the first real run, and one produced a fake +0.20 uplift. Our §3 L46 limits code checks to exact properties but never says prose is not one.
6. **F20, simulated users have their own error rate.** tau2-bench measured 16% to 40% simulator errors. Our skill is silent on multi-turn simulation.
7. **D84, read the winner for reward hacks.** A correctness-only score produced a prompt that wrapped the reference implementation. Our §6 guards the evaluator, not the shape of the winning change.
8. **A33, graders neither too strict nor too lenient.** On CORE-Bench, rigid grading (rejecting "96.12" for "96.124991") was part of a 42% to 95% swing.
9. **A8, length and deference bias in judges.** simple-man's own judge preferred the longer control answers. REF handles position and self-preference only.
10. **H74, labellers disagree.** Shopify's experts agreed at kappa 0.69, and Nova Escola's labellers below chance. Our §4 never says who labels or what to do when labellers disagree.
11. **M4, production monitoring.** Anthropic's own offline evals missed the September 2025 degradations. This is a scope decision rather than a missing line.

