# Routing interaction and presentation

This is the shared UX contract for both routers and the coordinator. Apply it after their
independent assessments; it does not select models or authorize task execution. Gemini embeds
this contract beside its host-specific runtime projection. Other hosts read this file through
the shared policy. Keep `recommended_setting` as the compatible internal field name; label it
**Task-fit setting** / **任務適配設定** in the UI. This is an evidence-based task recommendation,
not a proven optimum or an instruction to switch now.

## Ask before a change, not after every decision

Resolve interaction separately from the model's `decision: retain | change | defer`:

| Situation | `ask` interaction | Next-phase execution |
| --- | --- | --- |
| Retain, no pending context change or material quality blocker | No routing confirmation | Continue already authorized work |
| Defer, uncertainty does not prevent responsible progress | Explain provisional retention; no routing confirmation | Continue already authorized work with appropriate validation |
| Defer, missing information materially blocks quality or the next action | Ask one concrete question explaining what the answer changes | Wait for the missing decision |
| Justified context/model/effort change | Ask before the proposed change unless already explicitly authorized | Wait for the change decision; after a manual change, revalidate |
| User only requested analysis or a plan | Deliver that work and the relevant advice | Do not start implementation, regardless of mode or switch decision |

Unknown current model metadata alone is not a quality blocker. Assess the next phase's concrete
needs, observed work quality and available validation. An unmet quality floor, unresolved
destination, or missing requirement that prevents responsible progress must not become silent
continuation. Do not ask “keep current?” after deciding to retain. A missing implementation
authorization means the requested deliverable is complete, not that routing needs confirmation.
Do not require a fixed confirmation word. An explicit user-selected setting or acceptance is
already authorization for that setting; do not ask for it again.

`auto` still requires justified, authorized, callable and verifiable operations. A recommendation
is not an applied change. When an operation cannot be performed, explain the practical fallback;
continue in the effective context only if work is authorized and no material blocker remains.
Do not pretend a manual-only handoff occurred. If progress requires the destination, provide the
handoff and wait for the user to resume there. `off` skips that router entirely.

## Compose one action-first routing note

Present the user's requested findings or actionable plan first. Within the routing note, use:
Markdown divider → localized `Adaptive Task Routing` heading → action → one-sentence reason
→ conversation/window answer → useful AI setting → necessary control or next step.
Do not put a second explanation of the plan before the action. Localize all labels and keep
raw enums and internal scores out of ordinary output.

Select the action from the combined effective result, not just the model decision:

- **Keep current / 維持目前設定**: no proposed environment change; claim suitability only
  for enabled components with supporting evidence. Context-off cannot certify the conversation.
- **Keep provisionally / 暫時沿用設定**: uncertainty warrants retaining without certifying
  suitability. Explain the relevant uncertainty briefly, without dumping unreadable model fields.
- **New conversation with handoff / 開新對話並交接**: carry the objective, confirmed facts,
  constraints, decisions, relevant artifacts and next step. Omit failed hypotheses and secrets.
- **Start clean / 開啟全新對話**: explain why prior task context would interfere; do not carry
  a task-history handoff. Supply only the new task's self-contained request when needed.
- **Change setting / 調整 AI 設定**: show the justified target and the next action. Show the
  current pair only when actually observed or supplied by the user.
- **Need your decision / 需要你決定**: a material blocker remains; name it and ask the useful
  question. This is not a synonym for every deferred switch assessment.

A handoff or clean start can also require a model change. Lead with the context action and
include the destination setting when known; otherwise say it will be assessed there. Combine
pending choices only when accurate for the same destination. Never hide an enabled context
result behind model retention. The practical window answer stays visible in compact output:
`是否切換視窗：否` for staying, `是，待你確認` for a proposed change, or `待確認` when unresolved.
Distinguish a recommended window change from one already completed. Omit the entire conversation
assessment and window answer for context-off or an explicit model-only request.

## Compact and detailed

`compact` is the default presentation; `detailed` is available on request. These are presentation
preferences, not extra routing modes. Apply turn/conversation scope like other preferences;
persist a default only through an available host/user settings store, never in the installed
package. Asking for details reuses the current gate and does not authorize work or repeat probing.

- Compact shows the action, reason, enabled conversation/window answer and useful task-fit model
  and native reasoning setting. For a verified keep, the observed current pair can replace the
  task-fit line if showing an alternative would not help the user's decision. Otherwise keep
  the supported task-fit pair visible, including provisional retention. Mark it “not a request
  to switch now” when needed. An unavailable model component is reported, not silently omitted.
- Detailed adds the observed current pair when useful, **Minimum needed / 最低足夠設定**,
  **Task-fit setting / 任務適配設定**, upgrade value and concise comparison rationale. Both task
  settings are still computed and kept in structured evidence even when compact omits them.
- Keep `switch_value`, cache evidence, source/scope and other diagnostic fields internal unless
  diagnostics are explicitly requested. Detailed means more explanation, not hidden reasoning,
  a transcript, or a persistent developer activity log.

Examples below assume both routers are enabled. Replace sample values and reasons with evidence;
do not copy a positive suitability claim into an unknown-baseline result.

```text
---

### Adaptive Task Routing｜任務資源建議

✓ 維持目前設定
目前設定足以完成剩餘核對，切換帶來的改善有限。

對話：留在目前對話；是否切換視窗：否。
目前 AI：<已觀察的模型與原生推理設定>。

不需操作，接著執行已授權的核對。
```

```text
---

### Adaptive Task Routing｜任務資源建議

暫時沿用設定
切換效益尚未確立，先沿用設定完成可驗證的檢查。

對話：留在目前對話；是否切換視窗：否。
任務適配設定：<有依據的模型與原生推理設定>，不代表現在需要切換。

分析與計畫已交付；尚未開始實作。
```

The last sentence depends on authorization: continue authorized work immediately when no pending
decision remains; finish a plan-only deliverable without an artificial routing question. For
change or a material blocker, end with one concrete question or known manual next step instead.
