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
        self.codex_config = self.root / "config.toml"
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
                "--codex-config",
                str(self.codex_config),
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
        registration = self.codex_config.read_text()
        self.assertIn("[agents.reader_default]", registration)
        self.assertIn('config_file = "./agents/reader_default.toml"', registration)
        self.assertIn("[agents.reader_fast]", registration)

    def test_is_idempotent_for_matching_files(self):
        self.assertEqual(self.run_installer().returncode, 0)
        self.assertEqual(self.run_installer().returncode, 0)

    def test_refuses_to_overwrite_different_role(self):
        self.output.mkdir(parents=True)
        (self.output / "reader_default.toml").write_text("user configuration\n")
        result = self.run_installer()
        self.assertEqual(result.returncode, 2)
        self.assertIn("refusing to overwrite", result.stderr)

    def test_preserves_unrelated_config_and_updates_managed_block(self):
        self.codex_config.write_text('model = "gpt-5.6-sol"\n')
        self.assertEqual(self.run_installer().returncode, 0)
        self.assertEqual(self.run_installer().returncode, 0)
        result = self.codex_config.read_text()
        self.assertIn('model = "gpt-5.6-sol"', result)
        self.assertEqual(result.count("BEGIN bulk-read-routing"), 1)

    def test_refuses_unmanaged_registration(self):
        self.codex_config.write_text("[agents.reader_default]\n")
        result = self.run_installer()
        self.assertEqual(result.returncode, 2)
        self.assertIn("unmanaged agent registration", result.stderr)


if __name__ == "__main__":
    unittest.main()
