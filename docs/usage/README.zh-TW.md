# Adaptive Task Routing — 使用指南

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing 會協助 AI 判斷大型工作是否應留在目前對話，以及下一階段適合使用哪個模型與推理強度。AI 會先呈現你要求的分析或計畫，再以清楚分隔的區塊顯示資源建議。

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

## 明確啟用

- 支援 Skill 提及的 Codex 介面：`$adaptive-task-routing`
- Claude Code：`/adaptive-task-routing:adaptive-task-routing`
- 其他介面：輸入「開始這項工作前，請使用 adaptive-task-routing Skill。」

## 模式

- `ask`（預設）：顯示建議，並在大量執行前等待使用者回覆。
- `auto`：只套用目前宿主允許且能驗證的變更，然後繼續。
- `off`：略過該 Router。

對話路由與模型路由可分別設定模式。若要更改預設值，請編輯已安裝 Plugin 內的 `shared/defaults.yaml`，再重新啟動宿主。

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

開發與驗證細節請回到[專案 README](../../README.zh-TW.md)。
