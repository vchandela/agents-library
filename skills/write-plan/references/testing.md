# Testing

## Contents

- The loop
- Test speed when many agents share one machine
- Pick the kinds of test the change needs
- Fat tests
- A test worth keeping
- Anti-patterns
- The real-world test
- When the repo cannot run tests
- A claim and its evidence
- Done when

## The loop

- **Red.** Write the failing test first. Run it and watch it fail for the reason you expect: the feature is missing, not a typo or a bad import. A test that passes on its first run proves nothing, so fix the test.
- **Green.** Write the least code that makes it pass. Run the repo's full suite, not just your file. A failure in the full suite that you did not cause still goes in your report by name. A red test you saw and did not mention is a false report.
- **Refactor only on green.** Tidy (rename, extract, dedupe) only while every test passes. Then a red after tidying means the tidy broke it; tidying while something is already red leaves you unable to tell which change did.
- Code written before its test: stash it, confirm the test fails without it, restore it. Never skip the red.
- Bug fix: reproduce it in a failing test before touching the fix.
- One slice at a time: one test, then its code. Not every test up front.
- **Fast tier while building, heavy tier once.** While building, run the fast tier: the tests that read what you changed (search the tests for the file, route, selector or symbol), the cheap whole-repo guards (wiring, links, copy, schema), and a parse or collect of every file a script edited. Run the heavy full tier once, on the final head. A long run started first answers in 20 minutes what the fast tier answers in seconds: one full run of 27 minutes was spent on a test database behind main, and a docs-only change merged without the fast checks that read documents and turned main red. A repo with a test-selection table takes the selection from the table instead of searching by hand.

## Test speed when many agents share one machine

Several agent sessions on one machine share its cores and test database. A lock lets one run use the shared database at a time. The rules below remove repeated work before making any single run faster.

- **Measure from the run log.** A run log is the record each run writes. By 22:50 on 9 Nov 2026, one 10-core M5 laptop's run log had 217 locked starts from 24 worktrees. A locked start is a run that takes the shared test lock. A worktree is a second checkout of the repository with its own files. A checkout survey that day found 19 git trees (the files at one commit) open in more than one worktree. Anthropic's CI article ("Agentic coding is straining CI") reports job volume rising 25 times in six months.
- **Never run the same code twice.** A result cache stores each run's result under a key. The key names everything the result depends on. That is the git tree, the lockfile, the runtime version, the environment revision, and the test command and its arguments. The git tree is the exact content of a commit. The environment revision is the version of everything outside the code, such as a template database's migration revision. Reuse a green result. Never reuse a red one: Bazel does not cache a failed test by default. Nx replays a task when its inputs did not change. Turborepo hashes its inputs.
- **Scope a run from one table.** The table maps each changed path to the tests that path can affect. Generate it from the import graph: which module imports which. Two tests keep the table honest. A drift test fails when the table and the graph disagree. An exhaustiveness test fails when a tracked file is missing from the table. There is no catch-all row, a row that names every path no other row names. A module imported across many test areas maps to the full suite. The threshold is a named constant with its reason. A file that no import shows, such as a template, CSS, content, SQL or TOML file, maps to the full suite. The pytest-testmon docs say it does not track static files. Fowler's article "The Rise of Test Impact Analysis" says a test's outcome can depend on external input such as resource files. The Testar tool described there could not tell which tests read one.
- **Gate the merge on one recorded full run.** The record is a green full-suite run on the exact tree being merged. That tests the merged tree once. GitLab runs the full suite after approval. Home Assistant runs it when core files change. A reviewer checks the record instead of rerunning the suite.
- **Add nothing that does not fit one machine.** Do not add sharding, a merge queue service, nightly runs or cloud CI. Sharding splits one suite across several machines, for example with pytest-split. A merge queue is a service that retests merges in order. Do not add a lock slot (a second run allowed to hold the shared lock) on a saturated machine. A machine is saturated when it has no free core; check the load average against the core count first. The load average is the count of processes running or waiting to run. On that laptop, the load average was 27.7 on 10 cores when measured, so another slot would only queue.
- **Size the worker count to the cores, not above them.** pytest-xdist is pytest's parallel runner. Use one worker per core at most. Use its worksteal scheduler when test durations are uneven, so a free worker takes tests from a busy one. More workers gave diminishing returns on that busy machine: going from 3 to 4 saved about 69 seconds in a 5 minute run.
- **Give an end-of-response hook the same runner and log.** Some agents run the suite from a hook after every response. That hook must use the same test runner and log as every other run. Otherwise its cost is invisible to the cache and the log, and repeated work looks free. Cancel the run still going when a newer push supersedes it. CI calls this cancel-in-progress.
- **No fallbacks.** The selection is a pure function of the changed paths. A pure function's answer depends only on its inputs, so the same paths always choose the same tests. An unclassified file fails a test, so someone adds its row. A fallback that quietly runs everything burns the machine. A fallback that quietly runs nothing ships the bug.

## Pick the kinds of test the change needs

Choose per change, name the choice in the plan step, and say why a kind is left out. Each kind catches what the others miss:

- **Unit:** one module through its public entry point, with only the network, clock and randomness faked. For logic with many branches (a token refresher, a parser).
- **Integration:** the real parts wired together over the real protocol, with only the far end faked (a real MCP client against the real server with a local fake upstream). It catches wiring the unit tests cannot see.
- **Contract:** where one part writes a shape another part reads and they ship separately (a config file, a status trailer a monitor parses, a step's output the next step reads), pin the shape on both sides with typed-out values.
- **Live, read-only:** one call against the real external system, when the fake might not match it (an auth flow, a token endpoint's error body).
- **Mutation:** put each fixed bug back, and flip each important branch; a test must fail each time.
- **Static checks:** the repo's linter and type checker on every changed file, plus the checker for each other language touched (`terraform fmt` and `validate`, `shellcheck`, `node --check`, a container build). Run them even where CI does not block on them, and a secret scan on the diff.
- **Failure and concurrency:** inject each failure the spec names (timeout, 5xx, a write that fails, a restart mid-flow) and run the racy path concurrently, asserting the outcome, not just that nothing crashed.
- **Security:** for anything with an auth or allowlist, the refusal paths are tests too: no token, a wrong token, a forbidden tool called directly, and no secret in any log line or response.
- **Unchanged behaviour:** when a change wraps something that already works, the old tests pass unchanged and one test shows the old path still answers through the new wiring.
- **Real-world:** the original ask, on the deployed system (below).

## Fat tests

- One test per scenario a user would recognise, not one per function. Name it as the scenario: `test_after_the_rename_every_reply_uses_the_new_handle`, not `test_mention_for`.
- Go through the public entry point. Fake only what crosses a process boundary: network APIs, the clock, randomness. Use a real test DB where it is cheap. Never mock your own modules.
- Assert everything the user would see in that scenario, in that one test. "One behaviour per test" means one scenario, not one assert.
- A thin test is fine for a tricky pure function. It is never the only proof.
- **Agree the seams first.** Before the first test, write down where you will test (the public interfaces) and confirm them with the user. Prefer a seam that already exists, and the highest one that still shows the behaviour. Fewer seams is better; one is ideal.

## A test worth keeping

- **Name the break.** Say which production change would make it fail, and whether that change would be a bug or a decision. If only a decision (a constant, a message's wording) can fail it, it is a change detector. If no change would fail it, delete it.
- **Mock below what the test depends on.** Before replacing a method, list what it does besides return a value. A mock that swallows a config write the next step reads makes the test pass and production fail. Mock the slow or external call one level down.
- **One fixture per branch.** Give success, error and malformed input their own fake, so the wrong branch cannot satisfy the assertion.
- **Expected values are typed out, never recomputed.** `assert slugify("Hello World") == "hello-world"`, not `== "Hello World".lower().replace(" ", "-")`. A bug in the shared logic sits on both sides and passes.
- **Assert outcomes, not calls.** Check the output, the state, the side effect. A mock earns no assertion of its own.
- **Fakes have the real shape**, with every documented field. A partial fake hides the field production needs.
- **Know the environment before you fake its input.** Read the code that produces the input in this repo (the runner, wrapper or transport between the producer and your code), not the producer's own comment, and follow the repo's existing test helpers for it. Example: a workflow step's script printed JSON and its tests fed the next step bare JSON, but the step runner wraps every script's output in a ``` fence. 24 tests passed and the first production run failed on character 0. Build each fake from the producer's code, or from a real captured value.
- **No test-only methods on production code.** A `reset_cache_for_tests()` ships to prod and someone calls it. Build a fresh object, or keep the helper in the tests.
- **A "not None" or "still there" assert usually proves nothing.** Something else often sets the same value earlier. Compare against the value from just before the step (`!= before`), and revert the fix once to watch the test fail.
- **Mutation check before done.** Flip a constant, drop a branch, return empty. At least one test fails each time. If none does, either a test is missing or that code is not needed. In Python, run mutations with `PYTHONDONTWRITEBYTECODE=1` and no `__pycache__`: a same-size edit within the same second reuses the stale `.pyc`, so a mutation looks killed (or a restore looks broken) when it never ran. Run the suite green first: a mutation "caught" by a test that was already failing proves nothing.

## Anti-patterns

- **Change detectors.** `assert MAX_RETRIES == 5` fails when someone changes it on purpose and passes when retrying is broken. Test the behaviour: make every call fail, assert 5 attempts.
- **Mock setup bigger than the test.** Use the real component instead.
- **Grepping source text instead of running it.** The exception is code CI cannot run at all; say so in the test.
- **Flaky or order-dependent tests.** Fix or delete; never retry them green.
- **Testing the framework** rather than your code.
- **Sleeping for a guessed time.** `sleep(0.5)` then assert passes on a fast laptop and fails in CI. Wait for the condition itself (the event arrived, the file exists, the count reached five), poll it, and fail with a named timeout. A fixed delay is right only when timing is the behaviour under test, and then a comment says where the number came from.
- **Waiting on your own long job by polling.** A foreground `sleep` loop blocks the turn until the tool cap (a harness refused a `sleep` 31 times across 9 sessions), and a chain of timed watches wakes the agent with nothing to report (one session armed 23 in about 5 hours). Start the job once in the background with its output in a file, check that it started, end the turn, and let the completion notice wake you.
- **Testing only the state a fresh user is in.** Changing what a stored value means (a cached flag, a cookie, a local storage key, a row's default) leaves every existing user holding the old shape, and a suite that creates its fixtures fresh never meets it. When the meaning of stored state changes, add a test that starts from the old shape and walks the main path. A shipped example: a cache that held `true` came to mean a version string, every member from before that day looked signed out, and Log in sent them in a loop.
- **A check that walks a list of pages.** A list is blind to the page added next week, and to the forty it never named: one layout test held a single guide, so four others ran wider than the phone and nothing failed. Walk every page the router can serve, and fix the kind of mistake on all of them in the same change, not the one instance someone reported.
- **Reading layout back mid-transition.** A script that sets a size and then measures gets the old value while a CSS transition runs, and reduced-motion styles often give every element a 1ms transition. It looks like a script that never ran. Measure with `transition: none` set, and run layout tests with reduced motion on.
- **A list of pages that never checks each one loaded.** A probe walking pages measures a 404 or an error page as clean. Assert each response is OK before measuring it: a craft check passed on a question page that did not exist in the test database.
- **Shared test fixtures drift.** A template database, a cache or a build directory that several worktrees share is at whatever the last run left it. Check its version before trusting a red run: 226 failures in one run were a template built from the main branch, missing one migration.
- **Layered tests after a refactor.** Once tests exist at the deeper interface, delete the old tests on the shallow modules it replaced. Keeping both doubles the upkeep and pins the old shape.

## The real-world test

Repo tests are often enough. When they cannot show the change working for its real users (a new integration, a bot's behaviour, anything that only shows up once deployed), add one test a person can run against the real system, and design it before the work starts. Use judgement: a refactor or a pure function needs no real-world test.

- **Replay the original ask.** The best real-world test is the request that motivated the change, sent the way its user sent it. Example: a team's chat bot gains an MCP server for its identity provider because it could not answer "which users in this org log in with SSO?". The test is to ask the bot that same question in chat. If it answers from the identity provider's data, the change works. If it still says it has no access, it does not, whatever the unit tests say.
- **Test on a representative set, never the whole list.** Each run costs money, a model account's usage cap and fix-loop time, so pick the fewest items that still cover every case. Group the candidates by what each one tests (each rule or branch the change adds, each output surface, each kind of control, one held-out item the change was not written from) and keep one item per group, two only when the group has two distinct kinds. Drop items that repeat a group, that test code the change does not touch, or that cannot change the verdict (an item reported but not counted). Repeat runs only on the side the pass bar depends on. List the dropped items with the reason, so the reader can add one back. Example: a prompt replay planned 14 tickets × 2 arms × 3 runs = 84 runs; grouping by question and surface kept 8 tickets, one run of main and three of the branch, 32 runs, with every case still covered. This is for tests. When the job is to measure a rate (accuracy over a week), count the whole population or a sample sized for the error you can accept.
- **A replay must not reach anywhere real people read.** Replaying a real item (a ticket, a chat thread, an alert) copies its addresses: the channel, the thread, the ticket, the pull request. Every path that can post from a run then points at the real place. Before the first replay, list every outbound path the run can reach (the final comment, a live status message, a progress note, a ticket write, a failure alert), and confirm in the code that each one is switched off for a test run, not only the main one. Then run one replay alone and check that it wrote nothing outside the sandbox before you start the batch. Failure this prevents: a team's replay runs were walled off from the bot's final reply, but a live status message opened at run start had no such check, so the replays posted findings into real support threads and a support engineer reported that the bot was answering threads nobody had asked it about; the user said "please ensure this is not repeated" (9 Nov).
- **Write it down as four things:** the action (a Slack ping, a UI click, a CLI call), the exact input, the expected result, and what failure looks like.
- **Add a negative check where it matters.** For a read-only integration, ask for a write and see it refused.
- **When there is one, nothing is announced as live until it has passed.** Hand the user the exact steps, or run it yourself when it posts nowhere other people read or the user asked, before saying the change is done.

## When the repo cannot run tests

Terraform, Helm, shell: say so and why, then use the closest real check. `terraform plan` output review, a linter, a manual checklist mapped to the spec. Every invariant still maps to a check, even when that check is a person reading something.

## A claim and its evidence

| Claim | Needs | Not enough |
|---|---|---|
| Tests pass | The suite command, run now, zero failures | An earlier run, "should pass" |
| The build works | The build command, exit 0 | The linter passing |
| The bug is fixed | The original reproduction, now correct | The code changed |
| The regression test works | It failed with the fix reverted | It passes |
| An agent finished | The diff shows the change, and you ran its tests | The agent said done |
| Requirements met | Each one ticked against the spec | Tests pass |

"Should", "probably" and "seems to" in a status line mean the check has not run. Run it, then say what it returned.

## Done when

Every new behaviour and every error case has a test that failed before the code existed. The full suite is green with the repo's own command (CI's run on the exact pushed commit counts), the output is clean, and the evidence is shown: the command run and what it returned. If the change has a real-world test, it has passed on the deployed system or its exact steps are with the user.

List only commands you ran. Reading the code is not running it. A check you skipped is named, with the reason.
