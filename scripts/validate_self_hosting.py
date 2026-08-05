#!/usr/bin/env python3
"""Validate Careful's portable core, adapters, and fixture contract."""

from __future__ import annotations

import json
from pathlib import Path

from validate_change_dependencies import validate_change_dependencies


ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "careful"
SKILLS = ("careful-workflow", "careful-documentation", "careful-retrospective", "careful-adopt")
CORE = ROOT / "core"
ADAPTERS = {
    "claude-code": ROOT / "adapters" / "claude-code",
    "factory-droid": ROOT / "adapters" / "factory-droid",
}
GUIDANCE_FILES = (
    ROOT / "AGENTS.md",
    ROOT / "fixtures" / "adopted-project" / "codex" / "AGENTS.md",
    PLUGIN / "skills" / "careful-adopt" / "references" / "project-guidance.md",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def parse_adapter_manifest(path: Path) -> tuple[int | None, str | None, dict[str, dict[str, str]]]:
    """Parse the small, checked-in manifest shape without a runtime YAML dependency."""
    version = None
    core_policy = None
    adapters: dict[str, dict[str, str]] = {}
    current_adapter: str | None = None
    for raw_line in path.read_text().splitlines():
        if raw_line.startswith("version: "):
            version = int(raw_line.removeprefix("version: "))
        elif raw_line.startswith("core_policy: "):
            core_policy = raw_line.removeprefix("core_policy: ")
        elif raw_line.startswith("  ") and not raw_line.startswith("    ") and raw_line.endswith(":"):
            current_adapter = raw_line.strip().removesuffix(":")
            adapters[current_adapter] = {}
        elif raw_line.startswith("    ") and not raw_line.startswith("      ") and ":" in raw_line and current_adapter:
            key, value = raw_line.strip().split(":", 1)
            adapters[current_adapter][key] = value.strip()
    return version, core_policy, adapters


def main() -> None:
    dependency_errors = validate_change_dependencies(ROOT)
    require(not dependency_errors, "\nFAIL: ".join(dependency_errors))

    policy = CORE / "policy.md"
    deep_change_checklist = CORE / "deep-change-checklist.md"
    manifest_file = CORE / "adapter-manifest.yaml"
    require(policy.is_file(), "portable policy must exist")
    require(deep_change_checklist.is_file(), "portable Deep change checklist must exist")
    require(manifest_file.is_file(), "adapter manifest must exist")
    policy_text = policy.read_text()
    require("Version: 1" in policy_text, "portable policy must be versioned")
    for phrase in ("Quick", "Standard", "Deep", "BLOCKED:", "independent review", ".careful/"):
        require(phrase in policy_text, f"portable policy missing {phrase!r}")

    manifest_version, manifest_policy, supported_adapters = parse_adapter_manifest(manifest_file)
    require(manifest_version == 1, "adapter manifest version must be 1")
    require(manifest_policy == "core/policy.md", "manifest must point to portable policy")
    required_adapter_fields = {"status", "distribution", "project_guidance", "explicit_controls", "automatic_activation", "independent_review", "validation", "fixture"}
    for adapter in ("codex", "claude-code", "factory-droid"):
        require(adapter in supported_adapters, f"manifest missing {adapter} adapter")
        missing_fields = required_adapter_fields - supported_adapters[adapter].keys()
        require(not missing_fields, f"manifest {adapter} missing fields: {sorted(missing_fields)}")

    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())
    require(manifest["name"] == "careful", "plugin manifest must be named careful")
    require(manifest["skills"] == "./skills/", "plugin must expose its skills directory")

    for skill in SKILLS:
        skill_file = PLUGIN / "skills" / skill / "SKILL.md"
        require(skill_file.is_file(), f"missing {skill} skill")
        text = skill_file.read_text()
        require(f"name: {skill}" in text, f"{skill} frontmatter must match its directory")
        require("[TODO:" not in text, f"{skill} must not contain placeholders")

    workflow = (PLUGIN / "skills" / "careful-workflow" / "SKILL.md").read_text()
    require("documentation map inline" in workflow, "workflow must own baseline documentation checks")
    require("retrospective signals" in workflow, "workflow must own baseline retrospective checks")
    require("careful.project.yaml" in workflow, "workflow must discover the self-hosting profile")
    require("deep-change-checklist.md" in workflow, "Codex workflow must reference the portable Deep change checklist")
    bridge = (PLUGIN / "skills" / "careful-workflow" / "references" / "core-contract.md").read_text()
    require("core/policy.md" in bridge, "Codex bridge must reference portable policy")

    ignore = (ROOT / ".gitignore").read_text()
    require(".careful/" in ignore, "private .careful context must be ignored")

    profile = (ROOT / "careful.project.yaml").read_text()
    for fixture in ("fixtures/adopted-project/codex/", "fixtures/adopted-project/claude-code/", "fixtures/adopted-project/factory-droid/"):
        require(fixture in profile, f"profile must declare {fixture}")
    require("validate_self_hosting" in profile, "profile must declare portable validation")

    for guidance in GUIDANCE_FILES:
        require(guidance.is_file(), f"missing guidance file: {guidance.relative_to(ROOT)}")
        require("$careful-workflow" in guidance.read_text(), f"{guidance.relative_to(ROOT)} must activate Careful")

    for doc in ("release.md", "adoption.md", "compatibility.md"):
        require((ROOT / "docs" / doc).is_file(), f"missing documentation: docs/{doc}")
    compatibility = (ROOT / "docs" / "compatibility.md").read_text()
    for adapter, metadata in supported_adapters.items():
        display_name = {"codex": "Codex", "claude-code": "Claude Code", "factory-droid": "Factory Droid"}[adapter]
        status_label = metadata["status"].replace("-", " ").capitalize()
        require(f"| {display_name} | {status_label} |" in compatibility, f"compatibility matrix status mismatch for {adapter}")

    for name, adapter in ADAPTERS.items():
        require((adapter / "README.md").is_file(), f"missing {name} adapter documentation")
        guidance = adapter / "AGENTS.md"
        require(guidance.is_file(), f"missing {name} adapter guidance")
        require("[core/policy.md](core/policy.md)" in guidance.read_text(), f"{name} guidance must use installed-project policy path")
        skill_root = adapter / (".claude" if name == "claude-code" else ".factory") / "skills"
        for skill in SKILLS:
            skill_file = skill_root / skill / "SKILL.md"
            require(skill_file.is_file(), f"missing {name} {skill} skill")
            text = skill_file.read_text()
            require(f"name: {skill}" in text, f"{name} {skill} frontmatter must match")
            require("../../../core/policy.md" in text, f"{name} {skill} must use installed-project policy path")
            require("## Evidence" not in text and "BLOCKED:" not in text, f"{name} {skill} duplicates portable policy")
            if skill == "careful-workflow":
                require(
                    "../../../core/deep-change-checklist.md" in text,
                    f"{name} workflow must reference the installed-project Deep change checklist",
                )
        if name == "claude-code":
            require((adapter / "CLAUDE.md").is_file(), "Claude adapter must provide CLAUDE.md")
            require("@AGENTS.md" in (adapter / "CLAUDE.md").read_text(), "Claude entry point must import AGENTS.md")
            require((adapter / ".claude" / "agents" / "careful-independent-review.md").is_file(), "Claude adapter missing reviewer")
        else:
            require((adapter / ".factory" / "droids" / "careful-independent-review.md").is_file(), "Factory adapter missing reviewer")

    for fixture in ("codex", "claude-code", "factory-droid"):
        fixture_root = ROOT / "fixtures" / "adopted-project" / fixture
        require((fixture_root / "AGENTS.md").is_file(), f"missing {fixture} fixture guidance")
        require((fixture_root / "README.md").is_file(), f"missing {fixture} fixture documentation")
    require((ROOT / "fixtures" / "adopted-project" / "SCENARIO.md").is_file(), "missing common fixture scenario")

    deep_design = (ROOT / "examples" / "openspec-schemas" / "critical-deep" / "templates" / "design.md").read_text()
    require("## Distribution contract" in deep_design, "Critical Deep design template must provide a Distribution contract")

    checklist_fields = (
        "Bootstrap and discovery:",
        "Consumer path and reference resolution:",
        "Cloneable source and immutable version:",
        "Interactive, dry-run, and non-interactive defaults:",
        "Tracked, ignored, local, and private state:",
        "Upgrade, repair, migration, rollback, and destructive boundaries:",
    )
    workflow_files = [
        PLUGIN / "skills" / "careful-workflow" / "SKILL.md",
        ADAPTERS["claude-code"] / ".claude" / "skills" / "careful-workflow" / "SKILL.md",
        ADAPTERS["factory-droid"] / ".factory" / "skills" / "careful-workflow" / "SKILL.md",
    ]
    for workflow_file in workflow_files:
        workflow_text = workflow_file.read_text()
        duplicated_fields = [field for field in checklist_fields if field in workflow_text]
        require(
            not duplicated_fields,
            f"{workflow_file.relative_to(ROOT)} duplicates portable Deep checklist fields: {duplicated_fields}",
        )
    print("Careful self-hosting validation passed")


if __name__ == "__main__":
    main()
