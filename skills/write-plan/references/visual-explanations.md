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

## Pick the form by what the reader must understand

Decide what the reader must understand first, then the picture. If a three-column table says the same thing, use the table. A one-box diagram is a sentence.

| The reader must understand | Draw |
|---|---|
| Why two similar requests ended differently | The same ordered checks as two traces side by side. Each check is PASS, FAIL, SKIPPED (bypassed on purpose) or NOT REACHED (an earlier check stopped it). Mark the first divergence. |
| What a change did to a system | Before, Changes, After. Two snapshots on the same grid, with unchanged boxes in the same place, and a short ledger between them, one line per change: ADDED, REMOVED, CHANGED (old to new), MOVED, REWIRED. |
| Why work waits | Sources fanning into one queue with its count, the capacity as a number with units (8 per hour), and both outcomes (served, deferred). |
| How one thing moves through phases, waits, retries and ends | A phase rail left to right, a separate band for waits and retries, and a separate band for endings, with cancelled and failed as different boxes. |
| What layered defences leave behind | Layers in order. Each says what it stops and what gets past. End with the risk that remains. Never imply the last layer makes risk zero. |
| Who does what across a handoff | One lane per owner. A step sits in exactly one lane. The handoffs are the arrows that matter. |
| Events over time | A timeline with honest spacing: unequal gaps are drawn unequal. |

This is not a "minimum viable diagram" rule. A tiny diagram that still requires the reader to decode a paragraph has failed. Make the visual complete enough to stand on its own.

## Budget

- At most 9 boxes and 12 arrows per diagram. Highlight 1 or 2 elements. If you want to highlight 4, you have not decided what matters.
- Sequence: at most 5 participants and one branch frame (alt with at most 2 regions, or opt, or loop), never nested. Swimlane: at most 5 lanes. State: more transitions than twice the states means two machines.
- Over budget: split into an overview and a detail. Never drop a real arrow to fit.
- Before drawing, say in one line which form, and what the budget will push into a second diagram.

## Remove test

Before publishing, ask of every box: can it go, or merge with one it always travels with? Ask of every arrow: does the layout already show it? Remove those. The plain-words note under a label is not up for removal; it is how a tired reader reads the arrow.

## Steps first, or the map first: it depends on the reader

- **A reader new to the subject** (learning how something works): numbered steps in order (why it exists, the pieces, one run, where it breaks), each with plain words, one small picture, a real example and a one-line takeaway. System names come at the end of each step. An overview of boxes and arrows goes after the steps as a recap, never in their place.
- **A reader who knows the domain and is judging a design** (a spec, a plan, a tech doc, a system page): the problem in a few lines, then one map of four to seven big boxes, then a section per box, layer by layer.

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
- Arrows bend at right angles, never diagonally. Two arrows never share a line or a point on a box. An arrow does not pass behind a box that is not one of its ends.
- An arrow's label sits beside the line with a visible gap, never on top of it.
- The legend is a strip below the diagram, never inside it.
- Boxes differ by kind (store, service, person, external). Identical boxes for everything erase the hierarchy.
- The diagram's title and description say what it shows ("Requests from three teams queue at one reviewer"), not its geometry ("a box with three boxes above it").

## Grammar

- Sequence: time flows down, and no arrow points up. A reply is dashed (`-->>` in Mermaid). A fire-and-forget message has an open head (`-)`). A branch goes in a labelled frame (`alt`, `opt`, `loop`) with guards such as `[token valid]` and `[else]`. Never two loose clusters of arrows.
- State: label every transition `event [guard] / action`. A transition from any state is one note (`* to Error on timeout`), not an arrow from every box.
- Flowchart: shape carries the type (rounded for start and end, box for a step, diamond for a decision). A diamond has at most 3 exits, each labelled.
- Colour never carries meaning alone. Pair it with a word, a dash pattern or a shape, so the diagram survives print, dark mode and colour blindness.

## Code quality

Pseudocode is optional and secondary. Do not add it when the diagram and example already explain the mechanism. When it is useful, keep it small and hide or place it after the primary visual. Include only the fields and branches needed to explain the decision. Mark pseudocode as pseudocode. If a call or API does not exist yet, say so; do not make invented code look real.

## Progressive detail

Keep the main visual and example visible. Collapse or move supporting proof, code and edge-case detail below them. The first screen should explain the idea, not display every piece of evidence.

## Check

Could a tired reader explain the mechanism back without borrowing the document's jargon? If not, the visual or example has not done its job.

## Notion pages and docs others read

The same rule applies hardest to a Notion page or a doc for the team, whether a skill or a person writes it: diagrams over text.

- **Draw the flow, don't narrate it.** A process that crosses repos, people or systems (who opens which PR, what approves it, what applies it) is an Excalidraw diagram, or a Mermaid flow or sequence diagram where the page renders one. Draw it with the Excalidraw tool and hand over the file; the author exports it into Notion.
- **Visible text is one-line points.** Supporting detail goes in a toggle whose summary is the one-line point, for example a toggle "However, this is for alerts only." that hides which folders and workflows that covers.
- **Keep everything, show less.** Collapsing is not cutting: every fact stays, under the toggle that owns it.

Failure this prevents: a one-pager on syncing dashboards through another team's repo explained the PR flow in five numbered paragraphs. The reader asked for the flow as an Excalidraw diagram and the details collapsed into toggles, "so we cut down on text", and for every doc and skill to work that way.
