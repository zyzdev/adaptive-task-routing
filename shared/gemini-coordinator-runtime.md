# Gemini coordinator runtime projection

This compact projection is appended to the coordinator in the generated Gemini package because
Gemini CLI grants one activated Skill access to only that Skill directory. It is the complete
runtime contract for the coordinated gate. Do not activate sibling Skills and do not infer rules
from memory.

## Sequence

1. Understand the request and form a lightweight rough plan without broad exploration or execution.
2. Assess conversation placement before model choice.
3. Assess minimum-sufficient and recommended Gemini model settings for the upcoming phase.
4. When work will continue, precede the localized routing note with one brief localized sentence
   stating the understood task and rough approach. Render the routing note and apply the `ask` or
   `auto` action.
5. Put detailed planning, findings, or execution after the routing note. Stop only when a context
   decision or the user's requested scope requires it.

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

## Optional model action

Gemini CLI does not expose an agent-callable, verifiable operation for changing the current model
through this Skill. Whenever the recommended model may differ from the current model or the current
model is unreadable, present `/model` as an option without blocking authorized downstream work. In
Traditional Chinese use:

```text
目前環境無法代為切換模型；Reasoning 使用模型預設。如需採用建議，可用 /model 選擇模型；我會先依目前設定繼續執行。
```

Continue authorized work in the same turn. For a model-advice-only or plan-only request, replace the
continuation clause with the localized equivalent of “you may also keep the current setting.” In
another user language, translate the same action and keep `/model` unchanged.
