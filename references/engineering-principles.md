# Engineering principles

Applied by the pipeline skills. Referenced, never copied.

## The four

- **DRY.** One fact has one home. A second copy is right the day it is written and wrong from the moment either changes.
- **YAGNI.** Build what is needed now. No speculative abstraction for a use case nobody has.
- **KISS.** Prefer boring and obvious. Clever code is a cost somebody pays later.
- **SOLID**, plus separation of concerns and the Law of Demeter. Reach for these when a module starts doing two jobs.

## Every complexity earns its place

Before adding anything, say what it buys. If the answer is "it might be useful", cut it.

Specifically, remove:

- **Retries and fallbacks nobody measured.** A retry hides a failure you have not diagnosed. A three-deep fallback chain is three untested paths.
- **Backward compatibility nobody asked for.** Supporting an old shape doubles the surface. Delete the old shape instead.
- **Config for things that never vary.** A flag with one value is a constant plus a branch.
- **Abstraction with one implementation.** Wait for the second.

## Keep v1 small

Bare minimum in v1. Everything else goes in a "later" list, written down so it is a decision and not an omission. A v1 that ships and gets used beats a v2 that is still being designed.

## When it is a bug fix

A bug report names one instance. Ask what kind of mistake it is, grep for every other place the code makes the same mistake, and fix those too. Otherwise the same bug returns wearing a different filename.
