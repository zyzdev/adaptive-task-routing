# Adaptive Task Routing for ChatGPT 與 Codex

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing 協助 ChatGPT 與 Codex 為下一個實質階段選擇對話環境、模型與推理強度。AI 會先呈現你要求的發現或計畫，再顯示資源建議。

## 安裝

公開 Plugin 透過 OpenAI Plugins portal 管理。正式上架前，可從[最新版本](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.4.2)下載 `adaptive-task-routing-openai-0.4.2.zip`，解壓縮後將該目錄註冊為本地 Plugin 來源或 Marketplace。

Codex CLI 可從已設定的 Marketplace 安裝；公開上架後，ChatGPT 與 Codex App 可直接從 Plugins Directory 選取。

## 第一次使用

開啟新對話，輸入具有一定規模的任務，例如：

> 稽核這個專案的發布流程，並為主要風險提出實作計畫。

支援具名 Skill 的介面也可使用 `$adaptive-task-routing` 明確啟用。

## 在對話中切換模式

- 「這個對話的 Adaptive Task Routing 改用 auto。」
- 「模型路由改成 ask。」
- 「這次關閉對話路由。」
- 「目前兩個路由模式是什麼？」

未指定 Router 的模式切換會同時套用兩者。預設為 `ask`；`auto` 只套用目前 OpenAI 介面能執行並驗證的變更；`off` 略過指定 Router。

## 你會看到什麼

以下以「檢查 Plugin 的發布流程、跨平台一致性與測試缺口」為例。實際的計畫與建議會依任務及平台調整。

### 回覆範例

#### 1. AI 的任務計畫

```text
1. 檢查發布腳本與 Manifest。
2. 核對 CI 與測試缺口。
```

#### 2. Adaptive Task Routing 的資源建議

```text
---

### Adaptive Task Routing｜任務資源建議

【對話設定】
* 建議：留在目前對話
* 是否切換視窗：否

【最低足夠 AI 設定】
* Model：GPT-5.6 Sol
* Reasoning：high

【建議 AI 設定】
* Model：GPT-6 Astra
* Reasoning：high
* 升級價值：中。較適合追蹤不易察覺的跨檔案依賴。

目前環境無法代為切換設定。如有需要，可使用 ChatGPT 或 Codex App 的模型與推理強度選單，Codex CLI 則可使用 `/model`；我先停在這裡，等你決定調整或沿用目前設定。
```

模型名稱與強度只是範例；實際建議只使用目前 OpenAI 環境有依據的選項。`ask` 會停在此區塊；`auto` 可繼續已授權的工作。

## 移除

可透過 Plugins Directory 或已設定的 Codex Marketplace 移除。若是手動解壓縮的本地版本，請移除 Marketplace 項目並刪除該目錄。

套件、驗證與發布細節請參考[開發說明](DEVELOPMENT.md)。
