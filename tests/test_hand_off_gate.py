"""The hand-off gate in scripts/review-request-check.py, run the way Claude Code runs a hook.

The gate logs a "not ready" line when work that reaches the user has red or running CI, a change
request, or an unresolved review thread. Every test runs the real script with the hook input as
JSON on stdin, HOME and CC_SOCKS_DIR in temporary folders, and a stand-in `gh` first on PATH
(tests/fixtures/bin/gh) that prints an answer shaped like the real GraphQL one: the real query,
run on a real PR, returns reviewDecision, reviewThreads.nodes[].isResolved and
commits.nodes[0].commit.statusCheckRollup.state (null when a PR has no checks).
All names are placeholders.
"""

import contextlib
import importlib.util
import io
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "review-request-check.py"
FAKE_GH = ROOT / "tests" / "fixtures" / "bin"
PR7, PR8 = "https://github.com/acme/shop/pull/7", "https://github.com/acme/api/pull/8"
GOOD_REQUEST = "[ship topic] plan v1 round 1: review request\nPrinciples check:\n- reuse: scripts/lint-skills.py:27 holds."


def pr(ci="SUCCESS", unresolved=0, decision=None):
    rollup = {"state": ci} if ci else None
    return {"pullRequest": {"reviewDecision": decision,
                            "reviewThreads": {"pageInfo": {"hasNextPage": False},
                                              "nodes": [{"isResolved": False}] * unresolved + [{"isResolved": True}]},
                            "commits": {"nodes": [{"commit": {"statusCheckRollup": rollup}}]}}}


def cos(verdict, *links, needs="none"):
    return f"[cos] topic pr v1 round 2: {verdict}; heads {' '.join(links)}; needs user: {needs}"


class Rig:
    """A temporary HOME, socket folder and gh answer for one gate run."""

    def __init__(self, answers=None, coordinator=("uds:{socks}/42.sock", "admin"), live=True):
        self.tmp = tempfile.TemporaryDirectory()
        self.socks = tempfile.mkdtemp(dir="/tmp")  # a short path: Unix socket paths are limited to about 100 characters
        self.home = Path(self.tmp.name)
        self.keep = []
        if coordinator:
            (self.home / ".claude" / "cos").mkdir(parents=True)
            address, name = coordinator
            (self.home / ".claude" / "cos" / "coordinator").write_text(address.format(socks=self.socks) + "\n" + name + "\n")
        if live:
            server = socket.socket(socket.AF_UNIX)
            server.bind(f"{self.socks}/42.sock")
            self.keep.append(server)
        answer = {f"p{i}": a for i, a in enumerate(answers or [])}
        self.answer = self.home / "answer.json"
        self.answer.write_text(json.dumps({"data": answer}))
        self.calls = self.home / "calls.txt"
        self.calls.touch()

    def env(self, **extra):
        return {"HOME": str(self.home), "CC_SOCKS_DIR": self.socks, "PATH": f"{FAKE_GH}:/usr/bin:/bin",
                "GH_ANSWER": str(self.answer), "GH_CALLS": str(self.calls), **extra}

    def run(self, event, **extra):
        started = time.monotonic()
        done = subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(event), text=True,
                              capture_output=True, env=self.env(**extra))
        self.seconds = time.monotonic() - started
        return done.returncode, done.stderr

    def log(self):
        path = self.home / ".claude" / "logs" / "handoff-gate.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def gh_calls(self):
        return len(self.calls.read_text().splitlines())

    def close(self):
        for server in self.keep:
            server.close()
        self.tmp.cleanup()


def send(to, message):
    return {"hook_event_name": "PreToolUse", "tool_name": "SendMessage", "session_id": "s1",
            "tool_input": {"to": to, "message": message}}


def stop(text, active=False):
    return {"hook_event_name": "Stop", "session_id": "s1", "last_assistant_message": text, "stop_hook_active": active}


class GateTest(unittest.TestCase):
    def rig(self, *args, **kw):
        rig = Rig(*args, **kw)
        self.addCleanup(rig.close)
        return rig


class WhatIsAHandOff(GateTest):
    def test_a_review_request_to_the_reviewer_with_a_pending_link_passes_untouched(self):
        rig = self.rig([pr("PENDING")])
        self.assertEqual(rig.run(send("review ag-k8s", f"{GOOD_REQUEST}\n{PR7}"))[0], 0)
        self.assertEqual(rig.log(), [])
        self.assertEqual(rig.gh_calls(), 0)

    def test_a_status_line_to_the_coordinator_while_ci_is_red_passes_untouched(self):
        rig = self.rig([pr("FAILURE")])
        self.assertEqual(rig.run(send("admin", cos("changes", PR7)))[0], 0)
        self.assertEqual(rig.log(), [])

    def test_an_approve_line_to_the_coordinator_is_checked_by_name_and_by_address(self):
        for to in ("admin", "uds:{socks}/42.sock"):
            with self.subTest(to=to):
                rig = self.rig([pr("PENDING")])
                code, _ = rig.run(send(to.format(socks=rig.socks), cos("approve", PR7)))
                self.assertEqual(code, 0)
                self.assertEqual([(e["pr"], e["verdict"]) for e in rig.log()], [("acme/shop#7", "not ready")])

    def test_a_line_that_asks_the_user_to_review_counts_as_ready_for_them(self):
        rig = self.rig([pr("PENDING")])
        rig.run(send("admin", cos("changes", PR7, needs="review the PRs")))
        self.assertEqual([e["verdict"] for e in rig.log()], ["not ready"])

    def test_the_pr_is_found_in_the_heads_form_as_well_as_a_link(self):
        rig = self.rig([pr("PENDING")])
        rig.run(send("admin", cos("approve", "acme/shop#7@abc1234")))
        self.assertEqual([e["pr"] for e in rig.log()], ["acme/shop#7"])

    def test_a_send_to_anyone_else_passes_untouched(self):
        rig = self.rig([pr("PENDING")])
        rig.run(send("someone-else", cos("approve", PR7)))
        self.assertEqual(rig.log(), [])


class WhatMakesAPrNotReady(GateTest):
    def verdicts(self, *answers, message=None):
        rig = self.rig(list(answers))
        links = [PR7, PR8][:len(answers)]
        rig.run(send("admin", message or cos("approve", *links)))
        return [(e["pr"], e["verdict"], e.get("reasons")) for e in rig.log()]

    def test_green_ci_with_no_open_thread_is_ready(self):
        self.assertEqual(self.verdicts(pr("SUCCESS")), [("acme/shop#7", "ready", [])])

    def test_ci_that_is_failing_or_still_running_is_not_ready(self):
        for state in ("FAILURE", "ERROR", "PENDING"):
            with self.subTest(state=state):
                self.assertEqual(self.verdicts(pr(state)), [("acme/shop#7", "not ready", [f"CI {state}"])])

    def test_a_pr_with_no_checks_at_all_is_ready_because_nothing_is_red_or_running(self):
        self.assertEqual(self.verdicts(pr(None)), [("acme/shop#7", "ready", [])])

    def test_any_unresolved_thread_makes_it_not_ready_whoever_wrote_it(self):
        self.assertEqual(self.verdicts(pr("SUCCESS", unresolved=2)),
                         [("acme/shop#7", "not ready", ["2 unresolved review threads"])])

    def test_a_change_request_makes_it_not_ready(self):
        self.assertEqual(self.verdicts(pr("SUCCESS", decision="CHANGES_REQUESTED")),
                         [("acme/shop#7", "not ready", ["changes requested"])])

    def test_two_links_in_two_repos_make_one_call_and_one_line_each_and_name_only_the_one_not_ready(self):
        rig = self.rig([pr("SUCCESS"), pr("FAILURE")])
        rig.run(send("admin", cos("approve", PR7, PR8)))
        self.assertEqual(rig.gh_calls(), 1)
        self.assertEqual([(e["pr"], e["verdict"]) for e in rig.log()],
                         [("acme/shop#7", "ready"), ("acme/api#8", "not ready")])

    def test_one_prs_open_thread_does_not_leak_into_the_next_green_pr(self):
        """Found by running the gate on two real PRs: both were green, only the first had an open thread."""
        rig = self.rig([pr("SUCCESS", unresolved=1), pr("SUCCESS")])
        rig.run(send("admin", cos("approve", PR7, PR8)))
        self.assertEqual([(e["pr"], e["verdict"], e["reasons"]) for e in rig.log()],
                         [("acme/shop#7", "not ready", ["1 unresolved review thread"]), ("acme/api#8", "ready", [])])


class TheFinalReply(GateTest):
    def test_a_final_reply_with_a_red_link_is_logged_and_never_refused(self):
        rig = self.rig([pr("FAILURE")])
        code, _ = rig.run(stop(f"Done. {PR7}"))
        self.assertEqual(code, 0)
        self.assertEqual([(e["event"], e["verdict"]) for e in rig.log()], [("Stop", "not ready")])

    def test_a_stop_event_that_is_already_continuing_still_logs_once_and_exits_zero(self):
        rig = self.rig([pr("FAILURE")])
        self.assertEqual(rig.run(stop(f"Done. {PR7}", active=True))[0], 0)
        self.assertEqual(len(rig.log()), 1)

    def test_a_final_reply_with_no_link_logs_nothing(self):
        rig = self.rig([])
        rig.run(stop("All done, nothing to review."))
        self.assertEqual(rig.log(), [])


class WhenItCannotCheck(GateTest):
    def test_a_stale_coordinator_file_logs_unchecked_and_asks_gh_nothing(self):
        rig = self.rig([pr("FAILURE")], live=False)
        self.assertEqual(rig.run(send("admin", cos("approve", PR7)))[0], 0)
        self.assertEqual([e["verdict"] for e in rig.log()], ["unchecked"])
        self.assertIn("socket", rig.log()[0]["reasons"][0])
        self.assertEqual(rig.gh_calls(), 0)

    def test_a_stale_file_does_not_stop_a_review_request_to_the_reviewer(self):
        rig = self.rig([pr("FAILURE")], live=False)
        self.assertEqual(rig.run(send("review ag-k8s", f"{GOOD_REQUEST}\n{PR7}"))[0], 0)
        self.assertEqual(rig.log(), [])

    def test_a_gh_call_that_takes_too_long_logs_unchecked_within_six_seconds(self):
        rig = self.rig([pr("SUCCESS")])
        code, _ = rig.run(send("admin", cos("approve", PR7)), GH_SLEEP="10")
        self.assertEqual(code, 0)
        self.assertLess(rig.seconds, 6)
        self.assertEqual([e["verdict"] for e in rig.log()], ["unchecked"])

    def test_a_gh_call_that_fails_logs_unchecked_with_the_error(self):
        rig = self.rig([pr("SUCCESS")])
        rig.run(send("admin", cos("approve", PR7)), GH_FAIL="1")
        self.assertEqual([e["verdict"] for e in rig.log()], ["unchecked"])
        self.assertIn("Bad credentials", rig.log()[0]["reasons"][0])


class TodaysReviewRequestCheck(GateTest):
    """The check this script already did, unchanged."""

    def test_a_ship_review_request_with_no_principles_check_is_refused(self):
        rig = self.rig([])
        code, err = rig.run(send("review ag-k8s", "[ship topic] plan v1 round 1: review request\nplease look"))
        self.assertEqual(code, 2)
        self.assertIn("Principles check", err)

    def test_one_with_a_principles_check_and_a_citation_passes(self):
        self.assertEqual(self.rig([]).run(send("review ag-k8s", GOOD_REQUEST))[0], 0)

    def test_any_other_message_passes(self):
        self.assertEqual(self.rig([]).run(send("anyone", "hello"))[0], 0)


class TheLog(GateTest):
    def test_two_processes_appending_200_lines_each_leave_400_whole_json_lines(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        code = ("import importlib.util, sys\n"
                f"s = importlib.util.spec_from_file_location('gate', {str(SCRIPT)!r})\n"
                "m = importlib.util.module_from_spec(s); s.loader.exec_module(m)\n"
                "for i in range(200): m.append_log({'pr': 'acme/shop#7', 'verdict': 'ready', 'i': i, 'who': sys.argv[1], 'pad': 'x' * 300})\n")
        procs = [subprocess.Popen([sys.executable, "-c", code, who], env={"HOME": tmp.name, "PATH": "/usr/bin:/bin"}) for who in "ab"]
        for proc in procs:
            self.assertEqual(proc.wait(), 0)
        lines = (Path(tmp.name) / ".claude" / "logs" / "handoff-gate.jsonl").read_text().splitlines()
        self.assertEqual(len(lines), 400)
        self.assertEqual(sum(1 for line in lines if json.loads(line)["who"] == "a"), 200)


class WhenTheLogIsFlippedToRefuse(GateTest):
    """The one-line change after 25 Nov: the gate refuses a not-ready send to the coordinator."""

    def gate(self):
        spec = importlib.util.spec_from_file_location("review_request_check", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.MODE = "refuse"
        return module

    def run_in_process(self, rig, event):
        with mock.patch.dict(os.environ, rig.env()), mock.patch("pathlib.Path.home", return_value=rig.home), \
                contextlib.redirect_stderr(io.StringIO()):
            return self.gate().hand_off_gate(event)

    def test_a_not_ready_approve_line_is_refused(self):
        rig = self.rig([pr("PENDING")])
        self.assertEqual(self.run_in_process(rig, send("admin", cos("approve", PR7))), 2)

    def test_a_ready_approve_line_passes(self):
        rig = self.rig([pr("SUCCESS")])
        self.assertEqual(self.run_in_process(rig, send("admin", cos("approve", PR7))), 0)

    def test_an_unchecked_approve_line_is_refused_too(self):
        rig = self.rig([pr("SUCCESS")])
        with mock.patch.dict(os.environ, {"GH_FAIL": "1"}):
            self.assertEqual(self.run_in_process(rig, send("admin", cos("approve", PR7))), 2)

    def test_the_final_reply_is_never_refused(self):
        rig = self.rig([pr("FAILURE")])
        self.assertEqual(self.run_in_process(rig, stop(f"Done. {PR7}")), 0)


if __name__ == "__main__":
    unittest.main()
