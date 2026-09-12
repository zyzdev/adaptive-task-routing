# Adaptive Task Routing

[English](README.md)

Adaptive Task Routing 是跨平台的 Agent Skills Plugin，在高成本或大量消耗 Context 的工作開始前，處理兩個獨立決策：

1. **工作應該在哪個 Context 繼續？** `task-context-router` 建議留在目前對話、攜帶精簡交接移至新 Context，或從乾淨 Context 開始。
2. **下一階段需要多少模型能力？** `research-model-router` 為程式開發、除錯、架構、驗證、研究及分析建議受支援的 Model 與 Reasoning Effort。

兩個 Router 保持獨立。第三個薄型 `adaptive-task-routing` Skill 協調執行順序與結果顯示。三個 Skill 都讀取共用環境政策；協調入口沒有自己的自治模式或決策演算法。

## 為什麼需要它

長時間的 Agentic 工作若全部留在同一段對話，或始終使用最強模型，可能浪費 Context 與運算額度。本專案在理解任務之後、真正執行之前加入 Routing Gate：

```text
理解請求 → 初步計畫 → Context Routing → 確定 Context
→ Model Routing → 確定模型設定 → 執行
```

Plugin 不會因為使用者允許自動操作，就假設宿主環境真的具備操作能力。建議、使用者授權、環境能力與已驗證執行是四個不同狀態。

## 內含 Skills

### `adaptive-task-routing` — 完整流程入口

理解實質任務並形成初步計畫後，協調入口先讀取 Context Router，確定實際工作 Context，再讀取 Model Router。交付改善計畫且提出具體實質下一階段時，也要在回覆結束前給出該階段的建議；只要求計畫不代表授權實作。

簡短解釋、狀態詢問、小修改，以及僅詢問 Plugin 功能時不必自動觸發。後續階段只載入必要的 Router；回答完整且沒有實質下一階段時，不必再加 Routing 訊息。

### `task-context-router`

輸出以下其中一種建議：

- `CURRENT`：留在目前對話。
- `HANDOFF`：攜帶精簡且與任務直接相關的交接內容移至新 Context。
- `CLEAN`：不攜帶任務歷史，獨立開始。

它不選擇模型，也不執行主要任務。

### `research-model-router`

只從目前環境實際支援的選項中，建議 Model 與 Reasoning Effort 組合。判斷因素包括難度、模糊度、錯誤成本、驗證需求、運算成本與研究階段轉換。

它不決定工作 Context，也不執行主要工作。明確的模型專用請求留在本 Skill；宿主若在尚未完成 Context 路由的一般任務中直接選到它，會只轉交協調入口一次。除了 `off`，有足夠依據時每次都顯示具體的最低足夠與建議設定；精簡輸出不顯示無法讀取的目前值或探索診斷。

## 觸發與顯示

需要完整流程時，在宿主的 Skill 選擇器明確選取 **adaptive-task-routing Skill**，或要求：「開始這項工作前，請使用 adaptive-task-routing Skill。」支援 `$` 提及的 Codex 介面可用 `$adaptive-task-routing`；Claude Code 可用 `/adaptive-task-routing:adaptive-task-routing`。兩個 Router 也能各自單獨使用。

隱式選用取決於宿主對 Skill 描述的匹配。安裝 Plugin、選到 Plugin 顯示名稱，或新增共用描述檔，都不會變成常駐 Hook。一般實質任務會優先匹配協調入口；宿主若仍直接選到子 Router，除非使用者明確只要 Context 或 Model，子 Router 會只轉交協調入口一次，協調委派標記會避免循環。元件缺失或目的地未確定時，必須明確回報。

排查漏掉建議時，檢查可用 Skill 清單、實際載入路徑、模式及回覆；不能僅憑沒看到建議就斷定沒載入，也不能只因對話較舊就斷定清單過期。重新安裝後，建議用新任務作為測試邊界。

精簡輸出會跟隨使用者語言。對話路由代碼只保留在內部證據；畫面直接顯示「留在目前對話」等白話建議，不顯示英文代碼。

## 使用者控制模式

兩個 Router 可分別使用三種模式：

| 模式 | 行為 |
|---|---|
| `off` | 完全不執行該 Router。 |
| `ask` | 執行評估；不需改變時直接繼續，建議改變時先詢問使用者是否調整。這是預設值。 |
| `auto` | 執行評估；逐項套用已允許、可呼叫且可驗證的改變，只有無法自動完成的部分才交給使用者。 |

目前對話狀態就是備援，不需要第二份固定策略。`ask` 下拒絕調整就沿用現況。`auto` 代表使用者授權，不代表環境具備能力。能力按操作逐項解析，不能只看介面名稱；例如 App 可能允許 AI 建立 Context，但切換目前模型或強度仍只能由使用者完成。未知控制方式要說明未知，不捏造步驟。

## 環境判斷

第一次使用時，Plugin 先從宿主或使用者管理的設定區讀取能力快照；沒有快照或資料過期時，才偵測缺少的操作並在可持久化時記錄。後續 Gate 只做輕量新鮮度檢查；快取只是提示。介面、Session、權限、工具、宿主、模型清單或操作結果改變時，重新偵測受影響項目。

模型清單是動態資料，且與目前執行設定分開。優先使用 Runtime 資料，再使用明確標記的使用者提供清單，最後才使用有版本與有效期限的備援 Registry。已辨識為 OpenAI 介面但 App 資料無法讀取時，Registry 內有日期的官方跨介面說明仍可直接產生兩組具體建議，不宣稱帳號可用，也不先要求使用者抄寫選單。Runtime 清單可在 Session 或宿主定義的短期限內快取，遇到環境改變、錯誤或過期時更新。任務評分不綁定模型名稱，Plugin 不會永久替特定模型寫死分數。

一般備援流程不要求擴大權限。使用者之後質疑推薦時，Router 才說明資料來源、日期、適用限制與任務判斷；只有最小必要權限確實能查詢同一個 App 或 Session 時才詢問一次。只能查看另一個程序的權限不會被索取；使用者拒絕後沿用備援，不重複打擾。

預設值位於 [`shared/defaults.yaml`](shared/defaults.yaml)，共同規範位於 [`shared/runtime-routing-policy.md`](shared/runtime-routing-policy.md)。

## 單一來源與三平台產物

目前版本為 **0.4.0** 本機發布候選。根目錄 skills/ 與 shared/ 是唯一維護來源。
三個 Skill 名稱維持不變；描述已區分一般任務協調入口，以及 Context-only／Model-only 子 Router。主體與翻譯新增證據範圍與任務需求指引。release.json 統一管理版本與 metadata。

Model Router 先提出任務能力需求，再映射為適用且可選的模型／強度；未知設定不抹去需求建議。官方描述是能力參考，不代表帳號可用，也不是固定排名。
按需讀取[宿主探測指引](shared/host-discovery.md)。Codex 有選用的 Python 3.10+ 唯讀 helper，不做模型推論或設定寫入；CLI 清單、磁碟預設、保存的 thread 設定分開標示，不能冒充 App 即時狀態。Claude／Gemini 使用自己的指引，不呼叫 Codex helper。
helper 不在安裝或 Skill 載入時自動執行，也不是常駐服務或 hook。

| 平台 | 產物根目錄 | Manifest | 安裝 |
|---|---|---|---|
| OpenAI / ChatGPT / Codex | dist/openai/adaptive-task-routing | plugin.json 與 .codex-plugin/plugin.json | [OpenAI 指南](packaging/openai/README.md) |
| Claude Code | dist/claude/adaptive-task-routing | .claude-plugin/plugin.json | [Claude 指南](packaging/claude/README.md) |
| Gemini CLI | dist/gemini/adaptive-task-routing | gemini-extension.json | [Gemini 指南](packaging/gemini/README.md) |

先建置再使用對應產物；來源 repository 根目錄不能直接安裝。ZIP 名稱為
adaptive-task-routing-<平台>-<版本>.zip，Manifest 直接在 ZIP 根層，沒有外包目錄。
只產生三個 ZIP 與 SHA256SUMS；没有第四個 Codex Marketplace ZIP。

## 建置與驗證

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_release.py --source-only
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_release.py
.venv/bin/python scripts/validate_release.py --require-archives
claude plugin validate dist/claude/adaptive-task-routing --strict
gemini extensions validate dist/gemini/adaptive-task-routing
(cd dist && shasum -a 256 -c SHA256SUMS)
```

建置只取明確來源，每次重新產生；舊 dist 保存在 .release-backups/，不會混入新包。
驗證涵蓋相對連結與錨點、版本、frontmatter、觸發保留、共用檔、平台隔離、ZIP 內容與 SHA-256。
發行包不含建置腳本、其他平台 Manifest、MCP 服務或常駐 Hook。

[跨平台行為案例](tests/behavioral-cases.md) 保留原 24 案例，另加 10 個探測案例；包含 OpenAI 送審需要的五個正向、三個負向案例。
[七介面矩陣](tests/surface-matrix.json) 共 238 格：ChatGPT 網頁／桌面／手機、Codex App／CLI、Claude Code 與 Gemini CLI。唯讀探測通過不等於對話驗收或自動切換通過。
結構驗證與本機清單載入不代表行為通過；隱式觸發、帳號模型控制、跨 Skill 讀取權限仍須實測記錄。

## 文件與發布

- [架構](docs/architecture.zh-TW.md)及[完整範例](docs/full-example.zh-TW.md)
- [官方規格核對](docs/platform-specs.md)
- [盤點與回復資訊](docs/inventory.md)
- [驗證結果](docs/release-verification.md)
- [發布及三平台提交步驟](docs/release.md)
- [貢獻指南](CONTRIBUTING.md)、[安全政策](SECURITY.md)、[MIT 授權](LICENSE)

本次僅準備本機產物，沒有建立遠端 repository、push、Release、平台送審或公開上架。
實際發布身分、公開 listing 網址／圖像與行為測試證據由擁有者確認。
