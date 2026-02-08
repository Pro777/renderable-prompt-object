import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from rpo.cli import _load_json
from rpo.render_ui import render_ui
from rpo.schema import validate_rpo


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples"
SCHEMA_DIR = ROOT / "schema"
PACKAGED_SCHEMA_PATH = ROOT / "src" / "rpo" / "data" / "rpo.v1.schema.json"
SRC_DIR = ROOT / "src"


def _example(name: str) -> dict:
    return json.loads((EXAMPLES_DIR / name).read_text(encoding="utf-8"))


def test_examples_validate():
    for name in ["01-simple-codegen.json", "90-research-round.json"]:
        obj = _example(name)
        assert validate_rpo(obj) == []


def test_example_renders_required_sections():
    obj = _example("01-simple-codegen.json")
    out = render_ui(obj)
    assert "## RULES" in out
    assert "## TASK" in out
    assert "## OUTPUT" in out


def test_render_is_deterministic():
    obj = _example("90-research-round.json")
    assert render_ui(obj) == render_ui(obj)


def test_render_includes_task_type_and_inputs():
    obj = _example("01-simple-codegen.json")
    obj["hot_task"]["inputs"] = ["foo.py", {"kind": "artifact", "id": "A-1"}]
    out = render_ui(obj)
    assert "Type: codegen" in out
    assert "Inputs:" in out
    assert "- foo.py" in out
    assert "- {'kind': 'artifact', 'id': 'A-1'}" in out


def test_render_includes_zero_like_max_words():
    obj = _example("01-simple-codegen.json")
    obj["output_contract"]["max_words"] = 1
    out = render_ui(obj)
    assert "Format: markdown | Max: 1 words" in out


def test_cli_load_json_reports_file_not_found():
    with pytest.raises(SystemExit, match=r"^File not found: no-such-file\.json$"):
        _load_json("no-such-file.json")


def test_cli_load_json_reports_invalid_json(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text("{\n  not-json\n}\n", encoding="utf-8")

    with pytest.raises(SystemExit, match=r"^Invalid JSON in .* line 2, column 3$"):
        _load_json(str(bad))


def test_packaged_schema_matches_repo_schema():
    repo_schema = json.loads((SCHEMA_DIR / "rpo.v1.schema.json").read_text(encoding="utf-8"))
    packaged_schema = json.loads(PACKAGED_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert repo_schema == packaged_schema


def test_module_cli_entrypoint_works():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC_DIR)
    result = subprocess.run(
        [sys.executable, "-m", "rpo.cli", "validate", str(EXAMPLES_DIR / "01-simple-codegen.json")],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.stdout.strip() == "ok"
