# AGENTS.md

This repo is designed to be worked on with AI assistance.

## What this repo is
RPO is a prompt intermediate representation (IR): a JSON schema plus renderers.

## Ground rules
- Keep changes small and reviewable.
- Don’t expand scope casually: prefer shipping v0/v1 with a narrow contract.
- Keep docs honest (no “pip install works” claims until it does).
- If you reference a repo file in markdown, link it.

## Suggested verification
- Validate examples against the schema.
- Render an example to the UI target and ensure output is deterministic.

## Repo hygiene
- No secrets in examples.
- Keep examples minimal and purposeful.
