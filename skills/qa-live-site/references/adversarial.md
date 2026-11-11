# Adversarial testing

Try to make the system do something it should not, as a normal user with the
freedom to be careless, curious or hostile. Production: only what a normal user
could send, one request at a time. Everything at volume, every forged token and
every tampered id runs against the local app and its test database.

## Hostile input

For every free-text field, every query parameter and every JSON body:

- the empty string, a space, a very long string (10,000 characters), a string of
  only emoji, a string with a NUL, unmatched quotes and angle brackets;
- a valid value with one character changed, and a valid value with one field
  added (mass assignment);
- a number where a string is expected and the reverse; a negative number, zero,
  a float, a value beyond int64;
- control characters and newlines in names, titles and messages.

Watch for: a 500, a stack trace, a value stored and echoed back unescaped (XSS),
a length or charset not enforced on the server, a field accepted that the UI
never sends.

## Broken sequences

- Skip a step: open the second screen's URL directly, submit step three without
  step one.
- Reorder: finish before starting, confirm before paying, answer after
  submitting.
- Repeat: submit the same form twice, press the same button twice quickly, send
  the same API call twice.
- Go back and forward: after a write, go back and resubmit (stale state); after
  signing out, forward into the signed-in page.
- Two tabs: open the same record in two, change it in one, act in the other.

Expected: a defined refusal, never a duplicate write, never a crash, never a
stale screen that still acts.

## Stale and expired state

- Leave a page open past the session or token lifetime, then act. Expected: a
  clean redirect to sign in, the intended action not silently applied.
- Expire a one-time link, then use it twice.
- Change the price, plan or quantity in the client, then submit: the server must
  price from its own record, not the payload.
- Change an id in the URL or body to one that is not yours: the answer must be
  404, not 403 (a 403 confirms the thing exists). This is the security family's
  smallest proof; the adversarial version is doing it through the normal
  screens.

## Tampered ids and prices

- An object id from another account, in a query string, a path, a POST body.
- A sequential id where the UI uses a random one.
- A price field, a discount, a plan id, a currency, a coupon count.
- A created-at, an owner id, a role or a flag that the client should not set.

Every one is a finding if it is accepted; record the exact request and the
response.

## Races

Only where the target is yours or local: fire two identical writes at one
resource at the same instant; double-click a submit; race an answer against a
finish. Locks that hold at one request often do not hold at two. Report the
outcome, not the theory.

## What to write down

For every attempt: the input or sequence, what should have happened, what did,
and the smallest evidence that proves it (the request, the response, the stored
row, the screen). If nothing broke, the class goes in the verdict's Held line.
