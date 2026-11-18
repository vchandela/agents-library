"""scripts/setup installs the hooks, the memory folder and the hook settings file.

Every test runs the real setup as a subprocess with HOME pointed at a temporary folder, the way
its docstring says to try it on a copy. The "today's settings" case has the shape of a real
settings.json: a review-request-check entry on SendMessage, installed by hand, and an
Artifact entry that setup must leave alone.
"""

import json
import os
import pty
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETUP = ROOT / "scripts" / "setup"
HOOKS = {
    ("PreToolUse", "Edit|Write|MultiEdit|NotebookEdit", "skill-gate.py"),
    ("PreToolUse", "Bash", "prod-query-guard.py"),
    ("PreToolUse", "SendMessage", "review-request-check.py"),
    ("Stop", None, "review-request-check.py"),
    ("SessionStart", "compact", "session-rules.py"),
}
TODAY = {
    "autoMemoryDirectory": "~/.claude/memory",
    "model": "opus",
    "hooks": {"PreToolUse": [
        {"matcher": "SendMessage", "hooks": [{"type": "command", "command": "python3 /old/place/review-request-check.py"}]},
        {"matcher": "Artifact", "hooks": [{"type": "command", "command": "python3 /old/place/artifact-visual-check.py"}]},
    ]},
}


class SetupTest(unittest.TestCase):
    def home(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        home = Path(tmp.name)
        (home / ".claude").mkdir()
        return home

    def run_setup(self, home, *args):
        done = subprocess.run([sys.executable, str(SETUP), *args], capture_output=True, text=True,
                              stdin=subprocess.DEVNULL, env={"HOME": str(home), "PATH": "/usr/bin:/bin"})
        return done.returncode, done.stdout, done.stderr

    @staticmethod
    def installed(settings):
        found = set()
        for event, entries in settings.get("hooks", {}).items():
            for entry in entries:
                for hook in entry["hooks"]:
                    for want in HOOKS:
                        if want[0] == event and want[2] in hook["command"] and entry.get("matcher") == want[1]:
                            found.add(want)
        return found


class Install(SetupTest):
    def test_an_empty_home_gets_all_five_hooks_and_the_memory_folder_and_a_warning(self):
        home = self.home()
        code, out, err = self.run_setup(home)
        self.assertEqual(code, 0, err)
        settings = json.loads((home / ".claude" / "settings.json").read_text())
        self.assertEqual(self.installed(settings), HOOKS)
        self.assertEqual(settings["autoMemoryDirectory"], "~/.claude/memory")
        self.assertIn("hook-settings.json", err)
        self.assertFalse((home / ".claude" / "hook-settings.json").exists())

    def test_the_two_review_request_entries_carry_a_ten_second_timeout(self):
        home = self.home()
        self.run_setup(home)
        settings = json.loads((home / ".claude" / "settings.json").read_text())
        timeouts = [h.get("timeout") for entries in settings["hooks"].values() for e in entries for h in e["hooks"]
                    if "review-request-check.py" in h["command"]]
        self.assertEqual(timeouts, [10, 10])

    def test_a_second_run_leaves_settings_json_byte_identical(self):
        home = self.home()
        self.run_setup(home)
        first = (home / ".claude" / "settings.json").read_bytes()
        code, out, _ = self.run_setup(home)
        self.assertEqual(code, 0)
        self.assertEqual((home / ".claude" / "settings.json").read_bytes(), first)
        self.assertIn("nothing to change", out)


class OnlyOnChange(SetupTest):
    def test_settings_that_are_already_complete_are_not_rewritten_even_in_another_format(self):
        home = self.home()
        self.run_setup(home)
        file = home / ".claude" / "settings.json"
        compact = json.dumps(json.loads(file.read_text()), separators=(",", ":")).encode()
        file.write_bytes(compact)
        self.run_setup(home)
        self.assertEqual(file.read_bytes(), compact)


class TodaysSettings(SetupTest):
    def setUp(self):
        self.home_dir = self.home()
        (self.home_dir / ".claude" / "settings.json").write_text(json.dumps(TODAY, indent=2) + "\n")
        self.run_setup(self.home_dir)
        self.after = json.loads((self.home_dir / ".claude" / "settings.json").read_text())

    def test_the_hand_installed_send_message_entry_is_updated_in_place(self):
        first = self.after["hooks"]["PreToolUse"][0]
        self.assertEqual(first["matcher"], "SendMessage")
        self.assertEqual(first["hooks"][0]["command"], f"python3 {ROOT / 'scripts' / 'review-request-check.py'}")
        self.assertEqual(first["hooks"][0]["timeout"], 10)
        count = sum("review-request-check.py" in h["command"] for e in self.after["hooks"]["PreToolUse"] for h in e["hooks"])
        self.assertEqual(count, 1)

    def test_the_artifact_entry_and_every_other_setting_are_kept(self):
        self.assertEqual(self.after["hooks"]["PreToolUse"][1], TODAY["hooks"]["PreToolUse"][1])
        self.assertEqual(self.after["model"], "opus")

    def test_an_absolute_path_to_the_memory_folder_is_not_rewritten(self):
        home = self.home()
        mine = {"autoMemoryDirectory": str(home / ".claude" / "memory")}
        (home / ".claude" / "settings.json").write_text(json.dumps(mine))
        self.run_setup(home)
        self.assertEqual(json.loads((home / ".claude" / "settings.json").read_text())["autoMemoryDirectory"], mine["autoMemoryDirectory"])


class HookSettingsFile(SetupTest):
    def test_an_existing_file_is_never_touched(self):
        home = self.home()
        mine = '{"prod_markers": ["mine"], "readonly_logins": [], "refused_commands": []}\n'
        (home / ".claude" / "hook-settings.json").write_text(mine)
        self.run_setup(home)
        self.assertEqual((home / ".claude" / "hook-settings.json").read_text(), mine)

    def at_a_terminal(self, home):
        """Run setup with a real terminal as stdin, and type the three answers before it asks."""
        master, slave = pty.openpty()
        proc = subprocess.Popen([sys.executable, str(SETUP)], stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env={"HOME": str(home), "PATH": "/usr/bin:/bin"}, text=True)
        # The terminal holds typed input until setup reads it, so all three answers can go in at once.
        os.write(master, b"prod-db-tunnel, 127.0.0.1:15434\napp_readonly\nprod-db-tunnel.sh --admin\n")
        proc.communicate(timeout=20)
        os.close(master)

    def test_at_a_terminal_setup_asks_for_the_three_lists_and_writes_the_file(self):
        home = self.home()
        self.at_a_terminal(home)
        self.assertEqual(json.loads((home / ".claude" / "hook-settings.json").read_text()), {
            "prod_markers": ["prod-db-tunnel", "127.0.0.1:15434"],
            "readonly_logins": ["app_readonly"],
            "refused_commands": ["prod-db-tunnel.sh --admin"]})

    def test_at_a_terminal_an_existing_file_is_still_never_touched(self):
        home = self.home()
        mine = '{"prod_markers": ["mine"], "readonly_logins": [], "refused_commands": []}\n'
        (home / ".claude" / "hook-settings.json").write_text(mine)
        self.at_a_terminal(home)
        self.assertEqual((home / ".claude" / "hook-settings.json").read_text(), mine)


class Check(SetupTest):
    def test_check_on_a_fresh_home_names_each_missing_entry_and_changes_nothing(self):
        home = self.home()
        code, out, _ = self.run_setup(home, "--check")
        self.assertEqual(code, 1)
        for name in ("skill-gate.py", "prod-query-guard.py", "review-request-check.py", "session-rules.py",
                     "autoMemoryDirectory", "hook-settings.json"):
            self.assertIn(name, out)
        self.assertEqual(sum("review-request-check.py" in line for line in out.splitlines()), 2)
        self.assertFalse((home / ".claude" / "settings.json").exists())

    def test_check_after_setup_reports_only_the_missing_hook_settings_file(self):
        home = self.home()
        self.run_setup(home)
        code, out, _ = self.run_setup(home, "--check")
        self.assertEqual(code, 1)
        self.assertEqual([line for line in out.splitlines() if "missing" in line or "stale" in line],
                         [line for line in out.splitlines() if "hook-settings.json" in line])


class Safety(SetupTest):
    def test_a_symlinked_settings_file_is_written_through_and_the_link_kept(self):
        home = self.home()
        real = home / "dotfiles" / "settings.json"
        real.parent.mkdir()
        real.write_text('{"model": "opus"}\n')
        (home / ".claude" / "settings.json").symlink_to(real)
        self.run_setup(home)
        self.assertTrue((home / ".claude" / "settings.json").is_symlink())
        self.assertEqual(self.installed(json.loads(real.read_text())), HOOKS)

    def test_a_settings_file_that_is_not_valid_json_is_left_alone_and_reported(self):
        home = self.home()
        (home / ".claude" / "settings.json").write_text("{not json")
        code, _, err = self.run_setup(home)
        self.assertEqual(code, 1)
        self.assertIn("not valid JSON", err)
        self.assertEqual((home / ".claude" / "settings.json").read_text(), "{not json")


if __name__ == "__main__":
    unittest.main()
