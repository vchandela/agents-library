# Security checks

For every candidate, before reporting it: is the input attacker controlled, is
the sink reachable, what is the blast radius, and is every step feasible? Then
assign confidence: confirmed, likely, or needs verification. A missing header
with nothing reachable behind it is a hardening note, not a finding.

## Accounts and roles

Authorization testing needs more than one identity, and the identities are yours
or the user's own, never another customer's:

- **Two same-role accounts** for horizontal checks: A's object fetched with B's
  token must answer 404, not 403.
- **A higher-role account** for vertical checks: a normal user reaching an admin
  action must be refused, and the refusal must not leak whether the action
  exists.
- **Two tenants or workspaces** where the product has them: data must not cross.

Without a second identity you cannot test authorization; say so in Not covered
rather than implying it was clean.

## Authentication

**These run against the local app and its test database, never production.**
A forged, stale or swapped token is hostile input even when it is sent once.

- Token with the subject swapped, `alg:none`, an unsigned token, a token from
  another account, an expired token: each must be rejected, with no partial
  data leaked in the error.
- Session fixation: sign in on a known session id; the id must change.
- Sign out must invalidate the server side, not just the client.
- Password reset and magic links: single use, expiry enforced, no account
  enumeration by response time or wording.

## Injection

Every parameter and body field, with the payload appropriate to the sink:

- SQL: `' OR 1=1--`, a quoted string, a numeric context.
- XSS: a stored payload in every field that is later rendered, and a reflected
  payload in every parameter that is echoed; check the encoding in the rendered
  DOM, not the source.
- Path traversal where a name becomes a path: `../../`, URL-encoded and double
  encoded.
- Template or expression injection where a value is rendered by a template.
- SSRF where a URL is fetched: an internal address, a redirect to one, a
  non-HTTP scheme.

Expected: the input is treated as data everywhere; no 500s, no reflected
markup, no file outside the intended directory.

## Headers and cookies

Read the response headers on the main pages and on an API response:

- `Content-Security-Policy` present and meaningful; a nonce or hash, not
  `unsafe-inline` where a script runs.
- `Strict-Transport-Security` on the https site; `X-Content-Type-Options:
  nosniff`; `Referrer-Policy`; frame protection (`X-Frame-Options` or CSP
  `frame-ancestors`).
- Cookies that carry a session: `HttpOnly`, `Secure`, `SameSite`, and a sensible
  expiry. A session cookie readable from JavaScript is a finding.
- CORS: an arbitrary `Origin` must not be reflected with credentials.
- Error pages and 404s must not expose a stack trace, a framework version, an
  internal path or a SQL fragment.

## Rate limits

One request at a time against production: send the same sensitive request twice
in a row and a few seconds apart, and note whether a limit exists at all
(response 429, a backoff header, a lockout). Never prove a limit by loading the
service. The limit's absence is a hardening note unless the endpoint is
sensitive (sign in, reset, code entry), where it is a finding.

## Leaked data

Open the network panel and read every JSON response the flow touches:

- a field the screen never shows (a role, an internal id, an email of another
  user, a flag), which is excessive data exposure;
- another object's data in a list or in a search suggestion;
- the same secrets or tokens in a log the browser can read;
- a debug endpoint, a `/_next` or `/api/health` that reports environment
  details.

One record from the wrong account is enough to prove IDOR; stop at the smallest
proof, then close the tab.
