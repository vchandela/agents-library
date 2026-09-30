# Visual explanations

Applied by the spec, plan, plan-review and explain-simply skills.

## The rule

Prefer diagrams and concrete examples over explanatory prose. The goal is not to minimise words or draw the smallest possible diagram. The goal is that a tired reader understands the idea without decoding the surrounding text. Teach the mechanism first. Name it second.

Every spec, plan and plan review includes:

- at least one diagram showing the core flow;
- at least one real-looking worked example with concrete values.

When introducing a new mechanism or term, choose the clearest visual form:

- **Sequence diagram:** when several actors interact over time.
- **Flow diagram:** when a condition sends work down different paths.
- **State diagram:** when one thing moves through a lifecycle.
- **Code or pseudocode:** only when exact ordering, checks or stored values remain unclear after the visual.
- **Concrete data example:** when defining a table, request, response or message.
- **Analogy:** when it gives the reader a familiar bridge. Follow it with the real mechanism.

Do not use all of them for every point. Prefer a diagram plus a real example. Add prose only for the facts the visual cannot carry. Plain text is enough when the idea is already obvious.

This is not a "minimum viable diagram" rule. A tiny diagram that still requires the reader to decode a paragraph has failed. Make the visual complete enough to stand on its own.

## Step by step first

When the subject is new to the reader, or done for the first time, explain it as numbered steps in order (why it exists, the pieces, one run, where it breaks), each with plain words, one small picture, a real example and a one-line takeaway. System names come at the end of each step. An overview of boxes and arrows goes after the steps as a recap, never in their place.

## Before using a term

First say what the thing is and show one instance. Then give it a name.

Bad:

> Create a durable message intent and reconcile it on retry.

Better:

> Before posting, store one row that says: `INC-712 / rollback-started / not sent`. After posting, add the Slack timestamp and mark it sent. We call this row a send record.

Never leave a noun such as version, intent, generation, reconciliation, admission or delivery policy standing on its own. Show what value it holds, who changes it and which decision reads it.

## Diagram quality

- Every box is a real actor, store or state.
- Every arrow is a real call, write or state change, labelled with what moves.
- Show failure at the exact step where it happens.
- Show the corrected path beside or directly after the failing path.
- One example teaches one failure. Split unrelated failures.
- A diagram is not a compressed list of unexplained labels.

## Code quality

Pseudocode is optional and secondary. Do not add it when the diagram and example already explain the mechanism. When it is useful, keep it small and hide or place it after the primary visual. Include only the fields and branches needed to explain the decision. Mark pseudocode as pseudocode. If a call or API does not exist yet, say so; do not make invented code look real.

## Progressive detail

Keep the main visual and example visible. Collapse or move supporting proof, code and edge-case detail below them. The first screen should explain the idea, not display every piece of evidence.

## Check

Could a tired reader explain the mechanism back without borrowing the document's jargon? If not, the visual or example has not done its job.
