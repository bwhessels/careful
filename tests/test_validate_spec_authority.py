from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_spec_authority import (
    find_specification_conflicts,
    parse_documentation_profile,
    validate_spec_authority,
)


class ValidateSpecAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directories: list[tempfile.TemporaryDirectory[str]] = []

    def tearDown(self) -> None:
        for temporary_directory in self.temporary_directories:
            temporary_directory.cleanup()

    def fixture(self, documentation: str) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.temporary_directories.append(temporary_directory)
        root = Path(temporary_directory.name)
        (root / "careful.project.yaml").write_text(
            "version: 1\nproject:\n  name: fixture\n" + documentation
        )
        return root

    def test_parses_openspec_authority_and_execution_plans(self):
        root = self.fixture(
            "documentation:\n"
            "  specs: openspec/specs/\n"
            "  changes: openspec/changes/\n"
            "  spec_authority: openspec\n"
            "  execution_plans: docs/superpowers/plans/\n"
        )

        profile = parse_documentation_profile(root / "careful.project.yaml")

        self.assertEqual(profile["spec_authority"], "openspec")
        self.assertEqual(profile["execution_plans"], "docs/superpowers/plans/")

    def test_distinguishes_project_defined_none_and_unknown_authority(self):
        for declaration, expected in (
            ("  spec_authority: project-defined\n", "project-defined"),
            ("  spec_authority: none\n", "none"),
            ("", "unknown"),
        ):
            with self.subTest(expected=expected):
                root = self.fixture("documentation:\n" + declaration)
                self.assertEqual(
                    parse_documentation_profile(root / "careful.project.yaml")["spec_authority"],
                    expected,
                )

    def test_rejects_unsupported_authority(self):
        root = self.fixture("documentation:\n  spec_authority: invented\n")

        self.assertEqual(
            validate_spec_authority(root),
            ["unsupported documentation.spec_authority: invented"],
        )

    def test_reports_durable_competing_specification_without_mutating_it(self):
        root = self.fixture("documentation:\n  spec_authority: openspec\n")
        competing = root / "docs" / "superpowers" / "specs" / "design.md"
        competing.parent.mkdir(parents=True)
        competing.write_text("# Design\n\n## Goals\n\n- Keep one source of truth.\n")

        errors = find_specification_conflicts(
            root,
            parse_documentation_profile(root / "careful.project.yaml"),
        )

        self.assertEqual(len(errors), 1)
        self.assertIn("docs/superpowers/specs/design.md", errors[0])
        self.assertTrue(competing.exists())

    def test_ignores_pointer_historical_and_execution_plan_documents(self):
        root = self.fixture(
            "documentation:\n"
            "  spec_authority: openspec\n"
            "  execution_plans: docs/superpowers/plans/\n"
        )
        specs = root / "docs" / "superpowers" / "specs"
        specs.mkdir(parents=True)
        (specs / "pointer.md").write_text(
            "# Pointer\n\nThis is a pointer to `openspec/changes/example/design.md`.\n"
        )
        (specs / "historical.md").write_text(
            "# Historical\n\nStatus: historical\n\n## Goals\n\n- Old goal.\n"
        )
        plan = root / "docs" / "superpowers" / "plans" / "plan.md"
        plan.parent.mkdir(parents=True)
        plan.write_text("# Plan\n\nSpec: `openspec/changes/example/design.md`\n")

        self.assertEqual(
            find_specification_conflicts(
                root,
                parse_documentation_profile(root / "careful.project.yaml"),
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
