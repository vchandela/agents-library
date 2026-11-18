"""The SessionStart hook scripts/session-rules.py: after a compaction it names the skills the
session launched, so the session knows which ones to launch again.

Each test runs the real script with the hook input as JSON on stdin. The transcript fixture
has the shape Claude Code writes: one JSON line per message, with each Skill call a
tool_use block named "Skill" that carries input.skill.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "scripts" / "session-rules.py"
TRANSCRIPT = ROOT / "tests" / "fixtures" / "transcript.jsonl"


def run_hook(transcript_path):
    event = {"hook_event_name": "SessionStart", "source": "compact", "session_id": "s1"}
    if transcript_path is not None:
        event["transcript_path"] = str(transcript_path)
    done = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(event), text=True, capture_output=True)
    return done.returncode, done.stdout


class SkillsToRelaunch(unittest.TestCase):
    def test_a_transcript_with_skill_calls_prints_each_skill_once_in_first_use_order(self):
        code, out = run_hook(TRANSCRIPT)
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "Re-launch these skills: ship, explain-simply.")
        self.assertNotIn("decoy", out)

    def test_a_transcript_with_no_skill_calls_prints_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.jsonl"
            path.write_text(json.dumps({"type": "user", "message": {"role": "user", "content": "hello"}}) + "\n")
            self.assertEqual(run_hook(path), (0, ""))

    def test_a_missing_transcript_prints_the_generic_reminder_and_still_exits_zero(self):
        for path in (Path("/nonexistent/t.jsonl"), None):
            with self.subTest(path=path):
                code, out = run_hook(path)
                self.assertEqual(code, 0)
                self.assertIn("Could not read the transcript; re-launch the skills you were using", out)

    def test_the_hook_prints_no_rule_text(self):
        _, out = run_hook(TRANSCRIPT)
        core = (ROOT / "references" / "core.md").read_text()
        self.assertNotIn(core.splitlines()[4][:60], out)
        self.assertLess(len(out), 200)


if __name__ == "__main__":
    unittest.main()
