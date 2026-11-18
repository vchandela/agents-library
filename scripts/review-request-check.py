#!/usr/bin/env python3
"""Two hooks in one script, because both guard what a ship flow sends.

1. Review request (PreToolUse on SendMessage): refuse a ship review request that has no
   principles check.

   A review request is a message whose first line starts with "[ship" and says
   "review request". It passes only when it has a "Principles check" section that
   cites at least one file:line, the rule in references/tech-index.md ("A review
   request -> carries a Principles check"). Every other message passes untouched.

   Exit 2 blocks the send and shows the reason to the agent, as the Claude Code
   hooks docs describe for PreToolUse.

2. Hand-off gate (`hand_off_gate`, on SendMessage and on Stop): log, and after the
   log-only week refuse, a hand-off whose PR is not ready.

   A hand-off is what reaches the user: a final reply that links a PR (Stop), or a message
   to the coordinator, the session that passes work on to the user, that says the work is
   ready for them. The author sends the coordinator one [cos] line at every stage change
   (ship SKILL.md, "With a coordinator"); only a line whose verdict is "approve", or whose
   "needs user" asks for a review, is a hand-off. A "changes" or "blocked" line is a status
   report, sent while CI is red on purpose, and passes untouched. A review request goes out
   before CI and threads are clear, by design, so it is never gated.

   A PR is not ready when CI is failing or still running, a person requested changes, or any
   review thread is unresolved, whoever opened it. A PR with no checks has nothing red or
   running, so CI does not block it. One `gh api graphql` call reads every linked PR.

   The coordinator writes its address and its name to ~/.claude/cos/coordinator, two lines.
   A send is checked only when its `to` matches one of them. When the address has no live
   socket in CC_SOCKS_DIR the file is stale: the send is logged "unchecked" and not gated.

   While MODE is "log" the gate only appends a line per PR to ~/.claude/logs/handoff-gate.jsonl.
   After the log is read and every "not ready" line is checked by hand against its PR, one line
   changes MODE to "refuse": then a not-ready or unchecked send to the coordinator exits 2.
   The final-reply check stays a log, because Stop cannot undo a reply the user already reads.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_REQUEST = re.compile(r"^\[ship [^\]]*\].*review request", re.IGNORECASE)
_SECTION = re.compile(r"principles check", re.IGNORECASE)
# A file:line citation such as repos.py:13502 or postgres.py:1462, 1499.
_CITATION = re.compile(r"[\w./-]+\.\w+:\d+")


MODE = "log"  # "log" until the log is read on 25 Nov, then "refuse": see the module docstring
GH_TIMEOUT_S = 5  # 19 calls of this query on 16 Nov took 0.83 to 2.46 s, so 5 s is twice the slowest
LOG_LINE_MAX = 4000  # one append under 4 KB is written whole, so sessions writing at once never mix lines

_PR_LINK = re.compile(r"github\.com/([\w.-]+)/([\w.-]+)/pull/(\d+)")
_PR_HEADS = re.compile(r"(?<![\w./-])([\w.-]+)/([\w.-]+)#(\d+)")
_COS_LINE = re.compile(r"^\[cos\][^:\n]*\bround \S+: *(\w+)(.*)$", re.IGNORECASE)
_NEEDS_REVIEW = re.compile(r"needs user: *(?!none\b)[^\n]*\breview", re.IGNORECASE)
_CHECK_STATES = {"SUCCESS": [], "FAILURE": ["CI FAILURE"], "ERROR": ["CI ERROR"],
                 "PENDING": ["CI PENDING"], "EXPECTED": ["CI EXPECTED"]}

QUERY = """pullRequest(number: %d) { reviewDecision
  reviewThreads(first: 100) { pageInfo { hasNextPage } nodes { isResolved } }
  commits(last: 1) { nodes { commit { statusCheckRollup { state } } } } }"""


def review_request_check(event: dict) -> int:
    message = str((event.get("tool_input") or {}).get("message") or "")
    first_line = message.strip().splitlines()[0] if message.strip() else ""
    if not _REQUEST.search(first_line):
        return 0
    found = _SECTION.search(message)
    if found and _CITATION.search(message[found.end():]):
        return 0
    print(
        "Blocked: a ship review request needs a 'Principles check' section with one "
        "line per rule from references/tech-index.md that the change touches, each "
        "with its verdict and a file:line citation. Add it and send again.",
        file=sys.stderr,
    )
    return 2


def is_ready_line(message: str) -> bool:
    """True for a [cos] line that says the work is ready for the user."""
    match = _COS_LINE.match(message.strip().splitlines()[0]) if message.strip() else None
    return bool(match) and (match.group(1).lower() == "approve" or bool(_NEEDS_REVIEW.search(message)))


def pull_requests(text: str) -> list[tuple[str, str, int]]:
    found = [(o, r, int(n)) for pattern in (_PR_LINK, _PR_HEADS) for o, r, n in pattern.findall(text)]
    return list(dict.fromkeys(found))


def fetch(prs: list[tuple[str, str, int]]) -> dict:
    """One gh call for every PR. Raises on a gh failure or a timeout."""
    aliases = " ".join(f'p{i}: repository(owner: "{o}", name: "{r}") {{ {QUERY % n} }}' for i, (o, r, n) in enumerate(prs))
    done = subprocess.run(["gh", "api", "graphql", "-f", f"query=query {{ {aliases} }}"],
                          capture_output=True, text=True, timeout=GH_TIMEOUT_S, check=False)
    if done.returncode:
        raise RuntimeError(done.stderr.strip() or f"gh exited {done.returncode}")
    return json.loads(done.stdout)["data"]


def judge(answer: dict | None) -> tuple[str, list[str]]:
    """("ready" | "not ready" | "unchecked", the reasons) for one PR's answer."""
    pull = (answer or {}).get("pullRequest")
    if not pull:
        return "unchecked", ["gh found no such PR"]
    threads = pull["reviewThreads"]
    if threads["pageInfo"]["hasNextPage"]:
        return "unchecked", ["more than 100 review threads"]
    rollup = pull["commits"]["nodes"][0]["commit"]["statusCheckRollup"]
    reasons = list(_CHECK_STATES.get(rollup["state"], [f"CI {rollup['state']}"])) if rollup else []
    if pull["reviewDecision"] == "CHANGES_REQUESTED":
        reasons.append("changes requested")
    open_threads = sum(1 for n in threads["nodes"] if not n["isResolved"])
    if open_threads:
        reasons.append(f"{open_threads} unresolved review thread{'s' * (open_threads > 1)}")
    return ("not ready" if reasons else "ready"), reasons


def append_log(entry: dict) -> None:
    path = Path.home() / ".claude" / "logs" / "handoff-gate.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), **entry})
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, (line[:LOG_LINE_MAX] + "\n").encode())
    finally:
        os.close(fd)


def coordinator() -> tuple[str, str]:
    """The address and the name on the two lines of ~/.claude/cos/coordinator, or empty strings."""
    try:
        address, name, *_ = (Path.home() / ".claude" / "cos" / "coordinator").read_text().splitlines() + ["", ""]
    except OSError:
        return "", ""
    return address.strip(), name.strip()


def hand_off_gate(event: dict) -> int:
    """Log whether each PR in a hand-off is ready. Returns 2 only in "refuse" mode, on a send to the coordinator."""
    entry = {"session_id": event.get("session_id")}
    if event.get("tool_name") == "SendMessage":
        to = str((event.get("tool_input") or {}).get("to") or "")
        text = str((event.get("tool_input") or {}).get("message") or "")
        address, name = coordinator()
        if to not in (address, name) or not to or not is_ready_line(text):
            return 0
        socket_file = Path(os.environ.get("CC_SOCKS_DIR", "/tmp/cc-socks")) / Path(address.removeprefix("uds:")).name
        if not socket_file.is_socket():
            append_log({**entry, "event": "SendMessage", "to": to, "pr": None, "verdict": "unchecked",
                        "reasons": [f"coordinator address {address} has no live socket, so the file is stale"]})
            return 0
        entry |= {"event": "SendMessage", "to": to}
    elif event.get("hook_event_name") == "Stop":
        text = str(event.get("last_assistant_message") or "")
        entry |= {"event": "Stop"}
    else:
        return 0
    prs = pull_requests(text)
    if not prs:
        return 0
    try:
        answers = fetch(prs)
        results = [judge(answers.get(f"p{i}")) for i in range(len(prs))]
    except (subprocess.TimeoutExpired, RuntimeError, OSError, ValueError, KeyError, IndexError, TypeError) as error:
        results = [("unchecked", [f"{type(error).__name__}: {error}"[:200]])] * len(prs)
    for (owner, repo, number), (verdict, reasons) in zip(prs, results):
        append_log({**entry, "pr": f"{owner}/{repo}#{number}", "verdict": verdict, "reasons": reasons[:10]})
    bad = [f"{o}/{r}#{n}: {', '.join(reasons)}" for (o, r, n), (verdict, reasons) in zip(prs, results) if verdict != "ready"]
    if bad and MODE == "refuse" and entry["event"] == "SendMessage":
        print("Blocked: this hand-off names a PR that is not ready (" + "; ".join(bad) +
              "). Fix it, answer every review thread, then send again.", file=sys.stderr)
        return 2
    return 0


def main() -> int:
    event = json.load(sys.stdin)
    if event.get("tool_name") == "SendMessage" and (blocked := review_request_check(event)):
        return blocked
    return hand_off_gate(event)


if __name__ == "__main__":
    sys.exit(main())
