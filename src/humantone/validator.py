from __future__ import annotations

import re
from .schemas import Constraints, ValidationResult


NUM_PAT = r"\b\d+(?:\.\d+)?%?\b|R²|R2|β|p\s*[<=>]\s*0?\.\d+|H\d+[a-z]?"
CIT_PAT = r"\([^\)]*\d{4}[a-z]?[^\)]*\)"


def _extract_numbers(text: str) -> list[str]:
    return re.findall(NUM_PAT, text)


def validate_rewrite(original: str, rewritten: str, constraints: Constraints) -> ValidationResult:
    missing_terms = [t for t in constraints.preserve_terms if t not in rewritten]
    preserve_terms_ok = not missing_terms

    orig_nums = _extract_numbers(original)
    new_nums = _extract_numbers(rewritten)
    preserve_numbers_ok = True
    diff = {}
    if constraints.preserve_numbers and orig_nums != new_nums:
        preserve_numbers_ok = False
        diff = {"original": orig_nums, "rewritten": new_nums}

    l0 = max(len(original), 1)
    change_pct = abs(len(rewritten) - len(original)) * 100 / l0
    length_change_ok = change_pct <= constraints.max_length_change_pct

    risk = "low"
    if not preserve_terms_ok or not preserve_numbers_ok:
        risk = "high"
    elif not length_change_ok:
        risk = "medium"

    # citation safety bump
    if re.findall(CIT_PAT, original) and not all(c in rewritten for c in re.findall(CIT_PAT, original)):
        risk = "high"

    return ValidationResult(
        preserve_terms_ok=preserve_terms_ok,
        preserve_numbers_ok=preserve_numbers_ok,
        length_change_ok=length_change_ok,
        semantic_drift_risk=risk,
        missing_terms=missing_terms,
        number_diff=diff,
    )
