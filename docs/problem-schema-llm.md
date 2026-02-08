# Problem Schema Paradigm (LLM Guide)

This document defines the **operating contract** for any LLM consuming an RPO object.
All behavior must conform to this contract.

Schema source:
[`schema/rpo.v1.schema.json`](../schema/rpo.v1.schema.json)

## Field semantics (authoritative)

- `mode.rules`  
  Non-negotiable behavioral constraints. These always apply and override all other
  fields.

- `warm_state.*`  
  Maintained working context for this problem thread. Use as prior knowledge.
  Do not invent, infer, or extend facts beyond what is present.

- `hot_task.*`  
  The current request to execute now. This is the only active objective.

- `output_contract.*`  
  Required response format and bounds. Output must conform exactly.

## Processing order (mandatory)

1. Load and obey all `mode.rules`.
2. Load `warm_state` as context only; do not introduce new facts.
3. Execute `hot_task.prompt` to satisfy `hot_task.success_criteria`.
4. Emit output exactly in `output_contract.format`.
   - Respect `max_words` when present.

Deviation from this order is a contract violation.

## Conflict policy (explicit)

- If `hot_task` conflicts with `mode.rules`:
  - Follow `mode.rules`.
  - Report the conflict clearly and concisely.

- If `warm_state.facts` conflict with `hot_task`:
  - Treat `warm_state.facts` as prior context.
  - Execute cautiously and explicitly call out uncertainty or conflict.

- If `output_contract` constrains depth or completeness:
  - Satisfy the contract first.
  - Summarize what was omitted and why.

## Determinism requirements

- Preserve section order when rendering via
  [`src/rpo/render_ui.py`](../src/rpo/render_ui.py).
- Do not reorder lists or fields unless explicitly instructed.
- Prefer literal field values over paraphrase for:
  - constraints
  - rules
  - success criteria

## Safety and quality checks (required before final output)

Before emitting a response, confirm:

- The `hot_task.success_criteria` string is satisfied (it may contain an internal checklist).
- No `mode.rules` are violated.
- The required `output_contract.format` is fully respected.
- All referenced inputs are present and accounted for.

If execution is blocked:
- State **exactly** what input is missing.
- Do not guess or fabricate.

## Anti-patterns (forbidden)

- Mixing warm context into `mode.rules`.
- Introducing new assumptions outside `warm_state.facts`.
- Ignoring `output_contract` due to task breadth or complexity.
- Treating `hot_task.inputs` as decorative metadata rather than required artifacts.
