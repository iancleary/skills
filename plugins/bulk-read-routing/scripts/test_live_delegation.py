#!/usr/bin/env python3
"""Run an opt-in live test of hook-driven subagent delegation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-model", default="gpt-5.6-sol")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    target = root / "skills" / "schemdraw" / "examples" / "helpers" / "protocols.py"
    prompt = (
        f"Delegation integration test. First run exactly: cat {target}. After the hook "
        "denies it, delegate the broad read. The hook's recommended role is a starting "
        "point, but you are the driving agent: choose the role and recovery path. Ask the "
        "agent to identify PPS-related definitions with file line references. A failed "
        "attempt includes spawn errors, unavailable roles, tool errors, timeouts, malformed "
        "responses, and answers that fail the task. Retry, choose another role, or use "
        "bounded reads as appropriate. Do not claim delegation unless spawn_agent returns "
        "a receiver agent ID and that agent returns evidence. Spot-check only the returned "
        "range. End "
        "with exactly DELEGATED:<role>:PASS only after a subagent returns evidence; "
        "otherwise end DELEGATED:none:FAIL."
    )
    try:
        result = subprocess.run(
            [
                "codex", "exec", "--json", "--sandbox", "read-only",
                "-C", str(root), "-m", args.parent_model, prompt,
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=args.timeout,
        )
    except subprocess.TimeoutExpired:
        print("live delegation test timed out", file=sys.stderr)
        return 2

    events = []
    for line in result.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    blocked = "Command blocked by PreToolUse hook" in result.stderr
    collab_items = [
        event.get("item", {}) for event in events
        if event.get("type", "").startswith("item.")
        and event.get("item", {}).get("type") == "collab_tool_call"
    ]
    delegated = [item for item in collab_items if item.get("receiver_thread_ids")]
    final_messages = [
        event.get("item", {}).get("text", "") for event in events
        if event.get("type") == "item.completed"
        and event.get("item", {}).get("type") == "agent_message"
    ]
    final = final_messages[-1] if final_messages else ""
    final_parts = final.split(":")
    final_shape_valid = len(final_parts) == 3
    final_role = final_parts[1] if final_shape_valid else ""
    role_named = bool(final_role) and final_role in json.dumps(delegated)
    passed = (
        blocked
        and bool(delegated)
        and role_named
        and final_shape_valid
        and final_parts[0] == "DELEGATED"
        and final_parts[2] == "PASS"
    )
    if not passed:
        print(
            json.dumps(
                {
                    "blocked": blocked,
                    "delegatedCalls": len(delegated),
                    "roleNamedInEvents": role_named,
                    "final": final,
                    "stderrTail": result.stderr.splitlines()[-5:],
                },
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1
    print(final)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
