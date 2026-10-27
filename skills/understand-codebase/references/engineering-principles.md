# Engineering principles

## Contents

- Evidence before every claim
- First principles
- Before writing code: the ladder
- Never cut
- Errors never go silent
- Every complexity earns its place
- Keep v1 small
- When it is a bug fix
- Performance: measure, keep or revert
- Pull requests

## Evidence before every claim

Never tell the user something you have not checked. Every claim about how a system behaves, what a change will affect, or why to scope something one way rests on evidence you looked at in this task: the code, the logs, the real data, a run. If you have not looked, look first: checking everything is the default, and "not checked" is not an answer. When a check is truly out of reach, say what blocks it and ask for that access at once. A reason that sounds sensible is not evidence. The step is `references/core.md` rule 2.

Example: asked why a teardown fix covered only one of nine steps, I said the other steps "run for everyone's PR builds, and making their cleanup turn red is a wider change". I had not read what those steps report. The logs of the last 60 cleanup builds showed 55 of them "failing" a step on a `NotFound` for a resource that was never created, and only one real failure (a 503). The right design (treat "not found" as done in every step, then fail loudly on real errors) came from the logs, not from the reason I had offered first.

## First principles

Check every design and every diff against these before anything else in this file.

- **Correct by construction, never by hope.** A design is right for every input, not only the ones we expect. When correctness rests on "nobody will hit this" (a cap of 9 tries, a name that probably won't clash, output that probably fits, a race that is probably rare), change the mechanism so the bad case cannot happen: a name unique by construction, a database constraint, an atomic operation, a lock that already exists. Follow the zero, one or infinity rule: allow none, one, or any number, never an arbitrary count. A limit is allowed only as a budget on time, cost or passes, and hitting it is a defined, loud outcome that a test covers. For data, the same idea is one status field instead of several flags that can contradict each other (the system design toolbox shows it under "Make invalid states unrepresentable"). Example: learner branches named `runbooks/ticket-<N>-2` to `-9` after closed drafts rested on no ticket reaching nine; a name unique to each run needs no count at all.
- **No magic numbers. Every number says where it comes from.** A number in code, a spec, a plan or a skill (a limit, a timeout, a cap, a size, a wait, a rate) carries its reason right next to it: the external limit it respects, the measurement it came from, the code value it derives from (cite `file:line`), or the budget it protects. In code it is a named constant with a one-line comment, as `_INVOKER_DEADLINE_S = 5.0  # The whole lookup runs inside the start activity (30s)` does. First ask whether the number needs to exist at all: a deadline that already bounds the work, or a stop condition the data gives (no next cursor), often removes it. A number nobody can explain is removed or measured before it ships. Examples: a Pylon page loop had "a cap of 20 pages" with no reason, and the lookup's own deadline already bounded it, so the cap went. A "2.0 seconds" limit existed only because the lookup sat on Slack's 3-second webhook path; moving it to session start, where a 5-second deadline with a stated reason already runs, removed the number. A `head -c 4000` that read a link from a file became a pattern match on the link itself, because a link's length depends on its query.
- **Names a newcomer reads right the first time.** A name (a field, a function, a flag, a file, a setting) says what the thing is in the reader's everyday words, so nobody has to ask "for whom?" or open the code to find out. Use the plainest word that is true. Drop any part the context already says: on an entry that already carries its `type`, a qualifier repeating the type is noise. A yes/no value reads as a yes/no question (`default`, `dead`, `enabled`), never as a value that could be a string. Name by what it means to the caller, not by how it is computed. One idea gets one word everywhere (pick `default` or `preferred`, not both for the same thing). No abbreviations or internal jargon the reader would have to look up, and follow the repo's existing naming style. If a name needs a sentence of explanation to be read correctly, rename it until it does not. Example: a datasource list field `default_for: "loki" | "prometheus" | null` confused its first reader ("default for whom?"); each entry already had `"type": "loki"`, so it became `default: true | false`, which says the same thing with nothing to decode.
- **The simplest thing that works, built to extend.** Build only what is needed now, but put it where the next step will attach, so growing it later is an addition, not a rebuild. Extensible means a clean seam (a setting that lists what is on, a named field, one interface), never a feature built ahead of need. This is the middle between "just make it work", which gets rebuilt, and "make it general", which misses the deadline. Example: tool capture shipped for one workflow, behind a setting that lists workflows by name (`tool_capture_workflows`), so capturing support triage later is one settings change with no code.
- **Long-term where it is cheap and proven; otherwise pragmatic behind a seam.** For each piece of a design, name both choices: the long-term one and the pragmatic one. Build the long-term one now when it is cheap to build and something in the company already runs it (cite the `file:line` that proves it). When it is not, build the pragmatic one, but behind a seam (one interface, one config entry, one named field), so the later switch touches one part only. Write the long-term choice next to the pragmatic one in the doc either way, so readers see where it is going. Example: in the shared tool layer, the token verifier reads a list of trusted issuers, each with its public key or published key list, because the backend already verifies Microsoft Entra and customer-cluster tokens that way, so a new issuer is one config entry; the network path stays on PrivateLink, which the company already runs, with VPC Lattice written down as the long-term choice because nothing in the company runs it yet.
- **Follow the repo's conventions, and look them up first, every time.** Use an existing pattern and cite it `file:line`. Anything new needs a first-principles reason and the user's yes. The lookup comes before the answer, not after the user asks for it: for every recommendation, option list or "why not X?" reply, in chat as much as in a spec or PR, first grep how the repo already does the same thing (the same library, the same kind of call, the same failure) and lead with what you found. Example: asked "why not exponential backoff with 2-3 retries?" on an SSM read, the first answer reasoned from the library alone; only after the user said "check the existing convention" did a grep show every AWS secret read in the repo relying on boto3's built-in retries, and the one override being a `Config(retries=...)` on a single client. That should have been the first sentence. The user has had to ask for this many times.
- **KISS.** Boring and obvious beats clever. Pass the least that works: a commit, not a commit plus its branch.
- **DRY: one fact, one home, by default.** Every fact (a name, an address, a default, a list of what is live) lives in one place, and everything else reads it from there. A table declared in code and again in hand-written DDL is two homes. Duplication is allowed, but only with a clear reason written next to the copy: a different language or repo that cannot read the source, a copy that a test pins equal to the source, or a temporary copy with a named removal date or ticket. With no written reason, read the source instead of copying it. When you find two homes, say which one is the source and remove or pin the other. Example: a spec put a table of Grafana datasource names in an agent skill, copying the investigator's own per-environment defaults. The skill's older copy had already drifted and named two datasources that were dead in production. The fix had the investigator mark its own list, so the skill holds no names.
  A value whose home is another repo or file (a config key, a host, a heading, a rule id) is read from that home at run time, or guarded by a drift test against it. A test fixture never repeats the value the code would hardcode, or the test agrees with the bug. Example: the runbook learner hard-coded the Grafana keys "central" and "admin-zone", and the fixture used the same names. When the runbook repo renamed them, every query proof dropped silently, and neither the tests nor two reviews caught it.
- **YAGNI.** See "Every complexity earns its place" below.
- **Law of Demeter.** Talk to direct collaborators, not their insides. A caller reaching through two objects means the first one needs a method.
- **Separation of concerns.** One module, one job. SOLID is the longer form.
- **High cohesion, low coupling.** What changes together lives together, and modules know as little as possible about each other.
- **Deep modules.** A small interface over a lot of hidden work. A pass-through adds names, not value (see the deletion test below).
- **Fewest moving parts.** Every component, setting, lock or background job is something that can fail. Each earns its place, and you remove one when you can.
- **Design the wrong paths and the cleanup, not only the happy path.** For everything a change creates (a file, a branch, a row, a session, a cache entry), say who removes it and when, and what happens when a step fails halfway, runs twice or is killed. Be pragmatic: when the platform already removes it (a temp folder on a short-lived VM, a bucket lifecycle rule), cite that and add nothing; when nothing removes it, build the eviction now. Example: Slack images saved to `/tmp/slack-images` on an AgentCore microVM go away when the microVM ends (15 minutes idle, 8 hours at most), and a failed save removes its half-written `.part` file.
- **Fail fast.** Stop at the first broken assumption, with a message that says what broke.
- **Optimistic over pessimistic.** Prefer the design that keeps latency low and throughput high: work in parallel, detect a conflict early and fix or retry only the piece that conflicts. Take a lock, a queue or serial execution only when no reasonable optimistic option exists, and state its cost in time. Example: a write lock that queued every runbook-learner run for 13 to 16 minutes was replaced by checking each draft against the newest base and turning a known-safe conflict (an identical page that already exists) into an add, the way merge queues and stacked-PR tools replay changes onto the newest tip.
- **Fewest workflow steps.** Before adding a step to a workflow, ask whether it needs a model at all and whether an existing step already has the inputs and tools to do the job. Add a step only when none can. Example: a separate agent step to run a draft's queries became one rule in the investigation step, which already had the query tools.
- **No risky automation.** When an automatic decision could hurt availability, data or debuggability, report it and let a person decide.
- **Least privilege.** Each part gets only the access it needs.

## Before writing code: the ladder

Read the code the change touches and trace the real flow first. Then stop at the first rung that holds:

1. Does this need to exist? If the need is speculative, skip it and say so in one line.
2. Is it already in this codebase? Reuse the helper, type or pattern. Search before writing. The step is `references/core.md` rule 5.
3. Does the standard library do it?
4. Does the platform do it? A database constraint over app code, a native input over a widget library.
5. Does an installed dependency do it? Never add one for what a few lines can do.
6. Can it be one line?
7. Only then, the least code that works.

When two options are the same size, take the one that is correct on edge cases. A parser is not a validator: `email.utils.parseaddr` accepts `@missing-local.com`.

**Every new resource earns its place against what already exists.** Before adding a database table, column, queue, bucket, secret, setting, environment variable, service, alert route, channel or file, list what already exists for a similar job and check each candidate. Reuse one when it already means the same thing. Create a new one only when each candidate would break something or take on a second meaning, and say which, with a `file:line` for each. A resource whose purpose has to be stretched to fit ("this table also holds X") is two things under one name, and that is worse than one small new resource.

Example: recording which PagerDuty incidents the monitor had open. The probe results table would have shown each record as a failing check on the status page, and its 30-day prune would have dropped the record of a long incident. The budget alerts table and the settings table were each documented for one other job. So a new 9-line table with a one-line purpose comment was the right call, and the PR said why for each candidate.

## Never cut

Less code never means less of these: validation at trust boundaries, error handling that prevents data loss, security checks, accessibility basics, and anything the user asked for by name.

## Errors never go silent

1. **A key error** loses or corrupts something a person or a later step relies on: data not stored, a check skipped, a guard turned off. **A non-key error** costs only convenience, like a missing short link or a chart that did not render.
2. **Every key error does three things.** It records the failure where the data would have been (a status on the row, never just a missing row). It logs with context. And it reaches a human through the repo's existing alert route, never a new one.
3. **Non-key errors** are logged with context and nothing more.
4. **Before building, read how the repo alerts today** (a monitor probe, a chat thread, an error tracker, a metric with an alarm, a status page) and use that route.

Failure this prevents: a background job that was "best effort" stalled for days with nothing alarmed, because its failure was only a log line. "Fail open" and "logged and swallowed" are fine for convenience, never for something a later step trusts.

## Every complexity earns its place

Before adding anything, say what it buys. If the answer is "it might be useful", cut it.

Specifically, remove:

- **Retries and fallbacks nobody measured.** A retry hides a failure you have not diagnosed. A three-deep fallback chain is three untested paths. Before adding one, read the code that would fail and cite the line that shows the failure can happen. Example: a "fetch the branch if the fresh clone lacks the commit" fallback went into four steps and a new field went through the workflow; a plain `git clone` carries every branch, so the commit was always there, and the PR had to be rebuilt.
- **Backward compatibility nobody asked for.** Supporting an old shape doubles the surface. Delete the old shape instead.
- **Config for things that never vary.** A flag with one value is a constant plus a branch.
- **A new setting when an existing value already says it.** Before adding a variable, switch or field, look for a value the system already has that carries the same fact. Example: a Grafana dashboards module got a new `runbook_dashboards` on/off variable, and then needed a CI guard because turning it off would delete every dashboard. The repo's required `env` variable already said which targets were production, so the switch and its guard both went.
- **Abstraction with one implementation.** Wait for the second.

**Question the mechanism when fixes pile onto it.** When each fix to a design adds another setting, special case, limit or degraded path, the fixes are telling you the base choice is wrong. Stop patching and ask: what is the most direct way to do exactly this? Then replace the mechanism. Example: a learner read its earlier notes through a general sessions API; five review rounds added two settings, transcript exposure, a refused-read path, a row limit and paging. One narrow read on the learner's own route removed all of it.

**When the result looks complex, look for less before anyone else has to.** Fixes piling up is one signal; a long list of rules, cases or "what changes" items is another, even when every item is correct and tested. Before showing a design or PR, read it as a newcomer would. If it needs many rules to explain, ask on your own: can the same behaviour come from one rule, one fact the system already holds, or fewer moving parts? Keep the rules above (one home per fact, direct beats general, every complexity earns its place) and the sweep below in force while you cut. Example: a fix for two gateway copies sharing one OAuth login grew to seven rules (timestamp comparisons, a tie rule, a required timezone, a stopping rule) and passed review. The user called it complex. One rule did the same job: before a refresh, take the stored token if it changed since this process last took it, otherwise keep the one in memory. That replaced the timestamps, the tie and the timezone, and cut the added lines in that file from 64 to 19.

**Self-review before anyone sees a design.** Before a spec, plan or PR reaches a person, sweep it for these seven smells and fix them in the draft, without waiting for the reviewer or the user to ask. In a PR the sweep covers every function the diff touches, not only the added lines: "it was already there" does not excuse a smell in code you edited.

1. **A fact with two homes, or a fallback copy.** Give it one home and fail loudly when it is missing. Example: an agent's callback address was sent on every call and also baked into the runtime by a deploy script whose own comment said "keep these in sync". The fix sent it on every call and deleted the baked copy, so a missing value now fails with "not set" instead of silently using a blocked port.
2. **One name with two meanings.** Rename until each name means one thing. Example: `ORCHESTRATOR_INTERNAL_URL` was both the address handed to the agent and the UI server's `/api` target; renaming the first to `AGENT_ORCHESTRATOR_URL` removed a trap where setting it would break the UI.
3. **A comment or docstring the code contradicts.** Trust the code, and fix or drop the stale text in the change that touches it. Example: a module docstring said a route "waits for the build"; the handler returned at once, and an argument built on the docstring had to be withdrawn.
4. **A temporary piece with no removal step.** Every temporary rule, route copy or flag names the step that removes it and the gate for that step.
5. **A fallback, default or retry with no cited failure.** Look for `|| ""` that skips work, an empty `catch`, "return null on 404", "best effort", "keep polling". Cite the line that shows the failure can happen, or remove it and fail loudly. Example: a CLI returned an empty log on any error and polled on through a 404 for a job; the builder stores the job before dispatch returns its id, so both paths only hid real failures.
6. **An error path with no class.** Each error the change touches is key or non-key ("Errors never go silent" above). A key error records, logs and alerts through the repo's existing route; a non-key one logs with context. A silent `return ""` is neither. Example: a failed token push wrote a warning and a summary field that nothing read, so the next session broke and nobody was told.
7. **The same snippet in several files.** Code repeated across the files the change touches gets one home in the repo's shared module, under one name. Example: five files built the same two auth headers, under two different helper names.

Run the sweep as a list: for each smell, every instance found and its verdict (fixed, or kept with the cited line that justifies it). A smell with no instances says what was searched (for example a grep for `|| ""`, `catch` and `return null` in the touched files). A review verdict without this list is not finished.

The user said it plainly after catching two of these: "please think of things like these instead of waiting for my comments." Smells 5 to 7 were added after the user had to ask a third time in one day for fallbacks to be removed and code simplified.

**Direct beats general.** Reuse a shared, general API only when it is also the simplest way to get exactly what you need. A narrow call in the feature's own code usually wins over a general one plus settings to fence it in.

**No citation, no claim.** Every statement about code (what it does, what exists, what something can or cannot do, what a change would cost) carries a `file:line` citation to the code that shows it, the way Wikipedia needs a source for every claim. This holds in chat as much as in documents. Trace the actual code flow and cite the lines along it.

**Test every claim about an option before the reader sees it**, its cost and feasibility as much as its facts. The reader decides from what you write; a claim they agree to on first reading becomes their decision. Before saying something needs new work, cannot be done or costs a day, search the codebase for a mechanism that already does it, and settle the open questions you can settle by reading code yourself. Read each option's code path and write one line on what the user will actually see: where it posts, who is notified, what else it changes. Drop an option you have not traced, and the weaker of two that overlap. Examples: "add the workflow to the progress-thread setting" was offered for one quiet thread per ticket, but that path broadcasts every step to the whole channel; and a fix was offered as "needs an engine change, because script steps can't loop back", and the reader agreed; the engine already had a `loop` step (check script, fix agent only on failure, repeat) that another workflow used, so the fix needed no engine work at all.

**The deletion test.** Imagine deleting the module. If the complexity vanishes, it was a pass-through: inline it. If it reappears across its callers, it earns its place.

## Keep v1 small

Bare minimum in v1. Everything else goes in a "later" list, written down so it is a decision and not an omission. A v1 that ships and gets used beats a v2 that is still being designed.

The later list holds features. A corner cut inside code that ships is marked where it is cut, with its ceiling and the trigger to revisit it: `# simplified: one global lock; per-account locks once writes pass 50 a second`. A marker with no trigger is how later becomes never. Before a release, grep the markers and list any that name no trigger.

## When it is a bug fix

**Offer two options, never a patch.** For every failure, give the long-term right fix (what removes the class of failure at its root) and the pragmatic fix (the cheaper one we can take now), each with the trade-off we accept by taking it, named plainly: what it costs, what it leaves open, and what would make us move to the long-term fix. A patch is neither: a prompt line, a special case or an extra retry that makes this instance pass and leaves the cause in place. Example: a learner run failed its last review round on a placeholder the reviewer itself had suggested. "Tell the reviewer not to suggest placeholders" is a patch. The pragmatic fix was letting the drafter run the repo's own build check before handing off, so build errors stop costing review rounds; the long-term fix was a placeholder syntax that can't clash with real log text. Recommend the long-term fix by default. Recommend the pragmatic one only when the long-term fix needs a lot of build or is overkill for the problem, and say which. When the pragmatic one is taken, the long-term fix goes on the project's to-do list at once, and you say where. Never write "later" or "a follow-up" without that entry. Keep the two labelled and never blur them.

A bug report names one instance. Ask what kind of mistake it is, grep for every other place the code makes the same mistake, and fix those too. Otherwise the same bug returns wearing a different filename. Fix it at the shared point: grep every caller of the function you are about to change and put one guard there, not one per caller. Finding the cause is the `diagnose-bug` skill.

## Performance: measure, keep or revert

Do not make something faster until something is measured slow.

1. **Baseline.** Measure first, with a command you can run again. Write the number down.
2. **Find the bottleneck**, not the suspect. Read the query plan before adding an index. Read the trace before memoising.
3. **Change one thing.** Three changes measured together give one number nobody can attribute.
4. **Re-measure the same way:** same command, same conditions, same cache state. A cold baseline against a warm result measures the cache.
5. **Decide strictly.** Beyond run-to-run noise and tests green: keep, with before and after in the commit message. Within noise, worse, or a test went red: revert. **Neutral is a revert.**
6. **Log every attempt, kept and reverted,** in the PR description's Evidence paragraph. A reverted idea leaves no trace in git, so it gets tried again.
7. **Guard the metric users feel** with a budget in CI or a field alert.

**Never present a number you did not measure.** Reading code finds "potential impact", never a measurement. Lab and field numbers are different numbers; label which one you have.

Backend traps worth naming: a list endpoint without a limit; one query per row; a cache key that omits an input the response depends on (tenant, viewer, locale), which serves one user's data to another; a pool raised instead of finding what holds connections.

## Pull requests

Keep each PR under about 200 lines of production code, and atomic: one reviewable change that stands on its own. Bigger work becomes a stack, each PR built on the one before. Estimate the size before writing code.

Slice vertically where you can: each PR is a thin path through every layer that works and can be checked on its own. Backend first and UI later ships code nobody can exercise until the last PR. The exception is a wide mechanical change (a rename, a retyped shared symbol) that breaks every caller at once: expand (add the new form beside the old), migrate callers in batches with one PR each, then contract (delete the old form) once nothing uses it.

A PR body says what the PR does now, written with the `explain-simply` skill: full sentences, each design decision with a short before and after example, and a small tree diff where it is clearer than prose. No dense tables of fragments, private plan numbers, review history, or names of the skills or agent tools behind the work. Fold a fix into the sentence it changes; never append review-fix logs or fixed-in tables. Then two short paragraphs. **Evidence:** before and after, as a test run or output, and a screenshot when the change is visual. **Merge danger:** a one-way or two-way door (can it be rolled back cheaply?) and the blast radius.
