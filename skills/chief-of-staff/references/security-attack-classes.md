# Security attack classes

Pick the classes the map shows a real boundary for. Do not pick one because a language or library name appears.

## Ordinary classes

- **Injection.** Trace outside input to every dangerous sink: queries, HTML, shell, templates, file paths, redirects, deserialisation. Look past direct paths: data stored safely then used unsafely by other code; injection through field names, keys, headers and metadata; injection into logs, caches and search indexes.
- **Access control.** Not "does a check exist" but "is it the right check, for the right resource, by the right mechanism". Another path to the same change with a weaker check? A body field that overrides what permissions restrict? Authentication without authorisation? Bulk, export and import enforcing per item checks?
- **Files and resources.** Path traversal (symlinks, encodings, null bytes), server side request forgery (redirects, DNS rebinding, URL parser differences), archive extraction, temp files, check then use races.
- **Crypto and secrets.** Weak randomness for tokens; secrets in logs, errors or URLs; missing MAC checks; nonce reuse; timing leaks on comparison; and what happens when crypto fails: does the error path fall back to none?
- **Business logic.** Skipped, repeated or reversed steps; partial failure without rollback; double spend from check then act; negative, zero and overflowing quantities; trust in data "validated on the way in" that another path wrote; expiry and clock boundaries; posture when config is missing, a flag is off or a dependency is down.
- **Feature abuse.** Export as exfiltration, import as injection, search and sort as an oracle, different errors or timings for "missing" and "forbidden", preview tokens scoped too broadly, webhooks as server side request forgery.
- **Chains.** Component A guarantees less than component B assumes (truncation, coercion, normalisation, tenant scope). Stored data reused in a stronger context. Capabilities that grow on refresh, delegation or role change. Restore and rollback that skip current checks. Confirm each link; never assume the next one.
- **Wildcard.** No category. Read the strangest code, half finished and legacy features, API calls the UI never makes, undocumented parameters, reverted fixes in git history, and what the tests do not test. If a comment says why something is safe, verify the comment.
- **Obvious things.** Hardcoded secrets, security TODOs, debug modes reachable in production, seed credentials, unprotected admin or debug routes, committed key files, unpinned or vulnerable dependencies, dynamic eval, permissive CORS with credentials, cookie flags, open redirects, stack traces in errors. A flag is not a finding: trace what it exposes.

## Domain lenses

| Target has | Start here |
|---|---|
| A model, RAG, memory, tools or MCP | Prompt injection alone is not a finding. A guardrail prompt is not a boundary. Map each execution identity, capability, writable context and output, then trace from side effecting tools backwards. |
| Dependencies, CI, releases, updates, plugins | CI config is authorisation code. Walk back from a released artifact to every source, credential, worker and cache. A checksum fetched from the same place as the artifact proves nothing. |
| Multi tenant data, caches, search, export, deletion | A tenant field on a record is not isolation. Pick one record and draw every copy: cache, index, export, backup, restore. Compare two dummy tenants through the same methods. |
| Untrusted work that consumes shared CPU, memory, queues or paid calls | A missing rate limit is not enough. Build an input to cost table and compare aggregate limits with per item limits. Never validate by stressing a service. |
| HTTP, sessions, OAuth, API keys | Walk issue, store, send, use, refresh and revoke for every credential. The real policy is the weakest parallel path to the same operation. |
| Browser code | Start from DOM, navigation, worker, message and storage sinks and trace back. Test logout, account switch and stale tabs with dummy accounts. |
| Cloud, IaC, containers | Render every environment into one table of ports, identities, peers, secrets and resources. Show which credential performs the final operation. |
| RPC, queues, webhooks | For each message family, record the authenticated peer and the authoritative tenant field at every hop. Policy must survive retry, replay and dead letter routes. |
| Native code, parsers, FFI | One table per parser or FFI boundary: accepted length and type, allocation owner, consumer, thread, teardown. A check in one caller does not protect its siblings. |
