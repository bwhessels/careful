#!/usr/bin/env python3
"""Validate a project's durable specification authority and conflicts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


SUPPORTED_AUTHORITIES = {"openspec", "project-defined", "none"}
DEFAULT_COMPETING_SPEC_ROOT = Path("docs/superpowers/specs")
DURABLE_HEADINGS = re.compile(
    r"^#{1,3}\s+(Goals|Requirements|Decisions|Non-goals|Purpose|Design|Context|Problem)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def parse_documentation_profile(path: Path) -> dict[str, str]:
    """Parse the documented scalar fields from a project's documentation block."""
    profile = {"spec_authority": "unknown"}
    if not path.exists():
        return profile

    in_documentation = False
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if line == "documentation:":
            in_documentation = True
            continue
        if in_documentation and line and not line.startswith(" "):
            in_documentation = False
        if not in_documentation:
            continue
        match = re.fullmatch(r"  ([a-z_]+):\s*(\S.*)?", line)
        if not match:
            if line.strip() and not line.startswith("  "):
                raise ValueError(f"invalid documentation indentation at line {line_number}")
            continue
        key, value = match.groups()
        if key in {"spec_authority", "execution_plans"}:
            profile[key] = (value or "").strip()
    return profile


def looks_like_durable_spec(path: Path) -> bool:
    """Use conservative content signals rather than filename-only detection."""
    text = path.read_text()
    return bool(DURABLE_HEADINGS.search(text))


def is_explicit_pointer_or_history(path: Path) -> bool:
    """Recognize documents deliberately retained as non-authoritative context."""
    text = path.read_text().lower()
    header = "\n".join(text.splitlines()[:24])
    if re.search(r"\b(pointer|historical)\b", header):
        return True
    return "canonical" in header and "openspec/" in header


def find_specification_conflicts(
    root: Path, profile: dict[str, str]
) -> list[str]:
    """Return conflicts without mutating any project file."""
    if profile.get("spec_authority") != "openspec":
        return []

    competing_root = root / DEFAULT_COMPETING_SPEC_ROOT
    if not competing_root.exists():
        return []

    errors: list[str] = []
    for path in sorted(competing_root.rglob("*.md")):
        if is_explicit_pointer_or_history(path) or not looks_like_durable_spec(path):
            continue
        relative = path.relative_to(root).as_posix()
        errors.append(
            "competing durable specification: "
            f"{relative} (authority: openspec; owner decision required)"
        )
    return errors


def validate_spec_authority(root: Path) -> list[str]:
    """Validate profile values and report competing durable specifications."""
    profile_path = root / "careful.project.yaml"
    try:
        profile = parse_documentation_profile(profile_path)
    except ValueError as error:
        return [str(error)]

    authority = profile.get("spec_authority", "unknown")
    if authority not in SUPPORTED_AUTHORITIES and authority != "unknown":
        return [f"unsupported documentation.spec_authority: {authority}"]
    return find_specification_conflicts(root, profile)


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = validate_spec_authority(root)
    for error in errors:
        print(f"FAIL: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
