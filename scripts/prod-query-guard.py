#!/usr/bin/env python3
"""PreToolUse hook on Bash: refuse a database query that sets no time limit,
and a production query on a login that is not read-only.

Two checks, from the rule in references/shipping.md ("a query against production"):

1. Time limit. Every psql or pgcli command, every .sql file psql runs, and every
   script that connects to a production database must set a statement_timeout of
   60 s or less, and never zero. The login's own limit does not count: it lives
   in another repo and can be raised without anyone noticing.
2. Login. A command that runs SQL against production must name a login listed in
   `readonly_logins` in ~/.claude/hook-settings.json, which holds the company
   details so this repo holds none:

       {"prod_markers": [...], "readonly_logins": [...], "refused_commands": [...]}

   With no settings file, only check 1 runs, and one warning is printed per session.

A command counts as production when its text, or the text of a script it runs,
holds an RDS host, an RDS sign-in token, or a `prod_markers` entry. A command only
reads a script (`cat q.sql`, `sed -n 1,40p x.sh`, `git grep psql`) unless the
script is its program or an argument its program executes. Files are read one
level deep; a file that imports another is not followed. The guard is a strong
default, not a sandbox: a query built through a variable or a second file passes.

Exit 2 refuses the command and shows the reason to the agent. The guard never
rewrites a command, because Claude Code ignores a hook's rewrite of a Bash command.
A crash on a command that runs SQL refuses it, because a guard that fails open guards
nothing. A crash on any other command lets it run and prints the error.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
import tempfile
from pathlib import Path

MAX_MS = 60_000  # references/shipping.md: a production query sets 60 s at most
GENERIC_MARKERS = ("rds.amazonaws.com", "generate-db-auth-token")
SETTINGS_FILE = Path.home() / ".claude" / "hook-settings.json"
MAX_FILE_BYTES = 1_000_000

PSQL = {"psql", "pgcli"}
PYTHON = re.compile(r"python[\d.]*")
SHELLS = {"bash", "sh", "zsh"}
WRAPPERS = {"env", "time", "nohup", "command", "exec", "sudo"}
UV_FLAGS_WITH_VALUE = {"--with", "--python", "-p", "--directory", "--project", "--env-file", "--group", "--extra"}
HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1")
CONNECT = re.compile(r"\b(asyncpg\.(?:connect|create_pool)|psycopg2?\.connect|create_engine|create_async_engine)\s*\(")
SQL_SHAPED = re.compile(r"\b(psql|pgcli)\b|\.sql\b|asyncpg|psycopg|create_(async_)?engine")

_UNIT_MS = {"us": 0.001, "ms": 1, "s": 1000, "min": 60_000, "h": 3_600_000, "d": 86_400_000}
# A statement_timeout value in every form query scripts use: SET [LOCAL] x = '30s', SET x TO 30000,
# set_config('statement_timeout', '30s', ...), -c statement_timeout=30s in PGOPTIONS or options=,
# and 'statement_timeout': '30000' in asyncpg's server_settings. A bare number is milliseconds.
_TIMEOUT = re.compile(r"statement_timeout['\"]?\s*(?:=|:|,|\bTO\b)\s*['\"]?\s*(\d+(?:\.\d+)?)\s*(us|ms|s|min|h|d)?\b", re.I)
_LOGINS = (
    re.compile(r"\buser\s*=\s*['\"]?([\w.-]+)", re.I),                  # conninfo, Python user="x"
    re.compile(r"postgres(?:ql)?://([^:@/\s]+)(?::[^@/\s]*)?@"),         # URL
    re.compile(r"(?:^|\s)-U\s*['\"]?([\w.-]+)"),                         # psql -U x
    re.compile(r"--username[=\s]\s*['\"]?([\w.-]+)"),                    # --username x
    re.compile(r"\bPGUSER=['\"]?([\w.-]+)"),                             # environment
)


def timeouts_ms(text: str) -> list[float]:
    return [float(n) * _UNIT_MS[(u or "ms").lower()] for n, u in _TIMEOUT.findall(text)]


def logins(text: str) -> set[str]:
    return {m for pattern in _LOGINS for m in pattern.findall(text)}


def segments(command: str) -> list[str]:
    """Split a shell command on ; | & and newlines, outside quotes. A heredoc body stays in its segment."""
    out, cur, quote, pending, i = [], [], "", [], 0
    while i < len(command):
        c = command[i]
        if quote:
            cur.append(c)
            if c == "\\" and quote == '"' and i + 1 < len(command):
                i += 1
                cur.append(command[i])
            elif c == quote:
                quote = ""
        elif c in "'\"":
            quote = c
            cur.append(c)
        elif c == "\\" and i + 1 < len(command):
            cur.append(c + command[i + 1])
            i += 1
        elif command.startswith("<<", i) and not command.startswith("<<<", i) and (m := HEREDOC.match(command, i)):
            pending.append((m.group(2), "-" in m.group(0)[:3]))
            cur.append(m.group(0))
            i = m.end() - 1
        elif c == "\n" and pending:
            lines, j = [], i + 1
            delimiter, strip = pending.pop(0)
            while j < len(command):
                end = command.find("\n", j)
                end = len(command) if end < 0 else end
                line = command[j:end]
                j = end + 1
                if (line.strip() if strip else line) == delimiter:
                    break
                lines.append(line)
            cur.append("\n" + "\n".join(lines))
            out.append("".join(cur))
            cur = []
            i = j - 1
        elif c in ";|\n" or (c == "&" and command[i - 1:i] not in ("<", ">") and command[i + 1:i + 2] != ">"):
            out.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    out.append("".join(cur))
    return [s for s in out if s.strip()]


def tokens(segment: str) -> list[str]:
    head = segment[:m.end()] if (m := HEREDOC.search(segment)) else segment
    try:
        return shlex.split(head)
    except ValueError:
        return head.split()


def program(words: list[str]) -> tuple[str, list[str]]:
    """The program a segment starts, after VAR=value, env, uv run and the like, and its arguments."""
    i = 0
    while i < len(words):
        w = words[i]
        if re.match(r"\w+=", w) or w in WRAPPERS or (w.startswith("-") and i and words[i - 1] == "env"):
            i += 1
        elif w == "uv" and words[i + 1:i + 2] == ["run"]:
            i += 2
            while i < len(words) and words[i].startswith("-"):
                i += 2 if words[i] in UV_FLAGS_WITH_VALUE else 1
        else:
            break
    return (words[i], words[i + 1:]) if i < len(words) else ("", [])


def executed_files(prog: str, args: list[str], cwd: Path) -> list[Path]:
    """Files the program executes, as the command names them: python x.py, bash x.sh, ./x.sh, psql -f x.sql."""
    names = []
    base = os.path.basename(prog)
    if PYTHON.fullmatch(base):
        names = [next((a for a in args if not a.startswith("-")), "")]
    elif base in SHELLS and "-c" not in args:
        names = [next((a for a in args if not a.startswith("-")), "")]
    elif base in PSQL:
        for k, a in enumerate(args):
            if a in ("-f", "--file") and k + 1 < len(args):
                names.append(args[k + 1])
            elif a.startswith("--file="):
                names.append(a[7:])
            elif a.startswith("<") and not a.startswith("<<") and len(a) > 1:
                names.append(a[1:])
            elif a == "<" and k + 1 < len(args):
                names.append(args[k + 1])
    elif prog.endswith((".sh", ".py")):
        names = [prog]
    files = []
    for name in names:
        path = cwd / os.path.expanduser(name)
        if name and path.is_file() and path.stat().st_size <= MAX_FILE_BYTES:
            files.append(path)
    return files


def read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def check_segment(segment: str, cwd: Path, settings: dict, follow: bool = True) -> str | None:
    """The reason to refuse one segment, or None."""
    words = tokens(segment)
    prog, args = program(words)
    base = os.path.basename(prog)
    if base in SHELLS and "-c" in args and args.index("-c") + 1 < len(args):
        for inner in segments(args[args.index("-c") + 1]):
            if reason := check_segment(inner, cwd, settings, follow):
                return reason
    texts, runs_sql, is_python = [segment], base in PSQL, bool(PYTHON.fullmatch(base))
    for path in executed_files(prog, args, cwd) if follow else []:
        text = read(path)
        if text is None:
            continue
        if path.suffix == ".sh":
            for inner in segments(text):
                if reason := check_segment(inner, cwd, settings, follow=False):
                    return reason
        else:
            texts.append(text)
            runs_sql = runs_sql or path.suffix == ".sql"
            is_python = is_python or path.suffix == ".py"
    text = "\n".join(texts)
    has_connect = is_python and bool(CONNECT.search(text))
    if not (runs_sql or has_connect):
        return None
    markers = GENERIC_MARKERS + tuple(settings.get("prod_markers", []))
    prod = any(m in text for m in markers)
    if runs_sql or prod:
        limits = timeouts_ms(text)
        if not limits or any(ms <= 0 or ms > MAX_MS for ms in limits):
            return f"this command runs SQL with no statement_timeout of {MAX_MS // 1000}s or less. Set statement_timeout to {MAX_MS // 1000}s or less first."
    allowed = set(settings.get("readonly_logins", []))
    if prod and allowed:
        used = logins(text)
        if not used or used - allowed:
            who = ", ".join(sorted(used - allowed)) or "no login named"
            return f"production query on {who}; use a login in readonly_logins ({SETTINGS_FILE})."
    return None


def decide(command: str, cwd: Path, settings: dict) -> str | None:
    if any(entry in command for entry in settings.get("refused_commands", [])):
        return f"this command is listed in refused_commands in {SETTINGS_FILE}. The user runs it, not the agent."
    for segment in segments(command):
        if reason := check_segment(segment, cwd, settings):
            return reason
    return None


def load_settings(session: str) -> dict:
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        warned = Path(tempfile.gettempdir()) / f"prod-query-guard-warned-{re.sub(r'[^\w-]', '_', session)}"
        if not warned.exists():
            warned.touch()
            print(f"prod-query-guard: {SETTINGS_FILE} is missing or not valid JSON, so the login and "
                  "refused-command checks are off. The time limit check still runs.", file=sys.stderr)
        return {}


def main() -> int:
    event = json.load(sys.stdin)
    command = str((event.get("tool_input") or {}).get("command") or "")
    cwd = Path(event.get("cwd") or ".")
    try:
        reason = decide(command, cwd, load_settings(str(event.get("session_id") or "none")))
    except Exception as error:  # noqa: BLE001 - see the module docstring
        print(f"prod-query-guard crashed: {error!r}", file=sys.stderr)
        return 2 if SQL_SHAPED.search(command) else 0
    if reason:
        print(f"Blocked: {reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
