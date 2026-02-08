#!/usr/bin/env python3
from __future__ import annotations

import fnmatch
import os
import subprocess
import sys
from pathlib import PurePosixPath

CODE_PATTERNS = [
    "src/**",
    "schema/**",
    "tests/**",
    "examples/**",
    "pyproject.toml",
    "setup.py",
]

DOC_PATTERNS = [
    "CHANGELOG.md",
    "README.md",
    "docs/**",
    "SKILL.md",
    "AGENTS.md",
]


def _matches(path: str, patterns: list[str]) -> bool:
    p = PurePosixPath(path)
    return any(fnmatch.fnmatch(str(p), pat) for pat in patterns)


def _changed_files(base: str, head: str) -> list[str]:
    out = subprocess.check_output(["git", "diff", "--name-only", f"{base}...{head}"], text=True)
    return [line.strip() for line in out.splitlines() if line.strip()]


def main() -> int:
    base = os.environ.get("BASE_SHA")
    head = os.environ.get("HEAD_SHA")
    if not base or not head:
        print("Missing BASE_SHA or HEAD_SHA")
        return 2

    changed = _changed_files(base, head)
    code_changed = [p for p in changed if _matches(p, CODE_PATTERNS)]
    docs_changed = [p for p in changed if _matches(p, DOC_PATTERNS)]

    print(f"Changed files: {len(changed)}")
    print(f"Code-impact files: {len(code_changed)}")
    print(f"Docs/changelog files: {len(docs_changed)}")

    if not code_changed:
        print("PASS: no code-impact files changed; docs/changelog gate not required.")
        return 0

    if docs_changed:
        print("PASS: docs/changelog updated alongside code-impact changes.")
        return 0

    print("FAIL: code-impact files changed but no docs/changelog update was detected.")
    print("Add at least one of: CHANGELOG.md, README.md, docs/**, SKILL.md, AGENTS.md")
    print("Code-impact files detected:")
    for path in code_changed[:25]:
        print(f"- {path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
