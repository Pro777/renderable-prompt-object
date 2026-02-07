# Rubric: What RPO Optimizes For

RPO (Renderable Prompt Object) is a prompt IR with deterministic renderers. The goal is to make prompt work reviewable and testable like code.

## Problem-schema rubric

Use this as a pass/fail rubric for any schema or renderer change.

1. **Separation**
- Rules, persistent state, active task, and output contract are separate fields.
- No field silently carries another field’s responsibility.

2. **Determinism**
- Same input object yields identical render output.
- Renderer ordering is stable and explicit.

3. **Strictness**
- Unknown fields fail validation.
- Required fields stay required unless versioned schema change is intentional.

4. **Reviewability**
- A change in behavior maps to a clear JSON diff.
- Rationale for schema changes is documented in nearby docs/changelog.

5. **Portability**
- Schema remains target-agnostic; renderer handles target specifics.
- Adding a renderer should not require schema shape changes for existing fields.

## Decision tradeoffs

- Strong validation (`additionalProperties: false`) catches drift early, but reduces ad-hoc flexibility.
- Deterministic rendering improves testability, but limits stylistic output freedom.
- Explicit warm state improves handoffs and auditing, but requires ongoing curation.
- Required output contract improves downstream automation, but can constrain exploratory tasks.

## Non-goals

- Not an agent runtime.
- Not an eval framework.
- Not a truth/correctness guarantee.
- Not a replacement for retrieval or tool verification.

## Verification gates

- Validate examples against [`schema/rpo.v1.schema.json`](../schema/rpo.v1.schema.json).
- Ensure packaged schema matches repo schema: [`src/rpo/data/rpo.v1.schema.json`](../src/rpo/data/rpo.v1.schema.json).
- Keep renderer output deterministic in [`src/rpo/render_ui.py`](../src/rpo/render_ui.py).
- Keep regressions covered in [`tests/test_smoke.py`](../tests/test_smoke.py).
