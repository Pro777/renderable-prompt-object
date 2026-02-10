# RPO × Proof of Ship — Alignment Note

This repo treats prompts as shipped artifacts: structured inputs (RPO JSON) rendered deterministically into operational prompts.

## Deterministic rendering → behavioral receipts

RPO separates *what changed* (the JSON object) from *how it is presented* (the renderer). The UI renderer is intentionally deterministic:

- `src/rpo/render_ui.py` emits a stable section order and formatting for a given input object.
- Given the same RPO JSON, the rendered prompt string is expected to be identical (modulo newline normalization).

That determinism enables a receipt:

- The rendered prompt is the “behavioral contract” that a model will see.
- A reviewer can diff the RPO JSON and/or the rendered prompt and know exactly what the model was instructed to do.

## Schema diffs → proof-of-change

The schema (`schema/rpo.v1.schema.json`) defines the contractual surface:

- required fields: `mode`, `warm_state`, `hot_task`, `output_contract`
- prohibited drift: `additionalProperties: false` at each level

A change to the schema is a change to the allowed contract. In proof-of-ship terms:

- schema diff = proof that the *shape* of the contract changed
- schema versioning (e.g., `mode.version`) = explicit signal that consumers should treat the object as meaningfully revised

## Snapshot / characterization tests → ship receipts

Snapshot-style tests make “prompt shipping” behave like software shipping:

- `tests/test_smoke.py` validates an example against the schema and asserts that rendered output includes contractual sections.
- Example fixtures under `examples/` function as characterization inputs: they anchor expected rendering and validate that the renderer remains deterministic.

When these tests are executed in CI, they provide a receipt:

- *This exact object validated under this exact schema.*
- *This exact renderer produced this exact (or equivalently asserted) output.*

## Prompts as artifacts, not transient text

RPO’s design assumes:

- prompts should be reviewable and diffable like code
- renderers are contracts (the string output is not “just a prompt”; it is the shipped interface)
- test fixtures are part of the shipped surface (they document intended behavior and protect it)

In proof-of-ship terms, the combination of:

1) a structured RPO object,
2) a deterministic renderer,
3) schema validation, and
4) stable tests/examples

creates a chain of evidence that a given prompt behavior was authored, reviewed, and shipped deliberately.
