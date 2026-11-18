"""The production query guard (scripts/prod-query-guard.py), run the way Claude Code runs a hook.

Every test starts the real script as a subprocess, with the hook input as JSON on
stdin and HOME pointed at a temporary folder that holds the settings file.
All names are placeholders: app_readonly is the read-only login, app_admin the master one.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUARD = ROOT / "scripts" / "prod-query-guard.py"
FIXTURE = ROOT / "tests" / "fixtures" / "query_script.py"
SETTINGS = {
    "prod_markers": ["prod-db-tunnel"],
    "readonly_logins": ["app_readonly"],
    "refused_commands": ["prod-db-tunnel.sh --admin"],
}
HOST = "db.x.rds.amazonaws.com"
GOOD_SET = "SET statement_timeout='30s'"


def run_guard(command, settings=SETTINGS, files=None, session="s1"):
    """Return (exit code, stderr) for one Bash command, in a fresh HOME and cwd."""
    with tempfile.TemporaryDirectory() as tmp:
        home, work = Path(tmp) / "home", Path(tmp) / "work"
        (home / ".claude").mkdir(parents=True)
        work.mkdir()
        if settings is not None:
            text = settings if isinstance(settings, str) else json.dumps(settings)
            (home / ".claude" / "hook-settings.json").write_text(text)
        for name, content in (files or {}).items():
            (work / name).parent.mkdir(parents=True, exist_ok=True)
            (work / name).write_bytes(content if isinstance(content, bytes) else content.encode())
        event = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "session_id": session,
                 "cwd": str(work), "tool_input": {"command": command}}
        done = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(event), text=True,
                              capture_output=True, env={"HOME": str(home), "PATH": "/usr/bin:/bin"})
        return done.returncode, done.stderr


class GuardTest(unittest.TestCase):
    def passes(self, command, **kw):
        code, err = run_guard(command, **kw)
        self.assertEqual(code, 0, f"expected to pass: {command}\n{err}")

    def refused(self, command, needle=None, **kw):
        code, err = run_guard(command, **kw)
        self.assertEqual(code, 2, f"expected a refusal: {command}\n{err}")
        if needle:
            self.assertIn(needle, err)


class LoginForms(GuardTest):
    FORMS = {
        "conninfo": lambda u: f'psql "host={HOST} user={u}" -c "{GOOD_SET}; select 1"',
        "url": lambda u: f'psql postgresql://{u}@{HOST}/app -c "{GOOD_SET}; select 1"',
        "-U": lambda u: f'psql -h {HOST} -U {u} -c "{GOOD_SET}; select 1"',
        "--username": lambda u: f'psql -h {HOST} --username {u} -c "{GOOD_SET}; select 1"',
        "PGUSER": lambda u: f'PGUSER={u} psql -h {HOST} -c "{GOOD_SET}; select 1"',
        "python, single quotes": lambda u: (
            f"python3 -c \"import asyncpg; asyncpg.connect(host='{HOST}', user='{u}', "
            "server_settings={'statement_timeout': '30000'})\""),
        "python, double quotes": lambda u: (
            f"python3 -c 'import asyncpg; asyncpg.connect(host=\"{HOST}\", user=\"{u}\", "
            "server_settings={\"statement_timeout\": \"30000\"})'"),
    }

    def test_every_form_passes_for_the_read_only_login_and_is_refused_for_the_master_login(self):
        for name, form in self.FORMS.items():
            with self.subTest(form=name):
                self.passes(form("app_readonly"))
                self.refused(form("app_admin"), "app_admin")

    def test_a_production_query_with_no_login_named_is_refused(self):
        self.refused(f'psql -h {HOST} -c "{GOOD_SET}; select 1"', "login")


class TimeLimitForms(GuardTest):
    SQL = {
        "SET": "SET statement_timeout = {v}",
        "SET TO": "SET statement_timeout TO {v}",
        "SET LOCAL": "SET LOCAL statement_timeout = {v}",
        "set_config": "select set_config('statement_timeout', {v}, false)",
    }

    @staticmethod
    def quoted(value):
        return value if value.isdigit() else f"'{value}'"

    def test_sql_forms_pass_up_to_60s_and_are_refused_above_it_or_at_zero(self):
        for name, template in self.SQL.items():
            for value, ok in [("30s", True), ("60s", True), ("60S", True), ("1min", True), ("60000", True),
                              ("60001", False), ("90s", False), ("2min", False), ("0", False), ("0s", False)]:
                with self.subTest(form=name, value=value):
                    command = f'psql -h localhost -c "{template.format(v=self.quoted(value))}; select 1"'
                    self.passes(command) if ok else self.refused(command, "statement_timeout")

    def test_the_environment_and_driver_forms_are_read_the_same_way(self):
        connect = (f"python3 -c 'import asyncpg; asyncpg.connect(host=\"{HOST}\", user=\"app_readonly\", %s)'")
        forms = {
            "PGOPTIONS": lambda v: f"PGOPTIONS='-c statement_timeout={v}' psql -h {HOST} -U app_readonly -c 'select 1'",
            "options=": lambda v: connect % f"options='-c statement_timeout={v}'",
            "server_settings": lambda v: connect % "server_settings={\"statement_timeout\": \"%s\"}" % v,
        }
        for name, form in forms.items():
            with self.subTest(form=name):
                self.passes(form("30s"))
                self.refused(form("90s"), "statement_timeout")

    def test_a_psql_command_with_no_limit_is_refused_on_any_host(self):
        self.refused('psql -h localhost -c "select 1"', "statement_timeout")

    def test_the_same_command_with_a_limit_passes(self):
        self.passes(f'psql -h localhost -c "{GOOD_SET}; select 1"')


class ThirteenthOfNovember(GuardTest):
    """The query script that stalled a production roll, and its two refused twins."""

    COMMAND = "uv run python query_script.py"

    def script(self):
        return FIXTURE.read_text()

    def test_the_script_as_written_passes(self):
        self.passes(self.COMMAND, files={"query_script.py": self.script()})

    def test_the_same_script_without_its_time_limit_is_refused(self):
        text = self.script().replace('        server_settings={"statement_timeout": "60s"},\n', "")
        self.assertNotIn("statement_timeout", text)
        self.refused(self.COMMAND, "statement_timeout", files={"query_script.py": text})

    def test_the_same_script_on_the_master_login_is_refused(self):
        text = self.script().replace('user="app_readonly"', 'user="app_admin"')
        self.refused(self.COMMAND, "app_admin", files={"query_script.py": text})


class ReadingIsNotRunning(GuardTest):
    UNGUARDED = f'#!/bin/sh\npsql "host={HOST} user=app_readonly" -c "select 1"\n'

    def test_commands_that_only_read_a_script_pass(self):
        files = {"tunnel.sh": self.UNGUARDED, "q.sql": "select 1;\n"}
        for command in ["sed -n 1,40p tunnel.sh", "cat q.sql", "git grep -n psql", "git diff -- q.sql",
                        "grep -n psql tunnel.sh | head"]:
            with self.subTest(command=command):
                self.passes(command, files=files)

    def test_running_a_script_that_holds_an_unguarded_psql_is_refused(self):
        for command in ["bash q.sh", "sh q.sh", "./q.sh"]:
            with self.subTest(command=command):
                self.refused(command, "statement_timeout", files={"q.sh": self.UNGUARDED})

    def test_running_a_script_whose_psql_is_guarded_passes(self):
        guarded = f'#!/bin/sh\npsql "host={HOST} user=app_readonly" -c "{GOOD_SET}; select 1"\n'
        self.passes("bash q.sh", files={"q.sh": guarded})

    def test_running_a_sql_file_through_psql_reads_the_limit_from_the_file(self):
        self.refused("psql -h localhost -f q.sql", "statement_timeout", files={"q.sql": "select 1;\n"})
        self.passes("psql -h localhost -f q.sql", files={"q.sql": f"{GOOD_SET};\nselect 1;\n"})

    def test_a_command_that_wraps_psql_in_bash_c_is_still_seen(self):
        self.refused('bash -c "psql -h localhost -c \'select 1\'"', "statement_timeout")


class WhereTheCommandRuns(GuardTest):
    """An agent's Bash call is usually "cd <dir> && <command>", because the working folder resets after each call."""

    BAD = f"import asyncpg\nasyncpg.connect(host='{HOST}', user='app_admin')\n"

    def test_a_script_in_a_subfolder_is_found_after_cd_and_after_uv_run_directory(self):
        files = {"sub/q.py": self.BAD}
        for command in ["python3 sub/q.py", "cd sub && python q.py", "cd sub && uv run python q.py",
                        "uv run --directory sub python q.py", "uv run --directory=sub python q.py",
                        "cd ./sub; python3 q.py", "cd sub\npython3 q.py"]:
            with self.subTest(command=command):
                self.refused(command, "statement_timeout", files=files)

    def test_a_guarded_script_in_a_subfolder_passes_the_same_way(self):
        good = f"import asyncpg\nasyncpg.connect(host='{HOST}', user='app_readonly', server_settings={{'statement_timeout': '30000'}})\n"
        self.passes("cd sub && uv run python q.py", files={"sub/q.py": good})

    def test_a_cd_to_a_missing_folder_leaves_the_command_text_checked(self):
        self.refused("cd nowhere && psql -h localhost -c 'select 1'", "statement_timeout")


class ReadOnlyFlags(GuardTest):
    def test_asking_psql_for_its_version_or_help_runs_no_sql_and_passes(self):
        for command in ["psql --version", "psql -V", "psql --help", "pgcli --version"]:
            with self.subTest(command=command):
                self.passes(command)


class LoginFromAVariable(GuardTest):
    def test_a_login_read_from_a_variable_is_refused_with_a_clear_reason(self):
        body = f"import os, asyncpg\nasyncpg.connect(host='{HOST}', user=os.environ[\"DB_USER\"], server_settings={{'statement_timeout': '30000'}})\n"
        self.refused(f"uv run python - <<EOF\n{body}EOF", "no literal login")


class Heredocs(GuardTest):
    def test_a_python_heredoc_with_a_production_marker_and_the_master_login_is_refused(self):
        body = f"import asyncpg\nasyncpg.connect(host='{HOST}', user='app_admin', server_settings={{'statement_timeout': '30000'}})\n"
        self.refused(f"uv run python - <<EOF\n{body}EOF", "app_admin")

    def test_the_same_heredoc_on_the_read_only_login_passes(self):
        body = f"import asyncpg\nasyncpg.connect(host='{HOST}', user='app_readonly', server_settings={{'statement_timeout': '30000'}})\n"
        self.passes(f"uv run python - <<EOF\n{body}EOF")


class Tunnel(GuardTest):
    def test_the_tunnel_opener_and_the_token_line_pass(self):
        self.passes("./scripts/prod-db-tunnel.sh")
        self.passes(f"aws rds generate-db-auth-token --hostname {HOST} --username app_readonly --region us-west-2")

    def test_the_tunnel_with_admin_is_refused_even_though_it_runs_no_sql(self):
        self.refused("./scripts/prod-db-tunnel.sh --admin", "refused_commands")


class OtherCommands(GuardTest):
    def test_a_command_that_runs_no_sql_passes(self):
        self.passes("ls -la")

    def test_a_test_run_that_opens_a_database_without_a_marker_passes(self):
        test = "from sqlalchemy.ext.asyncio import create_async_engine\nengine = create_async_engine('sqlite+aiosqlite://')\n"
        self.passes("uv run pytest tests/test_db.py", files={"tests/test_db.py": test})
        self.passes("python3 db_check.py", files={"db_check.py": test})

    def test_a_missing_or_binary_executed_file_is_skipped(self):
        self.passes("uv run python missing.py")
        self.passes("python3 data.py", files={"data.py": b"\xff\xfe\x00\x00binary"})

    def test_a_missing_sql_file_still_leaves_the_command_text_checked(self):
        self.refused("psql -h localhost -f missing.sql", "statement_timeout")

    def test_a_pipe_inside_quotes_does_not_split_the_command(self):
        self.passes(f"psql -h localhost -c \"select 'a|b'; {GOOD_SET}\"")


class WithoutSettings(GuardTest):
    def test_the_time_limit_check_still_runs_and_the_login_check_is_off(self):
        command = f'psql "host={HOST} user=app_admin" -c "{GOOD_SET}; select 1"'
        self.passes(command, settings=None)
        self.refused(f'psql "host={HOST} user=app_admin" -c "select 1"', "statement_timeout", settings=None)

    def test_a_broken_settings_file_is_treated_as_missing(self):
        self.passes(f'psql "host={HOST} user=app_admin" -c "{GOOD_SET}; select 1"', settings="{not json")

    def test_the_warning_is_printed_once_per_session(self):
        command = f'psql -h localhost -c "{GOOD_SET}; select 1"'
        with tempfile.TemporaryDirectory() as tmp:
            event = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "session_id": "warn-once",
                     "cwd": tmp, "tool_input": {"command": command}}
            env = {"HOME": tmp, "PATH": "/usr/bin:/bin", "TMPDIR": tmp}
            errs = [subprocess.run([sys.executable, str(GUARD)], input=json.dumps(event), text=True,
                                   capture_output=True, env=env).stderr for _ in range(2)]
        self.assertIn("hook-settings.json", errs[0])
        self.assertEqual(errs[1], "")


class WhenTheGuardCrashes(GuardTest):
    BAD = {"refused_commands": 5}

    def test_a_crash_on_a_command_that_runs_sql_refuses_with_the_error(self):
        self.refused(f'psql -h localhost -c "{GOOD_SET}; select 1"', "prod-query-guard", settings=self.BAD)

    def test_a_crash_on_any_other_command_lets_it_run_and_prints_the_error(self):
        code, err = run_guard("ls -la", settings=self.BAD)
        self.assertEqual(code, 0)
        self.assertIn("prod-query-guard", err)


if __name__ == "__main__":
    unittest.main()
