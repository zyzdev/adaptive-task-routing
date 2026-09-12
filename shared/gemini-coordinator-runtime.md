# Gemini coordinator runtime projection

This compact projection is appended both to the generated coordinator Skill and to the extension
startup context. It is the complete runtime contract for the coordinated gate. The startup context
applies it directly for automatic routing, so automatic behavior does not depend on Gemini CLI's
`activate_skill` executor. Do not activate sibling Skills and do not infer rules from memory.

## Sequence

Before classifying a task, handle direct conversational mode commands. Users may inspect or set
`ask`, `auto`, or `off` without editing files. A named Context or Model command changes only that
router; an unqualified Adaptive Task Routing mode command changes both independent modes. “This
time” is turn-local, “from now on” is conversation-local, and an explicit default request persists
only through a host/user settings store. When persistence is unavailable, keep it conversation-local
and state that limit. Confirm both effective modes and scope concisely. Do not run routing, model
discovery, or the branded resource note for a mode-only command. A mode change does not authorize
implementation. If the same prompt contains substantial work, apply the mode first and continue
with the sequence below.

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

切換評估：效益尚未確立，暫不自動調整設定。
```

Omit unreadable current settings, diagnostics, confidence, registry details, and internal schema.

## Model action

### Phase continuity and switching value

Route at task boundaries, not every prompt. Reuse the completed gate within an unchanged
phase; reassess after difficult work instead of automatically lowering settings. Optimize
total task cost and reliability over the remaining phase, including retries, rework,
latency, handoff/setup and user corrections; cheap-model turn share is not the objective.
Do not equate API prices with subscription usage or double-count cache processing costs.

Pass the effective context and continuity rationale into this decision. A declined
handoff uses the retained conversation; context-off or model-only uses current placement
without claiming a suitability assessment. Prefer model stickiness when the observed
pair meets the quality floor and continuity has value. A clear capability deficit or
failed validation outweighs cache preservation. A handoff or clean conversation permits
reassessment, but still has setup cost and does not require a different model.

Keep conversation continuity, prompt-cache reuse and switch capability separate. A cache
miss does not erase supplied history, and a retained conversation does not prove a hit.
Switching back may reuse a matching unexpired prefix. Provider, model, prefix, TTL,
tool/thinking compatibility and reasoning-only changes affect reuse under the host's
actual rules. Unknown cache evidence is not zero cost or certain cache loss. Use scoped
official rules or actual usage when available; do not start paid probes or warm caches.
Keep source/time/scope observations session-local and do not persist activity logs.

Keep both task-based setting blocks even when retaining another suitable configuration.
`upgrade_value` compares recommended versus minimum sufficient. Separately record
`switch_assessment` against the observed current pair for that same next phase, with
`switch_value: low | medium | high | unknown`, `decision: retain | change | defer`, and
a reason. The target is `recommended_setting`. Weigh capability/reliability and savings
over remaining work against switching cost and context disruption; use qualitative
judgment unless measured inputs support calculation. If gains do not meaningfully
exceed costs, retain. If the observed pair already matches, retain with low switch value.
Unknown current settings require unknown switch value and deferred automatic switching
while still giving both evidenced task settings. Unknown costs that could reverse the
decision require retention or deferral; a clear quality deficit may justify a change
despite unknown cache cost, with the tradeoff stated. A deferred switch assessment does
not make a completed task recommendation an unresolved destination gate.

In `auto`, only `decision: change` permits a router-initiated configuration change,
still subject to authorized, callable, verifiable operations. For retain or defer, keep
settings and continue authorized work, stating any material quality limitation. Explicit
user requests for a particular setting take precedence without an additional routing
confirmation, but do not create controls. Keep the existing `ask` hold and `off` skip.

After the AI blocks and before the action, add one localized switch-assessment sentence
with a task reason; use `切換評估：` in Traditional Chinese. For uncertain benefit, say
“切換評估：效益尚未確立，暫不自動調整設定。” Do not print unreadable current values or
diagnostic provenance. When retaining or deferring, the action must consistently say
settings are retained; in `ask` wait for a natural choice without instructing a switch.
The manual-switch paragraph below applies only to a justified change or an explicit
user-selected target. Every `ask` note still requires a final action/hold paragraph.

### Manual control when changing

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
