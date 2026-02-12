# Renderable Prompt Object (RPO) — Plain-English Explainer

## The one-sentence version

RPO turns AI prompts from messy blobs of text into structured, reviewable data objects.

## The problem

Most AI prompts are just big strings. They're hard to review, hard to compare, hard to version control, and hard to port between different AI systems. When someone changes a prompt, the diff looks like gibberish — just a wall of text with a few words swapped somewhere in the middle.

This matters because prompts are becoming critical infrastructure. Teams ship agents whose behavior is entirely determined by their prompts, but nobody can meaningfully code-review a prompt change the way they'd review a code change.

## What RPO does

RPO says: a prompt is really four things, so store them as four separate fields:

| Field              | What it holds                                                      | Analogy                        |
|-------------------|--------------------------------------------------------------------|--------------------------------|
| **Mode** (rules)   | The personality and style rules. "Be concise. Use Python."         | The job description            |
| **Warm State**      | What we already know — goal, constraints, facts, decisions so far. | The briefing document          |
| **Hot Task**        | What we need done right now, plus what success looks like.         | The specific work order        |
| **Output Contract** | What format the answer should come in. Markdown? JSON? How long?   | The delivery requirements      |

You write this once as a JSON object. A **renderer** then converts it into whatever format your target needs — a chat UI, an API call, a CLI prompt. Same content, different packaging.

## Why this matters

**Reviewable diffs.** When someone changes a prompt, the diff shows you exactly what changed: "they added a new constraint to warm_state" or "they changed the success criteria." Instead of squinting at two giant text blobs.

**Testability.** You can snapshot a rendered prompt and assert that it hasn't changed unexpectedly. Same input always produces the same output (deterministic rendering).

**Portability.** One RPO object can render to multiple targets. Write the prompt once, use it with Claude, GPT, Gemini, a chat UI, or a CLI tool — without manually reformatting each time.

**Fewer tokens.** Structured rendering can omit empty sections and compress formatting, sending only what's needed to each target.

## A concrete example

Instead of this string:

> "You are a code reviewer. Be concise and focus on correctness. The project uses Python 3.10 with pytest. We've already decided to use dataclasses over Pydantic. Review this pull request for bugs and suggest fixes. Output your review as markdown with no more than 300 words."

You write this object:

```json
{
  "mode": { "name": "code-review", "version": 1, "rules": "Be concise. Focus on correctness." },
  "warm_state": {
    "goal": "Maintain code quality",
    "constraints": ["Python 3.10", "pytest"],
    "facts": [],
    "decisions": ["Use dataclasses over Pydantic"],
    "next_actions": []
  },
  "hot_task": {
    "type": "review",
    "prompt": "Review this pull request for bugs and suggest fixes.",
    "success_criteria": "All bugs identified with suggested fixes.",
    "inputs": []
  },
  "output_contract": { "format": "markdown", "max_words": 300 }
}
```

Both say the same thing. But the second one is diffable, versionable, and machine-readable.

## What RPO is not

- It is **not a prompt library** or a collection of pre-written prompts. It's a format for structuring any prompt.
- It is **not tied to a specific AI provider**. The schema is target-agnostic; renderers handle provider differences.
- It is **not a prompt optimizer**. It doesn't rewrite your prompts to be better. It makes them reviewable and portable as-is.
