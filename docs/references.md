# References (Receipts)

RPO argues that prompts should be treated as software artifacts: schema, validation, rendering, and tests.

## Primary references used by this repo

- JSON Schema Draft 2020-12: [json-schema.org/specification](https://json-schema.org/specification)
  - Why it matters: RPO v1 is defined as strict JSON Schema in [`schema/rpo.v1.schema.json`](../schema/rpo.v1.schema.json).
- Python `jsonschema` library docs: [python-jsonschema.readthedocs.io](https://python-jsonschema.readthedocs.io/en/stable/)
  - Why it matters: [`src/rpo/schema.py`](../src/rpo/schema.py) validates objects with `Draft202012Validator`.
- Python `importlib.resources` docs: [docs.python.org/importlib.resources](https://docs.python.org/3/library/importlib.resources.html)
  - Why it matters: packaged schema loading in [`src/rpo/schema.py`](../src/rpo/schema.py) must work after install.
- Keep a Changelog: [keepachangelog.com](https://keepachangelog.com/en/1.1.0/)
  - Why it matters: release discipline in [`CHANGELOG.md`](../CHANGELOG.md).

## Engineering patterns RPO adopts

- Intermediate Representation (IR) pattern: [wikipedia.org/wiki/Intermediate_representation](https://en.wikipedia.org/wiki/Intermediate_representation)
  - Why it matters: one structured source, many render targets.
- Golden/snapshot testing pattern: [martinfowler.com/bliki/GoldenMaster.html](https://martinfowler.com/bliki/GoldenMaster.html)
  - Why it matters: renderer output is a contract and should not drift silently.

## Local repo anchors

- Schema contract: [`schema/rpo.v1.schema.json`](../schema/rpo.v1.schema.json)
- Packaged schema copy: [`src/rpo/data/rpo.v1.schema.json`](../src/rpo/data/rpo.v1.schema.json)
- Validator: [`src/rpo/schema.py`](../src/rpo/schema.py)
- UI renderer: [`src/rpo/render_ui.py`](../src/rpo/render_ui.py)
- CLI entrypoint: [`src/rpo/cli.py`](../src/rpo/cli.py)
- Examples: [`examples/01-simple-codegen.json`](../examples/01-simple-codegen.json), [`examples/90-research-round.json`](../examples/90-research-round.json)
- Tests: [`tests/test_smoke.py`](../tests/test_smoke.py)
