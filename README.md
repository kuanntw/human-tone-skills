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



## 學術領域強化（zh-TW）

已加入一份可直接套用的學術去 AI 味提示模板：

- `templates_human_tone_refiner_prompt_zhTW.md`

此模板特別強化：
- 機械式對稱辯證清洗
- 時序/引文異常提示
- 台灣職場 AL/SSG 詮釋脈絡
- 高頻 AI 詞彙替代建議



## 在各種 AI 工具中的使用方式

以下示範如何在不同 AI 平台中套用本專案（以 `templates_human_tone_refiner_prompt_zhTW.md` 與 `rulepacks/zh/*` 為核心）。

### 1) ChatGPT（自訂 GPT / 一般對話）

- 做法 A（建議）：建立「自訂 GPT」
  1. 將 `templates_human_tone_refiner_prompt_zhTW.md` 內容貼到 Instructions。
  2. 在 Knowledge 或附加檔案中放入：
     - `chinese-human-tone-skill-spec-v1.md`
     - `rulepacks/zh/*.yml`
     - `glossaries/brand_voice_glossary.yml`
  3. 對話時指定：`scenario=academic_paper|social_post|blog_writing|content_marketing|educational_content`。

- 做法 B：一般對話
  1. 先貼上模板（system-like 指令）。
  2. 再貼原文與約束（保留詞、保留數字、長度變化）。

### 2) Claude（Projects）

1. 建立 Project，將下列檔案加入 Project Knowledge：
   - `templates_human_tone_refiner_prompt_zhTW.md`
   - `chinese-human-tone-skill-spec-v1.md`
   - `rulepacks/zh/*.yml`
2. 在 Project Instructions 中要求 Claude 依 Output Schema 輸出：`rewrites/diagnostics/change_log`。
3. 每次任務給定 `scenario` 與 `tone` 參數。

### 3) Gemini（Gem / Notebook）

1. 建立 Gem（或在 NotebookLM / 文件工作流）並貼上模板規則。
2. 上傳規格與 rulepacks 檔案作為參考上下文。
3. 提示詞中固定附上 hard constraints：
   - 不改 B/SE/t/p/R²
   - preserve_terms 必須保留
   - preserve_numbers=true 時數字不可變

### 4) Microsoft Copilot（M365 / Copilot Studio）

1. 在 Copilot Studio 建立 topic 或 prompt action。
2. 將模板放入 system 指令層，並把 `scenario`、`tone`、`constraints` 設為輸入參數。
3. 若接企業知識庫，需先在流程中做「數字與專有名詞保留」校驗。

### 5) API 串接（OpenAI / Anthropic / Gemini API）

建議流程：
1. 先用 `src/humantone/parser.py` 讀取 `rulepacks/zh/*`。
2. 依 `scenario` 選 tone preset（`src/humantone/presets.py`）。
3. 組合 prompt：模板 + 原文 + constraints + glossary。
4. 要求模型輸出 JSON（`rewrites`, `diagnostics`, `change_log`）。
5. 後處理驗證：
   - preserve_terms 全部命中
   - preserve_numbers 檢查
   - semantic drift 風險分級

### 建議統一呼叫格式（貼給任何 AI 都可用）

```text
請使用 Human-Tone Refiner 規則改寫以下中文內容。
scenario: academic_paper
locale: zh-Hant
region: TW
tone: formality=90, warmth=35, confidence=75, directness=65
constraints:
- preserve_terms: ["AL", "SSG", "R²"]
- preserve_numbers: true
- max_length_change_pct: 25
輸出格式：rewrites, diagnostics, change_log
```



## 安裝方式

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pytest
```

## CLI 使用方式

```bash
python -m humantone analyze input.txt --scenario academic_paper --locale zh-Hant --region TW
python -m humantone build-prompt input.txt --scenario academic_paper --mode minimal_edit
python -m humantone validate original.txt rewritten.txt --preserve-numbers
```

## Python API 使用方式

```python
from humantone.schemas import RewriteInput
from humantone.pipeline import run_pipeline

payload = RewriteInput(text="你的文本", scenario="academic_paper")
out = run_pipeline(payload)
print(out.to_dict())
```

## Scenario 說明
- `academic_paper`：博士論文/期刊/摘要，保留嚴謹度與引文數據
- `social_post`：社群貼文，強調自然與節奏
- `blog_writing`：部落格，降低模板轉折
- `content_marketing`：內容行銷，保留賣點但避免浮誇
- `educational_content`：知識教育內容，強調清晰與正確

## academic_paper 使用範例
- 請搭配 `templates/academic_thesis_review_prompt_zhTW.md`
- 模式支援：`diagnose_only`, `minimal_edit`, `paragraph_rewrite`, `reviewer_suggestion`, `human_tone_revision`

## 重要聲明
本專案**不保證通過 AI detector**；目標是降低機械感並維持事實、數字、專有名詞與原意。

## 如何新增 rulepack
1. 在 `rulepacks/zh/` 新增 `.yml` 或 `.json`
2. 每條規則包含：`id/name/pattern|heuristic/severity/domain_applicability/suggestion/examples.before/examples.after`
3. 使用 `load_rulepacks("rulepacks/zh")` 驗證可讀取

## 如何跑測試

```bash
python -m pytest -q
```


## Skill-only 版本（可治理）

本專案提供一般 Skills 形態，不依賴 Python 執行。

目錄：
- `skills/human-tone-zh/SKILL.md`
- `skills/human-tone-zh/SYSTEM_PROMPT.md`
- `skills/human-tone-zh/INPUT_SCHEMA.json`
- `skills/human-tone-zh/OUTPUT_SCHEMA.json`
- `skills/human-tone-zh/RULES.md`
- `skills/human-tone-zh/EXAMPLES.md`
- `governance/CHANGE_POLICY.md`
- `governance/REVIEW_CHECKLIST.md`
- `governance/VERSIONING.md`

說明：
- 以模板 + rulepack + glossary 為核心
- 強制 academic_paper 保留學術嚴謹度
- 不保證通過 AI detector
