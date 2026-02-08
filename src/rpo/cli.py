from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .render_ui import render_ui
from .schema import validate_rpo


def _load_json(path: str) -> dict[str, Any]:
    try:
        obj = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: line {exc.lineno}, column {exc.colno}") from exc
    if not isinstance(obj, dict):
        raise SystemExit(f"Top-level JSON value in {path} must be an object")
    return obj


def main() -> None:
    p = argparse.ArgumentParser(prog="rpo", description="Renderable Prompt Object (RPO)")
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Validate an RPO JSON file")
    v.add_argument("path", help="Path to RPO JSON")

    r = sub.add_parser("render", help="Render an RPO JSON file")
    r.add_argument("path", help="Path to RPO JSON")
    r.add_argument("--target", choices=["ui"], default="ui")

    args = p.parse_args()

    obj = _load_json(args.path)

    if args.cmd == "validate":
        errors = validate_rpo(obj)
        if errors:
            for e in errors:
                print(e)
            raise SystemExit(1)
        print("ok")
        return

    if args.cmd == "render":
        errors = validate_rpo(obj)
        if errors:
            for e in errors:
                print(e)
            raise SystemExit(1)
        if args.target == "ui":
            print(render_ui(obj), end="")
            return

    raise SystemExit(2)


if __name__ == "__main__":
    main()
