import json
from pathlib import Path

from rpo.schema import validate_rpo
from rpo.render_ui import render_ui


def test_example_validates_and_renders():
    obj = json.loads(Path("examples/01-simple-codegen.json").read_text(encoding="utf-8"))
    errors = validate_rpo(obj)
    assert errors == []

    out = render_ui(obj)
    assert "## RULES" in out
    assert "## TASK" in out
    assert "## OUTPUT" in out
