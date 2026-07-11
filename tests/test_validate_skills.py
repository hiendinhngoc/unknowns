from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_skills", ROOT / "scripts/validate_skills.py")
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class FrontmatterTest(unittest.TestCase):
    def test_parses_supported_scalar_metadata(self) -> None:
        meta, body = VALIDATOR.parse_frontmatter(
            "---\nname: test\ndescription: Use for tests\nversion: 1.0.0\nauthor: A\nlicense: MIT\n---\nBody\n"
        )
        self.assertEqual("test", meta["name"])
        self.assertEqual("Body\n", body)

    def test_rejects_duplicate_keys(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate"):
            VALIDATOR.parse_frontmatter("---\nname: one\nname: two\n---\nBody\n")

    def test_rejects_malformed_or_unknown_metadata(self) -> None:
        for text in (
            "---\n name: indented\n---\nBody\n",
            "---\nname: test\nextra: value\n---\nBody\n",
            "---\nname\n---\nBody\n",
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                VALIDATOR.parse_frontmatter(text)


class RepositoryValidationTest(unittest.TestCase):
    def copy_fixture(self, destination: Path) -> None:
        shutil.copytree(ROOT / ".claude-plugin", destination / ".claude-plugin")
        shutil.copytree(ROOT / "skills", destination / "skills")
        shutil.copy2(ROOT / "README.md", destination / "README.md")

    def test_current_repository_is_valid(self) -> None:
        self.assertEqual([], VALIDATOR.validate(ROOT))

    def test_empty_repository_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            errors = VALIDATOR.validate(Path(temp))
        self.assertTrue(any("at least one skill" in error for error in errors))

    def test_empty_manifests_do_not_bypass_schema_checks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.copy_fixture(root)
            (root / ".claude-plugin/plugin.json").write_text("{}")
            (root / ".claude-plugin/marketplace.json").write_text("{}")
            errors = VALIDATOR.validate(root)
        self.assertTrue(any("name must be a string" in error for error in errors))
        self.assertTrue(any("plugins must contain" in error for error in errors))

    def test_bad_ui_metadata_encoding_is_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.copy_fixture(root)
            (root / "skills/blindspot/agents/openai.yaml").write_bytes(b"\xff")
            errors = VALIDATOR.validate(root)
        self.assertTrue(any("cannot read UTF-8" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
