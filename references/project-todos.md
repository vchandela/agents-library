# Project ToDos

Every project has one main Notion page, and its ToDos live there and nowhere else. This applies to every agent on the project: the author, the reviewer, a coordinator, a helper thread.

## Know the page

- Every agent knows its project's main Notion page. Look for it in the flow's state file (`store`), the project's memory, or the brief.
- If you cannot find it, ask the user before you defer anything. Never keep a private list instead.
- The ToDos sit under a heading 2 called "ToDos", as to-do checkboxes. If the heading is missing, ask before you create it.

## What goes on it

Anything left for later, from any source, in the same turn it comes up:

- a "later", a "not in this PR", a "phase 2", a "left as is, on purpose" in a PR description, spec, plan or findings page;
- a merge-order gate, an "after the deploy, check …", a real-world test still to run;
- a follow-up ticket, a question parked for the user, a decision someone else owes;
- an after-deploy check, or a removal due "a week after the deploy" (a temporary gate, a patch marker, a fixture);
- an item a peer session hands you.

**Write it on the page yourself. Telling another thread is not enough.** A ToDo sent to a reviewer, a lead or the coordinator, and kept nowhere else, is lost when that session compacts or closes. Whoever finds the ToDo puts it on the page in the same turn, then tells the others if they need to know. When you take up this rule, check that every ToDo you have already sent to another thread is on the page now. Failure this prevents: a thread told its reviewer and the coordinator that a replay gate and a patch marker come out a week after a deploy, and wrote it nowhere else; the user said "instead of just telling the threads, it is important to keep all ToDos in the main notion page" (9 Nov).

Each line says what to do, what it waits on, and where it came from (the PR, ticket or page). A PR description is read once and closed; the main page is where the project's open work lives. Failure this prevents: four phase-2 moves sat only in a PR's "Left as they are" section until the user found them.

## Keep it current

The list is a living view of what is open, not a log.

- **Add** an item the turn it is deferred.
- **Update** it when its state changes: approved, blocked, moved to a ticket, a new owner.
- **Tick** it when it is done, with one line on how (a merge sha, a run's result). When the plan changes, tick the old item with what replaced it ("moved to ARTM-638", "dropped: Pylon holds the context") rather than leaving it open.
- **Delete** an item only when it was never real (a duplicate, a mistake).

Before each hand-off to the user, and when a stage or project closes, read the whole list once and bring it up to date.

Only real deferrals go here. Low-hanging work gets done now, not listed.
