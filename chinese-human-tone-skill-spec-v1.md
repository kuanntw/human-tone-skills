# 中文 Human Tone Skill 規格 v1

## 1) 目標與定位

**目標**：將中文生成式 AI 產出的文字，改寫成更自然、可讀、有人味、符合情境的中文內容。  
**非目標**：
- 不承諾「100% 通過所有 AI Detector」。
- 不進行事實捏造、立場篡改、數據改寫。

---

## 2) 支援情境（Scenario）

Skill 必須至少支援以下場景模板：
1. 社群貼文（小紅書/IG/Threads）
2. 內容行銷（SEO 文章、品牌部落格）
3. 商務溝通（Email、提案摘要）
4. 客服回覆（FAQ、工單）
5. 知識型內容（教學文、說明文）

每個場景都要可切換「正式度」與「情緒溫度」。

---


## 2.1) 第一批必做領域（Domain-First）

依產品優先順序，v1 先落地以下 5 個領域：
1. 學術論文（academic_paper）
2. 社群媒體貼文（social_post）
3. Blog 撰寫（blog_writing）
4. 內容行銷（content_marketing）
5. 知識教育內容（educational_content）

> 原則：不同領域使用不同語氣模板、禁用詞、句型偏好與風險門檻，避免「同一套重寫規則套全部」。

## 3) 語言與地區

### 3.1 文字系統
- `zh-Hant`（繁體）
- `zh-Hans`（簡體）

### 3.2 地區風格偏好（可選）
- `TW`：台灣用語
- `HK`：香港用語
- `CN`：中國用語
- `SG`：新加坡中性用語

若未指定，預設使用中性現代中文。

---

## 4) 輸入 / 輸出介面

## 4.1 Input Schema (JSON)

```json
{
  "text": "string, required",
  "locale": "zh-Hant | zh-Hans",
  "region": "TW | HK | CN | SG | neutral",
  "scenario": "academic_paper | social_post | blog_writing | content_marketing | educational_content",
  "tone": {
    "formality": 0,
    "warmth": 0,
    "confidence": 0,
    "directness": 0
  },
  "constraints": {
    "preserve_terms": ["品牌名", "法規詞", "產品型號"],
    "preserve_numbers": true,
    "max_length_change_pct": 30,
    "forbidden_styles": ["過度口語", "浮誇", "網路迷因"]
  },
  "output_mode": "full_rewrite | minimal_edit | multi_variant",
  "variant_count": 3
}
```

> `tone` 四個維度範圍建議 `0~100`。若缺省，預設值：`formality 55 / warmth 60 / confidence 65 / directness 55`。

## 4.2 Output Schema (JSON)

```json
{
  "rewrites": [
    {
      "id": "v1",
      "text": "改寫後文本",
      "style_profile": {
        "formality": 58,
        "warmth": 63,
        "confidence": 67,
        "directness": 54
      },
      "readability_notes": [
        "拆解過長句",
        "減少模板式轉折",
        "補上具體主語"
      ]
    }
  ],
  "diagnostics": {
    "ai_trace_signals": [
      "句式過度整齊",
      "抽象名詞密度過高",
      "重複結論句"
    ],
    "semantic_drift_risk": "low | medium | high",
    "policy_flags": []
  },
  "change_log": [
    "保留品牌名與數字",
    "將 4 個長句改為短句群",
    "刪除 2 段空泛過渡語"
  ]
}
```

---

## 5) 核心流程（Pipeline）

### Step A — AI 痕跡診斷
檢測至少以下訊號：
- 模板開頭/結尾（如「總而言之」「在當今時代」高頻）
- 過度對稱排比
- 空泛抽象詞過密
- 轉折詞濫用（然而、此外、同時）
- 段落節奏單一

### Step B — 語氣重塑
- 優先調整句長與節奏（短-中-短混合）
- 用具體動詞替代空泛名詞化
- 補齊隱性主語，降低機械客觀腔
- 根據 `scenario + tone` 注入語域

### Step C — 約束校驗
- `preserve_terms` 必須完全保留
- 若 `preserve_numbers=true`，數值與單位不可變
- 內容長度變化不得超過 `max_length_change_pct`

### Step D — 風險檢查
- 語義偏移（semantic drift）
- 法規/醫療/金融語境的過度口語化
- 不當承諾語句（如保證、絕對）

---

## 6) 風格控制規則

1. **人味不等於錯字**：禁止刻意加入病句、錯別字。  
2. **資訊優先**：可讀性提升不能犧牲正確性。  
3. **場景一致**：商務語境避免過度網感；社群語境避免公文腔。  
4. **可追溯**：每次改寫需提供 `change_log`。  

---

## 7) 評分 Rubric（0-100）

- Naturalness 自然度（30%）
- Clarity 清晰度（25%）
- Tone Fit 語氣契合（20%）
- Faithfulness 忠實度（20%）
- Safety 安全合規（5%）

### 等級建議
- `90-100`：可直接發布
- `75-89`：小修可發布
- `60-74`：建議再改一輪
- `<60`：重寫

---

## 8) System Prompt（可直接用於 v1）

```text
你是「中文 Human Tone 重寫器」。
任務：把輸入文本改成自然的人類語氣，同時保持原始事實、立場、數據與專有名詞。

硬性規則：
1) 不捏造新事實，不改數字，不改專有名詞。
2) 不要為了像人而加入錯字病句。
3) 根據 scenario、locale、region、tone 調整語域。
4) 若有 preserve_terms，需逐字保留。
5) 先做診斷，再改寫，再輸出 change_log 與風險。

輸出格式：
- rewrites[]
- diagnostics
- change_log

若輸入為高風險領域（醫療/法律/金融）且要求過度口語化，請降低口語強度並在 diagnostics 提醒。
```

---

## 9) MVP 驗收測試（最小集）

至少建立 10 筆測試資料，覆蓋：
- 繁中/簡中各 5 筆
- social/marketing/business/support/educational 各 2 筆
- 每筆含：原文、期望語氣、不可改詞、可接受長度變化

**驗收標準**：
- 100% 保留不可改詞
- 100% 保留數字（在 preserve_numbers=true 時）
- 平均自然度 >= 80
- semantic_drift_risk 為 high 的比例 < 10%

---


## 10) 參考 Humanizer-zh-TW 的整合策略

參考來源：`https://github.com/kevintsai1202/Humanizer-zh-TW`。

### 10.1 可直接整合的規則層
- AI 痕跡規則庫：填充短語、公式化三段式、過度轉折、AI 高頻詞、模糊歸因、宣傳腔。
- 結構規則：避免句式全等、降低「不僅…而且…」與硬湊三點列舉。
- 節奏規則：短中長句混排、段尾多樣化。

### 10.2 詞庫/規則合併方法
1. 建立 `rulepacks/zh/`：
   - `base-ai-trace.yml`（通用去機器味規則）
   - `domain-academic.yml`
   - `domain-social.yml`
   - `domain-blog.yml`
   - `domain-marketing.yml`
   - `domain-education.yml`
2. 將 Humanizer-zh-TW 規則映射到本規格 `diagnostics.ai_trace_signals`，並保留可追溯規則 ID。
3. 對每一條規則增加 `severity`（low/medium/high）和 `domain_applicability`。
4. 衝突時以「忠實度與事實保留」優先，避免過度改寫。

### 10.3 授權與維運
- 導入前確認上游專案授權條款並保留 attribution。
- 建立同步策略：
  - 月度比對上游新增規則
  - 變更需跑回歸測試（保留詞、數字、語義偏移）

## 11) 版本演進建議

### v1.1
- 增加「一句話理由」模式（給編輯快速理解改動）
- 支援 A/B 變體的偏好學習

### v1.2
- 加入企業詞庫（brand voice glossary）
- 針對團隊寫作提供風格一致性報告

