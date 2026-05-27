from __future__ import annotations

from collections import Counter
from .analyzer import analyze_text
from .rewriter import build_rewrite_instruction
from .validator import validate_rewrite
from .schemas import RewriteInput, RewriteOutput


def run_pipeline(payload: RewriteInput, rewritten_text: str | None = None) -> RewriteOutput:
    signals = analyze_text(payload.text, payload.scenario)
    sev = Counter([s["severity"] for s in signals])
    rewrite_instruction = build_rewrite_instruction(
        payload.text, payload.scenario, payload.locale, payload.region, payload.tone.__dict__, payload.output_mode
    )
    rewritten = rewritten_text if rewritten_text is not None else payload.text
    validation = validate_rewrite(payload.text, rewritten, payload.constraints)
    change_log = [
        "analyze_text completed",
        "build_rewrite_instruction completed",
        "validate_rewrite completed",
    ]
    return RewriteOutput(signals, dict(sev), rewrite_instruction, validation.__dict__, change_log)
