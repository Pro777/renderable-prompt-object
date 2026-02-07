# Rubric: what RPO is optimizing for

RPO (Renderable Prompt Object) is a **prompt intermediate representation** (IR) plus deterministic renderers.

It’s meant to make prompt work behave more like software engineering:

- **diffable** (structured fields, not one giant string)
- **testable** (snapshot tests for rendered outputs)
- **portable** (render to UI and API targets)
- **auditable** (explicit constraints, decisions, artifacts)

## Core claims

1) **IR → renderer reduces drift**
- You can change content without changing structure.
- You can review changes as data, not prose.

2) **System vs user split is explicit**
- Cold/warm context belongs in system.
- Hot task belongs in user.

3) **Renderers are contracts**
- The rendered output is the artifact.
- Snapshot tests protect that contract.

## Non-goals

- RPO is not an agent framework.
- RPO does not guarantee correctness.
- RPO does not replace retrieval, evals, or verification gates.

## Verification (what we expect to be true)

- `rpo validate` rejects invalid objects with human-readable errors.
- `rpo render` is deterministic for a given input.
- Examples in `examples/` render to stable outputs under CI.
