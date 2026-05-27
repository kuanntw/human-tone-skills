from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal

Scenario = Literal["academic_paper", "social_post", "blog_writing", "content_marketing", "educational_content"]


@dataclass
class ToneProfile:
    formality: int = 55
    warmth: int = 60
    confidence: int = 65
    directness: int = 55


@dataclass
class Constraints:
    preserve_terms: list[str] = field(default_factory=list)
    preserve_numbers: bool = True
    max_length_change_pct: int = 30
    forbidden_styles: list[str] = field(default_factory=list)


@dataclass
class RewriteInput:
    text: str
    scenario: Scenario
    locale: str = "zh-Hant"
    region: str = "TW"
    tone: ToneProfile = field(default_factory=ToneProfile)
    constraints: Constraints = field(default_factory=Constraints)
    output_mode: str = "minimal_edit"


@dataclass
class ValidationResult:
    preserve_terms_ok: bool
    preserve_numbers_ok: bool
    length_change_ok: bool
    semantic_drift_risk: Literal["low", "medium", "high"]
    missing_terms: list[str] = field(default_factory=list)
    number_diff: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class RewriteOutput:
    ai_trace_signals: list[dict]
    severity_summary: dict[str, int]
    rewrite_instruction: dict
    validation_result: dict
    change_log: list[str]

    def to_dict(self) -> dict:
        return asdict(self)
