#!/usr/bin/env python3
"""Guard hook: blocks file modifications outside the project directory.

Placeholder {PROJECT_DIR} is replaced with the actual project path during init.
"""

import json
import os
import sys

PROJECT_DIR = "{PROJECT_DIR}"

WRITE_TOOLS = {"Write", "Edit", "NotebookEdit"}

ALLOWED_PREFIXES = [
    "/tmp",
    "/var/tmp",
]


def get_file_path(tool_input: dict) -> str | None:
    """Extract file_path from tool input regardless of tool type."""
    if "file_path" in tool_input:
        return tool_input["file_path"]
    if "path" in tool_input:
        return tool_input["path"]
    return None


def is_within_directory(file_path: str, directory: str) -> bool:
    """Check if file_path is within directory, resolving symlinks."""
    try:
        resolved = os.path.realpath(file_path)
        resolved_dir = os.path.realpath(directory)
        return resolved.startswith(resolved_dir + os.sep) or resolved == resolved_dir
    except (OSError, ValueError):
        return False


def is_allowed_exception(file_path: str) -> bool:
    """Check if the path falls under an allowed exception."""
    resolved = os.path.realpath(file_path)

    for prefix in ALLOWED_PREFIXES:
        if resolved.startswith(prefix + os.sep) or resolved == prefix:
            return True

    # .claude paths within the project directory
    if is_within_directory(file_path, os.path.join(PROJECT_DIR, ".claude")):
        return True

    return False


def block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


def allow() -> None:
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)


def main() -> None:
    if PROJECT_DIR == "{" + "PROJECT_DIR" + "}":
        block("Guard not initialized — run /snowloop:init first.")
        return

    try:
        raw = sys.stdin.read()
        event = json.loads(raw)
    except (json.JSONDecodeError, IOError) as e:
        block(f"Failed to parse hook event: {e}")
        return

    tool_name = event.get("tool_name", "")
    if tool_name not in WRITE_TOOLS:
        allow()
        return

    tool_input = event.get("tool_input", {})
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
