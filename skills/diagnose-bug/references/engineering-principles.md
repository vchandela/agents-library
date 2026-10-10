# Engineering principles

## The four

- **DRY.** One fact has one home. A second copy is right the day it is written and wrong from the moment either changes.
- **YAGNI.** Build what is needed now. No speculative abstraction for a use case nobody has.
- **KISS.** Prefer boring and obvious. Clever code is a cost somebody pays later.
- **SOLID**, plus separation of concerns and the Law of Demeter. Reach for these when a module starts doing two jobs.

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

## Every complexity earns its place

Before adding anything, say what it buys. If the answer is "it might be useful", cut it.

Specifically, remove:

- **Retries and fallbacks nobody measured.** A retry hides a failure you have not diagnosed. A three-deep fallback chain is three untested paths.
- **Backward compatibility nobody asked for.** Supporting an old shape doubles the surface. Delete the old shape instead.
- **Config for things that never vary.** A flag with one value is a constant plus a branch.
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

**Offer two options, never a patch.** For every failure, give the long-term right fix (what removes the class of failure at its root) and the pragmatic fix (the cheaper one we can take now), each with the trade-off we accept by taking it, named plainly: what it costs, what it leaves open, and what would make us move to the long-term fix. A patch is neither: a prompt line, a special case or an extra retry that makes this instance pass and leaves the cause in place. Example: a learner run failed its last review round on a placeholder the reviewer itself had suggested. "Tell the reviewer not to suggest placeholders" is a patch. The pragmatic fix was letting the drafter run the repo's own build check before handing off, so build errors stop costing review rounds; the long-term fix was a placeholder syntax that can't clash with real log text. Recommend the long-term fix by default. Recommend the pragmatic one only when the long-term fix needs a lot of build or is overkill for the problem, and say which. Keep the two labelled and never blur them.

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
