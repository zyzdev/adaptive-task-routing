# Adaptive Task Routing — 使用指南

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

**讓 AI 的額度用在需要的地方，協助減少後續工作的遺漏與返工。**

Adaptive Task Routing 會在下一個重要工作階段開始前，建議是否開啟新對話，以及合適的模型與推理強度，協助你兼顧額度消耗與工作可靠度。

- **減少舊任務對新工作的干擾：**判斷何時應開啟新對話，降低 AI 把上一個任務的假設或限制帶進新工作的機會，減少反覆糾正與返工；需要延續的資訊則整理後交接。
- **減少不必要的消耗：**提供「最低足夠」與「建議」兩組模型及推理設定，說明升級是否值得，避免每個任務都使用最高設定。
- **降低遺漏與返工的風險：**在複雜工作開始前，評估所需的模型能力與推理強度，降低設定不足造成的執行風險。
- **由你決定如何進行：**可以先看建議再決定，也能選擇在平台支援時自動套用設定。

換了主題不代表一定要開新對話；重點是減少無關歷史的干擾，同時保留下一個任務需要的資訊。實際節省與可靠度改善取決於任務及採用的設定。

## 運作方式

1. AI 先提出可執行計畫，或完成你要求的分析與檢查結果。
2. Plugin 評估下一階段：先建議保留或開啟新對話，再提供最低足夠與建議的模型、推理強度，以及升級價值。
3. 預設的 `ask` 模式會等待你的決定；`auto` 模式在平台支援且能驗證時套用設定，無法切換時會說明並沿用目前設定，繼續已授權的工作。

一般問答與微小操作會略過路由，避免增加不必要的判斷與等待。

## 安裝

### Gemini CLI

```bash
gemini extensions install https://github.com/zyzdev/adaptive-task-routing-gemini --ref v0.4.2
```

安裝完成後，請重新啟動 Gemini CLI。

### Claude Code

公開目錄申請正在審查中。在正式上架前，可先複製專用 repository，並以 plugin 目錄啟動 Claude Code：

```bash
git clone --branch v0.4.2 https://github.com/zyzdev/adaptive-task-routing-claude.git
claude --plugin-dir "$PWD/adaptive-task-routing-claude"
```

### ChatGPT 與 Codex

從 [v0.4.2 Release](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.4.2) 下載 `adaptive-task-routing-openai-0.4.2.zip`。若介面支援本機 Plugin，請解壓縮後透過該介面的 Plugin 或 Marketplace 功能加入。公開目錄是否可用仍以 OpenAI 審查結果為準。

## 第一次使用

安裝後開啟新對話，輸入具有一定規模的任務，例如：

> 掃描這個專案的發布流程、跨平台一致性與測試缺口。

AI 應先提供有用的檢查結果或可執行計畫。如果下一階段符合路由條件，接著會顯示 **Adaptive Task Routing** 資源建議，內容包含：

- 是否留在目前對話；
- 最低足夠的模型與推理強度；
- 建議的模型與推理強度；
- 有需要時說明升級價值。

預設的 `ask` 模式會在建議後暫停，等待你自然回覆。你可以先調整設定、要求沿用目前設定，或提出其他做法，不必使用指定的回覆詞。

## 你會看到什麼

以下以「檢查 Plugin 的發布流程、跨平台一致性與測試缺口」為例。實際的計畫與建議會依任務及平台調整。

### 回覆範例

#### 1. AI 的任務計畫

```text
1. 核對發布腳本與三平台 Manifest。
2. 檢查 CI、版本與測試缺口。
3. 整理風險並提出修改順序。
```

#### 2. Adaptive Task Routing 的資源建議

```text
---

### Adaptive Task Routing｜任務資源建議

以下建議是根據上述計畫的下一階段，評估適合的對話環境、模型與推理設定。

【對話設定】
* 建議：留在目前對話
* 是否切換視窗：否
目前對話保留了下一階段需要的需求與證據，因此直接繼續。

【最低足夠 AI 設定】
* Model：GPT-5.6 Sol
* Reasoning：high
足以完成跨檔案核對與一般驗證。

【建議 AI 設定】
* Model：GPT-6 Astra
* Reasoning：high
* 升級價值：中。較適合追蹤跨平台設定之間的隱性關聯。

目前環境無法代為切換模型與推理強度。如需採用建議，可使用介面中的模型與推理強度選單調整；我先停在這裡，等你決定是否調整，或沿用目前設定開始下一階段。
```

`ask` 模式會停在這裡；`auto` 模式只會套用平台支援且能驗證的變更，並可繼續已授權的工作。Gemini 會改用平台原生模型別名，且通常將 Reasoning 顯示為「使用模型預設」。

## 明確啟用

- 支援 Skill 提及的 Codex 介面：`$adaptive-task-routing`
- Claude Code：`/adaptive-task-routing:adaptive-task-routing`
- 其他介面：輸入「開始這項工作前，請使用 adaptive-task-routing Skill。」

## 模式

- `ask`（預設）：顯示建議，並在大量執行前等待使用者回覆。
- `auto`：只套用目前宿主允許且能驗證的變更，然後繼續。
- `off`：略過該 Router。

對話路由與模型路由可分別設定，而且可以直接在 AI 對話中切換，例如：

- 「這個對話的 Adaptive Task Routing 改用 auto。」
- 「模型路由改成 ask。」
- 「這次關閉對話路由。」
- 「目前兩個路由模式是什麼？」

未指定 Router 的 Adaptive Task Routing 模式會同時套用到兩者。AI 會立即確認實際模式與作用範圍，不會為了切換模式另跑一次 Routing 建議。若要跨新對話保留，請明確要求設為預設；宿主沒有可寫入的使用者設定區時，設定只保留在目前對話，AI 會說明這項限制。

## 移除

Gemini CLI：

```bash
gemini extensions uninstall adaptive-task-routing
```

Claude Code 若使用 `--plugin-dir` 啟動，結束該 Session 並刪除複製的目錄即可。ChatGPT 或 Codex 則從原本用來安裝的 Plugin 或 Marketplace 介面停用或移除。

## 疑難排解

- 安裝或更新後，請開啟新對話。
- 確認 Skill 清單包含 `adaptive-task-routing`、`task-context-router` 與 `research-model-router`。
- 沒有出現建議時，可先明確啟用 Skill 測試一次。
- 顯示建議不代表宿主已切換模型或對話；只有通過驗證的自動變更才會回報為已套用。

開發與驗證細節請回到[專案 README](https://github.com/zyzdev/adaptive-task-routing/blob/main/README.zh-TW.md)。
