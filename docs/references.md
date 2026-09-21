# What was taken, and what was refused

Where each idea came from, so adopting the next harness is a decision rather than a habit.

## Taken

| From | Idea |
|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | A description says when to read, never what it does. Found by testing, not taste. |
| obra/superpowers | Rationalisation tables: write down the excuse, then the rebuttal. |
| obra/superpowers | Match the form to the failure. A rule broken under pressure needs a prohibition, not guidance. |
| obra/superpowers | No skill without a failing baseline first. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | User invoked against model invoked, stated per skill. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Process, not prose. Steps, checkpoints, exit criteria. |
| addyosmani/agent-skills | Evidence requirements. "Seems right" is never sufficient. |
| [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) | Negative triggers in the description. |
| mgechev/skills-best-practices | The three step validation loop, which replaced a compliance harness. |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | Distribution. `npx skills add` already handles 80+ agents. |
| [anthropics/skills](https://github.com/anthropics/skills) | Minimal frontmatter. Two fields. |

## Refused

| From | Refused | Why |
|---|---|---|
| obra/superpowers | Nine harness plugin directories | Ship the one in use. Add another when another is actually used. |
| ECC | 286 skills, 68 agents, 94 commands | A catalogue to maintain. Sixteen is the working set. |
| ECC | Auto extracted "learned" skills from transcripts | Unreviewed content writing itself is the thing a curated repo exists to prevent. |
| ECC | Per session cost tracking, desktop notifications, MCP health checks | Agency scale problems. |
| ECC | The plugin bootstrap resolver | A 900 character inline resolver for marketplace installs. Not needed for a repo you clone. |
| everyone | A build step that compiles skills from fragments | Five of five hand write. Ten lines of duplication does not justify a generator and a drift test. |
| everyone | An install script | `npx skills add` exists and does symlinks properly. |
| me | A compliance measurement harness | The three step validation above gets most of the value with none of the machinery. Revisit if a skill keeps being ignored in practice. |

## Own

Not found in any of the repos read.

- **Separation of proposer and critic.** All five assume one agent plans, implements and reviews. The pipeline here hands off instead, with bounded rounds and a gate before implementation.
