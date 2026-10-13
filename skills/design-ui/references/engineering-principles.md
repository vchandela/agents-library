# Engineering principles

## First principles

Check every design and every diff against these before anything else in this file.

- **KISS.** Boring and obvious beats clever. Pass the least that works: a commit, not a commit plus its branch.
- **DRY.** One fact, one home. A table declared in code and again in hand-written DDL is two homes.
- **YAGNI.** Build what is needed now. No abstraction, fallback, retry or backstop for a failure nobody has shown can happen.
- **Law of Demeter.** Talk to direct collaborators, not their insides. A caller reaching through two objects means the first one needs a method.
- **Separation of concerns.** One module, one job. SOLID is the longer form.
- **High cohesion, low coupling.** What changes together lives together, and modules know as little as possible about each other.
- **Deep modules.** A small interface over a lot of hidden work. A pass-through adds names, not value (see the deletion test below).
- **Fewest moving parts.** Every component, setting, lock or background job is something that can fail. Each earns its place, and you remove one when you can.
- **Fail fast.** Stop at the first broken assumption, with a message that says what broke.
- **Optimistic over pessimistic.** Prefer the design that keeps latency low and throughput high: work in parallel, detect a conflict early and fix or retry only the piece that conflicts. Take a lock, a queue or serial execution only when no reasonable optimistic option exists, and state its cost in time. Example: a write lock that queued every runbook-learner run for 13 to 16 minutes was replaced by checking each draft against the newest base and turning a known-safe conflict (an identical page that already exists) into an add, the way merge queues and stacked-PR tools replay changes onto the newest tip.
- **Fewest workflow steps.** Before adding a step to a workflow, ask whether it needs a model at all and whether an existing step already has the inputs and tools to do the job. Add a step only when none can. Example: a separate agent step to run a draft's queries became one rule in the investigation step, which already had the query tools.
- **No risky automation.** When an automatic decision could hurt availability, data or debuggability, report it and let a person decide.
- **Least privilege.** Each part gets only the access it needs.

## Before writing code: the ladder

Read the code the change touches and trace the real flow first. Then stop at the first rung that holds:

1. Does this need to exist? If the need is speculative, skip it and say so in one line.
2. Is it already in this codebase? Reuse the helper, type or pattern. Search before writing.
3. Does the standard library do it?
4. Does the platform do it? A database constraint over app code, a native input over a widget library.
5. Does an installed dependency do it? Never add one for what a few lines can do.
6. Can it be one line?
7. Only then, the least code that works.

When two options are the same size, take the one that is correct on edge cases. A parser is not a validator: `email.utils.parseaddr` accepts `@missing-local.com`.

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

**Direct beats general.** Reuse a shared, general API only when it is also the simplest way to get exactly what you need. A narrow call in the feature's own code usually wins over a general one plus settings to fence it in.

**Trace an option before you offer it.** For every fix or option you propose, read its code path and write one line on what the user will actually see: where it posts, who is notified, what else it changes. Drop an option you have not traced, and drop the weaker of two that overlap. Example: "add the workflow to the progress-thread setting" was offered for one quiet thread per ticket, but that path broadcasts every step to the whole channel.

**No citation, no claim.** Every statement about code (what it does, what exists, what something can or cannot do, what a change would cost) carries a `file:line` citation to the code that shows it, the way Wikipedia needs a source for every claim. This holds in chat as much as in documents. Trace the actual code flow and cite the lines along it. A statement you cannot cite is not stated as fact: verify it, cite it, or label it plainly as an unverified inference.

**Test every claim about an option before the reader sees it**, its cost and feasibility as much as its facts. The reader decides from what you write; a claim they agree to on first reading becomes their decision. Before saying something needs new work, cannot be done or costs a day, search the codebase for a mechanism that already does it, and settle the open questions you can settle by reading code yourself. Example: a fix was offered as "needs an engine change, because script steps can't loop back", and the reader agreed; the engine already had a `loop` step (check script, fix agent only on failure, repeat) that another workflow used, so the fix needed no engine work at all.

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

A PR body says what the PR does now, in the voice of `references/writing-voice.md`: full sentences, each design decision with a short before and after example, and a small tree diff where it is clearer than prose. Then two short paragraphs. **Evidence:** before and after, as a test run or output, and a screenshot when the change is visual. **Merge danger:** a one-way or two-way door (can it be rolled back cheaply?) and the blast radius.
