# Chinese Human Tone Skill (zh)

將生成式 AI 的中文草稿，改寫為更自然、可讀、符合情境的「人味文字」規格與實作藍圖。  
本專案目前以規格文件為主，核心文件為：

- `chinese-human-tone-skill-spec-v1.md`

---

## 專案目標

- 降低中文 AI 文本的機械感（模板句、節奏單一、抽象詞過密）
- 在不改變事實、數字、專有名詞前提下，提升可讀性與語氣自然度
- 建立可控、可追溯、可測試的「領域化 human-tone」能力

> 非目標：不承諾「100% 通過 AI detector」。

---

## v1 第一批必做領域

1. 學術論文（`academic_paper`）
2. 社群媒體貼文（`social_post`）
3. blog 撰寫（`blog_writing`）
4. 內容行銷（`content_marketing`）
5. 知識教育內容（`educational_content`）

這 5 個領域使用不同的語氣模板、禁用詞、句型偏好與風險門檻。

---

## 規格摘要

### Input（核心欄位）

- `text`：待改寫文本
- `locale`：`zh-Hant` / `zh-Hans`
- `region`：`TW` / `HK` / `CN` / `SG` / `neutral`
- `scenario`：5 個領域枚舉
- `tone`：`formality`, `warmth`, `confidence`, `directness`（0~100）
- `constraints`：
  - `preserve_terms`
  - `preserve_numbers`
  - `max_length_change_pct`
  - `forbidden_styles`

### Output（核心欄位）

- `rewrites[]`：改寫版本（可單版或多版本）
- `diagnostics.ai_trace_signals`：偵測到的 AI 痕跡
- `diagnostics.semantic_drift_risk`：語義偏移風險
- `change_log[]`：改寫說明（可追溯）

---

## 核心流程（Pipeline）

1. **AI 痕跡診斷**：找出模板句、過度排比、轉折濫用等訊號
2. **語氣重塑**：調整句長節奏、主語明確化、領域語域注入
3. **約束校驗**：保留指定詞、保留數字、限制長度變化
4. **風險檢查**：語義偏移與高風險語境（醫療/法律/金融）控管

---

## Humanizer-zh-TW 整合方向

參考專案：<https://github.com/kevintsai1202/Humanizer-zh-TW>

建議整合：

- 將上游詞庫/規則映射到 `diagnostics.ai_trace_signals`
- 建立 `rulepacks/zh/` 分層：
  - `base-ai-trace.yml`
  - `domain-academic.yml`
  - `domain-social.yml`
  - `domain-blog.yml`
  - `domain-marketing.yml`
  - `domain-education.yml`
- 每條規則增加：
  - `severity`（low/medium/high）
  - `domain_applicability`
- 導入前檢查授權並保留 attribution

---

## 驗收標準（MVP）

- 至少 10 筆測試資料（繁中/簡中各 5）
- 5 領域皆覆蓋
- `preserve_terms` 100% 保留
- `preserve_numbers=true` 時數字 100% 保留
- 平均自然度分數 >= 80
- `semantic_drift_risk=high` 比例 < 10%

---

## 專案結構

```text
.
├── README.md
└── chinese-human-tone-skill-spec-v1.md
```

---

## 下一步建議

1. 先實作 rulepack parser（YAML/JSON）
2. 建立 5 領域 tone preset 與 prompt template
3. 加入自動回歸測試（保留詞、數字、語義偏移）
4. 再擴充企業詞庫（brand voice glossary）

