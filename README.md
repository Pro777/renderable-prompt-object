# Renderable Prompt Object (RPO)

A **prompt intermediate representation** (IR) you can validate, diff, and compile into multiple targets.

**Thesis:** schema stays rich; renderer stays lean.

## 🧾 What it produces (above the fold)

### Input (RPO JSON)
```json
{
  "mode": {"name": "codegen", "version": 1, "rules": "Write clean, tested Python."},
  "warm_state": {"goal": "Ship a tiny CLI", "constraints": ["Be concise"], "facts": [], "decisions": [], "next_actions": []},
  "hot_task": {"type": "codegen", "prompt": "Write a function...", "success_criteria": "...", "inputs": []},
  "output_contract": {"format": "markdown", "max_words": 200}
}
```

### Output (Chat UI target)
```text
## RULES (mode: codegen v1)
Write clean, tested Python.

## STATE
Goal: Ship a tiny CLI
Constraints:
- Be concise

## TASK
Write a function...
Success: ...

## OUTPUT
Format: markdown | Max: 200 words
```

## 🚀 Install (planned)
```bash
python -m pip install renderable-prompt-object
```

## 🛠️ CLI (planned)
```bash
rpo validate examples/01-simple-codegen.json
rpo render examples/01-simple-codegen.json --target ui
rpo render examples/01-simple-codegen.json --target api --provider openai
```

## 📎 References (receipts)
If you want the “why” behind the shape:
- `docs/rubric.md`
- `docs/references.md`

## License
MIT.
