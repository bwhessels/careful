#!/usr/bin/env python3
"""Validate project-configured public-readiness artifacts without running commands."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any


AUDIENCES = {"private", "internal", "public-intended", "public"}


def parse_public_readiness(path: Path) -> dict[str, Any]:
    """Parse the documented public_readiness subset without a YAML dependency."""
    profile: dict[str, Any] = {
        "audience": "unknown",
        "required_documents": [],
        "checks": [],
        "gates": {},
    }
    if not path.exists():
        return profile

    in_readiness = False
    active_list: str | None = None
    in_gates = False
    for line in path.read_text().splitlines():
        if line == "public_readiness:":
            in_readiness = True
            continue
        if in_readiness and line and not line.startswith(" "):
            break
        if not in_readiness or not line.strip():
            continue

        scalar = re.fullmatch(r"  (audience):\s*(\S.*)", line)
        if scalar:
            profile[scalar.group(1)] = scalar.group(2).strip()
            active_list = None
            in_gates = False
            continue

        list_key = re.fullmatch(r"  (required_documents|checks):\s*", line)
        if list_key:
            active_list = list_key.group(1)
            in_gates = False
            continue

        gate_key = re.fullmatch(r"  gates:\s*", line)
        if gate_key:
            active_list = None
            in_gates = True
            continue

        list_item = re.fullmatch(r"    -\s*(\S.*)", line)
        if list_item and active_list:
            profile[active_list].append(list_item.group(1).strip())
            continue

        gate_item = re.fullmatch(r"    ([a-z_]+):\s*(\S.*)", line)
        if gate_item and in_gates:
            profile["gates"][gate_item.group(1)] = gate_item.group(2).strip()
    return profile


def validate_public_readiness(root: Path) -> dict[str, Any]:
    """Return a stable result for project-owned public-readiness configuration."""
    profile = parse_public_readiness(root / "careful.project.yaml")
    mode = profile["audience"]
    checked_documents: list[str] = []
    failed_checks: list[str] = []
    warnings: list[str] = []
    evidence: list[str] = []

    if mode == "unknown":
        warnings.append("public_readiness is not configured")
    elif mode not in AUDIENCES:
        failed_checks.append(f"unsupported public_readiness.audience: {mode}")

    for document in profile["required_documents"]:
        if document.startswith(("http://", "https://")):
            warnings.append(f"external document requires project verifier: {document}")
            continue
        path = root / document
        if path.exists():
            checked_documents.append(document)
        else:
            failed_checks.append(f"missing required document: {document}")

    for command in profile["checks"]:
        if not command.strip():
            failed_checks.append("empty public_readiness check command")

    if profile["required_documents"] and not failed_checks:
        evidence.append("required-documents")
    if profile["checks"]:
        evidence.append("configured-checks-declared")
    if profile["gates"]:
        evidence.append("gates-declared")

    return {
        "status": "fail" if failed_checks else "pass",
        "mode": mode,
        "checked_documents": checked_documents,
        "failed_checks": failed_checks,
        "warnings": warnings,
        "evidence": evidence,
    }


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    result = validate_public_readiness(root)
    for failure in result["failed_checks"]:
        print(f"FAIL: {failure}")
    for warning in result["warnings"]:
        print(f"WARN: {warning}")
    print(f"Public-readiness validation: {result['status']} (mode: {result['mode']})")
    return 1 if result["failed_checks"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
