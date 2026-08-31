#!/usr/bin/env python3
"""Validate Careful's portable core, adapters, and fixture contract."""

from __future__ import annotations

import json
import re
from pathlib import Path

from validate_change_dependencies import validate_change_dependencies
from validate_public_readiness import validate_public_readiness
from validate_spec_authority import validate_spec_authority
from careful_assessment import analyze_change_impact, validate_evidence_ledger


ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "careful"
SKILLS = ("careful-workflow", "careful-documentation", "careful-retrospective", "careful-adopt")
ASSESSMENT_SCRIPTS = (
    ROOT / "scripts" / "careful_assessment.py",
    ROOT / "scripts" / "validate_evidence_ledger.py",
    ROOT / "scripts" / "analyze_change_impact.py",
    ROOT / "scripts" / "assess_careful.py",
    ROOT / "scripts" / "review_codebase_hygiene.py",
)
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
DEEP_CHANGE_FIELDS = (
    "Bootstrap and discovery:",
    "Consumer path and reference resolution:",
    "Cloneable source and immutable version:",
    "Interactive, dry-run, and non-interactive defaults:",
    "Tracked, ignored, local, and private state:",
    "Upgrade, repair, migration, rollback, and destructive boundaries:",
)
DEEP_CHANGE_TRIGGERS = (
    "command",
    "initializer",
    "installer",
    "package or plugin distribution",
    "symlink or submodule layout",
    "generated project guidance",
    "shared filesystem artifact",
)
CLEAN_CLOSURE_SEMANTICS = (
    "material Deep review finding",
    "independent review of the corrected artifact",
    "pass with no material actionable findings",
    "unavailable review",
    "residual risk",
    "accepted override",
)
MARKDOWN_CODE = re.compile(r"(`+).*?\1", re.DOTALL)
MARKDOWN_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)\s]+)(?:\s+[^)]*)?\)")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def markdown_indentation_columns(line: str) -> int:
    """Return leading indentation using four-column tab stops."""
    columns = 0
    for character in line:
        if character == " ":
            columns += 1
        elif character == "\t":
            columns += 4 - (columns % 4)
        else:
            break
    return columns


def markdown_link_destinations(text: str) -> set[str]:
    """Return link destinations outside Markdown code spans and fences."""
    visible_lines: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines():
        if markdown_indentation_columns(line) >= 4:
            continue
        fence = MARKDOWN_FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
            elif (
                marker[0] == fence_character
                and len(marker) >= fence_length
                and not line[fence.end() :].strip(" \t")
            ):
                fence_character = None
                fence_length = 0
            continue
        if fence_character is not None:
            continue
        visible_lines.append(line)

    visible_text = MARKDOWN_CODE.sub("", "\n".join(visible_lines))
    destinations: set[str] = set()
    for link in MARKDOWN_LINK.finditer(visible_text):
        preceding_backslashes = 0
        index = link.start() - 1
        while index >= 0 and visible_text[index] == "\\":
            preceding_backslashes += 1
            index -= 1
        if preceding_backslashes % 2:
            continue
        destinations.add(link.group(1))
    return destinations


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


def validate_installed_codex_plugin(plugin_root: Path) -> list[str]:
    """Validate references using only the files shipped in a Codex plugin package."""
    workflow_root = plugin_root / "skills" / "careful-workflow"
    workflow = workflow_root / "SKILL.md"
    bundled_policy = workflow_root / "references" / "core-contract.md"
    errors: list[str] = []
    if not workflow.is_file():
        return ["installed Codex plugin missing careful-workflow/SKILL.md"]
    workflow_text = workflow.read_text()
    workflow_destinations = markdown_link_destinations(workflow_text)
    for relative_reference in ("references/core-contract.md", "references/deep-change-checklist.md"):
        if relative_reference not in workflow_destinations:
            errors.append(f"Codex workflow missing install-resolvable reference {relative_reference}")
        elif not (workflow.parent / relative_reference).is_file():
            errors.append(f"Codex installed reference does not resolve: {relative_reference}")
    if not bundled_policy.is_file():
        errors.append("installed Codex plugin missing bundled core-contract.md")
    else:
        for relative_reference in markdown_link_destinations(bundled_policy.read_text()):
            if not relative_reference.endswith(".md"):
                continue
            if not (bundled_policy.parent / relative_reference).is_file():
                errors.append(f"Codex bundled policy reference does not resolve: {relative_reference}")
    return sorted(errors)


def validate_deep_change_contract(root: Path) -> list[str]:
    """Return deterministic errors for the portable Deep contract and its renderings."""
    core = root / "core"
    plugin_workflow_root = root / "plugins" / "careful" / "skills" / "careful-workflow"
    policy = core / "policy.md"
    checklist = core / "deep-change-checklist.md"
    design = root / "examples" / "openspec-schemas" / "critical-deep" / "templates" / "design.md"
    bundled_policy = plugin_workflow_root / "references" / "core-contract.md"
    bundled_checklist = plugin_workflow_root / "references" / "deep-change-checklist.md"
    workflow_files = (
        plugin_workflow_root / "SKILL.md",
        root / "adapters" / "claude-code" / ".claude" / "skills" / "careful-workflow" / "SKILL.md",
        root / "adapters" / "factory-droid" / ".factory" / "skills" / "careful-workflow" / "SKILL.md",
    )
    errors: list[str] = []

    required_files = (policy, checklist, design, bundled_policy, bundled_checklist, *workflow_files)
    for path in required_files:
        if not path.is_file():
            errors.append(f"missing Deep contract file: {path.relative_to(root)}")
    if errors:
        return sorted(errors)

    policy_text = policy.read_text()
    checklist_text = checklist.read_text()
    design_text = design.read_text()
    for path, text in ((checklist, checklist_text), (design, design_text)):
        for field in DEEP_CHANGE_FIELDS:
            if field not in text:
                errors.append(f"{path.relative_to(root)} missing canonical field {field}")
        for trigger in DEEP_CHANGE_TRIGGERS:
            if trigger not in text:
                errors.append(f"{path.relative_to(root)} missing trigger {trigger}")

    evidenced_rules = (
        (checklist, "`Not applicable` followed by concrete repository evidence"),
        (design, "`Not applicable` statement followed by concrete repository evidence"),
    )
    for path, phrase in evidenced_rules:
        if phrase not in path.read_text():
            errors.append(f"{path.relative_to(root)} missing evidenced rule {phrase}")

    clean_closure_rule = next(
        (line for line in policy_text.splitlines() if line.startswith("After correcting a material Deep review finding")),
        "",
    )
    for semantic in CLEAN_CLOSURE_SEMANTICS:
        if semantic not in clean_closure_rule:
            errors.append(f"core/policy.md missing clean-closure semantic {semantic}")

    if bundled_policy.read_text() != policy_text:
        errors.append("Codex bundled core-contract.md must exactly render core/policy.md")
    if bundled_checklist.read_text() != checklist_text:
        errors.append("Codex bundled deep-change-checklist.md must exactly render core/deep-change-checklist.md")

    errors.extend(validate_installed_codex_plugin(root / "plugins" / "careful"))

    for workflow_file in workflow_files:
        workflow_text = workflow_file.read_text()
        duplicated_fields = [field for field in DEEP_CHANGE_FIELDS if field in workflow_text]
        if duplicated_fields:
            errors.append(
                f"{workflow_file.relative_to(root)} duplicates portable Deep checklist fields: {duplicated_fields}"
            )
    return sorted(errors)


def main() -> None:
    dependency_errors = validate_change_dependencies(ROOT)
    require(not dependency_errors, "\nFAIL: ".join(dependency_errors))

    authority_errors = validate_spec_authority(ROOT)
    require(not authority_errors, "\nFAIL: ".join(authority_errors))

    public_readiness = validate_public_readiness(ROOT)
    require(not public_readiness["failed_checks"], "\nFAIL: ".join(public_readiness["failed_checks"]))

    deep_contract_errors = validate_deep_change_contract(ROOT)
    require(not deep_contract_errors, "\nFAIL: ".join(deep_contract_errors))

    fixture_root = ROOT / "fixtures" / "adopted-project"
    fixture_ledger = validate_evidence_ledger(fixture_root)
    require(fixture_ledger["status"] == "pass", "consumer fixture evidence ledger failed")
    fixture_impact = analyze_change_impact(fixture_root, ["README.md", "AGENTS.md"])
    require(
        any(item["surface"] == "public-documentation" for item in fixture_impact["findings"]),
        "consumer fixture impact analysis missed public documentation",
    )
    print("Consumer fixture assessment validation passed")

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
    for script in ASSESSMENT_SCRIPTS:
        require(script.is_file(), f"missing assessment implementation: {script.relative_to(ROOT)}")

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
    require("autonomous evidence, change-impact, and codebase-hygiene assessment" in workflow, "workflow must run autonomous assessment")

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
    fixture_root = ROOT / "fixtures" / "adopted-project"
    require((fixture_root / "careful.project.yaml").is_file(), "missing adopted-project fixture profile")
    fixture_authority_errors = validate_spec_authority(fixture_root)
    require(not fixture_authority_errors, "\nFAIL: ".join(fixture_authority_errors))
    require((ROOT / "fixtures" / "adopted-project" / "SCENARIO.md").is_file(), "missing common fixture scenario")

    deep_design = (ROOT / "examples" / "openspec-schemas" / "critical-deep" / "templates" / "design.md").read_text()
    require("## Distribution contract" in deep_design, "Critical Deep design template must provide a Distribution contract")

    print("Careful self-hosting validation passed")


if __name__ == "__main__":
    main()
