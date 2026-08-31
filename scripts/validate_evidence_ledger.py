#!/usr/bin/env python3
"""Validate a configured Careful evidence ledger."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from careful_assessment import validate_evidence_ledger


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    result = validate_evidence_ledger(root)
    for error in result["errors"]:
        print(f"FAIL: {error}")
    for warning in result["warnings"]:
        print(f"WARN: {warning}")
    print(json.dumps(result, sort_keys=True))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
