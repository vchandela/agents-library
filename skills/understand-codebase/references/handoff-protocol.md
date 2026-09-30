# Handoff protocol

Who proposes, and who judges. The pipeline skills reference this.

## The rule

**The agent that produced the work does not review the work.**

An agent reviewing its own plan re-reads its own reasoning and finds it convincing, because it is the reasoning it just chose. The bias is structural, not a matter of effort or prompting.

## What separation means

| Step | Runs where |
|---|---|
| Write the spec | any model |
| Write the plan | any model |
| **Review the plan** | **fresh session, different model family, or a stronger model in the same family** |
| Implement | any model, after the review approves |
| **Review the code** | **fresh session, and not the one that wrote the code** |

A fresh session is the minimum. A different model family is better, because two models from one family share failure modes.

## Gates

- **Implementation does not start until the plan review approves it.** Not "mostly fine". Approved.
- Review rounds are bounded. Up to five passes of back and forth, then a human decides. If five rounds have not converged, the disagreement is about the requirements, not the plan.
- A human reads the plan before implementation begins. The agents check each other; they do not replace the person who knows what is wanted.

## Why bounded

Unbounded review finds infinite issues, because any plan can be criticised forever. Five rounds is enough to catch what matters and short enough to finish.
