from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.careful_assessment import (
    AssessmentFinding,
    EvidenceRecord,
    EvidenceReference,
    assessment_state_for,
    load_project_assessment_config,
)


class CarefulAssessmentTests(unittest.TestCase):
    def test_reads_optional_assessment_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = Path(directory) / "careful.project.yaml"
            profile.write_text(
                "assessment:\n"
                "  ledger: evidence/ledger.json\n"
                "  fail_on_unknown: true\n"
                "  required_surfaces:\n"
                "    - public-documentation\n"
            )

            result = load_project_assessment_config(profile)

        self.assertEqual(result["ledger"], "evidence/ledger.json")
        self.assertTrue(result["fail_on_unknown"])
        self.assertEqual(result["required_surfaces"], ["public-documentation"])

    def test_selects_actionable_assessment_states(self):
        self.assertEqual(assessment_state_for(satisfied=True), "satisfied")
        self.assertEqual(assessment_state_for(stale=True), "stale")
        self.assertEqual(assessment_state_for(contradiction=True), "contradiction")
        self.assertEqual(assessment_state_for(user_action=True), "user-decision-needed")
        self.assertEqual(assessment_state_for(material=True), "needs-verification")

    def test_records_are_json_serializable(self):
        evidence = EvidenceRecord(
            id="claim-1",
            claim="The fixture passes.",
            classification="Verified",
            evidence=[EvidenceReference(kind="test", ref="tests/test.py")],
        )
        finding = AssessmentFinding(
            id="claim-1",
            state="satisfied",
            material=False,
            summary="Evidence is current.",
        )

        encoded = json.dumps({"record": evidence.to_dict(), "finding": finding.to_dict()})

        self.assertIn('"classification": "Verified"', encoded)
        self.assertIn('"state": "satisfied"', encoded)


if __name__ == "__main__":
    unittest.main()
