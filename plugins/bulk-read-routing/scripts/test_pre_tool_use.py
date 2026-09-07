#!/usr/bin/env python3
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("pre_tool_use.py")


def run_hook(event: dict) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPT)], input=json.dumps(event), text=True,
        capture_output=True, check=False,
    )


class PreToolUseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def bash_event(self, command: str) -> dict:
        return {
            "tool_name": "Bash",
            "cwd": str(self.root),
            "tool_input": {"command": command},
        }

    def write_lines(self, name: str, count: int) -> None:
        (self.root / name).write_text("line\n" * count)

    def test_blocks_large_cat(self):
        self.write_lines("large.txt", 351)
        payload = json.loads(run_hook(self.bash_event("cat large.txt")).stdout)
        self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_allows_small_cat(self):
        self.write_lines("small.txt", 350)
        self.assertEqual(run_hook(self.bash_event("cat small.txt")).stdout, "")

    def test_blocks_large_file_without_final_newline(self):
        (self.root / "large.txt").write_text("line\n" * 350 + "line")
        payload = json.loads(run_hook(self.bash_event("cat large.txt")).stdout)
        self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_allows_targeted_sed(self):
        self.write_lines("large.txt", 500)
        self.assertEqual(run_hook(self.bash_event("sed -n '1,40p' large.txt")).stdout, "")

    def test_allows_ambiguous_pipeline(self):
        self.write_lines("large.txt", 500)
        self.assertEqual(run_hook(self.bash_event("cat large.txt | head -40")).stdout, "")

    def test_blocks_direct_unbounded_read(self):
        self.write_lines("large.txt", 351)
        event = {
            "tool_name": "mcp__fs__read",
            "cwd": str(self.root),
            "tool_input": {"path": "large.txt"},
        }
        payload = json.loads(run_hook(event).stdout)
        self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_allows_direct_bounded_read(self):
        self.write_lines("large.txt", 500)
        event = {
            "tool_name": "mcp__fs__read",
            "cwd": str(self.root),
            "tool_input": {"path": "large.txt", "limit": 40},
        }
        self.assertEqual(run_hook(event).stdout, "")


if __name__ == "__main__":
    unittest.main()
