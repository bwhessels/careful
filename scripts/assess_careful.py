#!/usr/bin/env python3
"""Run Careful's autonomous ledger and impact assessment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from careful_assessment import run_assessment


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--depth", choices=("quick", "standard", "deep"), default="standard")
    parser.add_argument("--paths", nargs="*", default=None)
    args = parser.parse_args()
    result = run_assessment(args.root, args.depth, args.paths)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result["route"] == "block-until-verified" else 0


if __name__ == "__main__":
    raise SystemExit(main())
