from __future__ import annotations

from .presets import PROMPT_TEMPLATES, TONE_PRESETS


def rewrite_text(text: str, scenario: str, preserve_terms: list[str] | None = None, preserve_numbers: bool = True) -> dict:
    preset = TONE_PRESETS[scenario]
    prompt = PROMPT_TEMPLATES[scenario].format(domain=scenario)
    diagnostics = {"ai_trace_signals": [], "semantic_drift_risk": "low", "policy_flags": []}
    change_log = ["placeholder: integrate LLM rewriter"]
    rewritten = text
    if preserve_terms:
        for t in preserve_terms:
            if t not in rewritten:
                diagnostics["semantic_drift_risk"] = "medium"
    if preserve_numbers:
        pass
    return {
        "prompt": prompt,
        "rewrites": [{"id": "v1", "text": rewritten, "style_profile": preset, "readability_notes": []}],
        "diagnostics": diagnostics,
        "change_log": change_log,
    }
