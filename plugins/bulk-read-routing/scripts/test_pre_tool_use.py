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

    def bash_event(self, command: str, model: str = "gpt-5.5") -> dict:
        return {
            "model": model,
            "tool_name": "Bash",
            "cwd": str(self.root),
            "tool_input": {"command": command},
        }

    def exec_command_event(self, command: str, tool_name: str = "exec_command") -> dict:
        return {
            "tool_name": tool_name,
            "cwd": str(self.root),
            "tool_input": {"cmd": command},
        }

    def functions_exec_event(self, code, tool_name: str = "functions.exec") -> dict:
        return {
            "tool_name": tool_name,
            "cwd": str(self.root),
            "tool_input": code,
        }

    def write_lines(self, name: str, count: int) -> None:
        (self.root / name).write_text("line\n" * count)

    def test_blocks_large_cat(self):
        self.write_lines("large.txt", 351)
        payload = json.loads(run_hook(self.bash_event("cat large.txt")).stdout)
        self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_planner_model_suggests_explorer_delegation(self):
        self.write_lines("large.txt", 351)
        payload = json.loads(
            run_hook(self.bash_event("cat large.txt", "gpt-6-astra")).stdout
        )
        reason = payload["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("planner tier", reason)
        self.assertIn("`bulk_reader_fast` role", reason)
        self.assertIn("spot-check", reason)
        self.assertIn("remain responsible", reason)
        self.assertIn("unavailable agents", reason)
        self.assertIn("inadequate result", reason)

    def test_sol_model_uses_planner_tier(self):
        self.write_lines("large.txt", 351)
        payload = json.loads(
            run_hook(self.bash_event("cat large.txt", "gpt-5.6-sol")).stdout
        )
        reason = payload["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("planner tier", reason)

    def test_efficient_model_prefers_bounded_read(self):
        self.write_lines("large.txt", 351)
        payload = json.loads(
            run_hook(self.bash_event("cat large.txt", "gpt-5.6-terra")).stdout
        )
        reason = payload["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("efficient tier", reason)
        self.assertIn("`bulk_reader` role", reason)
        self.assertIn("coordination cost", reason)
        self.assertIn("recovering from the delegation path", reason)

    def test_unknown_model_gets_neutral_guidance(self):
        self.write_lines("large.txt", 351)
        payload = json.loads(
            run_hook(self.bash_event("cat large.txt", "future-model")).stdout
        )
        reason = payload["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("no configured tier", reason)
        self.assertIn("`explorer` role", reason)
        self.assertIn("role is a recommendation", reason)

    def test_blocks_large_cat_from_exec_command(self):
        self.write_lines("large.txt", 351)
        payload = json.loads(
            run_hook(self.exec_command_event("cat large.txt")).stdout
        )
        self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_blocks_large_cat_from_namespaced_exec_command(self):
        self.write_lines("large.txt", 351)
        payload = json.loads(
            run_hook(
                self.exec_command_event(
                    "cat large.txt", tool_name="functions.exec_command"
                )
            ).stdout
        )
        self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_blocks_large_cat_nested_in_functions_exec(self):
        self.write_lines("large.txt", 351)
        code = (
            'const r = await tools.exec_command({cmd:"cat large.txt",'
            'workdir:"/tmp"}); text(r.output);'
        )
        payload = json.loads(run_hook(self.functions_exec_event(code)).stdout)
        self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_blocks_wrapped_functions_exec_input(self):
        self.write_lines("large.txt", 351)
        code = 'await tools.exec_command({cmd:"cat large.txt"});'
        payload = json.loads(
            run_hook(self.functions_exec_event({"code": code})).stdout
        )
        self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_blocks_double_underscore_functions_exec_name(self):
        self.write_lines("large.txt", 351)
        code = 'await tools.exec_command({cmd:"cat large.txt"});'
        payload = json.loads(
            run_hook(self.functions_exec_event(code, "functions__exec")).stdout
        )
        self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_allows_small_cat(self):
        self.write_lines("small.txt", 350)
        self.assertEqual(run_hook(self.bash_event("cat small.txt")).stdout, "")

    def test_blocks_unresolved_relative_cat(self):
        payload = json.loads(run_hook(self.bash_event("cat elsewhere.txt")).stdout)
        reason = payload["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("could not be sized", reason)

    def test_allows_missing_direct_read_to_report_its_own_error(self):
        event = {
            "tool_name": "mcp__fs__read",
            "cwd": str(self.root),
            "tool_input": {"path": "missing.txt"},
        }
        self.assertEqual(run_hook(event).stdout, "")

    def test_blocks_large_file_without_final_newline(self):
        (self.root / "large.txt").write_text("line\n" * 350 + "line")
        payload = json.loads(run_hook(self.bash_event("cat large.txt")).stdout)
        self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_allows_targeted_sed(self):
        self.write_lines("large.txt", 500)
        self.assertEqual(run_hook(self.bash_event("sed -n '1,40p' large.txt")).stdout, "")

    def test_allows_targeted_sed_from_exec_command(self):
        self.write_lines("large.txt", 500)
        result = run_hook(self.exec_command_event("sed -n '1,40p' large.txt"))
        self.assertEqual(result.stdout, "")

    def test_allows_targeted_sed_nested_in_functions_exec(self):
        self.write_lines("large.txt", 500)
        code = 'await tools.exec_command({cmd:"sed -n \'1,40p\' large.txt"});'
        result = run_hook(self.functions_exec_event(code))
        self.assertEqual(result.stdout, "")

    def test_ignores_dynamic_functions_exec_command(self):
        self.write_lines("large.txt", 500)
        code = "await tools.exec_command({cmd: commandFromUser});"
        result = run_hook(self.functions_exec_event(code))
        self.assertEqual(result.stdout, "")

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
