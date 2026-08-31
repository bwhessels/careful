from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_public_readiness import parse_public_readiness, validate_public_readiness


class ValidatePublicReadinessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directories: list[tempfile.TemporaryDirectory[str]] = []

    def tearDown(self) -> None:
        for temporary_directory in self.temporary_directories:
            temporary_directory.cleanup()

    def fixture(self, readiness: str) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.temporary_directories.append(temporary_directory)
        root = Path(temporary_directory.name)
        (root / "careful.project.yaml").write_text(
            "version: 1\nproject:\n  name: fixture\n" + readiness
        )
        return root

    def test_parses_public_intended_documents_checks_and_gates(self):
        root = self.fixture(
            "public_readiness:\n"
            "  audience: public-intended\n"
            "  required_documents:\n"
            "    - README.md\n"
            "    - LICENSE\n"
            "  checks:\n"
            "    - npm run docs:check\n"
            "  gates:\n"
            "    first_publication: independent-review\n"
        )

        profile = parse_public_readiness(root / "careful.project.yaml")

        self.assertEqual(profile["audience"], "public-intended")
        self.assertEqual(profile["required_documents"], ["README.md", "LICENSE"])
        self.assertEqual(profile["checks"], ["npm run docs:check"])
        self.assertEqual(profile["gates"]["first_publication"], "independent-review")

    def test_reports_missing_required_documents(self):
        root = self.fixture(
            "public_readiness:\n"
            "  audience: public\n"
            "  required_documents:\n"
            "    - README.md\n"
            "    - LICENSE\n"
        )
        (root / "README.md").write_text("# Fixture\n")

        result = validate_public_readiness(root)

        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["mode"], "public")
        self.assertEqual(result["checked_documents"], ["README.md"])
        self.assertEqual(result["failed_checks"], ["missing required document: LICENSE"])

    def test_accepts_existing_documents_and_returns_standard_result_shape(self):
        root = self.fixture(
            "public_readiness:\n"
            "  audience: internal\n"
            "  required_documents:\n"
            "    - README.md\n"
        )
        (root / "README.md").write_text("# Fixture\n")

        result = validate_public_readiness(root)

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["mode"], "internal")
        self.assertEqual(result["checked_documents"], ["README.md"])
        self.assertEqual(result["failed_checks"], [])
        self.assertIn("required-documents", result["evidence"])

    def test_rejects_invalid_audience(self):
        root = self.fixture("public_readiness:\n  audience: everyone\n")

        result = validate_public_readiness(root)

        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["failed_checks"], ["unsupported public_readiness.audience: everyone"])

    def test_careful_declares_lightweight_public_readiness_without_security_document(self):
        repository_root = Path(__file__).resolve().parents[1]

        profile = parse_public_readiness(repository_root / "careful.project.yaml")
        result = validate_public_readiness(repository_root)

        self.assertEqual(profile["audience"], "public-intended")
        self.assertEqual(profile["required_documents"], ["README.md", "LICENSE"])
        self.assertNotIn("SECURITY.md", profile["required_documents"])
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["failed_checks"], [])


if __name__ == "__main__":
    unittest.main()
