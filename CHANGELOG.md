# Changelog

All notable changes to this project will be documented in this file.

The format is based on *Keep a Changelog*, and this project aims to follow Semantic Versioning when releases are cut.

## [Unreleased]

### Added
- Repository contribution skill document at [`SKILL.md`](./SKILL.md) with explicit
  verification gates for schema, renderer, and CLI changes.
- Problem-schema documentation pair for humans and LLMs:
  [`docs/problem-schema-human.md`](./docs/problem-schema-human.md) and
  [`docs/problem-schema-llm.md`](./docs/problem-schema-llm.md).
- Renderer regression tests in [`tests/test_render_ui.py`](./tests/test_render_ui.py) covering
  deterministic output, required sections, and `hot_task.inputs` presence/absence behavior.
- PR policy gate workflow at [`/.github/workflows/policy-gates.yml`](./.github/workflows/policy-gates.yml)
  with docs/changelog enforcement logic in [`/.github/scripts/pr_docs_gate.py`](./.github/scripts/pr_docs_gate.py).
- Copilot review auto-resolve workflow at [`/.github/workflows/copilot-autoresolve.yml`](./.github/workflows/copilot-autoresolve.yml)
  with thread triage logic in [`/.github/scripts/copilot_autoresolve.py`](./.github/scripts/copilot_autoresolve.py).

### Changed
- Clarified developer workflow expectations for agent-assisted changes via
  [`SKILL.md`](./SKILL.md).
- Refined rubric language in [`docs/rubric.md`](./docs/rubric.md) and reference guidance in
  [`docs/references.md`](./docs/references.md) to align with deterministic, schema-first behavior.
- CLI JSON loading now rejects non-object top-level JSON values with explicit errors in
  [`src/rpo/cli.py`](./src/rpo/cli.py).
- Test path handling in [`tests/test_smoke.py`](./tests/test_smoke.py) now resolves repo-root
  paths so tests are stable across working directories.

### Fixed
- Schema parity test now compares parsed JSON objects instead of raw file text in
  [`tests/test_smoke.py`](./tests/test_smoke.py).
- UI renderer contract explicitly omits the `Inputs` section when `hot_task.inputs` is missing
  or empty in [`src/rpo/render_ui.py`](./src/rpo/render_ui.py).

## [1.0.0a1] - 2026-02-07

### Added
- Minimal RPO v1 schema + validator (`rpo validate`).
- Deterministic Chat UI renderer (`rpo render --target ui`).
- Example RPO objects under [`examples/`](./examples/).
