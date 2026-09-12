# 共用執行環境路由規範

這是此 Plugin 內所有 Routing Skill 的共同規範。規範由 Skill 載入，不是 Manifest 強制的全域政策。協調入口依序載入兩個獨立 Router；協調流程內的子 Router 不回頭呼叫入口，也不彼此呼叫。宿主若把一般任務直接選到子 Router，子 Router 的直接選取守門規則可只轉交協調入口一次，協調委派標記會阻止循環。只有指令文件並不保證宿主會隱式觸發。

## 分離使用者意圖、環境能力與路由決策

每次分別解析三個層次：

1. `user_policy`：每個 Router 的 `off`、`ask` 或 `auto`。
2. `runtime_capabilities`：目前介面、Session、工具與權限對每一項操作實際能做什麼。
3. `routing_decision`：下一階段適合的 Context 或模型設定。

目前對話本來就有 Context 與模型設定。Router 為 `off`，或啟用後建議不變時，直接使用目前狀態，不需要另外建立固定策略。

## 能力快照與重新偵測

第一次在某環境執行時，先查看宿主或使用者管理的設定區是否已有能力快照。沒有快照、快照過期，或環境指紋不符時，才偵測各項相關操作；宿主提供合適的持久化機制時再記錄結果。

不得把可變觀察寫進已安裝的 Plugin 套件。快照只是快取，不是權威。應記錄足以判斷新鮮度的來源資料：介面、可取得的宿主或 Plugin 版本、工具／能力指紋、觀察時間、證據來源及信心。

每次 Routing Gate 只做輕量的新鮮度檢查。介面、Session、宿主／Plugin 版本、權限、工具或操作結果改變時，只重新偵測受影響的項目。自動操作失敗時立即讓該項能力失效，而且同一 Gate 不重試相同操作。

每一項操作必須分開偵測，不能把整個 App 或 CLI 統一歸為同一執行者：

```yaml
runtime_capabilities:
  surface: identified surface or unknown
  create_new_context: agent | orchestrator | user_only | unavailable | unknown
  create_handoff_context: agent | orchestrator | user_only | unavailable | unknown
  switch_current_model: agent | orchestrator | user_only | unavailable | unknown
  set_model_for_new_run: agent | orchestrator | user_only | unavailable | unknown
  set_reasoning_effort: agent | orchestrator | user_only | unavailable | unknown
  evidence: runtime metadata | user-provided settings | cached observation | unavailable
  observed_at: timestamp | unknown
  confidence: 0.00-1.00
```

同一介面可能具有混合能力。例如 Orchestrator 可以建立新 Context 並指定模型，但切換目前模型或強度仍只能由使用者操作。決策與執行結果都必須保留這項差異。

任務範圍內的唯讀中繼資料查詢可以用來確認能力。互動式指令、可見選擇器或啟動參數，除非 Agent 能呼叫精確操作並驗證結果，否則不算 Agent 能力。未知能力降級為使用者操作。

## 動態模型清單

### 探測範圍與證據

產品、介面／模式、執行宿主與實際 Context 分開辨識。資料不足時按[宿主探測指引](host-discovery.md)只讀適用的平台。對可用的唯讀途徑做有時間限制的探測；遇到權限不足或缺少工具就記錄限制，不繞過。Router 關閉時不探測。

每筆觀察保留 `status`、`source`、`scope`、`observed_at` 及適用性，區分 `not_probed`、`available`、`partial`、`unavailable`、`permission_denied`、`error`、`stale`、`scope_mismatch`。即時設定、最後保存的 thread 設定、磁碟預設與每輪實際執行證據不能混用；現在讀取舊值，不會讓它成為即時值。

探測不授權寫設定、啟動／恢復對話、發送模型提示或安裝 hook。不輸出完整設定、憑證、對話內容或無關 thread 識別。唯讀 helper 不寫使用者設定，但宿主仍可能更新自己的快取／日誌。

### 任務需求與能力依據

即使設定未知，仍交付下一階段能力與相對推理需求；這不是確認目前模型適合。能確認目的地清單時優先使用，並且始終需要能力證據。在已辨識的 OpenAI 介面，Runtime 探測無法完成時，未過期的內建 Registry 可依官方跨介面能力資料直接產生兩組具名建議；帳號可用性仍只在結構化證據標為未驗證，也不能據此觸發或授權切換。Gemini CLI 可使用相符 Registry 中記錄的穩定別名，但後端型號解析與帳號資格仍未驗證。不得先要求使用者抄寫選單才提供適用的備援建議。已知模型但強度清單未知時，可以只建議模型、強度暫留 `CURRENT` 並說明未知。

能力資料先使用 Runtime 描述，不足時按需查精確產品／型號的官方文件並標記推論；官方描述不能建立帳號可用性，API 價格與選項也不等於 App。別名、Auto 與子 Agent 設定不可冒充主對話每輪實際模型。有相關實測時據以校正，沒有時不捏造分數／最優結論。能力參考快取包含產品／模型／來源／日期及期限，預設最多七天，選單或宿主變動時提早更新；不必每個 Gate 上網。

Reasoning 輸出必須使用目的地平台原生設定；相對任務難度本身不是選單值。Gemini CLI 只有在目前 Session 確認可設定時才顯示 `thinkingBudget` 或 `thinkingLevel`，否則顯示「使用模型預設」。不得輸出沒有控制證據的 Codex 式低／中／高，也不得猜測帳號相依別名背後的具體型號。

每次啟用 Model Router 都要分別給出「最低足夠 AI 設定」與「建議 AI 設定」。最低足夠設定是預期能達到本階段品質及驗證要求、成本最低的受支援組合；建議設定則綜合模糊度、錯誤代價、驗證深度、延遲與用量後的最佳價值組合。兩者可以相同。另以 `low`／`medium`／`high` 說明升級價值，並具體指出較高設定可多帶來什麼；兩組相同時升級價值為 `low`。最低設定使用預期能成功的最低強度，只有具體的模糊問題、相依決策、困難核對、高錯誤代價或可有效拆分的工作，才提高建議設定。缺資料、缺歷史、口徑不明或外部瓶頸通常降低升級價值，因為更強模型無法補出證據。

目前執行設定、可用模型清單與模型能力證據是三種不同觀察；模型清單不能證明目前正在使用哪個模型。

模型資料依下列順序取得：

1. 目前 Runtime 中繼資料或可呼叫的宿主模型清單。
2. 使用者提供的選擇器清單，並明確標記為使用者提供。
3. 有版本及有效期限的備援 Registry，而且只有套件或設定明確提供此用途時才使用。

Runtime 模型清單可在目前 Session 或宿主明確定義的短期限內快取，不必在未改變的每個 Gate 重查。新 Session、宿主或清單改變、選擇器不一致、不支援模型錯誤或快取過期時重新整理。不得把快取或備援清單當成模型仍存在的證明。

任務評分準則應保持穩定且不綁模型名稱：難度、模糊度、相依推理、錯誤成本、驗證需求、延遲與運算偏好。再把這些需求對應到目前清單宣告的能力。不得在使用者政策中永久為模型名稱指定分數。只有識別碼、沒有可靠能力資料或仍有效的備援項目時，不捏造排名或具名建議。

## Codex 能力不足時的處理

只使用目前執行環境已提供的能力。Codex helper 成功時，使用完整模型清單，以及它能建立的相符即時目前設定。helper 回報 `codex_state_unwritable` 或 `permission_denied` 時，該次嘗試後就停止，直接改用未過期的內建 Registry；不要為讀取中斷路由、另行要求更大權限。已確認是 ChatGPT 桌面／網頁或 Codex App／CLI 時，可用 Registry 的官方跨介面能力資料產生兩組具名建議；清單是在 CLI 觀察、帳號可用性未驗證等限制只記在結構化證據，不可冒充即時 App 資料。無法讀取的目前欄位不參與建議，也不顯示在精簡結果中；不能因此回答 `CURRENT / CURRENT`，也不能先要求使用者提供選單名稱。

權限升級只用於診斷，不屬於一般推薦流程。使用者質疑建議或明確要求帳號專屬確認時，先說明實際資料來源、相關日期、適用限制與任務映射；接著只有額外權限能解鎖同一介面的 `model/list` 或同等具體唯讀途徑時，才詢問一次最小必要權限。只能查看另一個程序或仍無法接觸目前選單的一般權限不得詢問。使用者拒絕後沿用備援，在環境或明確意圖改變前不重複詢問。

讀取能力與切換能力分開判斷。`ask` 顯示兩組設定及符合目前介面的操作後停止，等待使用者自然決定，不要求固定回覆口令。`auto` 只有在模型及強度操作確實可呼叫、已授權且可驗證時才套用建議；否則把控制列為可選項，沿用目前設定繼續已授權工作。ChatGPT App 與網頁只提示可見的模型與推理強度選單，不顯示 CLI 專用的 `/model`；只有已確認的 Codex CLI 才使用該指令。不能只因讀得到清單就宣稱已切換。

## 解析模式與執行者

- `off`：不評估也不輸出該 Router，沿用目前 Context 或模型設定。
- `ask`：執行評估並顯示兩組設定後停止，即使已知目前設定適合也等待使用者自然回覆。除非使用者明確要求改變，否則沿用目前設定；需要時提供精確的手動操作，但不要求固定回覆口令。使用者要求且可驗證的改變，由 AI 執行可呼叫且已授權的操作。
- `auto`：執行評估，並逐項執行已允許、可呼叫且可驗證的操作。不支援、無法使用或 `user_only` 的項目改列為可選動作，同時沿用目前設定繼續已授權工作。因此混合能力可以產生部分自動結果，但每項結果都必須說明實際發生什麼。

只有觀察到宿主完成該項操作，才能回報 `applied`。使用者直接要求特定宿主操作代表明確授權，但不會憑空產生缺少的能力。

```yaml
execution:
  requested_owner: agent | orchestrator | user | none
  effective_owner: agent | orchestrator | user | none
  status: skipped | awaiting_user_confirmation | awaiting_user_action | applied | retained_current | blocked
  reason: concise explanation
  manual_action: null | concise surface-specific instruction
```

## 偏好與持久化

依序採用：目前回合的明確要求、宿主或使用者層級設定、專案設定、套件預設值。

只保存兩個模式、延遲／成本等使用者偏好，以及附帶來源的快取記錄。不要求第二份固定模型策略；目前對話設定就是備援。沒有設定儲存區時，使用套件預設值與 Session 內觀察，不因無法保存而反覆詢問 onboarding。

## 互動規則

- 先呈現使用者要求的發現或計畫，再顯示 Routing 建議；建議約束的是下一個實質階段，不是為產出計畫已完成的工作。
- Model `ask` 以 Routing 訊息結束該回合，後續執行等待使用者自然回覆；Model `auto` 才依能力套用或沿用設定並繼續。
- 對話路由的穩定代碼只保留在結構化證據；精簡使用者輸出直接使用使用者語言的白話描述，不顯示英文代碼。
- Context 與 Model 的建議對同一個實際目的地均可靠時，合併成一次詢問。
- 目的地模型清單未知時，明確延後 Model Gate，確定 Context 後再評估。
- `off` 不輸出該 Router 的結果；其餘模式每次載入 Model Router 都顯示模型與強度，包括 `CURRENT`、未知與延後。
- 每次啟用都要標示最低足夠設定、建議設定、升級價值及任務理由；不能因目前值未知就縮成一行 `CURRENT / CURRENT`，精簡結果也不顯示無法讀取的目前欄位。
- 診斷來源保留在結構化證據。除非使用者主動詢問，精簡結果不得提及探測、備援／Registry 來源、新鮮度、介面／帳號適用性、無法讀取的目前值、信心分數、內部 assessment 或 mode 名稱，也不要用探索機制解釋推薦理由；只說目前是否已自動套用，或需要使用者操作。ChatGPT App 與網頁提示模型與推理強度選單，不顯示 `/model`；已確認是 Codex CLI 時才提示 `/model`。
- 使用者質疑建議時，說明實際依據與限制。只有權限能解鎖同一介面的模型讀取時才詢問一次；無法改善結果的權限不得詢問。
- 只提供目前介面確實已知的控制方式，不捏造選單名稱或指令。
- 改善計畫附上的建議不代表已授權實作。
- 階段、實際 Context、政策、能力快照與模型清單未改變時，不重複 Gate。
- Routing 不會擴張任務範圍、權限或外部副作用授權。
