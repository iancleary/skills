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
        "denies it, call the collaboration spawn_agent tool with agent_type "
        "bulk_reader_fast and ask it to identify PPS-related definitions with file line "
        "references. Do not call wait until spawn_agent returns a receiver agent ID. If "
        "that spawn or task fails, call spawn_agent with agent_type explorer for the same "
        "task. Do not perform the analysis yourself. Spot-check only the returned range. End "
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
    role_named = "bulk_reader_fast" in json.dumps(delegated) or "explorer" in json.dumps(delegated)
    passed = blocked and bool(delegated) and role_named and final.startswith("DELEGATED:") and final.endswith(":PASS")
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
