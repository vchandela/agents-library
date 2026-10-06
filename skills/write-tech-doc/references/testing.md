# Testing

Applied by write-spec, write-plan and implement-plan. Referenced, never copied.

## The loop

- **Red.** Write the failing test first. Run it and watch it fail for the reason you expect: the feature is missing, not a typo or a bad import. A test that passes on its first run proves nothing, so fix the test.
- **Green.** Write the least code that makes it pass. Run the repo's full suite, not just your file. A failure in the full suite that you did not cause still goes in your report by name. A red test you saw and did not mention is a false report.
- **Refactor only on green.** Tidy (rename, extract, dedupe) only while every test passes. Then a red after tidying means the tidy broke it; tidying while something is already red leaves you unable to tell which change did.
- Code written before its test: stash it, confirm the test fails without it, restore it. Never skip the red.
- Bug fix: reproduce it in a failing test before touching the fix.
- One slice at a time: one test, then its code. Not every test up front.

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
- **Testing only the state a fresh user is in.** Changing what a stored value means (a cached flag, a cookie, a local storage key, a row's default) leaves every existing user holding the old shape, and a suite that creates its fixtures fresh never meets it. When the meaning of stored state changes, add a test that starts from the old shape and walks the main path. A shipped example: a cache that held `true` came to mean a version string, every member from before that day looked signed out, and Log in sent them in a loop.
- **A check that walks a list of pages.** A list is blind to the page added next week, and to the forty it never named: one layout test held a single guide, so four others ran wider than the phone and nothing failed. Walk every page the router can serve, and fix the kind of mistake on all of them in the same change, not the one instance someone reported.
- **Reading layout back mid-transition.** A script that sets a size and then measures gets the old value while a CSS transition runs, and reduced-motion styles often give every element a 1ms transition. It looks like a script that never ran. Measure with `transition: none` set, and run layout tests with reduced motion on.
- **Layered tests after a refactor.** Once tests exist at the deeper interface, delete the old tests on the shallow modules it replaced. Keeping both doubles the upkeep and pins the old shape.

## The real-world test

Repo tests are often enough. When they cannot show the change working for its real users (a new integration, a bot's behaviour, anything that only shows up once deployed), add one test a person can run against the real system, and design it before the work starts. Use judgement: a refactor or a pure function needs no real-world test.

- **Replay the original ask.** The best real-world test is the request that motivated the change, sent the way its user sent it. Example: a team's chat bot gains an MCP server for its identity provider because it could not answer "which users in this org log in with SSO?". The test is to ask the bot that same question in chat. If it answers from the identity provider's data, the change works. If it still says it has no access, it does not, whatever the unit tests say.
- **Write it down as four things:** the action (a Slack ping, a UI click, a CLI call), the exact input, the expected result, and what failure looks like.
- **Add a negative check where it matters.** For a read-only integration, ask for a write and see it refused.
- **When there is one, nothing is announced as live until it has passed.** Run it yourself, or hand the user the exact steps, before saying the change is done.

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

Every new behaviour and every error case has a test that failed before the code existed. The full suite is green with the repo's own command, the output is clean, and the evidence is shown: the command run and what it returned. If the change has a real-world test, it has passed on the deployed system or its exact steps are with the user.

List only commands you ran. Reading the code is not running it. A check you skipped is named, with the reason.
