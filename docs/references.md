# References (Receipts)

RPO argues that prompts should be treated as **software artifacts**: versioned schema,
validation, rendering, and tests.  
This section documents the primary technical and conceptual references that inform that
design.

## Primary references used by this repo

- **JSON Schema Draft 2020-12**  
  https://json-schema.org/specification  
  - *Why it matters*: RPO v1 is defined as a strict JSON Schema in  
    [`schema/rpo.v1.schema.json`](../schema/rpo.v1.schema.json).  
    This establishes a formal, machine-verifiable contract for prompt objects.

- **Python `jsonschema` library**  
  https://python-jsonschema.readthedocs.io/en/stable/  
  - *Why it matters*: [`src/rpo/schema.py`](../src/rpo/schema.py) validates RPOs using
    `Draft202012Validator`, enforcing schema correctness at runtime.

- **Python `importlib.resources`**  
  https://docs.python.org/3/library/importlib.resources.html  
  - *Why it matters*: RPO schemas are packaged and must be loadable after installation.
    This ensures schema validation works identically in development and installed
    environments.

- **Keep a Changelog**  
  https://keepachangelog.com/en/1.1.0/  
  - *Why it matters*: RPO treats prompt formats as evolving APIs.
    [`CHANGELOG.md`](../CHANGELOG.md) documents intentional, reviewable changes.

## Engineering patterns RPO adopts

- **Intermediate Representation (IR) pattern**  
  https://en.wikipedia.org/wiki/Intermediate_representation  
  - *Why it matters*: RPO acts as a single structured source of truth that can be rendered
    into multiple targets (UI, CLI, LLM prompts, artifacts) without duplication or drift.

- **Golden Master / Characterization Testing**  
  https://en.wikipedia.org/wiki/Characterization_test  
  - *Why it matters*: Renderer output is treated as a behavioral contract.
    Once captured, output must not change silently.

  - *Context*: The “Golden Master” concept is commonly discussed under the name
    **Characterization Tests**, popularized by Michael Feathers (*Working Effectively with
    Legacy Code*). It is also discussed by **[Martin Fowler](https://martinfowler.com/)**
    in the context of protecting existing behavior during refactoring, even though Fowler
    no longer hosts a dedicated Bliki page under the “Golden Master” name.

  - *Why RPO cares*: Prompts and renderers are *behavioral interfaces*. Snapshot-style
    tests provide proof that refactors, renderer changes, or formatting tweaks do not alter
    meaning unintentionally.

## Additional conceptual context

- **Treat configuration and data formats as APIs**  
  (Widely accepted engineering practice; see Fowler, Feathers, and API evolution
  literature.)  
  - *Why it matters*: RPO schemas are versioned, validated, and documented because
    downstream systems depend on their stability in the same way they depend on code
    APIs.

- **Approval / Snapshot Testing (related practice)**  
  https://approvaltests.com/  
  - *Why it matters*: This ecosystem reinforces the idea that complex outputs
    (text, documents, prompts) should be locked and reviewed explicitly when they change.

## Local repo anchors

- Schema contract: [`schema/rpo.v1.schema.json`](../schema/rpo.v1.schema.json)
- Packaged schema copy: [`src/rpo/data/rpo.v1.schema.json`](../src/rpo/data/rpo.v1.schema.json)
- Validator: [`src/rpo/schema.py`](../src/rpo/schema.py)
- UI renderer: [`src/rpo/render_ui.py`](../src/rpo/render_ui.py)
- CLI entrypoint: [`src/rpo/cli.py`](../src/rpo/cli.py)
- Examples:  
  [examples/01-simple-codegen.json](../examples/01-simple-codegen.json)  
  [examples/90-research-round.json](../examples/90-research-round.json)
- Tests: [`tests/test_smoke.py`](../tests/test_smoke.py)
