# Adaptive Task Routing for Claude Code

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing 協助 Claude 為下一個實質階段選擇對話環境、模型與推理強度。Claude 會先呈現你要求的發現或計畫，再顯示資源建議。

## 安裝

Claude Code 公開目錄申請正在審查中。正式上架前，可複製公開 repository，並以 Plugin 目錄啟動 Claude Code：

```bash
git clone --branch v0.4.2 https://github.com/zyzdev/adaptive-task-routing-claude.git
claude --plugin-dir "$PWD/adaptive-task-routing-claude"
```

## 第一次使用

開啟新 Session，輸入具有一定規模的任務，例如：

> 稽核這個專案的發布流程，並為主要風險提出實作計畫。

需要明確啟用時，可使用 `/adaptive-task-routing:adaptive-task-routing`。

## 在對話中切換模式

- 「這個對話的 Adaptive Task Routing 改用 auto。」
- 「模型路由改成 ask。」
- 「這次關閉對話路由。」
- 「目前兩個路由模式是什麼？」

未指定 Router 的模式切換會同時套用兩者。預設為 `ask`；`auto` 只套用 Claude 能執行並驗證的變更；`off` 略過指定 Router。

## 你會看到什麼

以下以「檢查 Plugin 的發布流程、跨平台一致性與測試缺口」為例。實際的計畫與建議會依任務及平台調整。

### 回覆範例

#### 1. AI 的任務計畫

```text
1. 檢查發布腳本與 Manifest。
2. 核對 CI 與測試缺口。
3. 整理風險並提出修改順序。
```

#### 2. Adaptive Task Routing 的資源建議

```text
---

### Adaptive Task Routing｜任務資源建議

【對話設定】
* 建議：留在目前對話
* 是否切換視窗：否

【最低足夠 AI 設定】
* Model：Sonnet
* Reasoning：high

【建議 AI 設定】
* Model：Opus
* Reasoning：high
* 升級價值：中。較適合追蹤不易察覺的跨檔案依賴。

目前環境無法代為切換設定。如有需要，可使用 Claude 的模型與推理強度控制；我先停在這裡，等你決定調整或沿用目前設定。
```

模型名稱與強度只是範例；實際建議只使用目前 Claude 環境有依據的選項。`ask` 會停在此區塊；`auto` 可繼續已授權的工作。

## 移除

若透過 `--plugin-dir` 啟動，結束 Claude Code 並刪除複製的目錄即可。公開上架後，Marketplace 使用者可透過 `/plugin` 移除。

驗證與發布細節請參考[開發說明](DEVELOPMENT.md)。正式來源位於[主專案](https://github.com/zyzdev/adaptive-task-routing)。
