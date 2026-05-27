from pathlib import Path
from humantone.schemas import Constraints
from humantone.validator import validate_rewrite


def test_preserve_terms():
    o = "威權型領導影響上下私交關係"
    r = "威權型領導確實影響上下私交關係"
    c = Constraints(preserve_terms=["威權型領導", "上下私交關係"])
    out = validate_rewrite(o, r, c)
    assert out.preserve_terms_ok


def test_preserve_numbers_and_citations_and_hypothesis():
    o = Path("tests/fixtures/zh_hant_academic_method.txt").read_text(encoding="utf-8") + " (Chen, 2021)"
    r = o
    c = Constraints(preserve_numbers=True, preserve_terms=["H1", "H2", "R²"])
    out = validate_rewrite(o, r, c)
    assert out.preserve_numbers_ok
    assert out.preserve_terms_ok


def test_max_length_change_pct():
    o = "短句"
    r = "短句" * 20
    c = Constraints(max_length_change_pct=10)
    out = validate_rewrite(o, r, c)
    assert not out.length_change_ok
