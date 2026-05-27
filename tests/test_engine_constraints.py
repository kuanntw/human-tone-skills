from humantone.engine import rewrite_text


def test_preserve_terms_no_drop():
    out = rewrite_text("OpenAI 在 2026 推出新功能", "blog_writing", preserve_terms=["OpenAI"], preserve_numbers=True)
    assert "OpenAI" in out["rewrites"][0]["text"]


def test_semantic_drift_risk_flag_when_term_missing():
    out = rewrite_text("這是一段文字", "social_post", preserve_terms=["不存在詞"])
    assert out["diagnostics"]["semantic_drift_risk"] in {"medium", "high", "low"}
