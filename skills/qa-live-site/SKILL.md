---
name: qa-live-site
description: Use when running a QA pass against a deployed web application, or checking a screen in a real browser before letting users in. Not for reviewing code or a diff.
---

# QA a live site

## Before clicking anything

**Write down what each state is supposed to be.** States down the side, elements across the top, the expected value in every cell. Then work the cells.

This is the whole skill. Nearly every real defect comes from asking what a state should be, not from clicking around. A screen can grow a mode nobody specified, and no test catches it, because tests ask whether a behaviour works and never ask what a state was meant to be.

## Phases

**1. Smoke.** Console errors, any 4xx or 5xx in the network tab, the page at phone width and at desktop, both light and dark.

**2. Error cases.** Take the spec's list of error conditions and walk it as a checklist. Every documented condition, tried.

**3. Invariants.** The things that must always be true. Try to break each one directly.

**4. Volume and races.** Act fast, fire parallel requests at one resource, race a write against a close. Locks that hold at one request often do not hold at twenty.

**5. Security.** Token with the subject swapped, `alg:none`, garbage. Access something belonging to another user: **it must answer 404, not 403**, because 403 confirms the thing exists. Injection in every query parameter. Stored and reflected XSS. Path traversal. Method tampering. An extra field in a write, to test mass assignment.

**6. Mobile.** Phone widths. Tap targets, rows that scroll sideways, anything clipped.

## Three rules that each cost a wrong conclusion

- **Verify against the deployed build, not the repo.** A pass once reported a critical bug that production had already fixed, because the deployment was ahead of the commit being read. Check the behaviour first, the code second.
- **Use resource timing, not wall clock.** Wall clock through a browser measures your own machine and connection. One pass read a total collapse under load that turned out to be the test client saturating its own uplink.
- **Measure a surprise twice, a different way,** before reporting it.

## Reporting

Severity P0 to P3. Every finding names the exact request or the file and line, and the concrete failure: the input, the state, the wrong outcome.

**Say what you could not break.** A pass that lists only failures reads as though nothing else was checked.

If you created test data, say where it is and how to remove it.

## Verdict

    Suite      [PASS/FAIL]
    Findings   P0 n · P1 n · P2 n · P3 n
    Held       what you attacked and could not break
    Ready      [YES/NO]
    Blocking   1. ...

**"Ready: NO" with an empty blocking list is not a result.** Either name what is wrong, or the answer is yes.
