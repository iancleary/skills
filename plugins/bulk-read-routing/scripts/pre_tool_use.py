#!/usr/bin/env python3
"""Block recognizable full-file reads above a configurable line threshold."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import sys
from typing import Any


DEFAULT_THRESHOLD = 350
FULL_READ_COMMANDS = {"cat", "less", "more"}


def threshold() -> int:
    try:
        value = int(os.environ.get("BULK_READ_LINE_THRESHOLD", DEFAULT_THRESHOLD))
    except ValueError:
        return DEFAULT_THRESHOLD
    return value if value > 0 else DEFAULT_THRESHOLD


def line_count_exceeds(path: Path, limit: int) -> bool:
    try:
        with path.open("rb") as handle:
            count = 0
            saw_data = False
            last_byte = b""
            while chunk := handle.read(64 * 1024):
                saw_data = True
                last_byte = chunk[-1:]
                count += chunk.count(b"\n")
                if count > limit:
                    return True
            if saw_data and last_byte != b"\n":
                count += 1
            return count > limit
    except OSError:
        return False


def resolve_path(value: Any, cwd: Path) -> Path | None:
    if not isinstance(value, str) or not value or value == "-":
        return None
    path = Path(value).expanduser()
    return path if path.is_absolute() else cwd / path


def shell_read_paths(command: str, cwd: Path) -> list[Path]:
    try:
        words = shlex.split(command)
    except ValueError:
        return []
    shell_operators = {"|", "||", "&&", ";", ">", ">>"}
    if not words or any(word in shell_operators for word in words):
        return []
    if Path(words[0]).name not in FULL_READ_COMMANDS:
        return []
    paths = (
        resolve_path(word, cwd) for word in words[1:] if not word.startswith("-")
    )
    return [path for path in paths if path is not None]


def direct_read_path(event: dict[str, Any], cwd: Path) -> Path | None:
    tool_name = str(event.get("tool_name", "")).lower()
    tool_input = event.get("tool_input")
    if "read" not in tool_name or not isinstance(tool_input, dict):
        return None
    if isinstance(tool_input.get("limit"), int) and tool_input["limit"] > 0:
        return None
    return resolve_path(tool_input.get("file_path") or tool_input.get("path"), cwd)


def blocked_paths(event: dict[str, Any]) -> list[Path]:
    cwd = Path(str(event.get("cwd") or Path.cwd()))
    tool_name = str(event.get("tool_name", ""))
    tool_input = event.get("tool_input")
    candidates: list[Path] = []
    shell_input_key = None
    if tool_name == "Bash":
        shell_input_key = "command"
    elif tool_name.lower().split(".")[-1] == "exec_command":
        shell_input_key = "cmd"

    if shell_input_key is not None and isinstance(tool_input, dict):
        command = tool_input.get(shell_input_key)
        if isinstance(command, str):
            candidates.extend(shell_read_paths(command, cwd))
    else:
        path = direct_read_path(event, cwd)
        if path is not None:
            candidates.append(path)
    limit = threshold()
    return [path for path in candidates if path.is_file() and line_count_exceeds(path, limit)]


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError):
        return 0
    if not isinstance(event, dict):
        return 0
    paths = blocked_paths(event)
    if not paths:
        return 0
    names = ", ".join(str(path) for path in paths)
    reason = (
        f"Full-file read blocked above {threshold()} lines: {names}. "
        "Use rg and a bounded sed range, or delegate a concise summary with file and line references."
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
