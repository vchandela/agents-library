# Explaining

How to make a reader understand something new: a system, a concept, a decision. Applied by the explain-simply and understand-codebase skills, and by anything that teaches. `writing-voice.md` covers the words; this file covers the order and the evidence.

## Build from the ground up

Each idea rests on the one before it.

- Define each term where it first appears, in plain words, before anything relies on it. Show one instance first, then give it a name.
- Never open with a summary that uses words the reader has not met yet. It reads as noise and has to be decoded after the fact.
- A short glossary at the top is fine, because every entry defines itself. A recap goes at the END, once every word in it means something.
- The first screen explains the idea. Evidence comes after.

## Show, do not characterise

- **Every claim carries its example.** "A merge takes up to two hours to deploy" is a claim. The cron line `13 */2 * * *` beside it is the explanation. Quote the real code or config, small enough to read in place, with its path.
- **Decisions are comparisons, drawn side by side.** A and B next to each other, as a diagram or a row-by-row table, with the part that differs made obvious. One diagram per decision beats one diagram for the whole page. A paragraph that describes one option and then mentions another is not a comparison.
- **Every comparison ends in a verdict.** Say which wins here, and why. Name where the loser wins.
- **Read what a metric counts before quoting it.** A dashboard field's name is not its definition: open the query behind it, then say in the sentence what it includes and excludes. Failure this prevents: "the pool built 900 envs and served 4 instantly" went to a colleague, who said the numbers were wrong. `deployed` also counted runs' own deploys, and `instant` counted people only, hiding 13 instant hand-outs to automated runs.
- **Numbers show their working.** A cost is size × unit price × hours, with where the price came from, and says "estimate" when it is not the bill.
- **"When to use which" is a table**: the situation, the choice, and a real example from the system being explained.

## Answer questions where they arise

- When the reader asked specific questions, quote each one in a small box at the top of the section that answers it, so they can find their answers.
- A judgement about whether a design is healthy goes in a box directly under the part that describes it, titled "Is this healthy?". Never in a section at the end.
- A risk, cost or gap the reader will ask about next gets the same inline box.

## Words

- Plain words, short sentences, active voice. No flourish or metaphor where a plain noun works: "every step goes through this one call", not "every step crosses the one teal edge".
- No em dashes. Use a comma, a colon, a full stop or brackets.
- **One name per concept, everywhere.** The same word in the prose, the diagrams, the example data and the table or file names. A reader who met "diary" in the text and `cases` as the table asked which was which.
- **Real names in brackets.** Any casual or made-up word carries the real thing: "robot (ContextCollectionWorkflow)", or for something new, "the learner (proposed name `KbLearnerWorkflow`)". Use the system's own name, not a screen label ("Areas" was the UI screen, not the engine).
- **Heavy words get a plain meaning in brackets** the first time: "span (one timed step inside a request)". Prefer the plain phrase outright where one exists: "looks like the cause, isn't" over "pitfall".
- No hand waving. If you cannot explain how it works, say that you cannot.
- No fluff, no filler, no throat clearing.
- No skipping the hard part. The hard part is usually why they asked.
- When a reader says a section is too verbose, explain it more simply. Never delete it.

## Devices that landed

Each of these was tried on a real reader and worked where prose had not. Pick the one that fits the concept; none is mandatory.

- **When the reader will explain it on to someone else, give them what they need to defend it.** For each issue or fix they will present: the story in one line, the flow it sits in, one real timestamped example with a link, what it fixes and what it does not, and the likely cross-questions with short answers backed by evidence. A reader asked for exactly this so they could answer "any cross-questioning" from the people reviewing the work; a bare finding left them unable to.
- **Name each tool's job before the flow uses it.** When a mechanism spans several tools (a CI service, a build tool, a step runner, an in-house worker), give a "who does what" table first: what each is, where it runs, what it does in this flow, then one trace through all of them. A glossary line per tool is not enough when they hand work to each other. Failure this prevents: a CI page used the CI service, the build tool, a step runner and an in-house build worker as known words, and the reader had to ask what each one was.
- **For a system with many parts, give the cast, then walk one real item end to end.** List every piece once (what it is, where it lives, who writes and reads it), then follow one real ticket, request or job through all of them, naming what it leaves behind at each stop. Answer the reader's open questions at the stop where they arise. Failure this prevents: a support-agent design explained piece by piece (pages, records, logs, evals) drew a dozen "how does X relate to Y?" questions; one ticket walked from arrival to a graded, merged edit answered them.
- **Compare capabilities in one table.** Things side by side as columns, one row per capability, ✅ or ❌ with a short qualifier and the evidence (`file:line` or the config key) in the cell. A reader called this "lovely" for three workflows (which one reads, posts, writes code, opens a PR), with a small picture of how they connect above it.
- **For "what happens when...", use a named scenario and a row-by-row table.** Set one concrete scene with real-looking names ("you ask for branch X; the pool has p3e7a1 and p9c2d0, both on master"). Put the options as columns and the moments as rows ("building X", "X succeeds", "X fails", "only one left"), each cell a concrete outcome, then end with a two-line trade-off. A reader said this landed "in one go" after several prose explanations of the same thing had not.
- **Explain a job by its inputs, then give its laptop equivalent.** For anything that runs (a CI job, a script, a teardown), name the two or three things it needs and what each one decides, then say "it's the same as running `<command>` on your laptop", then say in one sentence what goes wrong today. Example that landed first time: "A teardown job needs two things: a copy of the app's code, because the delete script lives there (any recent copy works, and master is always there), and the name of the environment to delete, given separately as `BUILD_ID=a4c842`. It's the same as checking out master and running `BUILD_ID=a4c842 make teardown`. Today the job tries to get its copy from the run's branch, which is deleted once the PR merges, so it stops before it starts." Before that, "the id alone can't replace the branch because the job checks out code for the script" was marked as needing easier words.
- **Pick the device per concept, pragmatically.** A bare table of rules (precedence orders, naming schemes, which values a runner forwards) often goes over a reader's head. No single fix is mandatory: choose whatever makes this concept land with the least translation. Options: facts in order followed by a timestamped run of the real system (a named branch, a build number, the id it gets, the URL it hits, what breaks); a short analogy when the reader knows the analogue well and it needs no vocabulary of its own; a diagram; an A vs B table. Reject an analogy that grows its own cast (hotel rooms, desks, couriers) the reader must map back. Failures this prevents: a build-id table the reader said "went over my head", then a hotel metaphor for it that he called "too convoluted".
