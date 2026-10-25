# Setup facts

Facts a repo's agent file states once, so no session rediscovers them by failing. Each is a thing a lookup in the code cannot find, or finds only after a failed run.

- **How to run the checks, and what they need first.** The one command that runs the fast tier and the one that runs the full tier, how long each takes, and what must exist before they work (tools on the path, a database and its migrations, a browser). A new machine that learns this from a 2 minute error flood has spent the time the line would have saved.
- **A commit identity set in this worktree, and one the deploy host accepts.** Check `git config user.name` and `user.email` before the first commit. A host that gates deploys on the commit author marks the deploy blocked, and the push then looks like a slow build: one session polled the live URL forty times over about 7 minutes before asking the host, and the fix was to change only the author. Commits already made keep the wrong author in history.
- **Which files are generated, and the command that regenerates them.** Run it in the edit-test loop, not as a step to remember. A committed generated file in a diff is stale until the generator ran, and a screenshot or a test of the source then describes what is not served.
- **The shell and the OS the agents run on, and the habits that bite there.** Name them once: on macOS the BSD `sed -i` needs a suffix argument (`-i ''`) and there is no `timeout` command, and zsh expands an unquoted glob and stops with "no matches found" when it matches nothing. Edit files with a short script in the repo's own interpreter instead of `sed -i`, and quote globs. Across 16 sessions these cost about 130 failed calls, each repeated by every new subagent.

A fact that has a script check belongs in the check, not here.
