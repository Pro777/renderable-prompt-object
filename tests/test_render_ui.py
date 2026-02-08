import json
from pathlib import Path

from rpo.render_ui import render_ui


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples"


def _example(name: str) -> dict:
    return json.loads((EXAMPLES_DIR / name).read_text(encoding="utf-8"))


def test_render_required_sections_and_success_present():
    obj = _example("01-simple-codegen.json")
    out = render_ui(obj)
    assert "## RULES" in out
    assert "## TASK" in out
    assert "Success:" in out
    assert "## OUTPUT" in out


def test_render_is_deterministic():
    obj = _example("90-research-round.json")
    assert render_ui(obj) == render_ui(obj)


def test_render_omits_inputs_when_missing():
    obj = _example("01-simple-codegen.json")
    obj["hot_task"].pop("inputs", None)
    out = render_ui(obj)
    assert "Inputs:" not in out


def test_render_omits_inputs_when_empty():
    obj = _example("01-simple-codegen.json")
    obj["hot_task"]["inputs"] = []
    out = render_ui(obj)
    assert "Inputs:" not in out


def test_render_includes_inputs_when_present():
    obj = _example("01-simple-codegen.json")
    obj["hot_task"]["inputs"] = ["foo.py", {"kind": "artifact", "id": "A-1"}]
    out = render_ui(obj)
    assert "Inputs:" in out
    assert "- foo.py" in out
    assert '- {"id": "A-1", "kind": "artifact"}' in out


def test_render_inputs_object_is_key_order_deterministic():
    obj = _example("01-simple-codegen.json")
    obj["hot_task"]["inputs"] = [{"kind": "artifact", "id": "A-1", "notes": "hello"}]
    out_one = render_ui(obj)
    obj["hot_task"]["inputs"] = [{"notes": "hello", "id": "A-1", "kind": "artifact"}]
    out_two = render_ui(obj)
    assert out_one == out_two


def test_render_inputs_presence_changes_structure():
    obj = _example("01-simple-codegen.json")
    obj["hot_task"]["inputs"] = []
    without_inputs = render_ui(obj)
    obj["hot_task"]["inputs"] = ["foo.py"]
    with_inputs = render_ui(obj)
    assert "Inputs:" not in without_inputs
    assert "Inputs:" in with_inputs
    assert with_inputs != without_inputs
