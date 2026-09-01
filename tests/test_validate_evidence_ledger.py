from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.careful_assessment import parse_evidence_ledger, validate_evidence_ledger


class EvidenceLedgerTests(unittest.TestCase):
    def write_project(self, ledger: object) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        (root / "careful.project.yaml").write_text(
            "version: 1\nproject:\n  name: fixture\n"
            "assessment:\n  ledger: evidence/ledger.json\n"
        )
        (root / "evidence").mkdir()
        (root / "evidence/ledger.json").write_text(json.dumps(ledger))
        return root

    def test_validates_verified_and_unknown_records(self):
        root = self.write_project(
            {
                "records": [
                    {
                        "id": "claim-1",
                        "claim": "Fixture passes",
                        "classification": "Verified",
                        "evidence": [{"kind": "fixture", "ref": "fixtures/adopted-project/codex"}],
                    },
                    {
                        "id": "claim-2",
                        "claim": "Claude session is fresh",
                        "classification": "Unknown",
                        "reason": "No authenticated session evidence",
                        "evidence": [],
                    },
                ]
            }
        )

        result = validate_evidence_ledger(root)

        self.assertEqual(result["status"], "pass")
        self.assertEqual([record.id for record in parse_evidence_ledger(root / "evidence/ledger.json")], ["claim-1", "claim-2"])

    def test_reports_duplicate_missing_and_unsupported_records(self):
        root = self.write_project(
            {
                "records": [
                    {"id": "duplicate", "claim": "one", "classification": "Verified", "evidence": []},
                    {"id": "duplicate", "claim": "two", "classification": "Nope", "evidence": [{"kind": "bogus", "ref": "x"}]},
                ]
            }
        )

        result = validate_evidence_ledger(root)

        self.assertEqual(result["status"], "fail")
        self.assertIn("duplicate: duplicate id", result["errors"])
        self.assertIn("duplicate: unsupported classification: Nope", result["errors"])
        self.assertIn("duplicate: unsupported evidence kind: bogus", result["errors"])
        self.assertIn("duplicate: evidence is required for Verified", result["errors"])

    def test_rejects_private_ledger_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "careful.project.yaml").write_text(
                "assessment:\n  ledger: .careful/ledger.json\n"
            )

            result = validate_evidence_ledger(root)

        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["errors"], ["ledger must not be under .careful/"])

    def test_unconfigured_ledger_is_advisory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = validate_evidence_ledger(root)

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["warnings"], ["ledger is not configured"])

    def test_rejects_ledger_outside_project_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = Path(directory).parent / (root.name + "-outside.json")
            outside.write_text(json.dumps({"records": []}))
            (root / "careful.project.yaml").write_text(
                "assessment:\n  ledger: ../" + outside.name + "\n"
            )

            result = validate_evidence_ledger(root)
            outside.unlink()

        self.assertEqual(result["status"], "fail")
        self.assertIn("ledger must remain inside project root", result["errors"])


if __name__ == "__main__":
    unittest.main()
