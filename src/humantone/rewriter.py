from __future__ import annotations

from .presets import TONE_PRESETS


def build_rewrite_instruction(text: str, scenario: str, locale: str, region: str, tone: dict, mode: str = "minimal_edit") -> dict:
    base_tone = TONE_PRESETS.get(scenario, TONE_PRESETS["blog_writing"])
    merged = {**base_tone, **(tone or {})}
    return {
        "scenario": scenario,
        "locale": locale,
        "region": region,
        "mode": mode,
        "tone": merged,
        "instruction": (
            "保持事實、數字、引文、構念與假設編號不變；"
            "降低模板轉折、避免每段結尾制式總結；"
            "學術場景請保留嚴謹語氣，避免社群口吻。"
        ),
        "text_preview": text[:200],
    }
