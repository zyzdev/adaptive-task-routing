# Gemini coordinator runtime projection

This compact projection is appended both to the generated coordinator Skill and to the extension
startup context. It is the complete runtime contract for the coordinated gate. The startup context
applies it directly for automatic routing, so automatic behavior does not depend on Gemini CLI's
`activate_skill` executor. Do not activate sibling Skills and do not infer rules from memory.

## Sequence

1. Treat substantial multi-step analysis, inspection, audits, scans, research, and planning as
   qualifying work. Complete and present the requested findings or plan first. When that deliverable
   identifies actionable changes, validation, or follow-on research, those actions are the concrete
   substantial next phase even if implementation was not requested. A cross-file release-flow,
   cross-platform consistency, or test-gap scan is not merely informational. If execution is already
   requested, present a concise actionable plan first without starting mutation or substantial execution.
2. Assess conversation placement for the substantial next phase before model choice.
3. Assess minimum-sufficient and recommended Gemini model settings for that next phase. Both
   setting blocks must evaluate the same concrete next phase, not the analysis or planning work
   that has already finished.
4. Render the localized routing note after the requested plan or findings. Begin it with a Markdown
   horizontal rule, a localized level-three `Adaptive Task Routing` resource-guidance heading, and
   one sentence explaining that the following recommendations assess resources for the planned
   next phase.
5. In `ask`, end the note with the applicable model-control and hold paragraph defined below, then
   stop and wait for the user's natural response without requiring a fixed keyword. The note is incomplete if that final paragraph is omitted. In `auto`, apply any callable, authorized and
   verifiable setting, or retain the current setting when switching is unavailable, then continue
   authorized execution.

Both routers default to `ask`. Skip a router only when its mode is explicitly `off`. Reuse a
completed gate for an unchanged phase. Never claim a context or model change unless the host
operation was callable, authorized, performed, and verified.

## Conversation decision

- Stay in the current conversation when it is focused and contains useful requirements or evidence.
  A fresh one-prompt session is focused; task complexity alone is not a reason to switch.
- Switch with a concise handoff when relevant evidence exists but accumulated unrelated history,
  conflicting instructions, or context pressure makes continued work materially less reliable.
- Start clean only when carrying current content is harmful and no task-specific history is needed.

For Traditional Chinese, render exactly this structure with task-specific values and reason:

```text
---

### Adaptive Task Routing｜任務資源建議

以下建議是根據上述計畫的下一階段，評估適合的對話環境、模型與推理設定。

【對話設定】
* 建議：留在目前對話
* 是否切換視窗：否
目前對話保留了完成下一階段所需的需求與證據，因此直接繼續。
```

Never show `CURRENT`, `HANDOFF`, or `CLEAN` in ordinary output.

## Gemini model decision

The bundled Gemini CLI fallback aliases are `Auto`, `Pro`, `Flash`, and `Flash-Lite`. Their actual
backend versions and account availability are runtime-dependent. Use only a live observed option or
one of these aliases. Never output Gemini 1.5. Use `Reasoning: model default`, localized as
`Reasoning：使用模型預設` in Traditional Chinese, unless the current session exposes an exact
configurable `thinkingBudget` or `thinkingLevel`. Never invent Codex-style low, medium, or high
Reasoning values for Gemini.

Choose the minimum setting that can complete the phase reliably, then a recommended setting that
offers meaningful value:

- `Flash-Lite`: narrow extraction, classification, or simple mechanical checks.
- `Flash`: ordinary bounded coding, analysis, validation, and structured review.
- `Pro`: broad cross-file or cross-platform reasoning, architecture, difficult debugging, high-cost
  error review, evidence reconciliation, or final synthesis.
- `Auto`: use only when delegating model choice to Gemini CLI is itself the recommendation.

For substantial cross-platform release, CI, manifest, testing, or supply-chain analysis, use at
least `Flash` and normally recommend `Pro`. Upgrade value is low, medium, or high based on whether
the stronger model is likely to change reliability; localize the value and explain it in one sentence.

For Traditional Chinese, render both blocks exactly in this order:

```text
【最低足夠 AI 設定】
* Model：Flash
* Reasoning：使用模型預設
<one task-specific sentence>

【建議 AI 設定】
* Model：Pro
* Reasoning：使用模型預設
* 升級價值：中。<one task-specific sentence>
```

Omit unreadable current settings, diagnostics, confidence, registry details, and internal schema.

## Model action

Gemini CLI does not expose an agent-callable, verifiable operation for changing the current model
through this Skill. Whenever the recommended model may differ from the current model or the current
model is unreadable, present `/model` as the user control. In Traditional Chinese `ask` mode, the
routing note must end with:

```text
目前環境無法代為切換模型；Reasoning 使用模型預設。如需採用建議，可用 /model 選擇模型；我先停在這裡，等你決定是否調整，或沿用目前設定開始下一階段。
```

Stop after the note in `ask`; the user may respond naturally with a changed setting or a request to
continue with the current one. In `auto`, show `/model` only as an optional control, retain the
current setting and continue authorized work. In another user language, translate the same action
and keep `/model` unchanged.
