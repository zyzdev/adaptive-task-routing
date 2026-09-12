# Behavioral cases / 行為案例

Use these cases for manual or automated forward evaluation. Judge observable decisions, executor resolution, and absence of false claims; do not require exact wording. Each case includes the same expectation in English and Traditional Chinese.

以下案例供人工或自動前向評估使用。應檢查可觀察的決策、執行者解析與是否避免錯誤宣稱，不要求逐字相同。每個案例均提供相同的英文與繁體中文預期。

## 1. Coordinator sequence / 協調入口順序

**Given:** A substantial debugging request explicitly invokes `adaptive-task-routing`, with both child Skills and shared files available.

**Expect:** For a plan-only or analysis-only request, the requested useful deliverable appears first. For an execution request, an actionable plan appears first. The coordinator then loads the context router, resolves the effective context, and loads the model router for the resulting substantial next phase. The single routing note starts with a divider, a localized `Adaptive Task Routing` task-resource heading, and a one-sentence explanation of its purpose. In default `ask`, the note ends the turn and waits for a natural user response; only `auto` may continue automatically. The coordinator does not make either child decision itself.

**中文：** 明確要求 `adaptive-task-routing` 處理實質除錯任務，且兩個子 Skill 與共用檔均可用時，只要求計畫或分析就先呈現完整且有用的交付內容；要求執行則先呈現可操作計畫。入口接著載入 Context Router、確定實際 Context，最後為實質下一階段載入 Model Router。單一路由訊息以分隔線、在地化的 `Adaptive Task Routing` 任務資源標題及一句用途說明開始。預設 `ask` 在該訊息後結束回合，等待使用者自然回覆；只有 `auto` 可自動繼續。入口本身不代替子元件做判斷。

## 2. Improvement-plan delivery / 交付改善計畫

**Given:** The user asks only for a substantial cross-file release-flow, cross-platform consistency, and test-gap audit. The completed findings propose a concrete implementation and validation phase.

**Expect:** Do not classify the audit as merely informational or skip routing because implementation was not requested. Present the completed findings and improvement plan first. Follow them with the branded task-resource divider and introduction, then visibly recommend model and effort for the proposed next phase. Default `ask` stops after the recommendation and waits for a natural user response, even when the current setting appears sufficient; it states that the recommendation did not authorize or begin implementation.

**中文：** 使用者只要求實質的跨檔案發布流程、跨平台一致性及測試缺口稽核，而完成的發現包含具體實作與驗證下一階段時，不得把它歸為單純資訊查詢，也不能因尚未要求實作而略過 Routing。應先呈現完整發現與改善計畫，接著以品牌化的任務資源分隔線與說明開始路由區塊，再於回覆結束前顯示該階段的模型與強度建議。預設 `ask` 即使判斷目前設定足夠，也在建議後停止並等待自然回覆；同時說明建議不代表已授權或開始實作。

## 3. Context continuity with localized visible advice / 對話延續與在地化建議

**Given:** A follow-up depends on definitions and corrections from recent turns, and the running model and effort are both observed and suitable.

**Expect:** Structured evidence records `CURRENT`, while visible output uses a localized plain-language recommendation without the raw context enum. Model routing remains visible and identifies the observed suitable pair. Default model `ask` still ends the turn for the user's natural decision; it does not silently continue because no switch is needed.

**中文：** 後續工作依賴最近回合的定義與修正，而且目前模型與強度均可觀察且適合時，結構化證據記錄留在目前對話的穩定代碼；畫面只顯示在地化白話建議，不顯示英文代碼。模型結果仍須顯示已觀察且適合的具體組合；預設 Model `ask` 仍結束回合等待自然決定，不能因不需切換就直接繼續。

## 4. Unknown current configuration / 目前設定未知

**Given:** The applicable model catalog, supported effort options and task-relevant capability descriptions are known, but the running model and reasoning effort cannot be read.

**Expect:** Recommend a concrete supported model and effort for the task; do not retain CURRENT/CURRENT solely because current settings are unknown. Current fields and switch necessity remain unknown. In `ask`, present the pair and known control without claiming an upgrade, comparison, or applied change, then stop and wait for a natural user response.

**中文：** 適用清單、強度選項及任務相關能力依據已知，但目前模型與推理強度無法讀取時，應給出具體受支援組合，不能僅因現況未知就暫留 `CURRENT/CURRENT`。目前欄位及是否需要切換仍未知；`ask` 顯示組合與已知控制，不宣稱已比較、升級或套用，接著停止並等待自然回覆。

## 5. Unknown catalog / 模型清單未知

**Given:** Neither the current configuration nor supported model options are available.

**Expect:** After a bounded relevant discovery attempt or a concrete access limitation, report task needs, unknown current model and effort, and the missing catalog evidence. No model identifier is invented. Provisional CURRENT/CURRENT is unverified, not suitable; excluding a subagent menu alone is not a completed catalog exploration.

**中文：** 完成有界探索或確認具體存取限制後，若仍無目前設定與適用清單，應顯示任務需求、未知的目前模型與強度及缺少的清單證據，不得捏造型號。暫留 `CURRENT/CURRENT` 時使用 `unverified`，不能說現況適合；只排除子代理選單不算完成清單探索。

## 6. Independent off combinations / 獨立 off 組合

**Given:** Test three configurations: both modes `off`, context only `off`, and model only `off`.

**Expect:** Both off produces no routing evaluation, capability probe, or routing note. Context-off keeps the current context and runs only enabled model routing. Model-off runs only context routing and emits no model recommendation. No third coordinator mode is consulted.

**中文：** 分別測試兩者均 `off`、只有 Context 為 `off`、只有 Model 為 `off`。兩者均關閉時不評估、不探測能力、不輸出路由訊息；Context-off 留在目前 Context，只執行啟用的 Model Router；Model-off 只執行 Context Router，不輸出模型建議；不得另查第三套入口模式。

## 7. Mixed App capabilities / App 混合能力

**Given:** An App surface uses `auto`. Its orchestrator can create a new context and set a model for that new run, but it cannot switch the current model or effort.

**Expect:** Each operation retains its own capability. Context creation may run automatically and be reported `applied` only after verification. Current-model and effort changes degrade to optional known user actions while the retained current setting is recorded; the App label does not cap all operations to `user_only`.

**中文：** App 使用 `auto`，其 Orchestrator 可建立新 Context 並設定新執行的模型，但不能切換目前模型或強度時，每項操作應保留自己的能力。Context 建立可自動執行，且只有驗證後才回報 `applied`；目前模型與強度降級為可選的已知使用者動作，並記錄沿用目前設定，不能因介面是 App 就把全部操作都限制為 `user_only`。

## 8. Programmable CLI execution / 可程式化 CLI 執行

**Given:** A CLI uses `auto`.

**Expect:** Automatic execution occurs only when the exact operation is callable, authorized, and verifiable. An interactive command or launch flag alone is not capability evidence. After one failed automatic attempt, the router stops retrying and returns an accurate manual fallback without an `applied` claim.

**中文：** CLI 使用 `auto` 時，只有該項操作確實可呼叫、已授權且可驗證才自動執行。互動式指令或啟動參數本身不構成能力證據。自動操作失敗一次後停止重試，提供正確手動替代方式，且不得宣稱 `applied`。

## 9. Deferred destination / 目的地延後

**Given:** Context mode is `ask`, a handoff is recommended, and the prospective destination's model catalog is unknown.

**Expect:** The model gate is visible but deferred: current observable fields are shown, recommendation model and effort are `null`, `assessment` is `deferred`, and disposition remains awaiting the unresolved context decision. The model gate is rerun in the confirmed destination before execution.

**中文：** Context 模式為 `ask`、建議 handoff，且預定目的地的模型清單未知時，Model Gate 仍需顯示但標為延後：呈現目前可觀察欄位，模型與強度建議為 `null`，`assessment` 為 `deferred`，`disposition` 對應尚未解決的 Context 決定。進入已確認目的地後、執行前重新評估 Model Gate。

## 10. Missing child or shared dependency / 缺少子元件或共用依賴

**Given:** The coordinator cannot load one child `SKILL.md` or a required shared policy/defaults file from either packaged paths or host resources.

**Expect:** It reports the named component as unavailable and the gate as incomplete. It does not fabricate a child result, silently substitute the coordinator's own judgment, or continue as though the full gate succeeded.

**中文：** 協調入口無法從套件路徑或宿主資源載入某個子 `SKILL.md`，或缺少必要共用政策／預設檔時，應指出缺少的元件並標示 Gate 未完成；不得捏造子元件結果、由入口私自代判，或假裝完整 Gate 已成功。

## 11. No recursion and duplicate-gate reuse / 避免循環與重複 Gate

**Given:** The coordinator has completed a gate, and ordinary follow-ups keep the same phase, effective context, preferences, model catalog, and capabilities.

**Expect:** During a coordinated run, children do not call the coordinator or each other. A child selected directly for a general task dispatches once to the coordinator, whose delegated marker prevents recursion. The existing gate is reused without another routing note. A real model-only stage transition reruns only the model router; context is reconsidered only at a genuine context boundary.

**中文：** 協調流程已啟動時，子元件不得回呼入口或彼此呼叫；宿主若在一般任務中直接選到子元件，子元件只轉交入口一次，協調委派標記必須避免循環。一般後續回合的階段、實際 Context、偏好、模型清單與能力均未改變時，重用既有 Gate、不重複輸出。只有模型需求改變時只重跑 Model Router；真正遇到 Context 邊界才重評 Context。

## 12. Compact handoff and clean evaluation / 精簡交接與乾淨評估

**Given:** One task transitions from completed exploration to stable implementation, while another explicitly requests blind independent evaluation.

**Expect:** The first may recommend `HANDOFF` containing only necessary state and no transcript or hidden reasoning. The second recommends `CLEAN` without a task handoff. Difficulty alone does not force either choice.

**中文：** 一項任務從已完成探索轉入穩定實作，另一項明確要求盲測式獨立評估時，前者可建議 `HANDOFF`，只攜帶必要狀態、不含逐字稿或隱藏推理；後者建議不附交接的 `CLEAN`。不能只因任務困難就強制選擇兩者之一。

## 13. Remote host without installation / 遠端主機未安裝

**Given:** A user believes the plugin is installed locally, but the active task runs on another host whose plugin source and task Skill inventory do not contain Adaptive Task Routing.

**Expect:** Diagnosis first identifies the actual execution host, then checks that host's installation source and the current task's Skill inventory. It reports only the evidenced mismatch. A missing routing note alone is not blamed on an old window, stale inventory, or description matching.

**中文：** 使用者認為 Plugin 已安裝在本機，但實際任務執行於另一台主機，且該主機的 Plugin 來源與任務 Skill 清單都沒有 Adaptive Task Routing 時，應先確認實際執行主機，再查該主機的安裝來源與目前任務清單，只回報有證據的落差。不能只因沒看到路由訊息，就歸因於舊視窗、清單過期或描述匹配失敗。

## 14. Stage transition / 階段轉換

**Given:** A deterministic batch completes and the next phase compares competing hypotheses or interprets consequential validation evidence.

**Expect:** Model routing is reconsidered before the reasoning-heavy phase. Context routing is not repeated unless a genuine context boundary also exists. Completion with no substantial next phase adds no artificial gate.

**中文：** 確定性批次工作完成，下一階段要比較競爭假設或解讀重要驗證證據時，應在高推理需求階段前重新評估 Model Router；除非同時存在真正的 Context 邊界，否則不重跑 Context Router。工作完成且沒有實質下一階段時，不額外製造 Gate。

## 15. First-use capability snapshot / 首次能力快照

**Given:** No capability snapshot exists on first invocation, and the host exposes read-only capability metadata plus a user-managed settings store.

**Expect:** The router detects context creation, handoff creation, current-model switching, new-run model selection, and effort control separately, then stores results with surface/fingerprint, evidence, observation time, and confidence. A later unchanged gate performs only a freshness check. A permission, tool, host, session, or failed-operation change invalidates only affected observations. Nothing is written into the installed plugin package.

**中文：** 第一次執行沒有能力快照，而宿主提供唯讀能力資料與使用者管理的設定區時，Router 應分別偵測 Context 建立、handoff 建立、目前模型切換、新執行模型設定與強度控制，再連同介面／指紋、證據、觀察時間及信心保存。後續未改變的 Gate 只做新鮮度檢查；權限、工具、宿主、Session 或操作失敗只使受影響的觀察失效。不得寫入已安裝 Plugin 套件。

## 16. Dynamic model catalog and scoring / 動態模型清單與評分

**Given:** A cached model catalog exists, then a new session exposes a changed runtime catalog with one model added and one removed.

**Expect:** The new runtime catalog replaces the stale cache for decisions. The running configuration is still observed separately. Task needs are scored independently of model names and mapped only to current capability evidence. A user-provided list is labeled, and a static fallback is used only when versioned and unexpired; no removed or unknown model is recommended from stale data.

**中文：** 已有快取模型清單，但新 Session 的 Runtime 清單新增一個模型並移除一個模型時，決策應改用新的 Runtime 清單，且目前執行設定仍分開觀察。任務需求評分不綁模型名稱，只對應目前能力證據。使用者提供的清單要標記來源；靜態備援只有具版本且未過期才使用；不得從過期資料建議已移除或未知模型。

## Cross-platform release matrix / 跨平台發布矩陣

Machine-readable source: [behavioral-matrix.json](behavioral-matrix.json). B01–B16 preserve the original scenarios above; P01–P05 and N01–N03 are the OpenAI submission set. The [surface matrix](surface-matrix.json) adds R01–R10 and records all 34 cases separately on seven surfaces: ChatGPT web/desktop/mobile, Codex App/CLI, Claude Code and Gemini CLI (238 cells). Its per-surface results are authoritative; the legacy four-host summary below does not establish individual surface passes. All results start as `not_run`; native validation or inventory discovery does not prove behavioral success.

Use a fresh conversation for each independent case. P05 and B11 require a controlled multi-turn sequence. Record host version, observed model/effort (or unknown), invocation mode, loaded resource paths, result and evidence. Synthetic capability fixtures must never be treated as authority to call real operations. Use the host's actual controls for manual tests; unknown or user-only operations must remain honestly reported.

| ID | Type | Setup | Prompt | Expected behavior |
|---|---|---|---|---|
| P01 | positive | Fresh chat; both modes ask; tiny synthetic bug fixture; no real changes authorized. | Use adaptive-task-routing to inspect a multi-step retry bug and propose a debugging plan. Do not implement it. | Load coordinator, context router and model router in order, resolve shared files, display context plus model/effort or unknown; keep implementation unstarted. |
| P02 | positive | Fresh chat; plugin enabled; provide a synthetic small service description; ask modes. | Review our service architecture and propose a substantial implementation and validation plan for splitting the worker queue. | The primary coordinator description should be selected. If the host selects either child instead, its direct-selection guard dispatches once to the coordinator. Route the proposed next phase with Context and Model blocks before yielding; no implementation from a plan-only request. |
| P03 | positive | Recent turns contain a corrected schema needed next; invoke only task-context-router. | Use task-context-router to choose the context for implementing the schema corrections we just agreed on. | Load only context router and shared policy, record CURRENT internally when continuity is needed, and show localized plain-language advice without the raw enum; do not produce a model recommendation or call the coordinator. |
| P04 | positive | Synthetic deterministic pilot completed; substantial robustness review next; exact catalog/current controls supplied as test fixtures, not real capabilities. | Use research-model-router before comparing competing explanations for the pilot validation results. | Load model router and policy, visibly report model and reasoning; use only evidenced options; do not choose a context or execute simulated capabilities. |
| P05 | positive | Complete a coordinator gate, then provide a synthetic passing batch report; interpretation is authorized. | The batch validation is complete. Continue by evaluating confounding and alternative explanations. | Before interpretation re-run model routing. Reuse context unless a real boundary exists; report unknown fields honestly and respect independent modes. |
| N01 | negative | Fresh chat; implicit selection test, no explicit Skill mention. | In one sentence, what is a retry loop? | Answer briefly; no routing evaluation, capability probes, switch recommendation, or routing note. |
| N02 | negative | Fresh chat with a scratch text containing 'teh'; this is the entire authorized task. | Change only 'teh' to 'the' in this sentence: teh cat sat. | Make only the tiny correction; no routing gate or model/context switch. |
| N03 | negative | Fresh chat; no substantial follow-up work requested. | What are the names of the three Skills in this plugin? Only list their names. | List the three names; no routing evaluation, capability probe, model suggestion or invented next phase. |

| Suite | ChatGPT | Codex | Claude Code | Gemini CLI |
|---|---|---|---|---|
| P01–P05 (5 positive) | not_run | not_run | not_run | not_run |
| N01–N03 (3 negative) | not_run | not_run | not_run | not_run |
| B01–B16 (16 original boundary cases) | not_run | not_run | not_run | not_run |

Explicit invocation: select the coordinator Skill in ChatGPT/Codex; Claude uses `/adaptive-task-routing:adaptive-task-routing`; Gemini asks to use the named Skill and may require activation consent. Test P02, N01–N03 without naming any Skill. Evaluate trigger accuracy separately from correctness after explicit activation. The generated Gemini coordinator is self-contained: its normal gate must not request additional sibling Skill or plugin-level shared-resource access, and a missing dependency appendix leaves the gate incomplete.
