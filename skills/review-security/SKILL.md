---
name: review-security
description: Use when code needs a security review, such as a security question about a repo, a diff that touches a trust boundary, or an explicit request to audit a codebase. Not for probing a deployed system; that is qa-live-site. Not for a general code review; that is review-pr.
---

# Review security

Find places where someone with less trust gets something they should not, and prove each one from the source. A missing best practice with nobody harmed is not a finding.

Apply `references/writing-voice.md` and `references/untrusted-input.md`. The attack classes are in `references/security-attack-classes.md`.

## Two sizes

- **Focused** (the default): a question, a diff, one subsystem. Use the parts below that apply. No ledger, no report files.
- **Full audit**: only when the user asks to audit the codebase or for a full report.

If the request could be either, ask one question before starting.

## Safety, in both sizes

- Read source freely. Run the target's code only in a sandbox with no network, a clean environment, writes only to a scratch directory, and time and memory limits. If you cannot get all of that, do not run it: record the check you could not do.
- Dummy users, dummy data, dummy secrets. Never touch a deployed endpoint, a shared service, a real account or another user's data. Never install or fetch dependencies.
- Stop at the smallest proof: one wrong return value, one record from the wrong tenant.

## The bar for a finding

Name all six, or it is not a finding:

1. The lower trust actor and what it can already do.
2. The input or action it controls.
3. The control that should stop it, with `file:line`.
4. The boundary crossed.
5. Who or what is harmed.
6. The result you saw, or that the owner could see.

**Defence in depth is not a vulnerability.** If layer A stops the attack, a missing layer B is a hardening note.

## Three verdicts

| Verdict | Means | Severity |
|---|---|---|
| Confirmed | A full source trace and a bounded result you observed | Yes |
| Needs validation | The trace is real, but one named fact lives outside the repo (proxy config, IAM policy, a header the CDN adds). State the exact fact and how the owner checks it safely | None |
| Rejected | Source or a test disproved it. Keep it, so the next pass does not raise it again | None |

Needs validation is never a parking place for a hunch. A guess with no trace is dropped.

## Severity

Overall severity is never higher than the impact you showed.

| Level | Anchor |
|---|---|
| Critical | No login needed, and the result is code execution, the whole data store, or any account |
| High | An explicit control fully defeated with real consequences: auth bypass, cross tenant read or write, stored script running for other users |
| Medium | A real boundary crossed, with narrow reach or uncommon preconditions |
| Low | Non secret internals disclosed, or a lot of effort for little gain |
| Informational | Confirmed, minimal impact, mainly a step in a bigger chain |

If you cannot state the concrete damage, the severity is lower than it feels.

## Full audit

1. **Map**, each line with `file:line`: what the product is and how it builds offline; every principal and its identity, authorisation and isolation controls; every place outside input enters, followed to its sinks; which controls live outside the repo. Under a page.
2. **Ledger.** One row per entry surface, trust boundary and attack class, each with one status: planned, covered, candidate, deferred, out of scope. Covered needs the paths read. **The ledger is the coverage claim.** "Auth reviewed" is not coverage.
3. **Hunt**, one fresh agent per group of rows, briefed with the map, its rows and the attack class text in full. Method: name the actor, the input and the control, then trace the path after the control decides. Try absent, empty, zero, negative, maximum, duplicate, stale, revoked, reordered and concurrent values. Compare sibling paths to the same effect: the check must be equally strong on each. Found a root cause? Search for its variants. Anything outside its rows goes in an "uncovered" list.
4. **Critic.** A fresh agent reads the ledger and the source and lists missing rows and rows closed without evidence. Repeat until a pass returns nothing, or mark the untouched rows deferred and say so.
5. **Verify.** Every candidate goes to a fresh agent that did not find it: "You did not write this. Try to refute it." It never sees another verifier's conclusion.
6. **Report.** Scope and what was deferred, then confirmed findings (severity, boundary, result, the smallest fix and a regression test), then needs validation with no severity, then hardening notes. A clean pass says so. Do not invent low findings to fill the table.

A full audit ends one of two ways: everything written, or the report stating exactly what was not done. One pass finds roughly half of what repeated passes find; on a second pass, read the last ledger first, and never read a scoped earlier pass as "the rest is fine".

## Rationalisations to refuse

| The excuse | What to do |
|---|---|
| "No rate limit, so it is a denial of service" | Show shared impact and that no other bound applies. Otherwise it is hardening. |
| "The proxy probably strips it" | You cannot see the proxy. Needs validation, with the exact fact. |
| "It crashes, so it is code execution" | Report the effect you observed, not the one it might lead to. |
| "Prompt injection is possible" | Show the code that grants the authority or reaches the sink. |
| "The flag is set wrong" | A flag is not a finding. Trace what it exposes. |

## Done when

Every finding names all six parts with `file:line`, every confirmed one was verified by an agent that did not find it, needs validation items name one exact fact and carry no severity, and the report states what was not covered.
