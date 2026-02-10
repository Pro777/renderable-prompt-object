# RPO Failure Modes (Deterministic Response Template)

Use this template when execution cannot proceed without violating the RPO contract.

## Output rules

- No apology language.
- No speculative fixes.
- No unstated assumptions.
- Reference the exact RPO field paths that caused the failure.

---

## FAILURE

### Class
One of:
- `missing_required_inputs`
- `rules_task_conflict`
- `schema_violation`
- `output_contract_infeasible`

### Reason
A single sentence stating why execution cannot proceed.

### Blocking condition (verbatim)
- Field path(s):
  - `<path>`
- Trigger:
  - `<verbatim rule / requirement / constraint>`

### Evidence
- Observed:
  - `<observable fact from the provided RPO or inputs>`
- Not present:
  - `<missing field / missing artifact / missing value>`

### Required action
- Provide exactly:
  1. `<required input or decision>`
  2. `<required input or decision>`

### Allowed next step
One of:
- `halt`
- `request_inputs_then_resume`

---

## Class-specific requirements

### 1) `missing_required_inputs`
Use when `hot_task.prompt` or `hot_task.success_criteria` requires an artifact/value not present in `hot_task.inputs` (or not provided in the conversation).

- Blocking condition must list each missing artifact.
- Required action must specify how each artifact should be provided (file path, pasted text, URL).

### 2) `rules_task_conflict`
Use when completing `hot_task` would violate `mode.rules`.

- Blocking condition must quote the conflicting `mode.rules` clause verbatim.
- Required action must request one of:
  1) a corrected `hot_task` that fits the rules, or
  2) a revised `mode.rules` (explicitly acknowledging the change).

### 3) `schema_violation`
Use when the RPO object fails validation against `schema/rpo.v1.schema.json`.

- Evidence must include the validator error(s) verbatim.
- Required action must request a corrected RPO object (no partial execution).

### 4) `output_contract_infeasible`
Use when the requested work cannot be completed while conforming to `output_contract`.

- Blocking condition must cite the exact `output_contract.*` constraint.
- Required action must request one of:
  1) a relaxed `output_contract` (e.g., higher `max_words`), or
  2) a narrowed `hot_task` scope.
