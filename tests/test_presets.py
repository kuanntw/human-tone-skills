from humantone.presets import TONE_PRESETS, PROMPT_TEMPLATES


def test_five_domain_presets_exist():
    for k in ["academic_paper", "social_post", "blog_writing", "content_marketing", "educational_content"]:
        assert k in TONE_PRESETS
        assert k in PROMPT_TEMPLATES
