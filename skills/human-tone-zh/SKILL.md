# Human Tone zh Skill

## Purpose
將中文文本去 AI 味並保留事實、數字、專有名詞與原意，不承諾通過 AI detector。

## Inputs
- scenario: academic_paper|social_post|blog_writing|content_marketing|educational_content
- locale: zh-Hant|zh-Hans
- region: TW|HK|CN|SG|neutral
- mode: diagnose_only|minimal_edit|paragraph_rewrite|reviewer_suggestion|human_tone_revision
- constraints: preserve_terms, preserve_numbers, max_length_change_pct

## Required Output
必須符合 `skills/human-tone-zh/OUTPUT_SCHEMA.json`。

## Rules
- academic_paper 不口語化
- 保留 citation/數字/H1 H2 H3a/R²/β/p 值
- 降低模板句與過度平滑段落節奏
- 提供作者判斷感與邊界條件
