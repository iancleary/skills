"""Verify real task and hook boundaries with unsupported ambient Python."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ManagedPythonTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="managed python ")
        self.addCleanup(self.tmp.cleanup)
        self.bin = Path(self.tmp.name)
        self.marker = self.bin / "ambient-used"
        for name in ["python", "python3"]:
            path = self.bin / name
            path.write_text(f"#!/bin/sh\ntouch '{self.marker}'\necho unsupported ambient Python >&2\nexit 99\n")
            path.chmod(0o755)
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ["PATH"],
                        PLUGIN_ROOT=str(ROOT / "plugins/bulk-read-routing"))
        self.env.pop("UV_PYTHON_PREFERENCE", None)
        self.just = shutil.which("just")
        self.assertIsNotNone(self.just)

    def test_real_managed_runtime_and_hook(self):
        # Prove the ambient fixture is unsupported before testing the boundaries.
        result = subprocess.run(["python3", "--version"], env=self.env, capture_output=True)
        self.assertEqual(result.returncode, 99)
        self.marker.unlink()
        for recipe in ["install-agent-roles", "test-live-delegation"]:
            result = subprocess.run([self.just, recipe, "--help"], cwd=ROOT,
                                    env=self.env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("usage:", result.stdout)
        result = subprocess.run(["uv", "run", "--no-project", "--managed-python",
                                 "--python", "3.11", "python", "scripts/release.py",
                                 "plan", "--json"], cwd=ROOT, env=self.env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["mode"], "plan")
        hooks = json.loads((ROOT / "plugins/bulk-read-routing/hooks/hooks.json").read_text())
        command = hooks["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        result = subprocess.run(command, shell=True, cwd=ROOT, env=self.env,
                                input="{}", capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.marker.exists())

    def test_literal_task_arguments(self):
        capture = self.bin / "argv.json"
        uv = self.bin / "uv"
        uv.write_text(f"#!{sys.executable}\nimport sys,json\nfrom pathlib import Path\nPath({str(capture)!r}).write_text(json.dumps(sys.argv[1:]))\n")
        uv.chmod(0o755)
        args = ["space path", "single'quote", 'double"quote', "$(touch injected)",
                "; touch injected", "`touch injected`", "", "line\nbreak"]
        for recipe, script in [("install-agent-roles", "install_agent_roles.py"),
                               ("test-live-delegation", "test_live_delegation.py")]:
            result = subprocess.run([self.just, recipe, *args], cwd=ROOT,
                                    env=self.env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(capture.read_text()),
                ["run", "--no-project", "--managed-python", "--python", "3.11", "python",
                 f"plugins/bulk-read-routing/scripts/{script}", *args])
        self.assertFalse((ROOT / "injected").exists())
        self.assertFalse(self.marker.exists())


if __name__ == "__main__":
    unittest.main()
