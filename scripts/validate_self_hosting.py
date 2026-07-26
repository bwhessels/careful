#!/usr/bin/env python3
"""Validate Careful's portable self-hosting and fixture contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "careful"
SKILLS = ("careful-workflow", "careful-documentation", "careful-retrospective", "careful-adopt")
GUIDANCE_FILES = (
    ROOT / "AGENTS.md",
    ROOT / "fixtures" / "adopted-project" / "AGENTS.md",
    PLUGIN / "skills" / "careful-adopt" / "references" / "project-guidance.md",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> None:
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

    ignore = (ROOT / ".gitignore").read_text()
    require(".careful/" in ignore, "private .careful context must be ignored")

    profile = (ROOT / "careful.project.yaml").read_text()
    require("fixtures/adopted-project/" in profile, "profile must declare its consumer fixture")
    require("validate_self_hosting" in profile, "profile must declare portable validation")

    for guidance in GUIDANCE_FILES:
        require(guidance.is_file(), f"missing guidance file: {guidance.relative_to(ROOT)}")
        require("$careful-workflow" in guidance.read_text(), f"{guidance.relative_to(ROOT)} must activate Careful")

    require((ROOT / "docs" / "release.md").is_file(), "release procedure must be documented")
    print("Careful self-hosting validation passed")


if __name__ == "__main__":
    main()
