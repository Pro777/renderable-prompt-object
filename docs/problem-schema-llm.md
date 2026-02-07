# Problem Schema Paradigm (LLM Guide)

Use this as the operating contract when consuming an RPO object.

Schema source: [`schema/rpo.v1.schema.json`](../schema/rpo.v1.schema.json)

## Field semantics
- `mode.rules`: hard behavioral constraints that always apply.
- `warm_state.*`: maintained working memory for this problem thread.
- `hot_task.*`: the current request that should be executed now.
- `output_contract.*`: response format and bounds.

## Processing order (required)

1. Load and obey `mode.rules`.
2. Use `warm_state` as context; do not invent missing facts.
3. Execute `hot_task.prompt` to satisfy `hot_task.success_criteria`.
4. Emit output exactly in `output_contract.format` and respect `max_words` when present.

## Conflict policy
- If `hot_task` conflicts with `mode.rules`, follow `mode.rules` and report the conflict.
- If `warm_state.facts` conflict with `hot_task`, treat facts as prior context and call out uncertainty.
- If `output_contract` conflicts with task depth, satisfy contract first and summarize what was omitted.

## Determinism expectations
- Keep section order stable when rendering via [`src/rpo/render_ui.py`](../src/rpo/render_ui.py).
- Do not reorder list items unless explicitly asked.
- Prefer literal field values over paraphrase for constraints and success criteria.

## Safety and quality checks before final output
- Confirm every success criterion is addressed.
- Confirm no rule in `mode.rules` is violated.
- Confirm required output format is respected.
- If blocked by missing input, state exactly what is missing.

## Anti-patterns
- Mixing warm context into rules.
- Hiding new assumptions outside `warm_state.facts`.
- Ignoring `output_contract` because the task is broad.
- Treating `inputs` as decorative metadata instead of task-relevant artifacts.
