TONE_PRESETS = {
    "academic_paper": {"formality": 90, "warmth": 35, "confidence": 75, "directness": 65},
    "social_post": {"formality": 40, "warmth": 80, "confidence": 70, "directness": 60},
    "blog_writing": {"formality": 60, "warmth": 70, "confidence": 70, "directness": 60},
    "content_marketing": {"formality": 65, "warmth": 75, "confidence": 78, "directness": 68},
    "educational_content": {"formality": 70, "warmth": 65, "confidence": 72, "directness": 62},
}

PROMPT_TEMPLATES = {
    domain: (
        "你是中文 Human Tone 重寫器。"
        "請針對領域 {domain} 改寫文字，保留事實、數字、專有名詞。"
        "輸出 rewrites, diagnostics, change_log。"
    )
    for domain in TONE_PRESETS
}


ACADEMIC_ZHTW_REFINER = {
    "name": "academic_paper_zhTW",
    "forbidden_lexicons": ["內內嵌於","深度的影響","此區辨","條件性催化","重新賦義","架構下","轉譯為","雙元性","妥善地"],
    "preferred_lexicons": ["根植於","脈絡化","深遠影響","上述區別","情境化調和機制","重新詮釋","在此模型中","轉化為","雙重特質","有效率地"],
}
