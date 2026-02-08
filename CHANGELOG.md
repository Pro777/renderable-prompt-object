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

### Changed
- Clarified developer workflow expectations for agent-assisted changes via
  [`SKILL.md`](./SKILL.md).
- Refined rubric language in [`docs/rubric.md`](./docs/rubric.md) and reference guidance in
  [`docs/references.md`](./docs/references.md) to align with deterministic, schema-first behavior.

### Fixed

## [1.0.0a1] - 2026-02-07

### Added
- Minimal RPO v1 schema + validator (`rpo validate`).
- Deterministic Chat UI renderer (`rpo render --target ui`).
- Example RPO objects under [`examples/`](./examples/).
