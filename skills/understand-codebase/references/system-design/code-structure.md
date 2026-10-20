# Code structure and algorithm choice

Ask first which one place owns each fact, and whether the question wants any answer, the best answer or every answer.

## Entities and where state lives

Make a class only for a noun that owns changing state, enforces a rule, or links other entities in a way you query. Other nouns become fields, enums or ids. Facts that relate things usually live in a map in one orchestrator, so a claim locks one place, though keeping them on an entity can be fine too. Each data rule sits with the object that owns the data, behind behaviour methods rather than getters, or callers rewrite it and drift (see "Law of Demeter" in [engineering-principles](../engineering-principles.md)).

## Derive or store a fact

Ask whether the two facts can ever disagree. If not, compute one from the other (see "DRY" in [engineering-principles](../engineering-principles.md)). Store both when they truly diverge, as when an expired token must still exist to report that it expired, or when a stored index buys a lookup or a lock boundary you need. A stored copy drifts, so update both in one place.

## Make invalid states unrepresentable

Shape the types so an impossible state cannot be written down, the type-level form of "Correct by construction" in [engineering-principles](../engineering-principles.md). Use one status enum instead of several booleans, and a tagged union when a state carries data. One forgotten flag otherwise makes a state no one meant to allow.

## Composition over inheritance

When behaviour varies along independent axes, give each axis an interface and combine them at runtime. Inherit only where is-a holds for every child, the shared code is stable, and each child keeps the parent's promises. Variants that differ only in constants want a table. A named pattern earns its place once the problem already has its shape, never for one implementation (see "Abstraction with one implementation" in [engineering-principles](../engineering-principles.md)).

## Graph search

Use BFS for fewest hops and Dijkstra or A* for least cost when no weight is negative. The real choice is the visited key. It must hold every fact the next step depends on, such as budget left. Keying on the node alone gives answers that are slightly wrong rather than slow.

## Dependency order and critical path

Use a topological sort for prerequisites and list scheduling for timed jobs on a fixed pool. Get edge direction right first, since the bugs live in graph building. Report a real cycle, never a silent partial order. A free worker takes the ready job with the longest chain behind it, because a fixed order starves that chain.

## Bin packing

Placing items on capacity-limited servers calls for first-fit decreasing, which is a heuristic. With two resources, sort by one combined key, each size divided by its capacity, since one axis alone fails, and check both on placement. Input order strands the large items. When you need the true minimum, which is NP-hard, use branch and bound or integer programming, and only on small inputs.

## Backtracking with propagation and bounds

Use backtracking for every valid arrangement. For a best value, use [dynamic programming](#dynamic-programming) or branch and bound. Deduce forced choices before guessing, and prune with an optimistic bound, one that may overstate what a branch can still reach but never understates it, or the real best answer gets cut. Shrink the state first, say to counts of distinct values. Mutate and undo when undo is simple, but copy the state at each guess when guesses trigger deductions, because an undo that misses state is the classic bug.

## Dynamic programming

Use DP for a best value or a count when subproblems repeat and the state fits in one sentence. Trying every subset is fine up to about 20 items, but trying every ordering is not. Greedy is cheaper, but only when the locally best choice is always safe and what remains is a smaller copy of the same problem. Hunt a small counterexample first, such as coins of 1, 3 and 4 making 6. A wrong greedy still passes the given tests.

## Tries

Match text against many fixed words with a trie, which walks each shared prefix once instead of trying every word. For a few short words, a plain loop is simpler. A cheap filter in front of a costly check is in [Cheap check first](scaling-and-partitioning.md#cheap-check-first).

## Containers that keep big-O honest

When big-O looks right but wall-clock is bad, look for a container that makes each step linear. Use a deque for queues and a hash set for membership. For clashing speed needs, compose primitives and name the invariant tying them. Small tests hide the cost (see "Performance: measure, keep or revert" in [engineering-principles](../engineering-principles.md)).
