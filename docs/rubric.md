# Rubric: What RPO Optimizes For

RPO (Renderable Prompt Object) is a **prompt intermediate representation (IR)** with
deterministic renderers. Its purpose is to make prompt work **reviewable, testable,
and evolvable** with the same rigor as code.

This rubric defines the **pass/fail criteria** for changes to the schema, renderers,
or surrounding tooling.

## Problem-schema rubric

Use this checklist to evaluate any schema or renderer change.

### 1. Separation
- Rules, persistent state, active task, and output contract live in **distinct fields**.
- No field implicitly carries another field’s responsibility.
- Cross-field coupling must be explicit and intentional.

### 2. Determinism
- The same input object always produces **identical rendered output**.
- Renderer ordering, layout, and section boundaries are stable and explicit.
- Formatting changes are considered behavior changes and must be reviewed as such.

### 3. Strictness
- Unknown fields **fail validation**.
- Required fields remain required unless changed via an intentional, versioned
  schema update.
- Typos and accidental extensions are treated as errors, not tolerated inputs.

### 4. Reviewability
- Any behavior change maps to a **clear, minimal JSON diff**.
- Schema or renderer changes include documented rationale
  (docs, comments, or changelog).
- Reviewers can understand *what changed and why* without reverse-engineering output.

### 5. Portability
- The schema remains **target-agnostic**.
- Renderers handle target-specific concerns (UI, CLI, LLM text, artifacts).
- Adding a new renderer must not require schema shape changes for existing fields.

## Decision tradeoffs (explicitly accepted)

- **Strong validation** (`additionalProperties: false`) catches drift early,
  but reduces ad-hoc flexibility.
- **Deterministic rendering** improves testability and diff-based review,
  but limits stylistic freedom.
- **Explicit warm state** improves handoffs and auditing,
  but requires ongoing curation.
- **Required output contracts** enable downstream automation,
  but can constrain early or exploratory tasks.

These tradeoffs are intentional and aligned with RPO’s goals.

## Non-goals

RPO explicitly does **not** aim to be:
- An agent runtime
- An evaluation framework
- A truth or correctness guarantee
- A replacement for retrieval, tools, or external verification

## Verification gates

Changes are **not acceptable** unless the required verification commands pass.
ds apply.

At minimum, the following must remain true:

- Examples validate against the canonical schema:
  [`schema/rpo.v1.schema.json`](../schema/rpo.v1.schema.json)
- The packaged schema matches the canonical schema:
  [`src/rpo/data/rpo.v1.schema.json`](../src/rpo/data/rpo.v1.schema.json)
- Rendering is deterministic for a given input (UI renderer):
  [`src/rpo/render_ui.py`](../src/rpo/render_ui.py)
- Regressions are covered by snapshot or smoke tests:
  [`tests/test_smoke.py`](../tests/test_smoke.py)
