#!/usr/bin/env python3
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("install_agent_roles.py")


class InstallAgentRolesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.output = self.root / "agents"
        self.config = self.root / "roles.json"
        self.config.write_text(
            json.dumps(
                {
                    "roles": [
                        {
                            "name": "reader_default",
                            "description": "Default reader.",
                            "model": "gpt-5.6-terra",
                            "modelReasoningEffort": "medium",
                            "serviceTier": "default",
                        },
                        {
                            "name": "reader_fast",
                            "description": "Fast reader.",
                            "model": "gpt-5.6-terra",
                            "modelReasoningEffort": "high",
                            "serviceTier": "fast",
                        },
                    ]
                }
            )
        )

    def tearDown(self):
        self.temporary.cleanup()

    def run_installer(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "python3",
                str(SCRIPT),
                "--config",
                str(self.config),
                "--output-dir",
                str(self.output),
                *extra,
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_installs_default_and_fast_roles(self):
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        default = (self.output / "reader_default.toml").read_text()
        fast = (self.output / "reader_fast.toml").read_text()
        self.assertNotIn("service_tier", default)
        self.assertIn('service_tier = "fast"', fast)
        self.assertIn('model_reasoning_effort = "high"', fast)
        self.assertIn('sandbox_mode = "read-only"', fast)

    def test_is_idempotent_for_matching_files(self):
        self.assertEqual(self.run_installer().returncode, 0)
        self.assertEqual(self.run_installer().returncode, 0)

    def test_refuses_to_overwrite_different_role(self):
        self.output.mkdir(parents=True)
        (self.output / "reader_default.toml").write_text("user configuration\n")
        result = self.run_installer()
        self.assertEqual(result.returncode, 2)
        self.assertIn("refusing to overwrite", result.stderr)


if __name__ == "__main__":
    unittest.main()
