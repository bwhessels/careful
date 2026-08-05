from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from validate_self_hosting import (  # noqa: E402
    validate_deep_change_contract,
    validate_installed_codex_plugin,
)


FIELDS = (
    "Bootstrap and discovery:",
    "Consumer path and reference resolution:",
    "Cloneable source and immutable version:",
    "Interactive, dry-run, and non-interactive defaults:",
    "Tracked, ignored, local, and private state:",
    "Upgrade, repair, migration, rollback, and destructive boundaries:",
)


class ValidateDeepChangeContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directories: list[tempfile.TemporaryDirectory[str]] = []

    def tearDown(self) -> None:
        for temporary_directory in self.temporary_directories:
            temporary_directory.cleanup()

    def fixture(self) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.temporary_directories.append(temporary_directory)
        root = Path(temporary_directory.name)
        for relative in (
            "core/policy.md",
            "core/deep-change-checklist.md",
            "examples/openspec-schemas/critical-deep/templates/design.md",
            "plugins/careful",
            "adapters/claude-code/.claude/skills/careful-workflow/SKILL.md",
            "adapters/factory-droid/.factory/skills/careful-workflow/SKILL.md",
        ):
            source = ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)
        return root

    def mutate(self, root: Path, relative: str, old: str, new: str = "") -> None:
        path = root / relative
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))

    def test_current_contract_and_installed_plugin_bundle_are_complete(self):
        self.assertEqual(validate_deep_change_contract(self.fixture()), [])

        temporary_directory = tempfile.TemporaryDirectory()
        self.temporary_directories.append(temporary_directory)
        installed_plugin = Path(temporary_directory.name) / "cache" / "careful" / "0.2.0"
        shutil.copytree(ROOT / "plugins" / "careful", installed_plugin)
        self.assertEqual(validate_installed_codex_plugin(installed_plugin), [])

    def test_installed_plugin_rejects_source_tree_only_reference(self):
        temporary_directory = tempfile.TemporaryDirectory()
        self.temporary_directories.append(temporary_directory)
        installed_plugin = Path(temporary_directory.name) / "cache" / "careful" / "0.2.0"
        shutil.copytree(ROOT / "plugins" / "careful", installed_plugin)
        workflow = installed_plugin / "skills" / "careful-workflow" / "SKILL.md"
        workflow.write_text(
            workflow.read_text().replace(
                "references/deep-change-checklist.md",
                "../../../../core/deep-change-checklist.md",
            )
        )
        errors = validate_installed_codex_plugin(installed_plugin)
        self.assertIn(
            "Codex workflow missing install-resolvable reference references/deep-change-checklist.md",
            errors,
        )

    def test_installed_plugin_requires_markdown_link_destinations(self):
        original = "[portable Deep change checklist](references/deep-change-checklist.md)"
        for replacement in (
            "references/deep-change-checklist.md",
            "`references/deep-change-checklist.md`",
            "`[portable Deep change checklist](references/deep-change-checklist.md)`",
            "\n```markdown\n[portable Deep change checklist](references/deep-change-checklist.md)\n```\n",
            "\n~~~markdown\n[portable Deep change checklist](references/deep-change-checklist.md)\n~~~\n",
            "\n    [portable Deep change checklist](references/deep-change-checklist.md)\n",
            "\\[portable Deep change checklist](references/deep-change-checklist.md)",
            "![portable Deep change checklist](references/deep-change-checklist.md)",
        ):
            with self.subTest(replacement=replacement):
                temporary_directory = tempfile.TemporaryDirectory()
                self.temporary_directories.append(temporary_directory)
                installed_plugin = Path(temporary_directory.name) / "cache" / "careful" / "0.2.0"
                shutil.copytree(ROOT / "plugins" / "careful", installed_plugin)
                workflow = installed_plugin / "skills" / "careful-workflow" / "SKILL.md"
                workflow_text = workflow.read_text()
                self.assertIn(original, workflow_text)
                workflow.write_text(workflow_text.replace(original, replacement, 1))

                self.assertIn(
                    "Codex workflow missing install-resolvable reference references/deep-change-checklist.md",
                    validate_installed_codex_plugin(installed_plugin),
                )

    def test_installed_plugin_does_not_close_fences_with_non_whitespace_suffixes(self):
        original = "[portable Deep change checklist](references/deep-change-checklist.md)"
        for marker in ("```", "~~~"):
            with self.subTest(marker=marker):
                temporary_directory = tempfile.TemporaryDirectory()
                self.temporary_directories.append(temporary_directory)
                installed_plugin = Path(temporary_directory.name) / "cache" / "careful" / "0.2.0"
                shutil.copytree(ROOT / "plugins" / "careful", installed_plugin)
                workflow = installed_plugin / "skills" / "careful-workflow" / "SKILL.md"
                workflow_text = workflow.read_text()
                replacement = (
                    f"\n{marker}markdown\n"
                    f"{marker}not-a-closing-fence\n"
                    f"{original}\n"
                )
                workflow.write_text(workflow_text.replace(original, replacement, 1))

                self.assertIn(
                    "Codex workflow missing install-resolvable reference references/deep-change-checklist.md",
                    validate_installed_codex_plugin(installed_plugin),
                )

    def test_installed_plugin_uses_tab_stops_for_indented_code(self):
        original = "[portable Deep change checklist](references/deep-change-checklist.md)"
        for indentation in ("   \t", " \t"):
            with self.subTest(indentation=repr(indentation)):
                temporary_directory = tempfile.TemporaryDirectory()
                self.temporary_directories.append(temporary_directory)
                installed_plugin = Path(temporary_directory.name) / "cache" / "careful" / "0.2.0"
                shutil.copytree(ROOT / "plugins" / "careful", installed_plugin)
                workflow = installed_plugin / "skills" / "careful-workflow" / "SKILL.md"
                workflow_text = workflow.read_text()
                workflow.write_text(
                    workflow_text.replace(original, f"\n{indentation}{original}\n", 1)
                )

                self.assertIn(
                    "Codex workflow missing install-resolvable reference references/deep-change-checklist.md",
                    validate_installed_codex_plugin(installed_plugin),
                )

    def test_installed_plugin_accepts_links_after_valid_fence_closers(self):
        original = "[portable Deep change checklist](references/deep-change-checklist.md)"
        cases = (
            ("```markdown", "```   "),
            ("```markdown", "   ````\t"),
            ("~~~~markdown", "~~~~~"),
        )
        for opener, closer in cases:
            with self.subTest(opener=opener, closer=closer):
                temporary_directory = tempfile.TemporaryDirectory()
                self.temporary_directories.append(temporary_directory)
                installed_plugin = Path(temporary_directory.name) / "cache" / "careful" / "0.2.0"
                shutil.copytree(ROOT / "plugins" / "careful", installed_plugin)
                workflow = installed_plugin / "skills" / "careful-workflow" / "SKILL.md"
                workflow_text = workflow.read_text()
                replacement = f"\n{opener}\nnot a link\n{closer}\n{original}\n"
                workflow.write_text(workflow_text.replace(original, replacement, 1))

                self.assertEqual(validate_installed_codex_plugin(installed_plugin), [])

    def test_installed_plugin_does_not_close_a_longer_fence_with_a_shorter_marker(self):
        original = "[portable Deep change checklist](references/deep-change-checklist.md)"
        temporary_directory = tempfile.TemporaryDirectory()
        self.temporary_directories.append(temporary_directory)
        installed_plugin = Path(temporary_directory.name) / "cache" / "careful" / "0.2.0"
        shutil.copytree(ROOT / "plugins" / "careful", installed_plugin)
        workflow = installed_plugin / "skills" / "careful-workflow" / "SKILL.md"
        workflow_text = workflow.read_text()
        replacement = f"\n````markdown\n```\n{original}\n"
        workflow.write_text(workflow_text.replace(original, replacement, 1))

        self.assertIn(
            "Codex workflow missing install-resolvable reference references/deep-change-checklist.md",
            validate_installed_codex_plugin(installed_plugin),
        )

    def test_each_canonical_field_is_required_in_checklist_and_template(self):
        for relative in (
            "core/deep-change-checklist.md",
            "examples/openspec-schemas/critical-deep/templates/design.md",
        ):
            for field in FIELDS:
                with self.subTest(relative=relative, field=field):
                    root = self.fixture()
                    self.mutate(root, relative, field)
                    errors = validate_deep_change_contract(root)
                    self.assertTrue(any(field in error for error in errors), errors)

    def test_trigger_and_evidenced_not_applicable_rule_are_required(self):
        cases = (
            ("core/deep-change-checklist.md", "symlink or submodule layout"),
            (
                "examples/openspec-schemas/critical-deep/templates/design.md",
                "symlink or submodule layout",
            ),
            (
                "core/deep-change-checklist.md",
                "`Not applicable` followed by concrete repository evidence",
            ),
            (
                "examples/openspec-schemas/critical-deep/templates/design.md",
                "`Not applicable` statement followed by concrete repository evidence",
            ),
        )
        for relative, phrase in cases:
            with self.subTest(relative=relative, phrase=phrase):
                root = self.fixture()
                self.mutate(root, relative, phrase)
                errors = validate_deep_change_contract(root)
                self.assertTrue(any(phrase in error for error in errors), errors)

    def test_clean_closure_requires_every_policy_semantic(self):
        semantics = (
            "material Deep review finding",
            "independent review of the corrected artifact",
            "pass with no material actionable findings",
            "unavailable review",
            "residual risk",
            "accepted override",
        )
        for phrase in semantics:
            with self.subTest(phrase=phrase):
                root = self.fixture()
                self.mutate(root, "core/policy.md", phrase)
                errors = validate_deep_change_contract(root)
                self.assertTrue(any(phrase in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
