#!/usr/bin/env python3
"""Validate dependencies between active OpenSpec changes."""

from __future__ import annotations

import re
import sys
from pathlib import Path


CAPABILITY_BULLET = re.compile(r"^- `([^`]+)`(?:\s*:|\s*$)")


def parse_capabilities(proposal: Path) -> tuple[set[str], set[str]]:
    """Return new and modified capability identifiers from a proposal."""
    new: set[str] = set()
    modified: set[str] = set()
    destination: set[str] | None = None

    for line in proposal.read_text().splitlines():
        if line == "### New Capabilities":
            destination = new
            continue
        if line == "### Modified Capabilities":
            destination = modified
            continue
        if line.startswith("#"):
            destination = None
            continue
        if destination is not None:
            match = CAPABILITY_BULLET.match(line)
            if match:
                destination.add(match.group(1))

    return new, modified


def parse_dependencies(metadata: Path) -> tuple[str, ...]:
    """Return the simple top-level depends_on list from change metadata."""
    if not metadata.is_file():
        return ()

    dependencies: list[str] = []
    in_dependencies = False
    for line in metadata.read_text().splitlines():
        if line == "depends_on:":
            in_dependencies = True
            continue
        if in_dependencies and line.startswith("  - "):
            dependencies.append(line.removeprefix("  - ").strip())
            continue
        if in_dependencies:
            break
    return tuple(dependencies)


def _dependency_cycles(graph: dict[str, tuple[str, ...]]) -> set[str]:
    cycles: set[str] = set()
    visiting: list[str] = []
    visited: set[str] = set()

    def visit(change: str) -> None:
        if change in visited:
            return
        visiting.append(change)
        for dependency in graph[change]:
            if dependency in visiting:
                cycle = visiting[visiting.index(dependency) :] + [dependency]
                body = cycle[:-1]
                start = min(range(len(body)), key=body.__getitem__)
                canonical = body[start:] + body[:start]
                canonical.append(canonical[0])
                cycles.add("dependency cycle: " + " -> ".join(canonical))
            else:
                visit(dependency)
        visiting.pop()
        visited.add(change)

    for change in sorted(graph):
        visit(change)
    return cycles


def validate_change_dependencies(root: Path) -> list[str]:
    """Return deterministic errors for invalid active-change dependencies."""
    specs_root = root / "openspec" / "specs"
    current = {
        capability.parent.name
        for capability in specs_root.glob("*/spec.md")
    }

    changes_root = root / "openspec" / "changes"
    change_directories = sorted(
        path
        for path in changes_root.iterdir()
        if path.is_dir() and path.name != "archive"
    ) if changes_root.is_dir() else []
    change_names = {path.name for path in change_directories}

    capabilities: dict[str, tuple[set[str], set[str]]] = {}
    dependencies: dict[str, tuple[str, ...]] = {}
    providers: dict[str, list[str]] = {}
    for change in change_directories:
        proposal = change / "proposal.md"
        new, modified = parse_capabilities(proposal) if proposal.is_file() else (set(), set())
        capabilities[change.name] = new, modified
        dependencies[change.name] = parse_dependencies(change / ".openspec.yaml")
        for capability in new:
            providers.setdefault(capability, []).append(change.name)

    errors: set[str] = set()
    graph: dict[str, tuple[str, ...]] = {}
    for change in sorted(change_names):
        known_dependencies: list[str] = []
        for dependency in dependencies[change]:
            if dependency == change:
                errors.add(f"{change} declares a dependency on itself")
            elif dependency not in change_names:
                errors.add(f"{change} declares unknown dependency {dependency}")
            else:
                known_dependencies.append(dependency)
        graph[change] = tuple(sorted(set(known_dependencies)))

        for capability in sorted(capabilities[change][1] - current):
            candidates = sorted(providers.get(capability, ()))
            if candidates and not set(candidates).intersection(dependencies[change]):
                errors.add(
                    f"{change} modifies non-current capability {capability}; "
                    f"declare depends_on: {candidates[0]}"
                )

    errors.update(_dependency_cycles(graph))
    return sorted(errors)


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    root = Path(arguments[0]) if arguments else Path(__file__).resolve().parent.parent
    errors = validate_change_dependencies(root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Careful active change dependencies passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
