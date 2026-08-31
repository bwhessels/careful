#!/usr/bin/env python3
"""Analyze changed paths against Careful workflow surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from careful_assessment import analyze_change_impact, collect_changed_paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--paths", nargs="*", default=None)
    parser.add_argument("--diff-file", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    if args.paths is None:
        paths, errors = collect_changed_paths(args.root, args.diff_file)
    else:
        paths = args.paths
    result = analyze_change_impact(args.root, paths)
    result["errors"].extend(errors)
    for error in sorted(result["errors"]):
        print(f"WARN: {error}")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
