# Problem Schema Paradigm (Human Guide)

RPO treats a prompt as a **problem schema**, not a prose blob.

A *problem schema* means every prompt instance must answer four distinct questions,
each in its own explicit field:

1. What standing rules govern behavior? (`mode`)
2. What context is already known and should persist? (`warm_state`)
3. What is being asked right now? (`hot_task`)
4. What shape should the answer take? (`output_contract`)

The schema is formally defined in
[`schema/rpo.v1.schema.json`](../schema/rpo.v1.schema.json).

## Why this shape

### 1. Mode is versioned on purpose
- **Choice**: `mode` requires `name`, `version`, and `rules`.
- **Why**: rules change over time; versioning prevents *silent prompt drift*.
- **Tradeoff**: more bookkeeping when changing wording, but changes become explicit,
  reviewable, and auditable.

### 2. Warm state is explicit and bounded
- **Choice**: `goal`, `constraints`, `facts`, `decisions`, and `next_actions` are
  first-class fields.
- **Why**: this forces teams to separate *stable working context* from the current ask.
- **Tradeoff**: writers must actively curate state instead of dumping everything into
  a single paragraph.

### 3. Hot task stays hot
- **Choice**: `hot_task` isolates the current objective
  (`type`, `prompt`, `success_criteria`, `inputs`).
- **Why**: task updates are frequent; isolating them keeps diffs small and reviewable.
- **Tradeoff**: some repetition across task instances is expected and intentional.

### 4. Output contract is not optional
- **Choice**: `output_contract.format` is required; `max_words` is optional.
- **Why**: an explicit output target improves determinism and downstream parsing.
- **Tradeoff**: early exploration can feel constrained; teams may need a permissive
  “explore” format during ideation.

## Design decisions and alternatives considered

### Decision: schema first, renderer second
- **Chosen**: keep the schema rich and the renderer deterministic.
- **Alternative**: keep prompt text as the source of truth and parse it later.
- **Why rejected**: reverse-parsing prose introduces ambiguity and brittle tooling.

### Decision: strict JSON Schema with `additionalProperties: false`
- **Chosen**: reject unknown fields.
- **Alternative**: permit extra keys for flexibility.
- **Why rejected**: silent typos become hidden behavior changes.

### Decision: deterministic UI rendering
- **Chosen**: one stable text layout from
  [`src/rpo/render_ui.py`](../src/rpo/render_ui.py).
- **Alternative**: stylistic freedom in renderer formatting.
- **Why rejected**: unstable output breaks snapshot tests and diff-based review.

## What this paradigm is not
- Not an agent framework.
- Not an eval system.
- Not a correctness guarantee.

These non-goals are captured explicitly in
[`docs/rubric.md`](./rubric.md).

## Practical usage checklist
- Validate every object with `rpo validate` via
  [`src/rpo/cli.py`](../src/rpo/cli.py).
- Keep examples small and purposeful under
  [`examples/`](../examples/).
- Snapshot renderer output in tests
  (see [`tests/test_smoke.py`](../tests/test_smoke.py)).
- When changing the schema, update both canonical and packaged copies:
  - [`schema/rpo.v1.schema.json`](../schema/rpo.v1.schema.json)
  - [`src/rpo/data/rpo.v1.schema.json`](../src/rpo/data/rpo.v1.schema.json)
