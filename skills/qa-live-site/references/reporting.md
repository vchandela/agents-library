# Reporting

## The finding shape

Every finding uses exactly these fields, in this order:

```
### F<n>: <title, a sentence naming the defect>
Severity: P0|P1|P2|P3 - <one line on why that severity>
Where: <URL or file:line; the flow and state>
Repro: <numbered steps, exact: the URL, the input, the click, the request>
Saw: <the exact outcome, with the value: the status, the text, the number>
Expected: <what the spec, the state grid or the invariant says should happen>
Evidence: <the smallest proof: request and response, console line, DOM excerpt,
  or screenshot path; a screenshot that failed to capture is retaken, never cited>
Fix: <the smallest change that removes the cause, pointing at the layer>
Confidence: confirmed | likely | needs verification
```

Severity is about the reader, not the code:

- **P0** - data loss, another person's data visible, a paid flow broken, or the
  site unusable for a normal user. Ship stops.
- **P1** - a normal flow broken or unsafe with a workaround, or a security
  weakness reachable by a normal user.
- **P2** - a real defect a reader hits in an uncommon state, or a misleading
  screen; the pass can ship with it.
- **P3** - polish, wording, a hardening note; listed, not blocking.

## One root cause, one finding

The same mistake on five pages is five lines in one finding, with every page
listed under Where. Do not file five cards for one cause. The test: fixing one
place fixes all of them. If it does not, they are different findings.

## Evidence rules

- The evidence is the smallest artifact that proves the observation: the raw
  request and response, the console line, the DOM excerpt, the stored row, or
  the screenshot. A finding with no artifact is a hypothesis, not a finding.
- **Fresh evidence.** A claim about the live site needs its observation in this
  pass; a description of a fix, a commit, or an earlier run is not evidence that
  the thing works now.
- **Proof bar for "it works":** a trigger, a stable end state, and a side effect
  (a request, a stored row, a reload that still shows it) in one walk. "It
  opens" proves nothing.
- A surprising result is measured twice, the second time a different way, before
  it becomes a finding.
- Retake a bad screenshot before writing anything from it.

## The verdict

    Suite      [PASS/FAIL]
    Findings   P0 n · P1 n · P2 n · P3 n
    Held       what you attacked and could not break
    Not covered  what was out of reach, and the blocker
    Ready      [YES/NO]
    Blocking   1. ...

- **Held** lists the attacks that failed, so a clean area reads as clean.
- **Not covered** names every path, account or environment the pass did not
  reach, with the blocker. It never implies coverage that did not happen.
- **Ready: YES** requires a rollback plan; see `shipping.md`.
- **Ready: NO** with an empty Blocking list is not a result.
