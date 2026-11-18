"""The skill size check in scripts/lint-skills.py: a SKILL.md of 20,000 characters or more fails.

Each test copies the repo to a temporary folder, sets one SKILL.md to an exact
length, and runs the real lint there, the way CI runs it.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = "save-to-notes"


def lint_with_skill_of(length: int) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        shutil.copytree(ROOT, repo, ignore=shutil.ignore_patterns(".git"))
        skill = repo / "skills" / SKILL / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        # One long word, so the word-count check stays out of the way.
        skill.write_text(text + "\n" + "x" * (length - len(text) - 1), encoding="utf-8")
        assert len(skill.read_text(encoding="utf-8")) == length
        return subprocess.run(
            [sys.executable, str(repo / "scripts" / "lint-skills.py")],
            capture_output=True, text=True, check=False,
        )


class SkillSizeCheck(unittest.TestCase):
    def test_a_skill_of_20000_characters_fails_and_names_the_skill(self):
        result = lint_with_skill_of(20000)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(f"skills/{SKILL}/SKILL.md", result.stdout)
        self.assertIn("20000", result.stdout)

    def test_a_skill_of_19999_characters_passes(self):
        result = lint_with_skill_of(19999)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
