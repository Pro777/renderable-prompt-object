from __future__ import annotations

from typing import Any, Dict


def _nonempty_lines(items: list[str]) -> list[str]:
    return [x for x in (i.strip() for i in items) if x]


def render_ui(rpo: Dict[str, Any]) -> str:
    """Render an RPO object into a Chat-UI-friendly prompt.

    Deterministic by construction: this is meant to be snapshot-testable.
    """

    mode = rpo.get("mode") or {}
    warm = rpo.get("warm_state") or {}
    hot = rpo.get("hot_task") or {}
    contract = rpo.get("output_contract") or {}

    parts: list[str] = []

    parts.append(f"## RULES (mode: {mode.get('name')} v{mode.get('version')})")
    rules = (mode.get("rules") or "").strip()
    if rules:
        parts.append(rules)

    parts.append("")
    parts.append("## STATE")
    goal = (warm.get("goal") or "").strip()
    if goal:
        parts.append(f"Goal: {goal}")

    constraints = _nonempty_lines(warm.get("constraints") or [])
    if constraints:
        parts.append("Constraints:")
        parts.extend([f"- {c}" for c in constraints])

    facts = _nonempty_lines(warm.get("facts") or [])
    if facts:
        parts.append("Facts:")
        parts.extend([f"- {f}" for f in facts])

    decisions = _nonempty_lines(warm.get("decisions") or [])
    if decisions:
        parts.append("Decisions:")
        parts.extend([f"- {d}" for d in decisions])

    next_actions = _nonempty_lines(warm.get("next_actions") or [])
    if next_actions:
        parts.append("Next actions:")
        parts.extend([f"- {a}" for a in next_actions])

    parts.append("")
    parts.append("## TASK")
    prompt = (hot.get("prompt") or "").strip()
    if prompt:
        parts.append(prompt)

    success = (hot.get("success_criteria") or "").strip()
    if success:
        parts.append(f"Success: {success}")

    parts.append("")
    parts.append("## OUTPUT")
    fmt = (contract.get("format") or "").strip()
    max_words = contract.get("max_words")
    if fmt and max_words:
        parts.append(f"Format: {fmt} | Max: {max_words} words")
    elif fmt:
        parts.append(f"Format: {fmt}")

    return "\n".join(parts).rstrip() + "\n"
