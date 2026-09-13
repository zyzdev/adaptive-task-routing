# 開發說明

[English](DEVELOPMENT.md) · [繁體中文](DEVELOPMENT.zh-TW.md)

[返回使用說明](README.zh-TW.md)

選用的 [Routing Evaluation Harness](docs/evaluation-protocol.md) 可規劃可重現的
重複實驗、匯入觀察結果、比較策略並準備盲評資料。規劃與報告均離線執行；
外部執行器須明確啟用並指定工作數上限。已完成[純本機驗證](docs/evaluation-validation.md)，
使用假資料與假 adapter，尚未執行模型評估；不代表既有宿主驗收案例已通過。
完整格式與操作方式請見協議文件。

## 內含 Skills

### `adaptive-task-routing` — 完整流程入口

協調入口先讓 AI 完成並呈現使用者要求的分析或計畫。若交付內容定義了具體且有份量的下一階段，再依序讀取 Context Router、確定實際工作 Context，並為該階段讀取 Model Router。使用者已要求執行時，也先呈現精簡可執行計畫，再顯示 Routing 建議，尚不開始大量執行。Model `ask` 只確認提議變更或關鍵阻礙；保留與非阻塞的暫緩可繼續已授權工作。Model `auto` 可套用值得、受支援且可驗證的變更。只要求計畫不代表授權實作。

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

三個平台產物現在都包含簡短的宿主原生啟動提醒。Codex 與 Claude Code 使用 `UserPromptSubmit` Plugin hook；Gemini CLI 在重啟後的每個工作階段載入 Extension 的 `GEMINI.md`。提醒要求宿主先呈現使用者要求的分析或計畫，再於下一個實質階段開始前呼叫協調 Skill，並保留 `ask` 只確認變更及所有模式皆須遵守任務授權的界線；它不會複製路由政策，也不會自行執行 Router。Codex 安裝的 hook 首次執行前可能需要一次審查；宿主或管理員仍可停用 hook 或 Extension。只讀取可攜式 Agent Plugins Manifest 的 ChatGPT 介面沒有本機 Prompt hook，因此仍要依賴描述匹配或明確選取 Skill。

需要明確觸發時，可在宿主的 Skill 選擇器選取 **adaptive-task-routing Skill**，或要求：「開始這項工作前，請使用 adaptive-task-routing Skill。」支援 `$` 提及的 Codex 介面可用 `$adaptive-task-routing`；Claude Code 可用 `/adaptive-task-routing:adaptive-task-routing`。一般實質任務仍以協調入口為主；誤選到子 Router 時，除非使用者明確只要 Context 或 Model，子 Router 只會轉交協調入口一次。

排查漏掉建議時，檢查可用 Skill 清單、實際載入路徑、模式及回覆；不能僅憑沒看到建議就斷定沒載入，也不能只因對話較舊就斷定清單過期。重新安裝後，建議用新任務作為測試邊界。

精簡輸出會跟隨使用者語言。對話路由代碼只保留在內部證據；畫面直接顯示「留在目前對話」等白話建議，不顯示英文代碼。

## 環境判斷

第一次使用時，Plugin 先從宿主或使用者管理的設定區讀取能力快照；沒有快照或資料過期時，才偵測缺少的操作並在可持久化時記錄。後續 Gate 只做輕量新鮮度檢查；快取只是提示。介面、Session、權限、工具、宿主、模型清單或操作結果改變時，重新偵測受影響項目。

模型清單是動態資料，且與目前執行設定分開。優先使用 Runtime 資料，再使用明確標記的使用者提供清單，最後才使用有版本與有效期限的備援 Registry。已辨識為 OpenAI 介面但 App 資料無法讀取時，Registry 內有日期的官方跨介面說明仍可直接產生兩組具體建議，不宣稱帳號可用，也不先要求使用者抄寫選單。Gemini CLI 使用自己的穩定模型別名參考，不借用 OpenAI 的強度等級，也不猜測帳號相依的後端型號。Runtime 清單可在 Session 或宿主定義的短期限內快取，遇到環境改變、錯誤或過期時更新。任務評分不綁定模型名稱，Plugin 不會永久替特定模型寫死分數。

一般備援流程不要求擴大權限。使用者之後質疑推薦時，Router 才說明資料來源、日期、適用限制與任務判斷；只有最小必要權限確實能查詢同一個 App 或 Session 時才詢問一次。只能查看另一個程序的權限不會被索取；使用者拒絕後沿用備援，不重複打擾。

預設值位於 [`shared/defaults.yaml`](shared/defaults.yaml)，共同規範位於 [`shared/runtime-routing-policy.md`](shared/runtime-routing-policy.md)。

## 單一來源與三平台產物

目前公開版本為 **0.5.0**。根目錄 skills/ 與 shared/ 是唯一維護來源。
三個 Skill 名稱維持不變；描述已區分一般任務協調入口，以及 Context-only／Model-only 子 Router。主體與翻譯新增證據範圍與任務需求指引。release.json 統一管理版本與 metadata。

Model Router 先提出任務能力需求，再映射為適用且可選的模型／強度；未知設定不抹去需求建議。官方描述是能力參考，不代表帳號可用，也不是固定排名。
按需讀取[宿主探測指引](shared/host-discovery.md)。Codex 有選用的 Python 3.10+ 唯讀 helper，不做模型推論或設定寫入；CLI 清單、磁碟預設、保存的 thread 設定分開標示，不能冒充 App 即時狀態。Claude／Gemini 使用自己的指引，不呼叫 Codex helper。
helper 不在安裝、Skill 載入或啟動提醒時自動執行。啟動 hook 只輸出固定提醒，不執行探測；本專案沒有常駐服務。

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
[七介面矩陣](tests/surface-matrix.json) 共 427 格（61 案例）：ChatGPT 網頁／桌面／手機、Codex App／CLI、Claude Code 與 Gemini CLI。唯讀探測通過不等於對話驗收或自動切換通過。
結構驗證與本機清單載入不代表行為通過；隱式觸發、帳號模型控制，以及 Gemini 單次 coordinator 啟用是否能完整執行，仍須實測記錄。

## 文件與發布

- [架構](docs/architecture.zh-TW.md)及[完整範例](docs/full-example.zh-TW.md)
- [官方規格核對](docs/platform-specs.md)
- [盤點與回復資訊](docs/inventory.md)
- [驗證結果](docs/release-verification.md)
- [發布及三平台提交步驟](docs/release.md)
- [貢獻指南](CONTRIBUTING.md)、[安全政策](SECURITY.md)、[MIT 授權](LICENSE)

[v0.5.0 Release](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.5.0) 已提供三平台安裝包。
[Gemini 專用 repository](https://github.com/zyzdev/adaptive-task-routing-gemini) 已可公開安裝；
[Claude 專用 repository](https://github.com/zyzdev/adaptive-task-routing-claude) 已送交 Claude Code Directory 審查。
OpenAI Directory 是否公開仍以平台審查結果為準。

切換評估新增 S01–S12 驗收素材。任務完成、修正、返工、延遲與整體成本需與靜態契約檢查分開驗證；新增案例在取得宿主證據前維持未執行。
