from __future__ import annotations

import re
from collections import Counter
from typing import Any

ABSTRACT_NOUNS = "機制|脈絡|意涵|歷程|條件|轉化|作用|模型|路徑|結構"

RULES = [
    ("template_transition_overuse", r"整體而言|由此可見|值得注意的是|換言之|基於上述", "medium"),
    ("parallel_structure_overuse", r"一方面.{0,30}另一方面|不僅.{0,20}(也|而且)", "medium"),
    ("generic_conclusion_sentence", r"因此，本研究|整體而言，本研究", "high"),
    ("repeated_research_gap_formula", r"目前研究.*不足.*因此本研究", "medium"),
    ("ai_like_literature_review_pattern", r"問題.{0,40}然而.{0,40}因此.{0,40}本研究", "high"),
]


def _sentence_lengths(text: str) -> list[int]:
    sents = [s.strip() for s in re.split(r"[。！？!?]", text) if s.strip()]
    return [len(s) for s in sents]


def analyze_text(text: str, scenario: str = "academic_paper") -> list[dict[str, Any]]:
    signals: list[dict[str, Any]] = []
    for rid, pat, sev in RULES:
        m = re.findall(pat, text)
        if m:
            signals.append({"id": rid, "severity": sev, "count": len(m), "evidence": m[:3]})

    abstract_hits = re.findall(ABSTRACT_NOUNS, text)
    if len(abstract_hits) >= 4:
        signals.append({"id": "abstract_noun_density", "severity": "medium", "count": len(abstract_hits), "evidence": list(Counter(abstract_hits).keys())[:5]})

    lengths = _sentence_lengths(text)
    if lengths and (max(lengths) - min(lengths) <= 8):
        signals.append({"id": "over_smooth_paragraph_flow", "severity": "low", "count": len(lengths), "evidence": [f"sentence_lengths={lengths[:6]}"]})

    if scenario == "academic_paper" and re.search(r"本研究認為|本文推論|此結果顯示", text) and not re.search(r"我們主張|本研究主張|研究者認為", text):
        signals.append({"id": "lack_of_authorial_stance", "severity": "medium", "count": 1, "evidence": ["缺乏明確研究者立場句"]})
    return signals
