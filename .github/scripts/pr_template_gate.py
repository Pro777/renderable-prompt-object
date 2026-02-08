#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import sys

REQUIRED_HEADINGS = ["## What", "## Why", "## Verification", "## Notes"]
REQUIRED_VERIFICATION_LABELS = [
    "Tests pass",
    "Examples/docs updated",
    "Changelog updated",
    "Copilot review threads addressed and resolved",
]


def main() -> int:
    body = os.environ.get("PR_BODY", "")
    if not body.strip():
        print("FAIL: PR body is empty.")
        return 1

    missing = [h for h in REQUIRED_HEADINGS if h not in body]
    if missing:
        print("FAIL: PR body is missing required template sections:")
        for heading in missing:
            print(f"- {heading}")
        return 1

    verification_block_match = re.search(r"## Verification\n(.*?)(\n## |\Z)", body, flags=re.S)
    if not verification_block_match:
        print("FAIL: Could not parse ## Verification section.")
        return 1

    verification_block = verification_block_match.group(1)
    missing_lines = []
    for label in REQUIRED_VERIFICATION_LABELS:
        pattern = rf"- \[[ xX]\] .*{re.escape(label)}"
        if not re.search(pattern, verification_block):
            missing_lines.append(label)
    if missing_lines:
        print("FAIL: ## Verification is missing required checklist items from template:")
        for label in missing_lines:
            print(f"- {label}")
        return 1

    print("PASS: PR body includes required PR template sections and checklist items.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
