# Testing

Applied by write-spec, write-plan and implement-plan. Referenced, never copied.

## The loop

- **Red.** Write the failing test first. Run it and watch it fail for the reason you expect: the feature is missing, not a typo or a bad import. A test that passes on its first run proves nothing, so fix the test.
- **Green.** Write the least code that makes it pass. Run the repo's full suite, not just your file.
- **Refactor only on green.** Tidy (rename, extract, dedupe) only while every test passes. Then a red after tidying means the tidy broke it; tidying while something is already red leaves you unable to tell which change did.
- Code written before its test: stash it, confirm the test fails without it, restore it. Never skip the red.
- Bug fix: reproduce it in a failing test before touching the fix.
- One slice at a time: one test, then its code. Not every test up front.

## Fat tests

- One test per scenario a user would recognise, not one per function. Name it as the scenario: `test_after_the_rename_every_reply_uses_the_new_handle`, not `test_mention_for`.
- Go through the public entry point. Fake only what crosses a process boundary: network APIs, the clock, randomness. Use a real test DB where it is cheap. Never mock your own modules.
- Assert everything the user would see in that scenario, in that one test. "One behaviour per test" means one scenario, not one assert.
- A thin test is fine for a tricky pure function. It is never the only proof.

## A test worth keeping

- **Name the break.** Say which production change would make it fail. If none would, delete it.
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

## The real-world test

Repo tests are often enough. When they cannot show the change working for its real users (a new integration, a bot's behaviour, anything that only shows up once deployed), add one test a person can run against the real system, and design it before the work starts. Use judgement: a refactor or a pure function needs no real-world test.

- **Replay the original ask.** The best real-world test is the request that motivated the change, sent the way its user sent it. Example: a team's chat bot gains an MCP server for its identity provider because it could not answer "which users in this org log in with SSO?". The test is to ask the bot that same question in chat. If it answers from the identity provider's data, the change works. If it still says it has no access, it does not, whatever the unit tests say.
- **Write it down as four things:** the action (a Slack ping, a UI click, a CLI call), the exact input, the expected result, and what failure looks like.
- **Add a negative check where it matters.** For a read-only integration, ask for a write and see it refused.
- **When there is one, nothing is announced as live until it has passed.** Run it yourself, or hand the user the exact steps, before saying the change is done.

## When the repo cannot run tests

Terraform, Helm, shell: say so and why, then use the closest real check. `terraform plan` output review, a linter, a manual checklist mapped to the spec. Every invariant still maps to a check, even when that check is a person reading something.

## Done when

Every new behaviour and every error case has a test that failed before the code existed. The full suite is green with the repo's own command, the output is clean, and the evidence is shown: the command run and what it returned. If the change has a real-world test, it has passed on the deployed system or its exact steps are with the user.
