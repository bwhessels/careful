#!/usr/bin/env python3
"""Run conservative, evidence-backed structural hygiene checks."""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path
from typing import Any


IGNORED_PARTS = {".git", ".careful", ".beads", ".superpowers", "__pycache__", "node_modules"}
SCANNED_SUFFIXES = {".py", ".md", ".yaml", ".yml", ".json", ".toml", ".sh"}
PLACEHOLDER_RE = re.compile(r"^\s*(?:TODO|TBD|FIXME)\s*[:!-]|^\s*\[TODO:", re.IGNORECASE)
SLOP_RE = re.compile(r"\b(?:as an ai|as a language model|certainly!|i hope this helps)\b", re.IGNORECASE)


def _files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.suffix in SCANNED_SUFFIXES and not IGNORED_PARTS.intersection(path.relative_to(root).parts)
    )


def _finding(path: str, category: str, severity: str, confidence: str, summary: str, evidence: str) -> dict[str, Any]:
    return {
        "path": path,
        "category": category,
        "severity": severity,
        "confidence": confidence,
        "summary": summary,
        "evidence": evidence,
    }


def _python_unused_candidates(path: str, text: str, all_names: set[str]) -> list[dict[str, Any]]:
    if Path(path).name.startswith("test_"):
        return []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    definitions: list[tuple[str, int]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and not node.name.startswith("_"):
            definitions.append((node.name, node.lineno))
    return [
        _finding(str(path), "unused-candidate", "minor", "inferred", f"Public definition may be unused: {name}", f"AST definition at line {line} has no repository name reference")
        for name, line in definitions if name not in all_names
    ]


def _python_duplication_candidates(path: str, text: str) -> list[dict[str, Any]]:
    if Path(path).name.startswith("test_"):
        return []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    bodies: dict[str, list[tuple[str, int]]] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = ast.dump(ast.Module(body=node.body, type_ignores=[]), annotate_fields=False)
            bodies.setdefault(body, []).append((node.name, node.lineno))
    findings: list[dict[str, Any]] = []
    for matches in bodies.values():
        if len(matches) > 1:
            names = ", ".join(name for name, _ in matches)
            lines = ", ".join(str(line) for _, line in matches)
            findings.append(_finding(str(path), "duplication-candidate", "minor", "inferred", f"Functions share an identical body: {names}", f"AST bodies repeat at lines {lines}"))
    return findings


def review_codebase_hygiene(root: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    scanned: list[str] = []
    files = _files(root)
    all_python_names: set[str] = set()
    for path in files:
        if path.suffix == ".py":
            try:
                tree = ast.parse(path.read_text())
                all_python_names.update(node.id for node in ast.walk(tree) if isinstance(node, ast.Name))
            except (OSError, SyntaxError, UnicodeDecodeError):
                continue
    for path in files:
        relative = str(path.relative_to(root))
        scanned.append(relative)
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        lines = text.splitlines()
        if path.suffix in {".py", ".sh"} and len(lines) > 200:
            findings.append(_finding(relative, "large-file", "minor", "verified", f"File has {len(lines)} lines", "line count exceeds the 200-line hygiene threshold"))
        for number, line in enumerate(lines, 1):
            if path.name not in {"review_codebase_hygiene.py", "test_codebase_hygiene.py"} and PLACEHOLDER_RE.search(line):
                findings.append(_finding(relative, "placeholder", "important", "verified", "Placeholder marker remains in tracked content", f"line {number}: {line.strip()}"))
            if path.name not in {"review_codebase_hygiene.py", "test_codebase_hygiene.py"} and SLOP_RE.search(line):
                findings.append(_finding(relative, "ai-slop", "minor", "verified", "Generic assistant-style filler appears in tracked content", f"line {number}: {line.strip()}"))
        if path.suffix == ".py":
            findings.extend(_python_duplication_candidates(relative, text))
            findings.extend(_python_unused_candidates(relative, text, all_python_names))
    findings.sort(key=lambda item: (item["severity"], item["category"], item["path"], item["summary"]))
    return {"status": "findings" if findings else "clean", "scanned": scanned, "findings": findings, "limitations": ["Static checks identify candidates; they do not prove semantic duplication or unused behavior."]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    result = review_codebase_hygiene(args.root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if any(item["severity"] in {"critical", "important"} for item in result["findings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
