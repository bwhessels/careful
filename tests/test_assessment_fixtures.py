from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.careful_assessment import analyze_change_impact, run_assessment, validate_evidence_ledger


class AssessmentFixtureTests(unittest.TestCase):
    root = Path(__file__).resolve().parents[1] / "fixtures" / "adopted-project"

    def test_consumer_ledger_exercises_current_stale_and_unknown_records(self):
        result = validate_evidence_ledger(self.root)

        self.assertEqual(result["status"], "pass")
        self.assertEqual(len(result["records"]), 3)

    def test_consumer_impact_fixture_identifies_public_documentation(self):
        fixture = json.loads((self.root / "assessment-fixture.json").read_text())
        result = analyze_change_impact(self.root, fixture["changed_paths"])

        self.assertIn("public-documentation", {item["surface"] for item in result["findings"]})

    def test_consumer_assessment_flags_only_material_findings(self):
        result = run_assessment(self.root, "standard", ["README.md"])

        self.assertEqual(result["route"], "escalate-or-verify")
        self.assertTrue(result["user_flags"])


if __name__ == "__main__":
    unittest.main()
