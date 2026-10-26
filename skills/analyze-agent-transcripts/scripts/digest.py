#!/usr/bin/env python3
"""Shorten a Claude Code session JSONL into a digest a reader can read whole.

Keeps every user and assistant sentence, incoming cross-session messages, slash
commands, each tool call with a shortened input, errors and "saved to" pointers.
Bulky tool results become [dropped, N lines]. Compaction summaries and skill
bodies are dropped and marked, since the agent under review wrote the former.
Every digest line starts with L<n>, the raw JSONL line number, so a reader can
ask for the raw spot. Anything shaped like a token, key or password is replaced
with [REDACTED] as it is written.

Pass from_line to read a session that grew since the ledger's "lines <n>": give
n + 1.

usage: digest.py <session.jsonl> [from_line] > digest.txt
"""
import json, re, sys

if len(sys.argv) not in (2, 3) or (len(sys.argv) == 3 and not sys.argv[2].isdigit()):
    sys.exit("usage: digest.py <session.jsonl> [from_line] > digest.txt")
path = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 1

# Cut lengths below are long enough to quote a message and short enough to keep a
# 360 MB session under 8 MB of digest.
REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
SECRET = re.compile(
    r"(sk-[A-Za-z0-9_\-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abpr]-[A-Za-z0-9\-]{10,}"
    r"|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"
    r"|(?i:(?:password|passwd|secret|token|api[_-]?key)\s*[=:]\s*)\S{6,})"
)


def red(s):
    return SECRET.sub("[REDACTED]", s)


def short(s, n):
    s = s if isinstance(s, str) else json.dumps(s)
    s = s.replace("\n", " ⏎ ")
    return s if len(s) <= n else s[:n] + f" …[+{len(s) - n} chars]"


def text_of(content):
    if isinstance(content, str):
        return content
    out = []
    for c in content or []:
        if isinstance(c, dict):
            if c.get("type") == "text":
                out.append(c.get("text", ""))
            elif c.get("type") == "image":
                out.append("[image]")
    return "\n".join(out)


def tool_input(name, inp):
    if not isinstance(inp, dict):
        return short(inp, 300)
    if name in ("SendMessage",):
        return f"to={inp.get('to')} :: " + short(inp.get("message", inp), 700)
    if name in ("Agent", "Task"):
        return f"[{inp.get('subagent_type', '')}/{inp.get('model', '')}] {inp.get('description', '')} :: " + short(inp.get("prompt", ""), 600)
    if name == "Bash":
        return (f"({inp.get('description', '')}) " if inp.get("description") else "") + short(inp.get("command", ""), 120)
    if name in ("Edit", "MultiEdit"):
        return f"{inp.get('file_path')} :: old={short(inp.get('old_string', ''), 150)} new={short(inp.get('new_string', ''), 250)}"
    if name == "Write":
        c = inp.get("content", "")
        return f"{inp.get('file_path')} [{c.count(chr(10)) + 1} lines] {short(c, 200)}"
    if name == "Read":
        return f"{inp.get('file_path')} off={inp.get('offset', '')} lim={inp.get('limit', '')}"
    if name == "AskUserQuestion":
        return short(inp.get("questions", inp), 800)
    if "slack" in name.lower() or "send_message" in name.lower() or "create" in name.lower():
        return short(inp, 600)
    return short(inp, 300)


pending = {}
last_model = None
out = []
with open(path) as fh:
    for n, line in enumerate(fh, 1):
        if n < start:
            continue
        try:
            d = json.loads(line)
        except Exception:
            out.append(f"L{n} [unparseable line]")
            continue
        t = d.get("type")
        ts = (d.get("timestamp") or "")[5:16].replace("T", " ")
        side = " (sidechain)" if d.get("isSidechain") else ""

        if t == "queue-operation" and d.get("operation") == "enqueue" and d.get("content"):
            c = d["content"]
            if isinstance(c, str):
                out.append(f"L{n} {ts} QUEUED-IN: " + short(red(c), 1000))
            continue
        if t == "attachment":
            a = d.get("attachment", {})
            at = a.get("type")
            if at == "file" and "tasks/" in str(a.get("filename", "")):
                out.append(f"L{n} {ts} [background task output attached: {a.get('filename')}]")
            continue
        if t == "system":
            st = d.get("subtype")
            if st == "local_command":
                out.append(f"L{n} {ts} SLASH: " + short(re.sub(r"<[^>]+>", " ", d.get("content", "")), 300))
            elif st == "compact_boundary":
                out.append(f"L{n} {ts} [=== context compacted ===]")
            elif st == "api_error" or d.get("level") == "error":
                out.append(f"L{n} {ts} SYS-ERROR: " + short(str(d.get("content", d.get("error", ""))), 400))
            continue
        if t not in ("user", "assistant"):
            continue
        msg = d.get("message", {})
        content = msg.get("content")

        if t == "assistant":
            m = msg.get("model")
            if m and m != last_model and m != "<synthetic>":
                out.append(f"L{n} [model: {m}]")
                last_model = m
            for c in content if isinstance(content, list) else []:
                ct = c.get("type")
                if ct == "text" and c.get("text", "").strip():
                    out.append(f"L{n} {ts} AGENT{side}: " + red(c["text"].strip()).replace("\n", f"\nL{n}   "))
                elif ct == "tool_use":
                    pending[c.get("id")] = c.get("name")
                    out.append(f"L{n} {ts} CALL{side} {c.get('name')}: " + red(tool_input(c.get("name"), c.get("input"))))
            continue

        # user
        if d.get("isCompactSummary"):
            out.append(f"L{n} {ts} [compaction summary dropped, {len(text_of(content))} chars; written by the agent under review]")
            continue
        if isinstance(content, list) and any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content):
            for c in content:
                if c.get("type") != "tool_result":
                    continue
                name = pending.get(c.get("tool_use_id"), "?")
                body = text_of(c.get("content")) if not isinstance(c.get("content"), str) else c.get("content")
                body = body or ""
                lines = body.count("\n") + 1
                saved = re.findall(r"[Oo]utput (?:has been |was )?saved to[^\n]*", body)
                if c.get("is_error"):
                    out.append(f"L{n} {ts} RESULT-ERROR {name}: " + short(red(body), 700))
                elif name in ("SendMessage", "AskUserQuestion", "ExitPlanMode") or len(body) <= 300:
                    out.append(f"L{n} {ts} RESULT {name}: " + short(red(body), 800))
                else:
                    out.append(f"L{n} {ts} RESULT {name}: {short(red(body), 80)} [dropped, {lines} lines]")
                for s in saved:
                    out.append(f"L{n}   ↳ {s[:300]}")
            continue
        txt = text_of(content)
        if txt.startswith("Base directory for this skill"):
            out.append(f"L{n} {ts} [skill body loaded: {short(txt.splitlines()[0], 140)}; dropped {txt.count(chr(10))} lines]")
            continue
        stripped = REMINDER.sub("", txt).strip()
        if not stripped:
            continue
        if d.get("isMeta") and ("Another Claude session sent" in stripped or "cross-session-message" in stripped):
            continue
        if d.get("isMeta"):
            out.append(f"L{n} {ts} META: " + short(red(stripped), 400))
            continue
        if stripped.startswith("<task-notification>"):
            st = re.search(r"<status>(.*?)</status>", stripped, re.S)
            sm = re.search(r"<summary>(.*?)</summary>", stripped, re.S)
            out.append(f"L{n} {ts} TASK-NOTICE: {st.group(1) if st else ''} {short(sm.group(1) if sm else stripped, 200)}")
            continue
        if stripped.startswith(("<bash-stdout>", "<local-command-stdout>", "<bash-stderr>")):
            out.append(f"L{n} {ts} USER-SHELL-OUT: " + short(red(stripped), 200))
            continue
        stripped = re.sub(r"<pasted_content[^>]*>(.*?)</pasted_content[^>]*>",
                          lambda m: "<pasted>" + short(m.group(1), 700) + f"</pasted {len(m.group(1))} chars>", stripped, flags=re.S)
        out.append(f"L{n} {ts} USER: " + red(stripped).replace("\n", f"\nL{n}   "))

sys.stdout.write("\n".join(out) + "\n")
