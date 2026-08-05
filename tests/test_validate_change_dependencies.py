from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_change_dependencies import parse_capabilities, validate_change_dependencies


class ValidateChangeDependenciesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directories: list[tempfile.TemporaryDirectory[str]] = []

    def tearDown(self) -> None:
        for temporary_directory in self.temporary_directories:
            temporary_directory.cleanup()

    def fixture(
        self,
        *,
        current: tuple[str, ...],
        changes: dict[str, dict[str, tuple[str, ...]]],
    ) -> Path:
        temporary_directory = tempfile.TemporaryDirectory()
        self.temporary_directories.append(temporary_directory)
        root = Path(temporary_directory.name)

        for capability in current:
            specification = root / "openspec" / "specs" / capability / "spec.md"
            specification.parent.mkdir(parents=True, exist_ok=True)
            specification.write_text(f"# {capability}\n")

        for name, details in changes.items():
            change = root / "openspec" / "changes" / name
            change.mkdir(parents=True, exist_ok=True)
            proposal_lines = ["## Capabilities", ""]
            for heading, key in (
                ("### New Capabilities", "new"),
                ("### Modified Capabilities", "modified"),
            ):
                proposal_lines.extend((heading, ""))
                proposal_lines.extend(
                    f"- `{capability}`: fixture description"
                    for capability in details.get(key, ())
                )
                proposal_lines.append("")
            (change / "proposal.md").write_text("\n".join(proposal_lines))

            metadata_lines = ["schema: spec-driven"]
            if details.get("depends_on"):
                metadata_lines.append("depends_on:")
                metadata_lines.extend(
                    f"  - {dependency}" for dependency in details["depends_on"]
                )
            (change / ".openspec.yaml").write_text("\n".join(metadata_lines) + "\n")

        return root

    def test_requires_provider_when_modified_capability_is_not_current(self):
        root = self.fixture(
            current=(),
            changes={
                "change-a": {"new": ("portable-core",)},
                "change-b": {"modified": ("portable-core",)},
            },
        )
        self.assertEqual(
            validate_change_dependencies(root),
            ["change-b modifies non-current capability portable-core; declare depends_on: change-a"],
        )

    def test_accepts_declared_provider(self):
        root = self.fixture(
            current=(),
            changes={
                "change-a": {"new": ("portable-core",)},
                "change-b": {
                    "modified": ("portable-core",),
                    "depends_on": ("change-a",),
                },
            },
        )
        self.assertEqual(validate_change_dependencies(root), [])

    def test_rejects_unknown_self_and_cycle_dependencies(self):
        cases = (
            (
                {"change-a": {"depends_on": ("missing-change",)}},
                ["change-a declares unknown dependency missing-change"],
            ),
            (
                {"change-a": {"depends_on": ("change-a",)}},
                ["change-a declares a dependency on itself"],
            ),
            (
                {
                    "change-a": {"depends_on": ("change-b",)},
                    "change-b": {"depends_on": ("change-a",)},
                },
                ["dependency cycle: change-a -> change-b -> change-a"],
            ),
        )
        for changes, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(
                    validate_change_dependencies(self.fixture(current=(), changes=changes)),
                    expected,
                )

    def test_current_capability_requires_no_predecessor(self):
        root = self.fixture(
            current=("portable-core",),
            changes={"change-b": {"modified": ("portable-core",)}},
        )
        self.assertEqual(validate_change_dependencies(root), [])

    def test_capability_section_ends_at_the_next_heading(self):
        root = self.fixture(
            current=(),
            changes={"change-a": {"new": ("portable-core",)}},
        )
        proposal = root / "openspec" / "changes" / "change-a" / "proposal.md"
        with proposal.open("a") as proposal_file:
            proposal_file.write("## Impact\n\n- `not-a-capability`: affected component\n")

        self.assertEqual(parse_capabilities(proposal), ({"portable-core"}, set()))


if __name__ == "__main__":
    unittest.main()
