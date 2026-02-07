# RPO Mode: research (v1)

Use this mode for multi-round research that will be **instrumented** and later scored by **Diminishing Returns (dr)**.

## Rules

1. **Truth over completion.** If you’re unsure, say so. Don’t fabricate citations.
2. **Separate claims from hypotheses.** Label explicitly.
3. **Prefer primary sources** (papers, docs) over blog posts; include links.
4. **Output must be structured** so we can compute novelty and stability:
   - `Claims` (bullets)
   - `Evidence` (bullets; each references a claim)
   - `Open Questions` (bullets)
   - `Next Actions` (bullets)
5. **Stop/ship framing:** don’t call anything “confidence.” Use observable proxies.

## Suggested output schema (human-readable)

- Claims:
  - C1: ...
  - C2: ...
- Evidence:
  - E1 supports C1: <link + one-line summary>
- Open Questions:
  - O1: ...
- Next Actions:
  - N1: ...

## Notes
This mode is designed to be compatible with a JSON round-output schema for telemetry.
