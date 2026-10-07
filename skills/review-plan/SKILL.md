---
name: review-plan
description: Use when a plan needs adversarial review before implementation starts. Not for reviewing code or a diff; that is review-pr.
---

# Review a plan

You did not write this plan. Read `references/handoff-protocol.md` before starting: if you wrote it, stop and hand it to a different agent.

Apply `references/use-your-judgement.md` and `references/stop-decide-hold.md`: the checks below are a floor. Report what an expert reviewer would catch beyond them.

The person who wrote this will not grow if you go easy on them.

## Order

**1. Steelman it.** Say what the plan is trying to do and why, in your own words, before criticising anything. If you cannot, you do not understand it well enough to review it.

**2. Attack it.** Find logic gaps, missing edge cases, wrong ordering, unstated assumptions, and anything that breaks at 2am in production. Skip style. Find what will actually break. Three checks that caught real misses:

- **Who else writes this at the same moment?** For every fixed path, key or row the plan writes, find what runs in parallel on the same machine or store. Search the repo's own notes on concurrency. Example: a plan saved Slack images to `/tmp/slack-images/<id>.png`, and four workflow steps ran at once in one microVM. One step could read a file while another was rewriting it. Round 1 missed this.
- **Every caller of a shared entry point.** A change to a shared CLI, prompt banner or helper reaches every caller, including ones that loop over many items. Grep for all of them. Example: "open every image" was right for one thread and wrong for a step reading 20 incident threads.
- **Every planned test names its break.** Revert the fix in your head. If the planned test still passes, that is a finding. Example: a write-then-rename test that checked "file complete, no `.part` left" also passed with a direct write. Checking that the inode changed fixed it. See `references/testing.md`.

**3. Fix it.** Every issue gets a concrete fix. Not "consider handling errors". Show what handling that error looks like.

**4. Cut it.** Apply `references/engineering-principles.md`. Remove retries and fallbacks nobody measured, backward compatibility nobody asked for, and abstraction with one implementation.

**Fixes use the repo's conventions.** A required fix must use a pattern the repo already has, cited `file:line`. If only something new would work, say so, explain why from first principles, and mark it for the user to confirm.

## Write the review for a tired reader

The reader must not have to reconstruct the plan or translate review jargon. Use the same discipline as `write-spec` and `write-plan`.

Apply `references/visual-explanations.md`. Prefer diagrams and real examples over prose. The review must include a diagram of the main failing and corrected flow plus a real-looking worked example. When a fix introduces a mechanism the plan did not have, show that mechanism operating before naming it. Pseudocode is optional and secondary; hide or omit it when the diagram already makes the decision clear.

Open with the verdict and the first concrete example. A "whole review in one picture" summary is optional. Omit it when compressing the findings would turn them into labels that only make sense after the reader understands the review. Never open with unexplained phrases such as "stale-work rejection" or "delivery semantics."

Use a concrete, real-looking example for anything abstract. One example should teach one failure. If two failures interact, split them into two short examples unless their interaction is the point being reviewed. Show only the state changes needed to understand that failure, then state the visible outcome and the fix. A worked example is better than another paragraph of abstraction.

For every finding, show the current and required design. Use a left-versus-right diagram when timing, actors or state matter. Use a compact comparison when the mapping is simple. Prose supports the visual; it is not the default explanation.

| Before: current plan | After: required plan |
|---|---|
| What it does today, in plain words. | The exact replacement, in plain words. |

Put a concrete example above the comparison. Name the actors, the state change and what the user sees. Use **"If unchanged: ..."** only when it adds a clear consequence; it does not replace the example. Put proof below as `file:line`, collapsed or visually secondary when the format allows. The reader should understand the problem without reading the proof.

Use stable finding IDs so the author can reply per item. Group related findings by system boundary, not by the order in which they were discovered. Do not repeat the same root cause once in the spec review and again in the plan review; one finding can name both locations.

### Words and tone

Apply `references/respect-human-attention.md`: judge the work, not whether an agent helped, and show how you would tighten it.

- Calm, direct and decision-ready. Short sentences. One consequence per sentence.
- Plain words before technical terms. Define a necessary term where it first appears.
- Say "the same cycle can post twice," not "the idempotency boundary is incomplete."
- Say "an old run can post after the incident is resolved," not "there is a reconciliation race."
- Say "store which Slack identity owns the message," not "persist delivery identity semantics."
- Never use "consider" or "might want to" for a required change. Say **required**.
- No dense paragraphs, including inside table cells. Use bullets, small tables and diagrams.
- No em dashes. No shorthand that makes the reader infer the missing link.

**Preview before sharing the review.** Apply `references/preview.md`.

Put unresolved choices side by side. Mark one answer recommended and state the cost of the alternative. End with a compact reply template: finding ID, accept/reject/modify, exact before/after text, and counterevidence when rejected.

## Verdict

End with one of:

- **Approved.** Implementation may start.
- **Approved with fixes.** List them. They are not optional.
- **Not approved.** Say what has to change and why it blocks.

**Never end without a verdict.** A review that lists concerns and stops leaves the author guessing whether they may proceed.

## Re-review rounds

When the plan comes back after fixes, show what the revision did: `references/handoff-protocol.md`, "Re-review rounds".

## Bounded

Up to five rounds of back and forth. If five rounds have not converged, the disagreement is about requirements, not the plan, and a human decides.

## Done when

Every issue cites the plan line it is about, each has a fix or a question, and the verdict is one of the three above.
