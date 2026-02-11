from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .render_ui import render_ui
from .schema import validate_rpo, validate_rpo_detailed


def _load_json(path: str) -> dict[str, Any]:
    try:
        obj = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(2) from RuntimeError(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(2) from RuntimeError(
            f"Invalid JSON in {path}: line {exc.lineno}, column {exc.colno}"
        )
    if not isinstance(obj, dict):
        raise SystemExit(2) from RuntimeError(f"Top-level JSON value in {path} must be an object")
    return obj


def main() -> None:
    p = argparse.ArgumentParser(prog="rpo", description="Renderable Prompt Object (RPO)")
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Validate an RPO JSON file")
    v.add_argument("path", help="Path to RPO JSON")
    v.add_argument("--format", choices=["text", "json"], default="text", help="Output format")

    r = sub.add_parser("render", help="Render an RPO JSON file")
    r.add_argument("path", help="Path to RPO JSON")
    r.add_argument("--target", choices=["ui"], default="ui")

    args = p.parse_args()

    try:
        obj = _load_json(args.path)
    except SystemExit as exc:
        cause = exc.__cause__
        if cause:
            print(str(cause), file=sys.stderr)
        raise

    if args.cmd == "validate":
        if args.format == "json":
            errors = validate_rpo_detailed(obj)
            print(json.dumps({"ok": len(errors) == 0, "errors": errors}))
            if errors:
                raise SystemExit(1)
            return

        errors = validate_rpo(obj)
        if errors:
            for e in errors:
                print(e, file=sys.stderr)
            raise SystemExit(1)
        print("ok")
        return

    if args.cmd == "render":
        errors = validate_rpo(obj)
        if errors:
            for e in errors:
                print(e, file=sys.stderr)
            raise SystemExit(1)
        if args.target == "ui":
            print(render_ui(obj), end="")
            return

    raise SystemExit(2)


if __name__ == "__main__":
    main()
