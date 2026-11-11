# Throughput and correctness

The user holds the chief of staff responsible, always, for how much correct work reaches production, and for its impact (Vivek, 10 November 2026: "it is your duty to make sure that my throughput is always high while maintaining the correctness of my work"). The failure it prevents: three pull requests queued behind each other because each bumped the same version lines; a merge-tree check found all three conflict in CHANGELOG.md, pyproject.toml and uv.lock (session b10ddf4e, 10 Nov 2026).

## The loop

1. **Measure before you think.** At every batch, read the cadence from the sources: merges per day (`gh`), how long each PR waited and why, the run log (`~/.claude/flows/suite-runs.log`; waited and seconds), which files conflict, stalls and idle sessions. Compute each number with a command in the same turn (`references/core.md` rule 2).
2. **Name the one constraint now.** Find what slows the most work (one shared file every PR edits, a stuck lock, a sleeping laptop, a review nobody picked up) and name the thread that owns the fix. Fix the kind, not the instance.
3. **Look outside before you design.** Read how mature projects solve the same problem, in their repos and docs and never from memory. Bring the ambitious option next to the obvious one (`references/ambition.md`), with numbers before and after.
4. **Ask every thread, at every check-in,** what work in its pipeline would raise throughput or catch a mistake earlier. When throughput is the constraint, tooling goes before feature work, and you tell the threads so.
5. **Never trade correctness for speed.** The gates stay: a full run on the exact tree, a reviewer's verdict, and the user's legal hard lines (a legal deadline or claim is always P0). Remove repeated work and waiting, never a check. Keep the tooling deterministic and cheap, with no special-case patches and no fallbacks.
6. **Order work by impact.** Say which items move the business most, and flag threads busy with low-impact work as a suggestion to the user, never as an order to the thread.

## Where the waste is now (measured 11 Nov 2026)

The test and CI work did its job on cost, queue and latency. Full-suite p90 fell from 1,430 s (25 Oct) to 681 s (11 Nov); slot waits p90 from 1,182 s to 459 s and the longest from 85 to 32 minutes; full runs per merged PR from 19 to 3.3; merges per day rose from 12 to 53; open to merge p90 fell from 68.3 to 13.4 hours; the result cache returned 3.4 hours of suite time in one day.

The rate at which runs are wasted did not fall. About 28 of 139 candidate moments in the seven-session transcript analysis were a full suite spent on a head that could not count. The levers, in order:

- **Eligibility, not speed.** A gate run taken while main moves is dead by the merge gate's overlap rule. Hold merges while a critical-path gate runs, and repeat a run after a move only on the rebased head. A changed path with no table row makes a "scoped" run the whole suite.
- **The pre-gate checks.** The table's drift test, the coverage floor locally, the new or changed test at the head, the content checker's reports, and the self-solve before the blind. Each has cost a full run.
- **A positive check for every waiter.** A thread waiting on a process that died sends no message. Name the file, line or status each waiter reads; the motion sweep catches suite end lines and interactive notices, but a billing stop, a lock holder or a permission prompt needs its own check.
- **The coordinator's own claims.** The previous admin's largest cluster was a status or tool fact stated without checking: production called healthy, a macOS block that did not exist, launch blockers taken from card titles. Run the command that reads the source before stating the fact (`references/core.md` rule 2).
- **Shared state is a gate input.** A cache-off experiment can write a red line the gate reads; a migration re-chained under the same revision id leaves a stale template the lock tool thinks is current. Mark experiments, recreate templates, and never pass a blocking hook.

The detail, with session line numbers, is in the project's bottleneck report of 11 Nov 2026.

## How it reaches the user

This duty does not lift the silence. Think continuously and keep the ideas in the registry. An idea that needs no decision from the user goes to the thread that owns it. One that needs the user is a single item under "Needs you" with your pick, or a line under "Suggestions" on the board.
