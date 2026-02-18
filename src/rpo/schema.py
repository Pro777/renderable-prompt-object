from __future__ import annotations

import json
from importlib import resources
from typing import Any, Dict, List

import jsonschema


def _load_schema() -> Dict[str, Any]:
    # Load schema from package data so validation works when installed from PyPI.
    with resources.files("rpo.data").joinpath("rpo.v1.schema.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def get_schema() -> Dict[str, Any]:
    """Return the bundled RPO JSON schema."""
    return _load_schema()


def _iter_sorted_errors(obj: Dict[str, Any]) -> List[jsonschema.ValidationError]:
    schema = _load_schema()
    validator = jsonschema.Draft202012Validator(schema)
    return sorted(validator.iter_errors(obj), key=lambda e: (tuple(e.path), e.message))


def validate_rpo_detailed(obj: Dict[str, Any]) -> List[Dict[str, str]]:
    """Validate an RPO object and return structured errors."""
    errors: List[Dict[str, str]] = []
    for err in _iter_sorted_errors(obj):
        loc = ".".join([str(x) for x in err.path])
        errors.append({"path": loc, "message": err.message})
    return errors


def validate_rpo(obj: Dict[str, Any]) -> List[str]:
    """Validate an RPO object. Returns a list of human-readable errors (empty if valid)."""
    errors: List[str] = []
    for err in validate_rpo_detailed(obj):
        loc = err["path"]
        if loc:
            errors.append(f"{loc}: {err['message']}")
        else:
            errors.append(err["message"])
    return errors
