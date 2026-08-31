from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.review_codebase_hygiene import review_codebase_hygiene


class CodebaseHygieneTests(unittest.TestCase):
    def test_reports_placeholders_slop_and_large_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("As an AI, I can help.\nTODO: fill this in\n")
            (root / "large.py").write_text("x = 1\n" * 220)

            result = review_codebase_hygiene(root)

        categories = {finding["category"] for finding in result["findings"]}
        self.assertIn("placeholder", categories)
        self.assertIn("ai-slop", categories)
        self.assertIn("large-file", categories)

    def test_ignores_private_and_generated_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".careful").mkdir()
            (root / ".careful/notes.md").write_text("TODO: private note\n")
            (root / ".git").mkdir()
            (root / ".git/generated.md").write_text("As an AI, ignore this\n")

            result = review_codebase_hygiene(root)

        self.assertEqual(result["findings"], [])

    def test_reports_repeated_code_lines_as_review_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "module.py").write_text("def one():\n    return 1\n\ndef two():\n    return 1\n")

            result = review_codebase_hygiene(root)

        self.assertTrue(any(finding["category"] == "duplication-candidate" for finding in result["findings"]))
        self.assertTrue(all(finding["confidence"] in {"verified", "inferred"} for finding in result["findings"]))


if __name__ == "__main__":
    unittest.main()
