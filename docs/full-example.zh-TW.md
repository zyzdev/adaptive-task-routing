# 完整 Routing 範例

## 1. 提問與第一次 Gate

> 檢查這個 App 啟動很慢的原因，給我改善計畫，先不要實作。請使用 adaptive-task-routing Skill。

AI 先理解任務，形成初步階段：檢查啟動入口與既有計時證據，再提出改善方案。大量讀程式之前，協調入口依序讀取 Context Router 與 Model Router。兩個模式預設都是 `ask`。本例 App 的 Orchestrator 可以建立 Context，但不能切換目前模型或強度。

以下模型名稱是**虛構測試標籤**，不是可安裝的模型或真實推薦。本例 Runtime 回報目前設定 `fixture-balanced`／`medium`，可選模型為 `fixture-fast`、`fixture-balanced`，兩者都支援 `low`、`medium`、`high`。

對話路由判斷最近的需求仍相關，建議留在目前對話。模型路由判斷已知的平衡設定足以進行初步檢查。只需精簡顯示：

```text
【對話設定】
建議：留在目前對話
是否切換視窗：否
最近確認的需求仍有用。

【最低足夠 AI 設定】
Model：fixture-balanced
Reasoning：medium
足以處理範圍明確的檢查。

【建議 AI 設定】
Model：fixture-balanced
Reasoning：medium
升級價值：低；證據尚未指出困難分支，提高設定的幫助有限。
```

接著主要 Agent 執行已授權的檢查；Router 本身不負責檢查 App。

## 2. 交付改善計畫

假設檢查發現初始化過度串行，提出三個相依改動：延後非必要服務、平行讀取獨立資料、加入啟動順序測試。AI 先說明證據與改善方案。

回覆結束前，協調入口辨識出實質**下一階段**：實作並驗證初始化改動。Context 結果仍有效，只重跑 Model Gate。Model Router 從測試環境已確認的選項建議提高強度：

```text
【對話設定】
建議：留在目前對話
是否切換視窗：否
沿用已確定的對話脈絡。

【最低足夠 AI 設定】
Model：fixture-balanced
Reasoning：medium
足以完成已定義的修改與測試。

【建議 AI 設定】
Model：fixture-balanced
Reasoning：high
升級價值：中；額外核對有助於處理初始化順序與回歸互動。

如需採用建議，可在已知的 App 選擇器選擇 high；也可沿用目前設定。目前尚未開始實作。
```

提供建議不等於獲得實作授權。App 選擇器位置未知時，應說明未知，不能捏造精確選單路徑。模型建議不要求使用者回覆特定口令；留在目前對話時不打斷工作。

## 3. 使用者批准下一階段

> 我切成 high 了，開始照計畫實作。

AI 用可取得的 Runtime 資料重檢目前設定；沒有這種資料時，記錄為使用者提供，不能宣稱已獨立驗證。Context 沒有改變就不再重複分析。以簡短模型訊息確認預期組合或回報差異後，依授權開始實作。

如果使用者只問「延後初始化是什麼意思？」，就直接解釋，不開新 Gate，也不開始實作。

## 4. 完成工作

最後要進行困難的 Benchmark 結果解釋時，如果工作需求實質改變，可在解釋之前再評估 Model。交付完整結論且沒有實質下一階段時正常結束；不為了保持 Routing 而憑空提出新任務或新視窗。

## 目前設定未知的變化例

如果宿主既不提供目前設定，也不提供模型清單，Model 結果仍要出現：

```yaml
skill: research-model-router
phase: 建議的實作與驗證階段
current_configuration:
  model: unknown
  reasoning_effort: unknown
  evidence: unavailable
model_catalog:
  availability: unknown
  source: unavailable
  observed_at: unknown
  cache_scope: none
assessment: unverified
minimum_sufficient_setting:
  model: null
  reasoning_effort: null
  availability: unknown
  reason: 沒有適用清單可用來提出受支援的具名組合。
recommended_setting:
  model: null
  reasoning_effort: null
  availability: unknown
upgrade_value: low
upgrade_reason: 更強能力無法補足缺少的候選資料。
confidence: 0.30
mode: ask
disposition: awaiting_user_confirmation
```

這不表示已確認目前模型足夠。沒有適用內建參考的宿主，真正需要選擇設定時可以詢問一次實際選擇器選項。已辨識為 OpenAI 介面且有相符、未過期的內建 Registry 時，則直接給出兩組可用性未驗證的具名建議，不先要求使用者抄寫選單，再把 App 選單或 CLI 指令列為可選操作。只有可選清單時，也不能據此猜測目前使用哪個模型。

## Context 與執行者的變化例

- Context 是 `ask` 且建議 `HANDOFF`：先詢問是否移動。拒絕就留在目前對話；接受後使用可用的 Context 建立操作，無法呼叫時才交給使用者。
- Context 是 `ask` 且目的地模型清單未定：明確顯示 Model Gate 延後，目的地確定後再評估，不能說 Gate 已完成。
- 兩者均 `off`：不評估、不輸出。只有 Model-off 時，不提供模型建議，但 Context Router 仍生效。
- CLI 是 `auto`：逐項確認設定操作可呼叫、已授權且可驗證才執行。互動式指令本身不能證明能力。自動操作失敗一次後提供手動方式。
- App 是 `auto`：已暴露的 Context 操作可以自動執行，切換目前模型或強度等 `user_only` 操作則降級為使用者動作。不能只依 App 名稱決定能力。
