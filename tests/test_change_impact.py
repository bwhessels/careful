from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import subprocess

from scripts.careful_assessment import analyze_change_impact, collect_changed_paths


class ChangeImpactTests(unittest.TestCase):
    def project(self, assessment: str = "") -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        (root / "careful.project.yaml").write_text("version: 1\nproject:\n  name: fixture\n" + assessment)
        (root / "core").mkdir()
        (root / "core/adapter-manifest.yaml").write_text(
            "version: 1\ncore_policy: core/policy.md\nsupported_adapters:\n"
            "  codex:\n    distribution: plugins/careful/\n"
        )
        return root

    def test_maps_canonical_surfaces_as_verified(self):
        root = self.project()

        result = analyze_change_impact(root, ["plugins/careful/skills/careful-workflow/SKILL.md", "README.md"])

        surfaces = {item["surface"] for item in result["findings"]}
        self.assertIn("codex-adapter", surfaces)
        self.assertIn("public-documentation", surfaces)
        self.assertTrue(all(item["classification"] == "verified" for item in result["findings"]))

    def test_honors_explicit_mapping_and_required_flag(self):
        root = self.project(
            "assessment:\n"
            "  mappings:\n"
            "    - pattern: src/api/\n"
            "      surface: public-api\n"
            "      required: true\n"
        )

        result = analyze_change_impact(root, ["src/api/users.py"])

        self.assertEqual(result["findings"], [
            {
                "surface": "public-api",
                "classification": "verified",
                "paths": ["src/api/users.py"],
                "source": "careful.project.yaml assessment.mappings",
                "required": True,
                "summary": "explicit project mapping",
            }
        ])

    def test_unknown_content_is_not_claimed_unaffected(self):
        root = self.project()

        result = analyze_change_impact(root, ["src/unknown.txt"])
        self.assertEqual(result["findings"][0]["classification"], "unknown")
        result = analyze_change_impact(root, ["src/unknown.yaml"])
        self.assertEqual(result["findings"][0]["classification"], "unknown")

    def test_changed_paths_are_sorted_and_git_failure_is_explicit(self):
        root = self.project()
        changed, errors = collect_changed_paths(root)

        self.assertEqual(changed, [])
        self.assertTrue(errors)

        result = analyze_change_impact(root, ["README.md", "openspec/specs/a.md", "README.md"])
        self.assertEqual(result["changed_paths"], ["README.md", "openspec/specs/a.md"])

    def test_clean_input_does_not_create_missing_required_surface_findings(self):
        root = self.project(
            "assessment:\n"
            "  required_surfaces:\n"
            "    - public-documentation\n"
        )

        result = analyze_change_impact(root, [])

        self.assertEqual(result["findings"], [])

    def test_collects_untracked_paths_from_git_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "new.py").write_text("print('new')\n")

            changed, errors = collect_changed_paths(root)

        self.assertEqual(changed, ["new.py"])
        self.assertEqual(errors, [])

    def test_unmapped_source_files_are_unknown(self):
        root = self.project()

        result = analyze_change_impact(root, ["src/internal.py"])

        self.assertEqual(result["findings"][0]["classification"], "unknown")


if __name__ == "__main__":
    unittest.main()
