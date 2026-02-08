# Renderable Prompt Object (RPO)

RPO is a **prompt intermediate representation** (IR): a small JSON schema for capturing *rules + state + task + output contract*, then **rendering** it into the exact prompt formats your tools need.

> Status: early v0 (spec/examples first; CLI/package catching up). Created 2026-02-07.

## ✅ What it is
- A **diffable** prompt object (not one giant string)
- A **validator** (schema + constraints)
- A set of **renderers** (Chat UI, API/provider formats)

## 🧠 Why it matters
Prompts rot because they’re unreviewable blobs. RPO makes prompt changes:
- reviewable (data diffs)
- testable (snapshot rendered outputs)
- portable (one object → many targets)

## 🎯 Who should use it
- People shipping agents/prompts in teams (code review / versioning)
- Anyone maintaining “modes” or reusable prompt templates
- Tooling authors who want a clean boundary: **schema stays rich; renderer stays lean**

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

## 🚀 Install
```bash
python -m pip install renderable-prompt-object
```

## 🛠️ CLI
```bash
rpo validate examples/01-simple-codegen.json
rpo render examples/01-simple-codegen.json --target ui
```

(Provider/API rendering is intentionally out of scope for this early release.)

Examples:
- [`examples/01-simple-codegen.json`](./examples/01-simple-codegen.json)
- [`examples/90-research-round.json`](./examples/90-research-round.json) (paired with [`modes/research.mode.md`](./modes/research.mode.md))

## 🤝 Contribution Workflow
- Agent/reviewer workflow and completion gates: [`SKILL.md`](./SKILL.md)
- Collaboration guardrails: [`AGENTS.md`](./AGENTS.md)

## 📎 References (receipts)
If you want the “why” behind the shape:
- [`docs/rubric.md`](./docs/rubric.md)
- [`docs/references.md`](./docs/references.md)

## License
MIT.
