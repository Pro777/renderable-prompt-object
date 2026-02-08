# RPO Repo Skill

Purpose: help an agent make safe, reviewable changes to Renderable Prompt Object (RPO), a prompt IR with schema validation and deterministic rendering.

## When to use this skill

Use this skill for tasks involving:
- RPO schema changes
- renderer behavior changes
- CLI validation/render behavior
- examples/docs/rubric/reference updates tied to schema or renderer behavior

## Canonical files

- Schema (source of truth): [`schema/rpo.v1.schema.json`](./schema/rpo.v1.schema.json)
- Packaged schema copy: [`src/rpo/data/rpo.v1.schema.json`](./src/rpo/data/rpo.v1.schema.json)
- Validator: [`src/rpo/schema.py`](./src/rpo/schema.py)
- UI renderer: [`src/rpo/render_ui.py`](./src/rpo/render_ui.py)
- CLI: [`src/rpo/cli.py`](./src/rpo/cli.py)
- Examples: [`examples/01-simple-codegen.json`](./examples/01-simple-codegen.json), [`examples/90-research-round.json`](./examples/90-research-round.json)
- Tests: [`tests/test_smoke.py`](./tests/test_smoke.py)
- Rubric: [`docs/rubric.md`](./docs/rubric.md)

## Required workflow

1. Keep scope narrow and reviewable.
2. If schema changes, update both schema copies:
   - [`schema/rpo.v1.schema.json`](./schema/rpo.v1.schema.json)
   - [`src/rpo/data/rpo.v1.schema.json`](./src/rpo/data/rpo.v1.schema.json)
3. Update renderer/CLI/tests as needed for behavior changes.
4. Keep examples minimal and valid.
5. Run verification commands.
6. If external behavior changes, update [`CHANGELOG.md`](./CHANGELOG.md).

## Verification commands

> Note: These commands intentionally use `PYTHONPATH=src` and `python -m rpo.cli`
> to ensure verification runs against the working tree, not an installed package.

Use these commands from repo root:

```bash
PYTHONPATH=src python3 -m pytest -q
PYTHONPATH=src python3 -m rpo.cli validate examples/01-simple-codegen.json
PYTHONPATH=src python3 -m rpo.cli validate examples/90-research-round.json
PYTHONPATH=src python3 -m rpo.cli render examples/01-simple-codegen.json --target ui
```

## Completion gate (mandatory)

A change is **not complete** unless all verification commands listed above pass
without modification or exception.

Partial success, skipped commands, or “passes locally but not in CI” do not meet
this bar.

## Guardrails

- Do not add secrets or sensitive data to examples.
- Do not claim provider/API targets exist unless implemented.
- Keep renderer output deterministic.
- Prefer explicit validation errors over silent fallback behavior.

## Done criteria

- Tests pass.
- Example validation passes.
- Docs reflect actual behavior.
- Diffs are small and easy to review.
