"""Exercise the vendored runner without contacting a hosting provider."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReleaseContractTests(unittest.TestCase):
    def test_calver_contract_and_failed_check(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo = base / "repo"
            repo.mkdir()

            def run(*args, ok=True):
                result = subprocess.run(args, cwd=repo, capture_output=True, text=True)
                if ok:
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return result

            shutil.copytree(ROOT / "scripts", repo / "scripts")
            shutil.copytree(ROOT / "plugins", repo / "plugins")
            shutil.copy2(ROOT / "release.toml", repo / "release.toml")
            run("git", "init", "--bare", str(base / "origin.git"))
            run("git", "init", "-b", "main")
            run("git", "config", "user.name", "Release Test")
            run("git", "config", "user.email", "release@example.invalid")
            run("git", "remote", "add", "origin", str(base / "origin.git"))
            run("git", "add", ".")
            run("git", "commit", "-m", "fixture")
            run("git", "push", "origin", "main")
            run("git", "tag", "2026.09.01.0")
            prefix = ("uv", "run", "scripts/release.py")
            plan = json.loads(run(*prefix, "plan", "--json").stdout)
            self.assertEqual(plan["current_version"], "2026.09.01.0")
            self.assertIsNone(plan["ready"])
            self.assertFalse(plan["checks_verified"])
            self.assertRegex(plan["next_version"], r"^\d{4}\.\d{2}\.\d{2}\.\d+$")
            checks = json.loads(run(*prefix, "check", "--json").stdout)
            self.assertTrue(checks["ready"])
            result = json.loads(run(*prefix, "run", "--dry-run", "--version",
                                    plan["next_version"], "--expected-head", plan["target_commit"],
                                    "--expected-config", plan["config_sha256"], "--json").stdout)
            self.assertTrue(result["executed"])
            self.assertEqual(run("git", "status", "--porcelain").stdout, "")
            self.assertEqual(run("git", "tag", "--list").stdout.strip(), "2026.09.01.0")
            self.assertEqual(run("git", "ls-remote", "--tags", "origin").stdout, "")
            for version in ("1.2.3", "2026.02.30.0"):
                failure = run(*prefix, "run", "--dry-run", "--version", version, "--json", ok=False)
                self.assertNotEqual(failure.returncode, 0)
                self.assertIn("error", json.loads(failure.stdout))
            run("git", "switch", "-c", "wrong-branch")
            failure = run(*prefix, "run", "--dry-run", "--version",
                          plan["next_version"], "--json", ok=False)
            self.assertNotEqual(failure.returncode, 0)
            self.assertIn("main", json.loads(failure.stdout)["error"])


if __name__ == "__main__":
    unittest.main()
