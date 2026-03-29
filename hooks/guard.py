#!/usr/bin/env python3
"""Guard hook: blocks file modifications and dangerous Bash commands outside the project directory."""

from __future__ import annotations

import json
import os
import re
import shlex
import sys

PROJECT_DIR = "{PROJECT_DIR}"

WRITE_TOOLS = {"Write", "Edit", "NotebookEdit"}

ALLOWED_PREFIXES = [
    "/tmp",
    "/var/tmp",
]

DANGEROUS_COMMANDS = {
    "rm", "rmdir", "unlink", "shred",
    "mv", "cp",
    "chmod", "chown",
    "dd", "truncate",
    "ln",
}

DANGEROUS_GIT_PATTERNS = [
    re.compile(r"\bgit\s+reset\s+--hard"),
    re.compile(r"\bgit\s+clean\s+.*-[a-zA-Z]*[fd]"),
    re.compile(r"\bgit\s+push\s+.*(-f\b|--force)"),
    re.compile(r"\bgit\s+checkout\s+--\s+\."),
]

REDIRECT_PATH_RE = re.compile(r"(?<!<)>{1,2}\s*(/\S+)")
TEE_PATH_RE = re.compile(r"\btee\s+(?:-[a-zA-Z]*\s+)*(/\S+)")

SUDO_ARG_FLAGS = {"-u", "-g", "-C", "-D", "-R", "-T", "-h", "-p"}


def get_file_path(tool_input: dict) -> str | None:
    if "file_path" in tool_input:
        return tool_input["file_path"]
    if "path" in tool_input:
        return tool_input["path"]
    return None


def is_within_directory(file_path: str, directory: str) -> bool:
    try:
        resolved = os.path.realpath(file_path)
        resolved_dir = os.path.realpath(directory)
        return resolved.startswith(resolved_dir + os.sep) or resolved == resolved_dir
    except (OSError, ValueError):
        return False


def is_allowed_exception(file_path: str) -> bool:
    resolved = os.path.realpath(file_path)

    for prefix in ALLOWED_PREFIXES:
        if resolved.startswith(prefix + os.sep) or resolved == prefix:
            return True

    if is_within_directory(file_path, os.path.join(PROJECT_DIR, ".claude")):
        return True

    return False


def is_path_ok(path: str) -> bool:
    return is_within_directory(path, PROJECT_DIR) or is_allowed_exception(path)


def strip_sudo(tokens: list[str]) -> list[str]:
    if not tokens or tokens[0] != "sudo":
        return tokens
    i = 1
    while i < len(tokens):
        if tokens[i] == "--":
            return tokens[i + 1:]
        if tokens[i].startswith("-"):
            if tokens[i] in SUDO_ARG_FLAGS and i + 1 < len(tokens):
                i += 2
            else:
                i += 1
        else:
            break
    return tokens[i:] if i < len(tokens) else tokens


def check_bash_command(command: str) -> str | None:
    for pattern in DANGEROUS_GIT_PATTERNS:
        if pattern.search(command):
            return f"Destructive git operation blocked."

    reason = _check_redirects(command)
    if reason:
        return reason

    for segment in re.split(r"\s*(?:&&|\|\||;|\|)\s*", command):
        reason = _check_segment(segment.strip())
        if reason:
            return reason

    return None


def _check_redirects(command: str) -> str | None:
    for match in REDIRECT_PATH_RE.finditer(command):
        path = match.group(1)
        if not is_path_ok(path):
            return f"Redirect targets outside project: {path}"

    for match in TEE_PATH_RE.finditer(command):
        path = match.group(1)
        if not is_path_ok(path):
            return f"tee targets outside project: {path}"

    return None


def _check_segment(segment: str) -> str | None:
    if not segment:
        return None

    try:
        tokens = shlex.split(segment)
    except ValueError:
        return None

    if not tokens:
        return None

    tokens = strip_sudo(tokens)
    if not tokens:
        return None

    cmd = os.path.basename(tokens[0])

    if cmd not in DANGEROUS_COMMANDS:
        return None

    for arg in tokens[1:]:
        if arg.startswith("-"):
            continue
        if arg.startswith("$"):
            continue

        # dd uses key=value args (e.g. of=/dev/sda)
        if cmd == "dd" and "=" in arg:
            key, _, val = arg.partition("=")
            if key in ("of", "if") and val:
                path = val if os.path.isabs(val) else os.path.join(PROJECT_DIR, val)
                if not is_path_ok(path):
                    return f"'{cmd}' targets outside project: {val}"
            continue

        path = arg if os.path.isabs(arg) else os.path.join(PROJECT_DIR, arg)
        if not is_path_ok(path):
            return f"'{cmd}' targets outside project: {arg}"

    return None


def block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


def allow() -> None:
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)


def main() -> None:
    if PROJECT_DIR == "{" + "PROJECT_DIR" + "}":
        block("Guard not initialized — run /tars:init first.")
        return

    try:
        raw = sys.stdin.read()
        event = json.loads(raw)
    except (json.JSONDecodeError, IOError) as e:
        block(f"Failed to parse hook event: {e}")
        return

    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input", {})

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        reason = check_bash_command(command)
        if reason:
            block(reason)
        allow()
        return

    if tool_name not in WRITE_TOOLS:
        allow()
        return

    file_path = get_file_path(tool_input)
    if file_path is None:
        allow()
        return

    if is_within_directory(file_path, PROJECT_DIR):
        allow()
        return

    if is_allowed_exception(file_path):
        allow()
        return

    block(
        f"Blocked: {tool_name} targets '{file_path}' which is outside "
        f"the project directory '{PROJECT_DIR}'."
    )


if __name__ == "__main__":
    main()
