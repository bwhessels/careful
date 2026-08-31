from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.careful_assessment import assess_findings, run_assessment


class AutonomousAssessmentTests(unittest.TestCase):
    def test_material_unknown_impact_is_flagged_and_escalated(self):
        result = assess_findings(
            {"status": "pass", "records": [], "errors": []},
            {"findings": [{"surface": "public-api", "classification": "unknown", "required": True, "summary": "API impact unknown", "source": "no reliable mapping"}]},
            "standard",
        )

        self.assertEqual(result["route"], "escalate-or-verify")
        self.assertEqual(result["user_flags"][0]["state"], "user-decision-needed")
        self.assertIn("API impact unknown", result["handoff"][0]["summary"])

    def test_satisfied_inferred_finding_does_not_interrupt_user(self):
        result = assess_findings(
            {"status": "pass", "records": [], "errors": []},
            {"findings": [{"surface": "documentation", "classification": "inferred", "required": False, "summary": "Docs may be affected", "source": "convention"}]},
            "standard",
        )

        self.assertEqual(result["route"], "continue")
        self.assertEqual(result["user_flags"], [])
        self.assertEqual(result["handoff"], [])

    def test_automatic_verification_does_not_interrupt_user(self):
        result = assess_findings(
            {"status": "pass", "records": [], "errors": []},
            {"findings": [{"surface": "codex-adapter", "classification": "verified", "required": True, "summary": "Adapter changed", "source": "manifest"}]},
            "standard",
        )

        self.assertEqual(result["route"], "escalate-or-verify")
        self.assertEqual(result["user_flags"], [])

    def test_ledger_statuses_are_carried_into_assessment(self):
        result = assess_findings(
            {"status": "pass", "records": [
                {"id": "stale-claim", "classification": "Verified", "status": "stale", "claim": "old"},
                {"id": "unknown-claim", "classification": "Unknown", "status": "current", "claim": "unknown", "reason": "missing"},
            ], "errors": []},
            {"findings": []},
            "standard",
        )

        states = {item["id"]: item["state"] for item in result["findings"]}
        self.assertEqual(states["stale-claim"], "stale")
        self.assertEqual(states["unknown-claim"], "user-decision-needed")
        self.assertEqual(len(result["user_flags"]), 2)

    def test_run_assessment_reads_configured_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "careful.project.yaml").write_text(
                "assessment:\n  ledger: evidence.json\n"
            )
            (root / "evidence.json").write_text(json.dumps({"records": []}))

            result = run_assessment(root, "quick", ["src/unknown.yaml"])

        self.assertEqual(result["ledger"]["status"], "pass")
        self.assertEqual(result["depth"], "quick")
        self.assertIn("hygiene", result)


if __name__ == "__main__":
    unittest.main()
