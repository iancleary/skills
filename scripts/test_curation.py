import shutil
import tempfile
import unittest
from pathlib import Path
from check_curation import check

ROOT = Path(__file__).resolve().parents[1]


class CurationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copy(ROOT / "curation.toml", self.root)
        for package in ROOT.rglob("SKILL.md"):
            if ".git" not in package.parts:
                target = self.root / package.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(package, target)

    def test_current_packages_pass(self):
        check(self.root)

    def test_invalid_frontmatter_rejected(self):
        path = self.root / "skills/librarian/SKILL.md"
        path.write_text(path.read_text().replace("name: librarian", "extra: invalid\nname: librarian"))
        with self.assertRaisesRegex(ValueError, "only name and description"):
            check(self.root)

    def test_malformed_frontmatter_rejected(self):
        path = self.root / "skills/librarian/SKILL.md"
        for value in ["[unterminated", "'unterminated", "{invalid", "|", "true", "null", "123", "- item", "? item"]:
            with self.subTest(value=value):
                path.write_text(f"---\nname: librarian\ndescription: {value}\n---\n")
                with self.assertRaises(ValueError):
                    check(self.root)
        path.write_text("---\nname: librarian\n description: indented\n---\n")
        with self.assertRaises(ValueError):
            check(self.root)
        path.write_text("---\nname: librarian\ndescription: valid\n---not-a-delimiter\n")
        with self.assertRaises(ValueError):
            check(self.root)

    def test_malformed_ownership_rejected(self):
        path = self.root / "curation.toml"
        original = path.read_text()
        for policy in [original.replace('cut-release = "iancleary/release-skills"', ''),
                       original.replace('cut-release = "iancleary/release-skills"', 'cut-release = "wrong/owner"'),
                       original.replace('active = [', 'active = ["skills/cut-release", '),
                       original.replace('retired = [', 'retired = ["cut-release", ')]:
            with self.subTest(policy=policy):
                path.write_text(policy)
                with self.assertRaises(ValueError):
                    check(self.root)
        path.write_text(original)

    def test_retired_and_moved_packages_rejected(self):
        for name in ["codegraph", "cut-release", "release-runner", "create-release-process"]:
            with self.subTest(name=name):
                path = self.root / "skills" / name / "SKILL.md"
                path.parent.mkdir()
                path.write_text(f"---\nname: {name}\ndescription: Use when testing ownership.\n---\n")
                with self.assertRaisesRegex(ValueError, "retired or moved"):
                    check(self.root)
                shutil.rmtree(path.parent)

    def test_duplicate_plugin_package_rejected(self):
        source = self.root / "skills/librarian/SKILL.md"
        target = self.root / "plugins/duplicate/skills/librarian/SKILL.md"
        target.parent.mkdir(parents=True)
        shutil.copy(source, target)
        with self.assertRaisesRegex(ValueError, "duplicate package name"):
            check(self.root)

    def test_missing_active_package_rejected(self):
        (self.root / "skills/librarian/SKILL.md").unlink()
        with self.assertRaisesRegex(ValueError, "inventory drift"):
            check(self.root)


if __name__ == "__main__":
    unittest.main()
