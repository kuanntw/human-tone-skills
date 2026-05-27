from pathlib import Path
from humantone.analyzer import analyze_text


def test_academic_trace_detection():
    text = Path("tests/fixtures/zh_hant_academic_lit_review.txt").read_text(encoding="utf-8")
    signals = analyze_text(text, "academic_paper")
    ids = {s["id"] for s in signals}
    assert "template_transition_overuse" in ids


def test_social_tone_has_parallel_pattern():
    text = Path("tests/fixtures/zh_hant_social.txt").read_text(encoding="utf-8")
    signals = analyze_text(text, "social_post")
    assert any(s["id"] == "parallel_structure_overuse" for s in signals)
